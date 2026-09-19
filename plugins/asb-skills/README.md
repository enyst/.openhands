# asb-skills (bundled)

Verbatim copy of the 21 public skills from
[asmartbear/asb-skills](https://github.com/asmartbear/asb-skills), by Jason Cohen —
the AI skills behind [A Smart Bear](https://longform.asmartbear.com) and
*Hidden Multipliers*, vendored so this marketplace stays a single install.

- **Source:** https://github.com/asmartbear/asb-skills @ `e536b22`
- **Browse them:** https://skills.asmartbear.com
- **License:** CC-BY-4.0. Attribution is required, which is why the plugin manifest and
  this file name the author.
- **Nothing here is modified.** Upstream is the source of truth.

These are a different-but-similar set to the sibling `minimalist-entrepreneur` plugin:
that one is 9 skills hand-adapted from Sahil Lavingia's book; this one is upstream
verbatim (each skill already ships `name` + `description` frontmatter).

## What they are for

They interrogate rather than answer: each one asks questions, tests the answers, and
refuses to let a vague claim through. You leave with your own thinking written to a file.

Workshops, meant to run in sequence:

| Workshop | Skills |
|---|---|
| **Find Yourself** (2) | `asb-who-me`, `asb-voters` |
| **Find Your Carol** (6) | `asb-carol-observations`, `asb-carol-strengths`, `asb-carol-keystones`, `asb-carol-dealbreakers`, `asb-carol-inciting-events`, `asb-carol-define` |
| **Customer Interviews** (6) | `asb-interview-goals`, `asb-interview-hypotheses`, `asb-interview-questions`, `asb-interview-debrief`, `asb-interview-learning`, `asb-interview-report` |
| **Set Your Price** (3) | `asb-more-or-less`, `asb-willingness-to-pay`, `asb-raise-prices` |

Standalone: `asb-rude-qa` (grills a plan until it cracks), `asb-problem` (is this a good
market?), `asb-positioning` (the pitch that sells), `asb-needs-stack` (what the customer
really wants). Groupings copied from upstream `skills.sh.json`.

## Updating

```sh
git clone --depth 1 https://github.com/asmartbear/asb-skills /tmp/asb-skills
# copy each .claude/skills/asb-*/SKILL.md back here, then re-read this README's commit pin
```

Upstream's `plugins/asb-skills/skills/*` are symlinks into `.claude/skills/`, so copy from
`.claude/skills/<name>/SKILL.md` (resolving the symlink) rather than from the plugin folder.

Five upstream skills are deliberately excluded: `book-prose-writer`, `create-asb-skill`,
`doc-skills`, `exercise-asb-skill`, `jason-corpus-search` — all marked
`metadata.internal: true`, i.e. they are the author's own dev tooling, not published skills.

## Using them

Install this plugin from the marketplace the same way as `minimalist-entrepreneur`, or copy
`skills/<name>/` into `~/.openhands/skills/<name>/`.
