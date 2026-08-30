# ZADÁNÍ — Přepisovač audia (desktop, Windows)

Verze 1.0 · Autor: Milan Trnka

---

## 1. Účel

Desktopová aplikace, která na vstupu přijme URL (YouTube, podcast, přímý odkaz
na audio) nebo lokální soubor a na výstupu vytvoří textový přepis (`.txt`, `.srt`).

Cílem je nahradit ruční spouštění `whisper-ctranslate2` z konzole, kde není vidět
postup, není jasné, zda proces žije, a chyby mizí ve výpisu.

**Klíčový požadavek: nic se nesmí spustit naslepo.** Každý předpoklad se ověří
předem a uživatel dostane konkrétní hlášku, co chybí a jak to napravit.

---

## 2. Rozsah

### 2.1 Ve scope

- Vstup: URL nebo lokální audio/video soubor
- Volba modelu, jazyka, výstupní složky
- Průběžné hlášení stavu (progress bar + stavový řádek + log)
- Přerušení běhu kdykoli
- Výstup `.txt` a volitelně `.srt`
- Preflight kontrola prostředí před každým během
- Sestavení do EXE

### 2.2 Mimo scope (v1)

- Rozpoznávání mluvčích (diarizace)
- Dávkové zpracování více souborů
- GPU akcelerace
- Editace přepisu v aplikaci
- Sumarizace / extrakce témat přes LLM

---

## 3. Technologie

| Vrstva | Volba | Zdůvodnění |
|---|---|---|
| Jazyk | Python 3.12 | 3.14 je pro tento stack zbytečně čerstvý |
| GUI | tkinter (stdlib) | žádná externí závislost, nehrozí chybějící wheel |
| Přepis | faster-whisper ≥ 1.2 | CTranslate2, na CPU výrazně rychlejší než openai-whisper |
| Stahování | yt-dlp | jediný udržovaný nástroj pro YouTube |
| Balení | PyInstaller (`--onedir`) | `--onefile` rozbaluje 300 MB při každém startu |

Prostředí: virtuální prostředí `.venv` v kořeni projektu. Aplikace se nikdy
neinstaluje do globálního Pythonu.

---

## 4. Struktura projektu

```
whisper-app/
├─ .vscode/
│  ├─ launch.json          spuštění F5
│  └─ settings.json        interpret = .venv
├─ src/
│  ├─ main.py              GUI, orchestrace, fronta zpráv
│  ├─ preflight.py         kontroly prostředí         ← klíčový modul
│  ├─ validators.py        validace uživatelského vstupu
│  ├─ transcriber.py       wrapper nad faster-whisper
│  ├─ downloader.py        stažení audia přes yt-dlp
│  └─ appstate.py          stavový automat, sdílené typy
├─ tests/
│  └─ test_validators.py
├─ requirements.txt
├─ build.ps1
└─ README.md
```

---

## 5. Kontroly prostředí (preflight)

Modul `preflight.py`. Spouští se **při startu aplikace** a znovu **před každým
během**. Vrací seznam nálezů.

### 5.1 Datový model nálezu

```python
@dataclass
class Check:
    id: str            # "python_version", "lib_faster_whisper", ...
    label: str         # co se kontrolovalo, česky
    status: Status     # OK | WARN | FAIL
    detail: str        # co konkrétně bylo nalezeno
    remedy: str = ""   # jak to napravit (příkaz k vložení do konzole)
```

`Status.FAIL` blokuje spuštění. `Status.WARN` jen informuje.

### 5.2 Seznam kontrol

| ID | Co ověřuje | Selže když | Náprava v hlášce |
|---|---|---|---|
| `python_version` | 3.10 ≤ verze < 4.0 | mimo rozsah | doporučit 3.12 |
| `venv_active` | běží ve `.venv` | ne (WARN) | příkaz na aktivaci |
| `lib_faster_whisper` | import + verze ≥ 1.2 | ImportError | `pip install -r requirements.txt` |
| `lib_ctranslate2` | import, načtení nativních DLL | OSError | totéž + poznámka o VC++ redistributable |
| `lib_av` | import (dekódování audia) | ImportError | totéž |
| `lib_yt_dlp` | import + stáří verze | ImportError / verze > 90 dní (WARN) | `pip install -U yt-dlp` |
| `disk_space` | ≥ 5 GB volných na cílovém disku | méně | uvést kolik chybí |
| `ram_free` | ≥ 2 GB volné (podle modelu) | méně | doporučit menší model |
| `hf_reachable` | HTTPS na `huggingface.co`, timeout 5 s | nedostupné, a model není v cache | firewall / proxy |
| `model_cached` | model už je v `%USERPROFILE%\.cache\huggingface` | není (INFO) | upozornit na první stahování |
| `outdir_writable` | zápis testovacího souboru do výstupní složky | selže | oprávnění / jiná složka |
| `ffmpeg` | `ffmpeg` v PATH | není (WARN) | není nutný, PyAV dekóduje sám |

### 5.3 Chování v GUI

- Při startu se výsledek zobrazí v panelu **Stav prostředí** — zelená/žlutá/červená.
- Je-li aspoň jeden `FAIL`, tlačítko *Spustit přepis* je neaktivní.
- Tlačítko *Zkontrolovat znovu* spustí preflight opakovaně.
- Každý nález s nápravou má tlačítko *Kopírovat příkaz*.

---

## 6. Validace vstupu

Modul `validators.py`. Volá se při stisku *Spustit*, před jakoukoli těžkou prací.

### 6.1 Zdroj

```
prázdný řetězec              → "Zadej URL nebo vyber soubor."
začíná http:// nebo https:// → větev URL
jinak                        → větev lokální soubor
```

**Větev URL:**
- syntaktická kontrola přes `urllib.parse` (musí mít schéma a host)
- host není `localhost` ani IP z privátního rozsahu (ochrana proti překlepu)
- žádné síťové volání ve fázi validace — dostupnost řeší až downloader

**Větev soubor:**
- `Path.exists()` — jinak "Soubor neexistuje: {cesta}"
- `Path.is_file()` — jinak "Zadaná cesta je složka."
- velikost > 0 — jinak "Soubor je prázdný."
- přípona v povoleném seznamu (`.mp3 .m4a .wav .ogg .opus .flac .mp4 .mkv .webm`)
  — jinak WARN "Neobvyklá přípona, zkusím to i tak."
- test otevření na čtení — odchytí zamčený soubor i chybějící oprávnění
- kontrola dekódovatelnosti přes PyAV: otevřít kontejner, ověřit, že obsahuje
  audio stopu, a přečíst délku → jinak "Soubor neobsahuje audio stopu."

Délka se rovnou použije pro odhad doby běhu, který se ukáže před startem.

### 6.2 Výstupní složka

- neexistuje → nabídnout vytvoření, ne selhat
- existuje, ale není zapisovatelná → FAIL
- cílový `.txt` už existuje → dotaz *Přepsat / Přejmenovat / Zrušit*

### 6.3 Kombinace model × RAM

Před načtením modelu porovnat požadavek s volnou pamětí:

| Model | Potřeba RAM (int8) |
|---|---|
| `small` | ~1,0 GB |
| `medium` | ~2,0 GB |
| `large-v3-turbo` | ~2,2 GB |
| `large-v3` | ~3,5 GB |

Je-li volné paměti méně než 1,5× požadavek, zobrazit varování s návrhem
menšího modelu. Neblokovat — jen upozornit.

---

## 7. Stavový automat

```
IDLE ──start──> VALIDATING ──ok──> DOWNLOADING ──> LOADING_MODEL ──> TRANSCRIBING ──> WRITING ──> DONE
                     │                   │                │                │             │
                     └── chyba ──────────┴────────────────┴────────────────┴─────────────┴──> ERROR
                                         │                │                │
                                         └── přerušení ───┴────────────────┴──────────────> CANCELLED
```

`DOWNLOADING` se přeskočí u lokálního souboru. Z `DONE`, `ERROR` i `CANCELLED`
vede cesta zpět do `IDLE`.

Ovládací prvky podle stavu:

| Stav | Spustit | Přerušit | Otevřít výsledek |
|---|---|---|---|
| IDLE | aktivní (pokud preflight OK) | — | — |
| VALIDATING … WRITING | — | aktivní | — |
| DONE | aktivní | — | aktivní |
| ERROR / CANCELLED | aktivní | — | — |

---

## 8. Průběžné hlášení

### 8.1 Architektura

Veškerá práce běží ve vlákně na pozadí. Komunikace s GUI výhradně přes
`queue.Queue`. GUI frontu vyzvedává v `self.after(100, ...)`.

**Do widgetů se nesmí sahat z pracovního vlákna** — tkinter to nepřežije.

### 8.2 Typy zpráv

| Typ | Payload | Cíl |
|---|---|---|
| `status` | text | stavový řádek |
| `progress` | 0–100 nebo `None` | progress bar (`None` → indeterminate) |
| `log` | řádek | textové okno |
| `phase` | stav automatu | přepnutí tlačítek |
| `done` | cesta k výstupu | stavový řádek + tlačítko |
| `error` | zpráva + traceback | log + stavový řádek |
| `cancelled` | — | návrat do IDLE |

### 8.3 Co se hlásí v jednotlivých fázích

| Fáze | Stavový řádek | Progress |
|---|---|---|
| Validace | "Ověřuji vstup..." | indeterminate |
| Stahování | "Stahuji audio... 12,4 / 36,2 MB" | z `yt-dlp` hooku |
| Načítání modelu | "Načítám model medium (první spuštění stahuje ~1,5 GB)..." | indeterminate |
| Přepis | "Přepisuji... 8,3 / 41,0 min · zbývá ~12 min" | `segment.end / duration` |
| Zápis | "Ukládám výstup..." | 100 |

Odhad zbývajícího času se počítá z uplynulého času a poměru zpracovaného audia,
klouzavým průměrem přes posledních 10 segmentů.

Do logu se průběžně vypisují přepsané segmenty s časovými značkami — uživatel
hned vidí, jestli whisper chytil správný jazyk.

---

## 9. Přerušení

`threading.Event`, kontrolovaný na těchto místech:

- v progress hooku yt-dlp
- před načtením modelu
- **u každého segmentu v přepisovací smyčce** (hlavní bod)
- před zápisem souboru

Po přerušení: smazat rozpracované dočasné soubory, vrátit se do `IDLE`,
do stavového řádku "Přerušeno uživatelem."

Načtený model zůstává v paměti — příští běh tak nastartuje okamžitě.

---

## 10. Chování při chybách

| Situace | Reakce |
|---|---|
| Chybějící knihovna | zachytit už v preflightu, nespouštět |
| Model se nestáhne (síť) | konkrétní hláška + odkaz na preflight `hf_reachable` |
| yt-dlp selže (změna YouTube) | hláška + návrh `pip install -U yt-dlp` |
| Nedostatek paměti | zachytit `MemoryError`, doporučit menší model |
| Soubor zamčený jiným procesem | zachytit `PermissionError`, uvést název souboru |
| Neznámá výjimka | traceback do logu + do souboru `%LOCALAPPDATA%\Prepisovac\error.log` |

Žádná výjimka nesmí shodit okno. Vše končí v `ERROR`, odkud lze spustit znovu.

---

## 11. Logování

- Do souboru `%LOCALAPPDATA%\Prepisovac\app.log`, rotace po 5 MB, 3 generace
- Úroveň INFO standardně, DEBUG přes přepínač `--debug`
- Logují se: výsledky preflightu, parametry běhu, doba trvání fází, chyby
- Do logu **nepatří** obsah přepisu — jen metadata

---

## 12. Sestavení EXE

```powershell
.\.venv\Scripts\Activate.ps1
.\build.ps1
```

PyInstaller `--onedir --windowed` s `--collect-all` pro `ctranslate2`, `av`,
`faster_whisper`, `tokenizers`, `onnxruntime`, `yt_dlp` — tyto balíčky nesou
nativní DLL nebo datové soubory, které PyInstaller sám nenajde.

Build skript ověří před během:
- aktivní `.venv`
- nainstalovaný PyInstaller
- projdou-li všechny importy (`python -c "import ..."`)

Výsledek: `dist\Prepisovac\` — přenositelná složka, ~350 MB.

---

## 13. Akceptační kritéria

Aplikace je hotová, když projdou všechny tyto scénáře:

1. **Čisté prostředí** — na PC bez nainstalovaných knihoven aplikace nastartuje,
   preflight ukáže červeně chybějící balíčky a nabídne příkaz k instalaci.
   Tlačítko *Spustit* je neaktivní.
2. **Neexistující soubor** — zadání nesmyslné cesty vrátí hlášku do vteřiny,
   bez načítání modelu.
3. **Soubor bez audia** — vybrání textového souboru s příponou `.mp3` skončí
   hláškou "Soubor neobsahuje audio stopu."
4. **Plný disk** — při méně než 5 GB volných preflight varuje.
5. **Lokální mp3, 40 min, model medium** — proběhne, progress bar roste plynule,
   výstup `.txt` obsahuje smysluplný český text.
6. **YouTube URL** — stáhne se audio, přepis proběhne, obojí zůstane ve výstupní složce.
7. **Přerušení v půlce** — tlačítko *Přerušit* zastaví běh do 5 sekund,
   okno zůstane funkční, lze spustit znovu.
8. **Druhý běh** — nestahuje model znovu, začne přepisovat do 3 sekund.
9. **Odpojená síť během stahování** — hláška o chybě sítě, ne pád aplikace.
10. **Existující výstupní soubor** — nabídne se přepsání/přejmenování.

---

## 14. Poznámky k implementaci

- Vlastní jména a odborné termíny whisper v češtině komolí. U obsahu o AI čekej
  zkomolené názvy modelů a firem. Není to chyba aplikace.
- `vad_filter=True` přeskakuje ticho a znatelně zrychluje běh, ale u velmi
  tichých nahrávek může ukrojit začátky vět. Nechat jako volbu.
- Procenta z `segment.end / info.duration` jsou spolehlivá, protože `info.duration`
  se zjistí předem z kontejneru. Jediná fáze bez procent je stahování modelu.
- Model držet v instanci `Transcriber`, ne v lokální proměnné — jinak se
  načítá znovu při každém běhu.
