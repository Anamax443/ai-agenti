# HANDOFF — state diary: ai-agenti

Append-only. Newest entry at the top. Used to pick the work back up from another machine or
after a break.

Czech original: [HANDOFF.md](HANDOFF.md) — **the Czech version is the authoritative one.**

## 2026-09-01 (4) — risk has two axes: action reversibility × system impact

- **Why:** the external review (`A3`) showed that classifying by action reversibility alone
  is not enough. An agent that merely reads CVs and proposes a ranking has no irreversible
  action — under §7 that is the lowest mode, "act alone, just report". Yet it decides who
  gets an interview, and for the person filtered out the mistake is irreversible. The
  converse holds too: "a high-impact agent" says nothing about which of its forty calls
  needs approval.
- **Done — principles §7 rewritten around two axes** (CS and EN):
  - the **action axis** (reversibility) sets the **mode** of an individual action —
    unchanged, only named,
  - the **system axis** (impact) sets the **strictness** with which everything is verified.
    Five questions: who the decision is about · what it affects · on what data · at what
    scale · whether a mistake is noticed in time. The answers produce a level **N / Z / V**.
- **Strictness has consequences, otherwise it would be one more label.** A "what strictness
  changes" table binds the level to phase simplification, mandatory hard negatives in evals,
  the **minimum closure level for a finding** (N → U1, Z → U2, V → U3), the recipient of
  crash reports, oversight, and the scenario-review cadence. At level **V** additionally:
  a decision about a person has a human in the loop **even when it is reversible** — a
  record can be undone; being passed over cannot.
- **This also closes `N5`.** The "what to skip for a small agent" table no longer rests on
  the subjective "a simple agent built for yourself". Now: you may simplify only at
  strictness **N** and with no irreversible reputational or physical action; if only one
  holds, everything except F4 and F5 may be trimmed; if neither holds, the specification
  applies in full. The reason is in the text: every author knows their own agent and finds
  it simple because they know its **intent** — reversibility and impact do not know the
  intent, only the consequence.
- **Gate F0** gained an item: the strictness is **derived from the answers** in the design
  sheet, not guessed, and what follows from it is written down.
- **The design sheet** has a new section *Strictness — the system axis*: five questions with
  answers and a tick column, the resulting level, and a "what follows from it" line. You do
  not fill in the level; you fill in the answers.
- **A correction of our own imprecision.** Finding `N5` (and `O2` from review P2) claimed the
  "Risk category (AI Act)" label had **no** consequence. More precisely: it had one ("the
  specification is not abridged for those"), but only as a sentence in the design sheet — it
  was not wired to the gates or to the simplification table. Now it is.
- **The AI Act claim is qualified** (finding `B8`): the disclosure row now reads "depends on
  role and jurisdiction; our rule: always" instead of "mandatory (AI Act)". That does not
  settle the legal assessment — it only stops presenting an internal rule as a general
  statutory duty.
- **Verified:** `python kontrola/dvojice.py` — green.
- **Note on the `audit-2-freeze` tag:** it points at `85a45cd` and is the target of the
  second audit. This change sits **after** it and does not enter the audit — otherwise it
  would be retrospective fitting again (finding `B7`).
- **Remaining:** `N3` the state model · `N1` the evidence quintuple in the specification ·
  `N4` the role contract and metrics per model role · `A6` the tool-security layer
  (allowlist, argument validation, output control, exfiltration tests) · `A4` splitting eval
  sets into regression / challenge / held-out · `A2` narrowing the "any agent" scope · `N6`
  decommissioning · `N8` a machine consistency check. And above all, still: **the second
  audit**.

## 2026-09-01 (3) — the core sentence corrected: three states instead of two; the review found what eight self-findings did not

- **Why:** three external reviews of the dossier. The sharpest finding (`A1`) is that the
  sentence “either the process fails with a report or it goes well; **there is no third
  possibility**” is technically false for a remote call: the send goes through, the reply is
  lost, and the agent does not know whether to retry. The outcome is neither known success nor
  known failure. The methodology also contradicted itself — the JobWatch audit already asked
  for `failed`/`degraded`/`notification_pending`, which is more than two outcomes.
- **Done — the core sentence reformulated** (CS and EN, 15 files, 18 edits): success · failure ·
  **a recorded unknown outcome**; there is no *silent* branch. The original claim stays true in
  what it meant — no ending may be silent. Changed in `PRINCIPY` (§1, §11, §15, §16),
  `BUILD-PREDPIS` (F3 and the never-skipped minimum), `README`, `AGENTS`, `STATUS`,
  `mapa-mysleni`, `manazerske-shrnuti`, `vyvojovy-diagram`.
- **Gate F3 gained two items:** an unknown outcome has its own state and next step (query the
  target system / retry idempotently / queue for a person — never blindly, never as `ok`), and
  the provoked failures now include **a timeout after the send and before the write**.
- **New anti-pattern:** *An unknown outcome recorded as success.*
- **Deliberately unchanged:** the quotation in `00-zdroje/ZDROJE.md` (a record of what the
  source said, not our claim) and the gate wording quoted in `02-pripady/AUDIT-job-watch.md`
  (the historical state of the audit).
- **`B1` closed too:** commit `62d4b38` was pushed only after the first round of review. The
  dossier cited it as the version under review while `origin/main` was still `ed0b7bb` — the
  reviewer could reproduce nothing. **Lesson: the version cited in a document for a third party
  must be public before the document is.**
- **Verified:** `python kontrola/dvojice.py` — green.
- **Remaining:** reconcile the number of gate conditions (after today's change there are **42**, of which 3
  have a verifiable artefact and **39** are proven by assertion — the dossier wrongly said 38/37);
  restore the “evidence quadruple” to a **quintuple** including the artefact (a command is not
  evidence; its output is); extend the risk model with a system axis alongside action
  reversibility; separate regression / challenge / held-out eval sets; qualify the AI Act
  claims. And still: a second audit on an agent of a different class.

## 2026-09-01 (evening, 2) — the correction propagated into the summaries; the specification gained acceptance tests and hard negatives

- **Why:** commit `ed0b7bb` corrected the body of the audit, but the green claim stayed exactly
  where a reader looks first — the aftermath heading, the findings table row, the pill in
  `STATUS.html`, the "precision 100 %" number and the management summary. **The tick outlived the
  finding** — the same defect one floor up from the one the audit describes in JobWatch.
- **Done — summaries brought in line with the correction** (CS and EN): the aftermath heading in
  the audit, the table row for finding 3 (✅ → ⚠️ half), the F1 number qualified (all 17 negatives
  are rejected by the prefilter, so precision 100 % says nothing about discrimination), the State
  row and the Foreign text row in `STATUS.html`, the aftermath paragraph in
  `05-html/manazerske-shrnuti.html`.
- **Done — three changes to the specification**, each with a documented case from the second round:
  - **F3 and F6 gained acceptance tests for provoked failures.** "Two outcomes" is proven by
    provocation, not by a unit test over a pure function — 159 tests and 26 evals missed four
    orchestration defects in JobWatch. New items: all sources down, failure after the write and
    before the send, two concurrent runs, a stop mid-run, and that a stopped run stays stopped.
  - **F4 now distinguishes a CI-reachable backend from a runtime-only one** (the open item from the
    morning of 1 Sep) and additionally requires **hard negatives** — a negative the deterministic
    filter throws away says nothing about the model. Also added to `kostra-agenta/evals/README.md`
    (composition, not just count). In addition: foreign text must be wrapped **at every model call**,
    first where the model holds tools — that is exactly where JobWatch broke.
  - **Contradiction fixed:** the critical path read `F0 → F1 → F3 → F5` while the same document
    calls the kill switch in **F6** unskippable. Corrected to `F0 → F1 → F3 → F6`.
- **Verified:** `python kontrola/dvojice.py` — green.
- **Remaining:** a second audit on an agent of a different class (one that writes or sends
  outward) — the evidence base is still N = 1. Unchanged: deleting `03-projekty/prepisovac/kod/`,
  `AGENTS.md` into the other repos, the UX chapter from Albada, Vorel and Lanham, the glossary,
  gwalarn.

## 2026-09-01 — JobWatch audit aftermath: all findings closed, and one finding back into the specification
- **Done:** an **Aftermath** section was added to
  [`02-pripady/AUDIT-job-watch.en.md`](02-pripady/AUDIT-job-watch.en.md). Within two days all four
  findings had fallen, in the very order the audit prescribed (crash reporting → kill switch →
  wrapping foreign text → evals and prompt versioning). **F1 got its number:** scoring accuracy
  measured on 23 real listings inside the deployed version — precision 100 %, recall and effective
  recall 100 %, coverage 100 %.
- **A finding FOR THE SPECIFICATION (not yet incorporated, a proposal):** gate F4 requires "evals run
  in CI". For an agent whose default backend is a **binding available only at runtime** (Cloudflare
  Workers AI) that is unachievable — CI would measure a different model than the deciding one. The
  JobWatch set paid for this twice: first it called the paid model directly, then it failed to pass
  the backend choice, so it measured the free rung even with the paid model selected. **Proposal:**
  in F4, distinguish a backend reachable from CI (current wording) from one that exists only at
  runtime ("on the deployed version, manually, with a record, and the run notes which rung answered").
  Without that, the gate forces you either to lie or to measure the wrong thing.
- **A second insight:** *a green set stops discriminating.* After the fixes JobWatch is 23/23, which
  turns the instrument into an ornament. F8 ("evals grow") is therefore not administration but the
  condition for the measurement to keep meaning anything.
- **Updated:** `STATUS.html` + `.en.html` (three defects → four, all fixed, F1 number added),
  `05-html/manazerske-shrnuti.html` + `.en.html` (an aftermath paragraph).
- **Remaining:** fold the proposed F4 amendment into `sablony/BUILD-PREDPIS.md` — for now it is only
  described in the audit; the specification itself is unchanged.

## 2026-08-31 — visual outputs, bilingualism, the pair check

- **Done — four new pages in `05-html/`,** in Czech and English, in the same visual language
  as `postup-stavby.html` (the same palette and type, so everything speaks with one voice):
  - [`manazerske-shrnuti.html`](05-html/manazerske-shrnuti.html) — **one A4 portrait page to
    print for management.** The core, the two endings of the process with the third
    explicitly removed, what it means operationally (cost, accountability, identity,
    oversight, regulation), nine phases with the three that are never skipped highlighted,
    the evidence from the JobWatch audit and three numbers. `@page A4 portrait`, verified to
    fit on a single side.
  - [`mapa-mysleni.html`](05-html/mapa-mysleni.html) — the mind map: the core in the middle,
    five branches (foundation, construction, contact with the world, control, operation),
    with the anti-patterns and the entry point underneath. The left side answers “what is it
    made of”, the right side “how is it run”.
  - [`tok-informaci.html`](05-html/tok-informaci.html) — information flow through an agent:
    for each leg you can see what enters and what leaves, who does the step (model / code /
    person), and where the **trust boundary** lies, past which foreign text is only data. At
    the end, the three real defects from the audit mapped onto the legs of the route.
  - [`vyvojovy-diagram.html`](05-html/vyvojovy-diagram.html) — the F0–F8 flowchart in SVG:
    phase → gate → conditions → next phase, with a dashed “no” branch back to the same
    phase. The coordinates sit on a regular grid, so it can be edited by hand.
- **The repository is now bilingual.** The convention is `<name>.en.md` / `<name>.en.html`;
  where the two disagree, the Czech version wins. The core is translated: the principles, the
  build specification, the design sheet, the sources, the job-watch audit, the agent
  skeleton, README, AGENTS, CONTRIBUTING, ZALOZENI-REPO, STATUS, the diary, both portfolios
  in `04-firemni/`, all three gwalarn documents, the transcriber brief and both remaining
  pages (`postup-stavby`, `navrhovy-list-faktury`).
  **The pair check is green: 28 documents in both languages, 1 recorded exception.**
- **The new feature carries its own check:** [`kontrola/dvojice.py`](kontrola/dvojice.py)
  verifies that every Czech document has an English twin and vice versa. Exceptions are
  written by hand into `kontrola/bez-prekladu.txt` — a missing translation should be visible,
  not vanish quietly. Wired into CI alongside gitleaks and lychee. The script also reports a
  *stale* exception, so the list tidies itself once a file disappears.
- **In progress:** —
- **Remaining:**
  - **Deleting `03-projekty/prepisovac/kod/` is still blocked on permissions.** The decision
    stands (see the entry below); the command is `git rm -r 03-projekty/prepisovac/kod`.
  - Unchanged: the UX chapter from Albada, Vorel and Lanham, the glossary against the public
    specifications, gwalarn, the first agent from `04-firemni/`.

## 2026-08-31 — AGENTS.md

- **Done:** [`AGENTS.md`](AGENTS.md) — rules for AI assistants working in the repo. The
  important one is the first: **code does not belong here**. When a design turns into a
  working thing, it gets its own repo and a link from here; half-finished code left lying
  around drifts away from what actually runs, and nobody can tell which copy is the truth.
  Also: Czech with diacritics, link don't copy, never third-party transcripts in a public
  repo, keep `HANDOFF.md` and `STATUS.html` in agreement, the design sheet before the first
  line of code, and F1/F3/F6 which are never skipped. Referenced in `README.md` (Project
  standard) and in `STATUS.html` (repo contents + done).
- **In progress:** —
- **Remaining:**
  - **The transcriber duplication** — decided: delete `03-projekty/prepisovac/kod/` and keep
    only `ZADANI-prepisovac.md` here as a design artefact with a pointer to
    [mp3totxt](https://github.com/Anamax443/mp3totxt). The reason is not merely “two copies”:
    the prototype **failed its own gate**. The brief calls `preflight.py` the key module and
    “nothing may be started blind” the key requirement — and there is no `preflight.py`, no
    `validators.py`, no `appstate.py` in the code, and no tests either. What is left is a GUI
    prototype of three files with a single `audio.exists()` check. What `mp3totxt` does
    **not** cover against the brief: the GUI, downloading from a URL via yt-dlp, and
    preflight. That gap is not lost by deleting the code — it is described in the brief.
    *The deletion itself has not happened yet; it is blocked on permissions.*
  - `AGENTS.md` into the other repositories.
  - Unchanged: the UX chapter from Albada, Vorel and Lanham, the glossary against the public
    specifications, gwalarn, the first agent from `04-firemni/`.

## 2026-08-30 — first live use of the specification + the status sheet

- **Done:** the specification was applied to
  [`Anamax443/job-watch`](https://github.com/Anamax443/job-watch), the only agent running
  live. It found **three defects the tests had not**: a kill switch that closes the run
  record but does not stop the pipeline; a crashed run nobody finds out about, because
  notifications are only sent on findings; and listing text written by other people going
  into the model unwrapped. The analysis is in
  [`02-pripady/AUDIT-job-watch.md`](02-pripady/AUDIT-job-watch.md), with the record of the
  finding and a flowchart of the run in the project's own repo.
- **What this says about the specification:** the findings landed in F4 and F6 — that is, in
  the phases added most recently (from Albada and the analysis of sources). The phases that
  had been in the methodology from the start — determinism, limits, identity — held up. Weak
  but real evidence that the extensions went in the right direction.
- **Added `STATUS.html`** — a status sheet in the usual shape: overview, repo contents,
  phases F0–F8 with gates, sources of the methodology, done vs. remaining. Visually aligned
  with the `STATUS.html` in job-watch, so that it speaks one language across projects.
- **Remaining:** a chapter on agent UX (still unused from Albada), Vorel and Lanham, a
  glossary against the public specifications, `AGENTS.md`.

## 2026-08-30 — analysis of Albada, extending the specification

- **Done:** read the whole of Albada, *Building Applications with AI Agents* (O'Reilly 2025,
  355 pp.). Seven things we had been missing were added to `sablony/BUILD-PREDPIS.md`:
  discoverability of a text interface (F0), disabling tools by configuration (F2), the tool
  recall/precision and parameter accuracy metrics (F4), a budget of ~10 % for escalations,
  the principle of least power and the growth of autonomy (F5), the four ways human oversight
  fails (F6), the error-vs-variance rule and shadow runs (F7), PSI for distribution shift and
  golden paths (F8).
- **The eval template** was rewritten: an expected end state instead of an expected text, a
  table of metrics, instructions for manufacturing edge cases, and an example with an attack.
- **The design sheet:** a link to a training CTF on prompt injection.
- **The book citation** in `00-zdroje/ZDROJE.md`, including a chapter → what-we-took map. The
  text of the book is not in the repo (a warez bundle; see the rule about transcripts).
- **Remaining:** work through Vorel (NoOps) and Lanham; from Albada the UX chapter as a whole
  and the chapters on multiagent coordination and fine-tuning are unused (out of scope).

## 2026-08-30 — the build specification and template changes

- **Done:** `sablony/BUILD-PREDPIS.md` — a general phased procedure F0–F8, every phase with a
  gate. It fills the gap between the design sheet (what to design) and
  `05-html/postup-stavby.html` (the concrete plan for one project). The minimum that is never
  skipped: F1 a real sample, F3 the two endings of the process, F6 the kill switch.
- **The design sheet** was extended with two sections: *Hostile input* (prompt injection for
  agents that read other people's text) and *Regulation and data* (AI Act, personal data,
  retention).
- **A duplication removed:** `sablony/kostra-agenta/NAVRH.md` was a byte-for-byte copy of the
  design sheet. It is now a pointer to the single source of truth — two copies would drift
  apart and nobody would notice which.
- **Remaining:** compare the specification with the public ones (12-factor agents, Anthropic
  workflows-vs-agents) and add what makes sense to adopt.

## 2026-08-30 — the source of the methodology added

- **Done:** `00-zdroje/ZDROJE.md` — the citation for the show (Keci a politika, the special
  with Marek Bartoš, “Umělá inteligence je naše UFO”), the transcription parameters
  (mp3totxt 0.1.0, model `medium`, 55:51 of audio, a ratio of 1.81×) and a map of 19
  timestamps → chapters in `01-principy/`. Verified against the `.json` transcript.
- **A deliberate decision:** the transcript (`.txt`/`.json`/`.srt`/`.vtt`) lives in
  `00-zdroje/prepisy/` locally only and is in `.gitignore`. The repo is public and the
  transcript of somebody else's show, whose second half is paid, does not belong in it. The
  MP3 was not copied at all.
- **Remaining:** the same procedure for further sources (the transcript outside git, the
  citation and the timestamps in here).

## 2026-08-30 — repository created

- **Done:** the repo `Anamax443/ai-agenti` (public) was created from the local `agent-kit`
  bundle. Contents: the methodology (`01-principy/`), a completed case (`02-pripady/`),
  work-in-progress projects (`03-projekty/`), company portfolios (`04-firemni/`), the visual
  procedure (`05-html/`), templates (`sablony/`). Added according to project-standard:
  `LICENSE`, `.editorconfig`, `.gitattributes`, this diary. CI `kontrola.yml` (gitleaks +
  link check) has been running since the first push. Secret scanning + push protection +
  Dependabot enabled in Code security.
- **In progress:** —
- **Remaining / open questions:**
  - `03-projekty/prepisovac/kod/` is an older variant of the same thing that already lives in
    the separate repo `Anamax443/mp3totxt` (a working CLI with tests). Decide: keep only
    `ZADANI-prepisovac.md` here as a design artefact and delete the code with a pointer to
    mp3totxt, or the other way round.
  - Gwalarn: the design of a content agent fits the `Anamax443/gwalarn` repo. Decide whether
    `03-projekty/gwalarn/` should split off there.
  - Pick the first agent from `04-firemni/AGENTI-mala-kancelar.md` and build it.
