# Week 5 ALNS, Exact Charging Subproblem, and Branch-Price-and-Cut Methodology

## 1. Problem boundary

This implementation solves the electric vehicle routing problem with time windows,
EVRP-TW. Distances are unrounded 2D Euclidean `EUC_2D`; travel time is distance
divided by average speed; travel energy consumption is distance times the per-unit
energy rate. Vehicles leave the depot fully charged and may perform a full recharge
only at Schneider charging stations, with charging time linear in the replenished
energy. The current version does not claim support for partial recharge, nonlinear
charging, station capacity, or queueing constraints.

Stage 0's historical objective minimised total travel distance. From Stage 1 onward,
the formal unified objective is the lexicographic tuple `(vehicle count, total
distance, total charging time, charging count)`; vehicle count has absolute priority.
The historical `objective_value` is retained only as a total-distance compatibility
field and no longer represents the formal objective.

## 2. Main-problem / charging-subproblem decomposition

The ALNS-based matheuristic maintains customer route sequences

\[
S=(s_1,\ldots,s_m),\qquad s_k=(i_1,\ldots,i_{n_k}).
\]

The main problem decides customer assignment, the number of vehicle routes, and each
route's visit order. Once a customer sequence is fixed,
`solve_exact_charging(instance, customer_order)` decides the charging-station
insertion sequence. It returns the complete route, feasibility, distance, energy,
charge amount, charging time, label counts, pruning counts, and failure reasons. Any
infeasible subproblem makes the corresponding ALNS candidate unacceptable —
infeasibility is never disguised as feasibility through penalties.

### 2.1 Exact charging labelling

A label is

\[
L=(p,i,t,b,d,e,q,h,P),
\]

where `p` is the number of served customers, `i` the current position, `t` the time,
`b` the remaining battery, `d` the distance, `e` the total energy consumption, `q`
the total charge amount, `h` the charging time, and `P` the full node sequence.
Extensions are allowed only to the next fixed customer, to any legal charging
station, or back to the depot after all customers are served.

Travel extension:

\[
b'=b-rd_{ij},\qquad t'=\max\{a_j,t+d_{ij}/v\}.
\]

Customer nodes add a service time; charging-station nodes perform

\[
q'=Q-b',\qquad h'=gq',\qquad b'\leftarrow Q.
\]

Labels are deleted immediately if the battery goes negative or arrival exceeds the
due date. Within the same `(p,i)` state, label A dominates B if A's time and
distance are no greater, its battery no smaller, and at least one strictly better.
The algorithm therefore enumerates all undominated station-insertion structures
under the full-recharge linear model — it is not greedy charging.

## 3. ALNS design

ALNS uses the `random`, `worst`, and `related` destroy operators and the `greedy`,
`regret2`, and `energy` repair operators. Every insertion candidate calls the exact
charging subproblem. The acceptance criterion is simulated annealing; operator
weights adapt from rewards for acceptances, improvements, and new global-best
solutions. Candidates that reduce the vehicle count are always accepted; candidates
that increase it are always rejected; only at equal vehicle count does distance
degradation go through simulated annealing. Run logs record call counts,
acceptances, improvements, final weights, accepted/rejected counts, time-to-first-
feasible, time-to-best, and exact-subproblem call and label statistics.

## 4. Branch-Price-and-Cut and bidirectional labelling

The small-scale exact comparison uses the set-partitioning master problem:

\[
\min \sum_{r\in\Omega} c_r x_r,
\qquad
\sum_{r\in\Omega} a_{ir}x_r=1\quad\forall i,
\qquad x_r\in\{0,1\}.
\]

plus the capacity-derived fleet lower-bound cut:

\[
\sum_r x_r\ge
\left\lceil\frac{\sum_i q_i}{C}\right\rceil.
\]

`generate_columns_bidirectionally()` generates forward and backward labels
separately, joins them when their customer sets are disjoint and capacity-feasible,
then calls the exact charging subproblem to validate the complete route column. The
root starts from singleton columns and adds negative reduced-cost columns via LP
duals. To keep the current small-scale version exact, the branch tree uses the full
column pool enumerated by bidirectional labelling; the branching variables are route
columns. Every node retains the capacity lower-bound cut. Each column records its
vehicle, distance, charging-time, and charging-count contributions; the full column
pool finally confirms the four-level incumbent through exact lexicographic set
partitioning. Internal scalar search bounds serve search only and must not be
interpreted as formal objective gaps.

The implementation supports at most 8 customers and fails fast beyond that limit. It
is a genuine small-scale column generation, branching, and cutting implementation,
but not a production-grade BPC for 100-customer instances. Large-scale Ryan-Foster
branching and dynamic bidirectional ESPPRC pricing are not implemented; current
results must not be extrapolated to medium or large scale.

## 5. Unified feasibility validation

`validate_routes()` checks uniformly for all methods: depot endpoints, no depot in
route interiors, every customer visited exactly once, load, consistent time
propagation, time windows, non-negative battery, station legality, full-recharge
amounts, battery capacity, linear charging time, travel energy consumption, and the
declared objective value. The validator independently recomputes distance, energy,
charge amount, and charging time. Solutions that fail are marked `invalid` and never
enter the feasible-objective statistics.

## 6. Benchmark and battery bounds

The formal catalogue contains Schneider's 92 instances: 12 five-customer, 12
ten-customer, 12 fifteen-customer, and 56 100-customer instances. The full audit is
`experiments/summaries/schneider_instance_catalog.csv`.

For customer `i`, let `R` be the depot and charging-station set, and define

\[
B_{lb}=\max_i\{\min_{u\in R}e_{ui},\min_{v\in R}e_{iv}\},
\]

\[
B_{struct}=\max_i\min_{u,v\in R}(e_{ui}+e_{iv}).
\]

`B_lb` is the unavoidable single-segment energy lower bound; `B_struct` is a
customer-level necessary structural lower bound for each customer to sit between two
rechargeable nodes — not a sufficient condition for a complete feasible solution.
Formal instances use the original `B_exp=Q`; Stress instances use
`B_exp=1.05 B_struct` and re-pass the structural audit first. The stress factor is
`B_exp/B_struct`.

The Primary set pre-selects 12 instances: `c101C5/r105C5/rc105C5`,
`c104C10/r103C10/rc102C10`, `c106C15/r105C15/rc103C15`, and
`c101_21/r101_21/rc101_21`, covering 5/10/15/100 customers and the clustered,
random, and random-clustered families. BPC provides proven-optimal comparisons only
for the 5-customer subset; other scales are explicitly recorded as `not_applicable`.
This representative subset is not equivalent to full 92-instance statistics; the
selection rule fixes one C, one R, and one RC instance per scale, chosen without
reference to algorithm results.

## 7. Reproduction commands

```bash
uv sync --all-groups
uv run python -m evrptw.experiments.week05_advanced_benchmark \
  --benchmark-dir data/schneider \
  --output-dir results/week05_advanced \
  --instances c101C5,r105C5,rc105C5,c104C10,r103C10,rc102C10,c106C15,r105C15,rc103C15,c101_21,r101_21,rc101_21 \
  --stress-instances c101C5,r105C5,rc105C5 \
  --seeds 2014,2015,2016 \
  --alns-iterations 1000 \
  --time-limit-seconds 30 \
  --ga-population-size 60 \
  --ga-generations 80
```

Raw logs, solutions, and environment records live under `results/week05_advanced/`;
reviewable CSVs live under `experiments/summaries/week05_advanced_*.csv`.
