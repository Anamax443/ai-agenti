# AGENTS IN A LARGE COMPANY

Platform, governance and portfolio. It follows on from the small-office document, but it
solves a different problem.

Version 1.0 · August 2026 · Czech original: [AGENTI-velka-firma.md](AGENTI-velka-firma.md)

---

## Part A — What changes

In a small company the question is “which agent to build”. In a large company the question
is **“how do we let teams build agents themselves without ending up with an unmanageable
menagerie”.**

| | Small company | Large company |
|---|---|---|
| Who builds | one person | dozens of people across departments |
| Main risk | the agent makes a mistake | nobody knows how many agents run and what they can reach |
| Centre of gravity | the agents | the platform and the rules |
| Approval | one person in a chat | roles, cover, separation of duties |
| Cost | below the threshold of interest | charged back to cost centres |
| Regulation | marginal | AI Act, GDPR, internal audit |

If this is built as a series of standalone projects, a year later forty agents are running,
each with its own way of calling models, its own credentials and no records. Untangling that
then costs more than building it again.

**So build the platform first, then the agents.**

---

## Part B — The platform

### The model gateway

The single place every model call in the whole company passes through.

```
agents and applications
        │
        ▼
┌───────────────────────────────────────────┐
│  MODEL GATEWAY                            │
│  caller auth · limits · chargeback        │
│  personal-data redaction · call record    │
│  routing to a model · fallback model      │
└───────────────────────────────────────────┘
        │
     providers
```

What it buys you:

- **Chargeback.** Every call carries a cost centre and an agent. Without it nobody knows who
  is spending.
- **The model version in one place.** The provider retires a model — you change the
  configuration, not thirty applications.
- **A record.** An audit trail of all calls, separate from the application logs.
- **Data protection.** Redaction of national ID numbers, account numbers and similar fields
  in one place, not in every agent separately.
- **Limits.** A cap per agent and per cost centre, so that a bug in a loop does not eat the
  monthly budget overnight.

It does not have to be complicated — a reverse proxy with authentication, a log and limits.
But it has to be the mandatory route. Block direct calls to providers at the firewall.

### Shared services

Build once, everybody uses:

| Service | What it does |
|---|---|
| **Approval queue** | one place where people approve anything from any agent |
| **Run records** | who, when, what they started, how it turned out, what a person corrected |
| **Tool catalogue** | approved connectors into systems, with defined permissions |
| **Prompt library** | company tone, shared instructions, versioned |
| **Eval runner** | runs the regression sets in CI |
| **Agent template** | the repository skeleton you start from |

The template matters more than it looks. When a new thing can be stood up in two hours from
a ready-made skeleton, nobody will build their own.

---

## Part C — Governance and records

### The agent registry

A mandatory record for every agent in operation. Without a record it gets no access through
the gateway — that is the only way to keep the registry alive.

```
NAME
OWNER                 a specific person, not a department
DEPUTY                who handles it when the owner is away
PURPOSE               one sentence
COST CENTRE           who pays
RISK CATEGORY         1-4, see below
DATA                  what categories of data it processes
SYSTEMS               what it reaches, with what permissions
HUMAN OVERSIGHT       who approves what
STATE                 design | pilot | production | retired
REVIEW                date of the last and the next
```

### Risk categories

| | Description | What is required |
|---|---|---|
| **1** | only reads and summarises, changes nothing | notification, run records |
| **2** | changes internal data, reversible | approval by the system owner, an eval set |
| **3** | communicates outward, touches money or permissions | security approval, a human gate on every action |
| **4** | impact on people — recruitment, assessment, access | legal assessment, documented evidence, oversight |

The category is set by **impact, not technology.** A simple script that removes access is
category 3.

### Separation of duties

Whoever builds an agent must not approve its deployment into production, nor its own
actions. In a small company that is impractical; in a large one it is the minimum an auditor
will want to see.

---

## Part D — Regulation

### The AI Act, state as of August 2026

The timing changed last year, which is why a lot of internal material is out of date.

Regulation (EU) 2026/1744, the Digital Omnibus, came into force on 27 July 2026 — six days
before the original date. The obligations for standalone high-risk systems under Annex III
moved from 2 August 2026 to 2 December 2027; for AI embedded in products under Annex I, to
2 August 2028.

What did **not** move: the transparency obligations under Article 50 apply from 2 August
2026, that is, already. For systems placed on the market before that date, Art. 50(2)
applies only from 2 December 2026, which is also when the new prohibitions take effect.

In practice this means:

- **The agent must disclose that it is an AI** whenever it communicates with a person from
  outside. That applies today, not in a year.
- **A postponement is not a pause.** Inventorying and classifying systems is done now; the
  shift applies to demonstrating conformity, not to preparing it.
- The postponement is tied to a registration mechanism, and systems put into operation
  before the deadline have an exemption — which falls away as soon as you change the system
  substantially.

The penalties are high: prohibited practices up to EUR 35 million or 7 % of turnover;
breaches of transparency and of the rules for high-risk systems up to EUR 15 million or 3 %.

**What tends to be category 4:** recruitment and candidate selection, employee assessment,
decisions about access and promotion. Which is exactly the set of tasks HR wants to automate
first.

### Personal data protection

- An impact assessment (DPIA) for anything processing personal data at scale
- A processing agreement with the model provider, a verified retention period, and whether
  the data is used for training
- Add the agents to the record of processing activities — this is the one that gets forgotten
- Data location and cross-border transfers

Do the legal assessment **before the pilot, not after it.** A pilot stopped after a quarter
of a year of investment is worse than a delayed start.

---

## Part E — Identity and permissions

- **A dedicated service identity for every agent.** Not a shared account, not the admin's
  personal account. In an Entra ID environment, a managed identity or an application
  registration with a certificate, not a password.
- **The least possible permissions.** Read instead of write, one mailbox instead of the whole
  tenant, one database instead of the server.
- **Time-limited elevated permissions.** When an agent needs more, let it have them for the
  duration of the task and with a record.
- **An agent must not inherit the rights of the user** who started it. Otherwise permissions
  quietly spread.
- **Credential rotation** automatic, with expiry monitoring.
- **An employee's departure** must remove their agents too. An orphaned agent with valid
  permissions is a classic hole.

---

## Part F — Portfolio by department

| Department | Agent | Risk | Note |
|---|---|---|---|
| IT | ticket triage, draft reply | 1–2 | a good first one |
| IT | summarising operational alerts | 2 | does not triage incidents on its own |
| IT | preparing accounts from a template | 3 | write access only after the pilot |
| Finance | transcribing and matching documents | 2–3 | ends at approval, not at payment |
| Finance | watching deadlines and contracts | 1 | the best ratio |
| Purchasing | comparing quotes | 2 | a person decides |
| Sales | preparing pre-meeting briefs | 1 | reads CRM, changes nothing |
| Sales | drafting a reply to an enquiry | 2 | a person sends it |
| Legal | extracting dates from contracts | 2 | does not replace the assessment |
| HR | CV screening | **4** | Annex III, documented oversight |
| HR | answering benefits questions | 1 | from an approved knowledge base |
| Operations | meeting minutes | 1 | transcription done locally |

Deploy along the rows with risk 1 and 2. Leave HR until last — not because it is technically
hard, but because it is the most expensive in regulatory terms.

---

## Part G — Development and deployment

### Repositories

The platform in one repository, the agents in their own. The opposite of the small company —
with dozens of teams, a monorepo means every change waits on somebody else's CI.

```
platform/            gateway, shared services, libraries, template
agent-<name>/        one repository per agent, from the template
```

The platform publishes versioned libraries. The agents consume them as a dependency and
update themselves, with old versions carrying an announced support window.

### The golden path

A prepared route that is the fastest way through: a repository template, pre-built CI, the
model gateway, the tool catalogue, the registry. Whoever follows it is deployed in a day.
Whoever wants to leave it needs approval and has to justify why.

Banning deviations does not work. Making the golden path so comfortable that nobody wants to
turn off it does.

### CI/CD

```
push       → lint · types · tests · eval set · secret scan · SBOM
merge      → deploy to the development environment
             smoke tests
             ↓
             stage: full data, outbound channels disabled by configuration
             ↓
approval   → production (a different person than the author)
```

Mandatory CI gates that pay off in a large company:

- **The eval set** with a threshold. Dropping below the line stops the deployment the same
  way a failed test does.
- **A prompt change is a code change.** It goes through review, carries a version, and is
  written into every run.
- **A permission check.** When new access to a system appears in the configuration, CI flags
  it and requires security approval.
- **Secret scanning**, blocking, at the organisation level.

---

## Part H — Operation

| Area | What to put in place |
|---|---|
| **Monitoring** | a dashboard per agent: runs, error rate, latency, cost, share of human interventions |
| **Tracing** | every run traceable step by step, even a month later |
| **Incident reporting** | an agent is a system like any other and belongs in the same process |
| **Kill switch** | central, at the gateway level. One action can stop one agent or all of them. |
| **Chargeback** | monthly to cost centres, otherwise the costs become invisible |
| **Review** | every agent once a year: is it still running? does it still make sense? does it have rights it does not need? |
| **Retirement** | a process for shutting down: remove the identity, close the data, record it in the registry |

The indicator most worth watching: **the share of outputs a person edited before approving.**
When it rises, something has drifted — usually a change on the input side, not the model.

---

## Part I — Shadow deployments

The biggest real problem in large companies is not a badly built agent, but agents nobody
knows about centrally. They appear in departments, run on personal accounts and personal
access, and nobody reviews them.

What works:

1. **An amnesty.** Announce a period in which anything existing can be reported without
   penalty, with an offer to help move it onto the platform.
2. **A golden path faster than improvising.** As long as the official route is slower, people
   will go around it.
3. **A technical boundary.** Block direct access to model providers outside the gateway. Not
   as a punishment, but so that the shadow route simply does not work.
4. **Do not punish the first person who owns up.** Otherwise they are the last.

---

## Part J — Roll-out

| Months | Contents |
|---|---|
| 1–2 | Model gateway, registry, rules, risk categories |
| 2–3 | Agent template, CI, eval runner, approval queue |
| 3–5 | Two category-1 pilots, in different departments, a month running idle |
| 5–6 | Evaluation, adjusting the golden path based on what the pilots lacked |
| 6–9 | Opening the platform to further departments, training, the amnesty |
| 9–12 | Category 3 with documented oversight, preparation for category 4 |

Run the pilots **in two different departments.** A pilot in IT shows that it works for the
people who built it. The second one shows what is missing from the documentation.

---

## Part K — What not to do

- **Do not start with a portfolio of agents.** Without a gateway and a registry, a year later
  you have a mess that cannot be tidied.
- **Do not create a central team that builds everything.** It becomes a bottleneck and the
  departments go around it. Its job is to build the platform, not the agents.
- **Do not launch HR tasks first.** The most expensive part of the portfolio in regulatory
  terms.
- **Do not rely on last year's AI Act material.** The deadlines changed in July, and some
  obligations did not move at all.
- **Do not give an agent a user's rights.** Its own identity, its own scope.
- **Do not underestimate retirement.** After two years a company usually does not know what
  it still has running.
