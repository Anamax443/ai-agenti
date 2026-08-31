# BRIEF — Audio transcriber (desktop, Windows)

Version 1.0 · Author: Milan Trnka · Czech original: [ZADANI-prepisovac.md](ZADANI-prepisovac.md)

> **Status.** This is a design artefact. The transcription core itself is covered by the
> separate repository [mp3totxt](https://github.com/Anamax443/mp3totxt) (a working CLI with
> tests) — but `mp3totxt` does not cover the GUI, downloading from a URL, or preflight. That
> gap is exactly what this brief describes.

---

## 1. Purpose

A desktop application that takes a URL (YouTube, a podcast, a direct link to audio) or a
local file as input, and produces a text transcript (`.txt`, `.srt`) as output.

The aim is to replace running `whisper-ctranslate2` by hand from a console, where progress
is invisible, it is unclear whether the process is alive, and errors disappear into the
output.

**The key requirement: nothing may be started blind.** Every assumption is verified up front
and the user gets a concrete message about what is missing and how to fix it.

---

## 2. Scope

### 2.1 In scope

- Input: a URL or a local audio/video file
- Choice of model, language, output folder
- Continuous status reporting (progress bar + status line + log)
- Interrupting the run at any point
- `.txt` output and optionally `.srt`
- A preflight check of the environment before every run
- Building into an EXE

### 2.2 Out of scope (v1)

- Speaker diarisation
- Batch processing of multiple files
- GPU acceleration
- Editing the transcript inside the application
- Summarisation / topic extraction via an LLM

---

## 3. Technology

| Layer | Choice | Rationale |
|---|---|---|
| Language | Python 3.12 | 3.14 is needlessly fresh for this stack |
| GUI | tkinter (stdlib) | no external dependency, no risk of a missing wheel |
| Transcription | faster-whisper ≥ 1.2 | CTranslate2, markedly faster than openai-whisper on CPU |
| Downloading | yt-dlp | the only maintained tool for YouTube |
| Packaging | PyInstaller (`--onedir`) | `--onefile` unpacks 300 MB on every start |

Environment: a `.venv` virtual environment in the project root. The application is never
installed into the global Python.

---

## 4. Project structure

```
whisper-app/
├─ .vscode/
│  ├─ launch.json          run with F5
│  └─ settings.json        interpreter = .venv
├─ src/
│  ├─ main.py              GUI, orchestration, message queue
│  ├─ preflight.py         environment checks          ← the key module
│  ├─ validators.py        validation of user input
│  ├─ transcriber.py       wrapper around faster-whisper
│  ├─ downloader.py        audio download via yt-dlp
│  └─ appstate.py          state machine, shared types
├─ tests/
│  └─ test_validators.py
├─ requirements.txt
├─ build.ps1
└─ README.md
```

---

## 5. Environment checks (preflight)

The `preflight.py` module. It runs **at application start** and again **before every run**.
It returns a list of findings.

### 5.1 Finding data model

```python
@dataclass
class Check:
    id: str            # "python_version", "lib_faster_whisper", ...
    label: str         # what was checked, in Czech
    status: Status     # OK | WARN | FAIL
    detail: str        # what exactly was found
    remedy: str = ""   # how to fix it (a command to paste into a console)
```

`Status.FAIL` blocks the run. `Status.WARN` only informs.

### 5.2 List of checks

| ID | What it verifies | Fails when | Remedy in the message |
|---|---|---|---|
| `python_version` | 3.10 ≤ version < 4.0 | out of range | recommend 3.12 |
| `venv_active` | running inside `.venv` | no (WARN) | the activation command |
| `lib_faster_whisper` | import + version ≥ 1.2 | ImportError | `pip install -r requirements.txt` |
| `lib_ctranslate2` | import, native DLLs load | OSError | the same + a note about the VC++ redistributable |
| `lib_av` | import (audio decoding) | ImportError | the same |
| `lib_yt_dlp` | import + version age | ImportError / version > 90 days (WARN) | `pip install -U yt-dlp` |
| `disk_space` | ≥ 5 GB free on the target disk | less | state how much is missing |
| `ram_free` | ≥ 2 GB free (depending on the model) | less | recommend a smaller model |
| `hf_reachable` | HTTPS to `huggingface.co`, 5 s timeout | unreachable and the model is not cached | firewall / proxy |
| `model_cached` | the model is already in `%USERPROFILE%\.cache\huggingface` | it is not (INFO) | warn about the first download |
| `outdir_writable` | writing a test file into the output folder | fails | permissions / a different folder |
| `ffmpeg` | `ffmpeg` on PATH | absent (WARN) | not required, PyAV decodes on its own |

### 5.3 Behaviour in the GUI

- At start, the result is shown in an **Environment status** panel — green/amber/red.
- If there is at least one `FAIL`, the *Start transcription* button is disabled.
- The *Check again* button re-runs preflight.
- Every finding with a remedy has a *Copy command* button.

---

## 6. Input validation

The `validators.py` module. Called when *Start* is pressed, before any heavy work.

### 6.1 Source

```
empty string                  → "Enter a URL or select a file."
starts with http:// or https:// → the URL branch
otherwise                     → the local file branch
```

**URL branch:**
- syntactic check via `urllib.parse` (must have a scheme and a host)
- the host is neither `localhost` nor an IP from a private range (protection against a typo)
- no network call during validation — availability is the downloader's problem

**File branch:**
- `Path.exists()` — otherwise “File does not exist: {path}”
- `Path.is_file()` — otherwise “The given path is a folder.”
- size > 0 — otherwise “The file is empty.”
- the extension is on the allowed list (`.mp3 .m4a .wav .ogg .opus .flac .mp4 .mkv .webm`)
  — otherwise WARN “Unusual extension, I will try anyway.”
- a test open for reading — catches a locked file and missing permissions
- a decodability check via PyAV: open the container, verify it has an audio stream, and read
  the duration → otherwise “The file contains no audio stream.”

The duration is then used directly for the run-time estimate shown before the start.

### 6.2 Output folder

- does not exist → offer to create it, do not fail
- exists but is not writable → FAIL
- the target `.txt` already exists → ask *Overwrite / Rename / Cancel*

### 6.3 Model × RAM combination

Before loading the model, compare the requirement against free memory:

| Model | RAM needed (int8) |
|---|---|
| `small` | ~1.0 GB |
| `medium` | ~2.0 GB |
| `large-v3-turbo` | ~2.2 GB |
| `large-v3` | ~3.5 GB |

If free memory is less than 1.5× the requirement, show a warning suggesting a smaller model.
Do not block — only warn.

---

## 7. State machine

```
IDLE ──start──> VALIDATING ──ok──> DOWNLOADING ──> LOADING_MODEL ──> TRANSCRIBING ──> WRITING ──> DONE
                     │                   │                │                │             │
                     └── error ──────────┴────────────────┴────────────────┴─────────────┴──> ERROR
                                         │                │                │
                                         └── interrupt ───┴────────────────┴──────────────> CANCELLED
```

`DOWNLOADING` is skipped for a local file. From `DONE`, `ERROR` and `CANCELLED` there is a
path back to `IDLE`.

Controls by state:

| State | Start | Interrupt | Open result |
|---|---|---|---|
| IDLE | enabled (if preflight is OK) | — | — |
| VALIDATING … WRITING | — | enabled | — |
| DONE | enabled | — | enabled |
| ERROR / CANCELLED | enabled | — | — |

---

## 8. Progress reporting

### 8.1 Architecture

All work runs on a background thread. Communication with the GUI is exclusively through a
`queue.Queue`. The GUI drains the queue in `self.after(100, ...)`.

**Widgets must never be touched from the worker thread** — tkinter will not survive it.

### 8.2 Message types

| Type | Payload | Destination |
|---|---|---|
| `status` | text | the status line |
| `progress` | 0–100 or `None` | the progress bar (`None` → indeterminate) |
| `log` | a line | the text window |
| `phase` | a state-machine state | switching the buttons |
| `done` | path to the output | status line + button |
| `error` | message + traceback | log + status line |
| `cancelled` | — | return to IDLE |

### 8.3 What is reported in each phase

| Phase | Status line | Progress |
|---|---|---|
| Validation | “Checking the input…” | indeterminate |
| Downloading | “Downloading audio… 12.4 / 36.2 MB” | from the `yt-dlp` hook |
| Loading the model | “Loading model medium (the first run downloads ~1.5 GB)…” | indeterminate |
| Transcription | “Transcribing… 8.3 / 41.0 min · ~12 min left” | `segment.end / duration` |
| Writing | “Saving the output…” | 100 |

The remaining-time estimate is computed from elapsed time and the fraction of audio
processed, as a moving average over the last 10 segments.

Transcribed segments with timestamps are written into the log as they arrive — the user
immediately sees whether whisper picked the right language.

---

## 9. Interruption

A `threading.Event`, checked in these places:

- in the yt-dlp progress hook
- before loading the model
- **at every segment in the transcription loop** (the main point)
- before writing the file

After an interruption: delete partial temporary files, return to `IDLE`, and put “Interrupted
by the user.” in the status line.

The loaded model stays in memory — so the next run starts immediately.

---

## 10. Behaviour on errors

| Situation | Reaction |
|---|---|
| Missing library | caught in preflight, do not start |
| The model will not download (network) | a specific message + a pointer to the `hf_reachable` preflight check |
| yt-dlp fails (YouTube changed) | a message + a suggestion of `pip install -U yt-dlp` |
| Out of memory | catch `MemoryError`, recommend a smaller model |
| File locked by another process | catch `PermissionError`, name the file |
| Unknown exception | traceback into the log and into `%LOCALAPPDATA%\Prepisovac\error.log` |

No exception may take the window down. Everything ends in `ERROR`, from which it can be
started again.

---

## 11. Logging

- Into `%LOCALAPPDATA%\Prepisovac\app.log`, rotated at 5 MB, 3 generations
- Level INFO by default, DEBUG via the `--debug` switch
- Logged: preflight results, run parameters, phase durations, errors
- What does **not** belong in the log: the contents of the transcript — metadata only

---

## 12. Building the EXE

```powershell
.\.venv\Scripts\Activate.ps1
.\build.ps1
```

PyInstaller `--onedir --windowed` with `--collect-all` for `ctranslate2`, `av`,
`faster_whisper`, `tokenizers`, `onnxruntime`, `yt_dlp` — these packages carry native DLLs or
data files that PyInstaller will not find on its own.

The build script verifies before running:
- an active `.venv`
- PyInstaller installed
- that all imports succeed (`python -c "import ..."`)

Result: `dist\Prepisovac\` — a portable folder, ~350 MB.

---

## 13. Acceptance criteria

The application is finished when all of these scenarios pass:

1. **A clean environment** — on a PC with no libraries installed the application starts,
   preflight shows the missing packages in red and offers the install command. The *Start*
   button is disabled.
2. **A non-existent file** — entering a nonsense path returns a message within a second,
   without loading the model.
3. **A file with no audio** — selecting a text file with an `.mp3` extension ends with “The
   file contains no audio stream.”
4. **A full disk** — with less than 5 GB free, preflight warns.
5. **A local mp3, 40 min, model medium** — it runs, the progress bar grows smoothly, the
   `.txt` output contains sensible Czech text.
6. **A YouTube URL** — the audio downloads, the transcription runs, and both stay in the
   output folder.
7. **Interruption halfway** — the *Interrupt* button stops the run within 5 seconds, the
   window stays functional, and it can be started again.
8. **A second run** — the model is not downloaded again; transcription begins within
   3 seconds.
9. **Network disconnected during download** — a network error message, not a crash.
10. **An existing output file** — overwrite/rename is offered.

---

## 14. Implementation notes

- Whisper garbles proper nouns and technical terms in Czech. With content about AI, expect
  mangled model and company names. This is not an application defect.
- `vad_filter=True` skips silence and speeds the run up noticeably, but on very quiet
  recordings it can clip the beginnings of sentences. Keep it as an option.
- Percentages from `segment.end / info.duration` are reliable, because `info.duration` is
  determined up front from the container. The only phase without percentages is downloading
  the model.
- Keep the model on the `Transcriber` instance, not in a local variable — otherwise it gets
  loaded again on every run.
