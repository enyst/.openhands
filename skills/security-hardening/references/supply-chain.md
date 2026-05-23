# Supply Chain Security

## Current Threat Landscape

Package registry attacks are increasing in sophistication. Common patterns:

### Typosquatting
- Packages with names similar to popular libraries (e.g., `reqeusts` vs `requests`)
- Mitigation: use lockfiles, verify package names before install, avoid `pip install` from untrusted prompts

### Dependency Confusion
- Attackers publish internal package names to public registries with higher version numbers
- Mitigation: configure scoped registries, use private registry priority

### Compromised Maintainer Accounts
- Legitimate packages get malicious updates after account takeover
- Mitigation: pin exact versions in lockfiles, review changelogs on updates, wait 7 days for new versions

### GitHub Actions Supply Chain
- Actions referenced by tag (e.g., `actions/checkout@v4`) can be re-tagged to point at malicious code
- Mitigation: SHA-pin all Actions (e.g., `actions/checkout@b4ffde65f...`)
- Dependabot can auto-update SHA pins

## Practical Mitigations

1. **Lockfiles**: always commit `package-lock.json`, `uv.lock`, `poetry.lock`
2. **7-day rule**: don't install packages published less than 7 days ago
3. **Audit regularly**: `npm audit`, `pip audit`, `uv pip audit`
4. **SHA-pin Actions**: use full commit SHA, not tags
5. **Review transitive deps**: `npm ls`, `pip show <pkg>` for dependency trees
6. **AGENTS.md guidance**: instruct AI agents to follow these rules when installing packages
7. **PR review prompts**: include supply chain checks in automated review instructions
