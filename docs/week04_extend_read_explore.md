# Week 4 Extension: New Settings, Improved Repair, and Hybrid Post-Processing

## Research Question

Week 4 follows the required activity order:

1. try new experimental settings;
2. improve an existing method;
3. combine ideas from different methods.

The focused question is:

> Under different battery capacities, when do the Week 3 VRPTW baselines and
> late charging repair fail, and does anticipatory charging repair reduce EVRP-TW
> energy violations more reliably?

The experiment keeps the Week 3 comparison controls: same generated
Schneider-style instances, same seeds, same validator, and same metrics. The new
experimental setting is a battery-capacity sweep over `60`, `80`, `100`, and
`120`.

## Step 1: Try New Experimental Settings

The Week 4 runner is:

```bash
uv run python -m evrptw.experiments.week04_extension --output-dir results/week04
```

The tested methods are:

| Method | Role |
|---|---|
| `OR_TOOLS_VRPTW` | OR-Tools route constructor; ignores EV energy during construction |
| `OR_TOOLS_VRPTW_CHARGING_REPAIR` | OR-Tools plus the Week 3 late charging insertion |
| `GA_VRPTW` | GA route constructor; stochastic VRPTW baseline |
| `GA_VRPTW_CHARGING_REPAIR` | GA plus the Week 3 late charging insertion |

The battery sweep confirms that the pure VRPTW constructors remain infeasible
for EVRP-TW validation at all tested battery capacities. Their energy violations
fall as battery capacity increases, but feasibility remains zero because the
routes still ignore charging reachability.

| Battery | OR-Tools baseline feasible rate | OR-Tools avg energy violations | GA baseline feasible rate | GA avg energy violations |
|---:|---:|---:|---:|---:|
| 60 | 0.000 | 78.000 | 0.000 | 91.333 |
| 80 | 0.000 | 57.556 | 0.000 | 60.444 |
| 100 | 0.000 | 40.889 | 0.000 | 27.333 |
| 120 | 0.000 | 28.667 | 0.000 | 5.333 |

The Week 3 late charging repair helps GA more than OR-Tools, but it is still a
post-processing rule. It often waits until a route segment is already close to
infeasible, so it cannot always recover a compact VRPTW route.

## Step 2: Improve Existing Method

The new improvement is `insert_anticipatory_charging_stations()`. It does not
replace the Week 3 repair; it is added beside it so Week 3 remains reproducible.

The rule is simple:

- before traversing a leg, estimate the remaining battery after that leg;
- if the destination would be a customer with no reachable depot or charging
  station afterward, insert a reachable charging station before that customer;
- if the leg itself is already infeasible, also try to insert a station before
  the destination;
- if no reachable station can repair the risk, record the unrepaired leg.

This is still a heuristic. It does not reorder customers, split routes, or solve
charging amounts as continuous decisions. Its purpose is to test whether earlier
charging placement is more effective than late charging insertion.

## Step 3: Combine Ideas From Different Methods

The hybrid comparison keeps each route constructor fixed and changes only the
post-processing layer:

| Constructor | Post-processing variants |
|---|---|
| OR-Tools VRPTW | none, late charging repair, anticipatory charging repair |
| GA VRPTW | none, late charging repair, anticipatory charging repair |

This isolates the effect of repair strategy from the effect of route
construction.

| Battery | Method | Avg feasible rate | Avg energy violations | Avg charging count |
|---:|---|---:|---:|---:|
| 60 | `OR_TOOLS_VRPTW_CHARGING_REPAIR` | 0.000 | 75.333 | 0.667 |
| 60 | `OR_TOOLS_VRPTW_ANTICIPATORY_REPAIR` | 0.000 | 25.111 | 18.222 |
| 60 | `GA_VRPTW_CHARGING_REPAIR` | 0.000 | 47.111 | 44.222 |
| 60 | `GA_VRPTW_ANTICIPATORY_REPAIR` | 0.111 | 4.000 | 130.444 |
| 80 | `OR_TOOLS_VRPTW_CHARGING_REPAIR` | 0.000 | 55.556 | 0.333 |
| 80 | `OR_TOOLS_VRPTW_ANTICIPATORY_REPAIR` | 1.000 | 0.000 | 17.667 |
| 80 | `GA_VRPTW_CHARGING_REPAIR` | 0.000 | 7.222 | 53.222 |
| 80 | `GA_VRPTW_ANTICIPATORY_REPAIR` | 1.000 | 0.000 | 67.667 |
| 100 | `OR_TOOLS_VRPTW_CHARGING_REPAIR` | 0.000 | 37.111 | 1.000 |
| 100 | `OR_TOOLS_VRPTW_ANTICIPATORY_REPAIR` | 1.000 | 0.000 | 11.444 |
| 100 | `GA_VRPTW_CHARGING_REPAIR` | 1.000 | 0.000 | 27.333 |
| 100 | `GA_VRPTW_ANTICIPATORY_REPAIR` | 1.000 | 0.000 | 27.333 |
| 120 | `OR_TOOLS_VRPTW_CHARGING_REPAIR` | 0.000 | 24.444 | 1.000 |
| 120 | `OR_TOOLS_VRPTW_ANTICIPATORY_REPAIR` | 1.000 | 0.000 | 7.222 |
| 120 | `GA_VRPTW_CHARGING_REPAIR` | 1.000 | 0.000 | 5.333 |
| 120 | `GA_VRPTW_ANTICIPATORY_REPAIR` | 1.000 | 0.000 | 5.333 |

The main result is clear: anticipatory repair is much stronger than late repair
when battery capacity is 80 or higher. At battery 60, the problem is still too
tight for repair-only logic, especially for compact OR-Tools routes. That
failure is useful evidence: some routes need splitting or energy-aware
construction, not only station insertion.

## Original Paper Notes

The detailed Week 4 reading notes are now kept separately in
[`docs/week04_reading_notes.md`](week04_reading_notes.md). They are based on
the local PDFs in `/Users/guoyiyang/Documents/FURP-2026-EVRP-TW-Literature`;
the PDFs are not stored in Git.

## Failure Analysis

At battery capacity 60, anticipatory repair still fails in most settings. For
example, OR-Tools with anticipatory repair has average energy violations of
17.667, 26.667, and 31.000 for 50, 100, and 200 customers respectively. GA with
anticipatory repair is much better, but still not fully reliable at battery 60.

The failure mode is consistent with the Week 3 diagnosis: once route geometry is
too tight, station insertion alone is not enough. The route may need to be split
or constructed with battery reachability as a primary constraint.

## Conclusion

Week 4 produces a stronger result than Week 3. The battery sweep first shows how
baseline infeasibility changes with battery capacity. The improved repair then
shows that anticipatory charging placement can make all tested OR-Tools and GA
routes feasible at battery capacities 80, 100, and 120. The hybrid comparison
shows that the constructor matters less than whether the post-processing is
energy-aware early enough.

The next technical step should not be POMO or truck-drone routing. It should be
route splitting or energy-aware construction for the low-battery case, followed
by a partial-recharge model once the full-recharge repair workflow is stable.
