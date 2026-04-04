# Repository Notes

- This repository root now doubles as an OpenHands plugin and as a marketplace.
- Plugin metadata lives in `.plugin/plugin.json`; marketplace metadata lives in `.plugin/marketplace.json`.
- The marketplace exposes the root plugin as `enyst-workflow` with source `.` so the existing `skills/` and `hooks/` directories are reused instead of duplicated under `plugins/`.
- Plugin hook loading expects `hooks/hooks.json`, so keep `hooks/hooks.json` in sync with the repo-level `hooks.json` stop-hook configuration.
- The hook commands are deliberately portable: they try the current checkout, `~/.openhands/`, and `~/.openhands/plugins/installed/enyst-workflow/` in that order so the same config works as a repo checkout, a home config, or an installed plugin.
- Run `pytest -q` from the repository root for the local test suite.
