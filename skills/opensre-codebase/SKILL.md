---
name: opensre-codebase
description: This skill MUST be used when working in the OpenSRE codebase, enyst/opensre, Tracer-Cloud/opensre, or when creating OpenSRE issues, comments, commits, or pull requests.
triggers:
  - opensre
  - OpenSRE
  - enyst/opensre
  - Tracer-Cloud/opensre
  - open-sre-agent
---

# OpenSRE codebase workflow

Use this skill for all work involving OpenSRE code, issues, comments, reviews, or pull requests. Treat it as mandatory project procedure even for small changes.

## Repository setup

Work in the personal fork by default:

- Fork / working repo: `enyst/opensre`
- Upstream repo: `Tracer-Cloud/opensre`
- Historical docs/support links may mention `Tracer-Cloud/open-sre-agent`; verify the active repo before posting.

Start by verifying remotes and branch state:

```bash
git remote -v
git status --short --branch
```

Keep `origin` pointed at `enyst/opensre`. Add or verify `upstream` points at `Tracer-Cloud/opensre` when comparing issues, templates, or base branches:

```bash
git remote add upstream https://github.com/Tracer-Cloud/opensre.git 2>/dev/null || true
git fetch upstream main
```

Prefer branches in the fork and PRs from `enyst/opensre:<branch>` into `Tracer-Cloud/opensre:main`, unless the user explicitly asks for a PR within the fork.

## Issue-before-PR rule

Read `CONTRIBUTING.md` before opening a PR. OpenSRE's contribution policy requires:

1. Open an issue before opening a PR.
2. Obtain assignment to the issue before opening a PR.
3. Link the issue in the PR template (`Fixes #...`).

Do not open a PR without a linked upstream issue and assignment unless the user explicitly instructs to bypass the policy. If assignment cannot be verified or requested with available permissions, stop and ask the user how to proceed.

Before creating a new issue, search upstream open issues in `Tracer-Cloud/opensre` for duplicates. Include exact and broad searches, for example:

```bash
gh issue list --repo Tracer-Cloud/opensre --state open --limit 200 --json number,title,body,labels,url
gh search issues --repo Tracer-Cloud/opensre --state open "<keywords>" --json number,title,url --limit 20
```

If an appropriate issue already exists, use it instead of creating a duplicate.

## Issue templates are mandatory

Never create a blank OpenSRE issue body. Find and use the appropriate upstream template first:

```bash
find .github/ISSUE_TEMPLATE -maxdepth 1 -type f -print
sed -n '1,220p' .github/ISSUE_TEMPLATE/bug_report.yml
sed -n '1,220p' .github/ISSUE_TEMPLATE/improvement.yml
sed -n '1,220p' .github/ISSUE_TEMPLATE/feature_request.yml
```

Choose the template that matches the work:

- Bug report: broken behavior or reproducible incorrect behavior.
- Improvement: refactor, quality, UX, architecture, or maintenance improvement.
- Feature request: new user-visible capability.

Fill every required field from the selected template. Preserve the template's labels when permissions allow. When using `gh issue create` or the GitHub API instead of the browser form, reconstruct the template headings exactly and pass labels explicitly (for example `--label bug` or `--label enhancement`). Verify labels afterward. If permissions prevent label application, mention this in the handoff.

## PR template is mandatory

Before opening a PR, read the upstream PR template:

```bash
sed -n '1,260p' .github/PULL_REQUEST_TEMPLATE.md
```

Use the template as the PR body. Do not replace it with a free-form summary. Fill at least:

- `Fixes #...` with the assigned upstream issue.
- Change description.
- Demo/screenshot/proof section with test output, log snippet, screenshot, or an explicit reason when not applicable.
- AI usage checklist and implementation approach.
- Review checklist items that are true.

If creating the PR through an API/tool, still pass a body that preserves the template sections.

## AI disclosure and hidden agent details

OpenSRE cares about clear human communication. AI agents are welcome, but significant AI-generated content must be clearly delimited and hidden by default so humans can choose when to expand it.

Use GitHub's HTML disclosure tags for nontrivial AI-generated analysis in issues, comments, PR descriptions, and review replies:

```md
<details>
<summary>AGENT: One sentence summary of the AI-generated content.</summary>

Detailed AI-generated analysis, investigation notes, reproduction reasoning, or implementation explanation goes here.

</details>
```

Rules for this pattern:

- Start the summary text exactly with `AGENT:` followed by a one-sentence description.
- Place the block inside the relevant issue/PR template field, not outside or instead of the template.
- Keep concise human-facing fields visible when needed, then put substantial AI-generated detail in the hidden block.
- Use the standard external-service disclosure sentence when posting content created by OpenHands, for example: `_This issue/comment/PR was created by an AI agent (OpenHands) on behalf of the user._`
- Do not hide critical required facts so thoroughly that maintainers cannot triage the issue. Keep the template answer complete; hide the lengthy agent reasoning.

## Practical checklist

For issues:

1. Verify target repo is upstream `Tracer-Cloud/opensre` unless the user explicitly wants fork-only tracking.
2. Search open upstream issues for duplicates.
3. Read the matching issue template.
4. Fill every required template field.
5. Put significant AI-generated analysis under `<details><summary>AGENT: ...</summary> ... </details>` inside the relevant field.
6. Apply template labels when permissions allow; verify after creation.

For PRs:

1. Verify the linked upstream issue exists and assignment is satisfied.
2. Branch from the fork, not upstream main.
3. Make focused changes and run the required checks from `AGENTS.md`, `CI.md`, and `CONTRIBUTING.md` as applicable.
4. Read and fill `.github/PULL_REQUEST_TEMPLATE.md` exactly.
5. Link the issue with `Fixes #...`.
6. Hide substantial AI-generated explanation in an `AGENT:` details block inside the appropriate PR template section.
7. Push to `enyst/opensre` and open a PR against `Tracer-Cloud/opensre` only when policy requirements are met.
