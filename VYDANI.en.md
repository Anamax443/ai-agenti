# RELEASE v0.10 — 2 September 2026

> 🇬🇧 English · [🇨🇿 Čeština](VYDANI.md) — **the Czech version is the authoritative one.**

| | |
|---|---|
| **Version** | `v0.10` |
| **Date** | 2 Sep 2026 |
| **Scope** | 49 conditions across nine gates, F0–F8 |
| **Known error** | **a catch rate of 4 out of 8** on the single documented case |
| **Repeatability** | **not measured** |
| **Previous release** | `v0.9` (1 Sep 2026) |
| **Target of the second audit** | **`v0.10`** — the `audit-2-freeze` tag is superseded, see below |

This is not a final document and deliberately does not call itself one. It is a **release**: a
fixed point to measure against, with its own error written down and with a boundary beyond
which it does not hold.

---

## Changes since v0.9

Release `v0.9` was cut on the evening of 1 Sep and **the next day the first agent was measured
against it**. The measurement found no new defect in the subject; it found three in the
instrument:

| Finding | Change |
|---|---|
| `M1` the result **"not measured"** was missing — the measurer was pushed into `ne`, a different claim | a fourth value; the share of `neměřeno` is now a **metric of the measurement's honesty** |
| `M2` **the level was filled in only for `ano`** — for `ne` there was no telling "I provoked it" from "I read the code" | the level is filled in for `ne` too; the scale keeps asking one thing: *how do you know* |
| `M3` **the strictness was decided during measurement**, although F0.4 demands it | the protocol header gains an *origin of strictness* row; if the measurer sets it, that is simultaneously a `ne` on F0.4 |

The number of conditions is unchanged (**49**) and so is the wording of the gates. What changed
is the **instrument** — and that is enough for a new release, because measurements taken with the
old and the new form are not comparable.

**The `audit-2-freeze` tag is superseded.** It froze the state before the two-axis risk model, the
state model, the measurement protocol and the layers of checks. Measuring against a version that
no longer exists would waste the second audit. The target is `v0.10`; the tag stays as history.

## Why not 1.0

The methodology wants to be an **etalon** — an instrument, not a good text. An instrument has to
meet requirements a good text does not, and two of them are unmet:

- **Repeatability is unknown.** An etalon only its author can use is not an etalon. There is one
  way to verify it — two measurers, the same agent, the same form, and the difference between
  the forms is subtracted. Nobody has done it yet.
- **The evidence base is N = 1.** One audit, on the methodology author's own agent, which writes
  into no other system and communicates with no strangers.

The number 1.0 would claim more than is documented. Hence 0.10.

## Known error: 4 out of 8

An etalon must know its own inaccuracy. Here is the only number it has about itself:

On its first live use the specification found **four out of eight** defects that were eventually
proven in the same agent. It caught the kill switch that did not stop the pipeline · the silent
run failure · foreign text without a wrapper · the unmeasurable prompt. It **missed all four
orchestration defects**: a green run when every source failed, a lost notification, a missing
run lock, and a stopped run flipped back to success.

**A catch rate of 50 % on one sample.**

> That the current wording would catch 8 out of 8 is **not a measurement.** Those items came
> from those very defects, so it would be retrospective fitting. Hence measurement is always
> against a **release**, never against the current `main`.

## Scope of validity

The methodology has so far described itself as applicable to "any agent in any domain". That
claim is not documented, and this release narrows it.

**It holds for** an agent that has:

- a closed list of scenarios,
- the division *the model recognises / the code executes*,
- irreversible actions that can be enumerated.

**Unverified for:**

| Class of agent | Why we do not know |
|---|---|
| planning, research and multi-agent systems | they choose their next step themselves — the core does not account for them |
| agents writing into other systems (ERP, accounting) | F3 has no transactions or compensations, F5 has no multi-role approval |
| agents operated by someone other than their author | the methodology's readability for a stranger is not documented |
| domains with hard rules (accounting, manufacturing, healthcare) | the model/code boundary under regulatory pressure has not been tested |

This is not a list of where the methodology fails. It is a list of where we **do not know**
whether it works.

## What release v0.9 brought

All of it arose on 1 Sep 2026 from the audit, its aftermath and three external reviews. It holds unchanged in v0.10.

| Change | Origin |
|---|---|
| **Three states instead of two** — an observable ending: success · failure · a recorded unknown outcome | external finding `A1`/`N9`: "there is no third possibility" does not hold for a remote call |
| **Two axes of risk** — action reversibility sets the mode, system impact sets the strictness N/Z/V | external finding `A3`; reversibility alone misclassifies an agent that only reads and recommends |
| **The state model** — an irreversible action sits on a transition, not inside a state | `N3`: three of the four orchestration defects were its missing version |
| **Outgoing identity and the owner of the data** in F5 | a company mailbox is not the agent owner's mailbox |
| **A measurement protocol** and a gate inventory (`kontrola/brany.py`, `sablony/MERENI.md`) | a free-text audit is not comparable; the count of conditions drifted three times |
| **Layers of checks** — what each one structurally cannot see | 159 tests missed eight defects; breadth alone is not enough |
| **Acceptance tests for provoked failures** in F3 and F6 | the second round of findings |
| **Hard negatives** and the CI/runtime backend distinction in F4 | an eval set without hard negatives produced a precision of 100 % that means nothing |

## What is merely claimed

By our own scale: **every change above sits at level `U1`** — in the text, readable, **not
provoked**. No project has yet been measured against them.

Specifically missing:

- the acceptance test "a timeout after the send and before the write" — it exists in no project,
- a filled-in state model for an agent with an irreversible action,
- a documented catch for the new layers of checks.

**The first filled-in protocol now exists** — [`MERENI-job-watch.md`](02-pripady/MERENI-job-watch.md),
2 Sep 2026. It found no new defect in the subject but three in the instrument; they are in v0.10.

## What the release does not claim

- **It does not claim the methodology is finished.** Seven findings against it remain open: the
  evidence quintuple in the specification, the role contract and metrics per model role, the
  tool-security layer, splitting eval sets into regression/challenge/held-out, decommissioning,
  a machine consistency check, and the scope of validity.
- **It claims nothing about the law.** Statements about the AI Act are qualified in this release
  as an **internal rule, not a quotation of the law**. Legal assessment belongs to someone
  qualified to give it.
- **It does not claim that wrapping foreign text closes prompt injection.** That is defence in
  depth. Missing: an allowlist of tools and domains, validation of arguments against a schema,
  output control, and exfiltration tests.
- **It does not claim this assessment is independent.** It came from the methodology author's
  work on their own agent, aided by three external reviews, one of which was signed by that same
  author.

## How to measure against this release

```bash
python kontrola/brany.py --protokol v0.10 > 02-pripady/MERENI-<agent>.md
```

The rules for filling it in are in [`sablony/MERENI.en.md`](sablony/MERENI.en.md). What matters:
`nelze` (cannot be measured) is a full-fledged result, `ano` (yes) requires evidence, and **a
command is not evidence** — its output is.

Positional identifiers (`F3.4`) hold **within this release**. They shift when a condition is
inserted; the version pins their meaning, just as with `ISO 27001:2013 A.9.2.3`.

## What would make this release a 1.0

Not writing. These four things, in this order:

1. **A second audit** on an agent of a different class — ideally one that writes into another
   system or communicates outward. Against a frozen version, with predictions written down in
   advance.
2. **A repeatability test** — two measurers, the same agent, subtract the difference.
3. **A third case led by an outside person** — the only test of readability without the author.
4. **The catch rate measured again** on a case the rules did not come from.

Until then this is a very well documented experience from one agent. That is not nothing — but
it is named for what it is.

## Release history

| Version | Date | Note |
|---|---|---|
| `audit-2-freeze` | 1 Sep 2026 | frozen for the second audit; **superseded** — the target is `v0.10` |
| `v0.9` | 1 Sep 2026 | the first numbered release: three states, two axes of risk, the state model, the measurement protocol, layers of checks |
| `v0.10` | 2 Sep 2026 | the protocol after its first trial: the `neměřeno` result, a level for `ne`, the origin of strictness |
