# MODULES — The Gwalarn agent

A breakdown into standalone units that can be built and verified independently.
Version 1.0 · August 2026 · Czech original: [MODULY-gwalarn-agent.md](MODULY-gwalarn-agent.md)

---

## Principle

Every module has:

1. **A contract** — what it receives as input, what it returns as output. Written down, in
   advance.
2. **Its own CLI** — runnable from the command line without the rest of the system.
3. **Tests** — unit tests on the logic, manual verification on the output.
4. **A gate** — the list of conditions that must hold before the module is declared finished.

Modules **are not connected before each one has passed its own gate separately.** Integration
in which two unverified things are debugged at once is the most expensive way to lose a
weekend.

One repository, separate packages. Not ten repositories — the shared types would drift apart
within a month.

```
gwalarn-agent/
├─ packages/
│  ├─ media/          M1  ffmpeg, runs on the Beelink
│  ├─ store/          M2  R2 + the media catalogue
│  ├─ events/         M3  pure logic, no I/O
│  ├─ parse/          M4  text → structure via LLM
│  ├─ telegram/       M5  bot, buttons, whitelist
│  ├─ generate/       M6  identity + recipe + facts → draft
│  ├─ publish/        M7  FB / IG / web adapters
│  └─ metrics/        M8  collection and review
├─ apps/
│  ├─ worker/             Cloudflare Worker, orchestration
│  └─ runner/             the ffmpeg job on the Beelink
└─ tests/
```

---

## Where things run

| | Cloudflare Worker | Beelink |
|---|---|---|
| M1 media | ✗ no ffmpeg there | ✓ |
| M2 store | ✓ | ✓ |
| M3 events | ✓ | ✓ |
| M4 parse | ✓ | ✓ |
| M5 telegram | ✓ webhook | — |
| M6 generate | ✓ | ✓ |
| M7 publish | ✓ | — |
| M8 metrics | ✓ cron | — |

The boundary between the Worker and the Beelink runs exactly through M1. The Worker asks for
a video, the runner on the Beelink picks the task up and stores the finished file in R2.

---

## M1 · Media — image and sound into video

The best module to start with: you see the output with your own eyes, a mistake is
immediately obvious, and it needs neither a database nor API keys.

### Contract

```typescript
type RenderJob =
  | { kind: 'still';    photo: string; audio: string; format: Format }
  | { kind: 'slideshow'; photos: string[]; audio: string;
      secondsPerPhoto?: number; transition?: 'none' | 'fade'; format: Format }
  | { kind: 'waveform'; photo: string; audio: string; format: Format };

type Format = 'square' | 'portrait';   // 1080×1080 | 1080×1350

type RenderResult = {
  path: string;
  durationSec: number;
  width: number; height: number;
  sizeBytes: number;
};
```

### CLI

```bash
media still --photo foto.jpg --audio ukazka.mp3 --format square -o out.mp4
media slideshow --photos "fotky/*.jpg" --audio ukazka.mp3 --seconds 4 -o out.mp4
media waveform --photo foto.jpg --audio ukazka.mp3 -o out.mp4
```

### Input checks

- ffmpeg is on PATH, `ffmpeg -version` succeeds
- every input file exists and has a non-zero size
- the photos really are images (verified via `ffprobe`, not by extension)
- the audio contains an audio stream and has a known duration
- for a slideshow: at least one photo, count × duration ≈ audio length
- the target file does not exist, or overwriting was requested

### Output checks

- the file was created and has a non-zero size
- `ffprobe` confirms both a video and an audio stream
- the video duration matches the audio duration ±0.5 s
- the resolution matches the chosen format
- `pix_fmt` is `yuv420p` — otherwise some players will not play it

### ffmpeg recipes

```bash
# still: a static photo + sound
ffmpeg -loop 1 -i foto.jpg -i ukazka.mp3 \
  -c:v libx264 -tune stillimage -c:a aac -b:a 192k \
  -pix_fmt yuv420p -shortest \
  -vf "scale=1080:1080:force_original_aspect_ratio=increase,crop=1080:1080" \
  out.mp4

# slideshow with cross-fades
ffmpeg -f concat -safe 0 -i seznam.txt -i ukazka.mp3 \
  -vf "scale=1080:1350:force_original_aspect_ratio=increase,crop=1080:1350,fps=30" \
  -c:v libx264 -c:a aac -pix_fmt yuv420p -shortest out.mp4

# waveform over a photo
ffmpeg -i ukazka.mp3 -i foto.jpg -filter_complex \
  "[1:v]scale=1080:1080,crop=1080:1080[bg]; \
   [0:a]showwaves=s=1080x260:mode=cline:colors=white@0.85[w]; \
   [bg][w]overlay=0:820[v]" \
  -map "[v]" -map 0:a -c:v libx264 -c:a aac -pix_fmt yuv420p -shortest out.mp4
```

### Gate

- [ ] All three modes produce a playable video
- [ ] A video uploaded to IG by hand looks right — not cropped, with sound
- [ ] A missing file ends with a message within a second, not with an ffmpeg crash
- [ ] A portrait photo and a landscape photo give an equally sized output

---

## M2 · Store — media and their catalogue

### Contract

```typescript
interface Store {
  put(file: Buffer, meta: MediaMeta): Promise<MediaRecord>;
  get(id: string): Promise<MediaRecord | null>;
  find(q: { kind?: 'photo'|'audio'|'video'; eventId?: string;
            unusedOnly?: boolean; limit?: number }): Promise<MediaRecord[]>;
  markUsed(id: string): Promise<void>;
}
```

### Checks

- the caption is mandatory and non-empty — without it the medium is useless
- the file type is verified from the contents, not from the extension
- a size limit (photos up to 15 MB, audio up to 50 MB)
- `r2_key` is unique; uploading the same file twice is detected by hash

### Gate

- [ ] Upload, retrieval, and search by type and by event
- [ ] A medium with no caption is rejected
- [ ] A duplicate file is detected and not uploaded a second time

---

## M3 · Events — gig dates

Pure logic, no network calls. The most testable module in the whole project.

### Contract

```typescript
interface Events {
  create(e: EventInput): Promise<EventRecord>;
  update(id: string, patch: Partial<EventInput>): Promise<EventRecord>;
  remove(id: string): Promise<void>;
  upcoming(limit?: number): Promise<EventRecord[]>;
  inWindow(fromDays: number, toDays: number): Promise<EventRecord[]>;
  findDuplicate(startsAt: number, venue: string): Promise<EventRecord | null>;
}
```

### Checks

- the date is in the future, otherwise a warning (past dates are entered only exceptionally)
- **the year is filled in as the nearest future occurrence** — “14.11.” in December means
  next year
- the venue is non-empty
- duplication: same day + same venue → offer an edit instead of creating a new record
- time zone Europe/Prague, stored as a UTC timestamp

### Tests

```
"14.11. in December"       → next year
"14.11. in January"        → this year
"31.2."                    → error, a date that does not exist
"14.11. 19:30" + duplicate → found
daylight-saving transition → the correct UTC offset
```

### Gate

- [ ] The unit tests on filling in the year pass
- [ ] Duplication is detected
- [ ] The switch to winter time does not shift the gig times

---

## M4 · Parse — from a sentence into structure

### Contract

```typescript
parseEvent(text: string): Promise<{
  parsed: Partial<EventInput>;
  missing: string[];        // what could not be read out
  confidence: number;
}>;
```

### Checks

- the model's answer must be valid JSON against the schema — otherwise one retry, then give
  up and ask for manual entry
- the date is validated through M3; the model is not trusted
- an empty or too-short input is rejected without calling the LLM

### Tests

A set of twenty real sentences of the kind the band would write, with expected outputs.
Including incomplete ones (“a gig at the Sokolovna” — no date) and typos.

### Gate

- [ ] Eighteen of the twenty test sentences parse correctly
- [ ] Incomplete input returns a list of missing fields, not an invention
- [ ] An invalid model response does not take the process down

---

## M5 · Telegram — input and approval

### Contract

```typescript
interface TelegramIO {
  onCommand(cmd: string, h: Handler): void;
  onVoice(h: (fileId: string) => Promise<void>): void;
  askConfirm(chatId: number, text: string,
             buttons: Button[]): Promise<string>;   // returns the choice
  send(chatId: number, text: string, media?: string): Promise<void>;
}
```

### Checks

- **a whitelist of Telegram IDs** — otherwise anyone can write into the calendar
- webhook signature verification
- idempotence keyed on `update_id`; Telegram delivers repeatedly
- a timeout on an unanswered confirmation (24 h → the draft expires)

### Gate

- [ ] An outside account is refused
- [ ] Double delivery of the same message does not create two records
- [ ] The buttons still work after the Worker restarts

---

## M6 · Generate — drafting the text

### Contract

```typescript
generate(input: {
  recipe: Recipe;
  identity: string;
  event?: EventRecord;
  media?: MediaRecord[];
  recentPosts: string[];      // so it does not repeat itself
  platform: 'web' | 'facebook' | 'instagram';
}): Promise<{ text: string; usedMediaIds: string[] }>;
```

### Checks

- the output length is within the platform's limits
- it must not contain invented details — the date, venue and time are compared against
  `event`; a mismatch means discard and try again
- a check against `recentPosts` for verbatim repetition of phrasings
- forbidden words from `identity.md` (cliches) are watched for programmatically

### Gate

- [ ] The same event produces three variants of different lengths
- [ ] A planted event with a wrong date is caught
- [ ] Ten generations in a row do not give the same first sentence ten times

---

## M7 · Publish — adapters

A common interface, three implementations. The key thing is that they can be swapped out —
the Meta API will change; it is a matter of when, not whether.

```typescript
interface Publisher {
  name: 'facebook' | 'instagram' | 'web';
  validate(post: DraftPost): ValidationResult;   // no network call
  publish(post: DraftPost): Promise<PublishResult>;
}
```

### Checks before sending

| Platform | What to verify |
|---|---|
| Instagram | media mandatory · aspect ratio within limits · caption length · video ≤ 90 s |
| Facebook | text length · the link is a valid URL |
| Web | the slug is unique · the front matter is valid |

### Instagram — specifics

Publishing is two-step: first a container is created, then it is published. In between you
wait for processing, which for video can be tens of seconds — the container state has to be
polled, not blindly waited out for a fixed time.

### Gate

- [ ] A test post goes through to each platform separately
- [ ] Invalid input is caught in `validate()`, without calling the API
- [ ] An expired token gives a comprehensible message, not a generic 400

---

## M8 · Metrics — collection and review

### Contract

```typescript
collect(postId: string): Promise<Metrics>;
proposeRecipeUpdate(recipeId: string): Promise<{
  proposal: string; reasoning: string; sampleSize: number;
}>;
```

### Checks

- collection runs after 48 h and after 7 days, not at publication time
- an unavailable endpoint is logged and retried; it does not block the cron
- a proposal for a new recipe version is **never applied by itself**
- with a sample under 10 posts no proposal is generated, and the reason is stated

### Gate

- [ ] Metrics are filled in retrospectively for an existing post
- [ ] An API outage does not take the cron down
- [ ] A small sample returns a refusal instead of a recommendation

---

## Integration steps

Only once all the gates have passed. Each step is a vertical slice through the system — it
works from end to end, just over a narrow range.

| # | Slice | Modules involved |
|---|---|---|
| I1 | I enter a date from my phone and it is saved | M5 → M4 → M3 |
| I2 | I upload a photo with a caption | M5 → M2 |
| I3 | A draft is generated and arrives for approval | M3 + M2 → M6 → M5 |
| I4 | The approved text appears on the website | M7 (web) |
| I5 | The same on FB | M7 (facebook) |
| I6 | The same on IG with a photo | M7 (instagram) |
| I7 | An audio sample as a video | M1 → M2 → M7 |
| I8 | Metrics fill themselves in | M8 |

After I4 the project already has value even if it went no further. That is a good place to
pause.

---

## Build order

```
M1 media ──┐                      standalone, blocks nothing
M3 events ─┤
M2 store ──┘
              ↓
M4 parse ──> M5 telegram ──> I1, I2
              ↓
M6 generate ──> I3
              ↓
M7 publish ──> I4 ──> I5 ──> I6
              ↓
M1 + M7 ──> I7
              ↓
M8 metrics ──> I8
```

M1, M2 and M3 can be done in any order and independently of one another. M1 is the best
start: the result is visible, a mistake is obvious, and it needs no access credentials.
