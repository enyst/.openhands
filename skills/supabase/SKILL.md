---
name: supabase
description: Supabase platform — Postgres database, pgvector for embeddings, Auth, Storage, Edge Functions, and CLI. Use when building on or integrating with Supabase.
triggers:
- supabase
- Supabase
- pgvector hosted
- vector database hosted
---

# Supabase

Open-source Firebase alternative built on Postgres. Relevant to us as a potential hosted backend for gbrain (pgvector) and SmolPaws Cloud.

**Docs (agent-friendly):** `https://supabase.com/llms.txt` (index) / `https://supabase.com/llms-full.txt` (everything in one file)

When working with Supabase, fetch the relevant section from llms.txt rather than guessing at APIs.

## Key Services

| Service | What | Docs |
|---------|------|------|
| Database | Postgres with pgvector, RLS, extensions | `https://supabase.com/docs/guides/database.md` |
| AI & Vectors | Vector store, embeddings, semantic/hybrid search | `https://supabase.com/docs/guides/ai.md` |
| Auth | User auth, OAuth, RLS integration | `https://supabase.com/docs/guides/auth.md` |
| Storage | File storage with policies | `https://supabase.com/docs/guides/storage.md` |
| Edge Functions | Deno-based serverless functions | `https://supabase.com/docs/guides/functions.md` |
| Realtime | WebSocket subscriptions on DB changes | `https://supabase.com/docs/guides/realtime.md` |
| Queues | Background job processing | `https://supabase.com/docs/guides/queues.md` |
| Cron | Scheduled jobs | `https://supabase.com/docs/guides/cron.md` |

## Client Libraries

- **JavaScript:** `https://supabase.com/llms/js.txt`
- **Python:** `https://supabase.com/llms/python.txt`
- **CLI:** `https://supabase.com/llms/cli.txt`

## Pricing (as of 2026)

| Plan | Cost | Database | Key limits |
|------|------|----------|------------|
| Free | $0 | 500 MB, shared CPU | 2 projects max, paused after 1 week idle |
| Pro | $25/mo | 8 GB disk (then $0.125/GB) | 100K MAU, email support, daily backups |
| Team | $599/mo | SOC2, HIPAA available | SSO, priority support, 14-day backups |

Compute is billed separately per project ($10/mo for Micro instance, included in Pro).

## Why it matters for SmolPaws

- **gbrain already supports Supabase** as a Postgres backend (`gbrain init --supabase` or `gbrain migrate --to supabase`)
- pgvector for embeddings = same vector search we use locally with PGLite, but hosted
- Auth + RLS = multi-tenant memory isolation (each user's vectors are private)
- Free tier = good for prototyping; Pro at $25/mo = viable for SmolPaws Cloud backend
- Edge Functions could run the model routing proxy

## Local Development

```bash
# Install CLI
brew install supabase/tap/supabase

# Start local Supabase (Docker required)
supabase init
supabase start

# Link to remote project
supabase link --project-ref <ref>
supabase db push
```
