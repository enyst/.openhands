---
name: antislop-codebase
description: |
  Structural cleanup for prototype or fast-growing codebases. Use this skill when:
  (1) A repo has grown organically and needs maintainability improvements
  (2) Files are too large, boundaries are unclear, or types are missing
  (3) Test coverage is spotty or tests are unreliable
  (4) Duplicated code or patterns need consolidation
  (5) The codebase works but is hard to modify safely
  (6) Preparing a prototype for production use
  Focuses on: module boundaries, file size, type safety, test coverage, code duplication, and clear ownership.
---

# Antislop Codebase

Move a repo from "works but hurts" to maintainable shape. Preserve behavior, improve structure in thin reversible slices.

## Boundary

This skill is for structural maintainability: code organization, typed boundaries, tests, module structure, file size reduction, and duplication cleanup. Not for security audits, observability, or deployment — those are separate skills.

## Operating Principles

- Preserve behavior first. Improve architecture in thin, reversible slices.
- Ground every decision in repo facts: file sizes, dependency graph, test results, git history.
- Keep files editable: prefer modules under 300–500 lines, explicit exports, narrow tests.
- Never rewrite areas under active development without checking git log first.
- Commit at green checkpoints. Don't create a giant unreviewable diff.
- End with evidence: a summary of what changed, what improved, and what's left.

## Workflow

### 1. Discover the Shape

Non-mutating scan before planning:

```bash
# Largest files
find . -name '*.ts' -o -name '*.py' -o -name '*.tsx' | xargs wc -l | sort -rn | head -20

# Directory structure
find . -not -path '*/node_modules/*' -not -path '*/.git/*' -type f | head -50

# Test coverage (if available)
npm test -- --coverage 2>/dev/null || pytest --co -q 2>/dev/null

# Recent git activity (avoid active areas)
git log --oneline -20
git diff --stat HEAD~10
```

- Identify the largest files and hottest directories
- Map module boundaries: what imports what
- Check test infrastructure: does it exist, does it run, is it meaningful
- Read recent commits to avoid stepping on active work

### 2. Plan the Cleanup

Write a concrete plan before touching code:

- **Goal**: what "maintainable" means for this specific repo
- **Non-goals**: what you're explicitly NOT changing
- **Slices**: ordered list of changes, smallest blast radius first
- **Test plan**: how you'll verify each slice didn't break anything
- **Active areas**: files/modules to avoid because they're under active development

Ask the user to confirm the plan before executing.

### 3. Build a Safety Net

Before broad edits:

- Run existing tests and note the baseline (how many pass, how many fail)
- Run typecheck if available (`npm run typecheck`, `pyright`, `mypy`)
- If tests are missing for areas you'll change, add minimal characterization tests first
- Commit the safety net additions before refactoring

### 4. Execute in Green Slices

Process the plan methodically:

- **Split large files first**: extract coherent modules, keep old imports working via re-exports
- **Extract shared helpers**: when you see the same pattern in 3+ places, extract it
- **Add types to boundaries**: function signatures, API interfaces, config schemas
- **Remove dead code**: check git blame — if it hasn't been touched in months and nothing imports it, remove it
- **Consolidate duplicates**: only after both copies have tests

After each slice:
- Run tests
- Run typecheck
- Commit with a descriptive message

### 5. Verify and Report

After all slices:

- Run the full test suite
- Compare file count, average file size, and test count to the baseline
- List what was changed, what improved, and what's left for future work
- Note any risks or areas that need manual verification

## Subagent Pattern

For large repos, independent cleanup slices can run concurrently:

```bash
# Start a subagent for a specific slice
openhands --headless --json -t "Extract the auth helpers from src/server.ts into src/auth/index.ts. Keep the old imports working via re-export. Run tests after."
```

Or via the OpenHands Cloud API:
```bash
curl -X POST "$OPENHANDS_URL/api/conversations" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"initial_message": "...", "agent": {"tools": [{"name": "terminal"}, {"name": "file_editor"}]}}'
```

Assign workers to independent surfaces. Don't let subagents edit the same files concurrently. Merge results in the main conversation.

## Quick Checklist

- [ ] No file over 500 lines without good reason
- [ ] Each module has a clear single responsibility
- [ ] Public API surfaces are typed
- [ ] No copy-pasted code blocks (extract helpers)
- [ ] Dead code removed (check git blame first)
- [ ] Tests exist for all changed modules
- [ ] All tests pass after cleanup
- [ ] Typecheck passes (if applicable)
- [ ] Each commit is a green, reviewable slice
