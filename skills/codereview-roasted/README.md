# Codereview Roasted

Brutally honest code review in the style of Linus Torvalds, focusing on data structures, simplicity, and pragmatism. Use when you want critical, no-nonsense feedback that prioritizes engineering fundamentals over style preferences.

## Triggers

- `/codereview-roasted`

## Why this skill exists

This is a review with the Linus persona — using "the engineering mindset of Linus Torvalds", and "Linus's Three Questions".

This skill restores the pre-merge roasted content (`skills/codereview-roasted/SKILL.md` at `797675f^`) and then ports forward everything upstream has learned since, without the de-personalization.

## What was ported forward from upstream `code-review`

| Addition | Upstream PR |
|---|---|
| `GROUNDING` section — check the Files Changed manifest and read the file before flagging anything as missing; verify line numbers before posting inline comments | [#234](https://github.com/OpenHands/extensions/pull/234), [#329](https://github.com/OpenHands/extensions/pull/329) (Windows commands) |
| Unnecessary-comment detection under scenario 2 | [#304](https://github.com/OpenHands/extensions/pull/304) |
| Expanded security checklist (unsanitized input, hardcoded secrets, crypto misuse, race conditions) | merged from the standard skill in [#175](https://github.com/OpenHands/extensions/pull/175) |
| Poor naming / missing inline docs under scenario 2 | merged from the standard skill in [#175](https://github.com/OpenHands/extensions/pull/175) |
| Scenario 8 supply chain review + 7-day publication rule + `references/supply-chain-security.md` | [#226](https://github.com/OpenHands/extensions/pull/226), [#244](https://github.com/OpenHands/extensions/pull/244), [#353](https://github.com/OpenHands/extensions/pull/353) |
| Scenario 9 Risk and Safety Evaluation + `references/risk-evaluation.md` + `[RISK ASSESSMENT]` output block | [#148](https://github.com/OpenHands/extensions/pull/148) |
| Scenario 10 GitHub Action version update verification via CI | [#167](https://github.com/OpenHands/extensions/pull/167) |
| "If the code is good, just approve it" in `TASK` | [#175](https://github.com/OpenHands/extensions/pull/175) |
| Drop 🟢 Acceptable / Nit inline comments | [#207](https://github.com/OpenHands/extensions/pull/207) |
| Review self-improvement message block | [#217](https://github.com/OpenHands/extensions/pull/217), [#251](https://github.com/OpenHands/extensions/pull/251) |

## What was deliberately NOT ported

- **The de-Linus'd persona.** `PERSONA`, `CORE PHILOSOPHY`, "Linus's Three Questions", and "Linus-Style Analysis" stay as they were. That is the entire point of this skill.
- **The `/codereview` trigger.** This skill owns `/codereview-roasted` only, so it can coexist with the upstream unified skill.
- **The `/iterate` plug** in the self-improvement footer — it advertises a skill that is not installed here.
- **`triggers: [/codereview]`** in the custom-guideline instructions — retargeted to `/codereview-roasted` so per-repo overrides actually load alongside this skill.

## References

- [`references/risk-evaluation.md`](references/risk-evaluation.md) — risk levels, risk factors, escalation guidance
- [`references/supply-chain-security.md`](references/supply-chain-security.md) — dependency verification checklist and scrutiny tiers
