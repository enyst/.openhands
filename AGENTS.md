# Repository Notes

- This repository root doubles as an OpenHands plugin and as a marketplace.
- Plugin metadata lives in `.plugin/plugin.json`; marketplace metadata lives in `.plugin/marketplace.json`.
- The marketplace exposes the root plugin as `enyst-workflow` with source `.` so the existing `skills/` and `hooks/` directories are reused instead of duplicated under `plugins/`.
- Plugin hook loading expects `hooks/hooks.json`, so keep `hooks/hooks.json` in sync with the repo-level `hooks.json` stop-hook configuration.
- The hook commands are deliberately portable: they try the current checkout, `~/.openhands/`, and `~/.openhands/plugins/installed/enyst-workflow/` in that order so the same config works as a repo checkout, a home config, or an installed plugin.
- `automations/` holds versioned automation definitions for local Agent Canvas and OpenHands Cloud. Top-level `automations/*.json` files are direct API request bodies; subdirectories may contain an Agent Canvas import definition, source prompt, installer, tests, and documentation.
- Automation definitions in git are not live state. Editing one does not update an installed or deployed automation.
- In `automations/typescript-client-release-maintainer/`, keep the prompt embedded in `typescript-client-release-maintainer.automation.json` byte-for-byte equal to `prompt.md`. Run `pytest -q tests/test_typescript_client_release_automation.py` after changing that bundle.
- `skills/codereview-roasted` is a deliberate fork of upstream's unified `code-review` skill: upstream merged the roasted skill away in OpenHands/extensions#175 and dropped the Linus persona. When syncing new upstream review findings into it, port the checks and leave `PERSONA`, `CORE PHILOSOPHY`, and "Linus's Three Questions" alone.
- Run `pytest -q` from the repository root for the local test suite.
