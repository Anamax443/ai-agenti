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
| **Critical path** | F0 → F1 → F3 → F6 |
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
- [ ] **The strictness (N/Z/V) is derived from the answers in the design sheet**, not
      guessed — and what follows from it is written down (see
      [principles §7](../01-principy/PRINCIPY-stavby-agentu.en.md))
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

**An observable outcome is proven by provocation, not by assertion.** Unit tests over pure
functions cannot reach here: the defect is rarely in a step, it is in the orchestration
around it.
A documented case — in JobWatch, 159 tests, 15 region checks and 26 evals missed four defects at
once: a total source failure ended as a green run, an unsent notification was never retried, two
concurrent runs overwrote each other's stop flag, and a stopped run looked successful in history.

**List the states and the allowed transitions.** "An observable outcome" is a claim about
the result; a state model is **the artefact you can check it against**. Without one there is
no saying what an ending is: `ok = 1` written by the closing step is a write, not a finish.

The rule everything else follows from: **an irreversible action always sits on a transition,
never inside a state.** A send, a payment, a write into someone else's system are not states
— they are the edges between them. Once you draw it that way, you have to answer the question
that otherwise gets skipped: *what if the transition fails halfway?*

| The question a state model answers | What it prevents |
|---|---|
| Where is the state between "written" and "sent"? | the score stored, the message unsent — and the queue never comes back to it |
| Who owns the run, and what may a second run do? | two concurrent runs overwrite each other's state; the second clears the first one's stop flag |
| Which states are terminal? | a stopped run that the closing write flips back to success |
| What happens to an unknown outcome? | the call went through, the reply was lost — and nobody knows whether to retry |

All four right-hand cells are documented defects of one single agent. They did not come from
carelessness: **each of those functions behaves correctly on its own.** The defect lives in
the relation between them, and that only becomes visible on the diagram.

Patterns for this exist — outbox, lease, idempotency key, a dead-letter queue. The
specification does **not** prescribe them: code does not belong here, and a pattern bound to
a language and a platform ages faster than the question does. It prescribes the answers to
those four questions. Whoever knows them will find the pattern; whoever does not will misuse
it anyway.

**Gate**

- [ ] S1 passes from start to finish with manual input
- [ ] If the agent has at least one irreversible action: **the states and allowed transitions
      are listed** in the design sheet, and **every irreversible action sits on a transition**,
      not inside a state
- [ ] For every transition carrying an irreversible action it is written down **what happens
      if it fails halfway**
- [ ] When something goes wrong, the process **fails with a report** — not silently
- [ ] Every ending is **observable**: known success, known failure, or a recorded unknown
      outcome — no silent branch
- [ ] An unknown outcome (the call went through, the reply was lost) has its own state and
      next step: query the target system, retry idempotently, or queue it for a person.
      Never a blind retry, and never written as `ok`
- [ ] A repeated run does not do the thing twice (idempotence on irreversible steps)
- [ ] Every outcome is **provoked by an acceptance test**, not merely described: all sources down ·
      failure after the write and before the send · **a timeout after the send and before the
      write** · two concurrent runs · a stop mid-run
- [ ] Two runs cannot overwrite each other's state — either a second run cannot start, or a run
      holds a lease

---

## F4 — The model on its three jobs

**Goal:** add intent recognition, structure extraction and text synthesis. Nothing else.

- The prompt goes in `prompts/`, versioned like code, with the version number in the run record
- Generate the persona from source material and correct it; do not write it from memory
- Populate the [evals](kostra-agenta/evals/) — 20–40 real inputs, **hard negatives included**
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

**A set without hard negatives only measures itself.** A negative the deterministic filter throws
away says nothing about the model — the model never sees it. Only a negative that survives the
filter, one the model itself must reject, carries information. A documented case: JobWatch has 17
negative cases and the prefilter rejects all 17, so its stated precision of 100 % says nothing
about the ability to discriminate.

**Gate**

- [ ] The evals are above the threshold (classification 90 %+, extraction per field) and **measure
      the rung that decides in production**: if the backend is reachable from CI, they run in CI;
      if it exists only at runtime (a binding, secrets only in production), they run against the
      deployed version, by hand, with a protocol, and the run records which rung answered. Until
      such an eval has run, a deployment is a **candidate**, not an approved version
- [ ] The set contains **negative cases that survive the deterministic filter** — otherwise it does
      not measure the model's ability to refuse
- [ ] A prompt change without an eval run does not land — the gate watches the **eval run**, not
      merely a version bump
- [ ] Foreign text is delimited and marked as untrusted data **at every model call**, not just the
      main one — and first where the model holds tools
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

- [ ] The agent stops with one action and you have verified it **while it was running**, not on an idle system
- [ ] A simulated process crash reaches the owner within minutes
- [ ] The agent's silence is distinguishable from “there was nothing to do”
- [ ] Restoring from backup has been rehearsed at least once
- [ ] A stopped run stays stopped: the closing write does not flip it back to success, and a
      concurrent run cannot clear its stop flag

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

The specification is a maximum. **But you do not get to slim it down because the agent
feels small to you.** What decides is a pair of answers from the design sheet:

> You may simplify only when **both** hold:
> 1. the strictness is **N** (the system axis,
>    [principles §7](../01-principy/PRINCIPY-stavby-agentu.en.md)),
> 2. no action of the agent is irreversible reputationally or physically (the action axis).
>
> If only one holds, everything **except F4 and F5** may be slimmed down.
> If neither holds, the specification applies in full.

This replaces the earlier “a simple agent built for yourself”. That category was
subjective and was decided by the person with an interest in simplifying — every author
knows their own agent and considers it simple, because they know its **intent**.
Reversibility and impact do not know the intent, only the consequence.

At strictness N, **F0, F1, F3 and F6** stay mandatory — design, verification of the core on
real data, the deterministic backbone and the kill switch. The rest can be trimmed:

| Phase | Trimmed to |
|---|---|
| F2 | a flat structure instead of the skeleton; with one or two modules the contracts can stay in your head |
| F4 | evals run by hand over ten cases instead of in CI |
| F5 | a single global limit instead of a table of modes |
| F7 | no commit hash, but still with the manual review of the first week |

What can **never** be skipped: the real sample in F1, the observable outcome in F3 and the
kill switch in F6. These are the three whose missing versions are recognised only from the
damage.
