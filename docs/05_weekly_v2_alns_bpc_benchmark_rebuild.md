# 第 5 周周报第二版：EVRP-TW 主算法、精确充电、Branch-Price-and-Cut 与 Benchmark 体系重构

## 状态说明

- **已完成且已验证**：完整 Schneider 数据接入与 92 实例结构审计；精确充电子问题；
  ALNS 主算法；最多 8 客户的 BPC 与双向标号；统一验证器；覆盖 5/10/15/100 customers
  和 C/R/RC 三类的代表性 Primary 实验，以及电池 Stress 实验。
- **部分完成且已验证边界**：BPC 仅在 5-customer 正式实例运行，不支持中大规模。
- **尚未完成/尚未验证**：全部 92 个 Schneider 实例的完整多 seed 统计；partial/nonlinear
  charging；动态 ESPPRC pricing；固定车队规模和多目标权衡。

## 1. 本周目标与计划调整

原计划在 synthetic battery-60 failures（合成电池 60 失败案例）上继续预防性充电与路径
拆分。该方案可行率低，且无法区分实例生成缺陷、弱客户顺序和充电策略缺陷。因此保留原
周报与历史结果，但将主方法切换为 ALNS-based matheuristic + exact charging
subproblem，并引入小规模 Branch-Price-and-Cut 理论对照和原始 Schneider benchmark。

原 `docs/05_weekly.md` 未覆盖、未删除、未重命名；本文件是独立第二版。

## 2. Baseline 重新定位

| 方法 | 当前定位 | 完整 EVRP-TW 充电优化 | 当前验证状态 |
|---|---|---:|---|
| ALNS_EXACT_CHARGING | 主方法 | 是，full recharge 线性模型 | 已验证 |
| BRANCH_PRICE_AND_CUT | 小规模精确理论对照 | 是，最多 8 客户 | 已验证 |
| OR_TOOLS_VRPTW | 透明 classical baseline | 否 | 已验证其限制 |
| GA_VRPTW | weak baseline | 否，无精确插站 | 已验证其限制 |

OR-Tools 和 GA 的低可行率不能解释为软件失败：它们输出 VRPTW 客户路线后由同一 EVRP-TW
验证器检查，能量违反会被诚实标记为 `invalid`。

## 3. 方法与数学模型

主问题、充电子问题、ALNS 算子、BPC 集合划分模型、fleet lower-bound cut、双向标号、
支配规则和统一验证公式详见 `docs/week05_alns_bpc_methodology.md`。代码与文档共同采用：

\[
b_j=b_i-rd_{ij},\quad
t_j=\max(a_j,t_i+d_{ij}/v),\quad
h_j=g(Q-b_j)\text{ at a station}.
\]

关键接口为：

- `solve_exact_charging(instance, customer_order)`：固定客户序列到完整可行路径；
- `solve_alns(instance, seed, ...)`：客户分配/顺序搜索并调用精确充电；
- `solve_branch_price_and_cut(instance, ...)`：小规模精确对照；
- `validate_routes(instance, routes, claimed_objective=...)`：算法无关验证。

## 4. Schneider Benchmark 与结构审计

下载的公开镜像内容保存在 Git-ignored `data/schneider/`，包含 92 个实例和 SHA-256 清单。
全部 92 个实例通过客户需求、时间窗最早到达、仓库时域、进出充电节点、电池单段下界和
客户级结构下界检查。完整逐实例表在
`experiments/summaries/schneider_instance_catalog.csv`。

### 4.1 本轮实例与最低合理电池容量

| Benchmark | Instance | Customers | Stations | Q | B_lb | B_struct | Q/B_struct | Audit |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Primary | c101C5 | 5 | 3 | 77.750 | 29.732 | 59.464 | 1.308 | pass |
| Primary | r105C5 | 5 | 3 | 60.630 | 27.785 | 55.570 | 1.091 | pass |
| Primary | rc105C5 | 5 | 4 | 77.750 | 19.925 | 39.850 | 1.951 | pass |
| Stress | c101C5 battery | 5 | 3 | 62.437 | 29.732 | 59.464 | 1.050 | pass |
| Stress | r105C5 battery | 5 | 3 | 58.348 | 27.785 | 55.570 | 1.050 | pass |
| Stress | rc105C5 battery | 5 | 4 | 41.842 | 19.925 | 39.850 | 1.050 | pass |

Primary 保持原始参数；Stress 只把电池设为 `1.05 B_struct`，未修改坐标、需求、站点或
时间窗。这个压力场景仍通过必要结构检查，但结构检查不等同于完整路线存在性证明。

## 5. 环境与实验设置

| 项目 | 实际值 |
|---|---|
| 运行时间范围 (UTC) | 2026-07-12 17:04:52.038179 至 17:10:05.012464 |
| OS / CPU | macOS 27.0 arm64 / Apple M5, 10 logical CPUs |
| RAM / GPU | 16 GiB / 未使用 GPU |
| Python / C++ compiler | CPython 3.13.13 / Apple clang 17.0.0 |
| LP backend | SciPy 1.17.1 + HiGHS 1.14.0 |
| 其他 solver | OR-Tools 9.15.6755；Gurobi 13.0.2；CPLEX 22.2.0.0 |
| Threads / wall limit | 1 / 30 s per run |
| Random seeds | 2014, 2015, 2016 |
| ALNS / GA | 1000 iterations / population 60, generations 80 |
| 安装命令 | `uv sync --all-groups` |

完整依赖、工具版本、命令和环境变量见 `results/week05_advanced/environment.json`。
Gurobi/CPLEX 已配置但本轮 BPC restricted master 使用开源 HiGHS，GPU 未参与。

## 6. 实验结果

### 6.1 Primary 按规模可行率

| Size | Method | Feasible / Runs | Feasibility rate | Mean runtime (s) |
|---:|---|---:|---:|---:|
| 5 | ALNS_EXACT_CHARGING | 9 / 9 | 100.0% | 0.0157 |
| 5 | BRANCH_PRICE_AND_CUT | 3 / 3 | 100.0% | 0.0472 |
| 5 | OR_TOOLS_VRPTW | 0 / 3 | 0.0% | 0.0027 |
| 5 | GA_VRPTW | 3 / 9 | 33.3% | 0.0993 |
| 10 | ALNS_EXACT_CHARGING | 9 / 9 | 100.0% | 0.4028 |
| 10 | BRANCH_PRICE_AND_CUT | 0 / 3 (`not_applicable`) | N/A | 0.0000 |
| 10 | OR_TOOLS_VRPTW | 0 / 3 | 0.0% | 0.0027 |
| 10 | GA_VRPTW | 3 / 9 | 33.3% | 0.1682 |
| 15 | ALNS_EXACT_CHARGING | 9 / 9 | 100.0% | 1.2211 |
| 15 | BRANCH_PRICE_AND_CUT | 0 / 3 (`not_applicable`) | N/A | 0.0000 |
| 15 | OR_TOOLS_VRPTW | 0 / 3 | 0.0% | 0.0049 |
| 15 | GA_VRPTW | 0 / 9 | 0.0% | 0.2498 |
| 100 | ALNS_EXACT_CHARGING | 9 / 9 | 100.0% | 30.0127 |
| 100 | BRANCH_PRICE_AND_CUT | 0 / 3 (`not_applicable`) | N/A | 0.0000 |
| 100 | OR_TOOLS_VRPTW | 0 / 3 | 0.0% | 0.1808 |
| 100 | GA_VRPTW | 0 / 9 | 0.0% | 2.2243 |

Stress 的 ALNS 为 9/9、BPC 为 3/3 可行；OR-Tools 为 0/3、GA 为 0/9。平均运行时间
依次为 0.0135、0.0347、0.0015 和 0.0976 秒。

### 6.2 Primary ALNS 多次运行统计

| Instance | Best | Mean | Median | Worst | Std | Feasible | Gap to proven optimum |
|---|---:|---:|---:|---:|---:|---:|---:|
| c101C5 | 247.1497 | 247.1497 | 247.1497 | 247.1497 | 0.0000 | 3/3 | 0.0% |
| r105C5 | 156.0821 | 156.0821 | 156.0821 | 156.0821 | 0.0000 | 3/3 | 0.0% |
| rc105C5 | 238.0522 | 239.1336 | 238.0522 | 241.2964 | 1.5293 | 3/3 | best 0.0% |

### 6.3 BPC 精确统计

| Benchmark | Instance | Root LB | Incumbent | Final LB | Gap | Nodes | Columns | Joined labels |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Primary | c101C5 | 247.1497 | 247.1497 | 247.1497 | 0% | 1 | 17 | 610 |
| Primary | r105C5 | 156.0821 | 156.0821 | 156.0821 | 0% | 1 | 16 | 610 |
| Primary | rc105C5 | 231.1586 | 238.0522 | 238.0522 | 0% | 9 | 18 | 610 |
| Stress | c101C5 | 250.0380 | 250.0380 | 250.0380 | 0% | 1 | 14 | 610 |
| Stress | r105C5 | 156.0821 | 156.0821 | 156.0821 | 0% | 1 | 16 | 610 |
| Stress | rc105C5 | 265.0945 | 265.0945 | 265.0945 | 0% | 1 | 13 | 610 |

### 6.4 100-customer ALNS 结果

| Instance | Seed | Objective | Vehicles | Feasible | Runtime (s) |
|---|---:|---:|---:|---|---:|
| c101_21 | 2014 | 1234.5033 | 14 | yes | 30.045 |
| c101_21 | 2015 | 1237.1389 | 14 | yes | 30.018 |
| c101_21 | 2016 | 1237.1389 | 14 | yes | 30.005 |
| r101_21 | 2014 | 1816.6087 | 23 | yes | 30.003 |
| r101_21 | 2015 | 1788.2156 | 22 | yes | 30.002 |
| r101_21 | 2016 | 2091.7771 | 28 | yes | 30.004 |
| rc101_21 | 2014 | 2167.8629 | 24 | yes | 30.025 |
| rc101_21 | 2015 | 2230.9209 | 25 | yes | 30.004 |
| rc101_21 | 2016 | 2271.0743 | 25 | yes | 30.008 |

大规模结果证明当前实现能稳定找到可行解，但 R/RC 的车辆数和 objective 尚无精确 gap，
不能据此声称接近最优。BPC 超过 8 客户时不运行，也不产生伪下界。

逐次 ALNS 算子调用、成功、权重、接受统计和精确充电调用时间保存在 per-run CSV 的 JSON
字段及对应 raw logs；不在周报中手工转录 18 组嵌套统计，避免形成第二事实来源。

## 7. 异常、失败与修复

| 类型 | 观察 | 处理 | 当前状态 |
|---|---|---|---|
| invalid baseline | OR-Tools 所有运行出现 energy violations | 保留结果，不计入可行目标均值 | 已验证 |
| weak GA | Primary 仅 c101C5 可行；Stress 全部 invalid | 保留失败并降级为 weak baseline | 已验证 |
| BPC optimality defect | 初版 rc105C5 错报 241.8894 为最优，但 ALNS 为 238.0522 | 定位为列变量分支遗漏零约化成本整数列；分支节点改用完整小规模列池 | 已修复、回归验证 |
| scale limit | 穷举列池随客户数阶乘增长 | `max_customers=8` fail fast | 已验证限制 |

所有失败明细位于 `experiments/summaries/week05_advanced_failure_cases.csv`，没有删除 timeout、
invalid 或 error 记录。本轮没有 timeout/error。

## 8. 新增与修改文件

新增核心文件：`src/evrptw/benchmark.py`、`charging.py`、`alns.py`、`bpc.py`、
`experiments/week05_advanced_benchmark.py` 及对应测试。修改 `validation.py`、`pyproject.toml`、
`README.md`。新增审阅 CSV、本文和 `docs/week05_alns_bpc_methodology.md`。历史 Week 5
路径拆分代码、日志和原周报均保留。

## 9. 当前限制与下一阶段计划

1. **下一阶段任务 1**：在 10/15-customer Schneider 实例运行 ALNS 多 seed，并实现动态
   bidirectional ESPPRC pricing，逐步将精确对照从 5 扩至 10 客户。
2. **下一阶段任务 2**：在预先声明的 100-customer C/R/RC 子集使用统一 30/60/300 s
   wall-clock budget，报告可行率、稳定性、车辆数和 gap；不把本周小规模 100% 可行率
   外推为大规模结论。

## 10. Revision Log

| 日期时间 (UTC) | 文件 | 修改 | 原因 | 影响 | 验证 | 状态 |
|---|---|---|---|---|---|---|
| 2026-07-12 16:35 | benchmark/charging modules | 新增实例审计、电池界与精确充电 | 修复任意电池和贪心插站问题 | 实例准入、路线可行性 | 单元测试与 92 实例审计 | 完成 |
| 2026-07-12 16:39 | ALNS/BPC modules | 主方法和精确对照重构 | 替换弱 GA 主方法 | 算法与理论对照 | toy + Schneider c101C5 | 完成 |
| 2026-07-12 16:44 | BPC branching | 分支节点启用完整小规模列池 | 修复错误最优性声明 | BPC bounds/incumbent | rc105C5 238.0522, gap 0 | 完成 |
| 2026-07-12 17:04 | experiment/results | 重跑 120 条正式记录并统一 GA 墙钟上限 | 覆盖 5/10/15/100 customers 并保证公平停止条件 | 全部正式表 | validator + raw logs + summary recomputation | 完成 |
| 2026-07-12 16:50 | 本周报与方法文档 | 新增第二版，不覆盖原报告 | 记录算法和 benchmark 重构 | 文档与复现入口 | 路径/CSV/命令核对 | 完成 |

## 11. 数据索引

| 数据 | 路径 |
|---|---|
| 92 实例目录审计 | `experiments/summaries/schneider_instance_catalog.csv` |
| 本轮实例审计 | `experiments/summaries/week05_advanced_instance_audits.csv` |
| 120 条逐次结果 | `experiments/summaries/week05_advanced_per_run_results.csv` |
| 汇总统计 | `experiments/summaries/week05_advanced_summary_results.csv` |
| 失败/无效解 | `experiments/summaries/week05_advanced_failure_cases.csv` |
| 原始日志和 solution | `results/week05_advanced/raw/`、`results/week05_advanced/solutions/` |
