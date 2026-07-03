# Week 4 Reading Notes

These notes are based on the local PDFs in
`/Users/guoyiyang/Documents/FURP-2026-EVRP-TW-Literature`. The PDFs are not
stored in Git.

## Keskin and Catay (2016)

Paper information:

- Title: *Partial recharge strategies for the electric vehicle routing problem with time windows*
- Journal: *Transportation Research Part C: Emerging Technologies*, 65, 111-127
- DOI: `10.1016/j.trc.2016.01.013`
- Local PDF checked: title page shows Elsevier, journal volume/pages, authors,
  article history, and DOI.

Problem setting:

- The paper extends EVRPTW by relaxing the full-recharge assumption.
- The partial recharge variant treats recharge amount as a decision, reducing
  unnecessary charging time when full recharge is not needed.

Method summary:

- The paper formulates the problem as a 0-1 mixed integer linear program and
  proposes ALNS, Adaptive Large Neighborhood Search.
- The ALNS framework destroys and repairs solutions using customer removal,
  customer insertion, station removal, and station insertion operators.
- The paper includes EVRP-specific station operations, such as removing stations
  alone or together with neighboring customers and inserting stations when
  recharging is necessary.

What is useful here:

- Week 4 borrows the idea that charging stations are not passive nodes; their
  placement needs explicit insertion logic.
- The current project does not yet implement partial recharge amounts, but it
  uses the paper's station-insertion motivation to improve from late repair to
  anticipatory repair.

Reproducibility reflection:

- Full ALNS is too large for this week because it requires adaptive operator
  scoring, destroy-repair neighborhoods, and parameter tuning.
- A smaller reproducible step is to isolate station insertion behavior and test
  it against the Week 3 repair baseline.

## Montoya et al. (2017)

Paper information:

- Title: *The electric vehicle routing problem with nonlinear charging function*
- Journal: *Transportation Research Part B: Methodological*, 103, 87-110
- DOI: `10.1016/j.trb.2017.02.004`
- Local PDF checked: metadata and title page show Elsevier, journal
  volume/pages, authors, keywords, and DOI.

Problem setting:

- The paper studies E-VRP with nonlinear charging functions.
- It argues that many E-VRP models assume a linear relation between charging
  time and battery level, while real charging is nonlinear.

Method summary:

- The paper introduces a piecewise-linear approximation of nonlinear charging
  behavior.
- It proposes a hybrid metaheuristic combining iterated local search and a
  charging-decision component.
- Its computational study compares nonlinear charging approximation against
  simpler linear approximations.

What is useful here:

- The Week 4 experiment keeps the repository's current linear charging model,
  but explicitly records this as a limitation.
- This matters because the local validator computes charging time from a simple
  inverse refueling rate. The result should not be interpreted as a realistic
  nonlinear charging model.

Reproducibility reflection:

- Implementing nonlinear charging would require changing the model, validator,
  metrics, and station data. That is not a safe Week 4 change.
- The practical next step is to keep the linear model stable and document the
  limitation before adding nonlinear charging later.

## Desaulniers et al. (2016)

Paper information:

- Title: *Exact Algorithms for Electric Vehicle-Routing Problems with Time Windows*
- Journal: *Operations Research*, 64(6), 1388-1405
- DOI: `10.1287/opre.2016.1535`
- Local PDF checked: JSTOR/INFORMS title page and article page show title,
  authors, journal, volume, issue, pages, publisher, stable URL, and DOI.

Problem setting:

- The paper studies four EVRPTW variants: single/full recharge,
  multiple/full recharge, single/partial recharge, and multiple/partial
  recharge.
- The distinction is directly relevant to this repository because the current
  validator allows multiple station visits but still assumes full recharge at
  station visits.

Method summary:

- The paper proposes exact branch-price-and-cut algorithms with customized
  mono-directional and bidirectional labeling algorithms.
- It reports that tailored resource extension functions and dominance rules are
  central to making exact solution practical on instances up to 100 customers.

What is useful here:

- The paper clarifies the modeling boundary of the current project: Week 4 is a
  multiple/full recharge heuristic experiment, not an exact algorithm and not a
  partial recharge model.
- It supports reporting full/partial and single/multiple recharge assumptions
  explicitly in future experiments.

Reproducibility reflection:

- Branch-price-and-cut is not appropriate for a quick Week 4 implementation.
- Its main value here is conceptual: it defines recharge variants cleanly and
  shows why energy feasibility should be embedded in route generation, not only
  repaired afterward.
