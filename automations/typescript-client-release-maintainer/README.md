# TypeScript client release maintainer

A local Agent Canvas automation for finishing the semantic part of automated Agent Server version bumps in [`OpenHands/typescript-client`](https://github.com/OpenHands/typescript-client).

The existing `software-agent-sdk` release workflow remains responsible for the deterministic work:

1. wait for the released Python packages, Agent Server image, and exact OpenAPI artifact;
2. update the pinned Agent Server version;
3. regenerate the checked-in TypeScript contract;
4. open a `bump-agent-server-*` pull request.

This automation begins after that PR exists. It inspects the generated contract and endpoint audit, decides whether handwritten client code needs adaptation, makes the smallest required change on the existing PR branch, validates it, and comments with the result.

It never merges the PR, publishes npm, changes the package version, or opens a competing bump PR.

## Contents

- `typescript-client-release-maintainer.automation.json`: importable Agent Canvas automation definition.
- `prompt.md`: source prompt used by the automation and API installer.
- `install-local.sh`: creates the automation through a running local Agent Canvas stack.

The definition is stored in git for review and recovery. Editing these files does not mutate an already-installed automation.

## Why this polls GitHub

A normal local Agent Canvas stack is reachable only on localhost, so GitHub cannot deliver webhooks to it directly. The OpenHands Automation backend also expects its built-in GitHub events to arrive through a normalized, HMAC-signed forwarding envelope rather than as an untouched GitHub webhook body.

For the first version, the automation runs hourly at minute 17 and searches for matching open PRs. SDK releases are infrequent, so this avoids maintaining a public webhook relay or permanent tunnel merely to catch one event.

## Prerequisites

- Node.js 22.12 or newer.
- Agent Canvas with the local Agent Server and Automation backend.
- A configured model profile in Agent Canvas.
- GitHub credentials available to the agent under the `enyst` account, with permission to:
  - read and comment on PRs in `OpenHands/typescript-client`;
  - push to same-repository `bump-agent-server-*` branches created by the release bot.

## Install through Agent Canvas

Start the local stack:

```bash
npx @openhands/agent-canvas
```

Then open **Automations**, import:

```text
typescript-client-release-maintainer.automation.json
```

Agent Canvas imports automations disabled. Review the prompt, model profile, GitHub access, schedule, and timeout, then enable it.

A manual dispatch is a useful smoke test. When no matching bump PR exists, a healthy run exits without modifying anything or posting a comment.

## Install through the local API

Start Agent Canvas with an explicit key so the installer can authenticate:

```bash
export LOCAL_BACKEND_API_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
npx @openhands/agent-canvas
```

In another terminal, with the same environment:

```bash
cd automations/typescript-client-release-maintainer
bash install-local.sh
```

The installer calls:

```text
POST /api/automation/v1/preset/prompt
```

It creates the automation disabled and prints its local Agent Canvas URL.

To use a non-default ingress address:

```bash
AGENT_CANVAS_URL=http://127.0.0.1:3000 bash install-local.sh
```

## Idempotency

After a successful run, the automation comments on the PR with a hidden marker tied to the final PR head SHA:

```html
<!-- oh-typescript-client-release-maintainer head=<final-head-sha> status=success -->
```

Later polls skip that exact SHA, but only when the marker was posted by the currently authenticated GitHub account. A human or bot push changes the SHA and causes the PR to be inspected again. Failed runs omit the success marker so the next scheduled run can retry.

## Safety boundaries

The prompt requires the agent to:

- process at most one matching PR per run;
- work only on the existing bump PR branch;
- treat the generated schema and version pin as deterministic inputs;
- avoid unrelated refactors, dependency upgrades, and package releases;
- post no comment when there is no work;
- re-read the remote head SHA after pushing;
- never expose tokens or secret values.

Human review and merge remain the final gate.

## Validation

From the repository root:

```bash
pytest -q tests/test_typescript_client_release_automation.py
```

The test keeps the embedded import prompt synchronized with `prompt.md`, checks the disabled schedule and repository target, asserts the main safety guardrails, and validates the installer with `bash -n`.

## Event-driven mode later

A small public relay could eventually accept GitHub release or PR events, normalize and sign them, then forward them to the local Automation backend. That can replace polling without changing the maintenance prompt. Until such a relay exists, polling is the simpler and less exposed mechanism.
