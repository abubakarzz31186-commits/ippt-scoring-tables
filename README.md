# IPPT Scoring Tables — Singapore SAF (male)

Exact, machine-readable Singapore Armed Forces (SAF) Individual Physical
Proficiency Test (IPPT) scoring tables for men, published as open data.

Use it to build calculators, training apps, spreadsheets, or to look up
exactly how many points a performance earns — without interpolating
between milestones, which is where most online calculators go wrong.

**Live calculator using these tables:** https://ipptscores.com
**How the tables were verified:** https://ipptscores.com/methodology/

## What is in this repo

| File | Contents |
|---|---|
| `data/push_ups.csv` / `data/push_ups.json` | Push-ups (1 minute): points for 0–60 reps × all 14 age groups (max 25 points) |
| `data/sit_ups.csv` / `data/sit_ups.json` | Sit-ups (1 minute): points for 0–60 reps × all 14 age groups (max 25 points) |
| `data/run_2_4km.csv` / `data/run_2_4km.json` | 2.4 km run: points for 10-second bands from 8:30 to 18:20 × all 14 age groups (max 50 points) |
| `data/ippt_scoring_tables.json` | All three stations in one file, plus NSman award thresholds |
| `LICENSE` | CC BY 4.0 — reuse freely with attribution (see below) |

CSV columns are named in full (`age_group`, `push_ups_reps` /
`sit_ups_reps`, `run_time`, `run_time_seconds`, `points`). JSON files are
keyed by age group, then by reps (push-ups / sit-ups) or band time
(run, `m:ss`).

## Age groups (14)

`<22`, `22–24`, `25–27`, `28–30`, `31–33`, `34–36`, `37–39`, `40–42`,
`43–45`, `46–48`, `49–51`, `52–54`, `55–57`, `58–60`.

**Male tables only.** Female IPPT tables are deliberately NOT included:
no complete, verifiable published female dataset could be found, so
publishing one here would risk wrong numbers. If a complete official or
second-source female dataset appears, it will be added and verified the
same way.

## Scoring rules

- Total = push-up points + sit-up points + run points, out of 100.
- You must score at least 1 point in **every** station — a zero in any
  station is an automatic fail, whatever the total.
- Run times round **up** to the next 10-second band: a finish of 12:31
  counts in the 12:40 band; 8:30 or faster counts in the 8:30 band.
- NSman award thresholds (total out of 100): Fail below 51 · Pass
  51–60 · Pass with Incentive 61–74 (SGD 200) · Silver 75–84 (SGD 300) ·
  Gold 85–100 (SGD 500; 90–100 for Commandos / Divers / Guards).
  Pre-enlistees and full-time national servicemen have different pass
  marks — see the methodology page.

## Worked example (regression anchor)

Age 25–27: 30 push-ups = **17 points**, 35 sit-ups = **18 points**,
12:40 run = **31 points** — total **66**, Pass with Incentive.
This example is checked against the generated files on every rebuild.

## Source and verification

**Source:** the published SAF / Central Manpower Base (CMPB) IPPT
scoring tables.

**How they were verified (30 October 2026):**

1. The tables in the live calculator were cross-checked cell-for-cell
   between two independent publishers of the CMPB/SAF chart
   (ipptcalculator.me's complete tables and ipptcalculator.live's full
   score table). The two sources agreed on every spot-checked row.
2. The tables were then validated against **16 published anchor
   examples** — worked examples and stated values from independent
   guides and the 2014 MINDEF revamp reporting. **All 16 matched.**
3. Monotonicity was checked throughout: more reps never score fewer
   points, a slower run never scores more points, and an older age
   group never scores fewer points than a younger one for the same
   performance.
4. The previous interpolation model this data replaced was measured
   against the exact tables first: it was wrong by up to 13 points on
   the run at slow times, which is why this dataset uses exact table
   lookup only — no formulas, no interpolation.

**One documented disagreement:** a 2015-era RunSociety article says a
12:30 run at age 28–30 earns 33 points; both current full tables say 34.
This dataset follows the current tables, as disclosed on the
methodology page.

**Extraction provenance:** the CSV/JSON files in `data/` were generated
directly from the verified tables in the live site's source
(`extract_tables.py` in this repo), and the anchor above was re-checked
in the generated files — not copied by hand.

## Reuse terms

The data files in this repository are licensed under
**Creative Commons Attribution 4.0 International (CC BY 4.0)**.
You may copy, adapt, and use them for any purpose, including
commercially, provided you give attribution: credit "IPPT Scores"
with a link to https://ipptscores.com (and, where practical, to
https://ipptscores.com/methodology/). Do not present your use as
endorsed by, or affiliated with, SAF, MINDEF, CMPB, OneNS, or
IPPT Scores. See `LICENSE` for the full licence terms.

## Disclaimer

An independent planning aid. Not affiliated with MINDEF, SAF, CMPB, or
OneNS. Official IPPT results are determined by SAF; always confirm
official matters with your unit or OneNS. Scoring tables are re-verified
quarterly against CMPB publications; if SAF publishes new charts, this
dataset will be updated.

## Suggested repo setup (for the owner)

- **Repo name:** `ippt-scoring-tables`
- **Description:** "Exact Singapore SAF IPPT scoring tables (male) as open data — push-ups, sit-ups and 2.4 km run points for all 14 age groups, verified against published tables. CSV + JSON, CC BY 4.0."
- **Website field:** https://ipptscores.com
- **Topics:** `ippt`, `singapore`, `saf`, `fitness`, `open-data`, `csv`, `json`, `scoring-tables`, `nsmen`, `national-service`
- Upload the whole pack: `README.md`, `LICENSE`, `extract_tables.py`,
  and the `data/` folder. Make the repo **public**.
