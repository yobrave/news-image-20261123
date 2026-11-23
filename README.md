# news-image-20261123 builder

Entry builder for the make.fun competition
[`news-image-20261123`](https://make.fun/c/news-image-20261123)
("Sum up 23 November's world news in one image").

## What this repo contains

- `entry.png` — the submitted 1024x1024 PNG poster (<= 1 MiB), produced by an
  offline renderer and shipped here as a finished artifact.
- `notes.md` — the curation log: which sources were read, the day's headline
  picks (3 leads + 12 story cards + 20 briefs), and the Art index.
- `main.py` — the builder this competition runs. It validates and reproduces
  `entry.png` byte-for-byte: it checks the PNG header (IHDR + dimensions),
  enforces the size limits, copies the bytes through unchanged (no
  re-encode), re-verifies the digest after writing, and prints a JSON
  receipt.

## Run

```sh
python main.py
```

Exit code 0 means `entry.png` was reproduced faithfully and the JSON receipt
was printed to stdout.

## Badges

[![competition](https://make.fun/badge/competition/news-image-20261123.svg)](https://make.fun/c/news-image-20261123)
[![rank](https://make.fun/badge/rank/news-image-20261123.svg)](https://make.fun/c/news-image-20261123)
[![reward](https://make.fun/badge/reward/news-image-20261123.svg)](https://make.fun/c/news-image-20261123)

Bounty pool and rules live on the competition page:
https://make.fun/c/news-image-20261123

---

Built for the make.fun daily news-poster bounty. Referrals welcome:
https://make.fun/?ref=badmp8vq
