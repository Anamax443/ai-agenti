# M1 · MEDIA — implementační zadání

Modul pro převod obrazu a zvuku do videa vhodného pro Instagram a Facebook.
Podklad pro Claude Code. Verze 1.0

---

## 1. Co modul dělá

Bere fotky a zvukový soubor, vyrábí z nich MP4. Tři režimy:

| Režim | Vstup | Výsledek |
|---|---|---|
| `still` | 1 fotka + audio | statický obraz po celou dobu zvuku |
| `slideshow` | N fotek + audio | fotky se střídají, volitelně s prolínáním |
| `waveform` | 1 fotka + audio | fotka s vykreslenou zvukovou vlnou přes spodní část |

Modul **nesahá na síť, na databázi ani na R2.** Dostane cesty k souborům,
vrátí cestu k souboru. Nic víc. Ukládání řeší M2.

---

## 2. Technologie

- **TypeScript**, Node ≥ 20, ESM
- CLI přes `commander`
- ffmpeg se volá přes `child_process.spawn` — **ne** přes `exec`,
  kvůli délce výstupu a průběžnému čtení
- testy: `vitest`
- žádná ffmpeg wrapper knihovna. Sestavování argumentů je pole stringů,
  wrapper by jen přidal vrstvu, přes kterou se hůř ladí

### Struktura

```
packages/media/
├─ src/
│  ├─ index.ts          veřejné API
│  ├─ types.ts          re-export ze společných typů + interní
│  ├─ probe.ts          ffprobe: zjištění vlastností souboru
│  ├─ validate.ts       kontroly vstupu
│  ├─ commands.ts       sestavení argumentů ffmpeg (čisté funkce)
│  ├─ render.ts         spuštění ffmpeg, průběh, výsledek
│  ├─ errors.ts         typované chyby
│  └─ cli.ts            rozhraní příkazové řádky
├─ tests/
│  ├─ commands.test.ts  jednotkové, bez ffmpeg
│  ├─ validate.test.ts  jednotkové
│  ├─ render.test.ts    integrační, potřebuje ffmpeg
│  └─ fixtures.ts       generování testovacích souborů
└─ package.json
```

---

## 3. Veřejné API

```typescript
export type Format = 'square' | 'portrait';

export const DIMENSIONS: Record<Format, { w: number; h: number }> = {
  square:   { w: 1080, h: 1080 },
  portrait: { w: 1080, h: 1350 },
};

export type RenderJob =
  | { kind: 'still';     photo: string;    audio: string; format: Format }
  | { kind: 'slideshow'; photos: string[]; audio: string; format: Format;
      secondsPerPhoto?: number;          // výchozí: délka audia / počet fotek
      transition?: 'none' | 'fade' }     // výchozí: 'fade'
  | { kind: 'waveform';  photo: string;    audio: string; format: Format;
      waveColor?: string };              // výchozí: 'white@0.85'

export type RenderOptions = {
  output: string;
  overwrite?: boolean;                   // výchozí: false
  onProgress?: (p: RenderProgress) => void;
  signal?: AbortSignal;                  // přerušení
};

export type RenderProgress = {
  processedSec: number;
  totalSec: number;
  percent: number;                       // 0-100
  speed: number;                         // násobek reálného času
};

export type RenderResult = {
  path: string;
  durationSec: number;
  width: number;
  height: number;
  sizeBytes: number;
  videoCodec: string;
  audioCodec: string;
};

export async function render(
  job: RenderJob,
  opts: RenderOptions
): Promise<RenderResult>;

export async function probe(path: string): Promise<ProbeResult>;
export async function checkEnvironment(): Promise<EnvCheck[]>;
```

---

## 4. Kontroly

### 4.1 Prostředí — `checkEnvironment()`

Volá se na začátku každého `render()` a taky samostatně z CLI.

| Kontrola | Selže když | Hláška |
|---|---|---|
| `ffmpeg` v PATH | `ffmpeg -version` vrátí nenulový kód | jak nainstalovat |
| `ffprobe` v PATH | totéž | většinou přijde s ffmpeg |
| verze ffmpeg ≥ 6 | starší | `xfade` filtr ve starších chybí |
| kodek `libx264` | není v `ffmpeg -encoders` | build bez x264 |
| kodek `aac` | není | totéž |

### 4.2 Vstup — `validate.ts`

Všechno **před** spuštěním ffmpeg. Cílem je, aby chyba přišla do vteřiny.

**Společné:**
- každá cesta existuje (`fs.access`), je soubor, ne složka
- velikost > 0
- výstupní složka existuje a je zapisovatelná
- výstupní soubor neexistuje, nebo `overwrite: true`
- výstupní cesta končí `.mp4`

**Audio:**
- `probe` najde audio stopu
- délka > 0,5 s a < 15 min (delší nemá pro sociální sítě smysl)

**Fotky:**
- `probe` najde video stopu s jedním snímkem, nebo formát v seznamu
  (`mjpeg`, `png`, `webp`) — **přípona se ignoruje**, rozhoduje obsah
- rozlišení ≥ 400 px na kratší straně, jinak varování o kvalitě

**Slideshow navíc:**
- aspoň 1 fotka, nejvýš 30
- při zadaném `secondsPerPhoto`: `photos.length × secondsPerPhoto`
  se nesmí lišit od délky audia o víc než 20 % → jinak varování
  (ne chyba — poslední fotka se prostě ořízne nebo prodlouží)

### 4.3 Výstup

Po doběhnutí ffmpeg, před vrácením výsledku:

- soubor existuje, velikost > 10 kB
- `probe` potvrdí video **i** audio stopu
- délka videa odpovídá délce audia ±0,5 s
- rozlišení přesně odpovídá `DIMENSIONS[format]`
- `pix_fmt` je `yuv420p`

Když kterákoli kontrola selže, **smazat vadný výstup** a vyhodit chybu.
Nedodělaný soubor na disku je horší než žádný.

---

## 5. Sestavení příkazů — `commands.ts`

Čisté funkce: `RenderJob` + rozměry → `string[]`. Žádné I/O, žádné spuštění.
Díky tomu jdou testovat bez ffmpeg.

```typescript
export function buildStillArgs(job, dim, output): string[];
export function buildSlideshowArgs(job, dim, output, audioDur): string[];
export function buildWaveformArgs(job, dim, output): string[];
```

### Škálovací filtr — společný pro všechny režimy

```
scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}
```

Ořezává na střed. Fotka na výšku i na šířku tak dá stejně velký výstup
bez černých pruhů.

### still

```
ffmpeg -loop 1 -i {photo} -i {audio}
  -c:v libx264 -preset medium -tune stillimage -crf 20
  -c:a aac -b:a 192k
  -pix_fmt yuv420p -shortest -r 30
  -vf "{scale}"
  -movflags +faststart
  {output}
```

### slideshow

Bez prolínání přes `concat` demuxer a dočasný seznam:

```
file 'foto1.jpg'
duration 4
file 'foto2.jpg'
duration 4
file 'foto2.jpg'
```

Poslední soubor se uvádí dvakrát — `concat` jinak zkrátí poslední položku.
Seznam se píše do dočasné složky a po doběhnutí maže.

S prolínáním přes `xfade`, řetězeně mezi sousedními vstupy, délka přechodu
0,5 s. U víc než osmi fotek `xfade` znatelně zpomaluje — nad osm fotek
přepnout na `none` a poznamenat to do varování.

### waveform

```
ffmpeg -i {audio} -i {photo} -filter_complex
  "[1:v]{scale}[bg];
   [0:a]showwaves=s={w}x{waveH}:mode=cline:colors={color}:rate=30[w];
   [bg][w]overlay=0:{h}-{waveH}-60[v]"
  -map "[v]" -map 0:a
  -c:v libx264 -crf 20 -c:a aac -b:a 192k
  -pix_fmt yuv420p -shortest -movflags +faststart
  {output}
```

`waveH` = 25 % výšky. Vlna sedí 60 px nad spodním okrajem, aby ji
nepřekryly ovládací prvky přehrávače.

---

## 6. Spuštění a průběh — `render.ts`

```typescript
const proc = spawn('ffmpeg', [...args, '-progress', 'pipe:1', '-nostats']);
```

`-progress pipe:1` posílá na stdout dvojice `klíč=hodnota`. Zajímavé jsou
`out_time_us` a `speed`. Z nich se počítají procenta proti známé délce audia.

- stderr se **celý sbírá do bufferu** — při nenulovém návratovém kódu
  jde posledních 20 řádků do chybové hlášky
- `signal.aborted` → `proc.kill('SIGTERM')`, po 3 s `SIGKILL`,
  smazat rozdělaný výstup, vyhodit `RenderCancelledError`
- `onProgress` se volá nejvýš 5× za sekundu, ne při každém řádku

---

## 7. Chyby — `errors.ts`

Typované třídy, každá s `code` a případnou nápravou:

| Třída | Kdy | `remedy` |
|---|---|---|
| `EnvironmentError` | chybí ffmpeg / kodek | příkaz k instalaci |
| `InputNotFoundError` | soubor neexistuje | cesta, kterou hledal |
| `InvalidMediaError` | soubor není obrázek / audio | co `probe` skutečně našel |
| `OutputExistsError` | cíl existuje, `overwrite` false | `--overwrite` |
| `FfmpegFailedError` | nenulový návratový kód | posledních 20 řádků stderr |
| `OutputValidationError` | výstup neprošel kontrolou | která kontrola |
| `RenderCancelledError` | přerušeno | — |

Žádná chyba nesmí uniknout jako holý `Error` s textem z ffmpeg.

---

## 8. CLI — `cli.ts`

```bash
media check
media still     --photo f.jpg --audio a.mp3 [--format square] -o out.mp4
media slideshow --photos "fotky/*.jpg" --audio a.mp3 [--seconds 4]
                [--transition fade|none] [--format portrait] -o out.mp4
media waveform  --photo f.jpg --audio a.mp3 [--wave-color "white@0.85"] -o out.mp4
media probe     soubor.mp4
```

Společné přepínače: `--overwrite`, `--json`, `--quiet`.

Chování:
- `--photos` přijímá glob, rozbaluje se v kódu (Windows shell to neumí),
  soubory se řadí abecedně
- průběh jako procenta na stderr, přepisovaný řádek
- `--json` vypíše `RenderResult` na stdout a nic jiného — pro volání z runneru
- návratový kód 0 při úspěchu, 1 při chybě, 2 při chybě prostředí

---

## 9. Testy

### 9.1 Fixtures — `tests/fixtures.ts`

**Do repozitáře nepatří binární soubory.** Testovací materiál se generuje
ffmpegem před během testů a maže po nich:

```bash
# testovací obrázky různých poměrů stran
ffmpeg -f lavfi -i "color=c=red:s=1600x900" -frames:v 1 wide.jpg
ffmpeg -f lavfi -i "color=c=blue:s=900x1600" -frames:v 1 tall.jpg
ffmpeg -f lavfi -i "color=c=green:s=200x200" -frames:v 1 tiny.jpg

# testovací zvuk, 6 sekund
ffmpeg -f lavfi -i "sine=frequency=440:duration=6" test.mp3

# poškozený soubor
echo "tohle neni obrazek" > broken.jpg
```

### 9.2 Jednotkové — bez ffmpeg

`commands.test.ts`:
- `buildStillArgs` obsahuje `-loop 1`, `-shortest`, správné rozměry
- škálovací filtr je pro `portrait` jiný než pro `square`
- slideshow s `transition: 'none'` používá `concat`, s `fade` používá `xfade`
- nad 8 fotek se `fade` degraduje na `none`

`validate.test.ts`:
- neexistující cesta → `InputNotFoundError`
- prázdný soubor → `InvalidMediaError`
- výstup bez `.mp4` → chyba
- existující výstup bez `--overwrite` → `OutputExistsError`
- slideshow s 0 fotkami → chyba
- slideshow s 31 fotkami → chyba

### 9.3 Integrační — s ffmpeg

`render.test.ts`, přeskočit když ffmpeg chybí:

| Test | Ověřuje |
|---|---|
| still ze širokoúhlé fotky | výstup 1080×1080, délka 6 s ±0,5 |
| still z fotky na výšku, portrait | výstup 1080×1350 |
| slideshow ze 3 fotek | délka odpovídá audiu, 3 různé barvy ve snímcích |
| slideshow s fade | doběhne, délka sedí |
| waveform | doběhne, má audio i video stopu |
| poškozená fotka | `InvalidMediaError`, ffmpeg se vůbec nespustí |
| přerušení po 1 s | `RenderCancelledError`, na disku nic nezůstane |
| `pix_fmt` výstupu | vždy `yuv420p` |

Kontrola barev ve slideshow: vyříznout snímek v čase 1 s, 3 s a 5 s
(`ffmpeg -ss`) a ověřit převažující barvu. Tak se pozná, že se fotky
skutečně střídají a nezůstala jen první.

---

## 10. Pokyny k implementaci

**Pořadí:**

1. `types.ts`, `errors.ts` — nejdřív tvary, pak chování
2. `probe.ts` + `checkEnvironment()` — vše ostatní na tom stojí
3. `commands.ts` + jednotkové testy — plně testovatelné bez ffmpeg
4. `validate.ts` + jednotkové testy
5. `render.ts` — spuštění, průběh, kontrola výstupu
6. `cli.ts`
7. integrační testy

**Nedělat:**

- žádné čtení z R2, D1 ani ze sítě — modul je čistě lokální
- nesnažit se ffmpeg nahradit knihovnou v čistém JS
- nepřidávat další režimy, dokud tyhle tři neprojdou branou
- nepoužívat `exec` ani `execSync`

**Poznámky:**

- Windows: cesty s mezerami, `spawn` s polem argumentů to řeší samo,
  ale dočasný seznam pro `concat` potřebuje dopředná lomítka
- `-movflags +faststart` je u videa pro web podstatné, jinak se přehrávání
  rozjede až po stažení celého souboru
- `-preset medium` je kompromis; u slideshow s `xfade` je většina času
  stejně ve filtru, ne v kodeku

---

## 11. Brána modulu

- [ ] `media check` na čistém systému bez ffmpeg vrátí srozumitelnou hlášku
- [ ] Všechny tři režimy vyprodukují přehratelné video
- [ ] Fotka na šířku i na výšku dá stejné rozlišení bez černých pruhů
- [ ] Délka videa odpovídá délce zvuku
- [ ] Video ručně nahrané na Instagram vypadá správně a má zvuk
- [ ] Poškozený vstup selže dřív, než se spustí ffmpeg
- [ ] Přerušení nenechá na disku nedodělaný soubor
- [ ] Jednotkové testy běží bez nainstalovaného ffmpeg
- [ ] `--json` vrací strojově čitelný výstup použitelný z runneru
