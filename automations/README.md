# Automations

Versioned OpenHands automation definitions for personal use. Keeping them here makes prompts, triggers, and safety boundaries reviewable in git instead of leaving the only copy in server-side state.

There are two shapes in this directory:

- top-level `*.json` files are direct Automation API request bodies;
- subdirectories are self-contained bundles, usually with an Agent Canvas import file, source prompt, installer, and their own README.

Editing a definition here does **not** update an installed or deployed automation. Import or create it again, or patch the live automation through its API.

## `typescript-client-release-maintainer/` - local release maintenance

A local Agent Canvas automation that polls for automated Agent Server bump PRs in `OpenHands/typescript-client`, inspects generated contract drift, adapts handwritten TypeScript when necessary, validates the existing PR branch, and posts a completion report.

| | |
|---|---|
| Runtime | Local Agent Canvas, Agent Server, and Automation backend |
| Trigger | Hourly cron poll at minute 17, Europe/Stockholm |
| Target | Existing `bump-agent-server-*` PRs in `OpenHands/typescript-client` |
| Write boundary | Existing PR branch and PR comments only |
| Human gate | Never merges or publishes |

See [`typescript-client-release-maintainer/README.md`](typescript-client-release-maintainer/README.md) for installation, credentials, idempotency, and validation.

## `codereview-roasted-pr.json` - Roasted PR Review

Label a pull request `roast-me` and an agent posts a Linus-style review on it.

| | |
|---|---|
| Trigger | GitHub webhook, `pull_request.labeled`, filtered to `label.name == 'roast-me'` |
| Review skill | [`skills/codereview-roasted`](../skills/codereview-roasted) from this repo, invoked via `/codereview-roasted` |
| Posting skill | `skills/github-pr-review` from [OpenHands/extensions](https://github.com/OpenHands/extensions) |
| Timeout | 1800s |

The agent is constrained to review only: it posts a `COMMENT` review, never `APPROVE` or `REQUEST_CHANGES`, does not modify code, and re-checks that the PR is still open at the same head SHA before posting so a force-push mid-run cannot produce a review of a diff that no longer exists.

### Deploy

```bash
OPENHANDS_HOST=https://app.all-hands.dev

curl -X POST "${OPENHANDS_HOST}/api/automation/v1/preset/plugin" \
  -H "Authorization: Bearer ${OPENHANDS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d @automations/codereview-roasted-pr.json
```

Prerequisites:

- The GitHub integration must be connected on the OpenHands account, with access to the repos you want reviewed.
- The `roast-me` label must exist in each repo:

  ```bash
  gh label create roast-me -d "Request a roasted code review"
  ```

### Manage

```bash
# list
curl -H "Authorization: Bearer ${OPENHANDS_API_KEY}" \
  "${OPENHANDS_HOST}/api/automation/v1"

# trigger a run by hand
curl -X POST -H "Authorization: Bearer ${OPENHANDS_API_KEY}" \
  "${OPENHANDS_HOST}/api/automation/v1/{id}/dispatch"

# run history
curl -H "Authorization: Bearer ${OPENHANDS_API_KEY}" \
  "${OPENHANDS_HOST}/api/automation/v1/{id}/runs"
```

To change a deployed automation, call `PATCH /api/automation/v1/{id}` with the changed fields, or delete and recreate it.
