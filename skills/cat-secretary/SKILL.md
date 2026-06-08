---
name: cat-secretary
description: Maintain SmolPaws secretary context and searchable Slack archives for the agent-canvas sprint. Use when asked about project status, Slack discussions, what someone said, heartbeat archive refreshes, or posting project context to GitHub issues.
---

# Cat-Secretary Skill

SmolPaws is acting as team secretary for the agent-canvas MVP sprint through May 2026 (target: June 1st MVP).

## What This Means

- Track discussions in the project Slack channels and keep searchable archives.
- Stay current on what the team is working on so SmolPaws can provide context in conversations.
- When asked about project status, decisions, or "what did X say about Y", search the archives first.
- Post summaries or context on GitHub issues when useful (tracked in `secretary-state.json`).

## Archive Location

All archives live at `~/.smolpaws/slack/archive/`:

| File | Channel | Slack ID |
|------|---------|----------|
| `proj-agent-canvas-may2026.md` | #proj-agent-canvas (was #proj-gui) | C06QT0AGY4W |
| `proj-agent-may2026.md` | #proj-agent | C06R25BT5B2 |
| `secretary-state.json` | — state tracking — | — |

Archives are markdown with date headers, author, timestamp, and threaded replies indented as blockquotes. Searchable with `grep`.

## State File

`~/.smolpaws/slack/archive/secretary-state.json` tracks:

- `lastArchiveDate` — last date the archive was refreshed
- `channels[name].lastReadTs` — Slack message timestamp of last archived message per channel
- `archiveStart` — beginning of the archive window (2026-05-01)
- `issuesCommented` — GitHub issues where secretary context was posted

## How to Refresh Archives

Use the Slack Web API from Chrome (see HEARTBEAT.md for token retrieval):

1. Read the current `secretary-state.json` to get `lastReadTs` per channel.
2. For each channel, call `conversations.history` with `oldest=lastReadTs` to get new messages.
3. For messages with threads (`reply_count > 0`), call `conversations.replies`.
4. Resolve user IDs to display names via `users.info` (cache results).
5. Append new messages to the appropriate `*-may2026.md` file under the correct date header.
6. Update `lastReadTs` and `lastArchiveDate` in `secretary-state.json`.

### Slack API Pattern

```javascript
// From Chrome tab logged into Slack:
const token = JSON.parse(localStorage.getItem('localConfig_v2')).teams['T06P212QSEA'].token;
const fd = new FormData();
fd.append('token', token);
fd.append('channel', 'C06QT0AGY4W');  // proj-agent-canvas
fd.append('oldest', '1778964424.633419');  // lastReadTs
fd.append('limit', '200');
const resp = await fetch('/api/conversations.history', { method: 'POST', body: fd, credentials: 'include' });
const data = await resp.json();
```

## How to Search

```bash
# Find what someone said about a topic
grep -i "worktree" ~/.smolpaws/slack/archive/proj-agent-canvas-may2026.md

# Find messages by a person
grep "Xingyao\|Graham\|Robert\|Engel\|Hiep\|Vasco" ~/.smolpaws/slack/archive/proj-agent-canvas-may2026.md

# Find discussions on a specific date
sed -n '/^## 2026-05-14/,/^## 2026-05-15/p' ~/.smolpaws/slack/archive/proj-agent-canvas-may2026.md
```

## When to Act as Secretary

- **On heartbeat**: refresh archives if `lastArchiveDate` is not today.
- **When asked about project context**: search archives before answering.
- **When reviewing PRs**: check if there was Slack discussion about the feature/issue.
- **Proactively**: if a GitHub issue lacks context that exists in Slack, consider posting a summary.

## Scope

- Duration: May 2026 (until MVP ships ~June 1st)
- Channels: `#proj-agent-canvas` and `#proj-agent`
- Not a bot — just a cat who pays attention and keeps notes.
