# BUILD-NOTES — news-image-20261122

Entry: a newspaper front page ("THE WORLD IN ONE DAY") summing up the world
news of **Sunday, 22 November 2026**. Drawn programmatically by
`draw_image.py` (Python + PIL, DejaVu fonts); `main.py` only copies the
finished image to the output directory.

## Stories chosen (all verified as 22 Nov 2026 news)

1. **COP31 climate talks collapse with no deal (Antalya, Turkey)** — UN
   climate talks ended without an agreement after overtime, split over
   mentioning fossil fuels. Reported 22 Nov 2026 by KPFA's Pacifica Evening
   News (11.22.26) and Standard Topic's Nov 22 world archive.
2. **Democrats win biggest US House majority since 1992** — the AP called
   North Carolina's 5th District for Democrat Chuck Hubbard on Sunday after
   a recount confirmed his 330-vote lead; Virginia Foxx conceded late
   Sunday, giving Democrats 258 seats to 173 Republicans. Reported 22 Nov
   2026 (dpa-AFX via TradingView; Public Radio East, 23 Nov 2026 6:17 AM
   EST, recounting Sunday's call).
3. **Two supertankers hit mines near the Strait of Hormuz** — Iran's navy
   said two supertankers hit naval mines east of the strait; Trump said he
   is inclined to strike Iran again after the new year if talks fail.
   First reported 22 Nov 2026 (Daily Summary of World, "First reported
   22 Nov, 09:13 GMT-8"; Candid Dragon evening briefing, 22 Nov 2026).
4. **Drone strike hits Russian warship at Benghazi** — a suspected sea drone
   hit the Russian corvette Merkury at the Benghazi naval base in eastern
   Libya early Sunday, causing an explosion and fire. First reported 22 Nov
   2026 (Daily Summary of World, "First reported 22 Nov, 07:36 GMT-8";
   Standard Topic Nov 22 archive).
5. **Russian attack near Kyiv kills three** — a Russian attack near
   Ukraine's capital struck an apartment building, killing 3 and burying
   others. Reported 22 Nov 2026 (AP via KIRO 7, "November 22, 2026 at
   8:53 am PST").
6. **Delta outage delays 1,600+ flights** — Delta's weight-and-balance
   system went down Sunday morning; the FAA briefly halted Delta flights
   bound for Atlanta. Reported 22 Nov 2026 (Candid Dragon evening briefing,
   22 Nov 2026).

Footer "ALSO TODAY" (all reported 22 Nov 2026): Israeli settlers torched
vehicles and homes in West Bank villages (KPFA 11.22.26; Standard Topic
Nov 22); Europe's cost-of-living protests entered a third straight day
(Daily Summary of World, 22 Nov); thousands marched in Istanbul against
the state seizure of Sözcü TV (ChronicleAI, 22 Nov 2026).

Deliberately excluded: the ICJ ruling that Myanmar committed genocide
against the Rohingya — it was delivered on **19 November 2026**, not
22 November, so it does not belong in a 22 Nov image. The Indonesian candy
factory fire broke out on Saturday 21 November, so it is not a headline
panel either (its Sunday search developments were reported 22 Nov, but the
event itself is a 21 Nov story).

## Image specs

- `entry.png`: PNG, 1024 x 1024 px, 116,743 bytes (under the 1,048,576-byte
  cap). Masthead names "SUNDAY, 22 NOVEMBER 2026" prominently in red.
- Six panels (3 x 2 grid), each with a kicker, a pictogram, a headline and
  a one-line summary; an "ALSO TODAY" footer strip; sources line at the
  bottom. Viewed after drawing; text checked legible, no overlap or
  clipping (one capitol pictogram was resized to stay inside its panel).

## Determinism

`main.py` (Python 3.13 stdlib only, no network) copies the `entry.png`
shipped in the repo to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`),
creating the directory if needed, and asserts the copy size matches. Both
graded runs therefore write byte-identical files. Verified by running
`main.py` twice into two different directories and comparing SHA-256
hashes (see verification below).

## Verification (build time)

- `python3 draw_image.py` → entry.png 1024x1024, 116,743 bytes.
- `MAKEFUN_OUTPUT_DIR=out1 python3 main.py` and
  `MAKEFUN_OUTPUT_DIR=out2 python3 main.py` → both outputs byte-identical
  (SHA-256 4ffe9d16162c137bec7c854fbcb1cc659aa5d72b107fb37d64b817e54b2a5b2c,
  same as entry.png itself).

## Rewrite 23 Nov 2026 ~20:53 WIB — thinking_reproduces fix

The kit check failed `thinking_reproduces`: main.py had 0 authored lines
and draw_image.py had 61 copied + 95 read lines, because the original
build agent had re-typed the 20 Nov entry's code. A fix agent rewrote
BOTH files fresh in its own session, from this BUILD-NOTES spec and the
viewed target image only — it never opened or read any existing .py file
(neither this entry's nor the 20 Nov entry's), using its own structure
(data-driven panel list, own helper names and pictogram code). The image
keeps the same masthead, six stories, headlines, sub-lines, footer and
sources; two pictograms were adjusted while re-drawing (capitol dome
shortened so its finial stays inside its panel, airliner redrawn as a
proper top-down plane with swept wings).

- `python3 draw_image.py` → entry.png 1024x1024, 122,518 bytes (under the
  1 MiB cap), SHA-256
  8e7f4552f7d2db84620d924b9fbf24adf74dae6cc64127fee5421f20f6bc2b8e.
- `MAKEFUN_OUTPUT_DIR=out1 python3 main.py` and `...=out2 ...` → both
  outputs byte-identical to each other and to entry.png (same SHA-256).
- Image viewed after the rewrite: masthead date prominent and correct,
  all six headlines + sub-lines present and spelled correctly, footer
  and sources line present, nothing cut off or garbled.
