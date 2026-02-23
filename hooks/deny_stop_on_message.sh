#!/usr/bin/env bash
# Deny stopping if the last persisted event is an agent MessageEvent.
# This is useful for headless/agentic runs where a message-only response is
# often an intermediate step; we want the model to keep going until it calls
# `finish`.

set -o pipefail

PERSIST_DIR="${OPENHANDS_PERSISTENCE_DIR:-$HOME/.openhands}"
CONV_ROOT="${OPENHANDS_CONVERSATIONS_DIR:-$PERSIST_DIR/conversations}"

CONV_DIR="$CONV_ROOT/$OPENHANDS_SESSION_ID"
EVENTS_DIR="$CONV_DIR/events"

if [ -z "$OPENHANDS_SESSION_ID" ]; then
  echo '{"decision":"allow","reason":"OPENHANDS_SESSION_ID not set"}'
  exit 0
fi

if [ ! -d "$EVENTS_DIR" ]; then
  echo '{"decision":"allow","reason":"events dir not found"}'
  exit 0
fi

LAST_EVENT_FILE="$(find "$EVENTS_DIR" -maxdepth 1 -type f -name 'event-*.json' -printf '%T@ %p\n' 2>/dev/null | sort -nr | head -n 1 | cut -d' ' -f2-)"
if [ -z "$LAST_EVENT_FILE" ]; then
  echo '{"decision":"allow","reason":"no events found"}'
  exit 0
fi

if ! command -v jq >/dev/null 2>&1; then
  echo '{"decision":"allow","reason":"jq not available"}'
  exit 0
fi

KIND="$(jq -r '.kind // ""' "$LAST_EVENT_FILE")"
SOURCE="$(jq -r '.source // ""' "$LAST_EVENT_FILE")"
TOOL_NAME="$(jq -r '.tool_name // ""' "$LAST_EVENT_FILE")"

# If the agent already finished via the finish tool, allow stop.
if [ "$KIND" = "ActionEvent" ] && [ "$SOURCE" = "agent" ] && [ "$TOOL_NAME" = "finish" ]; then
  echo '{"decision":"allow"}'
  exit 0
fi

# If the last event is an agent MessageEvent, block stop and ask the model to
# continue and finish properly.
if [ "$KIND" = "MessageEvent" ] && [ "$SOURCE" = "agent" ]; then
  echo '{"decision":"deny","additionalContext":"Your last turn was a plain message. Continue working until the task is complete. When complete, call the `finish` tool with your final answer (do not just send another message)."}'
  exit 2
fi

echo '{"decision":"allow"}'
exit 0
