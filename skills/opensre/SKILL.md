---
name: opensre
description: Contributing to OpenSRE (Tracer-Cloud/opensre) — contribution rules, project context, and maintainer sponsorship path.
triggers:
- opensre
- OpenSRE
- Tracer-Cloud
- sre agent
---

# OpenSRE — Contribution Guide

**Repo:** https://github.com/Tracer-Cloud/opensre
**Fork:** https://github.com/enyst/opensre
**Local clone:** `~/repos/opensre` (origin = enyst fork, upstream = Tracer-Cloud)
**Full dossier:** `~/.smolpaws/private-dossiers/opensre.md`

## Contribution rules (from CONTRIBUTING.md)

- **Bugs & small fixes** → open a PR directly, no issue needed
- **Features / behavioral changes** → file an issue first (feature request template), discuss before coding
- **Improvements** → file an issue first (improvement template)
- **Refactor-only PRs** → only if a maintainer explicitly asked
- **Test/CI-only PRs** → only if required for a real fix maintainers asked for
- **General flow:** find/create issue → request assignment (comment) → fork & branch → code & test → PR linked to issue → review → merge
- Branch naming: `issue/123-short-description` or `fix/...`
- Run before committing: `make lint && make format-check && make typecheck && make test-cov`

## Maintainer sponsorship

$300–500/month for active maintainers. Details in issue #344 and the private dossier.

## Our contributions

- PR #2510 (merged): fix stale model lists
- PR #2608: URL validation tests
- Issues #2517, #2521, #2522: improvements filed
- Comment on #1234: memory discussion
