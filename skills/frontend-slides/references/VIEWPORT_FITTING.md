# Fixed 16:9 Viewport Fitting Requirements

**This section is mandatory for ALL presentations. Every slide must be fully visible without scrolling on every screen size.**

## The Golden Rule

```text
Author slides at 1920×1080 → scale the whole stage to the viewport
Content overflows? → split into more slides or simplify
Never scroll inside a slide. Never reflow slide content for phones.
```

## Required Stage Model

Every generated deck must use a fixed-stage architecture:

- Browser viewport wrapper fills the window.
- Inner stage is exactly `1920px × 1080px`.
- JavaScript scales the entire stage uniformly to fit the viewport.
- Letterboxing / pillarboxing is allowed; content re-layout is not.
- Slides stack inside the fixed stage.
- Slide visibility is controlled by `.active` / `.visible`, using `visibility`, `opacity`, and `pointer-events`.
- Do **not** use `display: none` / `display: block` for slide switching; later layout rules can override them and make every slide visible.
- Use fixed internal slide measurements at the 1920×1080 design size.
- Use `clamp()` only for non-slide UI outside the stage, or for small fallback previews where a full stage is impractical.
- Never negate CSS functions directly (`-clamp()`, `-min()`, `-max()` are ignored); use `calc(-1 * clamp(...))` instead.

## Content Density Modes

Ask whether the deck is primarily a reading deck or a speaking deck, then design around that answer.

| Density mode | Best for | Design behavior |
| --- | --- | --- |
| **Low density / speaker-led** | Public talks, keynote-style sharing, live explanation | One idea per slide, large type, strong visual hierarchy, generous negative space, 1–3 bullets max, more slides if needed |
| **High density / reading-first** | Reports, handouts, async review, detailed internal docs | More self-contained slides, structured grids/tables/annotations, 4–8 bullets or 4–6 cards when readable, tighter but still intentional spacing |

Baseline limits still apply: no scrolling, no overflow, no overlapping panels, and no text below comfortable reading size. If content exceeds the selected density mode, split it into more slides instead of shrinking until it becomes cramped.

## Content Density Limits

| Slide Type | Maximum Content |
| --- | --- |
| Title slide | 1 heading + 1 subtitle + optional tagline |
| Content slide | 1 heading + 4–6 bullet points OR 1 heading + 2 short paragraphs |
| Feature grid | 1 heading + 6 cards maximum |
| Code slide | 1 heading + 8–10 lines of code maximum |
| Quote slide | 1 quote, max 3 lines, plus attribution |
| Image slide | 1 heading + 1 image or diagram fitted inside the stage |

If content exceeds these limits, split into multiple slides.

## Mandatory base CSS

The full base CSS is bundled as [`viewport-base.css`](viewport-base.css). Include its contents in every generated presentation, then add the chosen visual style on top.

## Minimum stage-scaling JavaScript

Use this pattern, or the richer implementation in [`bold-template-pack/deck-stage.js`](bold-template-pack/deck-stage.js), to scale the 1920×1080 stage as a whole:

```js
const stage = document.querySelector('.deck-stage');
const DESIGN_WIDTH = 1920;
const DESIGN_HEIGHT = 1080;

function scaleStage() {
  const scale = Math.min(window.innerWidth / DESIGN_WIDTH, window.innerHeight / DESIGN_HEIGHT);
  const left = (window.innerWidth - DESIGN_WIDTH * scale) / 2;
  const top = (window.innerHeight - DESIGN_HEIGHT * scale) / 2;
  stage.style.transform = `translate(${left}px, ${top}px) scale(${scale})`;
}

window.addEventListener('resize', scaleStage);
scaleStage();
```

## Validation Checklist

Before delivering, verify:

- [ ] No slide scrollbars at desktop, tablet, or phone viewport sizes
- [ ] No content clipped at 1920×1080 authoring size
- [ ] Stage scales uniformly and remains 16:9
- [ ] Slides do not reflow differently on small screens
- [ ] Navigation controls remain outside the authored slide system
- [ ] `prefers-reduced-motion` disables or minimizes motion
- [ ] Print/PDF mode renders one 16:9 slide per page
