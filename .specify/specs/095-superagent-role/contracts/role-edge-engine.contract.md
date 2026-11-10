# Contract — Role-Edge Judgement Engine (`role-edge-check.py`)

**Status**: design contract (Feature 095) · **Owner of the rule text**: `.specify/shared/definitions/superagent-definitions.md` ([[STR-004]]) · This file fixes the engine's executable interface; it does not own the role model.

**Engine paths**: framework source `scripts/python/role-edge-check.py`; runtime mirror `.specify/scripts/python/role-edge-check.py` (via `sync-mirrors.py`).

## C-1. Interface

| Element | Declaration |
|---------|-------------|
| `--action report` | Default action. Emits the full judged model. |
| `--action query` | Pair query; requires `--parent <id>` and `--child <id>`. |
| `--state-dir PATH` | Driver state root; default `.specify/state`. |
| `--teams-dir PATH` | Team run-report root; default `.specify/teams`. |
| `--logs-dir PATH` | Artifact-triplet root; default `.specify/agents/execution/logs`. |
| `--registry-dir PATH` | Line-registry cross-check root; default `$SPECIFY_LINE_REGISTRY_DIR` → `$XDG_STATE_HOME/spec-kit/lines` → `~/.local/state/spec-kit/lines`. |
| `--format json\|text` | Default `json`. |
| `--help`, `--version` | Answer before any read; one machine-readable identity line for `--version` (Constitution XXI, applied per FR-005 even though a read-only script is outside the REQUIRED set). |
| Undeclared option | Rejected non-zero with a recognizable error before any read. |

## C-2. Exit codes (closed)

| Code | Meaning |
|------|---------|
| `0` | Judged clean. An empty edge set is clean **and explicitly summarized** (`summary.edges = 0`); it is never a silent empty output. |
| `1` | One or more violations found (the violation list is emitted). |
| `2` | Unreadable or malformed input: a required input root missing/unreadable, or a malformed carrier row/record. The error names the offending path and field. Never a silent empty set, never exit 0. |

## C-3. `report` output (JSON)

Required keys: `schema_version` (integer, currently `1`), `action`, `inputs`, `roots`, `executors`, `edges`, `violations`, `conflicts`, `summary`.
`summary` keys: `edges`, `executors`, `violations`, `conflicts` (integers taken from the emitted arrays, never computed separately).
`executors[]` keys: `id`, `parent`, `roles` (array, set semantics), `depth`, `sources`.
`edges[]` keys: `parent`, `child`, `attempt`, `role_declaration`, `dispatch_duty` (`granted` \| `not-granted`), `depth`, `source` (`carrier`, `path`, `line`).
`violations[]` keys: `kind` ∈ closed set of C-5, `subjects`, `paths`.
`conflicts[]` keys: `field`, `paths` (exactly ≥2 paths).

`--format text` renders one line per edge and one line per violation; field names equal the JSON keys (no second vocabulary).

## C-4. `query` output

Required keys: `schema_version`, `action`, `edge_exists` (boolean), `edge` (object or null), `parent` (`{id, roles, depth}`), `child` (`{id, roles, depth}`), `violations` (only those whose `subjects` include either queried identity). A queried identity that cannot be resolved is a `2` (named error), not `edge_exists: false` — absence of an edge between two *known* identities is `false`; an unknown identity is unreadable input.

## C-5. Violations (closed four-kind set)

`self-dispatch` · `dangling-parent` · `unbacked-role-claim` · `depth-inconsistent` — predicates exactly as `data-model.md` § 5. A fifth kind MUST NOT be emitted before this contract is revised.

## C-6. Read-only invariant

The engine MUST contain zero write points: no file opened in a write/append mode, no mutation API on inputs, no temp-file creation inside input roots. The invariant is asserted structurally (source scan) and behaviourally (fixture run leaves the fixture tree byte-identical).

## C-7. Determinism

The same input tree yields byte-identical JSON on two consecutive runs (stable ordering: edges sorted by `(parent, child, attempt)`, executors by `id`, violations by `(kind, subjects)`).

## C-8. Conflict handling

When the same field of one edge disagrees between two carriers, the engine emits a `conflicts` row naming the field and **both** paths, and MUST NOT pick one. A `conflicts` row does not by itself cause exit 1; it is reported alongside the judgement.

## C-9. Input formats

Only the three carrier forms in `data-model.md` § 2.1 are parsed. Unknown rows inside a known table are `2` (malformed record), not silently skipped.

## C-10. Command examples

> **Premises / execution status (per example)**: the engine file does **not exist yet** — these examples are written against the interface above and are pinned by `tests/contract/test_role_edge_engine.py` (route: contract-test pinning). Premises: the engine ships at `scripts/python/role-edge-check.py` with `--action report|query`, `--format json|text`, and the exit codes of C-2; fixtures ship under `tests/fixtures/superagent-role/`. When the engine lands, `/speckit.tasks` MUST re-run these commands and record the readings in `test-evidence/`.

```bash
python3 scripts/python/role-edge-check.py --help
python3 scripts/python/role-edge-check.py --action report --state-dir tests/fixtures/superagent-role/root-a-b/state --teams-dir tests/fixtures/superagent-role/root-a-b/teams --logs-dir tests/fixtures/superagent-role/root-a-b/logs --registry-dir tests/fixtures/superagent-role/root-a-b/registry
python3 scripts/python/role-edge-check.py --action query --parent root --child A --state-dir tests/fixtures/superagent-role/root-a-b/state --teams-dir tests/fixtures/superagent-role/root-a-b/teams --logs-dir tests/fixtures/superagent-role/root-a-b/logs --registry-dir tests/fixtures/superagent-role/root-a-b/registry
```

Expected (pinned by the contract test, not assumed here): `--help` exits 0; the `report` run exits `0` with `summary.edges == 2`, `executors` containing `A` with `roles: ["subagent","superagent"]` and `depth: 1`, `B` with `roles: ["subagent"]` and `depth: 2`; the `query` run exits `0` with `edge_exists: true`.

## C-11. Guarding tests

`tests/contract/test_role_edge_engine.py` — CLI contract (C-1, C-2), schema (C-3, C-4), violation set (C-5), read-only (C-6), determinism (C-7), conflict (C-8), input strictness (C-9), and the three mutation drills: (a) classify roles by executor type → red; (b) inject one violation → red; (c) move a role claim off its edge → red.
