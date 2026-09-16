# FURP-2026 EVRP-TW — Complete Repository Report

> Report date: 2026-09-16
> Scope: the entire `FURP-2026-Yiyang-GUO-EVRP-TW` repository — code, experiment artifacts, verification system, documentation, and showcase materials
> Nature: read-only audit report (no repository content was modified in producing it, apart from this report itself)

---

## 0. One-Page Summary

This project is a Faculty Undergraduate Research Practice (FURP) individual research project at the University of Nottingham Ningbo China (UNNC). It replicates and extends the E-VRPTW (Electric Vehicle Routing Problem with Time Windows and recharging stations) of Schneider, Stenger & Goeke (2014), *Transportation Science*, DOI: 10.1287/trsc.2013.0490. The project ran from 2026-06-12 to the last commit on 09-14, totalling **188 commits**.

Headline results (each backed by an independent review evidence chain):

| Result | Value | Evidence |
|---|---|---|
| Fleet-size reduction (best-sum over 12 instances) | **87 → 76 vehicles (−12.64%)** | Stage 0 frozen baseline vs. Stage 2.1 accepted evidence |
| Total distance reduction (sum over best-vehicle runs) | 7,744.4 → 7,349.4 (**−5.10%**) | Same as above |
| Feasibility rate | **36/36** (all 12 instances × 3 seeds pass the unified validator) | Stage 2.3 rerun09 independent replay |
| Exact-charging solve speed-up (cpu_batch) | Median savings of 21.97% / 11.54% / 24.40% across the three 100-customer families (c101_21 median speed-up 1.281×) | `cpu_batch_pilot_attempt01` independent review |
| Stage 4 adaptive weights | Beats fixed weights on 7 (instance, seed) pairs (gate ≥ 3), with wins on all 3 seeds | `stage04_adaptive_weights_attempt15` formal review |
| Engineering system | 33 core modules + 31 experiment/review entry points ≈ **72,141 lines of Python** + a C++ pybind11 native kernel; **751 tests**; 12,121 raw-evidence files (≈ 172 GB); 173 archived Stage 5.2 runs | Measured directly in this repository |

The project has advanced to **Stage 5.2 G (benchmark)**: the Pilot passed (attempt21 — 36/36 axes, 18/18 gates, `READY_FOR_STAGE052_FORMAL_BENCHMARK`), but the **large-scale Formal benchmark (2,040 solves, 229,200 seconds of budget) is not yet complete** — the two most recent Formal attempts (attempt22: load-guard misjudgement; attempt25: SQLite cross-thread spill) have both been root-cause fixed with their failure evidence retained, pending a retry from a new Pilot label.

---

## 1. Project Positioning and Scale

### 1.1 Basic Facts

- **Student**: Yiyang Guo (郭一阳), Mathematics and Applied Mathematics, individual project
- **Title**: Replication and Extension of the Electric Vehicle-Routing Problem with Time Windows and Recharging Stations (EVRP-TW)
- **Replicated paper**: Schneider, Stenger & Goeke (2014), *Transportation Science* 48(4) 500–520
- **Remote repository**: `github.com/0neblaze/FURP-2026-Yiyang-GUO-EVRP-TW` (master branch + the historical `week05-alns-bpc-rebuild` branch)
- **Commit timeline**: 2026-06-12 → 09-14; peak activity 07-13 to 07-24 (the entire Stage 2.3 → 5.2 mainline was completed in late July)
- **Primary development environment**: macOS (review-report provenance shows `/Users/guoyiyang/...`, CPython 3.13.13, CPLEX 22.2 / Gurobi 13.0.2 / HiGHS 1.14 / OR-Tools 9.15.6755); this Windows checkout is a copy (see §8)

### 1.2 Measured Repository Scale

| Directory | Contents | Scale |
|---|---|---|
| `src/evrptw/` | Core library (33 top-level modules) + `experiments/` (31 runner/review CLIs) | 72,141 lines of Python |
| `cpp/evrptw_core.cpp` + `CMakeLists.txt` | C++20 pybind11 native kernel (screening/propagation/distance/exact labelling) | 1 translation unit |
| `tests/` | 47 test files, **751 tests** (measured via pytest collection) | — |
| `results/` | Raw experiment evidence (git-ignored), 115 run directories | 12,121 files / ≈ 172 GB |
| `experiments/` | Tracked summaries, registries, manifests, frozen baselines | 744 files / ≈ 3.7 GB (including 157 MB-scale operator-event CSVs) |
| `configs/` | 16 TOML files (one formal config per stage + local storage-root template) | — |
| `data/schneider/` | 92 Schneider benchmark instances + SHA256SUMS (git-ignored) | 94 files |
| `document/literature/` | 6 VOR journal-paper PDFs + 2 alternative copies + SHA256SUMS + references.bib (git-ignored) | 11 files |
| `docs/` | Weekly reports, stage protocols, method documents, publication-landscape survey | 24 md + 1 bib (worktree) |
| `poster/` | Poster v2 engineering sources (design/story docs, rebuild scripts, figure assets); final artifacts live at the repo root as `FURP_Showcase.pdf`/`poster.pptx` | 12 files |

---

## 2. Research Problem and Model

### 2.1 The Problem

E-VRPTW: battery-limited electric vehicles + hard time windows + en-route recharging stations (full-recharge model, charging time t = (Q − b)·g). Instances are the Solomon-derived Schneider benchmarks: C/R/RC families with 5/10/15/100 customers, 92 instances in total (12 representative instances form the formal experiment scope).

### 2.2 Formal Objective

A lexicographic four-tuple `(vehicle_count, total_distance, total_charging_time, charging_count)` — **vehicle count has absolute priority**; ALNS hard-rejects any candidate that increases the vehicle count, including during simulated annealing. All objective construction and comparison is forced through the deep module `evrptw.objective`; callers are forbidden from duplicating tuple construction or comparison logic.

### 2.3 Method Stack

1. **ALNS main search**: destroy/repair operator families, extended per stage via profiles (baseline → route_reduction → route_quality → constraint_guided; the current default is the Stage 2.3 profile).
2. **Exact charging subproblem**: for a fixed customer sequence, the station-insertion and full-recharge decisions are solved exactly, preventing greedy insertion from masking energy infeasibility. Backend evolution: `cpu_scalar` (historical reference) → `cpu_batch` (current default, adopted after a paired review) → the C++ native kernel (Stage 5.2 E).
3. **Unified validator**: independently re-checks capacity, time windows, battery, coverage, and objective values; a solution from any algorithm counts as feasible only after passing the validator.
4. **BPC exact comparison**: Branch-Price-and-Cut (bidirectional labelling) provides proven optima only for instances with ≤ 8 customers; beyond that capability it explicitly returns `not_applicable` rather than fabricating a lower bound.
5. **Baselines**: OR-Tools VRPTW (transparent classical baseline) and GA VRPTW (weak baseline, adapted from the `iRB-NAS/py-ga-VRPTW` reference implementation).
6. **Layered performance engineering** (Stages 3–5.2): measurement instrumentation → safe screening → caching/incremental propagation → exact-call deadlines → candidate control and controlled parallelism → adaptive weights → native kernels and streaming evidence.

---

## 3. Code Architecture

### 3.1 `src/evrptw/` Core Modules (33)

- **Model & parsing**: `models.py`, `parser.py`, `instances/`, `repository.py`
- **Algorithmic core**: `alns.py`, `heuristics.py`, `neighborhoods.py` (deep module: all destroy/repair/merge operator proposals and event records), `repairs.py`, `objective.py` (the sole objective-construction point), `validation.py` (unified validator), `charging.py` (exact charging subproblem), `bpc.py`, `baselines/` (ga_vrptw, ortools_vrptw)
- **Performance layer**: `cpu_batch.py`, `cache_incremental.py`, `measurement.py`, `exact_deadline.py`, `candidate_control.py`, `native_kernels.py` (C++ bindings), `_core.pyi` (native stubs)
- **Stage 4/5**: `stage04.py` (`Stage04Config`/`reward_for()`), `best_known.py`, `stage052*.py` (9 modules: performance, campaign, evidence, platform, remediation, retention, review service, accelerator)
- **Infrastructure**: `artifacts.py` (ArtifactBundleWriter/Reader, v1/v2/v3 storage), `environment.py`, `metrics.py`, `benchmark.py`

### 3.2 Experiment Entry Points (31 CLIs)

Every stage provides both a **runner** (produces evidence) and an **independent review CLI** (replays and audits): `stage00_baseline` … `stage052_campaign_review`, plus the Week 2–5 historical entry points and `cpu_batch_pilot(_review)`.

### 3.3 Toolchain

- Build: scikit-build-core + pybind11 3.0 (wheel packages `src/evrptw` + `tools`)
- Quality: ruff (line 100; E/F/I/UP/B/SIM), mypy **strict**, pytest
- Solvers: CPLEX 22.2, docplex, Gurobi 13.0.2, HiGHS 1.14 (for BPC/exact comparison), OR-Tools 9.15
- `tools/`: artifact preflight, runtime freeze, Stage 3.3/3.4/5.2 artifact publication (review-only)

---

## 4. Stage Evolution and Accepted Evidence Chains

> Full policies live in `AGENTS.md` (~880 lines, with a Canonical Artifact Policy per stage). Every stage's accepted evidence follows the pattern "producer run + independent review-CLI replay + two independent complete reruns (Stage 2.x)".

### 4.1 Weeks 1–6 (Literature and Baseline Period)

| Week | Output |
|---|---|
| W1 | Literature screening; SSG (2014) locked in as the replication paper; VOR verification; benchmark-data location |
| W2 | Baseline rebuild: OR-Tools VRPTW + GA VRPTW (against the py-ga-VRPTW reference repo); Schneider-style instance generation |
| W3 | Experiment design and evaluation framework: comparing the feasibility impact of charging insertion under a single independent validator |
| W4 | Battery-capacity sweep (60/80/100/120) + late/anticipatory charging repair |
| W5 | Main method takes shape: ALNS + exact charging + small-scale BPC comparison; 120 records (15 scenarios × 4 algorithms): **ALNS 45/45 feasible (100%)**, BPC 6/15 applicable and all proven optimal, GA 6/45 (13.3%), **OR-Tools 0/15 (all energy-invalid)**; ALNS matched the BPC-proven optimum on c101C5/r105C5/rc105C5 best solutions |
| W6 | Method integration (Track B): a unified auditable workflow (instance audit → ALNS → exact charging → unified validation → comparison → summary) |

### 4.2 Stage 0: Frozen Baseline

- Scope: 12 instances × seeds 2014/2015/2016 × 30 s × 1000 iterations × single thread; the sole parameter source is `configs/stage00_baseline.toml`
- Per-run records: feasibility/objective/energy/charging/iterations/acceptance/exact-call counts + structured violation counts + Git revision/dirty flag, source-file SHA-256, instance hashes, environment metadata
- `experiments/baselines/stage00/` is the **immutable frozen baseline** (manifest SHA-256 `b226b97e…`; every later review re-verifies it is unchanged)
- Baseline anchor values: 12-instance best vehicle-sum **87**, mean **90.67**; best-vehicle-run distance-sum **7,744.4**

### 4.3 Stage 1: Lexicographic Objective

Vehicle-first objective enabled; ALNS hard-rejects vehicle increases; the BPC comparison uses the same objective. Artifacts: `stage01_per_run_results.csv` and 5 other tables (36 runs).

### 4.4 Stage 2.1 → 2.2 → 2.3: The Operator-Extension Trilogy

- **2.1 Route reduction** (`stage02_route_reduction` profile): route-elimination destroy, vehicle-count-aware repair, route merge; acceptance criterion = every removed customer is repaired into existing routes and the candidate has exactly one fewer route. **Result: best vehicle-sum 87 → 76 (−12.64%), mean 90.67 → 77.0 (−15.06%)**; per-family best: C 22→19, R 31→28, RC 34→29; best-vehicle distance-sum −5.10%. Accepted: `stage02_attempt02` + `stage02_rerun01` (two independent complete reruns).
- **2.2 Cross-route quality** (`stage02_route_quality`): relocate / swap / two_opt_star / route_segment_destroy / ejection_chain; route count preserved + at least one same-vehicle-count distance improvement. Accepted: `stage02_quality_attempt02` (the comparison baseline thereafter).
- **2.3 Constraint-guided search** (`stage02_constraint_guided`, current default): four deterministic destroys — station_pressure / time_window_conflict / worst_energy_detour / shaw_related — plus dynamic removal sizes (three tiers 5–10/10–20/20–35%, escalating after 4/8 stagnation iterations) and an in-budget vehicle_reduction_refinement regret repair (512 exact-call cap). Accepted: `attempt16` + `rerun09`, independent review **READY_FOR_STAGE03**:
  - 36/36 raw solutions pass the unified validator with matching objective recomputation; 200,731 operator-event rows / 165,467 failure-event rows independently replayed; 20 real constraint-level failure cases (gate ≥ 3); 9/36 runs with 30 s timeout overruns ≤ 0.017 s, all with timeout events recorded; source/config/instance/environment hashes consistent; Stage 0 manifest unchanged.

### 4.5 Stage 3.0–3.4: Performance Engineering (reading chain: measurement → screening → caching → deadline → parallelism)

| Sub-stage | Component | Accepted evidence | Review status |
|---|---|---|---|
| 3.0 | `measurement` | `stage03_measurement_formal01` | `READY_FOR_STAGE03_ACCELERATION` |
| 3.1 | cheap screening | `stage031_cheap_screening_formal01` | `READY_FOR_STAGE03_2` |
| 3.2 | cache/incremental | `stage03.2_cache_incremental_attempt03` | `READY_FOR_STAGE03_3` |
| 3.3 | exact deadline | `stage03.3_exact_deadline_attempt06` | `READY_FOR_STAGE03_4` (72/72 axes) |
| 3.4 | control/parallel | `stage03.4_control_parallel_attempt10` (smoke 72/72) + `attempt11` (formal 144/144) | **`READY_FOR_STAGE04`** |

Key points:
- 3.1 safe screening may only reject "provably infeasible" candidates (structural/capacity lower bounds/forward-backward time-window propagation/relaxed non-negativity/optimistic battery reachability/energy lower bounds); the shortest-distance lower bound is diagnostic and ordering-only, never a hard rejection.
- 3.3 established the dual-axis protocol: wall-clock (30 s/1000 iterations) and fixed-work (process-level shared budget of 100 exact calls + 120 s watchdog); calls returning at or after the lane deadline are atomically marked interrupted.
- 3.4 inherits the warm-start protocol (loads the 3.3 wall-clock incumbent and fully revalidates it); candidate ordering is deterministic vehicle-first; a four-worker `spawn` process pool merges in submission order; the Stage 3 legacy targets (R/RC wall-clock median started exact calls ≤ 100, fixed-work median effective iterations ≥ 50) were met.
- Side result: `cpu_batch_pilot_attempt01` (4 instances × 3 seeds, paired review) achieved median savings of 21.97%/11.54%/24.40% on the three 100-customer families; **`solve_alns()` default switched to cpu_batch**; C5 comparison −0.12% median (from 8.66% slower to 4.54% faster).

### 4.6 Stage 4: Adaptive Weights and Search Control

- `Stage04Config` (frozen dataclass): segmented weight updates (default 50-iteration segment boundary + minimum 5 calls), six operator-class statistics, differentiated rewards (vehicle reduction 8.0 > distance improvement 4.0 > accept-equal 1.0 > accept-worse 0.5 > reject 0; global-best + vehicle reduction 16.0), automatic SA temperature estimation (30 samples calibrated to a 50% acceptance rate), reheat/stagnation restart/incumbent reinforcement.
- Four-axis experiment (adaptive/fixed × wall_clock/fixed_work), 144 formal axes.
- Six review gates: operator-call sufficiency, six-class statistics completeness, **adaptive beats fixed on ≥ 3 pairs (measured: 7)**, not a single seed (wins on all 3 seeds), vehicle-count std no higher than Stage 0, replay consistency.
- Evidence version chain (v1→v6 with progressively stricter reviewers): attempt01/02 (v1) → 03/05 (v2) → 06/07 (v3) → 10/11 (v4) → 12/13 (v5) → **accepted v6: `attempt14` (smoke 72/72) + `attempt15` (formal 144/144), `READY_FOR_STAGE05`**. All superseded attempts are retained and cannot be "revived" by the v6 reviewer.

### 4.7 Stage 5.1: Best-Known-Solution (BKS) Reference

- 92-instance BKS compilation: small instances (36) from SSG (2014) Table 5 CPLEX optima (RC204-15 takes the same table's VNS/TS value 384.86); large instances (56) from Keskin & Çatay (2016) Table 2 (which assembles SSG/GS/HPH sources).
- **Model-compatibility verdict: `model_compatible=False`** (5-dimension assessment: charging-model compatible, time-window compatible, vehicle-parameter compatible; objective function incompatible — published BKS uses a 2-term lexicographic/weighted sum vs. this repo's 4-tuple; distance metric possibly incompatible due to rounding) → **no gap computed, no estimated values backfilled**.
- Accepted: `stage05.1_best_known_attempt06` (v6, all 92 rows independently replayed, all five gates passed, `READY_FOR_STAGE05_2`); artifact `experiments/baselines/schneider_best_known.csv` (93 rows including header).

### 4.8 Stage 5.2: Performance Governance and the Layered Benchmark (A–G sequential gates, single implementation)

| Gate | Component | Content and thresholds | Status |
|---|---|---|---|
| A | `perf_baseline` | Frozen re-verifiable performance baseline (instrumentation on/off semantically identical) | Passed (`READY_FOR_STAGE052_HOT_PATH`) |
| B | `hot_path` | Python hot-path deduplication | Passed |
| C | `artifact_streaming` | Storage v2 strategy + `screening_decisions_v3` physical mode: 65,536-row row groups, ≤ 2 non-empty buffers, typed streams, **persistence ≤ 36% of end-to-end**, peak RSS ≤ 50% of v1 | Passed |
| D | `job_parallel` | Empirical worker-count selection among 1/2/4 (2w ≥ 1.5×, 4w ≥ 2.5×, RSS ≤ 12 GiB) | Passed |
| E | `native_kernels` | Profiling confirmed hotspots before C++ migration; **overall paired median end-to-end ≥ 15%, any-family regression ≤ 3%**, zero fallback | Passed (attempt15 et al.) |
| F | `accelerator_pilot` | Conditional GPU/Metal/MPS decision (start only if batch occupancy ≥ 32, else `GPU_NOT_JUSTIFIED`) | Passed (attempt12/14, `READY_FOR_STAGE052_BENCHMARK`) |
| G | `benchmark` | Pipeline pilot (12 instances × 3 seeds × 30 s single-axis, full-resource sampling/failure recovery/anytime checkpoints/archive drill) → Formal | **Pilot passed; Formal in progress** |

- **G Pilot accepted**: `stage05.2_benchmark_attempt21` — 36/36 axes, 18/18 campaign gates, aggregate persistence ratio 0.3360 < 0.36 hard gate, `READY_FOR_STAGE052_FORMAL_BENCHMARK`.
- **Formal budget matrix**: 36 small instances × 10 seeds × 30 s + 56 100-customer instances × 10 seeds × (30/60/300 s) = **2,040 solves, 229,200 declared solver-seconds, 10,400 anytime records, 920 atomic (instance, seed) shards**.
- Formal failure-retention chain (both root causes fixed): attempt22 — the runtime load guard counted the campaign's own 4 workers against the idle-host `load1 ≤ 4.0` check (fixed to a dynamic in-batch bound of `4.0 + selected_workers`, with the reviewer independently reconstructing from the frozen worker count); attempt25 — after route-identity disk spill, SQLite's same-thread check rejected cross-thread access (fixed with shard-turn serial handoff + `check_same_thread=False`, plus a forced-spill regression test).
- **Current status: awaiting a Formal retry from a new G Pilot label** (A–F do not need to be rerun; G-only fixes may consume the accepted F evidence provided the commit is a Git descendant and the diff falls within an explicit allowlist).

### 4.9 Stage 5.2 Review Infrastructure (Windows/WSL2 Formal Host)

- Long-running reviewers execute as **transient `systemd --user` services** (`MemoryHigh=5G/MemoryMax=6G/MemorySwapMax=2G`, no restart, `ExecStopPost` seals the execution receipt, cgroup memory-peak accounting enforced).
- Sealed reviewer wheels: per-file source binding to tracked `tools` modules, byte-identical rebuild without cache, `python -I` isolated review.
- Producer runtime identity is replayed by raw-bound frozen venvs; the Windows build uses the locale-independent `OperatingSystemSKU` instead of the localized Caption.
- Retention system: `experiments/registries/stage05.2_retention_registry.csv` (**173 archived runs**) + tree SHA-256 verification against the external `d_archive` volume; the worktree keeps only signed manifests/registries/change logs.

---

## 5. Key Quantitative Results Summary

| Metric | Value | Basis |
|---|---|---|
| Vehicles (best-sum) | 87 → 76, **−12.64%** | Stage 0 frozen vs. Stage 2.1 accepted; best over 3 seeds per instance, summed over 12 instances |
| Vehicles (mean-sum) | 90.67 → 77.00, −15.06% | Same, mean over seeds summed |
| Per-family best vehicles | C 22→19 / R 31→28 / RC 34→29 | Same |
| Total distance | 7,744.4 → 7,349.4, **−5.10%** | Distance summed over best-vehicle runs |
| Feasibility | 36/36 (0 synthetic cases) | Stage 2.3 rerun09 independent validator replay |
| Exact-call behaviour | 1,687–2,161 calls per 30 s (21-customer) | Stage 2.3 per-run records |
| Operator-event volume | 200,731 event rows / 165,467 failure-event rows | attempt16 review |
| Stagnation escalations | 17,892; global-best resets 144 | attempt16 event replay |
| Timeout discipline | 9/36 runs with overruns ≤ 0.017 s, all with timeout events recorded | rerun09 review |
| cpu_batch speed-up | Family medians −21.97%/−11.54%/−24.40% (c101_21 1.281×, r101_21 1.131×, rc101_21 1.323×) | 4-instance paired protocol, C5 comparison −0.12% median |
| Stage 4 adaptive wins | 7 pairs (c101_21×3, r101_21, r105C15, rc101_21×2), across 3 seeds | attempt15, all six gates passed |
| BKS coverage | 92/92 instances with vehicles+distance values; charging all unknown | Stage 5.1 attempt06 |
| Stage 5.2 Pilot persistence ratio | 0.3360 (< 0.36 hard gate) | attempt21 campaign |
| Archived runs | 173 (including NOT_READY/partial/superseded, all retained) | Retention registry |

---

## 6. Verification and Reproducibility System (This Repository's Defining Feature)

The trust design of this repository exceeds a typical undergraduate project and approaches an industrial-grade audit pipeline:

1. **Unified validator + objective recomputation**: every raw solution is re-run through `validate_routes()` by the review CLI with the objective independently recomputed via `evrptw.objective`; any mismatch fails.
2. **Per-stage independent review CLIs** (producer/reviewer separation): half of the 31 experiment entry points are reviewers; a reviewer verifies the manifest first, then checksums, then replays semantics — tracked summaries can only be regenerated from raw data, never copied from producer state tables.
3. **Hash and provenance chains**: source/config/instance/environment SHA-256, native-extension hashes, uv.lock, package versions, Python metadata, and both reference-repository revisions; Stage 0 manifest immutability is re-checked at every review.
4. **Two independent complete reruns**: Stage 2.1/2.3 both require the attempt plus an independent rerun to pass (the `independent_complete_rerun` gate).
5. **Failure retention and no overwriting**: every failed/interrupted/timed-out attempt retains its raw evidence under a new label; `NOT_READY`, `superseded`, and `partial` statuses are explicitly registered; relabelling as success is forbidden.
6. **Canonical artifact policy**: `run_label` must match `stageNN[.minor]_component_attemptNN|rerunNN`; physical layout `results/<run_label>/<instance>/<seed>/`; Parquet event streams + a route dictionary as the sole store of full customer sequences; semantic digests guarantee that physically compressed layouts do not affect replay.
7. **Byte budgets and resource guards**: hard caps of 2 GiB/shard and 32 GiB/run; exceeding them seals partial evidence and fails fast; reviewers use bounded Arrow streaming (`to_pylist()` forbidden).
8. **Resource and power governance** (Stage 5.2): dual-window `load1` preflight ≤ 4.0, dynamic in-batch bound of `4.0 + workers`, single-core exclusion of unrelated processes, hard gates on AC power/low-power mode, 12 GiB RSS process-tree cap, cgroup peak accounting.
9. **Gated review matrices**: Stage 2.3 has 14+ checks, Stage 4 six gates, Stage 5.1 five gates, Stage 5.2 campaign 18 gates; readiness statuses (`READY_FOR_STAGENN`) can only be issued by independent replay.
10. **Frozen reproducibility protocol**: the 12×3 scope, seeds 2014–2016, and 30 s/1000 iterations/single thread are hard-coded in configs and policy; the Stage 5.2 Formal adds the 92-instance × 10-seed budget matrix.

---

## 7. Materials and Artifact Inventory

### 7.1 Tracked Materials (`experiments/`)

- `baselines/stage00/`: frozen baseline (per_run/summary/failure/environment/manifest/solutions/reproduction_audit)
- `baselines/schneider_best_known.csv`: 92-instance BKS + compatibility annotations
- `summaries/`: per-stage per-run/summary/gate/review/report file families (Stage 2.3 alone has 382 file prefixes; Stage 4 six attempt versions; Stage 5.1 six attempt versions)
- `registries/`: stage03.0–3.4, stage04, stage05.1 artifact registries + legacy path map + **stage05.2 retention registry (173 runs)**
- `manifests/`: per-stage artifact-manifest JSON + SHA-256 sidecars

### 7.2 Raw Evidence (`results/`, git-ignored, ≈ 172 GB)

115 run directories: week01–05, all stage00–05.1 attempt/rerun directories, and the Stage 5.2 retention list (bulk evidence lives on the external archive volume).

### 7.3 Documentation (`docs/`)

- Weekly reports 01–06 plus per-week technical checkpoints (OR-Tools, baseline rebuild, experiment design, extended reading, ALNS/BPC methodology, second-edition rebuild report)
- 17 stage-protocol documents (stage00 → stage052_change_log / performance_benchmark_workflow; **currently deleted in the worktree but fully preserved in git HEAD**, see §9.1)
- `experiment_artifact_storage.md` (storage v2/v3 rules), `environment.md`, `reference_selection.md`, `references.bib`
- `research/evrptw_publication_landscape_2026.md` (untracked): 2023–2026 publication-landscape and Q1/Q2 threshold survey (211-paper ALNS-VRP meta-analysis, exact-method frontier, software-paper standards)

### 7.4 Showcase Materials

- `FURP_Showcase.pdf` + `poster.pptx` (repo root): the final showcase poster v2 artifacts (render-verified PDF exported via PowerPoint COM); they supersede the v1 `FURP_Showcase.pdf`/`FURP_Showcase_Poster.pptx` pair (v1 preserved in history at fd02d6a); the root PDF keeps the certificate-required filename
- `poster/`: the v2 poster engineering — `STORY.md` (narrative: Motivation → Method → Experiment → Results → Honest claims), `DESIGN.md` (A0-portrait layout mapping, palette #10263B/#2E6CA4, overflow-budget verification), `rebuild_poster.py`/`make_chart.py` (on-the-fly data extraction + assertions verifying 87→76), `verify_render.txt` (render-text verification)
- Poster headline claims (all traceable): −12.6% vehicles, zero regressions, −5.1% distance, 36/36 feasible, −22.0% CPU, EVIDENCE AT SCALE (12,121 files / 200,731 event rows / 20 real failure cases / 0 synthetic)

### 7.5 Literature Collection (`document/literature/`, git-ignored)

6 verified VOR papers: SSG 2014 (TS), Hiermann et al. 2016 (EJOR), Keskin & Çatay 2016 (TRC), Montoya et al. 2017 (TRB), Pelletier et al. 2016 (TS), Desaulniers et al. 2016 (OR) + 2 alternative copies; SHA256SUMS coverage; the "no downloads, user-provided VOR only" policy is respected.

### 7.6 Data and References

- `data/schneider/`: 92 instances + SHA256SUMS
- `reference/`: `py-ga-VRPTW` (GA baseline reference implementation), `VRP-EVRP-Project-Hub` (read-only reference)
- `configs/`: 16 TOML files (including the `stage052_storage_roots.example/local.toml` storage-root locator templates)

---

## 8. Tests and Current Environment State (Measured on This Windows Checkout)

### 8.1 Test Scale

pytest collects **751 tests** (47 files); static counting finds ~686 test functions (751 after parametrization expansion).

### 8.2 Full Local Run

`623 passed / 127 failed / 1 skipped` (73 s). **All failures are environmental, not algorithmic regressions**, with two root causes:

1. **Stale native extension (113 failures)**: this machine's `.venv` ships an old build of `evrptw._core` whose `dir()` shows **0** stage052/screening exports, while the `_core.pyi` stub already declares them (e.g. `create_stage052_screening_definition_cache`). All stage052/artifacts test series fail with `AttributeError`. Fix: rebuild the native extension (scikit-build-core + pybind11).
2. **Windows path escaping (14 failures)**: stage00/stage01 runner tests write `C:\Users\...` into TOML basic strings in temp directories, and `\U` is parsed as an invalid unicode escape (`tomllib.TOMLDecodeError: Invalid hex value`). A Windows-compatibility defect in the test fixtures.

There is also harmless noise: SQLite temp files locked during teardown (WinError 32) — cleanup warnings only.

**Conclusion: the primary development/review environment is macOS (per producer provenance), and the full protocol closes there; this Windows checkout needs a native-extension rebuild before it has full test capability.**

---

## 9. Risks, Open Items, and Worktree Anomalies

### 9.1 Uncommitted Worktree State (Attention Required)

`git status` shows:

- **17 tracked documents deleted in the worktree (not staged)**: `docs/stage00_baseline.md`, `stage01_lexicographic_objective.md`, `stage02_{route_reduction,route_quality,constraint_guided,constraint_guided_review}.md`, `stage03_{measurement,artifact_registry}.md`, `stage031/032/033/034_*.md`, `stage051_best_known.md`, `stage052_{change_log,performance_benchmark_workflow}.md`, `cpu_batch_pilot.md`, and the root `EVRP-TW主Baseline分阶段改进路线图.md`. All are fully preserved in git HEAD (several citations in this report were taken from HEAD). If the deletion was unintentional, run `git restore docs/`.
- **Untracked new directories**: `.workbuddy/` (AI workspace) and `docs/research/` (publication-landscape survey); the poster v2 engineering is tracked under `poster/`.
- In the README quick checklist, "share with the research group / public repository" and "first meeting_notes file" remain unchecked.

### 9.2 Project-Level Open Items

1. **Stage 5.2 G Formal incomplete**: the Pilot (attempt21) passed, but the 2,040-run budget experiment has not produced results; the two engineering root causes behind attempt22/25 are fixed, and policy requires retrying from a new G Pilot label (A–F not rerun).
2. **README not updated for Stages 3–5.2**: the README's stage narrative stops at Stage 2.3, while AGENTS.md and the docs/ protocol documents have evolved to Stage 5.2 — the externally visible narrative lags the actual progress.
3. **BKS incompatibility is an honest boundary**: the objective function and distance metric differ from the published BKS, so no gap comparison was made — publications must phrase improvements as "relative improvement within the self-consistent baseline".
4. Poster and weekly-report figures were verified consistent (87→76/−12.6%, −5.1%, 36/36, −22.0% c101_21 median).

### 9.3 Certificate-Condition Cross-Check (Three FURP Rules)

- Attendance > 50%: continuously recorded in weekly reports (W1 notes the supervisor had not booked a room; W4 unrecorded)
- `FURP_Showcase.pdf` (the final showcase poster v2) placed at the repository root ✓ — satisfies the certificate filename rule; v1 content preserved in history at fd02d6a
- Poster Showcase: poster v2 rebuilt and ready (pending presentation)

---

## 10. Conclusion

Starting from the FURP research requirement of "replicate SSG (2014) E-VRPTW + ≥ 10% novelty", this project has in practice delivered an **algorithm-engineering and research-audit system approaching publishable standards**:

1. **Academic results**: the ALNS + exact-charging-subproblem combination under a lexicographic vehicle-first objective achieved audited improvements of −12.64% vehicles and −5.10% distance within the frozen 12×3 protocol; the BPC exact comparison anchors small-scale optimality; cpu_batch and the native kernel deliver family-median speed-ups of up to 24.4%; Stage 4 adaptive weights passed the six-gate review with 7 winning pairs.
2. **Methodological value**: independent review CLIs, hash chains, dual reruns, failure retention, the canonical artifact registry, the retention archive, resource guards, and transient-service reviews — together forming a traceable chain from raw evidence to readiness status, such that any claim can be replayed and re-verified by a third party.
3. **Honest boundaries**: BKS-incompatible gaps are not computed, no near-optimality is claimed for 100-customer instances, timeout overruns are explicitly recorded, and failed attempts are all retained — there are no whitewashed negative results.
4. **Open items**: the Stage 5.2 G Formal benchmark (external archive volume ready, root causes fixed), the README stage-narrative update, and restoration or deliberate-cleanup confirmation for the 17 deleted worktree documents.

---

*This report is based on HEAD (b4ac986) and direct worktree measurements; all cited file paths are relative to the repository root.*
