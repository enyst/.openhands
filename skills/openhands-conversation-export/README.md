# openhands-conversation-export

Export an OpenHands Cloud conversation's event stream to JSON and render it into a human-readable Markdown transcript.

## Included tools

- `scripts/export_conversation.py` - fetches conversation details and paginated events from OpenHands Cloud
- `scripts/truncate_json.py` - redacts known secrets and truncates oversized strings for safer sharing
- `scripts/render_markdown.py` - renders a readable transcript with messages inline and tool activity in collapsed blocks
- `scripts/redaction.py` - shared redaction helpers used by the renderer and truncation script

All scripts are stdlib-only Python.

## Quick start

From the repository root:

```bash
export OPENHANDS_API_KEY=...

# 1) Fetch full raw event stream
python3 skills/openhands-conversation-export/scripts/export_conversation.py \
  --conversation-id 2c6ec633e00c4c5da99601de500e5752 \
  --out tmp/2c6ec633e00c4c5da99601de500e5752.raw.json

# 2) Create a smaller redacted copy for sharing/committing
python3 skills/openhands-conversation-export/scripts/truncate_json.py \
  --input-path tmp/2c6ec633e00c4c5da99601de500e5752.raw.json \
  --output-path tmp/2c6ec633e00c4c5da99601de500e5752.truncated.json

# 3) Render a markdown transcript
python3 skills/openhands-conversation-export/scripts/render_markdown.py \
  --input-path tmp/2c6ec633e00c4c5da99601de500e5752.truncated.json \
  --output-path tmp/2c6ec633e00c4c5da99601de500e5752.md
```

## Notes

- A conversation id is the final path segment from a conversation URL like `https://app.all-hands.dev/conversations/<conversation-id>`.
- The exporter automatically falls back to the per-conversation runtime URL when the app host returns an error page or non-JSON response for `/events`.
- Review raw exports before sharing them. Even with redaction, transcripts can still contain sensitive project context.

See `references/WORKFLOW.md` for a more detailed playbook.
