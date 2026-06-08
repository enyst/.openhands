---
name: brand-atomic-kit
description: Generate an agent-readable brand system as a structured folder of files. Use when building a brand identity, creating AI-usable brand guidelines, generating landing pages or marketing materials, or packaging brand work as a reusable deliverable.
---

# Brand Atomic Kit

Generate an agent-readable brand system as a structured folder of files. Based on Emmett Shine's "HTML Brand" concept — brand identity encoded as instructions, not documentation.

Source: https://x.com/emmettshine/status/2054539694097015171

## When to use

- Building a brand identity for a new project or company
- Creating brand guidelines that AI agents can actually build from
- Generating a landing page, product UI, or marketing materials that stay on-brand
- Packaging brand work as a deliverable for clients

## What it produces

A folder structure where every file is agent-readable:

```
brand_atomic_system/
├── readme.md                  ← project overview, how to use the kit
├── magic_trick.md             ← the human creative spark (see below)
├── human/                     ← traditional brand guidelines (PDF, prose)
│   └── brand-guidelines.md
└── agent/                     ← agent-readable brand instructions
    ├── verbal/
    │   ├── positioning.md     ← what the brand is, market position
    │   ├── audience.yaml      ← who it's for, segments, personas
    │   ├── messaging.md       ← key messages, taglines, elevator pitches
    │   ├── differentiation.md ← what makes it different, competitors
    │   ├── concepts.md        ← core ideas, metaphors, mental models
    │   └── voice.md           ← tone, style, do/don't examples
    └── visual/
        ├── colors_and_type.css ← CSS variables for colors, font stacks
        ├── fonts/              ← font files or references
        ├── assets/             ← logo SVGs, brand marks
        ├── components/         ← HTML/CSS UI primitives
        ├── tokens/             ← design token specimens
        └── motion/             ← animation system (JSON easing curves, CSS transitions)
```

## How to use

1. **Gather inputs:** project name, what it does, who it's for, what makes it different, any existing brand elements (colors, fonts, logos)
2. **Generate the verbal system first:** positioning → audience → differentiation → messaging → voice → concepts
3. **Generate the visual system:** colors/type CSS → component primitives → motion specs
4. **Write the human guidelines:** prose version of the same thinking for humans who don't read YAML
5. **Add the magic trick:** one original creative idea that can't be derived from the system — the thing that makes the brand memorable, not just correct

## Key principles

### The kit is instructions, not documentation
Every file should be structured so an agent (Cursor, Claude, Codex, SmolPaws) can read it and build from it. YAML for structured data, CSS for visual language, Markdown for prose that has structure, JSON for motion/animation specs.

### Upstream thinking is the value
The positioning, voice, and strategic choices are what matters. The downstream outputs (landing pages, campaigns, emails) are generated from these inputs. Get the inputs right and the outputs follow.

### magic_trick.md
After the system produces correct-but-median output, add a human creative idea that tilts it. A metaphor, a visual concept, a weird reference, a counterintuitive choice. This is what prevents "AI slop" — the system gives you correctness, the magic trick gives you memorability.

Example magic_trick.md:
```markdown
# Magic Trick

## The idea
[One sentence that captures the creative spark]

## Why it works
[Why this particular idea elevates the brand beyond the median]

## How to apply it
[Specific instructions for how an agent should incorporate this into outputs]

## References / inspiration
[Links, images, vibes that inform this idea]
```

### HTML > PDF
HTML, CSS, and SVG are parseable by agents. PDFs and PNGs can be looked at but not built from. When in doubt, encode in HTML.

## Verbal system details

### positioning.md
```markdown
# Positioning

## What we are
[One sentence, matter of fact]

## What we're not
[Explicit boundaries]

## Market position
[Where we sit relative to alternatives]

## Core promise
[What the user gets]
```

### audience.yaml
```yaml
primary:
  name: [segment name]
  description: [who they are]
  needs: [what they need]
  current_solution: [what they use now]
  why_us: [why they'd switch]

secondary:
  name: [segment name]
  # ...
```

### voice.md
```markdown
# Voice

## Tone
[3-5 adjectives that describe how the brand sounds]

## Do
- [specific example of on-brand language]

## Don't
- [specific example of off-brand language]

## Sample copy
[2-3 sentences in the brand voice, for different contexts]
```

## Visual system details

### colors_and_type.css
```css
:root {
  /* Primary palette */
  --color-primary: #...;
  --color-primary-light: #...;
  --color-primary-dark: #...;

  /* Neutral palette */
  --color-bg: #...;
  --color-surface: #...;
  --color-text: #...;
  --color-text-muted: #...;

  /* Accent */
  --color-accent: #...;

  /* Typography */
  --font-display: '...', serif;
  --font-body: '...', sans-serif;
  --font-mono: '...', monospace;

  /* Scale */
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 1.875rem;

  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-4: 1rem;
  --space-8: 2rem;
  --space-16: 4rem;
}
```

### motion/system.json
```json
{
  "curves": {
    "ease-default": "cubic-bezier(0.4, 0, 0.2, 1)",
    "ease-in": "cubic-bezier(0.4, 0, 1, 1)",
    "ease-out": "cubic-bezier(0, 0, 0.2, 1)",
    "ease-bounce": "cubic-bezier(0.34, 1.56, 0.64, 1)"
  },
  "durations": {
    "instant": "100ms",
    "fast": "200ms",
    "normal": "300ms",
    "slow": "500ms",
    "dramatic": "800ms"
  }
}
```

## After generation

Once the kit is generated, test it:
1. Feed the entire `/agent/` folder to an LLM and prompt: "Generate an HTML landing page from this brand system"
2. The output should have correct colors, fonts, tone of voice, and component patterns
3. If it doesn't, the kit needs more specificity in the files that failed
4. Add the magic trick and regenerate — the output should now have a distinctive creative edge
