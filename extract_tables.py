"""Extract exact IPPT scoring tables from ~/workspace/ippt-calculator/index.html
(PUSH_T / SIT_T / RUN_T / AGE_BANDS) and write CSV + JSON data files.
This script is a build helper; the pack itself is the CSV/JSON/README/LICENSE.
"""
import csv
import json
import re
from pathlib import Path

SRC = Path.home() / "workspace/ippt-calculator/index.html"
OUT = Path.home() / "workspace/ippt-calculator/github-repo-pack/data"
OUT.mkdir(parents=True, exist_ok=True)

html = SRC.read_text(encoding="utf-8")

m = re.search(r'const AGE_BANDS=\[(.*?)\];', html, re.S)
age_bands = re.findall(r'"([^"]+)"', m.group(1))
assert len(age_bands) == 14, age_bands


def parse_table(name):
    m = re.search(r'const %s=\[(.*?)\];\n' % name, html, re.S)
    rows = re.findall(r'\[([0-9, ]+)\]', m.group(1))
    table = [[int(x) for x in r.split(',')] for r in rows]
    return table


PUSH = parse_table("PUSH_T")
SIT = parse_table("SIT_T")
RUN = parse_table("RUN_T")

assert len(PUSH) == 14 and all(len(r) == 61 for r in PUSH), "push shape"
assert len(SIT) == 14 and all(len(r) == 61 for r in SIT), "sit shape"
assert len(RUN) == 14 and all(len(r) == 60 for r in RUN), "run shape"


def fmt(sec):
    return f"{sec // 60}:{sec % 60:02d}"


# --- CSVs (long format, clear column names) ---
with open(OUT / "push_ups.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["age_group", "push_ups_reps", "points"])
    for g, band in enumerate(age_bands):
        for reps in range(61):
            w.writerow([band, reps, PUSH[g][reps]])

with open(OUT / "sit_ups.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["age_group", "sit_ups_reps", "points"])
    for g, band in enumerate(age_bands):
        for reps in range(61):
            w.writerow([band, reps, SIT[g][reps]])

with open(OUT / "run_2_4km.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["age_group", "run_time", "run_time_seconds", "points"])
    for g, band in enumerate(age_bands):
        for i in range(60):
            sec = 510 + i * 10  # 8:30, 8:40, ... 18:20
            w.writerow([band, fmt(sec), sec, RUN[g][i]])

# --- JSONs ---
def static_json(table, rep_key):
    return {
        "age_groups": age_bands,
        "by_age_group": {
            band: {str(reps): table[g][reps] for reps in range(61)}
            for g, band in enumerate(age_bands)
        },
    }


run_json = {
    "age_groups": age_bands,
    "note": "run_time is the 10-second band time. A finish time rounds UP to the next "
            "band: e.g. 12:31 uses the 12:40 row. 8:30 or faster uses the 8:30 row.",
    "by_age_group": {
        band: {fmt(510 + i * 10): RUN[g][i] for i in range(60)}
        for g, band in enumerate(age_bands)
    },
}

with open(OUT / "push_ups.json", "w") as f:
    json.dump(static_json(PUSH, "reps"), f, indent=2)
with open(OUT / "sit_ups.json", "w") as f:
    json.dump(static_json(SIT, "reps"), f, indent=2)
with open(OUT / "run_2_4km.json", "w") as f:
    json.dump(run_json, f, indent=2)

combined = {
    "title": "Singapore SAF IPPT scoring tables (male, exact table lookup)",
    "source": "Published SAF/CMPB IPPT scoring tables, as used by https://ipptscores.com",
    "methodology": "https://ipptscores.com/methodology/",
    "verified": "2026-10-30; cross-checked between two independent publishers and "
                "16 published anchor examples (see README.md)",
    "age_groups": age_bands,
    "stations": {
        "push_ups_1_min": {"max_points": 25, "reps_range": "0-60",
                           "by_age_group": static_json(PUSH, "reps")["by_age_group"]},
        "sit_ups_1_min": {"max_points": 25, "reps_range": "0-60",
                          "by_age_group": static_json(SIT, "reps")["by_age_group"]},
        "run_2_4km": {"max_points": 50, "bands": "8:30 to 18:20 in 10-second steps",
                      "rounding": "round UP to the next band",
                      "by_age_group": run_json["by_age_group"]},
    },
    "award_thresholds_nsman_total_out_of_100": {
        "fail": "below 51, or 0 points in any station",
        "pass": "51-60",
        "pass_with_incentive": "61-74 (SGD 200)",
        "silver": "75-84 (SGD 300)",
        "gold": "85-100, or 90-100 for Commandos / Divers / Guards (SGD 500)",
    },
    "licence": "CC BY 4.0 (see LICENSE)",
}
with open(OUT / "ippt_scoring_tables.json", "w") as f:
    json.dump(combined, f, indent=2)

# --- Sanity checks ---
g = age_bands.index("25–27")
p, s = PUSH[g][30], SIT[g][35]
run_band = (760 - 510) // 10  # 12:40
r = RUN[g][run_band]
print(f"Anchor age 25-27: push-ups 30 reps = {p} (expect 17), "
      f"sit-ups 35 reps = {s} (expect 18), 12:40 run = {r} (expect 31), "
      f"total = {p + s + r} (expect 66)")
assert (p, s, r) == (17, 18, 31), "ANCHOR FAILED"

# Monotonicity + boundary checks
for table, name in [(PUSH, "push"), (SIT, "sit")]:
    for g in range(14):
        assert all(table[g][i] <= table[g][i + 1] for i in range(60)), name
    for g in range(13):
        # Same reps: an older age group never scores FEWER points than a younger one.
        assert all(table[g + 1][i] >= table[g][i] for i in range(61)), name
for g in range(14):
    assert RUN[g][0] == 50, f"run 8:30 group {g}"
    assert all(RUN[g][i] >= RUN[g][i + 1] for i in range(59)), "run monotonic"
assert RUN[13][59] == 1, "oldest group 18:20 = 1"
print("All checks passed: 14 age groups, push/sit 0-60 reps, run 60 bands, monotonic, boundaries OK")
print("Files:", sorted(p.name for p in OUT.iterdir()))
