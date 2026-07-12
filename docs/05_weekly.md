# Week 5 Progress Log

### Week 5 — 2026-07-12

**Attended this week's meeting:** Not recorded in this repository.

**Progress this week**
- Preserved the original battery-`60` route-splitting experiment as a
  structural-infeasibility control rather than misreporting its `1/3` result as
  a successful final outcome.
- Diagnosed the original instances at the safe-node-to-customer-to-safe-node
  level. Eight of nine instances contain structurally unreachable customers
  under the fixed `60`-unit battery and original charging infrastructure.
- Added deterministic midpoint charging-station augmentation for each such
  customer, with a JSON manifest containing every new station and its anchor.
- Added a dual-scenario Week 5 runner that evaluates original and augmented
  infrastructure using the same customer data, seeds, vehicle parameters,
  constructors, anticipatory charging, and route splitting.
- Reached `18/18` feasible augmented runs with zero capacity, time-window,
  energy, and coverage violations. This is `3/3` for both OR-Tools and GA at
  all three scales.
- Added tests for midpoint augmentation determinism, energy-feasible station
  cycles, manifests, and the dual-scenario experiment runner.

**Challenges & blockers**
- The original low-battery infrastructure cannot support every generated
  customer, so route-only repair cannot honestly meet the feasibility target.
- The deterministic station rule guarantees feasibility but is not a global
  minimum-infrastructure solution; it may add more stations than necessary.
- Objective value and runtime must be interpreted among feasible solutions,
  rather than against invalid routes with artificially short distances.

**Next steps**
- Design a shared-station placement or set-cover heuristic to reduce the number
  of added stations while maintaining full feasibility.
- Integrate battery reachability into route construction and compare it with the
  augmentation baseline under the same controls.

**Hours spent (optional):** Not recorded.

**Links (optional):**
- [Week 5 checkpoint](week05_project_checkpoint.md)
- [Week 5 technical report](week05_consolidation_and_route_splitting.md)
- [Infrastructure summary results](../experiments/summaries/week05_infrastructure_summary_results.csv)
- [Infrastructure per-run results](../experiments/summaries/week05_infrastructure_per_run_results.csv)
- [Original low-battery summary](../experiments/summaries/week05_summary_results.csv)
