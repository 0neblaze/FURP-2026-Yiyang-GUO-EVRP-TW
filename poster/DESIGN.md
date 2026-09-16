# DESIGN.md — FURP Showcase Poster v2

## Canvas

59.43 × 84.08 cm (A0 portrait), single page.

## Technical approach

Use `Poster Template - 副本.pptx` as the base file and replace text and figures programmatically with python-pptx (keeping all of the template's vector visuals: header block, section boxes, title bars, icon groups, footer). Complex FREEFORM custom geometry cannot be reproduced 1:1 with a DSL; editing the base file is the only precise path.

## Palette (≤4 hex values, all from the template)

| Color | Value | Usage |
|---|---|---|
| nottblue | #10263B | header block, title bars, footer bar, main title text |
| brand-blue | #2E6CA4 | icon circles, ✓/▲ symbols |
| box-frame | accent1 lumMod 75% (#335693) | box borders (template-native, untouched) |
| light-blue | #EFF5FD | bottom highlights bar background (template-native, untouched) |

Body text: inherits the template's default black.

## Typography (≤2 families)

- **Roboto Condensed ExtraBold**: poster title 48pt (the template's original 115pt cannot fit the current title), subtitle line 32pt, box titles 44pt (untouched), icon bullets 24pt, bottom cards 32pt (untouched)
- **Calibri**: body bullets 15–17pt, caption lines 14pt, References 12pt, footer 28pt

## Layout mapping (template → content)

| Region | Coordinates (cm) | Content |
|---|---|---|
| Header title area | (20.24, 0) 39.19×8.29 | 48pt two-line title + 32pt subtitle (author\|department) |
| Motivation box | (0, 9.36) 18.79×31.52 | 3 icon bullets (24pt ≤2 lines) + Fig1 (14.73×9.52) + Objective (24pt, 2 lines) |
| Method Overview box | (19.93, 9.36) 39.50×31.52 | Fig2 (24.5×23.05) left + right column of 4 bullets at 15pt |
| Experimental Settings box | (0, 41.89) 24.41×16.92 | Fig3 (15.6×11.38 centered) + bottom caption 14pt |
| Key Results box | (25.66, 41.89) 33.78×16.92 | Fig4 (26.5×11.38 centered) + bottom caption 14pt |
| Key Quant. Highlights box | (0, 59.82) 24.41×16.92 | Fig5 (23.4×9.5) + bottom caption 14pt |
| New bottom-right box (cloned template box structure) | (25.66, 59.82) 33.78×16.92 | title "Why It Works & Honest Audit"; 7 bullets at 15pt + refs 12pt + QR 4.2cm |
| Bottom bar, 3 cards | (0, 77.25) 59.38×3.82 | −5.1% distance / 36/36 feasible / −22.0% CPU |
| Footer | (0, 81.43) 59.43×2.68 | left: Department of Mathematical Sciences; right: author ID + supervisor |

## Figure fitting rules

Scale figures **proportionally, fit the smaller dimension, center within the placeholder**; stretching/distortion is forbidden:

- Fig1 1584×1000 → 14.73×9.30
- Fig2 1166×1098 → 24.5×23.05 (by height)
- Fig3 1506×1098 → 15.62×11.38 (by height)
- Fig4 2194×944 → 26.45×11.38 (by height)
- Fig5 2116×862 → 23.40×9.53 (by width)
- QR 370×370 → 4.2×4.2

## Overflow budget verification

- Title 48pt Roboto Condensed ≈ 0.76 cm/char, 39.19cm wide → 51 chars/line; two lines at 40/49 chars ✓
- Body 15pt ≈ 0.24 cm/char; bottom-right bullet column 26.5cm → ~106 chars/line, all ≤ 86 chars ✓
- Box titles 44pt ≈ 0.70 cm/char, longest "Key Quantitative Highlights" 27 chars = 18.9 ≤ 24.4 ✓
- Bottom cards 32pt ≈ 0.59 cm/char, 15.32cm → 26 chars; "−5.1% total distance" 20 ✓
