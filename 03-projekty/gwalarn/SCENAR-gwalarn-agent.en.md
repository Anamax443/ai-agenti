# SCENARIO — Content agent for Gwalarn

Facebook · Instagram · gwalarn.cz
Version 1.0 · August 2026 · Czech original: [SCENAR-gwalarn-agent.md](SCENAR-gwalarn-agent.md)

---

## Starting points

- Publishing happens **only to the band's own accounts** → no app review with Meta is needed;
  a Meta app in development mode plus the Instagram Tester role is enough.
- The gwalarn.cz website is the **primary target**. The FB and IG posts are shortened
  derivatives of it with a link back. One source of truth, three outputs.
- **Human approval is mandatory.** Nothing is published automatically.
- Learning rests primarily on **draft/final pairs**, not on reach. At four posts a month the
  sample is far too small for statistics.

Runtime: Cloudflare Workers + D1 + R2, Telegram for approvals. It builds on the existing
stack rather than starting from scratch.

---

## Phase 0 — Accounts and access

Boring, but it blocks everything else. Expect it to stretch over more than one sitting,
because some steps have to be confirmed by somebody else.

### Steps

1. Convert the Gwalarn Instagram account to **Business**
   (not Creator — Creator cannot publish Reels through the API)
2. Link it to the band's Facebook page
3. Create a Business-type Meta app on developers.facebook.com
4. Add the Instagram Graph API product
5. In dev mode, add the IG account as an **Instagram Tester** and accept the invitation in
   the Instagram settings
6. Generate a long-lived token and note the expiry date
7. Verify by hand through the Graph API Explorer: create a container and publish a test image

### Done when

- [ ] A test photo appeared on IG through the API, not from a phone
- [ ] The token is stored in Workers Secrets, not in the repository
- [ ] There is a note of when the token expires

### Traps

- The token is valid for 60 days and **does not renew itself**. The refresh cron is part of
  phase 3, but set a calendar reminder right away.
- Personal accounts do not work through the API at all. If somebody in the band has the
  impression that “it works without all that”, it does not.

---

## Phase 1 — Material and the data model

An agent with no sources writes padding. This phase is about what to feed it.

### Content to prepare

| Source | Where | Note |
|---|---|---|
| Gig calendar | D1 table `events` | date, venue, time, line-up, ticket link |
| Photos | R2 + table `media` | **each with a caption** — without that the photo bank is useless |
| Audio samples | R2 | must be converted to video, see phase 4 |
| Band identity | file `identity.md` | written once, changed rarely |
| Archive of published posts | D1 table `posts` | so that posts do not repeat |

### Band identity — what belongs in it

Not “a Breton band”. Specifics the model has something to work with:

- instruments: biniou, bombarde, who plays what
- dances and forms: an dro, hanter dro, gavotte, plinn
- the fest-noz context — what it is and how you talk about it
- language: how you write about Breton, whether you give translations
- what to avoid: generic adjectives about a “magical Celtic atmosphere”, cliches about
  mysticism, conflating Breton with Irish

This file is the most important thing in the whole project. The difference between your post
and the post of any other folk band originates precisely here.

### D1 schema

```sql
CREATE TABLE events (
  id TEXT PRIMARY KEY,
  starts_at INTEGER NOT NULL,
  venue TEXT NOT NULL,
  city TEXT,
  lineup TEXT,
  ticket_url TEXT,
  note TEXT              -- anything specific to this event
);

CREATE TABLE media (
  id TEXT PRIMARY KEY,
  r2_key TEXT NOT NULL,
  kind TEXT NOT NULL,    -- photo | audio
  caption TEXT NOT NULL, -- mandatory, otherwise the photo is unusable
  event_id TEXT,
  taken_at INTEGER,
  used_count INTEGER DEFAULT 0
);

CREATE TABLE recipes (
  id TEXT NOT NULL,
  version INTEGER NOT NULL,
  body TEXT NOT NULL,
  note TEXT,
  created_at INTEGER NOT NULL,
  PRIMARY KEY (id, version)
);

CREATE TABLE posts (
  id TEXT PRIMARY KEY,
  recipe_id TEXT,
  recipe_version INTEGER,
  event_id TEXT,
  media_ids TEXT,              -- JSON array
  platform TEXT,               -- web | facebook | instagram
  draft_text TEXT,             -- what the model generated
  final_text TEXT,             -- what you actually published
  edit_distance REAL,          -- how much you intervened, 0 = no change
  my_rating INTEGER,           -- 1-5, your satisfaction
  published_at INTEGER,
  metrics_json TEXT,
  metrics_fetched_at INTEGER
);
```

### Done when

- [ ] At least 20 photos in R2, each with a caption
- [ ] A gig calendar six months ahead
- [ ] `identity.md` read and agreed by the rest of the band

---

## Phase 2 — Composed prompts

A prompt is not written as one sentence. It is assembled from three layers only at generation
time.

```
┌─ band identity ────────────┐  static, changes rarely
├─ recipe for the post type ─┤  in D1, versioned
├─ facts about the event ────┤  from events + media
└────────────────────────────┘
              ↓
         draft post
```

### Recipes to create

| ID | When it is used | Goal |
|---|---|---|
| `pozvanka` | 10 days before a gig | get people to the event |
| `pripominka` | 2 days before a gig | short, facts only |
| `ohlednuti` | the day after a gig | a photo, thanks |
| `skladba` | any time, calendar filler | introduce a piece of the repertoire |
| `fotka` | any time | from a rehearsal, from travelling |

### What a good recipe looks like

Not “write an invitation with a hint of Brittany”. Concrete instructions about structure:

> Two to three sentences. The first is a concrete invitation with the date, venue and time.
> The second refers to one specific dance or piece from the programme — pick it from the note
> on the event. No generic adjectives about atmosphere. End with the link. No emoji at the
> start of sentences, at most one at the end.

Recipes are stored in D1, not in the code — you edit them without a deploy.

### Variants by platform

The same material produces three outputs of different lengths:

- **web** — the longest, context, can be an article
- **facebook** — medium, tolerates a link and longer text
- **instagram** — the shortest, the weight is on the image, a link does not work in the caption

### Done when

- [ ] Five recipes in D1
- [ ] Generation runs locally and the output makes sense
- [ ] The same event produces three variants of different lengths

---

## Phase 3 — The publishing pipeline

### Flow

```
cron ──> find an event in the window ──> pick a recipe ──> pick a photo
   ──> generate a draft ──> save as a draft ──> Telegram for approval
   ──> [you: approve / edit / discard] ──> publish ──> save final_text
```

### Telegram approval

The message contains: a preview of the text, a preview of the photo, the recipe name.
Buttons: **Publish** · **Edit** · **Discard**.

An edit arrives as a text reply. It is saved into `final_text` and `edit_distance` is
computed. This is the main learning signal — do not cut corners on it.

After publishing, a second message: a 1–5 rating of how satisfied you are. Five seconds of
work, more valuable than most metrics.

### Publishing to Instagram

A two-step call: first a POST to `/{ig-user-id}/media` creates a container, then
`/{ig-user-id}/media_publish` publishes it. In between you wait for processing — for video
that can be tens of seconds, and the container state has to be polled.

### Token refresh

A separate cron, once a week. It renews the long-lived token and sends a confirmation to
Telegram. When it fails it sends a warning — not silence.

### Done when

- [ ] An invitation for a real gig passes through the whole flow
- [ ] An edit made through Telegram is saved into `final_text`
- [ ] A publishing failure ends with a message in Telegram, not with silence

---

## Phase 4 — Audio samples

Neither Facebook nor Instagram will accept bare audio. It has to become video.

```bash
# a still photo + sound
ffmpeg -loop 1 -i foto.jpg -i ukazka.mp3 \
  -c:v libx264 -tune stillimage -c:a aac -b:a 192k \
  -pix_fmt yuv420p -shortest -vf "scale=1080:1080" out.mp4

# with a rendered waveform
ffmpeg -i ukazka.mp3 -filter_complex \
  "[0:a]showwaves=s=1080x300:mode=cline:colors=white[w]; \
   [1:v][w]overlay=0:390[v]" -i foto.jpg -map "[v]" -map 0:a \
  -c:v libx264 -c:a aac -shortest out.mp4
```

Where it will run: there is no ffmpeg in Workers. Either as a job on the Beelink that fetches
its own tasks, or pre-generate the videos in advance and store the finished ones in R2.

### Done when

- [ ] A sample appears on IG as a video with cover art
- [ ] The format is 1:1 or 4:5, not 16:9 — otherwise it gets lost on a phone

---

## Phase 5 — Metrics and learning

### Collecting metrics

A separate cron, not part of publishing. After **48 hours** and after **7 days** it fetches
insights and fills in `metrics_json`.

Careful: some Facebook Insights endpoints were retired this year. Before you build a schema
on it, verify what is still available — and expect it to change again.

### Quarterly review

**Not automatic.** Once a quarter you run a job that:

1. takes all the posts made with a given recipe
2. assembles `draft_text` / `final_text` pairs
3. adds the metrics and your ratings
4. has the model write **a proposal for a new version of the recipe, with a justification**

You read it and approve or discard it. The new version is saved as `version + 1`; the old one
stays.

### Why not automatically

At four posts a month, after a year you have fifty samples spread across five recipes and
three platforms. In a sample that size, the difference between a “successful” and an
“unsuccessful” post is usually whether you played a well-known festival and somebody shared
it. A loop that rewrites its own prompts on that basis drifts in the wrong direction and you
notice a year later.

### Done when

- [ ] Metrics fill themselves in
- [ ] The first quarterly review has happened and version 2 of at least one recipe exists
- [ ] Old recipe versions are traceable

---

## Order and estimate

| Phase | Work | Blocks |
|---|---|---|
| 0 · Accounts | 2–3 h spread out | everything |
| 1 · Material | 4 h + taking photos and writing captions | 2, 3 |
| 2 · Prompts | 4 h | 3 |
| 3 · Pipeline | 8 h | 4, 5 |
| 4 · Audio | 3 h | — |
| 5 · Learning | 4 h | — |

Phases 4 and 5 can be postponed. Phases 0 and 1 cannot be skipped or shortened — and phase 1
is the only one where the work cannot be done for you by code.

---

## What will go wrong

- **Nobody writes the photo captions.** The most common reason this kind of project ends up
  as an unfinished photo bank. Do it before the pipeline.
- **The token expires at the worst possible moment.** A refresh cron and monitoring into
  Telegram.
- **Meta changes the API.** It is a matter of when, not whether. Keep the publishing layer
  separate from the rest so it can be swapped out.
- **The agent starts writing padding.** The signal is a rising `edit_distance`. When it rises,
  the problem is not the model but `identity.md` or the recipe.
