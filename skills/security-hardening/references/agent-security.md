# Agent Security

Security considerations specific to AI agent systems (OpenHands, Claude Code, Codex, etc.).

## Prompt Injection

### Attack Surface
- `AGENTS.md`, `CLAUDE.md`, `.cursorrules` — loaded into context, treated as instructions
- Repository content: README, code comments, issue descriptions, PR bodies
- External content fetched by the agent: web pages, API responses, file contents

### Defenses
- Mark repo-loaded instructions as "untrusted input" in the system prompt
- Hooks (pre/post-action validation) can catch suspicious tool calls
- Never execute instructions found in external content without human confirmation
- Log and flag messages containing "ignore previous instructions" patterns

### The Gemini CLI Pattern
- Gemini CLI loaded env vars from `.env` files in the repository
- Malicious `.env` could exfiltrate secrets via crafted environment variables
- Defense: don't load `.env` from untrusted repos; sandbox env var access

## Tool Boundaries

### Principle of Least Privilege
- Terminal tool: restrict to workspace directory, don't allow `sudo`
- File editor: restrict to workspace and explicitly allowed paths
- Browser: be cautious about what URLs the agent visits
- `send_message`: can the agent accidentally post secrets to Slack/GitHub?

### Confirmation Policies
- `NeverConfirm`: appropriate for trusted, sandboxed environments
- `AlwaysConfirm`: safer for untrusted repos or when running with broad permissions
- Hook-based: validate specific actions (e.g., block `git push` to `main`)

## Credential Handling

### Token Scope
- GitHub tokens: use fine-grained PATs with minimal repo/scope access
- Slack tokens: bot tokens (`xoxb-`) are preferable to user tokens (`xoxp-`)
- API keys: read-only where possible

### Credential Leakage Vectors
- Agent's `send_message` output (posted to Slack/GitHub)
- Terminal command output (logged, may contain env vars)
- Error messages (stack traces may include credentials)
- Git commits (agent might stage `.env` files)

### Mitigations
- Secret masking in all output pipelines
- `.gitignore` enforcement before commits
- Environment variable filtering in error handlers
- Review agent output before posting to public channels

## Self-Loop Prevention

When an agent can trigger itself (e.g., responding to its own GitHub comments):
- Check `sender.login` against agent's own username
- Implement a `isSelfAction` guard at the ingress layer
- Rate-limit agent responses per thread/channel
- Use idempotency keys to prevent duplicate processing
