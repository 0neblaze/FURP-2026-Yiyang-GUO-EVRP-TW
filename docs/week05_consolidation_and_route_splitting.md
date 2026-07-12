# Week 5: Low-Battery Infrastructure Augmentation

## Research Question

At battery capacity `60`, can deterministic charging-infrastructure augmentation
make every original customer energy-serviceable while preserving customers,
seeds, vehicle parameters, and the existing routing workflow?

## Original Low-Battery Control

The original Week 5 setting uses the Week 4 generated instances, three seeds,
and anticipatory charging plus route splitting. It is kept unchanged as a
failure control. A customer is structurally unreachable when:

```text
min_safe_start, safe_end [energy(safe_start, customer) + energy(customer, safe_end)] > 60
```

where a safe node is the depot or an existing charging station. Eight of nine
instances contain one or more such customers. Therefore the original setting
cannot meet an 80% feasibility target without changing infrastructure, battery
capacity, or the customer set.

## Infrastructure Augmentation Rule

For every structurally unreachable customer, the experiment adds one station
named `F_AUG_<customer>` at the midpoint between that customer and its nearest
original safe node. The new station has zero demand and service time, opens at
time zero, and remains available through the maximum instance due date.

This guarantees an energy-feasible local cycle:

```text
safe node -> midpoint station -> customer -> midpoint station -> safe node
```

The rule is deterministic and stored in a JSON manifest for every instance. It
is not a claim of globally minimum infrastructure. The original and augmented
conditions use the same OR-Tools and GA constructors followed by anticipatory
charging and route splitting.

## Controlled Experimental Design

| Fixed factor | Value |
|---|---|
| Customer scales | 50, 100, 200 |
| Random seeds | 2014, 2015, 2016 |
| Battery capacity | 60 |
| Vehicle and customer data | Unchanged from Week 4 |
| Routing methods | OR-Tools VRPTW and GA VRPTW |
| Post-processing | Anticipatory charging plus route splitting |
| Independent feasibility gate | `validate_routes()` |

Run the experiment with:

```bash
uv run python -m evrptw.experiments.week05_infrastructure_augmentation \
  --output-dir results/week05_infrastructure \
  --summary-dir experiments/summaries
```

The runner records `infrastructure_variant`, `added_station_count`, route data,
station manifests, all feasibility metrics, and an acceptance report. It raises
an error if any augmented run has a capacity, time-window, energy, or coverage
violation.

## Results

| Size | Method | Original feasible rate | Augmented feasible rate | Original avg. energy violations | Augmented avg. energy violations | Original avg. vehicles | Augmented avg. vehicles |
|---:|---|---:|---:|---:|---:|---:|---:|
| 50 | OR-Tools | 0.333 | 1.000 | 1.667 | 0.000 | 7.333 | 4.667 |
| 100 | OR-Tools | 0.000 | 1.000 | 2.333 | 0.000 | 11.000 | 8.000 |
| 200 | OR-Tools | 0.000 | 1.000 | 3.667 | 0.000 | 18.667 | 14.000 |
| 50 | GA | 0.333 | 1.000 | 2.000 | 0.000 | 46.000 | 46.000 |
| 100 | GA | 0.000 | 1.000 | 3.000 | 0.000 | 89.333 | 89.333 |
| 200 | GA | 0.000 | 1.000 | 7.000 | 0.000 | 186.667 | 186.667 |

The augmented scenario reaches `18/18` feasible, zero-violation runs. It adds
an average of `2`, `3`, and `7` stations at sizes `50`, `100`, and `200`.
OR-Tools improves both feasibility and average vehicle count. GA improves
feasibility and violations without increasing average vehicle count. Distances
and runtimes are reported in the cleaned summary only for feasible solutions;
they are not claimed to dominate invalid original routes.

## Failure Analysis and Interpretation

The original failure table remains in the generated output. For example,
customer `C85` in the 100-customer seed-2014 instance has no feasible
safe-node-to-customer-to-safe-node cycle under the original infrastructure and
a 60-unit battery. The augmented midpoint station repairs this infrastructure
gap without changing that customer's coordinates, demand, or time window.

This establishes a clear separation between two effects: route splitting can
improve compact routes, while infrastructure feasibility is necessary before any
routing method can reach full EVRP-TW feasibility. The next research step is to
reduce station additions through shared-station placement or an integrated
infrastructure-routing model.
