"""Generate per-instance vehicle-savings chart (Method right column, poster v2.2).

Data is re-derived from the frozen Stage 0 baseline and the accepted Stage 2.3
attempt16 per-run CSVs. Assertions enforce the published poster numbers:
total 87 -> 76 vehicles, savings on 5/12 instances.
"""
import csv
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

S0 = r"D:\UserData\Documents\GitHub\FURP-2026-Yiyang-GUO-EVRP-TW\experiments\baselines\stage00\per_run_results.csv"
A16 = r"D:\UserData\Documents\GitHub\FURP-2026-Yiyang-GUO-EVRP-TW\experiments\summaries\stage02_constraint_guided_attempt16_per_run_results.csv"
OUT = r"D:\UserData\Documents\GitHub\FURP-2026-Yiyang-GUO-EVRP-TW\poster_rebuild\assets\fig6_savings.png"


def load(path, vcol):
    per = defaultdict(list)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            per[row["instance"]].append(int(row[vcol]))
    return per


s0 = load(S0, "vehicle_count")
a16 = load(A16, "primary_vehicle_count")
assert set(s0) == set(a16), "instance sets differ"

order = sorted(s0)  # c101C5, c101_21, c104C10, ... family-grouped lexicographic
saved = {}
for inst in order:
    b, a = min(s0[inst]), min(a16[inst])
    assert a <= b, "vehicle-count regression on %s" % inst
    saved[inst] = b - a

assert sum(min(s0[i]) for i in order) == 87, "baseline total != 87"
assert sum(min(a16[i]) for i in order) == 76, "candidate total != 76"
assert sum(saved.values()) == 11, "total savings != 11"
assert sum(1 for v in saved.values() if v > 0) == 5, "savings instances != 5"

labels = [i.upper() for i in order]
vals = [saved[i] for i in order]
NOTT, LIGHT = "#10263B", "#C9D6E4"
colors = [NOTT if v > 0 else LIGHT for v in vals]

fig, ax = plt.subplots(figsize=(4.80, 2.76))
bars = ax.bar(range(len(vals)), vals, width=0.62, color=colors, zorder=3)
for x, v in enumerate(vals):
    if v > 0:
        ax.text(x, v + 0.14, str(v), ha="center", va="bottom",
                fontsize=8, color=NOTT, fontweight="bold")
ax.set_xticks(range(len(vals)))
ax.set_xticklabels(labels, rotation=40, ha="right", fontsize=7)
ax.set_ylim(0, 5.6)
ax.set_yticks([0, 1, 2, 3, 4, 5])
ax.tick_params(axis="y", labelsize=7.5, length=2)
ax.tick_params(axis="x", length=0)
ax.set_ylabel("vehicles saved (best of 3 seeds)", fontsize=8)
ax.grid(axis="y", color="#E3E8EF", lw=0.6, zorder=0)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color("#8A97A8")
    ax.spines[s].set_linewidth(0.7)
fig.subplots_adjust(left=0.115, right=0.995, top=0.985, bottom=0.27)
fig.savefig(OUT, dpi=600, facecolor="white")
print("saved chart ->", OUT)
print("savings:", dict(zip(labels, vals)))
