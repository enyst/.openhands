# .openhands

This repo contains personal OpenHands configuration.

## Layout

- `skills/`: prompt snippets / micro-agents (renamed from `microagents/`)
- `hooks.json`: global hook configuration (loaded from `~/.openhands/hooks.json`)
- `hooks/`: hook scripts referenced by `hooks.json`

## Stop hooks

This repo provides two Stop hooks:

1. `hooks/deny_stop_on_message.sh`: denies stopping if the last persisted event is an
   `agent` `MessageEvent`, and tells the model to continue until it calls `finish`.
2. `hooks/on_stop.sh`: runs `pre-commit run --all-files` (best-effort) before allowing stop.

Both are registered under the `Stop` event in `hooks.json`.
