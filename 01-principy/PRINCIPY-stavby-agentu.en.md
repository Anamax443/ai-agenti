# PRINCIPLES OF BUILDING AI AGENTS

General methodology, applicable to any agent in any domain. It grew out of an analysis
of Skippy (Marek Bartoš, the *Keci a politika* podcast) and out of design work on our
own projects.

Version 1.0 · August 2026 · Czech original: [PRINCIPY-stavby-agentu.md](PRINCIPY-stavby-agentu.md)

---

## 1. The founding principle

> **AI recognises. Code executes.**

This is the one sentence almost everything else follows from. A model is good at working
out what an unstructured input is about. It is bad as an executor, because its output is
not guaranteed and cannot be debugged.

When an agent receives an e-mail with an invoice, the model has exactly one job: to
recognise that this is an invoice. Its role ends there. Transcription, validation,
matching against a supplier and sending the payment are a fixed process that no model
reasons about.

The same idea produces the security property that makes the whole thing worth doing:

> Every attempt ends in an **observable** state: known success, known failure, or a
> recorded unknown outcome.
> **There is no silent branch.**

An agent that decides for itself how to carry out a task does not have this property.
It can succeed, fail, or do something nobody asked for — and nobody finds out. That
silent branch is the source of most of the “the assistant e-mailed fifty people” stories.

**Why three states and not two.** Until 1 Sep 2026 this read “either it fails with a
report or it goes well; there is no third possibility”. For a remote call that does not
hold: the send goes through, the reply is lost, and the agent does not know whether to
retry. The outcome is neither known success nor known failure — it is **unknown**, and
that is a proper state, not a defect. The defect is hiding it or blindly retrying: the
first loses the effect, the second does it twice. An unknown outcome therefore has its own
next step — query the target system, retry idempotently, or queue it for a person. The
original sentence stays true in what it meant: **no ending may be silent.**

---

## 2. The test: does this belong to the model, or to the code?

For every activity in the system, ask four questions:

| Question | An answer of “yes” means |
|---|---|
| Can it be written as `if`–`then`? | code |
| Is the input structured (JSON, form, database)? | code |
| Must the result be identical every time? | code |
| Is the input free text, speech, an image, or a human intention? | model |

The three most common jobs for a model:

1. **Intent recognition** — “what does this person want from me”
2. **Structure extraction** — turn a sentence or a document into JSON
3. **Text synthesis** — write something that should sound like a person

Everything else is usually code. When you are unsure, try describing the task to a
colleague as a procedure. If you can do it without saying “and then it sort of judges
it”, it is code.

### Why this matters economically

A deterministic process costs a fraction of what a model costs. Bartoš puts his agent at
around five thousand crowns a month; pushing the same work through AI would cost tens of
thousands. The difference is not in the model, but in how much work it is given at all.

---

## 3. Anatomy of an agent

```
┌─ INPUT CHANNELS ─────────────────────────────────────┐
│  chat · voice · e-mail · webhook · sensor · cron     │
└──────────────────────┬───────────────────────────────┘
                       ▼
┌─ INTENT RECOGNITION ─────────────────────────────────┐
│  model: what is this? → one of the known scenarios   │
│  unknown intent → ask a person, never improvise      │
└──────────────────────┬───────────────────────────────┘
                       ▼
┌─ MAIN MIND ──────────────────────────────────────────┐
│  memory · context · persona · permissions            │
│  decides WHAT runs, not HOW it runs                  │
└──────────────────────┬───────────────────────────────┘
                       ▼
┌─ FIXED PROCESSES ────────────────────────────────────┐
│  deterministic code · validation · idempotence       │
│  optionally a small subagent for a narrow task       │
└──────────────────────┬───────────────────────────────┘
                       ▼
┌─ GATES ──────────────────────────────────────────────┐
│  limits · human approval · cross-check               │
└──────────────────────┬───────────────────────────────┘
                       ▼
┌─ OUTPUT CHANNELS ────────────────────────────────────┐
│  message · publication · write to a system · payment │
└──────────────────────────────────────────────────────┘
```

### The main mind and subagents

One main instance holds memory and context. Partial work is done by small, cheap models
with a narrow brief — Skippy has a separate “part of the brain” for invoices. A subagent
has access neither to the whole memory nor to the full permissions. It gets only what its
task requires.

This is not merely a saving. A subagent with limited context has no way to go wrong in a
manner you would not even know about.

---

## 4. The persona as an artefact

A persona is not a luxury, it is a saving of context. Instead of twenty instructions
about tone, one reference to a character description is enough.

**How to produce one:** do not assemble it by hand. Collect source material — for Skippy
it was e-books featuring a literary character, for a band it is song lyrics, existing
posts and the bio, for a company agent it is internal communication and manuals. Have the
model write an analytical description, then correct it by hand.

The description should also include a **negative definition** — what to avoid, which
clichés not to use. That part tends to be more effective than a list of desirable traits.

The persona propagates into subagents too; otherwise the system speaks with two voices.

---

## 5. Inputs and peripherals

An agent is only as usable as it is easy to talk to. An interface that requires opening a
laptop will not be used.

| Channel | What it suits | What to watch for |
|---|---|---|
| **Chat (Telegram, WhatsApp)** | the main two-way channel | identity by ID, not by name |
| **Voice message** | input while walking, in a car | transcribe with whisper, then treat as text |
| **E-mail** | incoming tasks from strangers | always via intent recognition, never straight into a process |
| **Webhook** | events from other systems | verify the signature, be idempotent |
| **Cron** | scheduled and repeated work | must survive being run twice |
| **Sensor / location** | context without asking | location and time imply the situation |
| **Glasses, watch** | output without pulling out a phone | short messages only |

**Choosing the channel to fit the situation.** Skippy can tell from location and speed
that the user is driving, and sends a voice message instead of text. This is cheap to
implement and raises usability out of all proportion.

**Chat beats a form.** On a phone, dictating a sentence is faster than filling in six
fields. The model turns the sentence into structure and the agent shows it for approval.
Build a form only when the agent has to be operated by someone who is not in the chat.

---

## 6. Permissions and identity

**Identity is bound to the channel, not to a name.** Phone number, Telegram ID, a signed
webhook. Anyone can write “this is Nikola” — but not from her number.

The permission model:

```
who (identity)  ×  what (action)  ×  how much (limit)  =  allowed / escalation
```

Practical rules:

- **Whitelist, not blacklist.** Anyone not listed has no access.
- **Different people, different rights.** In Skippy's case his wife has broader
  permission to rearrange the calendar than he does.
- **Foreign input never triggers an action directly.** An e-mail from an unknown sender
  passes through intent recognition and ends up in the daily digest, not in a process.
- **The agent admits it is an AI** when it writes outward **without human approval**. For a
  reply a person has read and approved, the responsibility is theirs and the label is their
  choice. The legal minimum differs by role and jurisdiction; this is our rule, not a
  quotation of the law.
- **Outgoing identity: a known channel, an own key.** Reply from the channel the other side
  knows (otherwise threading and deliverability fall apart), but **under the agent's own
  credential**, revocable on its own. Switching the agent off is then one action, not a
  change of your password.
- **A shared model is a shared context.** In a multi-tenant system one customer's context can
  end up in another's answer through a prompt cache, shared case memory or the model ladder. No
  attacker is needed, only carelessness. Tenant scoping therefore belongs **in the query**, not
  in the prompt — it is a hard criterion like any other.
- **For every channel it must be clear whose data it is.** A company mailbox is not your
  mailbox: the agent writes in the company's name and reads other people's data. When the
  owner of the data is not the owner of the agent, it must be recorded who gave consent and
  for what scope.

---

## 7. Gates: when to ask a person

What decides is not how much you trust the model, but **how expensive the mistake is.**
Bartoš lets invoices be paid without approval because money sent to a known supplier can
be recovered. Not because he trusts the AI.

**Risk has two axes and you need both.**

### The action axis — reversibility. It sets the **mode** of each individual action.

| Reversibility of the mistake | Mode | Example |
|---|---|---|
| Full, within minutes | act alone, just report | calendar entry, e-mail label |
| Financial, recoverable | fixed process + limit | payment to an approved supplier |
| Irreversible reputationally | **always approve** | public post, e-mail to an outside party |
| Irreversible physically | approval + second channel | device control, deleting data |

The test for every action: *what happens if it gets it wrong, and how long does it take
to undo.* The answer sets the mode.

### The system axis — impact. It sets the **strictness** with which everything is verified.

| Question | Strictness grows from left to right |
|---|---|
| **Who is the decision about?** | a person outside the company › a customer › a colleague › only you |
| **What does the decision affect?** | employment, credit, health, law, safety › money › convenience |
| **On what data?** | personal, health, secret › company › public |
| **At what scale?** | thousands of cases › dozens › single ones |
| **Is a mistake noticed in time?** | only at the other end › during a spot check › immediately |

The answers produce one of three levels:

- **N — normal:** no answer from the left-hand side. A personal tool, an internal aid.
- **Z — raised:** at least one answer from the left-hand side.
- **V — high:** a decision **about a person** (employment, credit, health, law, safety),
  or personal data at scale.

**Why one axis is not enough.** An agent that only reads CVs and proposes a ranking has no
irreversible action at all — on the action axis that is the lowest mode, "act alone, just
report". Yet it decides who gets an interview: for the person filtered out, the mistake is
irreversible, and it shows up only as never being invited. Conversely, "a high-impact
agent" says nothing about which of its forty calls needs approval. **The action axis sets
the mode, the system axis the strictness. Either one alone is blind.**

### What strictness changes

A level with no consequence is decoration. Hence, explicitly:

| | **N** | **Z** | **V** |
|---|---|---|---|
| Abridging phases (build spec) | allowed | **not allowed** | not allowed |
| Evals (F4) | per the gate | + hard negatives mandatory | + the set is reviewed by someone else |
| A finding may be closed at level | U1 (in the code) | **U2** (covered by a test) | **U3** (provoked in an environment) |
| Crash reporting (F6) | to the owner | to the owner and a deputy | + a deadline by which someone must respond |
| Oversight (F5) | per reversibility | per reversibility | **+ a person on every decision about a person, even a reversible one** |
| Reviewing the scenario list (F8) | now and then | every six months | quarterly |

The last row under **V** is the one that matters: for a decision about a person,
reversibility does not decide. A record can be undone; being passed over cannot.

**Two gates instead of one.** For repeated work, approve the plan once for the whole
series and then only the individual irreversible steps. This saves clicking without
losing control.

---

## 8. Cross-checking

Where accuracy genuinely matters, have the task done **twice independently and compare.**

In Skippy's case an invoice is transcribed by Mistral OCR and independently by Gemini.
Both models then have a single job — find the differences between their outputs. When
they agree, it is almost certainly right. When they do not, a person is asked.

Where it pays off: numbers, dates, amounts, names, identifiers. That is, everywhere a
mistake cannot be spotted at a glance and only surfaces later.

Where it does not: text synthesis. Two different phrasings are not a disagreement.

---

## 9. Memory

Distinguish three layers — they get confused, and each behaves differently:

| Layer | Contents | Where it lives |
|---|---|---|
| **Durable** | persona, rules, permissions | a file in the repository |
| **Factual** | events, contacts, history | a database |
| **Working** | the conversation in progress | the model's context |

Factual memory **does not belong in the prompt wholesale.** The agent requests only what
the task needs. Otherwise both cost and error rate grow over time.

Whatever the agent stores for itself, it should store structured. Free-form notes in
natural language become unusable after six months.

---

## 10. Proactivity

An agent that only answers is a tool. An agent that speaks up on its own is an assistant.
The difference is usually a few lines.

Sources of proactivity:

- **Time-based** — a morning digest, a reminder before a meeting
- **From a gap** — “you were at that company and said nothing, shall I ignore it?”
- **From a threshold** — something crossed a limit and is worth a message
- **From the surroundings** — a new article, a change, an event in a watched source

The dose is what matters. An agent that pesters gets switched off. A good rule: speak up
when **a question or a task follows from it** — not merely when something happened.

---

## 11. Failure and observability

- **Silent failure is the worst variant.** When a process crashes, a message must arrive.
  An agent that says nothing looks exactly like an agent that is working.
- **Idempotence.** Every channel delivers more than once. Key off the message ID, not the
  content.
- **An irreversible action sits on a transition, not inside a state.** A send, a payment and
  a write into someone else's system are not states, they are the edges between them. Draw it
  that way and you have to answer "what if the transition fails halfway" — which is exactly
  where a lost message and a double execution come from.
- **An unknown outcome is a state, not an error.** The remote call goes through, the reply
  is lost — the agent does not know what happened. That state is **recorded** (`unknown`,
  `reconciliation_required`) and resolved by querying the target system, retrying
  idempotently, or queueing it for a person. Never by a blind retry, and never as `ok`.
- **Expiry.** Waiting for approval has a deadline; after it the task is dropped and
  announced.
- **The log contains decisions, not just results.** In a month there will be no other way
  to find out why the agent ran this particular process.
- **A kill switch.** There must be a way to stop the agent with one message.

---

## 12. Improvement

The most valuable feedback is not metrics, it is **your own corrections.** Whenever the
agent proposes something and you edit it before approving, that difference is precise
information: “not like this, like this.” Store both versions.

How much you intervene over time is itself a diagnostic: when it rises, something has
drifted — usually the persona or the brief, not the model.

**Never apply prompt changes automatically.** Have a new version proposed with a
justification, read it, and approve it. An automatic loop on a small sample runs off in
the wrong direction and you find out too late.

Version the brief and the persona, do not overwrite them. Otherwise you cannot trace
which version produced the output that worked.

---

## 13. Modular decomposition

An agent is not built as a whole. It is built as a set of modules that can be tested
separately, and only then connected.

Every module has:

1. **A contract** — input and output, written down, in advance
2. **Its own CLI** — runnable without the rest of the system
3. **Tests** — unit tests on the logic, integration tests on the output
4. **A gate** — the conditions that must hold before it is declared finished

Contracts are frozen **before the first line of code.** When M1 returns a string and M2
expects an object, both get rewritten.

A module does not reach into someone else's database. It receives data as a parameter.
Otherwise it cannot be tested with substituted inputs and integration turns into
debugging everything at once.

**Order:** first the modules that need no external access and whose output can be checked
by eye. Those give you the fastest confidence that this is going to work.

Once connected, do not test everything at once. Run **vertical slices** — one narrow path
from input to output, then the next.

---

## 14. Design sheet for a new agent

Fill this in before you write any code. If it cannot be filled in, the agent has not been
thought through.

```
NAME:
WHAT IT IS FOR:       one sentence, concrete

INPUT CHANNELS:       where it receives prompts from
WHO MAY:              identities and their permissions

SCENARIOS:            a closed list of what it can do
  S1 …                trigger → steps → output
  S2 …
  unknown intent →    ask a person

ROLE OF THE MODEL:    exactly which steps, nothing more
  □ intent recognition
  □ structure extraction
  □ text synthesis
DETERMINISTIC:        everything else, enumerated

GATES:
  action             reversibility   mode
  ───────────────────────────────────────────
  …                  …               auto / limit / approval

CROSS-CHECK:          where two sources verify each other
LIMITS:               amounts, counts, frequency

MEMORY:
  durable:            persona, rules
  factual:            what goes into the database
  what is NOT stored: sensitive data

PROACTIVITY:          when it speaks up on its own
FAILURE:              who finds out, and how
KILL SWITCH:          how it is stopped

MODULES:              M1 … Mn with contracts
BUILD ORDER:          what comes first, what blocks what
```

---

## 15. Anti-patterns

| Anti-pattern | Why it is wrong |
|---|---|
| **An agent with free access to every tool** | decides about things it has no context for; the silent failure branch |
| **AI where an `if` would do** | expensive, slow, unreliable |
| **Trust instead of reversibility** | “I trust the model” is not a security measure |
| **Identity from a name in the text** | anyone can claim to be anyone |
| **The whole memory in the prompt** | cost and error rate grow over time |
| **Silent failure** | a broken agent looks like a working one |
| **An unknown outcome recorded as success** | a lost reply hides inside `ok`; the damage shows up at the other end |
| **Automatic prompt rewriting** | it drifts and nobody notices |
| **Integration before the modules are tested** | you are debugging two unknowns at once |
| **A persona hand-written in ten minutes** | flat, generic, useless |
| **A form instead of chat on a phone** | it will not be used |

---

## 16. One-page summary

1. AI recognises, code executes.
2. Every ending is visible: success, failure, or a recorded unknown outcome. The silent branch must not exist.
3. The model gets three kinds of job only: intent, structure, text.
4. The persona is generated from sources, not written from memory.
5. Identity is bound to the channel, not to a name.
6. The approval mode is set by the reversibility of the mistake, not by trust in the model.
6b. Reversibility sets the mode of an action, impact on people sets the strictness of the whole. You need both axes.
7. Where accuracy matters, verify with two independent passes.
8. Chat on a phone beats a form.
9. An agent that stays quiet when it crashes is worse than no agent.
10. Learn from your own corrections, not from metrics. And never automatically.
11. Modules with contracts, then gates, then integration.
12. Fill in the design sheet before you write the first line.
