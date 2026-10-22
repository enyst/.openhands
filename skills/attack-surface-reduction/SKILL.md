---
name: attack-surface-reduction
description: Map and reduce unnecessary code reachability in the current codebase. Use for attack-surface analysis, pre-authentication exposure, disabled-but-reachable features, or configuration combinations that weaken security controls. This is reachability reduction, not a general vulnerability hunt.
---

# Attack surface reduction

Find code that lower-trust input can reach unnecessarily. Move the gate before
that code runs. A useful reduction does not require finding an exploitable bug.
Do not label unnecessary exposure as a confirmed vulnerability by itself.

Adapted from Chris Rohlf / Anthropic Frontier Red Team,
[Using Claude to reduce the attack surface of code](https://www.anthropic.com/research/attack-surface-reduction)
(20 October 2026). Follow the source for rationale and examples. This is an
independent adaptation of the published method, not Anthropic's internal skill.

## Set scope

- Read the target repository's instructions. Record the source revision, local
  changes, intended functionality, shipped defaults and deployment assumptions.
- Identify whether it serves public/unidentified input, authenticated users, or
  an operator's private environment. Intended public reachability is not a bug;
  do not invent an authentication requirement for private software.
- Inventory entry points and security-relevant settings from source, not just
  documentation. Include alternate listeners, aliases, namespaces and overrides.
  Trace how configuration becomes effective runtime policy.
- Analysis is read-only unless the user authorized code changes. Run dynamic
  checks only in an isolated local test environment with dummy inputs and
  credentials. Do not probe deployed services or change live configuration.

## Run three passes

Use a fresh context or fresh worker for each pass when available. Hand over only
scope, revision, entry-point/configuration inventory and short evidence pointers,
not earlier conclusions to copy. Each pass must rebuild/check its entry-point
inventory against source. If fresh contexts are unavailable, keep separate passes
and disclose the limitation.

### 1. Shipped defaults

Find complex or security-sensitive code reachable with default settings but
unused by intended default functionality. Look for disabled features whose
parsers, decoders, verifiers, handlers or initialization still run.

For each candidate, trace `entry → untrusted input → sensitive code → gate`.
Can the gate run earlier or the unused path be removed? Preserve intended default
behavior. Set aside any gate that would change non-default behavior for a human
to decide; do not silently remove supported features.

### 2. Early reachability

Across supported configurations, find sensitive work before authentication,
authorization, required user interaction or a protocol state transition. Include
state allocation and recording, not just request handlers.

Check the actual encoded input, not only its advertised type. Follow nested
objects and alternate dispatch paths: an allowed outer wrapper may contain a
disabled parser or signature algorithm. Place checks before the relevant parsing
or verification, at the shared enforcement point where possible. Keep the small
amount of parsing genuinely needed to choose and enforce the gate.

### 3. Configuration interactions

Inspect related settings in pairs, following dependencies further where needed.
Find accepted combinations that silently disable a control, leave a supposedly
disabled path reachable, or make policy depend on option order or namespace.

Example: hostname deny rules plus disabled reverse DNS can make a deny list
match nothing and fail open. Check what happens when a control's prerequisite
is absent. Propose explicit rejection at configuration load, a guard, or corrected
ordering. A warning alone does not restore the control. Defer compatibility or
policy changes to the owner.

## Prove the reduction

- Confirm each finding with a bounded dynamic execution trace of the actual
  target path. Show the sensitive code runs before the gate on the baseline and
  is not entered after the fix. Record the input, effective config and command.
  Static-only candidates remain **needs validation**, with the exact blocker.
- Add regression cases for the bypass and intended allowed behavior. Include
  advertised-versus-encoded type mismatches, nested inputs or alternate settings
  when relevant. Rejected input alone does not prove the parser was never run.
- For default-configuration gates, run the project's own tests **and** a black-box
  regression suite on baseline and modified builds with the same inputs and
  environment. Require identical observed default-functionality results; any
  unexplained difference blocks acceptance. Passing tests supports only the
  behavior covered. Record missing tests rather than claim equivalence.
- For early-reachability and interaction fixes, test the forbidden path and
  valid configurations. Keep intentional behavior changes explicit for review.

Report briefly: **entry point; settings/principal; reachable code; misplaced or
missing gate; trace/test evidence; smallest proposed fix; compatibility decision**.
Separate confirmed reachability, validated reductions and untested candidates.
State coverage gaps. Do not equate lines made unreachable with vulnerabilities
fixed or claim an exhaustive audit.
