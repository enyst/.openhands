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

# GitHub forwarders (preserve bare `#NNN` without rewriting commits)

## Problem

If you copy a repository's git commit history into a new repository, GitHub will still render bare references like `#1234` in commit messages, but it will resolve them inside the new repo.

If the new repository does not have an Issue/PR `#1234`, those links break.

## Goal

Make historical bare `#NNN` references work again **without rewriting any git commits** (no commit message rewriting, no SHA changes).

End state:

- A commit message containing `#NNN` in the target repo links to `target#NNN`.
- `target#NNN` exists and contains a forwarder section pointing to the canonical upstream item (issue or PR).

## Non-goals

- Do not rewrite commit history, commit messages, or SHAs.
- Do not migrate real discussions.
- Do not close or lock issues/PRs.

## Key invariant (dense numbering)

GitHub issue/PR numbers are sequential. To make `#NNN` resolvable for all numbers up to `MAX`, the target repo must have a dense namespace:

- For every integer `N` in `[1..MAX]`, `target#N` must exist as either an Issue or a PR.

This means the script will create gap fillers for numbers not referenced by commits, because they are needed to reach later numbers.

## Safety cap

Always enforce a safety cap:

- `MAX_CAP = 14000`

Even if commit history references a larger number, do not touch beyond this cap.

## Forwarder section format

The script prepends a clearly separated banner to the body of `target#NNN`.

Example banner (placeholders):

```md
---
# Forwarder: UPSTREAM_OWNER/UPSTREAM_REPO#NNN

This item exists in **TARGET_OWNER/TARGET_REPO** to preserve historical `#NNN` references in commit messages.

**Canonical location:** https://github.com/UPSTREAM_OWNER/UPSTREAM_REPO/(issues|pull)/NNN

> This is an auto-generated forwarder. Please do not rely on discussion here.
---

<!-- forwarder: UPSTREAM_OWNER/UPSTREAM_REPO#NNN -->
```

If the target item already has content, the script keeps it by prepending:

```md
---

## Original content

(kept below)

---
```

## Script behavior (high level)

For each integer `N` in `[START..MAX]` (in order):

1. Read `upstream#N` via GitHub API.
   - If missing (404), still ensure `target#N` exists as a gap filler and state that upstream is missing.
2. Read `target#N` via GitHub API.
   - If missing (404): create a new issue.
     - Hard stop: the created issue number must equal `N`. If not, STOP immediately to avoid number drift.
   - If present:
     - If the exact marker `<!-- forwarder: OpenHands/OpenHands#N -->` is already present, do nothing.
     - If any other forwarder marker is present, hard stop (manual review required).
     - Otherwise, prepend the banner.
3. Ensure the label `forwarder` exists on `target#N`.

## Idempotency / restartability

- Idempotency is enforced by an exact marker match for the expected upstream repo + number.
- If a different marker is detected, the script stops immediately.
- Progress is tracked in a state file (default: `.forwarders/state.json`).
- Every processed number appends a JSONL record (default: `.forwarders/run.jsonl`).

## No-linkify mode (recommended for first runs)

By default, GitHub may turn upstream references into links and cross-repo references (which can trigger notifications).

For initial staging runs, pass:

- `--no-linkify-upstream`

This renders the upstream token (e.g. `OpenHands/OpenHands#1234`) and the canonical URL as inline code so it is easy to copy/paste, but GitHub should not treat it as an actionable link.

## Dry-run semantics

`--dry-run` performs no GitHub writes, but it still:

- reads upstream + target items,
- writes the JSONL log,
- updates the state file.

This is intentional so you can inspect what would happen and then resume.

## Important: dry-run and state files

By default, the script records progress in the state file even during `--dry-run`.

This is useful for inspection, but it also means that if you re-run *without* `--dry-run` using the same `--state-file`, the script will resume from the next number and may skip work you expected it to perform.

Recommended practice:

- Use a separate state/log location for dry-run (e.g. `--state-file .forwarders/dry-run-state.json --log-file .forwarders/dry-run.jsonl`), then switch to the default state/log for the real run.
- Or delete the dry-run state file before the real run.



## Safety checklist before running

- Disable bots that create issues/PRs in the target repo (Dependabot, etc.).
- Disable GHCR-pushing workflows (e.g. Docker) to avoid publishing side effects.
- Start with a small range (e.g. `--max 100`) on a staging repo.

## Rate limiting

The script includes basic automatic retry handling for GitHub rate limiting:

- Retries on HTTP 403/429 when rate-limit headers or rate-limit messages are detected.
- Uses `Retry-After` when present, otherwise sleeps until `X-RateLimit-Reset` (+ a small buffer).
- Falls back to exponential backoff when only a rate-limit message is available.

Tuning flags:

- `--api-max-retries`
- `--api-backoff-base-seconds`
- `--api-reset-buffer-seconds`

## Commands

Scan commit history (local clone) to find the maximum referenced `#NNN`:

```bash
python3 <this-skill-path>/scripts/scan_commit_refs.py \
  --repo-path <path-to-target-clone> \
  --rev main
```

Run forwarder sync (recommended staged rollout).

The example below targets a staging repo (`enyst/openhands-web`). For production, substitute your real target (e.g. `OpenHands/OpenHands-Web`).


```bash
python3 <this-skill-path>/scripts/sync_forwarders.py \
  --upstream OpenHands/OpenHands \
  --target enyst/openhands-web \
  --git-repo-path <path-to-local-clone-of-enyst-openhands-web> \
  --start 1 \
  --max 100 \
  --max-cap 14000 \
  --no-linkify-upstream \
  --dry-run
```

Remove `--dry-run` for the real run.
