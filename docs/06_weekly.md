# Week 6: EVRP-TW Method Integration and Batch Evaluation

## 1. Current Progress

This week selected **Track B: Combine Existing Methods Into One Workflow**.

As of Week 5, the project already had reproducible Schneider benchmark reading, structural
auditing, ALNS (Adaptive Large Neighbourhood Search), an exact charging subproblem, a
small-scale Branch-Price-and-Cut comparison, OR-Tools/GA baselines, and a unified
feasibility validator. This week's focus is therefore not adding new RL (Reinforcement
Learning) or DL (Deep Learning) models, but organising these components into one
explainable, comparable, and batch-verifiable research pipeline.

The reasons for choosing Track B:

- The current methods already run from instance input to final feasible solutions and
  summary tables;
- Week 5 already produced enough multi-instance, multi-scale, and multi-seed results;
- The main question has shifted from "does it run" to "is the combined method more
  reliable than simple baselines";
- Before introducing learning models, clear decision objects, reliable labels, and
  reproducible experimental controls should be established first.

## 2. Method Design

### 2.1 The unified workflow

```text
Schneider EVRP-TW instance
  -> instance parsing and structural audit
  -> ALNS customer assignment and ordering
  -> exact charging for each proposed customer sequence
  -> unified feasibility and objective validation
  -> comparison with BPC / OR-Tools / GA
  -> per-run records, failure records, and summary table
```

Each component's responsibility:

1. **Instance audit** checks demands, time windows, battery lower bounds, charging
   nodes, and depot horizons, exposing structural problems before running algorithms.
2. **ALNS** searches over customer assignments and visit orders, improving candidate
   solutions with destroy/repair operators.
3. **Exact charging subproblem** solves station insertion and full-recharge decisions
   for each fixed customer sequence, preventing greedy station insertion from masking
   energy infeasibility.
4. **Unified validator** independently checks capacity, time windows, battery,
   coverage, and objective values; invalid results never enter the feasible-objective
   statistics.
5. **Branch-Price-and-Cut** provides a small-scale exact theoretical comparison for
   instances with at most 8 customers; beyond its verified capability it explicitly
   returns `not_applicable` and does not fabricate lower bounds.
6. **OR-Tools VRPTW and GA VRPTW** are retained as transparent baselines, showing how
   customer routes that lack exact charging optimisation fail under EVRP-TW
   constraints.

This connection order separates the main-problem search from the charging subproblem
while letting every algorithm be checked by the same validator and result schema.
Comparisons prioritise feasibility first, then compare objective values, runtime, and
stability across random seeds for feasible solutions.

### 2.2 Simplified pseudocode

```text
for each instance and seed:
    audit(instance)
    customer_sequences = ALNS(instance, seed)
    routes = exact_charging(instance, customer_sequences)
    result = validate(instance, routes)
    retain feasible objective or explicit failure reason

for each supported small instance:
    exact_reference = BranchPriceAndCut(instance)
    compare ALNS with the proven reference

aggregate all runs by instance, scale, algorithm, and feasibility
```

## 3. Experiment Plan

### 3.1 Comparisons, scope, and parameters

- **Primary method**: `ALNS_EXACT_CHARGING`.
- **Exact reference**: `BRANCH_PRICE_AND_CUT`, only for at most 8 customers.
- **Baselines**: `OR_TOOLS_VRPTW` and `GA_VRPTW`.
- **Primary instances**: 12 Schneider instances covering the C/R/RC families and the
  5/10/15/100-customer scales.
- **Stress instances**: 3 five-customer low-battery scenarios.
- **Total scenarios**: 15.
- **Random seeds**: 2014, 2015, 2016, for ALNS and GA.
- **Stopping conditions**: ALNS 1000 iterations and at most 30 seconds per run;
  single thread.

### 3.2 Recorded metrics

- feasibility rate and failure reasons;
- objective value, best, mean, median, worst, and standard deviation;
- vehicle count, total distance, and charging time;
- runtime, iterations, accepted/rejected moves;
- exact-charging calls;
- BPC lower bound, incumbent, optimality gap, nodes, and generated columns.

### 3.3 Improvement criteria and expected failures

The combined method is considered valuable when:

- it stably produces solutions that pass the unified validator at every scale;
- it reaches or approaches the BPC proven optimum on small instances;
- it substantially raises the feasibility rate versus baselines that ignore charging
  decisions;
- it stays stable across multiple random seeds rather than showcasing a single best
  run.

Expected failures include:

- pure VRPTW routes produced by OR-Tools/GA may violate battery constraints;
- BPC returns `not_applicable` above 8 customers due to combinatorial growth;
- 100-customer instances can produce feasible solutions within 30 seconds, but this
  must not be claimed as near-global optimality.

## 4. Preliminary Result

The Week 5 batch experiments already provided checkable evidence for this week's
combined workflow. The data covers 2026-07-12 17:04:52 to 17:10:05 UTC, 120 records
in total.

| Algorithm | Runs | Feasible | Interpretation |
|---|---:|---:|---|
| ALNS_EXACT_CHARGING | 45 | 45 | All 15 scenarios pass; overall feasibility 100% |
| BRANCH_PRICE_AND_CUT | 15 | 6 | All 6 applicable small scenarios feasible and proven optimal; the other 9 explicitly not applicable |
| GA_VRPTW | 45 | 6 | Overall feasibility 13.3%; exact charging not integrated |
| OR_TOOLS_VRPTW | 15 | 0 | Every output identified as energy-invalid by the unified validator |

ALNS completed `9/9` feasible runs on each of the 5-, 10-, 15-, and 100-customer
scales of the Primary benchmark, and another `9/9` on the three Stress scenarios. In
the small-scale exact comparison, ALNS's best results on `c101C5`, `r105C5`, and
`rc105C5` all matched the BPC-proven optima.

These results support the following conclusions:

- The ALNS + exact-charging combination indeed solves the energy-feasibility problem
  exposed by the pure VRPTW baselines;
- The results cover 15 scenarios, 4 scales, and 3 random seeds — they do not rest on
  one or two easy examples;
- BPC's role is verifying small-scale quality, not being mis-extrapolated as a
  medium/large-scale solver;
- The 100-customer R/RC results still show clear cross-seed variance; search
  stability and solution quality should keep improving.

## 5. Evidence Index

- [Week 5 ALNS, exact charging, and BPC methodology](week05_alns_bpc_methodology.md)
- [Week 5 second-edition technical report](05_weekly_v2_alns_bpc_benchmark_rebuild.md)
- [120 per-run experiment records](../experiments/summaries/week05_advanced_per_run_results.csv)
- [Statistics aggregated by instance and algorithm](../experiments/summaries/week05_advanced_summary_results.csv)
- [Failure and not-applicable records](../experiments/summaries/week05_advanced_failure_cases.csv)
- [Schneider instance structural audits](../experiments/summaries/week05_advanced_instance_audits.csv)

## 6. Direction After Week 6

The project direction is now settled: keep ALNS + exact charging as the primary
method, BPC as the small-scale exact check, and evaluate feasibility, quality,
runtime, and stability through the unified validator and batch result tables. The
next step should prioritise improving the cross-seed stability of the 100-customer
R/RC instances and recording which destroy/repair operators work under different
instance characteristics. Only after accumulating stable, sufficient, and
clearly-defined decision data should bandit-style operator selection be
re-evaluated for implementation.
