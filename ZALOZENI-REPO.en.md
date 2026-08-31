# How the repository was set up

Czech original: [ZALOZENI-REPO.md](ZALOZENI-REPO.md)

The repository was created on 30 August 2026 from the local `agent-kit` bundle as
**[Anamax443/ai-agenti](https://github.com/Anamax443/ai-agenti)** — **public**.
Public on purpose: it is a methodological shop window, with no sensitive data and no keys
(verified by a scan before the first commit).

Local path on this machine: `D:\git\ai-agenti`.

## What is configured

**Code security**

- *Secret scanning* + *Push protection* — enabled. It blocks a commit containing a key
  before it reaches history; pulling one out afterwards is worse.
- *Dependabot alerts* — enabled.

**CI** — `.github/workflows/kontrola.yml` runs on every push: a secret scan (gitleaks),
a link check over `*.md`, and the language-pair check
([`kontrola/dvojice.py`](kontrola/dvojice.py)). Tests and evals are commented out until
there is agent code in the repository.

**To consider later** — branch protection on `main` with a mandatory pull request. For solo
work it only slows things down for now; it starts to make sense once a second person joins.

## Structure — one repo, or several

For now, one repo holding the methodology and the designs. Once you start building:

- **Keep it here** as `03-projekty/<project>/kod/` — clear enough while you are on your own
- **Split it out** into its own repo — as soon as somebody else gets involved

The first option is the default. Splitting out is possible at any time; merging back is
worse. Watch for duplicates: the transcriber already has its own repo
([mp3totxt](https://github.com/Anamax443/mp3totxt)), and so does Gwalarn
([gwalarn](https://github.com/Anamax443/gwalarn)) — see `HANDOFF.md`.
