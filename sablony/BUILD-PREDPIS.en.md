# BUILD SPECIFICATION — from zero to a deployed agent

A phased procedure that holds for any agent. A concrete plan for a single project looks
like [05-html/postup-stavby.html](../05-html/postup-stavby.html); this document is the
template such a plan is written from.

Czech original: [BUILD-PREDPIS.md](BUILD-PREDPIS.md) · flowchart:
[05-html/vyvojovy-diagram.en.html](../05-html/vyvojovy-diagram.en.html)

**A gate** = a list of conditions at the end of a phase. Until all of them hold, the next
phase does not begin. Each gate catches one class of mistake that the following phase
would otherwise run into — and more expensively.

| | |
|---|---|
| **Input** | an idea for an agent, and a person who will own it |
| **Output** | an agent in operation, with a runbook, evals and a kill switch |
| **Critical path** | F0 → F1 → F3 → F5 |
| **Where it usually goes wrong** | skipping F1 and F3 — the model gets started before a process exists |

---

## F0 — Design on paper

**Goal:** know what is being built before the first file exists.

- Fill in the [design sheet](navrhovy-list.en.md) — all of it, not just the pleasant parts
- Close the list of scenarios. What is not on it, the agent cannot do and does not improvise
- Split the steps into *model* / *code*. If you are unsure about a step, it is code
- List the modules and their contracts (input → output)

**Gate**

- [ ] The scenarios are filled in and there is a finite number of them
- [ ] Every step states whether the model or the code does it
- [ ] Every irreversible action has its mode in the Gates table
- [ ] It is clear **when the agent is finished** — measurably, not “once it works”

> If the Scenarios section cannot be filled in, the agent has not been thought through.
> That is not a reason to start coding and finish the thinking later. That is a reason
> not to start.

**How does the user find out what the agent can do?** A text interface has no buttons and
no menu. The user has no idea what they are allowed to say, so they guess — and when they
guess wrong they get a refusal without an explanation. The agent has to say it itself: on
first contact, and again every time it declines something (“I can't do that; I can do A,
B, C”). Without this, half the features go unused and the user is left feeling it does not
work.

---

## F1 — Verify the core against a real sample

**Goal:** measure the riskiest step before anything is built around it.

The riskiest step is the one most likely not to work: recognising intent from ugly input,
extracting from a poor scan, looking something up in a third-party API. Build the smallest
possible pass through it and run it on **real data**.

Measure three things, each as a number:

| Quantity | How |
|---|---|
| **Accuracy** | against a hand-transcribed truth, not by eye |
| **Cost** | per pass × the expected monthly volume |
| **Time** | at full input size, not on a clip |

**Gate**

- [ ] The core ran on a **real sample**, neither synthetic nor shortened
- [ ] Accuracy, cost and time are written down as numbers in `NAVRH.md`
- [ ] When the numbers are off, the project **stops or the brief changes** — it does not continue

> A short, synthetic sample lies systematically in your favour. For the transcriber, an
> estimate from a 70-second clip came out at 1.22× the duration; the reality on an
> hour-long show was 1.81× — real speech broke into 1,295 segments instead of 15, and each
> one costs extra overhead. The difference between a 68-minute and a 101-minute run.
> A sample lies about accuracy the same way: clean documents look excellent, right up
> until a photographed, crumpled receipt arrives.

---

## F2 — Skeleton and contracts

**Goal:** somewhere to build, and boundaries between modules.

- Copy the [agent skeleton](kostra-agenta/) and rename it
- Freeze the module contracts. A module does not reach into someone else's database — it
  gets a parameter
- Every module has a CLI and can be run without the rest of the system
- The test environment **has no outbound channels** — by configuration, not by an `if`

**Gate**

- [ ] `NAVRH.md` in the repository is filled in, not a blank template
- [ ] Every module can be run on its own from the command line
- [ ] In the test environment it is physically impossible to send an e-mail or a payment
- [ ] Tool calls can be switched off in tests **by configuration** (with an API that is
      the `tool_choice: none` parameter), not by a condition in the code
- [ ] No secrets in git, only `*.example`

---

## F3 — The deterministic backbone, still without a model

**Goal:** a process that runs to completion without ever asking a model.

Take scenario S1 and run it end to end with **hand-written input** — the kind the model
would otherwise produce. This is the part that carries consequences: the database write,
the payment, the send. It has to be finished and tested before the model gets access to it.

**Gate**

- [ ] S1 passes from start to finish with manual input
- [ ] When something goes wrong, the process **fails with a report** — not silently
- [ ] There are only two outcomes: it failed and you know, or it went well
- [ ] A repeated run does not do the thing twice (idempotence on irreversible steps)

---

## F4 — The model on its three jobs

**Goal:** add intent recognition, structure extraction and text synthesis. Nothing else.

- The prompt goes in `prompts/`, versioned like code, with the version number in the run record
- Generate the persona from source material and correct it; do not write it from memory
- Populate the [evals](kostra-agenta/evals/) — 20–40 real inputs
- Where numbers matter, add a cross-check with two independent passes

**Metrics that make sense for an agent.** “Passed / failed” is not enough — you need to
know *what* went wrong:

| Metric | What it measures | What a low value means |
|---|---|---|
| **tool recall** | did it call every step it should have? | it skipped a step |
| **tool precision** | did it avoid calling anything unnecessary? | it misread the intent |
| **parameter accuracy** | did it pass the right arguments? | right action, wrong number |
| **phrase recall** | does the output contain what it must contain? | a required phrase is missing |
| **task success** | did the whole scenario work out? | the sum of everything above |

The difference between “called the wrong tool” and “called the right tool with the wrong
amount” is the difference between confusion and damage. A single number will not tell you
which. For extraction, score field by field, not the whole output as one test.

**Gate**

- [ ] The evals run in CI and are above the threshold (classification 90 %+, extraction per field)
- [ ] A prompt change without an eval run does not land
- [ ] The model has no direct access to any irreversible action — only through the F3 process
- [ ] Hostile input does not push the agent off-scenario (see the design sheet)
- [ ] For borderline outputs the model returns **its own confidence** and asks when below threshold
- [ ] The share of cases escalated to a person stays under ~10 % — above that people go
      numb and start rubber-stamping

---

## F5 — Gates, limits, identity

**Goal:** bound what the agent may do on its own.

- Set the mode of each action by the **reversibility of the mistake**, not by trust in the model
- Limits: amounts, counts, frequency — and what happens when they are exceeded
- Identity from the channel (number, ID, webhook signature), never from a name in the text
- The agent discloses that it is an AI when writing outward — the AI Act requires it too

**The principle of least power.** A tool is a narrowly defined operation
(`issue_document(id)`), not a general gateway (`run_sql(query)`). A documented case: an
agent was given database access, “optimised performance” and deleted half the rows of a
production table. The model has no business composing queries — it gets buttons, not a
keyboard.

**Autonomy grows, it does not start at the top.** The human role shifts
*operator → reviewer → collaborator → supervisor*, and with it what the agent may do
alone. A new agent first prepares a draft; only later does it send it. The reverse order
gets punished: in 2024 Klarna replaced around 700 support staff with a chatbot, complaint
volume shot up, and in 2025 it was hiring people back. Just as important is the way back —
a means of taking authority away from the agent when it turns out it cannot handle it.

**Gate**

- [ ] An irreversible action above the limit cannot happen without human approval
- [ ] Impersonating another user is handled at the channel level
- [ ] A gate with no answer within X hours has defined behaviour
- [ ] Outgoing communication is labelled as written by an AI

---

## F6 — Failure, runbook, kill switch

**Goal:** so that a broken agent shows itself and can be stopped.

- Fill in the [runbook](kostra-agenta/runbook.md): shutdown, common faults, recovery
- A crash report goes **to a person**, not just to a log
- The kill switch is one action. Tested, not theoretical

**Four ways human oversight fails.** They are documented and are planned for:

| Failure | How it shows |
|---|---|
| **Blind trust in the automation** | the person stops reading the output, “it has always been right so far” |
| **Alert fatigue** | the important warning is lost among ten unimportant ones |
| **Skill loss** | after a year of automation the person can no longer step in manually |
| **Diverged interests** | the agent pushes for speed, the person needs certainty |

Therefore: report little and specifically. And with every escalation supply context — what
the agent tried, why it gave up and what exactly the person is being asked to decide. An
escalation without context is just passing the work along.

**Gate**

- [ ] The agent stops with one action and you have verified it
- [ ] A simulated process crash reaches the owner within minutes
- [ ] The agent's silence is distinguishable from “there was nothing to do”
- [ ] Restoring from backup has been rehearsed at least once

---

## F7 — Deployment

**Goal:** an operation where it is visible what is running.

- Put the commit hash in the build so the running version is identifiable
- Observability: how many passes, how many failures, how much it cost
- **Check every output by hand for the first week** before it goes out
- Run a new version **shadowed alongside the live one** first — same inputs, the output is
  discarded and only compared. Only then on a small share of traffic

**Error, or variance?** A model is probabilistic, so a different output is not yet a fault.
The rule: run the same input **3–5×**. If it fails in over 80 % of runs, it is a systematic
error and goes to be fixed. If it fails one time in four, it is variance — log it and watch
the trend. Without this rule you either chase ghosts or miss a real regression.

**Gate**

- [ ] The version and date are visible on the deployment
- [ ] A week of running costs matches the F1 estimate (within reason)
- [ ] The manual review of the first week found nothing that could have gone out quietly

---

## F8 — Operation and growth

**Goal:** so the agent improves, but not by itself.

- Every production error → a new case in the evals. After a year you have material that
  cannot be bought
- **Store the successful passes too**, not only the failures — they become a reference
  “golden path” against which a regression is recognisable
- Learn from your own corrections, not from metrics
- The prompt is **never rewritten automatically**
- Every change to a prompt or a tool records: what was observed, what was changed, and how
  you will know it helped

**An agent rarely crashes — it more often degrades quietly.** So watch distribution shift
as well as error rate. The cheapest measure: the share of each category (which scenarios
fire, which tools get called) against a baseline week.
A difference **below 0.1 relax · 0.1–0.25 watch · above 0.25 intervene** (the PSI index).
Add the implicit signals from people: how often they ask again in different words, and how
often they give up halfway. Both arrive before a complaint does.

**Gate (recurring, not one-off)**

- [ ] The eval set grows with operation
- [ ] Prompt changes get review like code changes
- [ ] Every so often: does the scenario list still hold, or has the agent crept somewhere?

---

## What a small agent may skip

The specification is a maximum. For a simple agent built for yourself, **F0, F1, F3 and
F6** stay mandatory — design, verification of the core on real data, the deterministic
backbone and the kill switch. The rest can be trimmed:

| Phase | Trimmed to |
|---|---|
| F2 | a flat structure instead of the skeleton; with one or two modules the contracts can stay in your head |
| F4 | evals run by hand over ten cases instead of in CI |
| F5 | a single global limit instead of a table of modes |
| F7 | no commit hash, but still with the manual review of the first week |

What can **never** be skipped: the real sample in F1, the two outcomes in F3 and the kill
switch in F6. These are the three whose missing versions are recognised only from the
damage.
