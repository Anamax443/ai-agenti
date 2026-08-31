# DESIGN SHEET — <agent name>

Fill this in before you write the first line of code. If it cannot be filled in — the
*Scenarios* section above all — the agent has not been thought through and should not
be built.

Czech original: [navrhovy-list.md](navrhovy-list.md)

---

## Basics

| | |
|---|---|
| **Name** | |
| **Owner** | a specific person |
| **What it is for** | one sentence, concrete |
| **What it replaces** | what is done by hand today |
| **When it is finished** | measurably |

---

## Inputs

| Channel | Who may use it | Identity verification |
|---|---|---|
| | | |

Identity is bound to the channel (phone number, ID, webhook signature), never to a name
in the text.

---

## Hostile input

An agent that reads e-mails, documents or web pages receives text from people who did not
write it for the agent. Some of them will try to redirect it.

| Channel | Who can write there | What its content must never reach |
|---|---|---|
| | | |

- [ ] Content from outside is **data for the model, not instructions** — separated in the prompt
- [ ] Hidden text (white type, metadata, comments) is stripped before the model
- [ ] An irreversible action is never triggered by what was written in the input
- [ ] Suspicious input has its own scenario ending: stop and ask

The rule: the more permissions an agent has, the less it may believe what it reads.

Before you design this for the first time, try an attack yourself — free and in half an
hour: [Gandalf](https://gandalf.lakera.ai) (Lakera), [Red](https://red.giskard.ai)
(Giskard), [Prompt Airlines](https://promptairlines.com) (Wiz). Writing a defence against
something you have never tried to break is guessing.

---

## Regulation and data

| Question | Answer |
|---|---|
| Does it disclose it is an AI when communicating outward? | mandatory (AI Act) |
| Does it process personal data? | what, whose, on what legal basis |
| Risk category (AI Act) | minimal / limited / **high** |
| Retention — what is deleted and when | |
| Where the data physically sits | |

High risk covers, among other things, personnel selection, assessment, and access to
services. The specification is not abridged for those.

---

## Scenarios

A closed list. Extending it means adding a scenario and a process for it, not giving the
model more freedom.

| Code | Trigger | Steps | Ending |
|---|---|---|---|
| S1 | | | |
| S2 | | | |
| — | anything else | does not improvise | ask a person |

---

## Division of labour

**The model does:**
- [ ] intent recognition
- [ ] structure extraction
- [ ] text synthesis

**The code does:** _(enumerate everything else)_

The test for each step: can it be written as `if`–`then`? Is the input structured? Must
the result be identical every time? → code.

---

## Gates

| Action | If it gets it wrong | How long it takes to undo | Mode |
|---|---|---|---|
| | | | auto / limit / approval |

The mode is set by the reversibility of the mistake, not by trust in the model.

---

## Cross-check

Where the same task is done twice independently and compared:

| Step | Source A | Source B | What is compared | On disagreement |
|---|---|---|---|---|
| | | | | |

Suits numbers, dates, amounts, identifiers. Does not suit text.

---

## Limits

| Quantity | Cap | What happens when exceeded |
|---|---|---|
| | | |

---

## Memory

| Layer | Contents | Where |
|---|---|---|
| Durable | persona, rules, permissions | repository, versioned |
| Factual | | database |
| Working | | run context |
| **Not stored** | | |

---

## Proactivity

When it speaks up on its own:

- [ ] time-based — when:
- [ ] from a gap — what it notices:
- [ ] from a threshold — what limit:
- [ ] from the surroundings — which source:

The rule: speak up when a question or a task follows from it. Not merely when something
happened.

---

## Failure

| Situation | Who finds out | How |
|---|---|---|
| the process crashed | | |
| the model is unavailable | | |
| a gate with no answer within X h | | |

**Kill switch:** _(how the agent is stopped with one action)_

---

## Modules

| ID | Module | Contract (input → output) | Depends on |
|---|---|---|---|
| M1 | | | — |
| M2 | | | |

Contracts are frozen first. A module does not reach into someone else's database; it
receives data as a parameter.

---

## Build order

1. _(what needs no external access and can be checked by eye)_
2.
3.

**Vertical slices once the modules are done:**

| # | Slice | Modules |
|---|---|---|
| I1 | | |

---

## Cost

| Item | Per month |
|---|---|
| model calls | |
| infrastructure | |
| **time to build** | hours |
| **time to maintain** | hours per month |
