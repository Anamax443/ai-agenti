# AGENTS.en.md — how to work in this repository

Instructions for AI assistants (Claude Code, Codex, Copilot and the like). The same applies
to people, they just read it voluntarily. Commit conventions and checklists are in
[CONTRIBUTING.en.md](CONTRIBUTING.en.md) — this file holds what an agent cannot guess from
them.

Czech original: [AGENTS.md](AGENTS.md) — **the Czech version is the authoritative one.**

---

## What this repository is

**A specification, not an application.** It contains no agent code, has no build and no
unit tests. It holds the methodology (`01-principy/`), a phased procedure with gates
(`sablony/BUILD-PREDPIS.en.md`), blank templates to fill in (`sablony/`) and completed
cases (`02-pripady/`).

From which the first rule follows: **code does not belong here.** When a design turns into
a working thing, it gets its own repository and a link from here. Half-finished code left
lying around drifts away from what actually runs — and nobody can tell which copy is the
truth. The same rule applies to text: `sablony/kostra-agenta/NAVRH.md` was a byte-for-byte
copy of the design sheet and is now only a pointer. **Link, do not copy.**

## Language and form

- The repository is written in **Czech**, diacritics included. File names, paths and code
  without diacritics.
- Every document has an English twin named `<name>.en.md` / `<name>.en.html`. **When you
  change one, change the other in the same commit.** The check is
  `python kontrola/dvojice.py` and it runs in CI.
- Where the two disagree, the Czech version wins. English is a translation, not a fork.
- Factual, no marketing. A claim without a reason does not belong in the text.
- For a list, a table beats a paragraph.

## Where the truth is

| Topic | File |
|---|---|
| The methodology, 16 chapters | [01-principy/PRINCIPY-stavby-agentu.en.md](01-principy/PRINCIPY-stavby-agentu.en.md) |
| What to fill in before building | [sablony/navrhovy-list.en.md](sablony/navrhovy-list.en.md) |
| How to build — phases F0–F8 and gates | [sablony/BUILD-PREDPIS.en.md](sablony/BUILD-PREDPIS.en.md) |
| How the specification did in the field | [02-pripady/AUDIT-job-watch.en.md](02-pripady/AUDIT-job-watch.en.md) |
| State and diary | [HANDOFF.en.md](HANDOFF.en.md) + its visual twin `STATUS.en.html` |

## What CI checks

`.github/workflows/kontrola.yml` runs on every push:

- **gitleaks** — a secret scan over the whole history.
- **lychee** `--offline` over `**/*.md` — every relative link must point at an existing
  file. When you rename or delete a file, fix the links to it or CI fails. External URLs
  are not checked offline, so a typo in an address will not be caught by CI — verify those
  by hand.
- **`kontrola/dvojice.py`** — every Czech document has an English twin and vice versa.
  A document that is deliberately not translated goes into `kontrola/bez-prekladu.txt`,
  where it is visible rather than silently missing.

The `testy` and `evaly` steps are commented out in the workflow. They get uncommented once
there is agent code here — which, by the rule above, is not supposed to happen.

## What must not go in here

- **Transcripts and full texts of third-party sources.** The repository is public.
  `00-zdroje/prepisy/` is in `.gitignore` and stays there. What goes into the repository is
  the citation, the transcription parameters and a map of “what was said at which
  timestamp → where it landed in the methodology”. Nothing more.
- **Secrets of any kind.** Not even in examples — use an obviously fake placeholder.

## The diary

`HANDOFF.md` is append-only, **newest entry at the top**, structured as
*Done / In progress / Remaining*. When you change the contents of the repo, record it there
and mirror the same change into `STATUS.html` — the two must not contradict each other. If
you update one and not the other, next time nobody knows which one is lying.

## Before you design an agent

The order is not a recommendation, it is the specification:

1. **`sablony/navrhovy-list.en.md` filled in before** the first line of code exists.
2. **F1** — the core verified against a real sample, not an invented one.
3. **F3** — a deterministic backbone with two outcomes (fails with a report / goes well),
   still without a model.
4. **F6** — a kill switch that actually stops the run.

These four are not skipped. The remaining phases and their gates are in
[sablony/BUILD-PREDPIS.en.md](sablony/BUILD-PREDPIS.en.md); for a small agent some of them
can be simplified — the chapter *What a small agent may skip* says exactly which.
A gate is not a formality: it is the list of conditions without which the next phase stands
on sand.

## The core in one sentence

> **AI recognises. Code executes.**

The model does three things: recognises intent, extracts structure, composes text.
Everything else is deterministic code. A design in which the model *executes* something is
a bad design — and it is the first thing to look for in review.
