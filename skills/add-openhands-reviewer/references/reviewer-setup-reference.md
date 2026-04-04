# OpenHands reviewer setup reference

This reference captures the final effective behavior in the compare range:

- base: `OpenHands/software-agent-sdk@main`
- head: `enyst/agent-sdk@main`

Focus on the final range diff, not every transient intermediate commit.
Commit `1bf557ed` changed the runtime script path, but `abb5d966` reverted it, so that path change is **not** part of the final implementation to copy.

## What the fork changed

### 1. GitHub App auth inside the composite action (`c0eddc40`)

The fork updated `.github/actions/pr-review/action.yml` so the workflow can pass either:

- a PAT via `github-token`, or
- GitHub App credentials via `github-app-id` + `github-app-private-key`

Important details from the diff:

- `github-token` became optional instead of required.
- Two new inputs were added:
  - `github-app-id`
  - `github-app-private-key`
- The composite action now runs `actions/create-github-app-token@v1` when both app inputs are present.
- It mints the installation token against the **base repository owner/name** from the PR event:
  - `owner: ${{ github.event.pull_request.base.repo.owner.login }}`
  - `repositories: ${{ github.event.pull_request.base.repo.name }}`
- The action validates auth using:
  - `steps.github-app-token.outputs.token || inputs.github-token`

That means the workflow file does **not** need to mint the installation token itself. It only has to pass the app secrets through.

### 2. Reviewer trigger expansion (`c0eddc40`)

The fork extended workflow trigger logic so a review can start when a maintainer requests:

- `openhands-agent`
- `openhands-reviewer`
- `openhands-reviewer[bot]`
- `all-hands-bot`

The extra `openhands-reviewer[bot]` case matters. If you only check for `openhands-reviewer`, some reviewer-request events may not match the actual login exposed by GitHub.

### 3. Action source switched to the fork (`e86e67f6`)

The workflow changed from:

```yaml
uses: OpenHands/software-agent-sdk/.github/actions/pr-review@main
```

to:

```yaml
uses: enyst/agent-sdk/.github/actions/pr-review@main
```

Why it matters:

- In the compare range, the fork is where the new GitHub App auth and reviewer-trigger behavior exists.
- If you want the exact behavior from this diff before it exists upstream, point at the forked action source.
- If the same functionality later lands upstream, you can switch back.

### 4. LLM config and self-reviewing repo support (`14823aab`)

The forked workflow also changed these details:

- `llm-model` now defaults from `vars.LLM_MODEL`, falling back to `anthropic/claude-sonnet-4-5-20250929`
- `llm-base-url` now defaults from `vars.LLM_BASE_URL`, falling back to an empty string
- `sdk-repo` is set to `${{ github.repository }}` for self-reviewing repos
- `sdk-version` is set to the PR head SHA so the review job uses the exact code under review

Use those self-review settings when the repo being reviewed is itself the SDK/action repo or another repo that needs the action to test PR changes from that same repository.

For ordinary consumer repos, the self-review settings are usually unnecessary.

## Required repository permissions

The example workflow comments added a concrete permission checklist for the GitHub App path:

- Pull requests: Read & write
- Issues: Read & write
- Contents: Read-only

These permissions belong to the GitHub App installation. The workflow file itself should also declare:

```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
```

## Recommended default workflow template

Use this when enabling OpenHands reviewer on a normal GitHub repository and you want support for fork PRs.

```yaml
name: PR Review by OpenHands

on:
  pull_request_target:
    types: [opened, ready_for_review, labeled, review_requested]

permissions:
  contents: read
  pull-requests: write
  issues: write

jobs:
  pr-review:
    if: |
      (github.event.action == 'opened' && github.event.pull_request.draft == false && github.event.pull_request.author_association != 'FIRST_TIME_CONTRIBUTOR' && github.event.pull_request.author_association != 'NONE') ||
      (github.event.action == 'ready_for_review' && github.event.pull_request.author_association != 'FIRST_TIME_CONTRIBUTOR' && github.event.pull_request.author_association != 'NONE') ||
      github.event.label.name == 'review-this' ||
      github.event.requested_reviewer.login == 'openhands-agent' ||
      github.event.requested_reviewer.login == 'openhands-reviewer' ||
      github.event.requested_reviewer.login == 'openhands-reviewer[bot]' ||
      github.event.requested_reviewer.login == 'all-hands-bot'
    concurrency:
      group: pr-review-${{ github.event.pull_request.number }}
      cancel-in-progress: true
    runs-on: ubuntu-24.04
    steps:
      - name: Run PR Review
        uses: enyst/agent-sdk/.github/actions/pr-review@main
        with:
          llm-model: ${{ vars.LLM_MODEL || 'anthropic/claude-sonnet-4-5-20250929' }}
          llm-base-url: ${{ vars.LLM_BASE_URL || '' }}
          review-style: roasted
          llm-api-key: ${{ secrets.LLM_API_KEY }}
          github-app-id: ${{ secrets.OH_REVIEWER_APP_ID }}
          github-app-private-key: ${{ secrets.OH_REVIEWER_APP_PRIVATE_KEY }}
          github-token: ${{ secrets.OPENHANDS_REVIEWER_GITHUB_TOKEN }}
```

Notes:

- The PAT input stays wired as a fallback even when the GitHub App path is preferred.
- If the repo already standardizes on a different PAT secret name, reuse that name instead of renaming everything.
- `LLM_BASE_URL` should stay optional.

## Self-reviewing SDK/fork template

Use this only when the repository being reviewed should run the reviewer against the current PR's version of the SDK/action logic.

```yaml
name: PR Review by OpenHands

on:
  pull_request_target:
    types: [opened, ready_for_review, labeled, review_requested]

permissions:
  contents: read
  pull-requests: write
  issues: write

jobs:
  pr-review:
    if: |
      (github.event.action == 'opened' && github.event.pull_request.draft == false && github.event.pull_request.author_association != 'FIRST_TIME_CONTRIBUTOR' && github.event.pull_request.author_association != 'NONE') ||
      (github.event.action == 'ready_for_review' && github.event.pull_request.author_association != 'FIRST_TIME_CONTRIBUTOR' && github.event.pull_request.author_association != 'NONE') ||
      github.event.label.name == 'review-this' ||
      github.event.requested_reviewer.login == 'openhands-agent' ||
      github.event.requested_reviewer.login == 'openhands-reviewer' ||
      github.event.requested_reviewer.login == 'openhands-reviewer[bot]' ||
      github.event.requested_reviewer.login == 'all-hands-bot'
    concurrency:
      group: pr-review-${{ github.event.pull_request.number }}
      cancel-in-progress: true
    runs-on: ubuntu-24.04
    steps:
      - name: Run PR Review
        uses: enyst/agent-sdk/.github/actions/pr-review@main
        with:
          llm-model: ${{ vars.LLM_MODEL || 'anthropic/claude-sonnet-4-5-20250929' }}
          llm-base-url: ${{ vars.LLM_BASE_URL || '' }}
          review-style: roasted
          sdk-repo: ${{ github.repository }}
          sdk-version: ${{ github.event.pull_request.head.sha }}
          llm-api-key: ${{ secrets.LLM_API_KEY }}
          github-app-id: ${{ secrets.OH_REVIEWER_APP_ID }}
          github-app-private-key: ${{ secrets.OH_REVIEWER_APP_PRIVATE_KEY }}
          github-token: ${{ secrets.ALLHANDS_BOT_GITHUB_PAT }}
          lmnr-api-key: ${{ secrets.LMNR_SKILLS_API_KEY }}
```

## Manual-only variant

If the repo owner wants to avoid automatic review on PR open / ready-for-review, keep the same job body but reduce the event types to:

```yaml
on:
  pull_request_target:
    types: [labeled, review_requested]
```

and simplify the `if:` clause to only the label and reviewer-login checks.

## Secret and variable checklist

### Required secrets

- `LLM_API_KEY`
- one of:
  - `OH_REVIEWER_APP_ID` + `OH_REVIEWER_APP_PRIVATE_KEY`, or
  - a PAT secret such as `OPENHANDS_REVIEWER_GITHUB_TOKEN`

### Optional secrets

- `LMNR_SKILLS_API_KEY`

### Optional repo variables

- `LLM_MODEL`
- `LLM_BASE_URL`

## Verification checklist

After editing the workflow:

1. Confirm all secret names referenced in YAML actually exist or have an explicit follow-up note.
2. Confirm both reviewer aliases are present:
   - `openhands-reviewer`
   - `openhands-reviewer[bot]`
3. Confirm the workflow file uses `contents: read`, `pull-requests: write`, `issues: write`.
4. Confirm `pull_request_target` is intentional and documented.
5. If this is a self-reviewing repo, confirm `sdk-repo` and `sdk-version` are set.
6. If there is already an open PR for testing, trigger the workflow by either:

```bash
gh pr edit <pr-number> --add-label review-this
```

or, for reviewer-request testing:

```bash
gh api \
  -X POST \
  repos/<owner>/<repo>/pulls/<pr-number>/requested_reviewers \
  -f reviewers[]=openhands-reviewer
```

If requesting `openhands-reviewer` fails because the app is not installed or not available as a reviewer, stop and tell the user to install/configure the GitHub App before expecting reviewer-request triggers to work.
