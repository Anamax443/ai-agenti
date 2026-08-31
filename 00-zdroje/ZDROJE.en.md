# Sources

Where the methodology in `01-principy/` comes from and how to check it.

Czech original: [ZDROJE.md](ZDROJE.md)

---

## Primary source — the interview with Marek Bartoš

**Keci a politika**, the special “Umělá inteligence je naše UFO” (*Artificial intelligence
is our UFO*). Guest: Marek Bartoš (science and AI communicator). Hosted by Bohumil Pečinka
and Petros Michopulos. Only the first half of the show is freely available; the second is
behind a paywall (keciapolitika.cz, herohero.co).

### How the transcript was produced

Locally, with [mp3totxt](https://github.com/Anamax443/mp3totxt) 0.1.0 (faster-whisper,
model `medium`, language `cs`, no GPU):

| Item | Value |
|---|---|
| Audio length | 3,351 s (55:51) |
| Transcription time | 6,076 s (1:41:16) |
| Ratio | **1.81×** the audio length |

### What is not in the repository

The transcript (`.txt`, `.json`, `.srt`, `.vtt`) sits in `00-zdroje/prepisy/`
**locally only** — the folder is in `.gitignore`. The repository is public, and the
transcript of someone else's show whose second half is paid does not belong in it. Only
this analysis goes into the repository: timestamps, paraphrases and short quotations.

### Limitations to account for

- The transcript covers **only the first half** of the show (the freely available part).
- The `medium` model garbles proper nouns and less common words. “Skippy” alternates in
  the transcript between *skipy / Skypy / Stiffy*, “Perplexity” becomes *Pelprexity*,
  “arXiv/bioRxiv” becomes *ArcSive / BioXSive*, and “Anthropic” disappears in places.
  **Never quote a name or a number from the transcript without listening to the audio.**
- The timestamps in the table below come from the `.json` (the `start` field), not from
  the audio by hand.

---

## Map: what was said in the show and where it landed in the repo

| Time | What was said | Where it is |
|---|---|---|
| 13:25 | One main mind holds the memories; the work is done by smaller, cheaper parts, each with “a little personality infused into it” | [Anatomy of an agent](../01-principy/PRINCIPY-stavby-agentu.en.md#3-anatomy-of-an-agent) |
| 11:43 | A persona extracted from a literary source (Skippy the Magnificent, *The Expeditionary Force*) by analysing e-books | [The persona as an artefact](../01-principy/PRINCIPY-stavby-agentu.en.md#4-the-persona-as-an-artefact) |
| 17:02 | A limit of CZK 50,000; for pre-approved suppliers it pays without approval and merely reports | [Gates](../01-principy/PRINCIPY-stavby-agentu.en.md#7-gates-when-to-ask-a-person) |
| 17:29 | **“I am not afraid, because it is not actually the artificial intelligence that does it.”** | [The founding principle](../01-principy/PRINCIPY-stavby-agentu.en.md#1-the-founding-principle) |
| 18:59 | An invoice is transcribed by Mistral OCR and independently by Gemini; they agree → it proceeds, they disagree → a person is asked. Transcribe, not pay. | [Cross-checking](../01-principy/PRINCIPY-stavby-agentu.en.md#8-cross-checking) |
| 19:45 | “Skippy doesn't actually pay it” — it only recognises and hands off to the process; the payment is done by the machinery | [The founding principle](../01-principy/PRINCIPY-stavby-agentu.en.md#1-the-founding-principle) |
| 20:53 | A predefined process has **only two endings**: it fails with a report, or it goes well | [Failure and observability](../01-principy/PRINCIPY-stavby-agentu.en.md#11-failure-and-observability) |
| 21:16 | Trust did not build up over time — it was there immediately, because it does not rest on the AI but on code that “runs hard-wired” | [Gates](../01-principy/PRINCIPY-stavby-agentu.en.md#7-gates-when-to-ask-a-person) |
| 21:32 | The QR-code analogy: you do not trust the model, you trust a process with a low error rate | same |
| 26:44 | Location every 5 minutes → from the speed it works out he is driving and sends a voice message instead of text | [Inputs and peripherals](../01-principy/PRINCIPY-stavby-agentu.en.md#5-inputs-and-peripherals) |
| 28:34 | His wife has **broader rights** in the agent than the owner does (she can rearrange the calendar) | [Permissions and identity](../01-principy/PRINCIPY-stavby-agentu.en.md#6-permissions-and-identity) |
| 29:14 | Identity verification over WhatsApp: phone number plus further identifiers, not a name in the prompt | same |
| 30:50 | A morning report: the agent reads the e-mails and summarises who wants what | [Proactivity](../01-principy/PRINCIPY-stavby-agentu.en.md#10-proactivity) |
| 31:48 | The agent **always admits it is an AI** — a reference to the AI Act | [Permissions and identity](../01-principy/PRINCIPY-stavby-agentu.en.md#6-permissions-and-identity) |
| 34:36 | Cost: ~CZK 5,000/month to run + ~CZK 2,000/month for further development | [Why this matters economically](../01-principy/PRINCIPY-stavby-agentu.en.md#why-this-matters-economically) |
| 36:08 | **The process costs a few cents per invoice; the same thing through AI costs dollars**; if the AI did everything it would run to tens of thousands a month | same |
| 37:12 | The agent reads arXiv/bioRxiv on its own, looking for ways to improve | [Improvement](../01-principy/PRINCIPY-stavby-agentu.en.md#12-improvement) |
| 06:32 | AI psychosis as a documented phenomenon — why not to build an agent on a relationship | [Anti-patterns](../01-principy/PRINCIPY-stavby-agentu.en.md#15-anti-patterns) |
| 46:43 | The model does not understand what it is saying — it is a next-word predictor | [The founding principle](../01-principy/PRINCIPY-stavby-agentu.en.md#1-the-founding-principle) |

---

## Book source

**Michael Albada — _Building Applications with AI Agents: Designing and Implementing
Multiagent Systems_** (O'Reilly, September 2025, ISBN 978-1-098-17650-1).

355 pages, 13 chapters following the agent life cycle. The closest structural counterpart
to our build specification; chapters 9–13 (measurement, monitoring, improvement loops,
security, working with people) cover the phases we had been dismissing with a single
bullet point.

What we took from it into [`sablony/BUILD-PREDPIS.en.md`](../sablony/BUILD-PREDPIS.en.md):

| From | What exactly |
|---|---|
| ch. 3 | a text interface has no menu — the agent must say what it can do |
| ch. 4 | least power for tools; disabling tools by configuration in tests |
| ch. 9 | the tool recall / precision, parameter accuracy, phrase recall, task success metrics |
| ch. 10 | telling an error from variance (3–5 runs, an 80 % threshold); shadow runs alongside live; PSI for distribution shift |
| ch. 11 | a budget for escalations (~10 % of cases); document every prompt change |
| ch. 12 | the documented case of an agent that “optimised” a production database by deleting rows |
| ch. 13 | autonomy growing operator → reviewer → collaborator → supervisor; the four ways human oversight fails; Klarna as a warning against the reverse order |

The book is built on LangGraph and on teams with ML engineers and SREs. For a solo
operation on Cloudflare, half the content (GPU scaling, multiagent coordination,
fine-tuning) is out of scope — we took the principles, not the stack.

---

## Supplementary sources

- **Anthropic** — *Building effective agents* and the follow-on material on designing
  agentic systems (workflow vs. agent, when a prompt chain is enough).
- **OpenAI** — *A practical guide to building agents* (tools, guardrails, escalation to a
  human).
- **AI Act** — the obligation to disclose that an AI is communicating. State as of August
  2026, after the Digital Omnibus came into force on 27 July 2026. Deadlines change;
  verify them.

## Rule for further sources

When another interview, talk or study is added: the transcript or PDF goes into
`00-zdroje/prepisy/` (outside git), and a line with the citation plus a map of timestamps
goes here. Only the conclusion belongs in the methodology in `01-principy/`, never the raw
material.
