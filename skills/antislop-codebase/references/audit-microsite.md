# Migration Audit

End major migrations with a structured audit artifact — either a markdown report or a self-contained static HTML microsite.

## Required Questions

- Is the repo clearer and more maintainable?
- How much LOC was added, deleted, and net changed?
- How many files were added, removed, renamed, and modified?
- Which large files collapsed, and what are the new largest files?
- How did directory structure evolve?
- How did tests, e2e, API functions, types, and runtime/deploy risk change?
- What costs and risks remain?

## Data Sources

Use git, not vibes:

```bash
git diff --shortstat BASE..HEAD
git diff --numstat BASE..HEAD
git diff --name-status BASE..HEAD
git ls-tree -r --name-only BASE
git ls-files
git log --date=iso --pretty=format:"%h %ad %s" BASE..HEAD
```

Use committed `HEAD:file` content for current metrics if the worktree is dirty. List dirty files separately. Per-file `wc -l` for baseline/current largest files.

## Visuals (for HTML microsite)

Include:

- commit timeline by theme
- LOC/file/API/test before/after charts
- extension/language mix
- directory/module map
- largest files before/after
- maintainability scorecard
- wins, costs, risks, next recommendations

Use inline SVG or embedded CSS/JS; avoid external network assets.

## Serving

Generate under a local artifact folder such as `test-results/migration-audit/`. For HTML microsites, start a static local server and return a clickable URL. For markdown, output to a file the user can review.

## QA

- Verify the audit data matches actual git stats.
- Cross-check headline numbers with direct shell commands.
- For HTML microsites: check for nonblank charts, readable tables, no horizontal overflow.
