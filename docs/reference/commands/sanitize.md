# `/speckit.sanitize` — Sanitize Command

Framework material hygiene: detects stale/residual and redundant materials (semantic claims vs repository evidence), runs deterministic correctness checks (dead references, index↔store consistency, compat symlink health, mirror drift), persists findings with a `pending` lifecycle state, and executes confirmation-gated cleanup (delete/archive destructive; reversible repairs automatic).

## Execution Flow

```text
/speckit.sanitize [check] [--lane materials|retention|renumber|all] [--roots <csv>]
```

**Materials lane (default)** — seven stages: Preflight → Collect → Judge → Present → Confirm → Apply → Wrap-up. Default runs the full flow; `check` stops after Present (no cleanup prompt); `--roots` restricts the scan to a subset of material roots (partial scans never auto-resolve findings).

**Retention lane (`--lane retention`)** — consume → receipt → retire for the per-run record stores. Five steps: Preflight → Scan → Distill/Promote → Plan/Present → Confirm/Apply. `--lane all` runs materials first, then retention, then renumber. `check` stops after Scan/Present.

**Renumber lane (`--lane renumber`)** — sequence-number collision repair for concurrent/parallel lines: Preflight → Scan → Plan/Present → Confirm → Apply. Four families: spec directory numbers (`.specify/specs/NNN-slug`), register IDs (`REC-<prefix>-NN`, `OI-<prefix>-NN`, `OI-N`, `T-NNN`), REC/OI prefix-follow for a renamed spec, and feature-local `T`/`CHK` duplicates. Repair is **duplicate-only**: a freed number is never reused and gaps are never compacted.

### Engine Calls

```bash
python3 .specify/scripts/python/sanitize-utils.py --action collect --workspace-root . --format json
python3 .specify/scripts/python/sanitize-utils.py --action record --file <verdicts.json> --workspace-root . --format json
python3 .specify/scripts/python/sanitize-utils.py --action status --workspace-root . --format json
python3 .specify/scripts/python/sanitize-utils.py --action apply --plan .specify/memory/sanitize/cleanup-plan.json --workspace-root . --format json
```

### Retention Engine Calls

```bash
python3 .specify/scripts/python/record-retention.py --action scan --workspace-root . --format json
python3 .specify/scripts/python/record-retention.py --action distill --workspace-root . --promotions <promotions.json> --format json
python3 .specify/scripts/python/record-retention.py --action plan --workspace-root . --format json
python3 .specify/scripts/python/record-retention.py --action apply --plan <plan.json> --workspace-root . --format json
```

The lane covers four stores: `exec-quant` records, `feedback` entries, `run-determination` session records, and free-form session notes. A raw record is deleted only when a retention receipt covers it and the default 30-day grace has elapsed. Never retired: open feedback, unsettled run-determination records, unreadable exec-quant records, and session notes without a promotion/ephemeral decision.

Retention artifacts are durable evidence under `.specify/memory/retention/`:

| Path | Content |
|------|---------|
| `summaries/<store>/` | append-only monthly rollups (counts/projections; no aggregate score) |
| `receipts/` | one per consumed raw record: carrier path + digest |
| `plans/` | one per scan, `confirmed: false` until the user releases it |
| `ledger/` | one per apply batch: removed entries, counts, conservation check |

`apply` requires `confirmed: true`, re-checks every receipt / grace / entry state, and refuses dirty git paths. A non-git workspace needs the explicit `--allow-unversioned` override. The lane never writes the materials findings ledger.

### Renumber Engine Calls

```bash
python3 .specify/scripts/python/renumber-utils.py --action scan --workspace-root . --format json
python3 .specify/scripts/python/renumber-utils.py --action plan --workspace-root . --format json
python3 .specify/scripts/python/renumber-utils.py --action apply --plan <plan.json> [--groups <csv>] --workspace-root . --format json
python3 .specify/scripts/python/renumber-utils.py --action dismiss --group <id> --reason <path> --workspace-root . --format json
python3 .specify/scripts/python/renumber-utils.py --action status --workspace-root . --format json
```

Stage semantics:

- **Scan** is read-only and reports per-family counts, the collision groups, and informational notes (non-conforming spec prefixes such as `065a-`, register codes with no machine allocation rule).
- **Plan** writes `confirmed: false` under `.specify/memory/renumber/plans/`. Each group names the kept owner with its evidence, the old → new token, the full reference inventory (file × hit count), branch-name guards, ambiguous-reference counts and cross-group dependencies. Next-free allocation counts archived spec numbers and never reuses a freed number.
- **Confirm** is the same single front-loaded destructive batch as the cleanup plan — no second gate. A group with ambiguous references is `needs-decision` and is never guessed: a duplicated identifier cannot say which definition a mention means. `--adopt-ambiguous-refs` exists only for the user-stated reading that every mention refers to the kept definition.
- **Apply** requires `confirmed: true` and a git workspace (a directory rename outside git loses its history). It re-checks the mapping, the git-clean state of every target and the branch guard, executes renames plus rewrites, re-scans, and writes one ledger per batch. Rewrites cover framework-owned materials; `.specify/history/`, archives, `test-evidence/` logs and date-named files keep the old identity and are reported as `excluded_hits` (not a failure). Branch renames are printed as `git branch -m` commands, never executed.

Renumber artifacts under `.specify/memory/renumber/` are durable evidence, one file per entry (concurrent writers never share a path):

| Path | Content |
|------|---------|
| `plans/` | one per plan, `confirmed: false` until the user releases it |
| `dismissals/` | one per adjudicated overlap: group id, reason path, timestamp |
| `ledger/` | one per apply batch: groups applied, unresolved groups, excluded hits |

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

Checks and cleanup target **framework-owned materials only** (memory layer, specs, history, mirrors, compat symlinks, docs tree). The retention lane additionally treats the framework-owned record stores (`exec-quant`, `feedback`, `session`) as **data**; it consumes and retires them under the receipt gate. The renumber lane rewrites references inside framework-owned materials but never touches git refs, dated records, or evidence logs. User source code, product scripts, and test cases are never assessed or modified. Non-git environments degrade semantic detection (deterministic checks unaffected); retention deletion in a non-git workspace requires an explicit override, while renumber apply refuses a non-git workspace outright.

## See Also

- [Feedback Command](feedback.md) — wrap-up self-reflection entries
- [Docs Command](docs.md) — delegated docs content reconciliation
- [Memory System](../skills/memory.md) — session/knowledge layout and retention lane
- [Feedback System](../skills/feedback.md) — feedback store lifecycle and retirement
- Tool record: `.specify/memory/tools/sanitize-utils.py.md`
