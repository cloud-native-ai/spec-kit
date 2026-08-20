# `/speckit.sanitize` — Sanitize Command

Framework material hygiene: detects stale/residual and redundant materials (semantic claims vs repository evidence), runs deterministic correctness checks (dead references, index↔store consistency, compat symlink health, mirror drift), persists findings with a `pending` lifecycle state, and executes confirmation-gated cleanup (delete/archive destructive; reversible repairs automatic).

## Execution Flow

```text
/speckit.sanitize [check] [--roots <csv>]
```

Seven stages — Preflight → Collect → Judge → Present → Confirm → Apply → Wrap-up. Default runs the full flow; `check` stops after Present (no cleanup prompt); `--roots` restricts the scan to a subset of material roots (partial scans never auto-resolve findings).

### Engine Calls

```bash
python3 .specify/scripts/python/sanitize-utils.py --action collect --workspace-root . --format json
python3 .specify/scripts/python/sanitize-utils.py --action record --file <verdicts.json> --workspace-root . --format json
python3 .specify/scripts/python/sanitize-utils.py --action status --workspace-root . --format json
python3 .specify/scripts/python/sanitize-utils.py --action apply --plan .specify/memory/sanitize/cleanup-plan.json --workspace-root . --format json
```

## Findings Store

`.specify/memory/sanitize/findings.json` — a cumulative ledger keyed by stable IDs (`sha1(category|target)[:12]`). Lifecycle: `pending` → `resolved` (disposition executed) or `dismissed` (user rejects); findings not re-detected on a full scan auto-resolve (external fixes converge naturally); re-detection after resolution reopens the finding (regression signal).

## Detection Categories

| Category | Detection | Default disposition |
|----------|-----------|---------------------|
| stale-residue | semantic (agent judges engine-gathered evidence pack: git log since claim date + path existence) | delete (destructive, gated) |
| redundant | semantic (content fully absorbed by a live carrier) | archive (destructive, gated) |
| dead-reference | programmatic (links / repo paths / `speckit.*` commands / skill dirs; docs tree reuses docs-utils) | repair (automatic) |
| index-inconsistency | programmatic (features / feedback / evidence index ↔ store, bidirectional) | repair (automatic) |
| broken-symlink | programmatic (compat links: broken / replaced / missing-when-tool-surface-exists) | delegate → `/speckit.instructions` |
| mirror-drift | programmatic (sync-mirrors --check + orphan mirror dirs + obsolete-registry cross-check) | delegate → sync-mirrors; unregistered orphans → delete (gated) |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | success (including "no findings", "nothing applicable") |
| 1 | CLI error (unknown action, unreadable file, malformed JSON) |
| 2 | verification failure (unconfirmed plan, schema violation, out-of-whitelist target) |

## Scope

Checks and cleanup target **framework-owned materials only** (memory layer, specs, history, mirrors, compat symlinks, docs tree). User source code, product scripts, and test cases are never assessed or modified. Non-git environments degrade semantic detection (deterministic checks unaffected).

## See Also

- [Feedback Command](feedback.md) — wrap-up self-reflection entries
- [Docs Command](docs.md) — delegated docs content reconciliation
- Tool record: `.specify/memory/tools/sanitize-utils.py.md`
