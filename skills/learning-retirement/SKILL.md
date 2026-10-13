---
name: learning-retirement
description: Record when a temporary engineering lesson stops applying, or check whether one is obsolete. Use while saving verified project learnings or when asked to refresh a specific learning. Does not sweep or delete memory automatically.
---

# Temporary learnings

Save a lesson only when verified work revealed useful reasoning that the final
code, tests or existing docs do not already explain. Update an existing matching
lesson rather than duplicate it. Follow the project's existing records format
and location; do not create a new knowledge store just for this skill.

For guidance that depends on an external condition (an upstream bug, dependency
version or platform behavior), record:

- **Applies while:** the condition that makes the guidance necessary.
- **Retire when:** the observable change that would make it obsolete.
- **How to check:** a read-only command, source or artifact that verifies the change.
- **Evidence:** the verified version, date and source of the original finding.

An existing YAML learning format can use a single quoted `retire_when` string
for the retirement condition and its check. Plain Markdown can use the labels
above. Permanent guidance does not need an invented expiration date.

Example:

> Applies while: the deployed service lacks the profile-scoped secret contract.
> Retire when: a fresh conversation on the deployed release preserves the
> selected profile's allow-list and excludes an unrelated credential.
> How to check: inspect profile provenance and secret names only; never read
> or print credential values.
> Evidence: link the dated, versioned probe.

A merged upstream fix or a new version is a reason to recheck, not proof that
the deployed environment changed. Keep the lesson if the check fails; mark it
unconfirmed if the environment is unavailable. When the condition no longer
holds, mark the lesson superseded and cite the evidence. Remove or archive it
only within the user's authorized scope and the project's retention rules.

If retirement requires changing repository code (for example removing a
workaround and rerunning tests), describe that as a separate verification step
before removal. A read-only refresh must not silently make that change.

Never promote private session data, secrets or sensitive personal facts into
Git-visible learnings. Record only the minimum project reasoning needed.
