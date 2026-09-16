# Week 5 Weekly Report, Second Edition: EVRP-TW Main Algorithm, Exact Charging, Branch-Price-and-Cut, and Benchmark System Rebuild

## Status summary

- **Complete and verified**: full Schneider data ingestion with the 92-instance
  structural audit; the exact charging subproblem; the ALNS main algorithm; BPC
  with bidirectional labelling up to 8 customers; the unified validator;
  representative Primary experiments covering 5/10/15/100 customers and the C/R/RC
  families, plus battery Stress experiments.
- **Partially complete with verified boundaries**: BPC runs only on the 5-customer
  formal instances and does not support medium or large scale.
- **Not yet done / not yet verified**: full multi-seed statistics over all 92
  Schneider instances; partial/nonlinear charging; dynamic ESPPRC pricing; fixed
  fleet size and multi-objective trade-offs.

## 1. This week's goal and plan adjustment

The original plan was to continue preventive charging and route splitting on the
synthetic battery-60 failure cases. That approach had a low feasibility rate and
could not distinguish instance-generation defects from weak customer orderings and
charging-strategy defects. The original weekly report and historical results are
therefore retained, but the main method switched to an ALNS-based matheuristic +
exact charging subproblem, with a small-scale Branch-Price-and-Cut theoretical
comparison and the original Schneider benchmark.

The original `docs/05_weekly.md` remains unmodified, undeleted, and unrenamed; this
file is an independent second edition.

## 2. Baseline repositioning

| Method | Current role | Full EVRP-TW charging optimisation | Verification status |
|---|---|---:|---|
| ALNS_EXACT_CHARGING | Primary method | Yes, full-recharge linear model | Verified |
| BRANCH_PRICE_AND_CUT | Small-scale exact theoretical comparison | Yes, up to 8 customers | Verified |
| OR_TOOLS_VRPTW | Transparent classical baseline | No | Limitations verified |
| GA_VRPTW | Weak baseline | No, no exact station insertion | Limitations verified |

The low feasibility of OR-Tools and GA must not be interpreted as software failure:
they output VRPTW customer routes that are then checked by the same EVRP-TW
validator, and energy violations are honestly marked `invalid`.

## 3. Method and mathematical model

The main problem, charging subproblem, ALNS operators, BPC set-partitioning model,
fleet lower-bound cut, bidirectional labelling, dominance rules, and unified
validation formulas are detailed in `docs/week05_alns_bpc_methodology.md`. Code and
documents jointly adopt:

\[
b_j=b_i-rd_{ij},\quad
t_j=\max(a_j,t_i+d_{ij}/v),\quad
h_j=g(Q-b_j)\text{ at a station}.
\]

The key interfaces are:

- `solve_exact_charging(instance, customer_order)`: fixed customer sequence to a
  complete feasible route;
- `solve_alns(instance, seed, ...)`: customer assignment/ordering search calling
  exact charging;
- `solve_branch_price_and_cut(instance, ...)`: small-scale exact comparison;
- `validate_routes(instance, routes, claimed_objective=...)`: algorithm-agnostic
  validation.

## 4. Schneider benchmark and structural audit

The downloaded public mirror is stored in the Git-ignored `data/schneider/`,
containing the 92 instances and a SHA-256 manifest. All 92 instances pass the
customer-demand, earliest-arrival time-window, depot-horizon, in/out charging-node,
battery single-segment lower-bound, and customer-level structural lower-bound
checks. The complete per-instance table is
`experiments/summaries/schneider_instance_catalog.csv`.

### 4.1 This round's instances and minimum reasonable battery capacity

| Benchmark | Instance | Customers | Stations | Q | B_lb | B_struct | Q/B_struct | Audit |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Primary | c101C5 | 5 | 3 | 77.750 | 29.732 | 59.464 | 1.308 | pass |
| Primary | r105C5 | 5 | 3 | 60.630 | 27.785 | 55.570 | 1.091 | pass |
| Primary | rc105C5 | 5 | 4 | 77.750 | 19.925 | 39.850 | 1.951 | pass |
| Stress | c101C5 battery | 5 | 3 | 62.437 | 29.732 | 59.464 | 1.050 | pass |
| Stress | r105C5 battery | 5 | 3 | 58.348 | 27.785 | 55.570 | 1.050 | pass |
| Stress | rc105C5 battery | 5 | 4 | 41.842 | 19.925 | 39.850 | 1.050 | pass |

Primary keeps the original parameters; Stress only sets the battery to
`1.05 B_struct` without modifying coordinates, demands, stations, or time windows.
The stress scenarios still pass the necessary structural checks, but a structural
check is not a proof that a complete feasible route exists.

## 5. Environment and experiment setup

| Item | Actual value |
|---|---|
| Runtime window (UTC) | 2026-07-12 17:04:52.038179 to 17:10:05.012464 |
| OS / CPU | macOS 27.0 arm64 / Apple M5, 10 logical CPUs |
| RAM / GPU | 16 GiB / GPU unused |
| Python / C++ compiler | CPython 3.13.13 / Apple clang 17.0.0 |
| LP backend | SciPy 1.17.1 + HiGHS 1.14.0 |
| Other solvers | OR-Tools 9.15.6755; Gurobi 13.0.2; CPLEX 22.2.0.0 |
| Threads / wall limit | 1 / 30 s per run |
| Random seeds | 2014, 2015, 2016 |
| ALNS / GA | 1000 iterations / population 60, generations 80 |
| Install command | `uv sync --all-groups` |

Full dependencies, tool versions, commands, and environment variables are in
`results/week05_advanced/environment.json`. Gurobi/CPLEX were configured but this
round's BPC restricted master used the open-source HiGHS; no GPU was involved.

## 6. Experiment results

### 6.1 Primary feasibility by scale

| Size | Method | Feasible / Runs | Feasibility rate | Mean runtime (s) |
|---:|---|---:|---:|---:|
| 5 | ALNS_EXACT_CHARGING | 9 / 9 | 100.0% | 0.0157 |
| 5 | BRANCH_PRICE_AND_CUT | 3 / 3 | 100.0% | 0.0472 |
| 5 | OR_TOOLS_VRPTW | 0 / 3 | 0.0% | 0.0027 |
| 5 | GA_VRPTW | 3 / 9 | 33.3% | 0.0993 |
| 10 | ALNS_EXACT_CHARGING | 9 / 9 | 100.0% | 0.4028 |
| 10 | BRANCH_PRICE_AND_CUT | 0 / 3 (`not_applicable`) | N/A | 0.0000 |
| 10 | OR_TOOLS_VRPTW | 0 / 3 | 0.0% | 0.0027 |
| 10 | GA_VRPTW | 3 / 9 | 33.3% | 0.1682 |
| 15 | ALNS_EXACT_CHARGING | 9 / 9 | 100.0% | 1.2211 |
| 15 | BRANCH_PRICE_AND_CUT | 0 / 3 (`not_applicable`) | N/A | 0.0000 |
| 15 | OR_TOOLS_VRPTW | 0 / 3 | 0.0% | 0.0049 |
| 15 | GA_VRPTW | 0 / 9 | 0.0% | 0.2498 |
| 100 | ALNS_EXACT_CHARGING | 9 / 9 | 100.0% | 30.0127 |
| 100 | BRANCH_PRICE_AND_CUT | 0 / 3 (`not_applicable`) | N/A | 0.0000 |
| 100 | OR_TOOLS_VRPTW | 0 / 3 | 0.0% | 0.1808 |
| 100 | GA_VRPTW | 0 / 9 | 0.0% | 2.2243 |

Stress: ALNS 9/9 and BPC 3/3 feasible; OR-Tools 0/3 and GA 0/9. Mean runtimes were
0.0135, 0.0347, 0.0015, and 0.0976 seconds respectively.

### 6.2 Primary ALNS multi-run statistics

| Instance | Best | Mean | Median | Worst | Std | Feasible | Gap to proven optimum |
|---|---:|---:|---:|---:|---:|---:|---:|
| c101C5 | 247.1497 | 247.1497 | 247.1497 | 247.1497 | 0.0000 | 3/3 | 0.0% |
| r105C5 | 156.0821 | 156.0821 | 156.0821 | 156.0821 | 0.0000 | 3/3 | 0.0% |
| rc105C5 | 238.0522 | 239.1336 | 238.0522 | 241.2964 | 1.5293 | 3/3 | best 0.0% |

### 6.3 BPC exact statistics

| Benchmark | Instance | Root LB | Incumbent | Final LB | Gap | Nodes | Columns | Joined labels |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Primary | c101C5 | 247.1497 | 247.1497 | 247.1497 | 0% | 1 | 17 | 610 |
| Primary | r105C5 | 156.0821 | 156.0821 | 156.0821 | 0% | 1 | 16 | 610 |
| Primary | rc105C5 | 231.1586 | 238.0522 | 238.0522 | 0% | 9 | 18 | 610 |
| Stress | c101C5 | 250.0380 | 250.0380 | 250.0380 | 0% | 1 | 14 | 610 |
| Stress | r105C5 | 156.0821 | 156.0821 | 156.0821 | 0% | 1 | 16 | 610 |
| Stress | rc105C5 | 265.0945 | 265.0945 | 265.0945 | 0% | 1 | 13 | 610 |

### 6.4 100-customer ALNS results

| Instance | Seed | Objective | Vehicles | Feasible | Runtime (s) |
|---|---:|---:|---:|---|---:|
| c101_21 | 2014 | 1234.5033 | 14 | yes | 30.045 |
| c101_21 | 2015 | 1237.1389 | 14 | yes | 30.018 |
| c101_21 | 2016 | 1237.1389 | 14 | yes | 30.005 |
| r101_21 | 2014 | 1816.6087 | 23 | yes | 30.003 |
| r101_21 | 2015 | 1788.2156 | 22 | yes | 30.002 |
| r101_21 | 2016 | 2091.7771 | 28 | yes | 30.004 |
| rc101_21 | 2014 | 2167.8629 | 24 | yes | 30.025 |
| rc101_21 | 2015 | 2230.9209 | 25 | yes | 30.004 |
| rc101_21 | 2016 | 2271.0743 | 25 | yes | 30.008 |

The large-scale results show the current implementation stably finds feasible
solutions, but R/RC vehicle counts and objectives have no exact gap and must not be
claimed near-optimal. BPC does not run beyond 8 customers and produces no fake
lower bounds.

Per-run ALNS operator calls, successes, weights, acceptance statistics, and exact
charging call times are kept in the per-run CSV JSON fields and the corresponding
raw logs; the 18 nested statistics are not hand-transcribed into the weekly report,
avoiding a second source of truth.

## 7. Anomalies, failures, and fixes

| Type | Observation | Handling | Current status |
|---|---|---|---|
| invalid baseline | All OR-Tools runs show energy violations | Results retained, excluded from feasible-objective means | Verified |
| weak GA | Primary feasible only on c101C5; Stress all invalid | Failures retained; demoted to weak baseline | Verified |
| BPC optimality defect | The first version wrongly reported rc105C5's 241.8894 as optimal, but ALNS reached 238.0522 | Traced to column-variable branching missing a zero-reduced-cost integer column; branch nodes now use the full small-scale column pool | Fixed, regression-verified |
| scale limit | The enumerated column pool grows factorially with customers | `max_customers=8` fail fast | Limit verified |

All failure details are in
`experiments/summaries/week05_advanced_failure_cases.csv`; no timeout, invalid, or
error records were deleted. This round had no timeouts or errors.

## 8. Added and modified files

New core files: `src/evrptw/benchmark.py`, `charging.py`, `alns.py`, `bpc.py`,
`experiments/week05_advanced_benchmark.py`, and their tests. Modified:
`validation.py`, `pyproject.toml`, `README.md`. Added review CSVs, this report, and
`docs/week05_alns_bpc_methodology.md`. The historical Week 5 route-splitting code,
logs, and the original weekly report are all retained.

## 9. Current limitations and next-stage plan

1. **Next-stage task 1**: run multi-seed ALNS on the 10/15-customer Schneider
   instances and implement dynamic bidirectional ESPPRC pricing, gradually
   extending the exact comparison from 5 to 10 customers.
2. **Next-stage task 2**: on a pre-declared 100-customer C/R/RC subset, use a
   unified 30/60/300 s wall-clock budget and report feasibility, stability,
   vehicle counts, and gaps; do not extrapolate this week's small-scale 100%
   feasibility into large-scale conclusions.

## 10. Revision Log

| Datetime (UTC) | File | Change | Reason | Impact | Verification | Status |
|---|---|---|---|---|---|---|
| 2026-07-12 16:35 | benchmark/charging modules | Added instance audit, battery bounds, and exact charging | Fix arbitrary-battery and greedy-insertion problems | Instance admission, route feasibility | Unit tests and the 92-instance audit | Done |
| 2026-07-12 16:39 | ALNS/BPC modules | Main-method and exact-comparison rebuild | Replace the weak GA main method | Algorithm and theoretical comparison | toy + Schneider c101C5 | Done |
| 2026-07-12 16:44 | BPC branching | Enabled the full small-scale column pool at branch nodes | Fix the false optimality claim | BPC bounds/incumbent | rc105C5 238.0522, gap 0 | Done |
| 2026-07-12 17:04 | experiment/results | Reran the 120 formal records with a unified GA wall-clock cap | Cover 5/10/15/100 customers with fair stopping conditions | All formal tables | validator + raw logs + summary recomputation | Done |
| 2026-07-12 16:50 | This weekly report and methodology doc | Added second edition without overwriting the original | Record the algorithm and benchmark rebuild | Documentation and reproduction entry | Path/CSV/command cross-check | Done |

## 11. Data index

| Data | Path |
|---|---|
| 92-instance catalogue audit | `experiments/summaries/schneider_instance_catalog.csv` |
| This round's instance audits | `experiments/summaries/week05_advanced_instance_audits.csv` |
| 120 per-run results | `experiments/summaries/week05_advanced_per_run_results.csv` |
| Summary statistics | `experiments/summaries/week05_advanced_summary_results.csv` |
| Failures / invalid solutions | `experiments/summaries/week05_advanced_failure_cases.csv` |
| Raw logs and solutions | `results/week05_advanced/raw/`, `results/week05_advanced/solutions/` |
