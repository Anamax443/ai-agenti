# AGENTS FOR A SMALL OFFICE

A portfolio of agents, shared infrastructure and operating practice. Built on the principle
“AI recognises, code executes” and on ordinary DevOps habits carried over to working with
models.

Version 1.0 · August 2026 · Czech original: [AGENTI-mala-kancelar.md](AGENTI-mala-kancelar.md)

---

## Part A — Which agents to build

### Order by benefit-to-risk ratio

| # | Agent | Saves | Risk of error | Build |
|---|---|---|---|---|
| 1 | **Mail and helpdesk triage** | 30–60 min a day | low, it only sorts | 3 days |
| 2 | **Documents and invoices** | 2–4 h a month | medium, money | 5 days |
| 3 | **Deadline and contract watcher** | prevents penalties | low | 2 days |
| 4 | **Meeting minutes** | 1–2 h a week | low | 3 days |
| 5 | **Operational alert triage** | noise in the mailbox | medium, something gets missed | 4 days |
| 6 | **Onboarding and offboarding** | 1–2 h per person | high, permissions | 8 days |

Build in this order. The first three touch nothing irreversible and put in place the shared
infrastructure the rest will run on.

---

### 1 · Mail and helpdesk triage

The best first agent. It changes nothing, it only sorts — and still saves the most.

**Input:** the shared mailboxes `podpora@`, `it@`
**The model does:** classification (category, urgency, who should handle it) and a
three-sentence summary
**The code does:** creating the ticket, assignment, notification, thread deduplication
**Gates:** none — nothing is irreversible. A misfiled item is fixed by a person in one click.

```
mail → [model: category + priority + summary] → code: ticket, assignment, alert
                                              → morning digest: what came in, what is waiting
```

Do not let it reply to customers. Have it draft a reply for somebody else to send. A reply
is irreversible; filing is not.

---

### 2 · Documents and invoices

Written up in detail in a separate design sheet. In summary:

**The model does:** recognises that this is a document, and transcribes the contents twice
independently
**The code does:** compares both transcriptions, matches the supplier by account number,
checks the limit, writes it into the accounting system
**Gates:** the transcriptions disagree → ask; a new supplier or an amount over the limit →
approval

In a small company I would **not go as far as payment.** The end of the process is a
prepared document in the accounting system with an approval step that stays human. The
difference in time saved is small; the difference in risk is large.

---

### 3 · Deadline and contract watcher

The cheapest agent with the best ratio. Most of the work is a one-off data load.

**The model does:** extracts the end date, notice period and amount from a contract or
invoice
**The code does:** watches the calendar, warns ahead of time according to the type
**Gates:** none, it only warns

Watch: licences, support contracts, insurance policies, leases, inspections, certificates,
domains, API token validity. That last one comes back to bite you on the agents themselves.

---

### 4 · Meeting minutes

**Input:** a recording or a voice message
**The code does:** transcription via whisper — locally; recordings of meetings do not belong
in someone else's service
**The model does:** the summary, decisions, tasks with owners
**Gates:** the minutes go for approval to whoever chaired the meeting, and only then get
circulated

You already have the transcription module. This is a layer on top of it.

---

### 5 · Operational alert triage

**Input:** alerts from monitoring, antivirus, backup, network devices
**The model does:** summarises what happened and estimates severity
**The code does:** deduplication, thresholds, escalation, silence at night for anything
non-critical
**Gates:** it fixes nothing on its own

The trap: an agent that is supposed to “resolve” an incident. It is not. Its job is to turn
fifty alerts into three sentences and say which single one is worth attention.

---

### 6 · Onboarding and offboarding

The highest risk in the whole portfolio, because it touches permissions.

**The model does:** extracts the name, position, start date and department from the request
**The code does:** everything else — account, groups, mailbox, licences, shared folders
**Gates:** approval before creation, a second approval for permissions beyond the template

Keep an employee's departure as a **fully deterministic process with no model.** The input
is a name and a date, nothing more. Permissions wrongly removed hurt; permissions wrongly
left in place hurt more.

---

## Part B — What to build once for everyone

Six agents does not mean six systems. They share most of the layers:

```
┌──────────────────────────────────────────────┐
│  CHANNELS    chat · mail · webhook · cron    │
├──────────────────────────────────────────────┤
│  IDENTITY    whitelist, roles, permissions   │
├──────────────────────────────────────────────┤
│  GATES       approvals, limits, deadlines    │
├──────────────────────────────────────────────┤
│  MODELS      calls, retry, cross-checking    │
├──────────────────────────────────────────────┤
│  RECORDS     runs, decisions, corrections    │
├──────────────────────────────────────────────┤
│  REPORTING   errors, digests, metrics        │
└──────────────────────────────────────────────┘
        ▲          ▲          ▲
     agent 1    agent 2    agent 3
```

**The approval layer is shared.** One message format, one table of pending tasks, one place
where approving happens. When every agent solves it its own way, six months later nobody
knows what is waiting where.

**The run records too.** One table: who, when, what they started, how it turned out, what a
person corrected. Everything else is built from it.

---

## Part C — Repository and versioning

### Monorepo

```
office-agents/
├─ packages/
│  ├─ core/            channels, identity, gates, records
│  ├─ models/          model calls, retry, cross-checking
│  └─ types/           shared types — frozen first
├─ agents/
│  ├─ triage-mail/
│  ├─ invoices/
│  ├─ deadlines/
│  └─ …                each with its own prompts/ and evals/
├─ prompts/
│  ├─ identity/        the company's tone and style, shared
│  └─ …
├─ evals/              regression sets
├─ infra/              database schema, migrations, configuration
├─ runbooks/           what to do when something happens
└─ .github/workflows/  or .gitlab-ci.yml
```

One repository. The agents share types and the core; in separate repositories they drift
apart within a month.

### A prompt is code

This is the main difference from an ordinary project, and the place small companies most
often cut corners.

- Prompts, personas and tool definitions **live in the repository**, not in some tool's UI
  and not in a database nobody versions.
- A prompt change goes through **the same review as a code change.** Pull request, a second
  pair of eyes, a description of why.
- A prompt has a **version** and every run records it. Without that you cannot trace which
  version produced the output that worked.
- The model and its version live in configuration, not hard-coded. When the provider retires
  a model, you change one line.

### Branches

A small company, one or two people: short branches off `main`, PR, squash merge. No
git-flow — with two developers it is overhead without benefit.

The commit conventions (`feat:`, `fix:`, `prompt:`) pay off because `prompt:` marks out the
changes that cannot be covered by a unit test.

---

## Part D — CI/CD

```
push to a branch
   │
   ├─ lint + types
   ├─ unit tests              (logic, gates, limits)
   ├─ eval set                (the AI parts — see below)
   ├─ secret scan             (blocking)
   └─ build
   │
merge to main
   │
   ├─ deploy to stage
   ├─ smoke tests against stage
   │
   └─ manual approval → production
```

**Keep the manual gate before production even in a small company.** Deploying an agent that
touches e-mail and money is not the same as deploying a website.

**The environments must be separate.** Stage has its own mailbox, its own test data, and
**must not be able to send anything out.** The most expensive mistake while developing an
agent is sending test messages to real people — disable the outbound channels at the
configuration level, not with an `if`.

**Secrets:** GitHub Actions secrets or GitLab CI variables; into production through Workers
Secrets. Never in the repository. Turn on secret scanning and add a `pre-commit` hook —
committed credentials are removed from history very poorly.

**Dependencies:** Dependabot or Renovate, automatic PRs, merged once CI is green.

---

## Part E — Evaluation

Without it you will not know that a prompt tweak broke something else. It is the analogue of
regression tests, and in a project with models it is needed even more, because the change is
opaque.

**How to do it in practice:**

1. Collect 20–40 real inputs for the agent — actual e-mails, documents, sentences
2. For each, record the expected output: the category, the extracted fields, the decision
3. Write a script that runs them and computes the match
4. Run it in CI on every prompt change

Thresholds: for classification aim for 90 % or better; for field extraction score **field by
field**, not the whole output as one test — otherwise you lose the information about exactly
where it fails.

The set grows out of failures. Whenever the agent makes a mistake in production, add that
input to the set. After a year you have material that cannot be bought.

---

## Part F — Operation

| Area | Minimum for a small company |
|---|---|
| **Accounts** | a dedicated service account for the agent, not the admin's personal account |
| **Permissions** | only for what it does; read instead of write wherever that suffices |
| **Tokens** | recorded, with an expiry date, renewal watched by agent no. 3 |
| **Backups** | a daily database export, a restore rehearsed monthly |
| **Logs** | runs for 90 days, decisions forever, message contents for as short a time as possible |
| **Kill switch** | one message stops the queue; the runbook says who and how |
| **Cost** | weekly monitoring of API spend, an alert when it is exceeded |
| **Runbooks** | what to do when a channel goes down, a token expires, an API changes |

**Personal data:** e-mails and documents contain it. Write down what is sent to the model,
how long it is kept and who has access. In a small company that is a page of text, but it
has to exist before the agent is switched on.

**Cover.** If you build the agent yourself and nobody else knows how it works, that is a risk
comparable to the one it was meant to replace. Runbooks and a flow diagram are the minimum.

---

## Part G — Roll-out

| Phase | Contents | Duration |
|---|---|---|
| 0 | Repository, CI, environments, run records, approval layer | 1 week |
| 1 | Agent 1 in “proposes only” mode — changes nothing, only sorts into a draft | 3 days |
| 2 | Agent 1 live, a month of monitoring, collecting errors into the eval set | 1 month |
| 3 | Agents 2 and 3 on the finished infrastructure | 1 week |
| 4 | The rest as needed | — |

**Phase 1 is the crucial one and the one most often skipped.** Let the agent run for a month
alongside the existing procedure, and compare what it would have done with what the person
did. Out of that come both the eval set and the trust.

---

## Part H — What not to do

- **Do not solve everything with one agent.** Six narrow ones are cheaper and more reliable
  than one broad one.
- **Do not give an agent write access to production systems before a month of reading.**
- **Do not hide prompts in a database without versioning.** You lose the ability to trace why
  something happened.
- **Do not let an agent reply to outsiders without approval.** Not even “just a confirmation”.
- **Do not launch without a kill switch.** There must be a single command that stops it.
- **Do not build offboarding first.** It looks like simple automation and it is the riskiest
  thing on the list.
