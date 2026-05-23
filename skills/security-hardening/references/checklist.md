# Security Hardening Checklist

## Authentication and Authorization

- Session creation, renewal, revocation, cookie flags.
- Role checks on server-side mutations and reads.
- API key scope, storage, rotation, and revocation.
- Admin-only surfaces and hidden client-only checks.
- Webhook signature verification (timing-safe HMAC).
- For agents: confirmation policy appropriate for deployment context.

## Input and Network Risk

- Runtime validation on API/body/query/path/provider payloads.
- SSRF: URL parsing, protocol allowlist (`https` only unless justified), private IP blocking, redirect following limits.
- File upload/download: MIME sniffing prevention, extension checks, size limits, storage path traversal.
- CORS/CSRF policy and unsafe methods.
- Rate limits and abuse controls on public endpoints.
- WebSocket authentication on connect.

## Secrets and Logging

- `.env`, deploy env, CI secrets, provider tokens — all gitignored.
- Secret leakage into client bundle, logs, screenshots, fixtures, analytics.
- Error envelopes that do not expose stack traces or provider raw payloads.
- For agents: `send_message` and tool output cannot contain credentials.

## Dependencies

- Package manager audit (`npm audit`, `pip audit`).
- Lockfile review for unexpected packages.
- Postinstall/build scripts inspection.
- Known CVEs, stale critical deps, abandoned packages.
- Package age check (7-day rule for new packages).
- GitHub Actions SHA-pinned (not tag-referenced).

## Agent-Specific

- Tool boundaries: workspace-scoped file access, no unnecessary `sudo`.
- Prompt injection: repo-loaded files treated as untrusted input.
- Self-loop prevention: agent cannot trigger itself infinitely.
- Credential scope: minimal permissions on all tokens.
- Output filtering: no secrets in agent responses posted externally.

## Output

- Severity-ranked findings with file paths and line numbers.
- Fixed issues with test evidence.
- Deferred risks with owner/action and severity.
- Explicit scope statement (what was reviewed, what was not).
