# <agent name>

Repository skeleton for a new agent. Copy the folder, rename it, fill in the design sheet
and start from the module with the fewest dependencies.

Czech original: [README.md](README.md)

## Structure

| Path | Contents |
|---|---|
| `NAVRH.md` | the filled-in design sheet — the first thing you write |
| `prompts/` | persona and instructions, versioned like code |
| `evals/` | the regression set, run in CI on every prompt change |
| `src/` | modules following the contracts from the design |
| `runbook.md` | what to do when it breaks |

## Rules

- A prompt is code: it goes through review, carries a version, and is written into the run record.
- A module does not reach into someone else's database. It receives data as a parameter.
- Every module has a CLI and can be run without the rest of the system.
- The test environment has no outbound channels — by configuration, not by an `if`.
