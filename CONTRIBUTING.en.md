# How to work with this repository

Czech original: [CONTRIBUTING.md](CONTRIBUTING.md)

## Commit conventions

| Prefix | When |
|---|---|
| `feat:` | a new feature |
| `fix:` | a fix |
| `prompt:` | a change to a prompt or a persona |
| `docs:` | documentation, methodology |
| `chore:` | dependencies, configuration |

The `prompt:` prefix is separate on purpose — such changes cannot be covered by a unit
test and need an eval set.

## A prompt is code

- It lives in the repository, not in a tool's UI and not in an unversioned database
- It goes through the same review as a code change
- It carries a version that every run records

## Before you build anything

1. Read [`01-principy/PRINCIPY-stavby-agentu.en.md`](01-principy/PRINCIPY-stavby-agentu.en.md)
2. Fill in [`sablony/navrhovy-list.en.md`](sablony/navrhovy-list.en.md)
3. Verify the core against a real sample (phase F1)
4. Freeze the module contracts
5. Only then write code

The order of the phases and their gates is in
[`sablony/BUILD-PREDPIS.en.md`](sablony/BUILD-PREDPIS.en.md). A gate is not a formality —
it is the list of conditions without which the next phase stands on sand.

## Before you deploy anything

- [ ] Unit tests pass
- [ ] The eval set is above the threshold
- [ ] No secrets in the repository
- [ ] The runbook is filled in
- [ ] The kill switch works

## Language

Czech is the primary language of this repository; each document has an English twin named
`<name>.en.md` (or `.en.html`). When you change one, change the other in the same commit —
`npm`-free check: `python kontrola/dvojice.py`, which also runs in CI.
