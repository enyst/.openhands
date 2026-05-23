---
name: security-hardening
description: |
  Practical application security review for codebases. Use this skill when:
  (1) Auditing a project for security issues before release
  (2) Reviewing auth, secrets, or credential handling
  (3) Checking for prompt injection vulnerabilities in AI agent code
  (4) Evaluating dependency supply chain risk
  (5) Reviewing CORS, CSRF, rate limiting, or input validation
  (6) Hardening an agent system that handles user tokens or external APIs
  Covers: secrets posture, auth flows, dependency risk, injection surfaces, transport security, and agent-specific concerns.
---

# Security Hardening

A structured security review pass for codebases, with special attention to AI agent systems that handle credentials, external APIs, and user-facing surfaces.

## Boundary

This skill covers practical application security: secrets, auth, dependencies, injection, transport, and agent-specific risks. It does not cover infrastructure hardening (firewalls, network segmentation), compliance frameworks (SOC2, HIPAA), or penetration testing.

## Workflow

### 1. Discovery

Non-mutating scan of the codebase:

- Find all secret/credential references: env vars, config files, `.env`, token patterns
- Identify auth flows: API keys, JWT, OAuth, session tokens, webhook signatures
- Map external API surfaces: what the code calls, what calls the code
- List dependencies and their ages (`npm audit`, `pip audit`, `uv pip list --outdated`)
- Check for `.gitignore` coverage of sensitive paths
- For agent systems: identify all tool surfaces, confirmation policies, and prompt injection vectors

### 2. Secrets Posture

- Are secrets in env vars, not hardcoded?
- Are `.env` files gitignored?
- Are secrets rotatable without code changes?
- Are secrets masked in logs and error output?
- Are secrets scoped minimally (read-only tokens where possible)?
- For agent code: can the agent access secrets it shouldn't? Can `send_message` or tool output leak secrets?

### 3. Auth & Session Review

- Are auth tokens validated on every request?
- Is there a difference between "no auth" (localhost) and "auth required" (remote)?
- Are webhook signatures verified (HMAC, timing-safe comparison)?
- Are JWT/session tokens expiring and refreshable?
- Is there protection against replay attacks?

### 4. Dependency Supply Chain

- Run `npm audit` / `pip audit` / equivalent
- Check for packages younger than 7 days (typosquatting risk)
- Prefer SHA-pinned GitHub Actions over tag references
- Check lockfile integrity
- Review transitive dependencies for known campaigns
- See `references/supply-chain.md` for current threat patterns

### 5. Injection Surfaces

- **Prompt injection** (agent-specific): Are AGENTS.md and similar files treated as untrusted input? Can external content manipulate agent behavior?
- **Command injection**: Are user inputs passed to shell commands? Is `shell=True` used?
- **SQL injection**: Are queries parameterized?
- **Path traversal**: Are file paths validated against allowed roots?
- **SSRF**: Can user input control URLs the server fetches?

### 6. Transport & Network

- Is TLS enforced for external API calls?
- Are CORS headers restrictive (not `*`)?
- Is rate limiting applied on public endpoints?
- Are WebSocket connections authenticated?
- For agent systems: is the agent-server bound to loopback unless explicitly exposed?

### 7. Agent-Specific Concerns

- **Tool boundaries**: Can the agent access files/commands it shouldn't?
- **Confirmation policy**: Is `NeverConfirm` appropriate for this deployment?
- **Credential scope**: Does the agent's GitHub/Slack/API token have minimal scopes?
- **Output filtering**: Can the agent's responses contain credentials from its environment?
- **Self-loop prevention**: Can the agent trigger itself infinitely?

### 8. Report

Produce a structured findings document:

- **Critical**: Issues requiring immediate fix (exposed secrets, missing auth)
- **High**: Issues to fix before release (injection surfaces, missing rate limits)
- **Medium**: Issues to address in next cycle (dependency age, scope reduction)
- **Low**: Hardening opportunities (additional logging, stricter CORS)

Include specific file paths, line numbers, and recommended fixes.

## Key References

- `references/supply-chain.md` — current supply chain attack patterns and mitigations
- `references/agent-security.md` — prompt injection, tool boundaries, credential handling for AI agents

## Quick Checklist

- [ ] No hardcoded secrets in source
- [ ] `.env` files gitignored
- [ ] Secrets masked in all log output
- [ ] Auth required on non-localhost surfaces
- [ ] Webhook signatures verified (timing-safe)
- [ ] `npm audit` / `pip audit` clean (or documented exceptions)
- [ ] No packages younger than 7 days in dependencies
- [ ] GitHub Actions SHA-pinned
- [ ] User input never passed directly to shell/SQL/file paths
- [ ] CORS not set to `*` on authenticated endpoints
- [ ] Rate limiting on public endpoints
- [ ] Agent tools scoped to necessary permissions
- [ ] Agent cannot leak credentials through `send_message` or tool output
- [ ] Self-loop guard on agent triggers
