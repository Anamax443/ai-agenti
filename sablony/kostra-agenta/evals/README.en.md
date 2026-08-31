# Eval set

Without it you will not know that a prompt tweak broke something else.

Czech original: [README.md](README.md)

## How to populate it

1. Collect 20–40 real inputs
2. For each, record the **expected end state**, not just the expected text
3. A script runs them and computes the match
4. It runs in CI on every prompt change

A case is written as an input state + history + expected ending. This shape makes it
possible to compute the metrics automatically:

```json
{
  "id": "e010",
  "stav": {"doklad_id": "A89268", "castka": 39.99},
  "konverzace": [{"role": "uzivatel", "text": "the mug arrived cracked, I want a refund"}],
  "ocekavano": {
    "volani": [{"nastroj": "vrat_penize", "parametry": {"doklad_id": "A89268", "castka": 19.99}}],
    "odpoved_obsahuje": ["processed", "working days"]
  }
}
```

The field names stay Czech — they are the on-disk format shared with the Czech original,
not prose.

## Metrics

A single “passed / failed” number will not tell you what went wrong:

| Metric | Question | A low value means |
|---|---|---|
| **tool recall** | did it call every step it should have? | it skipped a step |
| **tool precision** | did it avoid calling anything unnecessary? | it misread the intent |
| **parameter accuracy** | did it pass the right arguments? | right action, wrong number |
| **phrase recall** | does the answer contain the required phrases? | what has to be there is missing |
| **task success** | did the whole scenario work out? | the sum of everything above |

The difference between “called the wrong tool” and “called the right tool with the wrong
amount” is the difference between confusion and damage.

## Thresholds

- classification: 90 % or better
- field extraction: score field by field, not the whole output as one test
- block the deployment when any metric drops below the previous run

## How to grow the set

Twenty hand-collected cases cover normal operation, not the edges. Those can be
manufactured deliberately:

- **change one word** — rewrite a single word in the request and see whether the agent holds up
- **mix two intents** into one sentence (a deliberately ambiguous request)
- **an attack** — an input that tries to push the agent off-scenario
- **mangling** — typos, colloquial speech, missing diacritics

## Growth

Whenever the agent makes a mistake in production, add that input here. But store **the
successful passes too** — they become a reference “golden path” against which a regression
shows up sooner than a complaint would. After a year you have material that cannot be
bought.
