# Week 4 Progress Log

### Week 4 — 2026-07-03

**Attended this week's meeting:** Not recorded in this repository.

**Progress this week**
- Completed the Week 4 extension work in the required order: first new
  experimental settings, then method improvement, then hybrid comparison.
- Added a Week 4 battery-capacity sweep over `60`, `80`, `100`, and `120` using
  the same generated Schneider-style instances, seeds, validator, and metrics
  as Week 3.
- Added `insert_anticipatory_charging_stations()` beside the existing Week 3
  late charging repair. The new repair inserts a reachable charging station
  before a customer becomes stranded without reachable depot or station access.
- Added a Week 4 experiment runner comparing pure VRPTW construction, late
  charging repair, and anticipatory charging repair for both OR-Tools and GA
  constructors.
- Ran the full Week 4 experiment and generated local outputs under
  `results/week04/`. Curated summary copies are available under
  `experiments/summaries/`.
- Read the supplied local PDF originals for Keskin and Catay (2016), Montoya et
  al. (2017), and Desaulniers et al. (2016). The reading notes are stored in
  `docs/week04_reading_notes.md`; no paper PDF is committed to Git.
- Wrote the Week 4 report in `docs/week04_extend_read_explore.md`.
- Added tests for anticipatory repair and the Week 4 runner.

**Challenges & blockers**
- The battery-capacity sweep shows that increasing battery capacity reduces
  energy violations, but pure VRPTW construction remains infeasible under EVRP-TW
  validation because it never reasons about charging reachability.
- The Week 3 late charging repair is too reactive. It often inserts stations
  only after the route has already passed the point where recovery is easy.
- Anticipatory repair solves all tested cases at battery capacities `80`, `100`,
  and `120`, but battery `60` remains difficult. This is not a coding accident;
  it shows that repair-only logic is insufficient when route geometry and
  charging-station reachability are too tight.
- The current model still assumes linear full recharge at stations. Montoya et
  al. (2017) makes clear that nonlinear charging can change feasibility and
  cost, so the current results should be interpreted as full-recharge,
  linear-charging experiments only.

**Next steps**
- Add route splitting or customer reassignment for cases where no charging
  station can make a route segment energy-feasible.
- Move energy reachability into route construction instead of relying only on
  post-processing.
- Keep partial recharge and nonlinear charging as later extensions after the
  full-recharge workflow is stable.
- Continue using the same result-table structure so future improvements remain
  comparable against Week 3 and Week 4.

**Hours spent (optional):** Not recorded.

**Links (optional):**
- [Week 4 reading notes](week04_reading_notes.md)
- [Week 4 technical report](week04_extend_read_explore.md)
- [Week 4 summary results](../experiments/summaries/week04_summary_results.csv)
- [Week 4 per-run results](../experiments/summaries/week04_per_run_results.csv)
- [Week 3 experimental report](week03_experiment_design_and_evaluation.md)
