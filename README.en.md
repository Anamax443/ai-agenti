# AI-AGENTI

[Čeština](README.md) · **English**

Methodology for building AI agents, plus work-in-progress designs.

It grew out of an analysis of an interview with Marek Bartoš (the *Keci a politika*
podcast, “Artificial intelligence is our UFO”) and out of design work on our own projects.
Extended with Anthropic's and OpenAI's recommendations on building agents.

---

## Where to start

Read **[01-principy/PRINCIPY-stavby-agentu.en.md](01-principy/PRINCIPY-stavby-agentu.en.md)**.
The rest is that same thing applied to concrete cases.

When you need to design a new agent, take
**[sablony/navrhovy-list.en.md](sablony/navrhovy-list.en.md)** and fill it in before you
write the first line of code.

When you then build it, follow
**[sablony/BUILD-PREDPIS.en.md](sablony/BUILD-PREDPIS.en.md)** — phases F0–F8, each with a
gate you have to pass before the next one begins.

How the specification did in live operation is shown by
**[02-pripady/AUDIT-job-watch.en.md](02-pripady/AUDIT-job-watch.en.md)** — on a running
agent it found four defects the tests had not — all of them fixed by 1 Sep 2026.

### When you need to show it to somebody else

| Output | What for |
|---|---|
| [Management summary](05-html/manazerske-shrnuti.en.html) | one A4 portrait page, ready to print for management |
| [Mind map](05-html/mapa-mysleni.en.html) | the whole methodology on one surface, from the core outwards |
| [Information flow](05-html/tok-informaci.en.html) | where the data goes, who processes it, where the trust boundary sits |
| [Flowchart](05-html/vyvojovy-diagram.en.html) | phases F0–F8 with gates and returns |

Every page has a Czech version and a language switch in its header. The management summary
and the flowchart are set up for A4 printing.

---

## Contents

| Folder | What is in it |
|---|---|
| `00-zdroje/` | Where the methodology comes from — citations, a map of timestamps in the interview. |
| `01-principy/` | The general methodology. Holds for any domain. |
| `02-pripady/` | A completed design sheet (invoices) and an **audit of a running agent** against the specification. |
| `03-projekty/gwalarn/` | A content agent for a band: scenario, modules, brief for module M1. |
| `03-projekty/prepisovac/` | The brief for a desktop audio transcription app. The `kod/` subfolder is slated for deletion — an unfinished prototype next to the finished [mp3totxt](https://github.com/Anamax443/mp3totxt); see `HANDOFF.md`. |
| `04-firemni/` | Agent portfolios for a small office and for a large company. |
| `05-html/` | Visual outputs: management summary, mind map, information flow, flowchart, roadmap. |
| `sablony/` | The **build specification** (phases and gates), a blank design sheet and an agent repository skeleton. |
| `kontrola/` | The language-pair check — runs in CI. |

---

## The core in one sentence

> **AI recognises. Code executes.**

The model gets three kinds of task — intent recognition, structure extraction, text
synthesis. Everything else is deterministic code. What that produces is a system with only
two possible endings: it fails with a report, or it goes well. The third branch, where it
does something nobody asked for, is removed by design.

---

## Project status

| Project | State | Next step |
|---|---|---|
| Audio transcriber | brief finished; the transcription itself is handled by [mp3totxt](https://github.com/Anamax443/mp3totxt) | decide about the GUI and URL downloading — `mp3totxt` does not cover those |
| Gwalarn — content agent | design finished | module M1 (ffmpeg), Meta accounts |
| Office agents | design | pick the first one and build it |

---

## Notes on sources

The podcast was transcribed locally with
[mp3totxt](https://github.com/Anamax443/mp3totxt) (faster-whisper, model `medium`). The
transcript garbles proper nouns and covers only the first half of the show — the second is
behind a paywall. The transcript itself is not in the repository; it stays local, outside
git.

Citations, the transcription method and the map of “what was said when → where it landed in
the methodology” are in **[00-zdroje/ZDROJE.en.md](00-zdroje/ZDROJE.en.md)**.

References to regulation (the AI Act) reflect the state as of August 2026, after the
Digital Omnibus came into force on 27 July 2026. Deadlines change; verify them.

---

## Project standard

The repository follows
[project-standard](https://github.com/Anamax443/project-standard):

- [STATUS.en.html](STATUS.en.html) — a status sheet to read in a browser (overview, phases, sources)
- [HANDOFF.en.md](HANDOFF.en.md) — the state diary (done / in progress / remaining)
- [CONTRIBUTING.en.md](CONTRIBUTING.en.md) — commit conventions, “a prompt is code”
- [AGENTS.en.md](AGENTS.en.md) — rules for AI assistants working in the repo (code does not belong here, link don't copy)
- [ZALOZENI-REPO.en.md](ZALOZENI-REPO.en.md) — how the repository was created and what is configured
- `LICENSE` — the sources are publicly readable as a sample of the work, not open source

CI (`.github/workflows/kontrola.yml`) runs on every push: it scans for secrets (gitleaks),
checks the links in `*.md`, and verifies the language pairs (`kontrola/dvojice.py`).

## Language

The repository is bilingual. Every document has an English twin named `<name>.en.md`
(`.en.html` for pages). Where the two versions disagree, the Czech one wins — English is a
translation, not a fork. Anything deliberately left untranslated is listed in
[kontrola/bez-prekladu.txt](kontrola/bez-prekladu.txt), so that it is visible rather than
silently missing.

## Relationship to the other repositories

| Here | Separate repository |
|---|---|
| `03-projekty/prepisovac/` | [mp3totxt](https://github.com/Anamax443/mp3totxt) — a finished CLI; does not cover the GUI or URL downloading |
| `03-projekty/gwalarn/` | [gwalarn](https://github.com/Anamax443/gwalarn) — the band's website |
| `02-pripady/` (invoices) | [faxx-dox](https://github.com/Anamax443/faxx-dox) — data extraction from documents |
