# Automations

Deployable OpenHands Cloud automation definitions. Each `*.json` is the request body for a
[`POST /api/automation/v1/preset/plugin`](https://docs.openhands.dev) call — the definitions live here
so they are reviewable in git rather than only existing as server-side state.

## `codereview-roasted-pr.json` — Roasted PR Review

Label a pull request `roast-me` and an agent posts a Linus-style review on it.

| | |
|---|---|
| Trigger | GitHub webhook, `pull_request.labeled`, filtered to `label.name == 'roast-me'` |
| Review skill | [`skills/codereview-roasted`](../skills/codereview-roasted) from this repo, invoked via `/codereview-roasted` |
| Posting skill | `skills/github-pr-review` from [OpenHands/extensions](https://github.com/OpenHands/extensions) |
| Timeout | 1800s |

The agent is constrained to review only: it posts a `COMMENT` review (never `APPROVE` /
`REQUEST_CHANGES`), does not modify code, and re-checks that the PR is still open at the same head
SHA before posting so a force-push mid-run cannot produce a review of a diff that no longer exists.

### Deploy

```bash
OPENHANDS_HOST=https://app.all-hands.dev

curl -X POST "${OPENHANDS_HOST}/api/automation/v1/preset/plugin" \
  -H "Authorization: Bearer ${OPENHANDS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d @automations/codereview-roasted-pr.json
```

Prerequisites:

- The GitHub integration must be connected on the OpenHands account, with access to the repos you
  want reviewed.
- The `roast-me` label must exist in each repo (`gh label create roast-me -d "Request a roasted code review"`).

### Manage

```bash
# list
curl -H "Authorization: Bearer ${OPENHANDS_API_KEY}" "${OPENHANDS_HOST}/api/automation/v1"

# trigger a run by hand
curl -X POST -H "Authorization: Bearer ${OPENHANDS_API_KEY}" \
  "${OPENHANDS_HOST}/api/automation/v1/{id}/dispatch"

# run history
curl -H "Authorization: Bearer ${OPENHANDS_API_KEY}" \
  "${OPENHANDS_HOST}/api/automation/v1/{id}/runs"
```

Editing the JSON here does **not** update a deployed automation. `PATCH /api/automation/v1/{id}`
with the changed fields, or delete and recreate.
