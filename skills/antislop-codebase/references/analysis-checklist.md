# Analysis Checklist

Use this before planning or editing.

## Repo Shape

- `git status --short`
- `git log --oneline --decorate -40`
- package scripts, lockfile, build/test/typecheck/e2e commands
- framework/deployment config
- app entrypoints and API/server entrypoints
- persisted state, migrations, auth, environment variables

## Size and Complexity Metrics

- largest source/test/tool files by line count
- top-level directory counts and LOC
- duplicate helpers or repeated patterns
- public API route/function count
- bundle or artifact sizes if frontend
- current type coverage and `any`/unchecked boundaries

```bash
# Largest files
find . -name '*.ts' -o -name '*.py' -o -name '*.tsx' -o -name '*.js' \
  | grep -v node_modules | grep -v .git \
  | xargs wc -l | sort -rn | head -20

# Directory LOC
find . -not -path '*/node_modules/*' -not -path '*/.git/*' -type f \
  \( -name '*.ts' -o -name '*.py' -o -name '*.tsx' \) \
  | xargs wc -l | sort -rn | head -30

# Type coverage gaps (TypeScript)
grep -rn ': any' src/ --include='*.ts' --include='*.tsx' | wc -l
```

## Product Workflows

Identify the top user workflows and their risk:

- create/read/update/delete loops
- auth and persistence
- slow async/LLM/media/provider operations
- mobile and desktop UX surfaces
- admin/developer/debug views
- deploy and production smoke path

## Existing Safety Net

- What tests exist and what they actually prove?
- Which tests are broad, duplicated, slow, flaky, or low-value?
- Which missing tests block safe refactoring?
- Which screenshots or e2e flows represent real user experience?

## Dirty Worktree Rules

- Treat existing dirty files as user/other-agent work.
- Do not revert or format them unless explicitly asked.
- If they overlap with the requested migration, either work with them or mark the surface as no-touch.
