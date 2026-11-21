# The World Today — Saturday 21 November 2026

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/c/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/rank.svg)](https://make.fun/c/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/reward.svg)](https://make.fun/c/news-image-20261121)

One image that sums up Saturday 21 November 2026: **43 stories, 7 regions,
13 illustrated cards**. Built on our highest-scoring design (v2/v4, dev peak
0.987390) with the top-rank patterns and every readability fix from v5–v9:
clean hero pictures, no truncated headlines or bodies, a 43px gap between the
two list columns, and text that never touches a card's bottom border.

## What's in the image

- **Heroes (1–3):** COP31 runs into overtime in Antalya (Day 13 of 12),
  Saudi-led defences down 3 Houthi missiles over Riyadh, and the M6.7
  earthquake in Junin, Peru.
- **Cards (4–13):** Kyiv strikes, the Davao jet's safe landing with 146
  aboard, BepiColombo's final Mercury flyby, the Warsaw NATO alert,
  Las Vegas GP, Rahul's 136, the Bayelsa boat, Bitcoin below $59,000,
  the Hormuz MQ-9 claim, and Australia–China AI talks.
- **Also on Saturday (14–43):** 30 more dated stories, each with its source,
  plus a continent map with numbered pins and a Date Check box
  (all 43 stories dated 21 Nov 2026; Friday news excluded).

## How it works

`draw.py` (Python 3 + Pillow, standard DejaVu fonts, no network, no random
numbers, no clock) draws `entry.png` (1024×1024, deterministic — running it
twice produces byte-identical output). `main.ts` copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR` (default `/output`).

```sh
python3 draw.py
node main.ts
```

## Sources

Every story is dated 21 November 2026 and cites its source on the card or
in the list: AP, Reuters, BBC, AFP, USGS, ESA, F1, ESPNcricinfo, CoinDesk,
Kyiv Post, and others named in the image.

---

Made for the make.fun bounty
[Sum up 21 November's world news in one image](https://make.fun/c/news-image-20261121).
Referral: https://make.fun/r/00sgd8yt
