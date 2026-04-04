# Workflow

## When to use this skill

Use this skill when you need to:

- turn an OpenHands conversation into a readable transcript
- inspect or archive the event stream behind a conversation
- prepare a conversation export for a PR, issue, or design review
- share a reproducible agent run without pasting the raw event payload directly

## Prerequisites

- Python 3 available in the runtime
- `OPENHANDS_API_KEY` set in the environment
- a conversation id or URL

## Recommended process

1. Derive the conversation id.
   - If the user gives a URL, use the last path segment.
2. Choose an output directory.
   - Prefer a temp or scratch directory unless the user explicitly wants committed artifacts.
3. Export raw JSON.
4. Create a truncated copy before sharing or committing.
5. Render markdown from the truncated copy.
6. Open the markdown and spot-check the output.
   - Confirm title/metadata look right.
   - Confirm tool output was truncated where needed.
   - Confirm obvious secrets were redacted.

## Troubleshooting

### `OPENHANDS_API_KEY is required`

Set the environment variable before running the exporter.

### The app `/events` endpoint returns HTML or an error

This is expected on some deployments. The exporter already retries using the conversation-specific runtime URL plus `session_api_key` from the conversation details.

### You only have a conversation URL

Use the final segment after `/conversations/` as `--conversation-id`.

### The export is too large to review comfortably

Run `truncate_json.py` with a smaller `--max-len`, `--head`, or `--tail`.

### The markdown transcript is still too noisy

Render from the truncated JSON, not the raw export. The renderer already removes several internal noise events and groups tool activity into collapsed sections.

## Sharing guidance

- Do not post the raw export publicly unless the user explicitly wants that.
- Prefer sharing the rendered markdown plus, if needed, the truncated JSON.
- If you include the transcript in a PR or issue, describe it as an AI-generated OpenHands conversation export reviewed by the agent on the user's behalf.
