---
name: add-openhands-reviewer
description: Add OpenHands PR review automation to a GitHub repository by creating or updating the review workflow, wiring the openhands-reviewer trigger, and configuring GitHub App or PAT authentication. Use when asked to install, enable, or wire up OpenHands reviewer / openhands-reviewer on a repo.
compatibility: Requires git, gh or GitHub API access, and permission to edit repo workflows and settings.
triggers:
- add openhands reviewer
- add openhands-reviewer
- install openhands reviewer
- enable openhands reviewer
- enable pr review by openhands
- openhands-reviewer
---

# Add OpenHands reviewer to a repository

Use this skill when the user wants a GitHub repository to support PR review by **openhands-reviewer**.
It is grounded in the final diff between `OpenHands/software-agent-sdk` and `enyst/agent-sdk`, especially commits `c0eddc40`, `e86e67f6`, and `14823aab`.
Do **not** copy the temporary path tweak from `1bf557ed`; it was reverted by `abb5d966`.

## Goal

Leave the target repository with:

1. a PR review workflow under `.github/workflows/`
2. trigger logic that recognizes `openhands-reviewer` and `openhands-reviewer[bot]`
3. authentication wired through a GitHub App (preferred) or PAT fallback
4. required permissions and secret names documented or configured
5. a clear handoff for any secrets or repo settings you could not set yourself

## Inputs to gather

Collect these before editing anything if they are not already obvious:

- target repo and default branch
- whether the repo already has a PR review workflow
- whether review should run automatically on PR open / ready-for-review, or only on manual triggers
- which auth path to use:
  - GitHub App: `OH_REVIEWER_APP_ID` + `OH_REVIEWER_APP_PRIVATE_KEY`
  - PAT fallback: a repo secret such as `OPENHANDS_REVIEWER_GITHUB_TOKEN` or an existing legacy PAT secret name
- LLM secret: `LLM_API_KEY`
- optional repo variables: `LLM_MODEL`, `LLM_BASE_URL`
- whether the repo is reviewing its **own** SDK/action changes or is just a consumer repo

## Core workflow

1. Inspect the repo for existing review workflows and reviewer-related triggers.
2. Decide whether you are implementing the **general repo** pattern or the **self-reviewing SDK/fork** pattern.
3. Create or update the workflow so it:
   - uses `pull_request_target` when the repo must review fork PRs with secrets available in the base repo context
   - sets these permissions:
     ```yaml
     permissions:
       contents: read
       pull-requests: write
       issues: write
     ```
   - includes trigger handling for:
     - `review-this` label
     - `openhands-agent`
     - `openhands-reviewer`
     - `openhands-reviewer[bot]`
     - `all-hands-bot`
4. Prefer the GitHub App flow from the fork diff:
   - `github-app-id: ${{ secrets.OH_REVIEWER_APP_ID }}`
   - `github-app-private-key: ${{ secrets.OH_REVIEWER_APP_PRIVATE_KEY }}`
   - keep `github-token` wired as a fallback PAT path
5. Keep LLM config flexible:
   - `llm-api-key: ${{ secrets.LLM_API_KEY }}`
   - `llm-model: ${{ vars.LLM_MODEL || 'anthropic/claude-sonnet-4-5-20250929' }}`
   - `llm-base-url: ${{ vars.LLM_BASE_URL || '' }}`
6. If the repo is reviewing changes to its own reviewer workflow/action, set:
   - `sdk-repo: ${{ github.repository }}`
   - `sdk-version: ${{ github.event.pull_request.head.sha }}`
7. If secret values are unavailable, still patch the workflow and explicitly tell the user which secrets/variables must be added by an admin.

## Key gotchas from the diff

- Include **both** `openhands-reviewer` and `openhands-reviewer[bot]`. The fork added both because reviewer-request payloads can vary.
- GitHub App auth is now first-class. The composite action prefers the minted installation token and falls back to a PAT only if needed.
- `LLM_BASE_URL` must remain optional. The fork changed it to an empty default so direct provider setups still work.
- The GitHub App needs repo permissions:
  - Pull requests: Read & write
  - Issues: Read & write
  - Contents: Read-only
- If the repo is testing its own SDK/action changes, use `sdk-repo: ${{ github.repository }}` instead of silently reviewing against upstream `main`.
- The stable final state still runs the agent script from `../software-agent-sdk/...`; do not reintroduce the reverted intermediate path change.

## Useful commands

Inspect existing workflow files and reviewer references:

```bash
find .github/workflows -maxdepth 1 -type f 2>/dev/null | sort
rg -n "review-this|openhands-agent|openhands-reviewer|all-hands-bot|pr-review" . 2>/dev/null
```

Set optional repo variables:

```bash
gh variable set LLM_MODEL --body "anthropic/claude-sonnet-4-5-20250929"
gh variable set LLM_BASE_URL --body ""
```

Set secrets only when you actually have the values:

```bash
gh secret set LLM_API_KEY --body "$LLM_API_KEY"
gh secret set OH_REVIEWER_APP_ID --body "$OH_REVIEWER_APP_ID"
gh secret set OH_REVIEWER_APP_PRIVATE_KEY --body "$OH_REVIEWER_APP_PRIVATE_KEY"
```

## When you cannot finish end-to-end

If you can update the workflow but cannot set the required secrets or app credentials, still open a PR with the workflow change and include a short checklist of the missing repository settings.

## References

- `references/reviewer-setup-reference.md`
