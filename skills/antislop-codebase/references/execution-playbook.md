# Execution Playbook

## Slice Order

Prefer this order unless repo facts argue otherwise:

1. Baseline tests, build, typecheck, and smoke.
2. Minimal diagnostics/error handling needed to safely refactor hard-to-debug workflows.
3. Pure helpers/models from large files.
4. Feature components/hooks/actions from large UI files.
5. Shared types/contracts across module or frontend/backend boundaries.
6. Server/API/provider consolidation with behavior-pinning tests.
7. Styling migration by surface with visual checks.
8. Test/e2e dedupe and quality pass.
9. Final audit.

## Refactor Rules of Thumb

- Keep public imports stable with compatibility barrels while moving internals.
- Extract pure logic before extracting stateful UI.
- Name files by feature and behavior, not vague utilities.
- Avoid pass-through prop blobs except stable domain objects.
- Add abstractions only when they remove real duplication or isolate a volatile boundary.
- Prefer schema/runtime guards at external boundaries and static types inside trusted code.
- Do not change provider/API response shape in the same commit as route consolidation unless tests pin it.
- Keep CSS/theme tokens centralized, but move feature layout close to the feature.
- Remove dead CSS only after grep plus screenshot/viewport checks.

## Concurrent Subagent Pattern

Give each worker:

- a narrow surface
- explicit files or directories
- no-touch areas
- expected tests
- a request to report findings/diffs, not to deploy

### OpenHands Subagent Examples

Headless CLI:
```bash
openhands --headless --json -t "Split src/server.ts: extract auth helpers into src/auth/index.ts, re-export from src/server.ts. Run npm test after. Report what changed."
```

Via agent-server API:
```bash
curl -X POST "$AGENT_SERVER_URL/api/conversations" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "initial_message": "Split src/utils.py into src/utils/http.py and src/utils/parsing.py. Keep imports working. Run pytest after.",
    "agent": {"tools": [{"name": "terminal"}, {"name": "file_editor"}]}
  }'
```

### Good Parallel Lanes

- test characterization
- large-file splitting
- CSS dead selector audit
- server/provider helper extraction
- type-boundary tightening
- e2e/screenshot inspection
- documentation/audit metrics

### Bad Parallel Lanes

- multiple workers changing the same app shell
- simultaneous route contract and client contract changes
- formatting sweeps while feature edits are active
- edits inside user-declared active work areas
- broad security, observability, compliance, or SRE work (separate skills)

## Checkpoints

Commit when:

- the slice is behaviorally coherent
- narrow tests pass
- broader typecheck/build/unit pass when practical
- unrelated dirty work is excluded

Deploy when:

- production-shaped build/smoke passes
- e2e/visual smoke passes for touched UI
- known blockers are either fixed or explicitly accepted
