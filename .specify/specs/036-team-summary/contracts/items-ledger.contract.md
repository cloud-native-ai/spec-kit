# Contract: Item Ledger (`items.jsonl`)

**Requirement → Feature**: `036-team-summary` → Feature 027 Team Management
**Artifact**: `.specify/teams/<slug>/items.jsonl` — tracked, append-only, JSON Lines
**Covers**: FR-008, FR-010, FR-011, FR-018, FR-021, FR-026, FR-027, FR-029
**Pinned by**: `tests/contract/test_team_item_ledger.py`

## Purpose

The ledger is the team's machine-readable, version-controlled record of work-item identity and state across runs. It is the only structure the form generator treats as authoritative for work items.

## Line schema

Each line is a single JSON object representing one **state event**.

```json
{"item_id":"TI-0007","title":"P7 sync-mirrors 单入口","phase_ref":"PH-0002","state":"completed","provenance":".specify/teams/cws-workspace-cluster/runs/20260730T094500Z-report.md#deliverables","ts":"2026-07-30T09:45:00Z","identity":"explicit","maturity_at_event":"L1"}
```

Required keys: `item_id`, `title`, `phase_ref`, `state`, `provenance`, `ts`, `identity`.
Optional keys: `supersedes`, `excluded_reason`, `maturity_at_event`.

## Normative rules

- **LC-1**: The file MUST be append-only. Existing lines MUST NOT be rewritten or deleted. State progression MUST be expressed by appending a new event.
- **LC-2**: An item's current state MUST be resolved as the last event for that `item_id`, ordered by `ts`, ties broken by file order.
- **LC-3**: `provenance` MUST resolve to a path tracked in version control. The following MUST be rejected: `.specify/teams/.work/**`, `.specify/agents/execution/logs/**`, and any path outside the repository (including `${TMPDIR}/spec-kit-dispatch/**`).
- **LC-4**: `item_id` MUST match `TI-[0-9]{4}` when `identity` is `explicit`, and `TIX-[0-9a-f]{8}` when `identity` is `inferred`.
- **LC-5**: Every `item_id` MUST satisfy the upstream DDL identifier constraint — first character alphanumeric, remaining characters drawn from `[A-Za-z0-9_.-]`. Titles containing spaces or non-ASCII characters MUST NOT be used as identifiers.
- **LC-6**: When `supersedes` is present, the referenced identifier MUST appear earlier in the ledger, and folding MUST yield exactly one record for the pair, authoritative on the explicit identifier while retaining the inferred identifier's event history.
- **LC-7**: `state` MUST be one of `completed`, `in-progress`, `delayed`, `not-started`, `unknown`. An item with no state signal MUST be recorded as `unknown`, never as `not-started` and never with a zero progress value.
- **LC-8**: Only the Team Supervisor writes this file. Sub-agents MUST NOT write it.
- **LC-9**: `excluded_reason` non-empty removes the item from delay and incompletion accounting while keeping it in the data layer.
- **LC-10**: `maturity_at_event` anchors state semantics to the maturity in force when the event occurred. A later maturity promotion MUST NOT retroactively reinterpret earlier events.

## Identifier issuance

| Identifier | Grammar | Issued by | When |
|-----------|---------|-----------|------|
| `TI-<nnnn>` | zero-padded, monotonically increasing per team | Team Supervisor | On first observation of a work item |
| `TIX-<8hex>` | `sha256(title + "\u0000" + phase_ref)`, first 8 lowercase hex characters | Form generator | Backfill of items predating explicit issuance |

Renaming an item MUST NOT change an explicit identifier. Renaming during the inferred era changes the derived identifier; the prior identifier MUST then be reported as "not seen this run" in the material-gap declaration rather than silently dropped.

## STATE.md cross-reference

Teams that maintain `STATE.md` MUST carry the item identifier inline on tracked entries as a `[TI-nnnn]` token. This satisfies identifier coverage of `STATE.md` entries without imposing a schema on its prose form. The ledger remains the parse surface; the token is for human cross-reference.

## Verification

```bash
# Grammar and provenance rules, asserted per line (pinned by the contract test)
python3 -c "
import json,re,sys
ok=True
for n,l in enumerate(open('.specify/teams/<slug>/items.jsonl'),1):
    r=json.loads(l)
    pat=r'^TI-[0-9]{4}$' if r['identity']=='explicit' else r'^TIX-[0-9a-f]{8}$'
    if not re.match(pat,r['item_id']): ok=False; print(f'line {n}: LC-4 {r[\"item_id\"]}')
    if not re.match(r'^[A-Za-z0-9][A-Za-z0-9_.-]*$',r['item_id']): ok=False; print(f'line {n}: LC-5')
    if r['provenance'].startswith(('.specify/teams/.work/','.specify/agents/execution/logs/','/tmp/')): ok=False; print(f'line {n}: LC-3')
    if r['state'] not in {'completed','in-progress','delayed','not-started','unknown'}: ok=False; print(f'line {n}: LC-7')
sys.exit(0 if ok else 1)
"
```

LC-1 (append-only) is verified in CI by asserting that the diff for `items.jsonl` in any commit contains only added lines.
