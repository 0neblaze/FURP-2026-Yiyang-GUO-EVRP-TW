# DESIGN.md — FURP Showcase Poster v2

## 画布
59.43 × 84.08 cm（A0 竖版），单页。

## 技术路线
以 `Poster Template - 副本.pptx` 为底本，python-pptx 程序化替换文本与图片（保留模板全部矢量视觉：header 色块、section box、标题条、icon 组、footer）。复杂 FREEFORM 自定义几何无法用 DSL 1:1 复刻，编辑底本是唯一精准路径。

## 色板（≤4 hex，全部来自模板）
| 色 | 值 | 用途 |
|---|---|---|
| nottblue | #10263B | header 块、标题条、footer bar、正标题文字 |
| brand-blue | #2E6CA4 | icon 圆圈、✓/▲ 符号 |
| box-frame | accent1 lumMod 75%（#335693） | box 边框（模板原生，不动） |
| light-blue | #EFF5FD | 底部 highlights bar 底色（模板原生，不动） |
正文文字：继承模板默认黑。

## 字体（≤2 家族）
- **Roboto Condensed ExtraBold**：海报标题 48pt（模板原 115pt 无法容纳现标题）、副行 32pt、box 标题 44pt（不动）、icon 要点 24pt、底部卡 32pt（不动）
- **Calibri**：正文要点 15–17pt、说明行 14pt、References 12pt、footer 28pt

## 版面映射（模板 → 内容）
| 区域 | 坐标 cm | 内容 |
|---|---|---|
| Header 标题区 | (20.24, 0) 39.19×8.29 | 48pt 两行标题 + 32pt 副行（作者\|系所） |
| Motivation box | (0, 9.36) 18.79×31.52 | 3 icon 要点（24pt≤2行）+ Fig1 (14.73×9.52) + Objective（24pt 2行） |
| Method Overview box | (19.93, 9.36) 39.50×31.52 | Fig2 (24.5×23.05) 左 + 右列 4 条要点 15pt |
| Experimental Settings box | (0, 41.89) 24.41×16.92 | Fig3 (15.6×11.38 居中) + 底部说明 14pt |
| Key Results box | (25.66, 41.89) 33.78×16.92 | Fig4 (26.5×11.38 居中) + 底部说明 14pt |
| Key Quant. Highlights box | (0, 59.82) 24.41×16.92 | Fig5 (23.4×9.5) + 底部说明 14pt |
| 新增右下 box（克隆模板 box 结构） | (25.66, 59.82) 33.78×16.92 | 标题 "Why It Works & Honest Audit"；7 条 15pt + refs 12pt + QR 4.2cm |
| 底部 bar 3 卡 | (0, 77.25) 59.38×3.82 | −5.1% distance / 36/36 feasible / −22.0% CPU |
| Footer | (0, 81.43) 59.43×2.68 | 左：Department of Mathematical Sciences；右：作者 ID + 导师 |

## 图片适配规则
按占位框**等比缩放、取小维度适配、在框内居中**，禁止拉伸变形：
- Fig1 1584×1000 → 14.73×9.30
- Fig2 1166×1098 → 24.5×23.05（按高）
- Fig3 1506×1098 → 15.62×11.38（按高）
- Fig4 2194×944 → 26.45×11.38（按高）
- Fig5 2116×862 → 23.40×9.53（按宽）
- QR 370×370 → 4.2×4.2

## 溢出预算校验
- 标题 48pt Roboto Condensed ≈ 0.76 cm/char，39.19cm 宽 → 51 chars/行；两行 40/49 chars ✓
- 正文 15pt ≈ 0.24 cm/char；右下要点列 26.5cm → ~106 chars/行，全部 ≤ 86 chars ✓
- box 标题 44pt ≈ 0.70 cm/char，最长 "Key Quantitative Highlights" 27 chars = 18.9 ≤ 24.4 ✓
- 底部卡 32pt ≈ 0.59 cm/char，15.32cm → 26 chars；"−5.1% total distance" 20 ✓
