# Week 5 Project Checkpoint

## 1. Current Project Status

This project studies the Electric Vehicle Routing Problem with Time Windows and
Recharging Stations (E-VRPTW). The runnable workflow includes OR-Tools and
Genetic Algorithm (GA) VRPTW constructors, an independent EVRP-TW validator,
late and anticipatory charging repair, route splitting, controlled experiments,
and explicit failure analysis.

The Week 5 original `60`-unit battery experiment is retained as a structural
infeasibility control. Eight of its nine generated instances contain at least
one customer whose minimum safe-node-to-customer-to-safe-node energy cycle is
above `60`. This cannot be repaired by customer-boundary route splitting alone.

The Week 5 infrastructure-augmentation experiment keeps customer coordinates,
demands, time windows, seeds, battery capacity, vehicle parameters, and solver
settings fixed. It adds deterministic midpoint charging stations only for those
structurally unreachable customer cycles, then evaluates the existing
anticipatory-charging plus route-splitting workflow.

## 2. Evidence of Progress

All `18` augmented runs are feasible with zero capacity, time-window, energy,
and coverage violations. With three seeds per size, this is `3/3 = 100%` for
both constructors at every tested scale.

| Size | Constructor | Feasible runs | Avg. vehicles | Avg. added stations | Avg. runtime (s) | Avg. feasible objective |
|---:|---|---:|---:|---:|---:|---:|
| 50 | OR-Tools | 3/3 | 4.667 | 2.000 | 0.037 | 1102.789 |
| 100 | OR-Tools | 3/3 | 8.000 | 3.000 | 0.212 | 1782.520 |
| 200 | OR-Tools | 3/3 | 14.000 | 7.000 | 0.978 | 2656.192 |
| 50 | GA | 3/3 | 46.000 | 2.000 | 3.605 | 4515.957 |
| 100 | GA | 3/3 | 89.333 | 3.000 | 8.618 | 8429.093 |
| 200 | GA | 3/3 | 186.667 | 7.000 | 23.745 | 17333.915 |

For OR-Tools, average vehicle counts improve relative to the original
route-splitting control from `7.333/11.000/18.667` to `4.667/8.000/14.000` at
sizes `50/100/200`. GA does not increase its vehicle count and moves from
partial or zero feasibility to `100%` feasibility.

The reviewable results are:

- [`week05_infrastructure_summary_results.csv`](../experiments/summaries/week05_infrastructure_summary_results.csv)
- [`week05_infrastructure_per_run_results.csv`](../experiments/summaries/week05_infrastructure_per_run_results.csv)

## 3. Problems and Limitations

- Infrastructure augmentation is a new experimental condition, not a claim
  that the original charging-station layout was solved without modification.
- The rule adds one guaranteed midpoint station per structurally unreachable
  customer. It is deterministic and auditable, but not a globally minimum
  charging-infrastructure design.
- Objective value and runtime are reported only for feasible solutions. They
  should not be compared directly against a shorter but infeasible route.
- The model remains multiple/full recharge with linear charging. It does not
  implement partial recharge, nonlinear charging, or joint infrastructure-route
  optimization.

## 4. Next Step

1. Replace the one-customer-one-station guarantee with a shared-station or
   set-cover infrastructure design that reduces the number of new stations.
2. Add energy reachability to route construction, then compare its infrastructure
   requirements with the deterministic augmentation baseline.
