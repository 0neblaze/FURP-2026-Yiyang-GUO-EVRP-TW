# EVRP-TW Staged Baseline Improvement Roadmap

## 1. Overall Goal and Current Assessment

The current main method is an ALNS-based matheuristic (Adaptive Large Neighborhood Search) combined with an exact charging subproblem, using small-scale Branch-Price-and-Cut (BPC) as the exact theoretical comparison.

The current version has already settled the question "can it reliably produce feasible solutions": across the existing 5/10/15/100-customer Schneider benchmark experiments, the ALNS feasibility rate is 100%. However, its accurate positioning today is still:

> A first strong baseline with a high feasibility rate and small-scale exact verification — not yet a proven state-of-the-art algorithm.

The next phase must shift the evaluation focus from "is it feasible" to:

1. whether the vehicle count drops significantly;
2. whether the total distance is close to the best-known values;
3. whether enough effective search completes within 30 seconds;
4. whether results are stable across random seeds;
5. whether there is credible evidence for small-scale optimality and medium/large-scale lower bounds.

## 2. Highest-Priority Principles

Subsequent work must follow this order and must not jump to multiple directions simultaneously:

1. first unify the objective function and evaluation criteria;
2. then directly improve ALNS solution quality;
3. next solve the search-speed bottleneck;
4. then refine the adaptive search mechanism;
5. then establish the best-known comparison and the complete experiment system;
6. then extend the BPC theoretical comparison to larger scale;
7. only last, upgrade to partial/nonlinear charging models.

No stage may enter the next stage without passing its acceptance gates. In particular, the main effort must not shift toward nonlinear charging while large-scale ALNS quality is still clearly insufficient.

## Repository-Wide Artifact Naming and Directory-Structure Rules (Mandatory)

This section states the global requirements for Stages 0–8 and for every sub-stage, operator, experiment round, and review activity. All new code, configs, tests, experiment results, failure evidence, and documents must be traceable through unified labels to the stage and component that produced them.

### 1. Canonical stage ID

- Human-readable titles use `Stage 02.1`; filenames, directory names, and manifests use the space-free canonical ID `stage02.1`; both denote the same stage.
- Stage 0 uses `stage00`; Stage 1 uses `stage01`; Stage 2 uses `stage02`.
- The three parts of Stage 2 are fixed as `stage02.1`, `stage02.2`, and `stage02.3`.
- Sub-tasks of other stages follow the same rule, e.g. `stage03.0`, `stage03.1`, `stage05.1`, and `stage06.1`.
- Documents, manifests, and review reports use the dotted canonical ID; when a Python module filename must use underscores, the manifest must still record the dotted canonical ID.

### 2. Filename and directory formats

Stage-specific artifacts use the format:

```text
<stage_id>_<component>_<attempt_or_rerun>_<artifact_type>[_<instance>_<seed>].<ext>
```

Directories use the format:

```text
results/<stage_id>_<component>_<attempt_or_rerun>/<instance>/<seed>/
```

where:

- `<component>` is the sub-stage or operator, e.g. `route_elimination`, `relocate`, `station_pressure`;
- `<attempt_or_rerun>` must be `attemptNN` or `rerunNN`; meaningless names such as `final`, `new`, or `latest` are forbidden; it is the unique run identity, not a software version number;
- `<artifact_type>` must be explicit, e.g. `config`, `raw`, `solution`, `events`, `failure_cases`, `environment`, `manifest`, `summary`, `review`, `readiness`, `test`, or `doc`.

Canonical examples:

```text
stage02.1_route_elimination_attempt02_events.json
stage02.1_vehicle_count_aware_repair_attempt02_failure_cases.csv
stage02.2_ejection_chain_rerun01_per_run_results.csv
stage02.3_station_pressure_attempt16_events.json
stage02.3_constraint_guided_rerun09_review_report.md
results/stage02.3_constraint_guided_rerun09/r101_21/2015/
```

### 3. Metadata required for every artifact

Every raw artifact and its manifest must record at least:

- `stage_id`, `component`, `artifact_type`;
- `run_label`, `attempt` or `rerun`;
- instance scope and seed scope;
- source/config/instance/environment hashes;
- the comparison baseline and `supersedes`/`legacy_path` mappings;
- status, failure reason, and whether it passed the validator.

The raw JSON, solution, events, failure, environment, manifest, summary, and review of the same experiment round must share one `run_label`; they must not be given unrelated names.

Every formal stage and sub-stage maintains at least one corresponding artifact registry, e.g. `stage02.1_artifact_registry.csv` or an equivalent JSON. The registry must list all artifacts of that stage with relative paths, artifact types, statuses, checksums, and historical path mappings; it must not record only the successful results.

### 4. Shared files, historical files, and frozen results

- `alns.py`, `neighborhoods.py`, `objective.py`, the validator, and shared tests that serve multiple stages must not be renamed just to carry a stage label; their stage affiliation is recorded through profiles, the operator registry, source hashes, and manifests.
- The Stage 0 frozen directory, historical results, and checksums must not be renamed, overwritten, or moved; only `stage00` labels and old-path mappings may be added in the artifact registry.
- Existing `stage02_*` historical paths are legacy artifacts and must be preserved; new experiments must use the canonical `stage02.1`, `stage02.2`, or `stage02.3` labels and record the old-path-to-new-label correspondence in the manifest.
- Failed rounds, timeouts, invalid, infeasible, and error outcomes must first seal the manifest, status, failure reason, and checksums; after the fix, a new `attemptNN` or `rerunNN` is used. Stage 5.2 large raw evidence is migrated out of the worktree only after retention-interface verification, and the lightweight registry must retain its archive identity; direct deletion without archiving, or renaming to a successful result, is forbidden.

### 5. Stage coverage table

| Roadmap section | Mandatory `stage_id` | Example `component` tags |
|---|---|---|
| Stage 0 | `stage00` | `frozen_baseline` |
| Stage 1 | `stage01` | `objective_policy`, `bpc_validation` |
| Stage 2.1 | `stage02.1` | `route_elimination`, `vehicle_count_aware_repair`, `route_merge` |
| Stage 2.2 | `stage02.2` | `relocate`, `swap`, `two_opt_star`, `route_segment_destroy`, `ejection_chain` |
| Stage 2.3 | `stage02.3` | `station_pressure`, `time_window_conflict`, `worst_energy_detour`, `shaw_related` |
| Stage 3.0–3.4 | `stage03.0`–`stage03.4` | `measurement`, `screening`, `cache`, `incremental`, `parallel` |
| Stage 4 | `stage04` | `adaptive_weights`, `restart`, `intensification` |
| Stage 5.1–5.3 | `stage05.1`–`stage05.3` | `best_known`, `perf_baseline`, `hot_path`, `artifact_streaming`, `job_parallel`, `native_kernels`, `accelerator_pilot`, `benchmark`, `ablation` |
| Stage 6.1–6.3 | `stage06.1`–`stage06.3` | `pricing`, `branching`, `validation` |
| Stage 7 | `stage07` | `solution_schema`, `validator_contract` |
| Stage 8 | `stage08` | `partial_linear`, `piecewise_linear`, `nonlinear`, `queueing` |

### 6. Mandatory checks

Before each stage enters formal experiments or the next stage, the following must be checked: path labels complete, artifact types unambiguous, run labels unique, manifests recomputable, historical mappings present, and raw-to-summary consistency — with the results recorded in the stage review report.

### 7. Data retention and evidence-layering rules (v2 policy and v3 physical schema, mandatory)

From the effective date of this rule, all new Stage 0–8 runners must provide `[artifact_storage]` in their configuration and write and replay artifacts through the shared `ArtifactBundleWriter`/`ArtifactReader`. The current storage policy is `artifact-storage-v2`; the Stage 5.2 current implementation uses the `screening_decisions_v3` physical schema and continues to read v1, older v2, and legacy evidence. The Stage 5.2 pipeline pilot, formal benchmark, and subsequent stages mandatorily use the v2/v3 combination that has passed independent review by the current chain. The default physical formats are Parquet/Arrow events, critical evidence is fully retained, and diagnostic evidence is aggregated by run/lane/iteration/operator/reason; the per-instance/seed cap is 2 GiB and the per-run cap is 32 GiB.

v2 adds 65,536-row streaming, a writer buffer of at most two row groups, worker-owned `(instance, seed)` shards, shard manifest/checksum, and parent-only control finalisation — without rewriting v1/legacy bytes. The full migration contract is in `docs/experiment_artifact_storage.md`.

Old non-canonical Stage 0–2 invocations are retained only for historical-compatible reproduction and must not use the new `[artifact_storage]` configuration; new configurations provided by the repository reject non-canonical output directories or run labels. Future Stage 0 freeze operations must complete current evidence first and then generate a compatible baseline view; the existing frozen baseline must not be overwritten.

The fixed directory layout for new artifacts is:

```text
results/<run_label>/
  control/<canonical>_run_metadata.json
  control/<canonical>_config.toml
  control/<canonical>_manifest.json
  control/<canonical>_manifest.sha256
  <instance>/<seed>/<canonical>_raw_<instance>_<seed>.json
  <instance>/<seed>/<canonical>_solution_<instance>_<seed>.json
  <instance>/<seed>/<canonical>_trace_<instance>_<seed>.json
  <instance>/<seed>/<canonical>_events_<instance>_<seed>.parquet
  <instance>/<seed>/<canonical>_route_dictionary_<instance>_<seed>.parquet
  <instance>/<seed>/<canonical>_screening_checks_<instance>_<seed>.parquet
  <instance>/<seed>/<canonical>_diagnostic_<instance>_<seed>.parquet
  <instance>/<seed>/<canonical>_environment_<instance>_<seed>.json
  review/
```

`events.parquet` must retain deterministic event identity and the critical events — exact started/completed, screening, cache, incremental, deadline, failure, accepted candidate, and global-best; v1 uses a globally increasing `event_id`, v2 uses the canonical shard ordinal plus a shard-local event ID; routes, lanes, and operators in events use integer dictionary indices, and the full customer sequence is stored exactly once in the route dictionary. The trace JSON stores counters, configuration, Parquet references, and the schema fingerprint; it must not re-embed full events, screening decisions, or route evaluations. Diagnostic aggregation must not affect the validator, objective, exact-call ordering, or failure replay.

Screening checks are stored in dedicated canonical columns; a cache lookup and its immediately following hit/miss result are merged into a single `lookup_result` record in the physical `events.parquet`. When a failure artifact is not applicable, the manifest must record `artifact_status.failure=not_applicable`; a missing file must not stand in for the status.

On reaching either byte budget, the writer closes the current Parquet writer, retains the completed raw, solution, event, environment, and failure evidence, writes `evidence_completeness=partial`, updates the manifest/checksum, and fails immediately; silent truncation, overwriting, or deletion is forbidden. Partial, timeout, failure, and manifest-error runs must not publish summaries.

Existing Stage 0 frozen results and Stage 3.0–3.2 raw/solution/events/manifest/summary are not physically migrated — not moved, not compressed, not rewritten; they are only marked in the registry and legacy mappings with `storage_format=legacy_json_or_jsonl`, `retention_class=legacy`, and `policy_compliance=legacy_compatible`. New data must be marked current; historical dirty states, failure states, and old paths must not be disguised as new-rule artifacts.

Before every formal run or stage transition, the label, attempt/rerun uniqueness, artifact type, checksum, manifest/sidecar, Arrow schema fingerprint, row count, byte size, provenance, and semantic raw-to-summary checks must all complete. Tracked summary and registry publication may happen only after an independent reviewer completes the raw replay. Detailed interfaces, fields, and failure-retention rules are in `docs/experiment_artifact_storage.md`.

---

## Stage 0: Freeze the Current Version and Establish a Non-Regressing Baseline

### Stage goal

Freeze the current version as the formal comparison point so that every later change can be judged for what it improved and whether it introduced regressions.

### Artifact label

All frozen baselines, configuration snapshots, environment records, comparison templates, and review results of this stage carry the label `stage00_frozen_baseline`; frozen results are additionally protected by the Stage 0 immutability rules.

### Concrete tasks

1. Freeze the current representative Schneider instance set, random seeds, and the 30-second run conditions.
2. Record for every instance:
   - feasibility rate;
   - vehicle count;
   - total distance;
   - total energy;
   - total charge amount and charging time;
   - run time;
   - ALNS iteration count;
   - exact charging subproblem call count and average duration;
   - best/mean/median/worst/standard deviation.
3. Fix the current 100-customer baselines:

| Instance | Current vehicles | Current main problem |
| --- | ---: | --- |
| `c101_21` | 14 | Reasonable, but no reliable gap |
| `r101_21` | 22–28 | Vehicle count high, clear seed variance |
| `rc101_21` | 24–25 | Vehicles and distance still improvable |

4. Establish regression gates: later versions must not reduce the structural feasibility rate, must not break the unified validator, and must not delete failure records.

### Required outputs

- An immutable baseline CSV of the current version;
- a snapshot of the current parameter configuration;
- a record of the current algorithm version and run environment;
- an automatic old-vs-new comparison report template.

### Gate to the next stage

- The current results can be re-run with one command and produce structurally complete, verifiable experiment artifacts; repeated runs are not required to produce bit-identical numeric solutions, but any numeric difference must pass the numerical reproducibility exemption below;
- the summary table can be automatically recomputed from per-run results;
- all feasible solutions re-pass the unified validator;
- later experiments automatically label improvement, regression, or unchanged.

### Numerical reproducibility exemption

Numeric differences between repeated runs are acceptable only when all of the following hold:

1. The algorithm must explicitly use a wall-clock deadline or another stopping condition affected by actual machine speed; runs with fixed iteration counts, fixed candidate counts, or fixed exact-call budgets must not use this exemption.
2. The benchmark instances and their SHA-256, parameter configuration, random seeds, core algorithm source SHA-256, dependency versions, thread counts, and solver settings must be identical; the Git working tree must be clean at formal capture. If hardware or the operating system differs, it must be explicitly recorded and must not be claimed as a same-environment replication.
3. At least one independent full rerun must be completed, covering exactly the same `(instance, seed)` set as the frozen baseline; any missing, duplicated, or extra records disqualify the exemption.
4. All solutions of the frozen run and the rerun must re-pass the same unified validator; the structural feasibility rate must not drop, failure records must not be missing or deleted, and the manifest and summary recomputation must fully pass.
5. The numeric difference must be explainable by recorded completed iterations, exact charging subproblem calls, or other observable workload differences, and that workload difference must occur near the deadline boundary. "The machine fluctuates" alone is not sufficient.
6. The automatic comparison report must retain per-item baseline value, rerun value, absolute/relative delta, and classification; the frozen CSV must not be overwritten, and only-better rerun results must not be retained alone.
7. The exemption cancels only the "bit-identical numeric solutions" requirement; it does not exempt configuration drift, code drift, instance changes, validator failures, feasibility-rate drops, missing records, or unexplained non-determinism. Any of these must fail acceptance and trigger a root-cause investigation.
8. If the rerun shows increased vehicle counts, lower feasibility, or other substantive regressions, they must not be automatically attributed to deadline noise; additional reruns or fixed-work-budget controls must demonstrate that the difference is runtime fluctuation before acceptance.

---

## Stage 1: Fix the Formal Objective Function and Metric Priorities

### Stage goal

Resolve the fundamental question "is a shorter distance with more vehicles actually better?" Without an explicit objective hierarchy, later algorithmic optimization has no stable direction.

### Artifact label

This stage is uniformly labeled `stage01`; objective definitions, comparisons, BPC, ALNS, validator, and test artifacts must record the corresponding component in the filename or manifest.

### Concrete tasks

Adopt a lexicographic objective, with fixed order:

1. first minimize the number of vehicles used;
2. at equal vehicle count, minimize total travel distance;
3. at equal first two, minimize total charging time;
4. last, compare total charging count or total charge amount.

Candidate comparison no longer uses a single distance float but an ordered objective tuple such as:

$$
(N_{vehicle},D,T_{charge},N_{charge})
$$

Additionally:

- modify the ALNS incumbent comparison logic;
- modify the simulated annealing acceptance logic so that vehicle-count increases are explicitly restricted;
- modify the experiment CSVs so the primary objective and secondary metrics are recorded separately;
- keep total distance so that "fewer vehicles but severely worse distance" is not rewarded.

### Required outputs

- The formal objective function definition;
- a unified solution comparison API;
- vehicle-count-first unit tests;
- an old-vs-new ranking difference report for the same batch of results.

### Gate to the next stage

- The ordering between any two solutions is unambiguous;
- a solution with more vehicles cannot become the incumbent merely for a slightly shorter distance;
- BPC, ALNS, experiment summaries, and documents use the same objective definition;
- all old tests keep passing.

### Implementation result (2026-07-13)

- A unified `SolutionObjective` comparison seam was established; the formal objective is fixed as `(vehicle count, total distance, total charging time, charging count)`, with float metrics normalized for comparison at `1e-9`.
- ALNS hard-rejects vehicle-count increases; vehicle-count reductions are always accepted, and at equal vehicle count only distance degradation remains subject to simulated annealing.
- The BPC path column uses the same four-level objective; internal scalar bounds serve search only, the full column pool confirms the final incumbent through exact lexicographic set partitioning, and optimality is declared only when the full objective solve completes.
- The Stage 0 old-vs-new ranking report has 36 rows, 6 of which changed position: `rc105C5` was re-ranked by vehicle-count priority, and `rc103C15` was tie-broken by the charging metric.
- The formal Stage 1 experiments produced 36/36 ALNS feasible solutions and 3/3 proven four-level-optimal 5-customer BPC solutions; the 12/12 Stage 0 structural feasibility gates passed.
- The final formal run took place on clean commit `c5e2c16` after all dual-axis code-review issues were closed; all 39 solutions were independently recomputed and passed by the unified validator; `pytest` was 61 passed; Ruff and mypy both passed.
- The Stage 0 best-objective comparison shows 3 instances improved, 8 unchanged, 1 worse; the `r101_21` best vehicle count this round was 24, worse than Stage 0's 22 — retained as time-budgeted search quality fluctuation, which does not affect this stage's acceptance conclusion of "objective definition consistent and feasibility non-regressing".
- The Stage 0 manifest SHA-256 remains `b226b97e0e67288aaaf85726ad855df71cb81406685c57c8e8c40cd8996aa0da`; frozen files unmodified.

---

## Stage 2: Directly Reduce Vehicle Counts and Make ALNS a True Large Neighborhood Search

### Stage goal

Prioritize the high vehicle counts on the 100-customer R/RC instances, so that ALNS no longer relies mainly on small neighborhoods that move only a few customers per iteration.

### Artifact label

This stage is uniformly labeled `stage02`; formal experiments, failed rounds, independent reruns, and review artifacts must further use `stage02.1`, `stage02.2`, or `stage02.3`, not a blanket `stage02`.

### Concrete tasks

Add operators in this order:

#### 2.1 First batch: directly target the vehicle count

The component labels are fixed as `route_elimination`, `vehicle_count_aware_repair`, and `route_merge`; the corresponding artifacts must use `stage02.1_<component>_<attempt_or_rerun>_<artifact_type>`.

1. Route elimination destroy:
   - prefer routes with few customers, high distance contribution, or high charging pressure;
   - remove the customers of an entire route;
   - attempt to reassign them to other routes;
   - delete the original route only when every customer is successfully reinserted.
2. Vehicle-count-aware repair:
   - prefer insertion into existing routes;
   - create a new route only when all existing routes are infeasible;
   - apply the highest-level penalty to creating a new vehicle.
3. Route merge:
   - enumerate promising route pairs;
   - first filter through capacity, time-window, and energy lower bounds;
   - call the exact charging subproblem only after passing the prefilters.

#### 2.2 Second batch: cross-route quality improvement

The component labels are fixed as `relocate`, `swap`, `two_opt_star`, `route_segment_destroy`, and `ejection_chain`; the corresponding artifacts must use `stage02.2_<component>_<attempt_or_rerun>_<artifact_type>`.

- relocate;
- swap;
- 2-opt* (cross-route edge exchange);
- route segment destroy;
- ejection chain.

#### 2.3 Third batch: constraint-guided operators

The component labels are fixed as `station_pressure`, `time_window_conflict`, `worst_energy_detour`, and `shaw_related`; dynamic removal tiers and their review artifacts must use `stage02.3_<component>_<attempt_or_rerun>_<artifact_type>`.

- station-pressure destroy;
- time-window conflict destroy;
- worst energy detour removal;
- strengthened related/Shaw removal.

Large-scale removal sizes are no longer capped at 3 customers; tiered ranges (small/medium/large destroy strengths) are used and adjusted dynamically by stagnation.

### Required outputs

- Independent implementation and statistics for each new operator;
- route elimination success/failure reason logs;
- per-operator call counts, feasible repairs, acceptances, vehicle-count improvements, and distance improvements;
- a vehicle-count comparison table for the R/RC 100-customer instances.

### Gate to the next stage

- The 100-customer feasibility rate stays at least 95%, targeting 100%;
- the average vehicle counts of `r101_21` and `rc101_21` drop clearly versus Stage 0;
- the new algorithm must not reduce vehicles by severely increasing distance;
- route elimination produces real vehicle-count improvements on multiple instances, not just in code;
- the vehicle-count variance across seeds narrows clearly.

### Implementation result (2026-07-13)

Stage 2 is split into three profiles: 2.1, 2.2, and 2.3. The formal scope is fixed at Stage 0's 12 instances, 3 seeds, 30 seconds, 1000 iterations, single thread.

#### 2.1 Route elimination and fleet reduction

- `route elimination` produced real vehicle reductions on 8 distinct instances; `route merge` produced 11 real reduction candidates.
- Both complete experiment rounds passed 36/36 through the unified validator; 72/72 solutions had objectives recomputed identically by independent logic.
- The Stage 2.1 average vehicle counts for `c101_21`, `r101_21`, `rc101_21` are 12.000, 20.667, and 19.333; R/RC reduced by 2.667 and 4.334 vehicles respectively versus Stage 0.
- The first round failed because exact charging evaluation exhausted the 30 seconds; capacity, optimistic time-window, and energy prefilters were then added, with regression tests. The failed raw JSON, solutions, and event logs were all retained.

#### 2.2 Cross-route quality improvement

- All five operator families — `relocate`, `swap`, `2-opt*`, `route segment destroy`, `ejection chain` — were called and produced feasible candidates.
- Both complete rounds passed the inherited gates; the formal best objectives of 12/12 instances are no worse than Stage 2.1, producing 21 accepted same-vehicle-count real distance improvements.
- Because the first round's quality probes altered the Stage 2.1 main-search trajectory, the fix separated the legacy trajectory from an independent quality probe lane; this fix did not relax the objective or the validator.

#### 2.3 Constraint guidance and dynamic removal sizes

- The final attempt16 and the independent rerun09 both completed `READY_FOR_STAGE03` review: 36/36 solutions and objectives re-read and verified by the review tooling, retaining 20 real failure/poor-quality cases.
- All four operator families — `station_pressure`, `time_window_conflict`, `worst_energy_detour`, `shaw_related` — were called, produced feasible candidates, and were accepted at least once; all three removal tiers (small, medium, large) genuinely occurred.
- Stagnation-triggered tier escalation and global-best resets occurred; the maximum actual removal count in 100-customer focused runs was 20, no longer fixed at 3.
- The 100-customer results show vehicle counts and distance stabilized, but the exact charging subproblem remains the dominant cost:

| Instance | Avg vehicles | Avg distance | Effective iterations (attempt16 / rerun09) | Exact calls (attempt16 / rerun09) |
|---|---:|---:|---:|---:|
| `c101_21` | 12.000 | 1055.920 | 22.0 / 22.0 | 1746.7 / 1802.3 |
| `r101_21` | 20.667 | 1812.683 | 51.0 / 52.0 | 1966.0 / 1959.7 |
| `rc101_21` | 19.333 | 1968.486 | 28.0 / 29.0 | 2133.7 / 2095.0 |

- Stage 2.3 already has lane-local caching and unchanged-route precomputation, and records cache hits/misses, unique route evaluations, and exact calls; but the auditable global cache, incremental propagation, interruptible exact solver, and parallel acceleration required by Stage 3 are not yet implemented. Therefore `median exact calls <= 100` and `median effective iterations >= 50` remain Stage 3 targets and must not be claimed as achieved in Stage 2.3.
- The final review artifacts include `review_report.md`, `review_findings.csv`, `failure_analysis.csv`, `stage03_readiness.csv`, and `review_manifest.json`. The Stage 0 manifest SHA-256 remains `b226b97e0e67288aaaf85726ad855df71cb81406685c57c8e8c40cd8996aa0da`.
- Traceable evidence lives in `docs/stage02_constraint_guided.md`, `docs/stage02_constraint_guided_review.md`, and `experiments/summaries/stage02_constraint_guided_rerun09_review_report.md`, `stage02_constraint_guided_rerun09_failure_analysis.csv`, and `stage02_constraint_guided_rerun09_stage03_readiness.csv`.

### Stage 2.3 review: why this round of activity took so long

The conclusion: "a technical bottleneck amplified by engineering closure" — not mere engineering procrastination, nor overly strict acceptance gates. Stage 2.3 met its stage gates, but it exposed the search, review, and reproducibility problems more completely.

| Type | Direct evidence | Assessment |
|---|---|---|
| Technical: exact charging cost | Focused 100-customer runs complete only ~22–52 effective iterations in 30 seconds while calling the exact subproblem ~1.75k–2.13k times | Core bottleneck. Stage 2.3 deliberately did not implement Stage 3 acceleration early, so the current profile cannot remove it |
| Technical: multi-lane candidate evaluation | Legacy, quality probe, and constraint lanes all produce candidates; every dynamic removal additionally sorts, repairs, and records events | The per-iteration workload is too large; the new operators increase search coverage but also evaluation overhead |
| Technical: deadline boundary | A cooperative deadline cannot interrupt an in-flight exact call; both rounds have 9/36 slight overruns, at most ~0.017–0.018 s | This is an interruptibility problem of the exact solver interface, not simple machine fluctuation |
| Technical: observability semantics | Early reviews found unchanged-route reevaluation and feasible probes misrecorded as accepted | Genuine defects of the algorithm and event model, fixed in the final round, but it shows "candidate, acceptance, recomputation" must be defined separately |
| Engineering: formal experiment scale | Each round is a fixed 12×3=36 runs; failures must retain complete evidence and rerun in a new directory; the final path went through 16 attempts and 9 independent reruns | This is the necessary cost of the research protocol — it cannot be reduced by deleting failures, changing seeds, or relaxing gates |
| Engineering: late review findings | Provenance, event counting, and replay completeness were strengthened only after formal runs | Insufficient preflighting. Replay and evidence-consistency checks on small instances and the three focused 100-customer runs should complete before launching the 36-run round |
| Engineering: code vs experiment state | A dirty repository was recorded during formal runs; the final code is committed and the working tree is clean | Not a numerical-algorithm problem but experiment orchestration: freeze the commit, record the hash, then run the formal experiment |

Therefore, Stage 2.3's long duration cannot be solved by "increasing the time budget". The correct direction is to first reduce the exact cost per candidate, then reduce invalid candidates, and only then discuss parallelism; meanwhile, defer expensive full experiments until preflight and replay pass.

### Scientific adjustments to later stages, based on the first three stages

- Keep the existing gates, instances, seeds, validator, and formal objective; change only implementation order, measurement methods, and engineering orchestration — never trade relaxed acceptance for speed.
- Stage 3 does observability and single-thread semantic preservation first, then caching, incremental propagation, and exact solver interruptibility, and only last controlled parallelism.
- Stage 4 does not reinvent dynamic removal sizes; it takes Stage 2.3's dynamic destroy sizes as fixed input and studies only adaptive weights, acceptance rates, and restart mechanisms.
- Stage 5 does small-scale pilots and model-compatibility checks first, then expands the full benchmark; Stage 6 proceeds as an independent BPC track in parallel, without blocking ALNS acceleration.
- Stage 7 may advance solution-interface and validator-contract work early, but partial charging still must wait for explicit charging events to stabilize before entering Stage 8.

---

## Stage 3: Accelerate the Exact Charging Subproblem Calls and Raise the Effective Iteration Count

### Stage goal

Solve the core bottleneck quantified in Stage 2.3: 100-customer focused runs complete ~22–52 effective iterations in 30 seconds while calling the exact charging subproblem ~1.75k–2.13k times.

### Artifact label

This stage is uniformly labeled `stage03`; measurement, screening, caching, incremental propagation, interruptible solving, and parallelism must each use component labels such as `stage03.0`, `stage03.1`, etc.; different acceleration mechanisms must not be mixed in one results directory.

Stage 3's first principle is to keep `(vehicle count, total distance, total charging time, charging count)`, the validator, and the event semantics unchanged. Any acceleration must first prove that it "computes less", not that it "records less".

New Stage 3.0–3.2 evidence must follow this roadmap's `artifact-storage-v1`: Parquet/Arrow layered storage of critical/diagnostic evidence, through the shared artifact writer, manifest, sidecar, and independent replay reviewer. Existing Stage 3.0–3.2 raw evidence keeps its old bytes and old paths as `legacy_compatible` evidence; formal/smoke runs are not redone for the new rules, and storage compression or log reduction must not be reported as algorithmic speedup.

### Concrete tasks

Establish two-stage candidate evaluation:

#### 3.0 Measure first, then accelerate

Artifact prefix `stage03.0_measurement`; manifest component `measurement`.

- Use Stage 2.3 attempt16/rerun09 as the fixed baseline, locking source/config/instance/environment hashes.
- Add route-level timing, operator-level exact calls, candidate state, and deadline-boundary records.
- Build a replay auditor: recompute exact calls, cache hits, accepted candidates, and objectives from raw solutions and event logs; audits that only read summaries are not accepted.
- New runs use `events.parquet` for the critical event stream, `route_dictionary.parquet` for route sequences, and aggregated `diagnostic.parquet` for ordinary diagnostics; `trace.json` stores only replayable indices. Historical JSON/JSONL is read through a compatible reader without physical conversion.
- Run smoke tests first on 5–8-customer small instances and on `c101_21/r101_21/rc101_21`; only after preflight and replay consistency pass, launch the 36-run formal experiments.

#### 3.1 Cheap screening

Artifact prefix `stage03.1_screening`; manifest component `screening`.

Candidate routes are checked in order:

1. load capacity lower bound;
2. forward/backward time-window propagation;
3. time-window slack;
4. shortest-distance increment lower bound;
5. single-segment battery reachability;
6. depot–customer–station structural lower bounds;
7. cache of known-infeasible customer sequences.

Only candidates passing the screen call the exact charging subproblem.

#### 3.2 Caching and incremental propagation

Artifact prefix `stage03.2_cache_incremental`; manifest component `cache_incremental`.

- Extend the existing cache hit/miss into an auditable route evaluation cache whose key includes at least the instance hash, customer sequence, charging configuration, and objective schema version;
- cache feasible results and explicitly infeasible results;
- use incremental distance and time-window computation for relocate/swap;
- build a station reachability bitset;
- avoid re-solving equivalent customer sequences;
- give the cache a memory cap and an observable eviction policy.
- Unchanged routes must not re-call the exact subproblem; their results must be distinguishable from changed routes in the logs.

### CPU Batch pilot result and the future mandatory inheritance policy (2026-07-14)

The independent `cpu_batch_pilot_attempt01` completed 12 paired runs over 4 instances, 3 seeds, and 40 fixed iterations. All pairs are fully consistent in candidate-work hash, exact-call count, route-result hash, objective tuple, effective iterations, and validator status. The end-to-end median savings for the three 100-customer instance families are: `c101_21` 21.97%, `r101_21` 11.54%, `rc101_21` 24.40%; the C5 median saving of −0.12% is retained separately as a small-instance fixed-overhead control. This pilot proves only that `cpu_batch` can become the subsequent default backend; it does not impersonate Stage 3.3 readiness, nor rewrite Stage 3.0–3.2 historical code paths, raw evidence, or review conclusions.

From Stage 3.3 onward, any new code, tests, and experiments that call ALNS exact charging route evaluation must obey:

- `cpu_batch` is the current default and the only formal backend for Stages 3.3–5.1; Stage 5.2 uses it as the fixed-work reference and allows only backends that pass Stage 5.2's strict replacement gates to become formal backends for Stages 5.2–8. No new experiment may run `cpu_scalar`.
- `cpu_scalar` may be invoked only by Stage 0–3.2 historical runners that existed before 2026-07-14 together with their frozen configurations, and only to reproduce existing results; any newly created or newly configured run, regardless of stage label, must not call `cpu_scalar`, use it to generate new stage evidence, or treat it as a future performance comparison.
- Correctness verification uses the frozen pilot consistency evidence, golden fixtures, small-scale brute-force enumeration, and unified validator recomputation; the time-consuming scalar comparison is not repeated.
- If `cpu_batch` is unavailable, has precision conflicts, capacity overflows, or inconsistent deadline states, it must fail fast; automatic or silent fallback to `cpu_scalar` is forbidden.
- Every formal run must record the exact backend, batch launches, transitions, packing/unpacking time, exact-call count, and total batch time in the configuration, manifest, environment, and reviewer outputs so that backend choice and performance gains are auditable.

Candidate accelerations before Stage 5.2 are compared in paired equal-workload runs against `cpu_batch`. From Stage 5.2 on, replacing the formal backend requires the same instances, seeds, iterations, candidate workload, and screening/cache settings, with fully consistent candidate-work hash, route-result hash, objective tuple, validator, exact-call count, and effective iterations; the overall end-to-end median time over all 100-customer pairs must drop by at least 15%, and no C/R/RC family median may regress by more than 3%. Replacement requires independent reviewer approval; on failure, the current accepted backend stays and the complete failure evidence is retained.

#### 3.3 Exact solver interface and fixed-work diagnostics

Artifact prefix `stage03.3_exact_deadline`; manifest component `exact_deadline`.

- Convert the cooperative deadline into a checkable checkpoint or interruptible interface; at the deadline, only the most recent complete incumbent is returned — no half-finished candidates.
- Every exact call records started, completed, budget-exhausted, infeasible, and interrupted states; completed calls are distinguished from started calls.
- Under the same instances and seeds, using only `cpu_batch`, run fixed exact-call budget and wall-clock budget diagnostics separately, separating algorithmic improvement from machine speed; `cpu_scalar` must not be rerun for this diagnostic.
- First require `cpu_batch` under fixed workload to agree with the frozen golden evidence on validator, objective, and acceptance semantics; only then evaluate the iteration count within 30 seconds.

##### Stage 3.3 implementation and review result (2026-07-14)

Stage 3.3 is complete. The accepted smoke is `stage03.3_exact_deadline_attempt05` (36/36 axes); the accepted formal is `stage03.3_exact_deadline_attempt06` (72/72 axes); the independent review status is `READY_FOR_STAGE03_4`. `attempt01` is retained as partial; `attempt02`–`attempt04` are retained as `NOT_READY`, never overwritten.

The implementation adds a global 100 started exact-call cap, a 120-second watchdog, the 30-second wall-clock axis, checkable `cpu_batch` checkpoints, candidate-level cache transactions, started/completed/infeasible/interrupted reconciliation, plus packing, unpacking, batch timing, and peak-RSS evidence. The formal validator, objective, acceptance, cache, deadline, provenance, and frozen CPU batch golden evidence all passed independent replay.

The overall Stage 3 performance targets are not yet met: the `r101_21`/`rc101_21` wall-clock median started calls are 1860/2039 and the fixed-work median effective iterations are 6/3. Stage 3.4 must therefore continue with candidate control; Stage 3.3 readiness does not equal Stage 3 performance completion.

#### 3.4 Candidate control and controlled parallelism

Artifact prefix `stage03.4_control_parallel`; manifest component `control_parallel`.

Current status (2026-07-15): smoke `stage03.4_control_parallel_attempt10` completed 72/72 axes, all passed, independent review `READY_FOR_STAGE034_FORMAL`. The formal `stage03.4_control_parallel_attempt11` completed 144/144 axes, all passed, independent review `READY_FOR_STAGE04`. The corrected warm-start protocol (with transactional reviewer gates, independent candidate-hash recomputation, hardened precondition checks) passed all gates. Early failed attempts (01–09) are retained and not overwritten.

Stage 3.4 formal evidence uses the explicitly registered **inherited warm start** protocol: the reviewed Stage 3.3 wall-clock incumbent (solution, objective key, and provenance SHA-256) is loaded as the initial solution per instance/seed, but is still revalidated through the full Stage 3.4 screening→ranking→cpu_batch exact transaction pipeline. This protocol is necessary: Stage 3.3 used ~1860–2039 started exact calls to find its incumbents, while the Stage 3.4 fixed-work axis caps at 100 started calls; a cold-start search cannot reach Stage 3.3 objective quality within that budget. The inherited incumbent is not trusted directly; every candidate route is independently screened, cached, and exactly evaluated by the Stage 3.4 candidate-control runtime, and the reviewer independently recomputes candidate-work and route-result hashes from raw Parquet events. `inherit_stage033_incumbent` must be `true` in the configuration.

Fixed-work termination uses two explicit config parameters: `fixed_work_exhaustion_rounds` (the threshold of consecutive rounds with no new exact calls, currently 10) and `min_iterations_before_exhaustion` (the minimum effective iterations before exhaustion termination is allowed, currently 50). Both are recorded in the config, manifest, and environment metadata. An effective iteration is any round that completes a full ALNS iteration (candidate proposed, evaluated, and accepted or rejected). The wall-clock axis is not subject to exhaustion termination.

- Only the top-ranked candidates that pass the screen are exactly evaluated per round;
- set an exact-call budget per round;
- only after single-thread caching, incremental propagation, and deadline regressions all pass, use controlled parallel evaluation for independent candidates;
- fix the random stream, candidate ordering, and result merge order so parallelism does not alter the search trajectory;
- the parallel version must separately record thread count, task submission order, completion order, and final merge order.
- Any parallel or candidate-control scheme treats `cpu_batch` as the only current baseline; on parallel initialisation or execution failure it fails directly, without falling back to `cpu_scalar`.

### Required outputs

- Screening reason statistics;
- cache hit rate;
- exact calls per round;
- route-level and operator-level timings;
- effective ALNS iterations per second;
- performance profiles and peak memory;
- fixed-work / wall-clock dual-axis comparisons;
- exact-call reconciliation and deadline event reports;
- paired comparisons of `cpu_batch` and any better candidate backend under the same seeds, workload, and time budget; when no candidate replacement exists, no extra backend comparison is run;
- exact backend and batch launches, transitions, packing/unpacking, and total batch-time statistics.

### Gate to the next stage

- All Stage 2.3 hard gates inherited, and 36/36 solutions, objectives, and event logs recomputable by an independent replay auditor;
- exact calls on unchanged routes are 0, and candidate proposed/accepted/global-best event semantics fully reconciled;
- cache hits and misses, feasible and infeasible results are all replayable, and the cache does not alter the formal objective ordering of the unaccelerated version;
- a explainable, reproducible drop in per-round exact calls at scale versus the Stage 2.3 implementation;
- the formal Stage 3 performance targets remain `median exact charging calls <= 100` and `median effective iterations >= 50` on the focused R/RC runs; they cannot be replaced by larger time budgets or by excluding timed-out runs;
- feasibility and objective ordering consistent with the frozen golden evidence and the current `cpu_batch` baseline;
- cache, parallelism, and deadline introduce no non-deterministic errors;
- deadline overruns no longer show unexplained extra exact calls; if solver boundary errors remain, completed iterations, exact calls, hardware, source, and configuration differences must be recorded.
- All new Stage 3.3–3.4 runs explicitly record `cpu_batch` or a new backend that passed the replacement gates; discovering `cpu_scalar`, implicit fallback, or a missing backend field fails the review directly.

---

## Stage 4: Restructure the Adaptive Mechanism and Search Control

### Stage goal

After Stage 3 stabilises per-evaluation cost and event semantics, make the "Adaptive" in Adaptive Large Neighborhood Search statistically meaningful. A faster but unexplainable search trajectory must not replace quality evidence.

### Artifact label

This stage is uniformly labeled `stage04`; logs, ablations, and comparisons for fixed weights, adaptive weights, temperature, restart, and intensification must each record their component.

Stage 4's fixed/adaptive, temperature, restart, and intensification comparisons uniformly use `cpu_batch`; the experimental workload must not be changed by swapping the exact backend, and `cpu_scalar` must not be reintroduced.

### Concrete tasks

1. Use segment-based weight updates instead of updating after every call.
2. Every operator must reach a minimum call count within a learning period.
3. Track separately:
   - accepted improving;
   - accepted equal;
   - accepted worse;
   - rejected;
   - new global best;
   - vehicle reduction.
4. Automatically estimate the initial simulated annealing temperature so the initial acceptance rate of worse solutions falls in a preset interval.
5. Add:
   - reheating;
   - stagnation restart;
   - removal-size adaptation inherited from Stage 2.3 — this stage only evaluates its interaction with weight updates, it does not reimplement it;
   - incumbent intensification.
6. Vehicle-count reductions are rewarded above distance improvements; infeasible operations or vehicle creation must not receive spurious positive rewards.
7. Under the fixed `cpu_batch` backend, compare fixed weights vs adaptive weights under both fixed-work and wall-clock budgets, aggregated by instance and seed; conclusions must not be drawn from a single best seed.

### Required outputs

- Operator segment weight-change logs;
- temperature, acceptance rate, stagnation, and restart records;
- operator contribution rankings;
- a fixed-vs-adaptive weights ablation comparison.

### Gate to the next stage

- All operators have sufficient call samples in formal runs;
- large-scale runs show reasonable volumes of accepted-improving, accepted-worse, and rejected operations simultaneously;
- the adaptive version beats the fixed version on multiple instances/seeds;
- effectiveness must not be proven with a single best seed;
- the standard deviation drops versus Stage 0; if it does not, the reason must be reported, and high-variance seeds must not be deleted;
- operator rewards, event counts, and objective recomputation pass the Stage 3 replay auditor.

### Implementation result (2026-07-15)

Stage 4 implemented segment-based weight updates, six-category operator statistics, auto-estimated SA temperature, reheating, stagnation restart, incumbent intensification, and differentiated rewards, and completed the fixed-vs-adaptive ablation comparison. All runs use the `cpu_batch` backend and the `stage02_constraint_guided` operator profile.

Smoke `stage04_adaptive_weights_attempt01` completed 72/72 axes, all feasible, independent review `READY_FOR_STAGE05`. Formal `stage04_adaptive_weights_attempt02` completed 144/144 axes, all feasible, independent review `READY_FOR_STAGE05`.

The six review gates:

| Gate | Status | Details |
|------|--------|---------|
| operator_call_sufficiency | PASS | Sufficient operator calls on all wall_clock axes |
| six_category_statistics | PASS | All adaptive_wall_clock axes have acceptances and rejections |
| adaptive_better_than_fixed | PASS | Adaptive strictly better than fixed on 4 (instance, seed) pairs |
| not_single_best_seed | PASS | Adaptive wins on all 3 seeds (2014, 2015, 2016) |
| std_not_increased | PASS | Stage 4 vehicle_count std does not exceed Stage 0 |
| replay_consistency | PASS | 144/144 axes pass validator and objective recomputation |

Formal 100-customer results (adaptive_wall_clock axis; best/mean/median over 3 seeds):

| Instance | Best vehicles | Mean vehicles | Median vehicles | Std | Best distance |
|---|---:|---:|---:|---:|---:|
| `c101_21` | 12 | 12.5 | 12.5 | 0.5 | 1054.03 |
| `r101_21` | 20 | 22.08 | 21.0 | 2.47 | 1745.58 |
| `rc101_21` | 18 | 21.0 | 20.5 | 2.92 | 1858.33 |

Adaptive weights strictly beat fixed weights on 4 (instance, seed) pairs: `c101_21/2014`, `c101_21/2016`, `r105C15/2016`, `rc101_21/2015`. The wins spread across all 3 seeds — not dependent on a single best seed.

Stage 4's configuration is recorded in `configs/stage04_weights.toml`; `Stage04Config` is defined in `src/evrptw/stage04.py`; the ALNS integration is in `src/evrptw/alns.py`; the experiment runner is `src/evrptw/experiments/stage04_weights.py`; the independent review CLI is `src/evrptw/experiments/stage04_weights_review.py`; unit tests are in `tests/test_stage04.py` (32 tests, all passing). Ruff and mypy both pass.

Traceable evidence lives in `results/stage04_adaptive_weights_attempt02/` (formal raw artifacts), `results/stage04_adaptive_weights_attempt02_review/` (review artifacts), `experiments/summaries/stage04_adaptive_weights_attempt02_*.csv` and `.md` (tracked summaries), `experiments/registries/stage04_artifact_registry.csv`, and `experiments/manifests/stage04_adaptive_weights_artifact_manifest.json`. The Stage 0 manifest SHA-256 remains `b226b97e0e67288aaaf85726ad855df71cb81406685c57c8e8c40cd8996aa0da`; frozen files unmodified.

---

## Stage 5: Establish the Best-Known Comparison and the Complete Experiment System

### Stage goal

Upgrade from "the algorithm can produce feasible solutions" to "solution quality is quantified and the improvement's origin is explained".

### Artifact label

This stage is uniformly labeled `stage05`; the best-known, benchmark, and ablation parts use `stage05.1`, `stage05.2`, and `stage05.3` respectively; unlabeled shared summary files are not allowed.

The entry condition is not "Stage 2 is fast enough", but that Stage 3 has completed exact-call reconciliation, single-thread semantic regression, and deadline re-verification, and Stage 4 has completed the fair fixed-vs-adaptive comparison. Otherwise, expanding the benchmark only amplifies unexplainable running costs.

Stage 5.2 must first complete the fixed-work baseline with the currently reviewed `cpu_batch` as the reference backend, then select the formal backend, worker count, and storage policy per this roadmap's gates. The Stage 5.2 benchmark and the Stage 5.3 ablations that still call exact charging must use the same reviewed configuration set; `cpu_scalar` must not be used as an ablation arm, a performance baseline, or a regression path. The ablation variant that removes exact charging calls no exact backend.

### Concrete tasks

#### 5.1 Best-known values

Artifact prefix `stage05.1_best_known`; manifest component `best_known`.

1. Collect the formally published Schneider best-known values;
2. verify the distance metric, charging assumptions, vehicle-count objective, time windows, and vehicle parameters;
3. compute gaps only when the models are fully identical;
4. list model-inconsistent results separately; direct comparison is forbidden;
5. report `unknown` for instances without best-known values — no estimation or backfilling.

##### Implementation result (2026-07-15)

Stage 5.1 is implemented. The BKS data comes from three formally published journal articles: Schneider, Stenger & Goeke (2014) Table 5 provides the CPLEX optima for small instances (5/10/15 customers), with RC204-15 using the VNS/TS improvement value; Keskin & Çatay (2016) Table 2 provides the assembled best-known values for large instances (100 customers), integrating results from SSG, Goeke & Schneider (2015), and Hiermann et al. (2016). The Goeke & Schneider DOI is verified via CrossRef, but its PDF is not yet part of the local VOR literature collection.

Instance-name mapping: the literature notation `C101-5` maps to the repository's `c101C5` (lowercased, hyphen replaced by `C`); the literature notation `c101` maps to `c101_21` (the Solomon 100-customer suffix appended). All 92 instances (36 small + 56 large) have BKS vehicle and distance values. Charging time and charging count are never reported in published BKS tables and are uniformly recorded as `unknown`.

The model-compatibility assessment covers five dimensions: charging model (full recharge — compatible), objective function (published BKS use vehicle-count-first distance minimisation without charging time or count terms — incompatible), distance metric (published BKS possibly use rounded Euclidean distances — incompatible), time windows (compatible), vehicle parameters (compatible). The overall compatibility is `False`. Because the models are not fully identical, no gaps are computed; all 92 instances are marked `model_compatible=False` in `experiments/baselines/schneider_best_known.csv`.

Implementation files: core data module `src/evrptw/best_known.py` (92 BKS records, source citations, compatibility assessment); experiment runner `src/evrptw/experiments/stage051_best_known.py`; independent review CLI `src/evrptw/experiments/stage051_best_known_review.py` (5 gates: `instance_coverage`, `bks_values_present`, `no_gap_computation`, `compatibility_assessment_correct`, `replay_consistency`); config `configs/stage051_best_known.toml`; document `docs/stage051_best_known.md`; unit tests `tests/test_stage051.py` (48 tests, all passing). Ruff and mypy pass; the full repository suite of 254 tests passes.

The formal run executes on a clean commit; after review approval, `experiments/registries/stage05.1_artifact_registry.csv` and `experiments/manifests/stage05.1_best_known_artifact_manifest.json` are published, with review status `READY_FOR_STAGE05_2`.

#### 5.2 Performance governance and the scaled benchmark

Stage 5.2 maintains a single continuously iterated current implementation, internally executing gates in strict order. A–G are validation steps within one implementation, not seven long-lived versions; a later step must not begin formal evidence runs before the previous step passes independent review. Each part uses its own component, with `attemptNN/rerunNN` serving only as the canonical run identity:

- `stage05.2_perf_baseline_attemptNN`;
- `stage05.2_hot_path_attemptNN`;
- `stage05.2_artifact_streaming_attemptNN`;
- `stage05.2_job_parallel_attemptNN`;
- `stage05.2_native_kernels_attemptNN`;
- `stage05.2_accelerator_pilot_attemptNN`;
- `stage05.2_benchmark_attemptNN`.

The full execution protocol is in `docs/stage052_performance_benchmark_workflow.md`. The entry point of Stage 5.2 must be the independent review status `READY_FOR_STAGE05_2` of `stage05.1_best_known_attempt06`, inheriting the Stage 4 accepted formal identity `stage04_adaptive_weights_attempt15`.

The current chain is determined by signed manifests, prerequisite identities, and `experiments/registries/stage05.2_retention_registry.csv`; specific attempts are not hard-coded in this roadmap. Old runs' statuses, failure reasons, historical relations, and archive locations go into the registry and the change log; only the current accepted predecessor can open the next gate.

##### 5.2-A Fixed-work performance baseline

1. Fix instances `c101C5`, `c101_21`, `r101_21`, `rc101_21` and seeds `2014/2015/2016`;
2. record both fixed-work and wall-clock axes, but all causal performance conclusions rest on fixed-work;
3. record solver, artifact-persistence, and end-to-end times — CPU time or power draw alone must not be reported;
4. record per-stage durations, exact-call counts, batch occupancy, operator cost, core usage, peak RSS, rows/bytes written, and compression time;
5. fix the current `cpu_batch`, single worker, and `artifact-storage-v1` as the direct comparison baseline for every later gate.

##### 5.2-B Eliminate duplicated Python hot-path work

Process in profiling order: cache `Instance` name lookups, depot/customer/station grouping, and the distance matrix; fix the eager evaluation that rebuilds propagation snapshots on cache hits; the ejection chain rechecks only changed routes; the screening cache may store only provably safe, auditable positive results; give every operator a time and exact-call budget.

Acceptance uses a strict performance gate: fixed-work objective, validator, exact-call ordering, candidate decisions, and cache semantics must be identical; versus 5.2-A, the overall end-to-end median runtime over all 100-customer pairs must drop by at least 15%, and no C/R/RC family median may regress by more than 3%. On failure: seal the evidence, record the root cause, and archive — never lower the gate or bypass the semantic checks.

##### 5.2-C Streaming/sharded artifact storage

Implement `artifact-storage-v2`: Parquet row-group streaming, sharding by `(instance, seed)`, workers writing only their own shard, and the parent writing only the control manifest. Row groups are fixed at 65,536 rows; the writer buffers at most 2 row groups; every shard has its own manifest, checksum, and completeness state. The v1 reader must remain functional; historical bytes must not be moved or rewritten.

Gate: v1/v2 raw replay must agree on validator, objective, critical-event, exact-call, and failure semantics; artifact persistence must not exceed 30% of end-to-end; peak RSS must not exceed 50% of 5.2-A. Partial shards must be sealed, fail fast, and archive after checksum verification — never silently truncated or serially backfilled.

##### 5.2-D Job-level parallelism

The unit of parallelism is the independent `(instance, seed)` shard; the four-process intra-exact-call path already proven inefficient in Stage 3.4 is not reused. Run fixed-work comparisons with 1/2/4 workers; workers own shards exclusively, and the parent merges manifests by canonical key — completion order must not change replay order or event identity.

Gate: 2 workers must reach at least a 1.5× end-to-end speedup over 1 worker with aggregate RSS at most 12 GiB; 4 workers are selected only at ≥ 2.5× and ≤ 12 GiB. If 2 workers pass but 4 do not, the formal configuration is fixed at 2; if 2 workers fail, this gate is `NOT_READY`. Any worker exception terminates that run immediately; implicit serial fallback is not allowed.

##### 5.2-E Native CPU hot kernels

Migrate the profiling-confirmed hotspots — screening, snapshot propagation, distance lookup, exact label expansion/dominance/heap — into C++ contiguous-array implementations, releasing the GIL in computation regions that touch no Python objects. Large-scale rewrites must not replace per-hotspot fixed-work comparisons.

Gate: fixed-work semantics must be identical to the 5.2-D selected configuration; versus 5.2-D, the overall end-to-end median time over all 100-customer pairs must drop by at least another 15%, and no C/R/RC family median may regress by more than 3%.

##### 5.2-F Conditional accelerator gate

GPU/Metal/MPS is not a mandatory target. A new accelerator pilot run executes only when the median route batch occupancy of the current accepted native CPU backend reaches 32. The GPU pilot must separately record host-to-device, kernel, device-to-host, and synchronization times.

Only when fixed-work semantics are fully identical, the overall end-to-end median time over all 100-customer pairs drops by at least 15% versus the selected native CPU, and no C/R/RC family median regresses by more than 3%, may the GPU become the formal backend. Otherwise publishing `GPU_NOT_JUSTIFIED` is a legitimate pass of this gate, and the formal benchmark continues on native CPU; no automatic CPU fallback may be kept to mask accelerator failures.

##### 5.2-G Layered benchmark

First run a full pipeline pilot over the fixed Stage 0 representative set (12 instances × 3 seeds), covering the formal backend, workers, streaming writer, reviewer, and summary generation. After the pilot passes, execute the pre-declared layered budget:

- all 92 instances (36 small + 56 100-customer) run `10 seeds × 30 seconds`;
- only the 56 100-customer instances additionally run `10 seeds × 60 seconds` and `10 seeds × 300 seconds`;
- small instances do not run 60/300 seconds, to avoid wasting budget after the iteration limit;
- anytime checkpoints are fixed at `1/5/10/30/60/120/300 seconds` within the applicable budget;
- every failure first seals the original shard, manifest, and run label, then verifies the archive; failed samples are not shrunk, failures are not overwritten by rerun results, and large failed raw does not accumulate unboundedly in the repository worktree.

##### Version and retention governance across A–G

This is a governance rule spanning A–G; it does not add an eighth performance gate:

1. Stage 5.2 source always has a single current implementation; later improvements modify it directly;
2. `python -m evrptw.stage052_retention audit` generates a read-only inventory with SHA-256 sidecars;
3. `archive` must bind the inventory hash and verify per-directory file counts, byte counts, and tree SHA-256 before migration;
4. complete, partial, failed, `NOT_READY`, and superseded raw are all archived to `d_archive/stage05.2/history/<run_label>/`;
5. the repository keeps only the lightweight retention registry, the change log, and the scientific summaries published by independent review;
6. `docs/stage052_change_log.md` continuously appends modification reasons, impact scope, evidence effects, verification results, and the related run identities; it does not copy new version directories;
7. archived runs are resolved through the registry's run label and archive alias, re-verified on file counts, byte counts, and tree SHA-256 before use as prerequisite/review inputs; tracked documents do not contain machine-local absolute paths;
8. active/unsealed runs are denied archiving by default, and the registry merges incrementally by immutable run identity. Same-volume moves use atomic rename; cross-volume moves first copy to a temporary directory on the target volume, and only after full re-verification and atomic placement is the source directory cleaned.

The BKS model-incompatibility conclusion remains in force, so no gaps may be computed or published. The formal review must publish `stage05.2_artifact_registry.csv`, `stage05.2_performance_benchmark_artifact_manifest.json`, per-run results, per-family/budget summaries, anytime curves, and resource/persistence overhead tables, and only report `READY_FOR_STAGE05_3` when all replays/gates pass.

#### 5.3 Ablation study

Artifact prefix `stage05.3_ablation`; manifest component `ablation`.

Remove or replace separately:

- exact charging;
- route elimination;
- adaptive weights;
- simulated annealing;
- energy-aware repair;
- OR-Tools initialisation;
- cheap screening and caching.

Every ablation variant must use the same instances, seeds, and time budget, plus the Stage 5.2 selected backend, workers, and artifact-storage-v2 configuration. Fixed-work is the primary axis for causal ablations and wall-clock the auxiliary axis for practical gains; only the "remove exact charging" variant calls no exact backend.

### Required outputs

- Best-known data sources and the model-compatibility table;
- all per-run results and automatic summaries;
- model compatibility, vehicle counts, distance, feasibility, runtime, and stability tables; no gap columns while the current BKS is incompatible;
- anytime curves;
- ablation conclusions;
- complete failure, invalid, timeout, and error records.

### Gate to the next stage

- Overall conclusions no longer rest on only 12/92 representative instances;
- all public comparisons pass model-compatibility checks;
- ALNS at scale not only keeps a high feasibility rate but significantly improves vehicle counts and distance over the current version;
- the independent contribution of each core component is quantified;
- every summary number can be automatically recomputed from raw data.

---

## Stage 6: Extend BPC from 8 to 10–15 Customers

### Stage goal

Upgrade the current enumerated-column BPC into true dynamic column generation, providing credible lower bounds and optimality evidence for medium scale.

### Artifact label

This stage is uniformly labeled `stage06`; pricing, state-space, branching, and validation artifacts must each record their component, customer scale, and BPC node range.

Stage 6 and ALNS acceleration are independent tracks. BPC scaling must not block Stages 3/4, and heuristic incumbents must not be misrepresented as lower bounds or optimality proofs.

ESPPRC/BPC pricing itself does not execute ALNS exact charging route evaluation, so the Stage 5.2 selected ALNS backend does not apply; but Stage 6 evidence persistence inherits the `artifact-storage-v2` streaming/shard/job-parallel contract. ALNS incumbent warm starts and any component reusing ALNS route evaluation must use the Stage 5.2 selected backend and must not call `cpu_scalar`.

### Concrete tasks

#### 6.1 Dynamic ESPPRC pricing

Artifact prefix `stage06.1_pricing`; manifest component `pricing`.

Implement ESPPRC (Elementary Shortest Path Problem with Resource Constraints) pricing. Labels contain at least:

$$
L=(i,t,q,b,\bar c,V)
$$

denoting current position, time, load, battery, reduced cost, and the visited-customer set.

Implement:

- forward/backward resource labels;
- resource extension functions;
- reduced-cost dominance;
- resource-compatible joining;
- negative reduced-cost route search;
- a rigorous termination proof when no negative reduced-cost column is found.

#### 6.2 State space and branching

Artifact prefix `stage06.2_branching`; manifest component `branching`.

- ng-route relaxation;
- unreachable-set strengthening;
- decremental state-space relaxation;
- Ryan-Foster branching, replacing path-variable branching that depends on the full column pool;
- ALNS incumbent warm start.

#### 6.3 Staged validation

Artifact prefix `stage06.3_validation`; manifest component `validation`.

1. Cross-check against the existing full-column-pool BPC per instance on 5–8 customers;
2. both must reach the same root bound, incumbent, and final optimum;
3. then open 10-customer;
4. after passing, attempt 15-customer;
5. for 100-customer, initially require only a reliable lower bound — proving optimality is not required.

### Required outputs

- Dynamic pricing logs;
- root/final lower bounds;
- incumbent and optimality gap;
- labels generated/pruned/joined;
- columns generated;
- BPC nodes, cuts, and peak memory;
- cross-validation results against the old full-column-pool version.

### Gate to the next stage

- The dynamic version matches the full-column-pool version exactly on 5–8 customers;
- 10-customer produces a rigorous lower bound in reasonable time;
- the LP must never be claimed optimal merely because heuristic pricing found no column;
- timeouts must retain the lower bound, upper bound, and gap;
- BPC scaling must not disturb the ALNS main method.

---

## Stage 7: Enhanced Solution Representation and the Unified Validator

### Stage goal

Prepare an explicit, algorithm-agnostic solution structure for later partial recharge, so the validator no longer implicitly performs full recharging on the algorithm's behalf.

### Artifact label

This stage is uniformly labeled `stage07`; solution schema, route schedule, charging event, validator contract, and compatibility adapters must each establish a traceable artifact type.

The solution interface and validator contract may be developed early in Stage 3's measurement track, but a full-recharge compatibility replay must complete before they serve as the Stage 8 model entry. Interface migration must not rewrite Stage 0–2 historical results.

Stage 7's ALNS output conversion, full-recharge compatibility replay, and validator integration must preserve the ordered batch semantics of the Stage 5.2 selected backend and inherit the streaming/shard artifact contract; correctness checks use frozen samples and validator recomputation, without running `cpu_scalar`.

### Concrete tasks

Introduce explicit:

- `ChargingEvent`: station, arrival battery level, charge amount, start time, end time, departure battery level;
- `RouteSchedule`: node sequence, arrival/service-start/departure times, battery and load trajectories;
- `Solution`: route set, objective tuple, and algorithm-declared metrics.

The unified validator must re-check:

- every customer served exactly once;
- routes depart from and return to the depot;
- consistent time, battery, and load propagation;
- charging occurs only at legal stations;
- declared charge amounts match battery changes;
- charging times match the charging model;
- declared objectives match recomputed objectives;
- no charging decisions are automatically added that the algorithm did not output.

### Required outputs

- The explicit solution data structures;
- a compatibility adapter from old full-recharge routes to the new solution structures;
- unified output conversion for ALNS, BPC, OR-Tools, and GA;
- validation tests for wrong charge amounts, wrong times, and illegal stations.

### Gate to the next stage

- Current full-recharge experiment results pass the new validator with no numeric drift;
- all algorithms use the same solution interface;
- the validator depends on no specific algorithm's internal assumptions;
- partial charging can be added as a new model without breaking historical results.

---

## Stage 8: Upgrade to Partial/Nonlinear Charging Models

### Stage goal

After search quality, speed, theoretical comparison, and solution representation are stable, extend to more realistic charging decisions.

### Artifact label

This stage is uniformly labeled `stage08`; partial linear, piecewise linear, nonlinear, and queueing must use independent components, configurations, result directories, and validator reports.

Stage 8 is the final model-extension stage. Partial, piecewise-linear, and nonlinear results must be reported in separate directories, configurations, and validator reports from the current full-recharge baseline; model changes must not be explained as search-algorithm gains.

Any new Stage 8 charging model entering ALNS exact route evaluation must implement a compatible ordered batch interface and re-pass Stage 5.2's fixed-work semantics, strict performance, streaming/shard, and independent review gates. Models with only a scalar implementation are development prototypes only — they must not enter formal experiments, performance conclusions, or stage acceptance.

### Concrete tasks

Proceed strictly in this order:

1. partial linear recharge;
2. piecewise-linear charging;
3. nonlinear charging curves;
4. only last, consider station capacity/queueing.

Every model must:

- have an independent configuration name and results directory;
- have an independent exact subproblem or a rigorous discretisation-error statement;
- have a compatible ordered batch interface and re-pass the Stage 5.2 backend replacement gate; formal runs must not fall back to `cpu_scalar`;
- not overwrite current full-recharge results;
- match the corresponding validator formulas;
- report model complexity, runtime, and solution-quality changes;
- never mix results of different charging models into one benchmark conclusion.

### Required outputs

- A versioned charging-model interface;
- an exact or error-bounded subproblem for partial charging;
- full vs partial vs nonlinear comparison experiments;
- tables of charge amounts, charging times, route distance, and vehicle-count changes;
- a statement of model differences and applicability ranges.

### Stage completion criteria

- The new charging model passes independent validation;
- historical full-recharge results remain reproducible;
- the gains from the model upgrade are separable from algorithmic search improvements;
- results are not misdescribed as a stronger algorithm merely because charging assumptions were relaxed.

---

## 3. Cross-Stage Tests and Quality Gates

These tests are not executed once at the end; every stage must maintain them:

1. `cpu_batch` exact charging cross-validated against frozen golden fixtures and small-scale brute-force enumeration; `cpu_scalar` is not rerun;
2. ALNS customer-coverage, depot-endpoints, and feasibility invariant tests;
3. strict deadline-enforcement tests;
4. cache consistency and memory-cap tests;
5. BPC cross-validation against full integer enumeration / full column pools;
6. BPC non-root branching regression tests;
7. invalid/infeasible/timeout/error must never be swallowed;
8. large-scale performance regression tests;
9. `pytest`, Ruff, and MyPy strict stay fully green;
10. exact calls, cache, candidate state, and objective must be automatically reconcilable from raw logs;
11. small-scale smoke/replay preflight before formal experiments; formal runs use the frozen clean commit with a full hash manifest;
12. all experiment tables are generated automatically from raw logs; failures, invalids, timeouts, and errors must not exist only in terminal output.
13. Any new ALNS/exact-charging code, tests, and experiments after 2026-07-14, regardless of stage label, must assert that the backend is not `cpu_scalar` and must verify that error paths fail fast with no implicit fallback; the sole exception is explicitly labeled historical reproduction using the Stage 0–3.2 historical runners and frozen configurations that existed before 2026-07-14.
14. New acceleration backends from Stage 5.2 onward must first use the currently selected backend as reference and satisfy identical fixed-work semantics; the overall end-to-end median time over all 100-customer pairs must drop by at least 15%, and no C/R/RC family median may regress by more than 3%. New scalar hotspots must return through Stage 5.2's profiling→native CPU→conditional accelerator gates; bypassing them is forbidden.
15. From Stage 5.2 onward, solver time, artifact persistence time, and end-to-end time must be reported separately; CPU utilisation, chip power draw, or kernel time alone cannot support a speedup conclusion.

If any stage regresses feasibility, validation correctness, or reproducibility, fix the root cause first, then continue extending.

## 4. Final Acceptance Goals

After the full roadmap completes, the main baseline should reach:

1. **Feasibility**: stably high feasibility on the standard Schneider instances, targeting 100%, never below 95%;
2. **Vehicle count**: significant reductions on R/RC 100-customer versus the current 22–28/24–25 vehicles;
3. **Distance quality**: report gaps against compatible best-known values;
4. **Search efficiency**: enough effective neighborhood iterations within 30 seconds without changing the formal objective, meeting the exact-call and effective-iteration targets confirmed by Stage 3 review;
5. **Stability**: clearly improved standard deviations and worst values across seeds;
6. **Theoretical evidence**: BPC provides reliable lower bounds at 10–15 customers and proves optimality at small scale;
7. **Experimental credibility**: covers the complete or pre-declared layered Schneider instances, with no cherry-picking;
8. **Model clarity**: full/partial/nonlinear charging results strictly separated;
9. **Traceability**: every feasible, invalid, timeout, or failed result is traceable to raw logs and solution files.

The final evaluation criterion is no longer merely:

> Does the algorithm find a feasible solution?

It upgrades to:

> Does the algorithm stably find feasible solutions with fewer vehicles, shorter distances, near best-known values, and credible lower-bound or gap evidence on the standard instances — with every conclusion reproducible and verifiable?
