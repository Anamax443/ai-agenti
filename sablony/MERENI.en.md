# MEASUREMENT — how an agent is measured against the etalon

> 🇬🇧 English · [🇨🇿 Čeština](MERENI.md) — **the Czech version is the authoritative one.**

An audit written as free text reads well and is **not comparable**. Two measurers produce two
different documents and there is no subtracting one from the other to see whether they agreed.
An etalon where that cannot be done is not an etalon — it is an opinion with tables.

This sheet is therefore a form, not an essay.

## The blank form is generated, not copied

```bash
python kontrola/brany.py --protokol v0.9 > 02-pripady/MERENI-<agent>.md
```

The form is derived directly from [`BUILD-PREDPIS.en.md`](BUILD-PREDPIS.en.md)'s Czech
original. **There is no second list of conditions**, and there must not be: while the count
was written by hand it drifted — one document stated 38, 37, 41 and 42 in four places, and it
took an outside review to notice.

A filled-in measurement is a **record**, not a methodology document — either give it an
English twin or list it in [`kontrola/bez-prekladu.txt`](../kontrola/bez-prekladu.txt), so the
pair check passes while the missing translation stays visible.

The inventory and the check:

```bash
python kontrola/brany.py            # check: the number of conditions matches CS × EN
python kontrola/brany.py --seznam   # inventory with identifiers
```

## What is filled in for each condition

| Field | Values | When it is mandatory |
|---|---|---|
| **Result** | `ano` (yes) · `ne` (no) · `nelze` (cannot be measured) | always |
| **Level** | `U0`–`U4` | when the result is `ano` |
| **Evidence / note** | a file, a test, a command **with its output** | for `ano` and for `nelze` |

### Closure levels

| | Meaning | Who knows |
|---|---|---|
| **U0** | claimed — the author says it holds | the author |
| **U1** | in the code — the change is in the repository and can be read | anyone reading |
| **U2** | covered by a test — the test fails when it breaks | CI |
| **U3** | provoked in an environment — the state actually occurred | production |
| **U4** | independently closed — verified by someone other than the author of the fix | a third party |

The minimum level at which a condition may be closed is **set by the agent's strictness**
(N → U1, Z → U2, V → U3; see [principles §7](../01-principy/PRINCIPY-stavby-agentu.en.md)).

### Two rules without which the form is worthless

**`nelze` is a full-fledged result.** Without it the measurer is pushed into yes/no even where
the gate does not fit the agent at hand. That is exactly how the dispute over gate F4 arose
for an agent whose default backend exists only at runtime: in CI a different model would be
measured than the one that decides. The gate then forced either lying or measuring beside the
point — and it should have been marked `nelze` with a note, not `ne`.

**For `ano` evidence is mandatory, and a command is not evidence.** The evidence is its
**output**, a stored artefact, or a test. Without that it counts as `U0` at best, even if it
happens to be true.

## Summary and calibration of the etalon

The form ends with two blocks. The first counts `ano` / `ne` / `nelze`. The second matters
more and is easy to skip:

> **Findings the measurement did not catch.**

It is filled in **later**, when a defect surfaces some other way — from production, from an
outside review, from an incident. It is not the measurer's disgrace; it is **the only number
about the accuracy of the etalon itself**.

One is documented today: on its first live use the specification found **4 out of 8** defects
that were eventually proven in the same agent. It caught the kill switch, the silent failure,
the unwrapped foreign text and the unmeasurable prompt; it **missed all four orchestration
defects**. A catch rate of 50 % on a single sample is a weak number — but an etalon without
its number is worse.

> That the current wording would catch 8 out of 8 is **not a measurement**. Those items were
> derived from those very defects, so it would be retrospective fitting. Hence measurement is
> always against a **release** of the etalon, never against the current `main`.

## Releases of the etalon

A measurement refers to a release, not to a branch:

```
Etalon: ai-agenti v0.9  (git tag audit-2-freeze)
```

Positional identifiers (`F3.4`) hold **within a release**. They shift when a condition is
inserted, and that is fine — their meaning is pinned by the version. Standards do the same:
`ISO 27001:2013 A.9.2.3` means something else than the same code in the 2022 release.

**The etalon does not change during a measurement.** Changes arising from a measurement belong
to the next release and are verified on the next case — otherwise the etalon tunes itself to
whatever it has just seen.

## Repeatability

An etalon only its author can use is not an etalon. There is one way to verify that:
**two measurers, the same agent, the same form — and the difference between the forms is
subtracted.**

Nobody has done that yet. Until then repeatability is unknown, and a measurement signed by the
author of the subject counts as a self-assessment, not as an independent measurement.
