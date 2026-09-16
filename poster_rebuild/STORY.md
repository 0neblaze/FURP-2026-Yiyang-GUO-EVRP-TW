# STORY.md — FURP Showcase Poster v2（重构版）

## 叙事目标
以 SSCI2024_AMR 范例的叙事骨架（Motivation → Method → Experiment → Results → Honest claims）承载现有海报的全部内容，套用 Poster Template 的精准版式。核心 selling point 不变：**Audit-first ALNS，−12.6% 车队规模，零回归**。

## 叙事流（观看顺序）
1. **Header**：标题直接给出结论（−12.6% vehicles, zero regressions）+ 作者/系所。
2. **Motivation**（左上）：问题（E-VRPTW）→ 挑战（字典序目标、车队优先）→ 空白（BKS 不兼容、缺独立审计）→ Objective 一句话 → Fig1 问题示意。
3. **Method Overview**（右上，视觉锚点）：Fig2 ALNS Engine 主图 + 右列 4 条机制要点。
4. **Experimental Settings**（左中）：Fig3 审计协议图 + 一行实验参数（12×3 seeds · 30s · 1000 iters · Stage 0 hash-verified）。
5. **Key Results**（右中）：Fig4 车队质量图 + 一行结论（87→76 · −5.1% distance · 36/36 feasible）。
6. **Key Quantitative Highlights**（左下）：Fig5 充电运行时图 + 一行结论（−22.0% CPU，audit 后设为默认）。
7. **Why It Works & Honest Audit**（右下）：4 条机制 ✓ + 3 条诚实边界 ▲ + References + QR（代码与证据）。
8. **底部量化卡**：−5.1% distance / 36/36 feasible runs / −22.0% CPU（三个未上标题的 KPI）。
9. **Footer**：系所（左）+ 作者与导师（右）。

## 内容来源
全部文本与图片来自现有 `FURP_Showcase_Poster.pptx`（FURP 项目真实结果），不做内容创作或数字改动。
