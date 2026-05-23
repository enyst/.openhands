---
name: antislop-codebase
description: |
  Analyze and transform messy, prototype, overgrown, or hard-to-maintain repositories into maintainable product-shaped codebases while preserving existing product behavior. Use when the user asks to antislop a codebase, clean up a messy repo, run a maintainability migration, write a refactor plan, modernize structure, improve type boundaries, harden tests, reduce large files, clean architecture, coordinate subagent-driven refactors, or produce a final migration audit. Do not use for broader production-readiness specialties such as security audits, observability/logging programs, compliance hardening, or reliability engineering unless the user explicitly scopes those as part of the maintainability refactor.
---

# Antislop Codebase

Use this skill to move a repo from "works but hurts" to a product-shaped cluster of small, typed, tested, maintainable modules while keeping the current product essentially as-is. Treat this as the first maintainability/productization pass, not the broader production-readiness program.

## Boundary

This skill is for structural maintainability: code organization, typed boundaries, tests, feature folders, API consolidation, file-size reduction, styling cleanup, and audit evidence.

Do not expand the scope into a full production-readiness initiative. Observability/logging programs, security reviews, compliance, incident response, SLOs, runbooks, secrets posture, penetration testing, and deep reliability engineering belong in separate follow-on skills (see `security-hardening`) unless the user explicitly asks to include a small enabling change.

## Operating Principles

- Preserve behavior first. Improve architecture in thin, reversible slices.
- Ground every decision in repo facts: file sizes, dependency graph, tests, runtime shape, API surfaces, user workflows, deployment limits, and current dirty worktree.
- Keep files AI-editable: prefer focused modules under roughly 300–500 lines, explicit feature folders, stable compatibility barrels, and narrow tests.
- Never rewrite active user-owned areas without permission. If other agents/users are editing a surface, audit or work around it.
- Use concurrent subagents for independent analysis or isolated edit slices when available, but merge with one owner who validates the whole tree.
- Commit at green checkpoints. Do not let a migration become a giant unreviewable diff.
- End with evidence: a migration audit with visuals, metrics, risks, and before/after interpretation.

## Workflow

### 1. Establish the Product Shape

Run a quick non-mutating discovery pass before planning:

- Find package scripts, app entrypoints, API routes, deployment config, test harnesses, type config, and current git status.
- Measure largest files and top directories.
- Identify user-critical workflows, deployment constraints, data persistence, auth, provider integrations, and expensive operations only insofar as they affect safe refactoring.
- Read recent commits and docs to avoid undoing active work.

If the repo is live or user-facing, default to compatibility-preserving migrations and rollback paths.

For deeper discovery prompts and commands, see [analysis-checklist.md](references/analysis-checklist.md).

### 2. Write a Decision-Complete Migration Plan

Produce a plan that can evolve, but is complete enough for another agent to execute:

- Goal, success criteria, explicit non-goals, active no-touch areas, and risk posture.
- Staged slices ordered by blast radius and verification confidence.
- Public interfaces and compatibility promises.
- Test plan: current baseline, new tests needed, e2e/visual checks, deploy smokes.
- Concurrency map: which workers can edit independently and which files are single-owner.
- Checkpoint policy: when to commit, push, deploy, and audit.

Ask the user to confirm the plan before executing. Only ask about product tradeoffs that cannot be discovered from the repo.

### 3. Build the Baseline Safety Net

Before broad edits:

- Run existing typecheck, unit tests, build, and e2e if practical.
- If tests are missing, add or plan the smallest high-value characterization tests before refactoring behavior.
- Add only minimal diagnostics or recoverable error handling needed to make the refactor safe; defer comprehensive logging/observability programs to a separate skill.
- Capture screenshots for core UX surfaces when practical.

### 4. Execute in Green Slices

Process the migration methodically:

- Split largest and hottest files first, preserving old import surfaces through barrels/facades.
- Extract pure models/helpers before UI shells.
- Convert untyped or ad hoc boundaries to shared domain types and runtime validation where API/provider data crosses a trust boundary.
- Consolidate duplicated server/API functions only after response shapes are pinned by tests.
- Migrate styling surface-by-surface; remove legacy selectors only after screenshot checks.
- Keep each slice small enough to test, review, and revert.

Use up to the user-approved subagent concurrency. Assign workers to independent surfaces. Do not let subagents edit the same hot files concurrently.

For execution rules and worker prompts, see [execution-playbook.md](references/execution-playbook.md).

### 5. Validate, Commit, Deploy

At each checkpoint:

- Run the narrow tests for the touched surface.
- Run broader typecheck/build/unit tests before committing.
- Run e2e/visual smoke before deploy when UI or production flows changed.
- Commit only the intended files; preserve unrelated dirty user work.
- Deploy only when the agreed release gate is green, or explicitly mark a known-risk release.

### 6. Finish with a Migration Audit

When the migration is stable, produce a structured audit that answers:

- Did maintainability improve?
- How many LOC/files were added/removed?
- Which file sizes collapsed?
- How did the structure evolve?
- What changed in tests, types, API functions, deployment risk, and UX coverage?
- What costs and risks remain?

Use [audit-microsite.md](references/audit-microsite.md) for metrics, structure, and validation. The audit can be a markdown report or a static HTML microsite served locally.

## Subagent Pattern

For large repos, independent cleanup slices can run concurrently.

Via OpenHands CLI:
```bash
openhands --headless --json -t "Extract the auth helpers from src/server.ts into src/auth/index.ts. Keep the old imports working via re-export. Run tests after."
```

Via the agent-server API:
```bash
curl -X POST "$AGENT_SERVER_URL/api/conversations" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"initial_message": "...", "agent": {"tools": [{"name": "terminal"}, {"name": "file_editor"}]}}'
```

Good parallel lanes: test characterization, large-file splitting, CSS dead selector audit, server/provider helper extraction, type-boundary tightening, documentation/audit metrics.

Bad parallel lanes: multiple workers changing the same app shell, simultaneous route and client contract changes, formatting sweeps while feature edits are active, edits inside user-declared active work areas.

## Quality Bar

A successful antislop migration has:

- No giant ownership-free files in hot paths.
- Clear feature/provider/domain folders.
- Typed module boundaries for frontend/backend/API/provider data.
- Tests that carry their weight and can be run narrowly.
- Production-shaped local/dev deploy checks.
- A final audit artifact that is honest about wins, costs, and residual risks.
