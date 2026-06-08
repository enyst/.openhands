---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

---

## Style Library

Documented reference styles extracted from real, well-designed sites. Use these as starting points or inspiration — never copy wholesale. Each entry captures the design system so you can remix it into new contexts.

### Builder's Journal — warm editorial workshop

**Source:** [enyst.github.io](https://enyst.github.io) — Engel Nyst's personal site and architecture pages. Full system in `brand.css`.

**Vibe:** A builder's journal written by lamplight. Technical but never cold. Noise texture for tactile depth — like aged paper under warm light. Elegant restraint with just enough personality.

**Color system** (CSS variables):
```css
:root {
  --ink: #e5e0d8;          /* warm parchment — primary text */
  --muted: #8a847a;        /* worn stone — secondary, captions */
  --bg: #0f0f0e;           /* near-black — dark workshop surface */
  --card: #1a1a18;         /* slightly lifted surface */
  --border: #2a2a26;       /* subtle edge — dividers */
  --accent: #c9a84c;       /* warm gold — headers, highlights */
  --teal: #6bbfab;         /* cool mint — links, interactive */
  --green: #7bc47f;        /* soft green — live/success */
  --report: #dc6b4a;       /* warm red-orange — alerts */
}
```

Narrower than Amber Noir — gold accent for structure, teal for interaction. The two-accent split (warm gold for headers, cool teal for links) creates visual hierarchy without adding colors.

**Typography:**
- **Serif:** Instrument Serif (400) — display headlines only. The hero name is enormous (`clamp(3.2em, 8vw, 5em)`) with tight letter-spacing (−0.04em). One font weight, used once, maximum impact.
- **Sans:** DM Sans (400/500/700) — body text. Warm, readable, a step above system fonts.
- **Mono:** JetBrains Mono (400/600) — section headers (h2), tags, links lists, footer. h2 is uppercase mono with 0.14em letter-spacing and a gold underline border — section headers read like chapter tabs.

The key move: serif for the name only, mono for all structural labels. The body disappears into readability while the extremes (serif display, mono labels) create the visual identity.

**Layout:**
- Max-width 680px (780px for architecture pages) — deliberately narrow, editorial column width.
- 100px top padding — generous breathing room.
- Cards with a hidden left-edge accent bar (3px gold) that reveals on hover with a 4px translateX shift.
- Status tags: mono, uppercase, tiny (`0.65em`), with color-coded translucent backgrounds (12% opacity fills).
- Links list: horizontal flex with mono font, teal color, underline-on-hover.

**Atmospheric depth:**
- SVG fractal noise texture on the body at 3% opacity — creates a paper-like tactile surface without being visible as a pattern.
- `fadeUp` animation on hero elements (12px translate + opacity) with staggered delays.
- Card hover: border-color transition + translateX + box-shadow accent line — subtle but satisfying.

**Distinctive patterns:**
- **Section headers as mono-gold tabs:** h2 is uppercase JetBrains Mono in gold with a border-bottom — reads like physical divider tabs.
- **Fractal noise background:** inline SVG data URI, not an image file — zero extra requests, works everywhere.
- **Card left-accent reveal:** invisible 3px gold bar appears on hover — rewards interaction without cluttering rest state.
- **Prose styling:** dedicated `.prose` class with careful code inline styling, link underline transitions, and comfortable 1.7 line-height.

**When to use this style:** Personal sites, documentation hubs, editorial long-form, architecture writeups, anything where reading comfort and quiet confidence matter more than flash.

**When to avoid:** Marketing pages that need energy, product launches, anything with lots of interactive elements or dense data.

---

### Amber Noir — warm dark developer tool

**Source:** [PawPause for Mac](https://miladsafarzadeh1.github.io/PawPause-mac/) landing page.

**Vibe:** Candlelit workshop. A developer tool that feels like it was designed by someone who cares about craft. Dark, warm, precise — not cold or sterile. The kind of page where you slow down and actually read.

**Color system** (CSS variables):
```css
:root {
  --bg: #16140f;           /* near-black warm brown */
  --panel: #1c190f;        /* card/section background — barely lifted */
  --panel2: #161309;       /* recessed inputs */
  --line: #2d281d;         /* borders, dividers */
  --ink: #f3e9d6;          /* primary text — warm cream */
  --ink2: #cabfa8;         /* secondary text — muted gold */
  --mut: #7a7263;          /* tertiary/caption — earthy gray */
  --mut2: #5c554a;         /* lowest contrast text */
  --amber: #e8a33d;        /* primary accent — warm gold */
  --amber2: #c97a1f;       /* darker accent for gradients */
  --red: #ff5c47;          /* warning/error */
  --green: #7fcf9b;        /* success */
}
```

The amber-on-dark-brown creates a "candlelight" warmth that cold blue-on-black dark themes never achieve. The palette is narrow — almost everything is amber or cream — which makes it cohesive without effort.

**Typography:**
- **Display:** Syne (600–800) — geometric, chunky, personality-forward. Used for all headings. Tight letter-spacing (−0.5px on h1, −0.3px on h2).
- **Mono:** IBM Plex Mono (400–600) — the workhorse. Buttons, nav labels, eyebrow text, metadata, signal names, download stats. Gives the whole page a "tool built by engineers" texture.
- **Body:** System sans-serif stack — deliberately invisible so Syne and Plex Mono dominate.
- **Fluid sizing:** `clamp()` on headings (e.g. `clamp(34px, 5.5vw, 58px)` for h1).

The key move: mono isn't just for code blocks. It's the UI voice. Buttons, tags, captions — all mono. This shifts the feel from "marketing page" to "product page built by the person who wrote the product."

**Layout:**
- Max-width 1020px, 22px side padding — tighter than typical marketing, closer to a readme.
- Sticky nav with `backdrop-filter: blur(8px)` and semi-transparent background (`rgba(22,20,15,.72)`).
- 3-column card grid (→ 1-column on mobile) for feature trust cards.
- Numbered step cards using CSS `counter-reset`/`counter-increment` with amber numbered badges.
- Interactive demo as a split panel (terminal-style) embedded directly in the page.
- FAQ using styled `<details>` with custom `+`/`–` markers in amber mono.

**Atmospheric depth:**
- Body background has two large `radial-gradient` overlays in faint amber (~0.04–0.09 opacity), positioned top-right and bottom-left. This creates subtle warmth without being visible as a shape.
- Cards use 1px borders (`var(--line)`) instead of shadows — flat but structured.
- App icon has a deep `box-shadow: 0 18px 50px rgba(0,0,0,.45)` for floating effect.

**Distinctive patterns:**
- **Eyebrow labels:** uppercase, letter-spaced (3px), mono, amber — above every hero and section header.
- **Ghost buttons:** transparent background + 1px border alongside solid amber CTAs — clean hierarchy.
- **Interactive demo:** a live, working cat-detection simulator built into the landing page with SVG arc gauge, signal meters, and a textarea that actually locks when "cat detected." Not a video, not a gif — real code.
- **Download metadata:** version, size, and OS compatibility in a single mono line below the CTA — doesn't hide the practical info.

**When to use this style:** Developer tools, open-source project landing pages, macOS utilities, anything indie/craft where warmth and precision both matter. Works well for single-page marketing of a small focused product.

**When to avoid:** Consumer SaaS, anything that needs to feel light/playful/corporate, data-heavy dashboards (too dark for dense tables).
