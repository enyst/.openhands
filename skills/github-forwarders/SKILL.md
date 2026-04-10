---
name: github-forwarders
description: Create numbered forwarder issues/PR body banners to preserve bare #NNN references in commit history without rewriting git commits. Use for staging repos like enyst/openhands-web and eventually OpenHands/OpenHands-Web.
triggers:
  - forwarder issues
  - preserve #1234 references
  - make #1234 links work
  - create thousands of issues
  - github issue forwarders
---

# GitHub forwarders (no history rewriting)

## Goal

Preserve historical bare `#NNN` references in **commit messages** when the commit history has been copied to another repository (e.g. `OpenHands/OpenHands` → `OpenHands/OpenHands-Web`) **without rewriting any git commits**.

End state:

- A commit message containing `#NNN` in the *target* repo links to `target#NNN`.
- `target#NNN` exists and contains a clearly separated forwarder section linking to the canonical upstream `upstream#NNN`.

## Non-goals

- Do **not** rewrite commit history, commit messages, or SHAs.
- Do **not** close or lock issues/PRs (including those created by the script).

## Key invariant

To ensure `#NNN` is resolvable for all references up to some number `MAX`, the target repo must have a dense namespace:

- for every integer `N` in `[1..MAX]`, `target#N` must exist as either an Issue or a PR.

This implies the script may need to create **gap fillers** (numbers not referenced by any commit).

## Hard cap

Always enforce a safety cap:

- `MAX_CAP = 14000`

Even if commit history references a larger number, the script must not create or modify beyond this cap.

## Forwarder section format

The script prepends the following block to the body of `target#NNN`.

```md
---
# Forwarder: OpenHands/OpenHands#NNN

This item exists in **OpenHands/OpenHands-Web** to preserve historical `#NNN` references in commit messages.

**Canonical location:** https://github.com/OpenHands/OpenHands/(issues|pull)/NNN

> This is an auto-generated forwarder. Please do not rely on discussion here.
---

<!-- forwarder: OpenHands/OpenHands#NNN -->
```

When the item already has content, prepend additionally:

```md
---

## Original content

(kept below)

---
```

## Script behavior

For each integer `N` in `[START..MAX]` (in order):

1. Read `upstream#N` (Issue/PR) via GitHub API.
   - If upstream is missing (404), still create/update `target#N` as a **gap filler** that states the upstream item is missing.
2. Read `target#N` via GitHub API.
   - If missing (404): create a new **issue**.
     - **Hard stop:** the created issue number must equal `N`. If not, STOP immediately.
   - If present: prepend forwarder section unless marker already exists.
3. Ensure label `forwarder` exists on `target#N`.

## Idempotency / restartability

- The body marker `<!-- forwarder: OpenHands/OpenHands#NNN -->` makes the operation idempotent.
- A state file tracks the next number to process (resume after interruption).
- Every operation must be logged as JSONL for auditing.

## Safety

- Pause/disable automation that creates PRs/issues in the target repo during the run (e.g. Dependabot), otherwise numbering may drift.
- Disable GHCR-pushing workflows (e.g. `Docker`) to avoid publishing side effects during mass updates.

## Commands

Scan commit history (local clone) to discover the maximum referenced `#NNN`:

```bash
python3 <this-skill-path>/scripts/scan_commit_refs.py --repo-path <path-to-target-clone> --rev main
```

Create/update forwarders up to the discovered max (but never beyond 14000):

```bash
python3 <this-skill-path>/scripts/sync_forwarders.py \
  --upstream OpenHands/OpenHands \
  --target OpenHands/OpenHands-Web \
  --git-repo-path <path-to-target-clone> \
  --start 1 \
  --dry-run
```

Remove `--dry-run` for the real run.
