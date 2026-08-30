# Přepisovač audia

Desktopová aplikace: na vstupu URL (YouTube, podcast) nebo lokální soubor,
na výstupu `.txt` a `.srt`.

## Zprovoznění ve VS Code

```powershell
# 1) Rozbalit projekt a otevřít ve VS Code
code C:\Projects\whisper-app

# 2) Virtuální prostředí (v terminálu VS Code)
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Když `py -3.12` nemáš, funguje i `python -m venv .venv` s tvým 3.14 —
faster-whisper na něm běží. Venv je tu hlavně proto, aby ti balíčky
nekolidovaly s globální instalací.

Ve VS Code pak `Ctrl+Shift+P` → *Python: Select Interpreter* → `.venv`.
Spuštění klávesou **F5** (konfigurace *Spustit aplikaci* je připravená).

## Sestavení EXE

```powershell
.\.venv\Scripts\Activate.ps1
.\build.ps1
```

Výsledek je `dist\Prepisovac\Prepisovac.exe`. Celá složka `dist\Prepisovac`
je přenositelná na jiný počítač bez instalace Pythonu — má ale přes 300 MB,
protože nese CTranslate2 a dekodéry.

## Struktura

| Soubor | Účel |
|---|---|
| `src/main.py` | GUI, vlákna, stavový řádek |
| `src/transcriber.py` | wrapper nad faster-whisper, hlášení postupu |
| `src/downloader.py` | stažení audia z URL přes yt-dlp |
| `build.ps1` | sestavení EXE |

## Jak funguje průběžné hlášení

Práce běží ve vlákně na pozadí a posílá zprávy do `queue.Queue`.
GUI ji každých 100 ms vyzvedává (`self.after`) a překlápí do progress baru,
stavového řádku a logu. Proto okno nezamrzne a jde běh kdykoli přerušit —
`threading.Event` se kontroluje u každého segmentu.

Procenta se počítají jako `segment.end / info.duration`, což je poměrně
přesné. Jediná fáze bez procent je první stažení modelu z Hugging Face;
tam se ukazuje jen text ve stavovém řádku.

## Modely

| Model | Velikost | Rychlost na 8 jádrech | Kvalita češtiny |
|---|---|---|---|
| `small` | ~0,5 GB | ~6× realtime | orientační |
| `medium` | ~1,5 GB | ~2–3× realtime | dobrá |
| `large-v3-turbo` | ~1,6 GB | ~2× realtime | velmi dobrá |
| `large-v3` | ~3 GB | ~0,7× realtime | nejlepší |

Pro mluvené slovo v češtině je rozumný kompromis `large-v3-turbo`.
Modely se stahují jednou do `%USERPROFILE%\.cache\huggingface`.

## Známá omezení

- Vlastní jména a odborné termíny whisper komolí — u obsahu o AI čekej
  zkomolené názvy modelů a firem.
- Rozpoznávání mluvčích (diarizace) tu není. Kdybys ho chtěl, přidává se
  přes `pyannote.audio`, což je ale samostatný model a token na Hugging Face.
- yt-dlp se u YouTube občas rozbije po změně na jejich straně; řeší se
  `pip install -U yt-dlp`.
