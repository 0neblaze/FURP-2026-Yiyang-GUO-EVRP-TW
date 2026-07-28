# 第 6 周：EVRP-TW 方法整合与批量评估

## 1. Current Progress（当前进度）

本周选择 **Track B：Combine Existing Methods Into One Workflow（将已有方法整合为统一工作流）**。

截至第 5 周，项目已经具备可复现的 Schneider benchmark（基准算例）读取、结构审计、
ALNS（Adaptive Large Neighbourhood Search，自适应大邻域搜索）、exact charging
subproblem（精确充电子问题）、小规模 Branch-Price-and-Cut（分支定价切割）对照、
OR-Tools/GA baselines（基线）和统一可行性验证器。因此，本周重点不是增加新的 RL
（Reinforcement Learning，强化学习）或 DL（Deep Learning，深度学习）模型，而是把
这些组件组织成一条可解释、可比较、可批量验证的研究流程。

选择 Track B 的原因如下：

- 当前方法已经能从实例输入运行到最终可行解和汇总表；
- 第 5 周已有足够的多实例、多规模和多随机种子结果；
- 主要问题已经从“能否运行”转为“组合方法是否比简单基线更可靠”；
- 在引入学习模型前，应先建立清晰的决策对象、可靠标签和可复现实验对照。

## 2. Method Design（方法设计）

### 2.1 统一工作流

```text
Schneider EVRP-TW instance
  -> instance parsing and structural audit
  -> ALNS customer assignment and ordering
  -> exact charging for each proposed customer sequence
  -> unified feasibility and objective validation
  -> comparison with BPC / OR-Tools / GA
  -> per-run records, failure records, and summary table
```

各组件的职责为：

1. **Instance audit（实例审计）**检查需求、时间窗、电池下界、充电节点和仓库时域，
   在运行算法前暴露结构问题。
2. **ALNS** 搜索客户分配和访问顺序，使用 destroy/repair operators（破坏/修复算子）
   改进候选解。
3. **Exact charging subproblem** 对固定客户序列求解充电站插入与完整充电决策，避免用
   贪心插站掩盖能量不可行。
4. **Unified validator（统一验证器）**独立检查容量、时间窗、电池、覆盖和目标值，
   invalid（无效）结果不会进入可行目标统计。
5. **Branch-Price-and-Cut** 为最多 8 个客户的实例提供小规模精确理论对照；超过其
   已验证能力时明确返回 `not_applicable`，不生成伪下界。
6. **OR-Tools VRPTW 和 GA VRPTW** 保留为透明基线，用于说明不包含精确充电优化的
   客户路线在 EVRP-TW 约束下会如何失败。

这种连接顺序把主问题搜索和充电子问题分离，同时让所有算法通过同一个验证器和结果
schema（数据结构）接受检查。比较时优先判断 feasibility（可行性），然后才比较可行解
的 objective value（目标值）、runtime（运行时间）和跨随机种子的稳定性。

### 2.2 简化伪代码

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

## 3. Experiment Plan（实验计划）

### 3.1 对照、范围和参数

- **Primary method（主方法）**：`ALNS_EXACT_CHARGING`。
- **Exact reference（精确对照）**：`BRANCH_PRICE_AND_CUT`，仅用于最多 8 个客户。
- **Baselines**：`OR_TOOLS_VRPTW` 和 `GA_VRPTW`。
- **Primary instances**：12 个 Schneider 实例，覆盖 C/R/RC 三类和
  5/10/15/100-customer 四种规模。
- **Stress instances（压力场景）**：3 个 5-customer 低电池场景。
- **总场景数**：15。
- **随机种子**：2014、2015、2016，用于 ALNS 和 GA。
- **停止条件**：ALNS 1000 iterations（迭代）且每次最多 30 秒；单线程。

### 3.2 记录指标

- feasibility rate（可行率）和 failure reason（失败原因）；
- objective value、best、mean、median、worst 和 standard deviation（标准差）；
- vehicle count、total distance 和 charging time；
- runtime、iterations、accepted/rejected moves；
- exact-charging calls；
- BPC lower bound、incumbent、optimality gap、nodes 和 generated columns。

### 3.3 改进判据和预期失败

组合方法满足以下条件时视为有价值：

- 在全部规模上稳定产生通过统一验证器的解；
- 在小规模实例上达到或接近 BPC 的 proven optimum（已证明最优值）；
- 相比不处理充电决策的基线显著提高可行率；
- 多个随机种子下保持稳定，而不是只展示单次最好结果。

预期失败包括：

- OR-Tools/GA 产生的纯 VRPTW 路线可能违反电池约束；
- BPC 在 8 个客户以上会因组合规模增长而返回 `not_applicable`；
- 100-customer 实例在 30 秒内可以得到可行解，但不能据此声称接近全局最优。

## 4. Preliminary Result（初步结果）

第 5 周批量实验已经为本周的组合工作流提供了可检查证据。数据时间范围为
2026-07-12 17:04:52 至 17:10:05 UTC，共 120 条记录。

| Algorithm | Runs | Feasible | Interpretation |
|---|---:|---:|---|
| ALNS_EXACT_CHARGING | 45 | 45 | 15 个场景全部通过，整体可行率 100% |
| BRANCH_PRICE_AND_CUT | 15 | 6 | 6 个适用的小规模场景全部可行且已证明最优；其余 9 个明确不适用 |
| GA_VRPTW | 45 | 6 | 整体可行率 13.3%，未集成精确充电 |
| OR_TOOLS_VRPTW | 15 | 0 | 所有输出均被统一验证器识别为 energy-invalid |

ALNS 在 Primary benchmark 的 5、10、15 和 100-customer 四种规模上分别完成
`9/9` 次可行运行，在三个 Stress 场景上也完成 `9/9` 次可行运行。小规模精确对照中，
ALNS 在 `c101C5`、`r105C5` 和 `rc105C5` 的最好结果均达到 BPC 证明的最优值。

这些结果支持以下结论：

- ALNS 与精确充电子问题的组合确实解决了纯 VRPTW 基线暴露出的能量可行性问题；
- 结果覆盖 15 个场景、4 种规模和 3 个随机种子，不依赖一两个简单样例；
- BPC 的作用是校验小规模质量，而不是被错误外推为中大规模求解器；
- 100-customer R/RC 结果仍有明显跨种子波动，后续应继续改进搜索稳定性和解质量。

## 5. Evidence Index（证据索引）

- [第 5 周 ALNS、精确充电与 BPC 方法说明](week05_alns_bpc_methodology.md)
- [第 5 周第二版技术周报](05_weekly_v2_alns_bpc_benchmark_rebuild.md)
- [120 条逐次实验结果](../experiments/summaries/week05_advanced_per_run_results.csv)
- [按实例和算法汇总的统计结果](../experiments/summaries/week05_advanced_summary_results.csv)
- [失败与不适用记录](../experiments/summaries/week05_advanced_failure_cases.csv)
- [Schneider 实例结构审计](../experiments/summaries/week05_advanced_instance_audits.csv)

## 6. Week 6 Direction（第 6 周后的项目方向）

当前项目方向确定为：继续使用 ALNS + exact charging 作为主方法，以 BPC 作为小规模
精确校验，并通过统一验证器与批量结果表评估可行性、质量、运行时间和稳定性。下一步应
优先改进 100-customer R/RC 实例的跨种子稳定性，并记录哪些 destroy/repair operators
在不同实例特征下有效。只有在积累了稳定、足量且定义清晰的决策数据后，才重新评估
bandit-style operator selection（多臂老虎机式算子选择）是否值得实现。
