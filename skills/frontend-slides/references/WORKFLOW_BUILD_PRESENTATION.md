# Workflow: Build Presentation

Split from [WORKFLOW.md](WORKFLOW.md). Use after you have content + a chosen style.

## Phase 3: Generate Presentation

Now generate the full presentation based on:
- Content from Phase 1
- Style from Phase 2

### File Structure

For single presentations:
```
presentation.html    # Self-contained presentation
assets/              # Images, if any
```

For projects with multiple presentations:
```
[presentation-name].html
[presentation-name]-assets/
```

### HTML Architecture

Use the fixed-stage template in [HTML_TEMPLATE.md](HTML_TEMPLATE.md) as the reference architecture. Every deck must include the full base CSS from [viewport-base.css](viewport-base.css).

Minimum structure:

```html
<body>
  <div class="deck-viewport">
    <main class="deck-stage">
      <section class="slide active title-slide">
        <div class="slide-content">
          <h1 class="reveal">Presentation Title</h1>
          <p class="reveal">Subtitle or author</p>
        </div>
      </section>

      <section class="slide">
        <div class="slide-content">
          <h2 class="reveal">Slide Title</h2>
          <p class="reveal">Content...</p>
        </div>
      </section>
    </main>
  </div>
</body>
```

Core requirements:

- Author every slide at `1920px x 1080px` inside `.deck-stage`.
- Scale `.deck-stage` as a whole to fit the viewport; allow letterboxing/pillarboxing.
- Do not use responsive breakpoints to rearrange slide content for phones.
- Do not switch slides with `display: none`; use `.active` / `.visible` plus `visibility`, `opacity`, and `pointer-events`.
- Keep navigation chrome outside the authored slide system.
- Use `prefers-reduced-motion` support for all animations.

### Required JavaScript Features

Every presentation should include:

1. **Stage scaling**
   - Compute `Math.min(window.innerWidth / 1920, window.innerHeight / 1080)`.
   - Translate and scale `.deck-stage` on load and resize.
   - See [VIEWPORT_FITTING.md](VIEWPORT_FITTING.md) for the minimum implementation.

2. **SlidePresentation controller**
   - Keyboard navigation (arrows, space)
   - Touch/tap support
   - Progress bar or slide count updates
   - Adds `.active` / `.visible` to the current slide

3. **Optional enhancements** (based on style)
   - Custom cursor with trail
   - Particle system background (canvas)
   - Parallax effects inside the fixed stage
   - 3D tilt on hover
   - Magnetic buttons
   - Counter animations

### Code Quality Requirements

**Comments:**
Every section should have clear comments explaining:
- What it does
- Why it exists
- How to modify it

```javascript
/* ===========================================
   CUSTOM CURSOR
   Creates a stylized cursor that follows mouse with a trail effect.
   - Uses lerp (linear interpolation) for smooth movement
   - Grows larger when hovering over interactive elements
   =========================================== */
class CustomCursor {
    constructor() {
        // ...
    }
}
```

**Accessibility:**
- Semantic HTML (`<section>`, `<nav>`, `<main>`)
- Keyboard navigation works
- ARIA labels where needed
- Reduced motion support

```css
@media (prefers-reduced-motion: reduce) {
    .reveal {
        transition: opacity 0.3s ease;
        transform: none;
    }
}
```

**Responsive & Viewport Fitting (CRITICAL):**

See [VIEWPORT_FITTING.md](VIEWPORT_FITTING.md) for the full mandatory base CSS and guidelines.

Quick reference:
- Every `.slide` must have `height: 100vh; height: 100dvh; overflow: hidden;`
- All typography and spacing must use `clamp()`
- Respect content density limits (max 4-6 bullets, max 6 cards, etc.)
- Include breakpoints for heights: 700px, 600px, 500px
- When content doesn't fit → split into multiple slides, never scroll

---

