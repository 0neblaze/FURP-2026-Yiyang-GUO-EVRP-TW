# EVRPTW Publication Landscape and Q1/Q2 Threshold Survey (2023–2026)

Survey date: 2026-07-27

## 1. Scope and quartile conventions

This document answers only questions about the external literature and journal
thresholds; it does not judge whether this repository's current code and
experiments already meet those thresholds.

"Q1/Q2" has several non-equivalent conventions, including the JCR quartile, the
SJR quartile, and the Chinese Academy of Sciences journal ranking. The publicly
verifiable convention used here is **2024 SJR** or the **2024 JCR** quartiles
published on journal websites; these must not be equated directly with the CAS
ranking. Re-check against the school's official assessment convention of the
submission year.

## 2. External conclusions

### 2.1 The field is already quite crowded

Merely implementing a working EVRPTW solver, adding a few destroy/repair
operators, introducing adaptive weights, or parallelising existing candidate
evaluation is usually not enough to form the core contribution of a Q1/Q2 paper.

Direct evidence is Voigt's systematic study of the 2006–2023 literature: it
analysed **211** ALNS-based VRP papers, uniformly identifying **57 removal
operators and 42 insertion operators**; sequence-based removal and regret
insertion with foresight are already established high-performance designs.
Therefore, "we also implemented ALNS with several common operators" is not a
scarce contribution. [EJOR paper](https://doi.org/10.1016/j.ejor.2024.05.033)

### 2.2 Strong recent papers usually occupy at least two contribution dimensions

Common combinations:

1. **New problem mechanism + new algorithm**: e.g. time-dependent travel and
   discharge, heterogeneous nonlinear charging, capacitated charging stations.
2. **New algorithmic mechanism + provable/verifiable properties**: e.g. new
   bidirectional labeling, dominance rules, branching, safe preprocessing.
3. **New algorithm + strong computational evidence**: complete public
   benchmarks, exact comparisons, multi-scale instances, ablations, statistical
   inference, and new BKS/optimal solutions.
4. **Software/data contribution + long-term reproduction value**: not just
   uploading code, but stable APIs, documentation, tests, licences, pinned
   version snapshots, and rerunnable results.

### 2.3 "Large engineering effort" and "strong academic novelty" are different things

High-quality logs, manifests, hashes, independent replay, deadline safety, and
parallel consistency significantly strengthen credibility, but reviewers will
still ask:

- What is the new scientific question?
- Why does the new method work compared with the strongest recent methods?
- Can the contribution transfer beyond this repository's problem or solver?
- Does it produce better solutions, faster equivalent solutions, or new
  modelling/managerial insight?
- Do the performance gains hold under the same objective, the same workload,
  and the same hardware constraints?

These questions must be answered by the paper's research design; they cannot be
replaced by the sheer volume of engineering evidence.

## 3. Representative frontier, 2023–2026

| Year | Paper and venue | Core innovation | Data scale and comparison | Implication for submission thresholds |
|---|---|---|---|---|
| 2023 | Bruglieri, Paolucci & Pisacane, *Computers & Operations Research*, [DOI](https://doi.org/10.1016/j.cor.2023.106261), [author institutional copy](https://re.public.polimi.it/bitstream/11311/1260037/1/Bruglieri_Paolucci_Pisacane_CAOR2023_Matheuristic_EVRP.pdf) | First to let speed and load jointly enter the energy consumption rate; cloneless MILP and a Random Kernel Search matheuristic | Schneider/Solomon-derived instances; 12 25-customer and 30 100-customer instances; MILP vs matheuristic; **15 runs** per stochastic instance with sample size from 90% confidence and 0.1% margin of error, plus the Friedman test | Strong papers put the realistic energy model, the mathematical model, the algorithm, and the statistical design into one contribution chain |
| 2023 | Rastani & Çatay, *Annals of Operations Research*, [DOI](https://doi.org/10.1007/s10479-021-04320-9), [institutional entry](https://research.sabanciuniv.edu/id/eprint/47761/) | Load-dependent EVRPTW; two mathematical models; optimal repair embedded in an LNS matheuristic | Small instances verified by a commercial solver, large instances for LNS; further analysis of how ignoring load affects fleet size and route feasibility | Beyond algorithmic results, papers must answer the decision impact of model factors |
| 2024 | Lera-Romero, Miranda-Bront & Soulignac, *European Journal of Operational Research*, [DOI](https://doi.org/10.1016/j.ejor.2023.06.037), [public preprint](https://optimization-online.org/wp-content/uploads/2020/09/8026.pdf) | Jointly models time-dependent travel time and speed-dependent battery consumption; unified variable waiting/charging times; new BCP, piecewise-linear resource labels, partial dominance, and preprocessing | Extends the Desaulniers/Schneider benchmarks; up to 100 customers; reports **13 new optimal solutions**; analyses infeasibility from ignoring time-dependent speeds — up to 40% of some scenarios from exceeding battery capacity | Q1 methodology papers usually extend the model and substantively advance the exact algorithm itself |
| 2024 | Klein & Schiffer, *INFORMS Journal on Computing*, [paper](https://doi.org/10.1287/ijoc.2023.0104), [development repo](https://github.com/tumBAIS/RoutingBlocks), [journal pinned snapshot](https://github.com/INFORMSJoC/2023.0104) | RoutingBlocks: a modular Python/C++ algorithm framework for VRPs with intermediate stops; provides ALNS, local search, move caches, and an EVRPTW partial-recharge example | Software, data, results, documentation, licence, and fixed SHA snapshots public; the journal repository has its own DOI | The competitive bar for software papers is not "code is available" but "reusable, maintainable, verifiable, and of community value" |
| 2024 | Zhou et al., *Journal of Cleaner Production*, [DOI](https://doi.org/10.1016/j.jclepro.2023.140188) | Time-dependent EV routing and scheduling; MILP + VNS with a partial model allowing waiting to be scheduled at nodes or on arcs during congestion | Large instances reach **200 customers**; reports **11 new BKS** across 56 related EVRPTW benchmarks; plus a case study and sensitivity analysis | Reproducing experiments only on small 100-customer ranges is no longer a scale advantage; practical insight can markedly improve fit with transportation/sustainability venues |
| 2025 | Voigt, *European Journal of Operational Research*, [DOI](https://doi.org/10.1016/j.ejor.2024.05.033) | Network meta-analysis of 211 ALNS-VRP papers; operator taxonomy, rankings, and future experiment guidance | 57 removal and 42 insertion operators; sequence removal and regret-style insertion rank at the top | New ALNS papers must prove the independent value of problem-specific operators with ablation and statistical evidence |
| 2025 | Nafstad, Desaulniers & Stålhane, *Transportation Science*, [paper and open copy](https://doi.org/10.1287/trsc.2024.0725) | E-VRPTW with heterogeneous technologies and nonlinear charging; the full time–SoC trade-off embedded in exact pricing; bidirectional labeling outperforms unidirectional | New benchmarks at 25/50/100 customers, 21 stations, three charging technologies; compared with existing E-VRPTW-L and E-VRP-NL exact methods; up to 100 customers solvable within an hour, 24 newly proven-optimal instances versus the E-VRP-NL comparison | The "exact charging" frontier has reached heterogeneity, nonlinearity, bidirectional labeling, and full BPC; a linear/full-recharge route evaluator is by itself hard to sell as a modelling innovation |
| 2025 | Bruglieri et al., *International Transactions in Operational Research*, [DOI](https://doi.org/10.1111/itor.70104) | EVRPTW with capacitated recharging stations; partial recharge; MILP-based ALNS; handles linear and piecewise-linear charging simultaneously | Compared with the state-of-the-art exact algorithm on public benchmarks | Charging-station resource conflicts and partial charging are already within the direct comparison scope of recent matheuristics |
| 2026 | Rastani et al., *European Journal of Operational Research*, [DOI](https://doi.org/10.1016/j.ejor.2026.01.020), [institutional abstract](https://research.sabanciuniv.edu/id/eprint/53686/) | Jointly handles road gradients, load dynamics, and regenerative braking; four mathematical models | Generates new datasets with elevation from the benchmarks, comparing three terrain classes and analysing feasibility and route changes | Realistic energy-consumption research is advancing from fixed distance-based rates to gradients, load, and energy recovery |
| 2026 | Bacci, Gentile & Pizzari, *Optimization Letters*, [open copy](https://doi.org/10.1007/s11590-026-02319-4) | Exact perspective-cut linearisation for nonlinear charging, with preprocessing of dominated charging paths | Compared with existing piecewise-linear/path formulations | Even for a more focused optimisation venue, a clear mathematical methodological innovation is still required — not just implementation tuning |

## 4. Common experimental standards of recent work

These are not explicit "minimum terms" of any journal, but the de facto standards
reflected by representative papers.

### 4.1 Benchmark coverage

- Small instances for exact validation: MILP/CPLEX/Gurobi or an exact algorithm
  should provide optimum/bound.
- Large instances for heuristic performance: not just one family or a few
  convenient instances.
- Schneider/Solomon-derived 5/10/15/25/50/100-customer instances remain common,
  but 2024 papers already reach 200 customers; larger scale is not automatically
  novel, yet is one necessary piece of evidence for algorithmic scalability.
  [Zhou et al.](https://doi.org/10.1016/j.jclepro.2023.140188)
- If the objective or charging model differs from the original benchmark,
  incompatible gap comparisons must be explicitly blocked, or a verified new
  baseline established; numbers under different objectives must not be reported
  as progress.

### 4.2 Baselines

A paper whose main contribution is a solving algorithm typically needs at least
three classes of comparison:

1. the original/classical published baseline;
2. a recent state of the art or public implementation;
3. controlled ablations of one's own method, e.g.:
   - adaptive vs fixed weights;
   - new operator on/off;
   - cache/screening/batching/parallel each on/off;
   - serial vs parallel under the same candidate order and the same work budget.

RoutingBlocks has published high-performance Python/C++ ALNS components and an
EVRPTW partial-recharge example, so it must at least be discussed; if the
problem definition is compatible, it should serve as an implementation/efficiency
reference. [Paper](https://doi.org/10.1287/ijoc.2023.0104); [code](https://github.com/tumBAIS/RoutingBlocks)

### 4.3 Randomised evaluation

- Three seeds suit regression/evidence gates but usually cannot stably estimate
  the mean, variance, and tail behaviour of a stochastic metaheuristic.
- A representative COR paper computed its sample size from 90% confidence and a
  0.1% margin of error, ending at 15 runs per instance with the Friedman
  non-parametric test. [Public paper, Section 6](https://re.public.polimi.it/bitstream/11311/1260037/1/Bruglieri_Paolucci_Pisacane_CAOR2023_Matheuristic_EVRP.pdf)
- An actual paper should pre-state whether the sampling unit is the instance,
  the instance-seed, or the family; report median/mean, dispersion, confidence
  intervals, effect sizes, and paired tests — not just "how many wins".
- Multi-algorithm/multi-parameter comparisons need multiple-comparison control
  or an omnibus test; do not cherry-pick the best results from many
  seeds/instances after the fact.

### 4.4 Performance protocol

- Wall-clock comparisons must record CPU, threads, memory, compiler, and solver
  versions.
- Parallel algorithms should report:
  - fixed-work quality;
  - fixed-time quality;
  - speedup and parallel efficiency;
  - 1/2/4/8 worker scaling, if the hardware allows;
  - deterministic equivalence or the stochastic differences parallelism
    introduces.
- Advantages from stronger hardware, more exact calls, pre-warmed caches, or
  different deadline semantics must not be attributed to the algorithm.
- "Four workers are faster" is just a result; a publishable contribution must
  further explain a transferable batching/scheduling/transaction design,
  ideally with complexity, correctness invariants, or a sufficiently general
  algorithmic framework.

### 4.5 Reproducibility

IJOC explicitly requires a software/data archive; its Software Tools area
separately reviews software quality/maintainability and paper
novelty/community value. [IJOC editorial statement](https://pubsonline.informs.org/page/ijoc/editorial-statement); [submission guidelines](https://pubsonline.informs.org/page/ijoc/submission-guidelines)

A competitive reproduction package should include at least:

- a pinned commit/tag and an open-source licence;
- one-command generation of tables/figures from the raw instances;
- an environment lockfile/container;
- raw per-run results, not just summary CSVs;
- a validator and objective recomputation;
- seed, time/work budget, hardware, thread, and solver metadata;
- explicit handling of failed/timed-out runs;
- artifact checksums;
- expected runtimes and a minimal reproduction experiment stated in the README.

The RoutingBlocks IJOC pinned repository contains `data/`, `results/`, `src/`,
documentation, a licence, CITATION, and an SHA-pinned journal snapshot — a
directly usable public example. [Journal code snapshot](https://github.com/INFORMSJoC/2023.0104)

## 5. Candidate journals and actual fit

### 5.1 Quartile reminder

In 2024 SJR, the main candidates below are all Q1: Transportation Science,
Transportation Research Part E, European Journal of Operational Research,
Computers & Operations Research, and INFORMS Journal on Computing. The public
SJR values are roughly 2.324, 2.513, 2.239, 1.605, and 1.439 respectively;
quartiles shift with year and subject category. [2024 SJR table for Transportation/OR](https://kniznica.umb.sk/app/cmsFile.php?ID=22055&disposition=i); [2024 SJR table for Computing/OR](https://kniznica.umb.sk/app/cmsFile.php?ID=21759&disposition=i); [EJOR SCImago page](https://www.scimagojr.com/journalsearch.php?q=22489&tip=sid)

The public 2024 JCR convention may differ — for example, Optimization Letters
is Q2 there; this again shows that submissions must state which quartile
convention they use. [Springer journal page](https://link.springer.com/journal/11590); [public JCR summary](https://journalsimpactfactors.com/journal.php?id=13121)

### 5.2 Journal gradient

| Target | Journal scope and suitable manuscripts | Actual threshold for the current topic |
|---|---|---|
| Stretch Q1 | **Transportation Science**: flagship transportation analysis; the Logistics & Routing area requires exciting new modelling/methodology and new scientific knowledge; data-driven/real-time routing encouraged. [Official scope](https://pubsonline.informs.org/page/trsc/editorial-statement) | Requires a clear new problem or transferable algorithmic innovation; ALNS tuning, caching, and single-machine parallel speedups alone are easily judged contribution-insufficient at desk review |
| Stretch Q1 | **EJOR**: high-quality original OR methodology or innovative applications. [Official scope](https://www.sciencedirect.com/journal/european-journal-of-operational-research) | Requires methodological depth, strong state-of-the-art comparisons, new optima/BKS, or explanatory decision insight; recent same-topic papers include time-dependent BCP, an ALNS operator meta-analysis, and gradients/load/regenerative braking |
| Stretch Q1 | **Transportation Research Part C / E**: Part C emphasises the impact of emerging technology on transport systems and open big data; Part E emphasises logistics and accepts broad OR/AI methods. [Part C scope](https://www.sciencedirect.com/journal/transportation-research-part-c-emerging-technologies); [Part E scope](https://www.sciencedirect.com/journal/transportation-research-part-e-logistics-and-transportation-review) | A pure benchmark algorithm paper is often not enough; realistic transport/logistics mechanisms, case studies, or transferable managerial insight are needed |
| Strong Q1 | **Computers & Operations Research**: the combination of OR theory/practice and advanced computational methodology, explicitly covering transportation/logistics. [Official scope](https://www.sciencedirect.com/journal/computers-and-operations-research) | The most natural home for a "deadline-safe exact evaluator + batching/cache/screening + rigorous benchmark" computational-methods paper, but the engineering mechanisms must be elevated into general algorithmic contributions with full ablations and statistics |
| Strong Q1 / software route | **INFORMS Journal on Computing**: requires a significant computing contribution; the Software Tools area requires long-term software usefulness and open licences, and reviews software and paper separately. [Official scope](https://pubsonline.informs.org/page/ijoc/editorial-statement) | Claiming a solver/framework contribution requires RoutingBlocks-level modularity, documentation, stable APIs, maintainability, and a public archive; a single-project experimental codebase is a weak fit |
| Broad OR candidate | **Annals of Operations Research / International Transactions in Operational Research**: both recently published EVRPTW LNS/matheuristics directly; ITOR emphasises bridges between theory and application and between academia and practice. [ITOR official scope](https://onlinelibrary.wiley.com/page/journal/14753995/homepage/productinformation.html) | Better suited than Transportation Science for "new variant + solid matheuristic", but still needs an independent new problem setting, complete models, strong comparisons, and insight |
| Focused Q2 example | **Optimization Letters**: covers optimisation theory, algorithms, computational studies, and applications; recently published perspective cuts for nonlinear charging. [Journal scope](https://link.springer.com/journal/11590); [2026 EVRP paper](https://doi.org/10.1007/s11590-026-02319-4) | Suits a sharply bounded, compact contribution with mathematical/algorithmic novelty in exact charging or preprocessing; not for stuffing a large staged engineering record into one article |

## 6. Three viable paper routes

These routes are research-design suggestions derived from the external
literature; they do not imply the repository already has the corresponding
contributions.

### Route A: computational-methods paper (closest to the current technical topic)

Possible central question:

> How can exact charging route evaluation be safely batched, cached, and
> parallelised under strict deadline/work-budget semantics, while preserving
> candidate transaction atomicity, objective consistency, and
> reproducibility?

Must be completed:

1. Abstract the evaluator into an independent, reusable problem and API, not
   an ALNS-internal optimisation detail.
2. State correctness invariants: started/completed/interrupted calls, cache
   commits, deadline boundaries, candidate atomicity.
3. Compare with naive scalar, existing exact route charging/scheduling
   methods, and a compatible RoutingBlocks path.
4. Dual fixed-work and fixed-time axes; multi-worker scaling; independent
   repetitions; confidence intervals and paired tests.
5. On a fully compatible benchmark, demonstrate:
   - equivalent objective/feasibility;
   - statistically significant and practically sized wall-clock or
     effective-search improvements;
   - no regression in final solution quality.
6. Discuss extension to partial/nonlinear/heterogeneous charging; if only
   full linear charging is supported, state the limitation clearly.

Natural venue: COR; if it grows into general open software with a long-term
maintenance route, IJOC becomes possible.

### Route B: new EVRPTW model + matheuristic/exact hybrid

Choose a mechanism not already directly covered by the recent literature and
with practical significance, e.g.:

- charging station capacity + queue uncertainty;
- heterogeneous nonlinear charging + load/gradient;
- battery degradation;
- dynamic requests + robust/stochastic energy.

Must be completed:

1. Complete mathematical definition and objective compatibility.
2. Exact verification on small instances.
3. A new benchmark or an auditable public benchmark extension.
4. Comparison with the most recent same-variant algorithms, not only
   Schneider 2014.
5. Parameter/mechanism sensitivity analysis and managerial insights.

Natural venue: AOR/ITOR/COR; with a very strong model and insight,
EJOR/TR-C/TR-E/Transportation Science become a stretch.

### Route C: open-software/reproduction-infrastructure paper

The central contribution must be a community tool, not "this project's code made
public":

- a stable, documented EVRPTW research framework;
- pluggable charging oracle, objective, validator, and ALNS operators;
- a benchmark registry and one-command experiment reproduction;
- a Python API + performance-critical native backend;
- third-party extensible examples, tests, versioned data/results, and a
  long-term maintenance plan.

The non-duplicative value relative to RoutingBlocks must be stated directly,
e.g.:

- deadline-transaction semantics;
- formal evidence/replay;
- heterogeneous exact charging backends;
- benchmark provenance/audit;
- cross-platform reproducibility.

Natural venue: IJOC Software Tools; but this is a high-bar route competing
head-on with mature public packages.

## 7. A quantifiable submission-readiness checklist

This is not an official journal score; it is an internal gate to avoid
"feels about right".

### Minimum suggestions for Q2 / broad strong OR venues

- [ ] One central research question stateable in a sentence, not directly
  covered by recent papers
- [ ] At least one model- or algorithm-level primary contribution, not a pure
  engineering rebuild
- [ ] Exact validation on small instances; large instances covering the main
  benchmark families
- [ ] At least 2 external baselines + a complete self-ablation matrix
- [ ] Justified repetition counts for randomised algorithms; at minimum CIs,
  effect sizes, paired non-parametric tests
- [ ] Fully compatible objective/model; no misleading gaps computed when
  incompatible
- [ ] A rerunnable artifact package, pinned versions, licence, raw per-run
  results
- [ ] Limitations, failures, and negative results honestly reported

If the central question or the primary contribution is missing, no amount of
engineering quality constitutes submission readiness. If more than two other
items are missing, the work is usually still at the research-prototype /
experimental-infrastructure stage.

### Additional suggestions for strong Q1 methods/transportation venues

- [ ] Item-by-item comparison with the strongest similar methods of the last
  3 years, not just classical citations
- [ ] At least one provable property, general algorithmic mechanism, new
  optimum/BKS, or modelling insight not replaceable by a simple
  implementation
- [ ] Multi-scale, multi-family, full-scope results not relying on a few
  seeds/instances
- [ ] Practical/managerial interpretation, or a method clearly transferable to
  other problems
- [ ] Every headline claim backed by statistical and reproduction experiments

Q1 is not "the Q2 checklist with more instances". The biggest additional
distance is usually **contribution sharpness and generality**; experimental
scale comes second.

## 8. Necessary convergence in paper writing

The final manuscript must not be organised along the Stage 0–5 development
timeline. A better paper structure:

1. one research question;
2. one precise problem definition;
3. 2–3 verifiable contributions;
4. methods with correctness/complexity;
5. experimental questions and a pre-registered-style protocol;
6. results, ablations, statistics, and managerial/algorithmic insight;
7. limitations and next steps.

Stage registries, manifests, review gates, and raw traces belong in the
supplement/artifact as the reproducibility backbone — they do not replace the
paper's scientific narrative.

## 9. Final judgement framework

Based only on external field thresholds:

- a rigorous, reproducible EVRPTW ALNS engineering effort **has value as a
  paper's experimental platform**;
- but "completed many solver stages, operators, caches, parallelism, and
  evidence gates" does not by itself demonstrate Q1/Q2 readiness;
- the shortest publication path is usually to distil **one generalised
  algorithmic question** from the existing work, then strengthen recent
  external baselines, statistical experiments, and a compatible benchmark;
- without a new central research question, the distance to Q1/Q2 is not "run
  20% more experiments" — it is the missing core contribution;
- if a transferable deadline-safe/batched exact-evaluation method already
  exists, the remaining distance is more likely: theorisation, external
  comparisons, the full benchmark, statistical inference, and a public
  reproduction package.

For "how much is done and how much is missing" in this specific repository,
map this checklist item by item against the current implementation, formal
results, failure evidence, and model boundaries before scoring.
