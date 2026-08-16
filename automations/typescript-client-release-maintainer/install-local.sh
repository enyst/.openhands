#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${AGENT_CANVAS_URL:-http://127.0.0.1:8000}"
API_KEY="${LOCAL_BACKEND_API_KEY:-}"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROMPT_FILE="$SCRIPT_DIR/prompt.md"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN=python
else
  echo "Python 3 is required to build and parse the API payload." >&2
  exit 2
fi

if [[ -z "$API_KEY" ]]; then
  cat >&2 <<'MSG'
LOCAL_BACKEND_API_KEY is required.

Start Agent Canvas with a key you know, for example:

  export LOCAL_BACKEND_API_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
  npx @openhands/agent-canvas

Then run this installer from another terminal with the same environment.
MSG
  exit 2
fi

if [[ ! -f "$PROMPT_FILE" ]]; then
  echo "Missing prompt file: $PROMPT_FILE" >&2
  exit 2
fi

PAYLOAD="$("$PYTHON_BIN" - "$PROMPT_FILE" <<'PY'
import json
import sys
from pathlib import Path

prompt = Path(sys.argv[1]).read_text()
print(
    json.dumps(
        {
            "name": "typescript-client Agent Server release maintainer",
            "prompt": prompt,
            "trigger": {
                "type": "cron",
                "schedule": "17 * * * *",
                "timezone": "Europe/Stockholm",
            },
            "repos": [
                {
                    "url": "https://github.com/OpenHands/typescript-client",
                    "ref": "main",
                    "provider": "github",
                }
            ],
            "timeout": 1800,
            "keep_alive": False,
            "enabled": False,
        }
    )
)
PY
)"

RESPONSE_FILE="$(mktemp)"
trap 'rm -f "$RESPONSE_FILE"' EXIT

curl --fail-with-body --silent --show-error \
  --request POST \
  --url "${BASE_URL%/}/api/automation/v1/preset/prompt" \
  --header "Content-Type: application/json" \
  --header "X-Session-API-Key: $API_KEY" \
  --data "$PAYLOAD" \
  --output "$RESPONSE_FILE"

"$PYTHON_BIN" - "$RESPONSE_FILE" "$BASE_URL" <<'PY'
import json
import sys
from pathlib import Path

response = json.loads(Path(sys.argv[1]).read_text())
base_url = sys.argv[2].rstrip("/")
automation_id = response.get("id")

print("Created local automation successfully.")
if automation_id:
    print(f"Automation ID: {automation_id}")
    print(f"Open Agent Canvas: {base_url}/automations/{automation_id}")
else:
    print(json.dumps(response, indent=2))
print(
    "The automation is disabled by default. Review its model, GitHub access, "
    "and schedule, then enable it in Agent Canvas."
)
PY
