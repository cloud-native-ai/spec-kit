# `/speckit.seal` — Seal Command

Takes one reviewed spec to its terminal state. A spec whose review conclusion is settled is first **sealed**: split slices are merged back into the parent spec, then the parent is fixed at `Sealed` with a receipt. The merge half is inspectable and applicable on its own, but sealing never precedes a complete merge. `Sealed` is the only status admitted to the existing archive lanes.

```text
/speckit.seal                                  # target the current feature
/speckit.seal .specify/specs/074-goal-team-sdd-unification
/speckit.seal merge-plan .specify/specs/<parent>   # read-only merge preview
/speckit.seal merge-apply .specify/specs/<parent>  # merge write only
```

## Three pieces, one engine

| Piece | Path | Role |
|---|---|---|
| Command template | `templates/commands/seal.md` | thin entry: user input, delegation, glossary, compiled wrap-up, handoffs |
| Internal skill | `skills/internal/seal-artifact/SKILL.md` | orchestration and reporting only — never recomputes a judgment |
| Engine | `scripts/python/seal-utils.py` | every judgment, every count, every verdict |

Per-tool command copies are generated from the template by `scripts/python/regen-command-copies.py` (never hand-copied); the skill is projected into `.specify/skills/internal/seal-artifact/` by `scripts/python/sync-mirrors.py`.

The engine owns its own call surface. Its action set, the meaning of each exit status, the `--json` payload shape and the per-action argument manifests are all read from the engine itself: `python3 scripts/python/seal-utils.py --help`, and the contract `.specify/specs/099-speckit-seal/contracts/seal-engine.contract.md` (C-001…C-004, C-010). This page does not restate those closed sets — a second copy would drift.

## Execution flow

1. **Preview the merge** (read-only). `--action merge-plan` reports the slice set, the per-output-file actions, the ID maps and the conflict list; it writes nothing. Open conflicts are named individually and stop the run before any write — repair the named inputs and rerun the preview until the conflict no longer reproduces.
2. **Apply the merge** (split parents only). `--action merge-apply` writes the parent-side merged outputs, `merge-manifest.json` and the slice-side `**Merged into**:` markers. The action is deterministic and idempotent.
3. **Commit before sealing.** The seal judgment refuses on a dirty spec tree, so the merge products are committed first — staged by explicit path, never `git add -A`.
4. **Run the seal judgment.** `--action seal` computes every conjunctive condition in a read-only phase; only when all hold does it write its batch (`seal.md`, the registry row and the feature detail). A refusal lists every unmet condition with its repair path and persists nothing. An environment or state contradiction is an error class of its own, never a pass.
5. **Report and hand off.** On success the spec is `Sealed` and eligible for the existing archive lane; on a refusal the named repairs are applied and the command rerun — the same input reproduces the same list.

The status transition and its conjunctive conditions are owned by `shared/workflow/acceptance-hardening.md` § Feature Status; the registry-row wiring is owned by `shared/workflow/feature-integration.md`. Both are reached by pointer from the command and the skill.

## Artifacts

| Artifact | Location | Written by |
|---|---|---|
| `merge-manifest.json` | parent spec directory | `merge-apply` |
| Merged parent-side outputs | parent spec directory | `merge-apply` |
| Slice `**Merged into**:` marker | each slice's `requirements.md` | `merge-apply` |
| `seal.md` receipt | parent spec directory | `seal` (success only) |
| Registry row + feature detail status | `.specify/features.md`, `.specify/features/<ID>.md` | `seal` (same batch) |
| Refusal list | stdout only | `seal` (refusals persist nothing) |

Review records, code-review records and measurement files are read-only inputs throughout: the run never edits, re-verdicts or downgrades them.

## Archive admission

The engine's `archive-gate` action is the single owner of the "only `Sealed` may be archived" query. It is consumed by the existing archive lanes — `/speckit.sanitize`'s retirement/archival path and `manage-features`' archive-pointer action — which query it before acting and refuse by name when the answer is negative, pointing back to `/speckit.seal`. The seal command itself defines the admitted state; it performs no archival, moving or deletion.

## Boundaries

- `/speckit.feature` keeps ownership of the feature-registry reconcile and its declaration semantics; the seal run writes only its own transition and records.
- `/speckit.review` owns review records and verdicts — the seal run reads them.
- `/speckit.sanitize` and `/speckit.docs` keep ownership of archival, retirement and documentation-space actions.
- `/speckit.goal migrate-archive` keeps ownership of spec-local goal/team tree migration; seal neither migrates nor deletes those trees.

## Related

- Engine contract: `.specify/specs/099-speckit-seal/contracts/seal-engine.contract.md`; records and boundaries: `.specify/specs/099-speckit-seal/contracts/records-and-boundaries.contract.md`
- Status owner: `shared/workflow/acceptance-hardening.md`; integration protocol: `shared/workflow/feature-integration.md`
- Walkthrough: `.specify/specs/099-speckit-seal/quickstart.md`
