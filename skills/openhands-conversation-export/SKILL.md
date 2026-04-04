---
name: openhands-conversation-export
description: Export an OpenHands Cloud conversation to JSON and render a readable markdown transcript. Use when the user wants to export/share an OpenHands conversation, inspect conversation events, make a redacted truncated transcript for committing, or turn a conversation URL/id into a markdown transcript.
triggers:
- export openhands conversation
- openhands conversation export
- render conversation transcript
- export conversation transcript
- download conversation events
- app.all-hands.dev/conversations/
---

# OpenHands conversation export

Use this skill to export an OpenHands Cloud conversation's event stream, optionally create a redacted truncated JSON for sharing, and render a human-readable markdown transcript.

## Inputs

You usually need:

- a conversation id, or a conversation URL like `https://app.all-hands.dev/conversations/<conversation-id>`
- `OPENHANDS_API_KEY`
- optionally `OPENHANDS_APP_BASE` when the deployment is not `https://app.all-hands.dev`

If the user only gives a URL, extract the final path segment as the conversation id.

## Default workflow

1. Pick an output directory and filenames.
2. Export the raw event stream with `scripts/export_conversation.py`.
3. If the result may be shared or committed, run `scripts/truncate_json.py` to redact known secrets and shorten long payloads.
4. Render markdown with `scripts/render_markdown.py`.
5. Inspect the generated markdown before sending or committing it.

## Commands

Export raw JSON:

```bash
python3 <this-skill-path>/scripts/export_conversation.py \
  --conversation-id <conversation-id> \
  --out <output-dir>/<conversation-id>.raw.json
```

Create a smaller redacted JSON copy:

```bash
python3 <this-skill-path>/scripts/truncate_json.py \
  --input-path <output-dir>/<conversation-id>.raw.json \
  --output-path <output-dir>/<conversation-id>.truncated.json
```

Render markdown transcript:

```bash
python3 <this-skill-path>/scripts/render_markdown.py \
  --input-path <output-dir>/<conversation-id>.truncated.json \
  --output-path <output-dir>/<conversation-id>.md
```

If you need maximum fidelity for local debugging, you can render from the raw JSON instead of the truncated copy, but do not share the raw export without checking for sensitive content.

## Notes

- `export_conversation.py` first tries the app API under `/api/conversations/...`.
- If the app host returns non-JSON or an error page for `/events`, the exporter automatically falls back to the conversation-specific runtime URL using `session_api_key` from the conversation details.
- `render_markdown.py` keeps user/agent messages readable and groups tool calls/results in collapsed `<details>` blocks.
- `truncate_json.py` redacts known API/session keys and shortens very long strings so exports are easier to review and commit.

## Safety

- Treat raw exports as sensitive. Tool output can contain secrets, tokens, URLs with embedded credentials, or other private context.
- Prefer the truncated JSON plus rendered markdown for anything that leaves the local workspace.
- If you are exporting a conversation for a public PR or issue, mention that the transcript was generated from an OpenHands conversation export and review the redacted output manually.

## References

- Human-oriented usage notes: `README.md`
- Detailed workflow and troubleshooting: `references/WORKFLOW.md`
