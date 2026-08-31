# M1 · MEDIA — implementation brief

A module for turning images and sound into video suitable for Instagram and Facebook.
Written as input for Claude Code. Version 1.0 · Czech original:
[M1-media-zadani.md](M1-media-zadani.md)

---

## 1. What the module does

It takes photos and an audio file and produces an MP4 from them. Three modes:

| Mode | Input | Result |
|---|---|---|
| `still` | 1 photo + audio | a static image for the whole duration of the sound |
| `slideshow` | N photos + audio | the photos alternate, optionally with cross-fades |
| `waveform` | 1 photo + audio | the photo with a waveform drawn across the lower part |

The module **touches neither the network, nor a database, nor R2.** It receives file paths
and returns a file path. Nothing more. Storage is M2's problem.

---

## 2. Technology

- **TypeScript**, Node ≥ 20, ESM
- CLI via `commander`
- ffmpeg is called through `child_process.spawn` — **not** through `exec`, because of the
  output length and the need to read it as it arrives
- tests: `vitest`
- no ffmpeg wrapper library. Assembling the arguments is an array of strings; a wrapper would
  only add a layer that is harder to debug through

### Structure

```
packages/media/
├─ src/
│  ├─ index.ts          the public API
│  ├─ types.ts          re-export from the shared types + internal ones
│  ├─ probe.ts          ffprobe: determining a file's properties
│  ├─ validate.ts       input checks
│  ├─ commands.ts       assembling the ffmpeg arguments (pure functions)
│  ├─ render.ts         running ffmpeg, progress, result
│  ├─ errors.ts         typed errors
│  └─ cli.ts            the command-line interface
├─ tests/
│  ├─ commands.test.ts  unit, without ffmpeg
│  ├─ validate.test.ts  unit
│  ├─ render.test.ts    integration, needs ffmpeg
│  └─ fixtures.ts       generating the test files
└─ package.json
```

---

## 3. Public API

```typescript
export type Format = 'square' | 'portrait';

export const DIMENSIONS: Record<Format, { w: number; h: number }> = {
  square:   { w: 1080, h: 1080 },
  portrait: { w: 1080, h: 1350 },
};

export type RenderJob =
  | { kind: 'still';     photo: string;    audio: string; format: Format }
  | { kind: 'slideshow'; photos: string[]; audio: string; format: Format;
      secondsPerPhoto?: number;          // default: audio length / photo count
      transition?: 'none' | 'fade' }     // default: 'fade'
  | { kind: 'waveform';  photo: string;    audio: string; format: Format;
      waveColor?: string };              // default: 'white@0.85'

export type RenderOptions = {
  output: string;
  overwrite?: boolean;                   // default: false
  onProgress?: (p: RenderProgress) => void;
  signal?: AbortSignal;                  // interruption
};

export type RenderProgress = {
  processedSec: number;
  totalSec: number;
  percent: number;                       // 0-100
  speed: number;                         // multiple of real time
};

export type RenderResult = {
  path: string;
  durationSec: number;
  width: number;
  height: number;
  sizeBytes: number;
  videoCodec: string;
  audioCodec: string;
};

export async function render(
  job: RenderJob,
  opts: RenderOptions
): Promise<RenderResult>;

export async function probe(path: string): Promise<ProbeResult>;
export async function checkEnvironment(): Promise<EnvCheck[]>;
```

---

## 4. Checks

### 4.1 Environment — `checkEnvironment()`

Called at the start of every `render()` and also on its own from the CLI.

| Check | Fails when | Message |
|---|---|---|
| `ffmpeg` on PATH | `ffmpeg -version` returns a non-zero code | how to install it |
| `ffprobe` on PATH | the same | it usually comes with ffmpeg |
| ffmpeg version ≥ 6 | older | the `xfade` filter is missing in older ones |
| codec `libx264` | not in `ffmpeg -encoders` | a build without x264 |
| codec `aac` | absent | the same |

### 4.2 Input — `validate.ts`

All of it **before** ffmpeg is started. The aim is for the error to arrive within a second.

**Common:**
- every path exists (`fs.access`) and is a file, not a folder
- size > 0
- the output folder exists and is writable
- the output file does not exist, or `overwrite: true`
- the output path ends in `.mp4`

**Audio:**
- `probe` finds an audio stream
- duration > 0.5 s and < 15 min (anything longer makes no sense for social media)

**Photos:**
- `probe` finds a video stream with a single frame, or a format on the list (`mjpeg`, `png`,
  `webp`) — **the extension is ignored**, the contents decide
- resolution ≥ 400 px on the shorter side, otherwise a quality warning

**Slideshow additionally:**
- at least 1 photo, at most 30
- when `secondsPerPhoto` is given: `photos.length × secondsPerPhoto` must not differ from the
  audio length by more than 20 % → otherwise a warning (not an error — the last photo simply
  gets trimmed or extended)

### 4.3 Output

After ffmpeg finishes, before the result is returned:

- the file exists, size > 10 kB
- `probe` confirms a video **and** an audio stream
- the video duration matches the audio duration ±0.5 s
- the resolution matches `DIMENSIONS[format]` exactly
- `pix_fmt` is `yuv420p`

When any check fails, **delete the faulty output** and throw an error. A half-finished file
on disk is worse than none.

---

## 5. Assembling the commands — `commands.ts`

Pure functions: `RenderJob` + dimensions → `string[]`. No I/O, no execution. That makes them
testable without ffmpeg.

```typescript
export function buildStillArgs(job, dim, output): string[];
export function buildSlideshowArgs(job, dim, output, audioDur): string[];
export function buildWaveformArgs(job, dim, output): string[];
```

### The scaling filter — shared by all modes

```
scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}
```

It crops to the centre. A portrait photo and a landscape photo thus give an equally sized
output with no black bars.

### still

```
ffmpeg -loop 1 -i {photo} -i {audio}
  -c:v libx264 -preset medium -tune stillimage -crf 20
  -c:a aac -b:a 192k
  -pix_fmt yuv420p -shortest -r 30
  -vf "{scale}"
  -movflags +faststart
  {output}
```

### slideshow

Without cross-fades, via the `concat` demuxer and a temporary list:

```
file 'foto1.jpg'
duration 4
file 'foto2.jpg'
duration 4
file 'foto2.jpg'
```

The last file is listed twice — otherwise `concat` shortens the final item. The list is
written into a temporary folder and deleted after the run.

With cross-fades via `xfade`, chained between adjacent inputs, with a 0.5 s transition. With
more than eight photos `xfade` slows things down noticeably — above eight photos switch to
`none` and note it in a warning.

### waveform

```
ffmpeg -i {audio} -i {photo} -filter_complex
  "[1:v]{scale}[bg];
   [0:a]showwaves=s={w}x{waveH}:mode=cline:colors={color}:rate=30[w];
   [bg][w]overlay=0:{h}-{waveH}-60[v]"
  -map "[v]" -map 0:a
  -c:v libx264 -crf 20 -c:a aac -b:a 192k
  -pix_fmt yuv420p -shortest -movflags +faststart
  {output}
```

`waveH` = 25 % of the height. The wave sits 60 px above the bottom edge so that the player
controls do not cover it.

---

## 6. Running and progress — `render.ts`

```typescript
const proc = spawn('ffmpeg', [...args, '-progress', 'pipe:1', '-nostats']);
```

`-progress pipe:1` sends `key=value` pairs to stdout. The interesting ones are `out_time_us`
and `speed`. Percentages are computed from them against the known audio length.

- stderr is **collected in full into a buffer** — on a non-zero return code the last 20 lines
  go into the error message
- `signal.aborted` → `proc.kill('SIGTERM')`, after 3 s `SIGKILL`, delete the partial output,
  throw `RenderCancelledError`
- `onProgress` is called at most 5× per second, not on every line

---

## 7. Errors — `errors.ts`

Typed classes, each with a `code` and, where applicable, a remedy:

| Class | When | `remedy` |
|---|---|---|
| `EnvironmentError` | ffmpeg / a codec is missing | the install command |
| `InputNotFoundError` | the file does not exist | the path it looked for |
| `InvalidMediaError` | the file is not an image / audio | what `probe` actually found |
| `OutputExistsError` | the target exists, `overwrite` false | `--overwrite` |
| `FfmpegFailedError` | a non-zero return code | the last 20 lines of stderr |
| `OutputValidationError` | the output failed a check | which check |
| `RenderCancelledError` | interrupted | — |

No error may escape as a bare `Error` carrying text from ffmpeg.

---

## 8. CLI — `cli.ts`

```bash
media check
media still     --photo f.jpg --audio a.mp3 [--format square] -o out.mp4
media slideshow --photos "fotky/*.jpg" --audio a.mp3 [--seconds 4]
                [--transition fade|none] [--format portrait] -o out.mp4
media waveform  --photo f.jpg --audio a.mp3 [--wave-color "white@0.85"] -o out.mp4
media probe     soubor.mp4
```

Common switches: `--overwrite`, `--json`, `--quiet`.

Behaviour:
- `--photos` accepts a glob, expanded in code (the Windows shell cannot do it); the files are
  sorted alphabetically
- progress as a percentage on stderr, on a rewritten line
- `--json` prints `RenderResult` to stdout and nothing else — for being called from the runner
- return code 0 on success, 1 on an error, 2 on an environment error

---

## 9. Tests

### 9.1 Fixtures — `tests/fixtures.ts`

**Binary files do not belong in the repository.** The test material is generated with ffmpeg
before the tests run and deleted afterwards:

```bash
# test images with various aspect ratios
ffmpeg -f lavfi -i "color=c=red:s=1600x900" -frames:v 1 wide.jpg
ffmpeg -f lavfi -i "color=c=blue:s=900x1600" -frames:v 1 tall.jpg
ffmpeg -f lavfi -i "color=c=green:s=200x200" -frames:v 1 tiny.jpg

# test audio, 6 seconds
ffmpeg -f lavfi -i "sine=frequency=440:duration=6" test.mp3

# a corrupted file
echo "this is not an image" > broken.jpg
```

### 9.2 Unit — without ffmpeg

`commands.test.ts`:
- `buildStillArgs` contains `-loop 1`, `-shortest` and the right dimensions
- the scaling filter differs between `portrait` and `square`
- a slideshow with `transition: 'none'` uses `concat`, with `fade` it uses `xfade`
- above 8 photos, `fade` degrades to `none`

`validate.test.ts`:
- a non-existent path → `InputNotFoundError`
- an empty file → `InvalidMediaError`
- an output without `.mp4` → an error
- an existing output without `--overwrite` → `OutputExistsError`
- a slideshow with 0 photos → an error
- a slideshow with 31 photos → an error

### 9.3 Integration — with ffmpeg

`render.test.ts`, skipped when ffmpeg is missing:

| Test | Verifies |
|---|---|
| still from a widescreen photo | output 1080×1080, duration 6 s ±0.5 |
| still from a portrait photo, portrait format | output 1080×1350 |
| slideshow from 3 photos | the duration matches the audio, 3 different colours in the frames |
| slideshow with fade | it completes, the duration matches |
| waveform | it completes, has both an audio and a video stream |
| a corrupted photo | `InvalidMediaError`, ffmpeg is never started |
| interruption after 1 s | `RenderCancelledError`, nothing left on disk |
| the output `pix_fmt` | always `yuv420p` |

Checking the colours in a slideshow: extract a frame at 1 s, 3 s and 5 s (`ffmpeg -ss`) and
verify the dominant colour. That is how you know the photos really do alternate and it did not
just stay on the first one.

---

## 10. Implementation instructions

**Order:**

1. `types.ts`, `errors.ts` — shapes first, behaviour second
2. `probe.ts` + `checkEnvironment()` — everything else rests on them
3. `commands.ts` + unit tests — fully testable without ffmpeg
4. `validate.ts` + unit tests
5. `render.ts` — running, progress, output checking
6. `cli.ts`
7. integration tests

**Do not:**

- read from R2, D1 or the network — the module is purely local
- try to replace ffmpeg with a pure-JS library
- add further modes until these three have passed the gate
- use `exec` or `execSync`

**Notes:**

- Windows: paths with spaces are handled by `spawn` with an argument array on its own, but the
  temporary list for `concat` needs forward slashes
- `-movflags +faststart` matters for web video; otherwise playback only starts once the whole
  file has downloaded
- `-preset medium` is a compromise; with a slideshow using `xfade` most of the time goes into
  the filter anyway, not into the codec

---

## 11. Module gate

- [ ] `media check` on a clean system without ffmpeg returns a comprehensible message
- [ ] All three modes produce a playable video
- [ ] A landscape and a portrait photo give the same resolution with no black bars
- [ ] The video duration matches the audio duration
- [ ] A video uploaded to Instagram by hand looks right and has sound
- [ ] Corrupted input fails before ffmpeg is started
- [ ] An interruption does not leave a half-finished file on disk
- [ ] The unit tests run without ffmpeg installed
- [ ] `--json` returns machine-readable output usable from the runner
