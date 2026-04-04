# .openhands

This repo contains personal OpenHands configuration.
It now also declares the repository root as an OpenHands marketplace and as a plugin named `enyst-workflow`.

## Layout

- `.plugin/plugin.json`: plugin manifest for the root `enyst-workflow` plugin
- `.plugin/marketplace.json`: marketplace manifest that exposes the root plugin and bundled skills
- `skills/`: agent skills or old OpenHands skills
- `hooks.json`: repo-level hook configuration (loaded from `~/.openhands/hooks.json`)
- `hooks/`: hook scripts plus `hooks/hooks.json` for plugin-compatible hook loading

## Marketplace and plugin layout

The [OpenHands Software Agent SDK](https://github.com/OpenHands/software-agent-sdk) looks for:

- `.plugin/marketplace.json` to load a repository as a marketplace
- `.plugin/plugin.json` to load a directory as a plugin
- `hooks/hooks.json` when a plugin bundles hooks

This repository uses those conventions directly at the root so the existing `skills/` and `hooks/` directories can be reused without duplicating them under `plugins/enyst-workflow/`.
The hook commands intentionally try the current checkout, `~/.openhands/`, and the installed plugin path under `~/.openhands/plugins/installed/enyst-workflow/` so the same manifests work in all three layouts.

## Stop hooks

This repo provides two Stop hooks:

1. `hooks/deny_stop_on_message.sh`: denies stopping if the last persisted event is an
   `agent` `MessageEvent`, and tells the model to continue until it calls `finish`.
2. `hooks/on_stop.sh`: runs `pre-commit run --all-files` (best-effort) before allowing stop.

Both are registered under the `Stop` event in both `hooks.json` and `hooks/hooks.json`.
