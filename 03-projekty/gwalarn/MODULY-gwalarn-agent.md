# MODULY — Agent Gwalarn

Rozpad na samostatné celky, které jdou postavit a ověřit nezávisle.
Verze 1.0 · srpen 2026

---

## Princip

Každý modul má:

1. **Kontrakt** — co dostane na vstupu, co vrátí na výstupu. Písemně, předem.
2. **Vlastní CLI** — jde spustit z příkazové řádky bez zbytku systému.
3. **Testy** — jednotkové na logiku, ruční ověření na výstup.
4. **Bránu** — seznam podmínek, které musí platit, než se modul prohlásí za hotový.

Moduly se **nespojují dřív, než každý zvlášť projde svou bránou.** Integrace,
při které se ladí dvě neověřené věci naráz, je nejdražší způsob, jak přijít
o víkend.

Jedno repo, oddělené balíčky. Ne deset repozitářů — sdílené typy by se
rozešly během měsíce.

```
gwalarn-agent/
├─ packages/
│  ├─ media/          M1  ffmpeg, běží na Beelinku
│  ├─ store/          M2  R2 + katalog médií
│  ├─ events/         M3  čistá logika, žádné I/O
│  ├─ parse/          M4  text → struktura přes LLM
│  ├─ telegram/       M5  bot, tlačítka, whitelist
│  ├─ generate/       M6  identita + recept + fakta → návrh
│  ├─ publish/        M7  adaptéry FB / IG / web
│  └─ metrics/        M8  sběr a revize
├─ apps/
│  ├─ worker/             Cloudflare Worker, orchestrace
│  └─ runner/             job na Beelinku pro ffmpeg
└─ tests/
```

---

## Kde co běží

| | Cloudflare Worker | Beelink |
|---|---|---|
| M1 media | ✗ ffmpeg tam není | ✓ |
| M2 store | ✓ | ✓ |
| M3 events | ✓ | ✓ |
| M4 parse | ✓ | ✓ |
| M5 telegram | ✓ webhook | — |
| M6 generate | ✓ | ✓ |
| M7 publish | ✓ | — |
| M8 metrics | ✓ cron | — |

Hranice mezi Workerem a Beelinkem vede přesně přes M1. Worker si o video
řekne, runner na Beelinku si úkol vyzvedne a hotový soubor uloží do R2.

---

## M1 · Media — obraz a zvuk do videa

Nejlepší modul na začátek: výstup vidíš očima, chyba je okamžitě zřejmá,
a nepotřebuje ani databázi, ani API klíče.

### Kontrakt

```typescript
type RenderJob =
  | { kind: 'still';    photo: string; audio: string; format: Format }
  | { kind: 'slideshow'; photos: string[]; audio: string;
      secondsPerPhoto?: number; transition?: 'none' | 'fade'; format: Format }
  | { kind: 'waveform'; photo: string; audio: string; format: Format };

type Format = 'square' | 'portrait';   // 1080×1080 | 1080×1350

type RenderResult = {
  path: string;
  durationSec: number;
  width: number; height: number;
  sizeBytes: number;
};
```

### CLI

```bash
media still --photo foto.jpg --audio ukazka.mp3 --format square -o out.mp4
media slideshow --photos "fotky/*.jpg" --audio ukazka.mp3 --seconds 4 -o out.mp4
media waveform --photo foto.jpg --audio ukazka.mp3 -o out.mp4
```

### Kontroly na vstupu

- ffmpeg je v PATH, `ffmpeg -version` projde
- každý vstupní soubor existuje a má nenulovou velikost
- fotky jsou skutečně obrázky (ověřit přes `ffprobe`, ne podle přípony)
- audio obsahuje audio stopu a má známou délku
- u slideshow: aspoň jedna fotka, počet × délka ≈ délka zvuku
- cílový soubor neexistuje, nebo je zadán přepis

### Kontroly na výstupu

- soubor vznikl a má nenulovou velikost
- `ffprobe` potvrdí video i audio stopu
- délka videa odpovídá délce zvuku ±0,5 s
- rozlišení sedí se zvoleným formátem
- `pix_fmt` je `yuv420p` — jinak to část přehrávačů nepřehraje

### Recepty ffmpeg

```bash
# still: statická fotka + zvuk
ffmpeg -loop 1 -i foto.jpg -i ukazka.mp3 \
  -c:v libx264 -tune stillimage -c:a aac -b:a 192k \
  -pix_fmt yuv420p -shortest \
  -vf "scale=1080:1080:force_original_aspect_ratio=increase,crop=1080:1080" \
  out.mp4

# slideshow s prolínáním
ffmpeg -f concat -safe 0 -i seznam.txt -i ukazka.mp3 \
  -vf "scale=1080:1350:force_original_aspect_ratio=increase,crop=1080:1350,fps=30" \
  -c:v libx264 -c:a aac -pix_fmt yuv420p -shortest out.mp4

# waveform přes fotku
ffmpeg -i ukazka.mp3 -i foto.jpg -filter_complex \
  "[1:v]scale=1080:1080,crop=1080:1080[bg]; \
   [0:a]showwaves=s=1080x260:mode=cline:colors=white@0.85[w]; \
   [bg][w]overlay=0:820[v]" \
  -map "[v]" -map 0:a -c:v libx264 -c:a aac -pix_fmt yuv420p -shortest out.mp4
```

### Brána

- [ ] Všechny tři režimy vyprodukují přehratelné video
- [ ] Video nahrané ručně na IG vypadá správně — necropnuté, se zvukem
- [ ] Chybějící soubor skončí hláškou do vteřiny, ne pádem ffmpeg
- [ ] Fotka na výšku i na šířku dá stejně velký výstup

---

## M2 · Store — média a jejich katalog

### Kontrakt

```typescript
interface Store {
  put(file: Buffer, meta: MediaMeta): Promise<MediaRecord>;
  get(id: string): Promise<MediaRecord | null>;
  find(q: { kind?: 'photo'|'audio'|'video'; eventId?: string;
            unusedOnly?: boolean; limit?: number }): Promise<MediaRecord[]>;
  markUsed(id: string): Promise<void>;
}
```

### Kontroly

- popisek je povinný a neprázdný — bez něj je médium k ničemu
- typ souboru se ověřuje z obsahu, ne z přípony
- limit velikosti (fotky do 15 MB, audio do 50 MB)
- `r2_key` je unikátní, nahrání stejného souboru dvakrát se pozná podle hashe

### Brána

- [ ] Nahrání, načtení, vyhledání podle typu i události
- [ ] Médium bez popisku projde odmítnutím
- [ ] Duplicitní soubor se pozná a nenahraje podruhé

---

## M3 · Events — termíny koncertů

Čistá logika, žádné síťové volání. Nejlépe testovatelný modul z celého projektu.

### Kontrakt

```typescript
interface Events {
  create(e: EventInput): Promise<EventRecord>;
  update(id: string, patch: Partial<EventInput>): Promise<EventRecord>;
  remove(id: string): Promise<void>;
  upcoming(limit?: number): Promise<EventRecord[]>;
  inWindow(fromDays: number, toDays: number): Promise<EventRecord[]>;
  findDuplicate(startsAt: number, venue: string): Promise<EventRecord | null>;
}
```

### Kontroly

- datum v budoucnosti, jinak varování (minulé se zadává jen výjimečně)
- **rok se doplňuje na nejbližší budoucí výskyt** — „14.11." v prosinci
  znamená příští rok
- místo neprázdné
- duplicita: stejný den + stejné místo → nabídnout úpravu místo založení
- časová zóna Europe/Prague, ukládat jako UTC timestamp

### Testy

```
"14.11. v prosinci"        → příští rok
"14.11. v lednu"           → letošní rok
"31.2."                    → chyba, neexistující datum
"14.11. 19:30" + duplicita → nalezena
přechod letního času       → správný UTC offset
```

### Brána

- [ ] Jednotkové testy na doplňování roku procházejí
- [ ] Duplicita se pozná
- [ ] Přechod na zimní čas nerozhodí časy koncertů

---

## M4 · Parse — z věty do struktury

### Kontrakt

```typescript
parseEvent(text: string): Promise<{
  parsed: Partial<EventInput>;
  missing: string[];        // co se nepodařilo vyčíst
  confidence: number;
}>;
```

### Kontroly

- odpověď modelu musí být validní JSON podle schématu — jinak jeden retry,
  pak vzdát a poprosit o ruční zadání
- datum se validuje přes M3, ne se věří modelu
- prázdný nebo příliš krátký vstup se odmítne bez volání LLM

### Testy

Sada dvaceti reálných vět, jak by je kapela napsala, s očekávaným výstupem.
Včetně neúplných („koncert v Sokolovně" — chybí datum) a překlepů.

### Brána

- [ ] Osmnáct z dvaceti testovacích vět se rozparsuje správně
- [ ] Neúplný vstup vrátí seznam chybějících polí, ne výmysl
- [ ] Nevalidní odpověď modelu neshodí proces

---

## M5 · Telegram — vstup a schvalování

### Kontrakt

```typescript
interface TelegramIO {
  onCommand(cmd: string, h: Handler): void;
  onVoice(h: (fileId: string) => Promise<void>): void;
  askConfirm(chatId: number, text: string,
             buttons: Button[]): Promise<string>;   // vrátí volbu
  send(chatId: number, text: string, media?: string): Promise<void>;
}
```

### Kontroly

- **whitelist Telegram ID** — jinak do kalendáře píše kdokoli
- ověření podpisu webhooku
- idempotence podle `update_id`, Telegram doručuje opakovaně
- timeout na nezodpovězené potvrzení (24 h → draft vyprší)

### Brána

- [ ] Cizí účet dostane odmítnutí
- [ ] Dvojí doručení stejné zprávy nezaloží dva záznamy
- [ ] Tlačítka fungují i po restartu Workeru

---

## M6 · Generate — návrh textu

### Kontrakt

```typescript
generate(input: {
  recipe: Recipe;
  identity: string;
  event?: EventRecord;
  media?: MediaRecord[];
  recentPosts: string[];      // aby se to neopakovalo
  platform: 'web' | 'facebook' | 'instagram';
}): Promise<{ text: string; usedMediaIds: string[] }>;
```

### Kontroly

- délka výstupu v mezích platformy
- nesmí obsahovat vymyšlené údaje — datum, místo a čas se porovnají
  s `event`, neshoda znamená zahodit a zkusit znovu
- kontrola proti `recentPosts` na doslovné opakování formulací
- zakázaná slova z `identity.md` (klišé) se hlídají programově

### Brána

- [ ] Ze stejné události vzniknou tři různě dlouhé varianty
- [ ] Podvržená událost s chybným datem se chytí
- [ ] Deset generování po sobě nedá desetkrát stejnou první větu

---

## M7 · Publish — adaptéry

Společné rozhraní, tři implementace. Klíčové je, aby šly vyměnit —
Meta API se změní, ne jestli, ale kdy.

```typescript
interface Publisher {
  name: 'facebook' | 'instagram' | 'web';
  validate(post: DraftPost): ValidationResult;   // bez síťového volání
  publish(post: DraftPost): Promise<PublishResult>;
}
```

### Kontroly před odesláním

| Platforma | Co ověřit |
|---|---|
| Instagram | médium povinné · poměr stran v mezích · délka popisku · video ≤ 90 s |
| Facebook | délka textu · odkaz je platná URL |
| Web | slug je unikátní · front matter validní |

### Instagram — specifika

Publikace je dvoukroková: nejdřív se vytvoří container, pak se publikuje.
Mezi tím se čeká na zpracování, u videa i desítky sekund — je potřeba
pollovat stav containeru, ne slepě čekat pevný čas.

### Brána

- [ ] Testovací příspěvek projde na každou platformu zvlášť
- [ ] Nevalidní vstup se zachytí ve `validate()`, bez volání API
- [ ] Vypršelý token dá srozumitelnou hlášku, ne obecnou chybu 400

---

## M8 · Metrics — sběr a revize

### Kontrakt

```typescript
collect(postId: string): Promise<Metrics>;
proposeRecipeUpdate(recipeId: string): Promise<{
  proposal: string; reasoning: string; sampleSize: number;
}>;
```

### Kontroly

- sběr běží po 48 h a po 7 dnech, ne při publikaci
- nedostupný endpoint se zaloguje a zkusí znovu, nezablokuje cron
- návrh nové verze receptu se **nikdy neaplikuje sám**
- při vzorku pod 10 příspěvků se návrh negeneruje a řekne se proč

### Brána

- [ ] Metriky se doplní zpětně u existujícího příspěvku
- [ ] Výpadek API neshodí cron
- [ ] Malý vzorek vrátí odmítnutí místo doporučení

---

## Integrační kroky

Teprve až všechny brány projdou. Každý krok je svislý řez systémem —
funguje od začátku do konce, jen v úzkém rozsahu.

| # | Řez | Zapojené moduly |
|---|---|---|
| I1 | Zadám termín z mobilu, uloží se | M5 → M4 → M3 |
| I2 | Nahraju fotku s popiskem | M5 → M2 |
| I3 | Vygeneruje se návrh, přijde ke schválení | M3 + M2 → M6 → M5 |
| I4 | Schválený text se objeví na webu | M7 (web) |
| I5 | Totéž na FB | M7 (facebook) |
| I6 | Totéž na IG s fotkou | M7 (instagram) |
| I7 | Zvuková ukázka jako video | M1 → M2 → M7 |
| I8 | Metriky se doplní samy | M8 |

Po I4 už má projekt hodnotu i kdyby se dál nepokračovalo. To je dobré
místo na pauzu.

---

## Pořadí stavby

```
M1 media ──┐                      samostatné, nic neblokuje
M3 events ─┤
M2 store ──┘
              ↓
M4 parse ──> M5 telegram ──> I1, I2
              ↓
M6 generate ──> I3
              ↓
M7 publish ──> I4 ──> I5 ──> I6
              ↓
M1 + M7 ──> I7
              ↓
M8 metrics ──> I8
```

M1, M2 a M3 jdou dělat v libovolném pořadí a nezávisle na sobě.
M1 je nejlepší začátek: výsledek je vidět, chyba je zřejmá,
a nepotřebuje žádné přístupy.
