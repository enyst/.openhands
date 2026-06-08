---
name: frontend-slides
description: Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when the user wants to build a presentation, convert a PPT/PPTX to web, or create slides for a talk/pitch. Helps non-designers discover their aesthetic through visual exploration rather than abstract choices.
license: MIT (see LICENSE.txt)
compatibility: For PPT/PPTX conversion requires Python and the python-pptx package.
---

# Frontend Slides Skill

Create **zero-dependency**, animation-rich HTML presentations that run entirely in the browser.

## Non-negotiables

- **Single-file output:** generate a self-contained `.html` with inline CSS/JS (no npm, no build tools).
- **Distinctive design:** avoid generic, templated “AI slop” aesthetics.
- **Fixed 16:9 stage (CRITICAL):** author slides in a 1920×1080 stage and scale the whole stage to the viewport. Do not reflow slide content for phones.
  - Details + mandatory base CSS: see [references/VIEWPORT_FITTING.md](references/VIEWPORT_FITTING.md) and [references/viewport-base.css](references/viewport-base.css).
- **Progressive disclosure:** read style indexes first; load detailed presets/templates only after the user picks a direction.

## How to use (choose a mode)

1. **New presentation** (from scratch)
   - Use the structured workflow in [references/WORKFLOW.md](references/WORKFLOW.md).
   - Use the style index in [references/STYLE_PRESETS.md](references/STYLE_PRESETS.md) and load the chosen preset from `references/presets/`.
   - For more adventurous design directions, use the upstream bold template pack index at `references/bold-template-pack/selection-index.json`, then load only the selected template's `design.md`.

2. **PPT/PPTX conversion**
   - Extract content + images with the workflow in [references/PPT_CONVERSION.md](references/PPT_CONVERSION.md).

3. **Enhance an existing HTML presentation**
   - Read the existing HTML/CSS/JS, preserve the content structure, then apply the same constraints:
     - viewport fitting
     - accessibility
     - performance
     - distinctive visuals

## Design + animation references

- Effect → feeling mapping: [references/STYLE_EFFECT_MAPPING.md](references/STYLE_EFFECT_MAPPING.md)
- Animation patterns (CSS/JS snippets): [references/ANIMATION_PATTERNS.md](references/ANIMATION_PATTERNS.md)

## Troubleshooting

See [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md).
