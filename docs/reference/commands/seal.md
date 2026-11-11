# `/speckit.seal` — Seal Command

Takes one reviewed spec to its terminal state. A spec whose review conclusion is settled is first **sealed**: split slices are merged back into the parent spec, the merged slices are archived under the parent's `slices/` directory, then the parent is fixed at `Sealed` with a receipt. The merge and archive halves are inspectable and applicable on their own; sealing never precedes a complete merge, and archival starts only after a successful `merge-apply`. `Sealed` is the only status admitted to the existing retirement lanes.

```text
/speckit.seal                                       # target the current feature
/speckit.seal .specify/specs/074-goal-team-sdd-unification
/speckit.seal merge-plan .specify/specs/<parent>    # read-only merge preview
/speckit.seal merge-apply .specify/specs/<parent>   # merge write only
/speckit.seal archive-plan .specify/specs/<parent>  # read-only archive preview
/speckit.seal archive-apply .specify/specs/<parent> # archive write only
```

## Three pieces, one engine

| Piece | Path | Role |
|---|---|---|
| Command template | `templates/commands/seal.md` | thin entry: user input, delegation, glossary, compiled wrap-up, handoffs |
| Internal skill | `skills/internal/seal-artifact/SKILL.md` | orchestration and reporting only — never recomputes a judgment |
| Engine | `scripts/python/seal-utils.py` | every judgment, every count, every verdict |

Per-tool command copies are generated from the template by `scripts/python/regen-command-copies.py` (never hand-copied); the skill is projected into `.specify/skills/internal/seal-artifact/` by `scripts/python/sync-mirrors.py`.

The engine owns its own call surface. Its six-action set, the meaning of each exit status, the `--json` payload shape and the per-action argument manifests are all read from the engine itself: `python3 scripts/python/seal-utils.py --help`, the engine contract `.specify/specs/099-speckit-seal/contracts/seal-engine.contract.md` (C-001…C-004, C-010, revised in place to six actions), and the archive action contract `.specify/specs/100-seal-slice-archive/contracts/archive-actions.contract.md` (C-101…C-116). This page does not restate those closed sets — a second copy would drift.

## Execution flow

1. **Preview the merge** (read-only). `--action merge-plan` reports the slice set, the per-output-file actions, the ID maps and the conflict list; it writes nothing. Open conflicts are named individually and stop the run before any write — repair the named inputs and rerun the preview until the conflict no longer reproduces.
2. **Apply the merge** (split parents only). `--action merge-apply` writes the parent-side merged outputs, `merge-manifest.json` and the slice-side `**Merged into**:` markers. The action is deterministic and idempotent.
3. **Commit the merge batch.** The archive preview and the seal judgment both refuse on a dirty spec tree, so the merge products are committed first — staged by explicit path, never `git add -A`.
4. **Preview the archive** (read-only). `--action archive-plan` runs the same computation `archive-apply` repeats as its read-only stage and writes nothing. The engine names the outcome: `would-archive` proceeds to step 5; `already-archived` and `not-applicable` are named successes that skip to step 7; a refusal lists every unmet condition with its repair path and persists nothing; an error is an input or environment defect. An interactive run shows this preview before applying; an unattended authorized run applies directly and records the decision in the archived parent spec's `test-evidence/` round record.
5. **Apply the archive** (only when the preview reports `would-archive`). `--action archive-apply` moves every slice wholesale with `git mv` semantics, rewrites the live references, writes `archive-manifest.json` and amends the parent `merge-manifest.json` path/digest fields as one atomic batch. A failure inside the batch restores it from the original bytes and exits `2` (`write-failed`).
6. **Commit the archive batch.** The moved slice directories, `archive-manifest.json`, the rewritten live carriers and the amended parent `merge-manifest.json` are committed by explicit path. The seal judgment refuses on a dirty spec tree, so this commit lands before step 7.
7. **Run the seal judgment.** `--action seal` computes every conjunctive condition in a read-only phase; only when all hold does it write its batch (`seal.md`, the registry row and the feature detail). A refusal lists every unmet condition with its repair path and persists nothing. An environment or state contradiction is an error class of its own, never a pass. Archival is never gated on this verdict: the spec's slices stay archived whether the judgment ends `Sealed` or in named blocking.
8. **Report and hand off.** On success the spec is `Sealed` and eligible for the existing retirement lane; on a seal refusal the named repairs are applied and the command rerun — the archive steps report `already-archived` and the same refusal list reproduces; on an archive refusal nothing was persisted, so the repairs are applied and the command rerun before the seal judgment is reached.

The status transition and its conjunctive conditions are owned by `shared/workflow/acceptance-hardening.md` § Feature Status; the registry-row wiring is owned by `shared/workflow/feature-integration.md`. The slice disposition is owned by `shared/definitions/non-disposable-definitions.md` (Disposition Set / Disposal Pathways). All are reached by pointer from the command and the skill.

## Artifacts

| Artifact | Location | Written by |
|---|---|---|
| `merge-manifest.json` | parent spec directory | `merge-apply` |
| Merged parent-side outputs | parent spec directory | `merge-apply` |
| Slice `**Merged into**:` marker | each slice's `requirements.md` | `merge-apply` |
| Moved slice directories | `<parent>/slices/<slug>` | `archive-apply` |
| `archive-manifest.json` | parent spec directory | `archive-apply` |
| Rewritten live carriers + amended `merge-manifest.json` | carriers recorded in `references.rows[]` | `archive-apply` (same batch) |
| `seal.md` receipt | parent spec directory | `seal` (success only) |
| Registry row + feature detail status | `.specify/features.md`, `.specify/features/<ID>.md` | `seal` (same batch) |
| Refusal list | stdout only | any action (refusals persist nothing) |

Review records, code-review records and measurement files are read-only inputs throughout: the run never edits, re-verdicts or downgrades them.

## Archive walkthrough (executable)

Run against a split parent whose merge batch is committed. `<parent>` is the parent spec directory name, `<slug-a>` / `<slug-b>` its slices.

```bash
# 1. Preview — read-only, zero writes; outcome is would-archive / already-archived / not-applicable
python3 scripts/python/seal-utils.py --action archive-plan \
  --spec-dir .specify/specs/<parent> --repo . --json

# 2. Apply — recomputes the plan, writes one atomic batch (git mv moves + rewrites + manifest)
python3 scripts/python/seal-utils.py --action archive-apply \
  --spec-dir .specify/specs/<parent> --repo .

# 3. Verify the move pairs: R on every moved file, A = archive-manifest.json, M = rewritten carriers, no D
PINNED=$(python3 -c 'import json;print(json.load(open(".specify/specs/<parent>/archive-manifest.json"))["pinned_commit"])')
git diff --name-status -M "$PINNED" -- \
  .specify/specs/<parent>/slices .specify/specs/<slug-a> .specify/specs/<slug-b>

# 4. Commit the archive batch by explicit path (never git add -A)
git add -- .specify/specs/<parent>/slices/<slug-a> .specify/specs/<parent>/slices/<slug-b> \
  .specify/specs/<parent>/archive-manifest.json .specify/specs/<parent>/merge-manifest.json \
  .specify/register.md .specify/features/<ID>.md
git commit -m "<single-line message>"

# 5. Idempotency: both actions report already-archived and the rerun leaves zero diff
python3 scripts/python/seal-utils.py --action archive-plan --spec-dir .specify/specs/<parent> --repo .
python3 scripts/python/seal-utils.py --action archive-apply --spec-dir .specify/specs/<parent> --repo .
git status --porcelain
```

Every refusal exit (`1`) names all unmet conditions with a fix and a rerun command and persists nothing — repair the named inputs and rerun the same action; the identical input reproduces the identical list. `not-applicable` is a named success for a spec with no slice set, never a silent skip.

## Recovery walkthrough (executable)

The engine ships no rollback action; recovery is the documented git-level recipe below (contract C-110), executed verbatim. `<pinned_commit>` is the manifest's `pinned_commit`, and the manifest's `slices[]` / `references.rows[]` are the rollback plan.

```bash
# 1. Read the pinned commit, the slice order and the reference ledger from the manifest
python3 - <<'PY'
import json
m = json.load(open(".specify/specs/<parent>/archive-manifest.json"))
print("pinned:", m["pinned_commit"])
for s in sorted(m["slices"], key=lambda s: s["order"]):
    print("slice:", s["order"], s["to"], "->", s["from"])
for r in m["references"]["rows"]:
    if r["kind"] == "live-rewrite":
        print("live:", r["carrier"], r["line"])
for r in m["references"]["runtime"]:
    for u in r["updates"]:
        print("runtime:", r["carrier"], u["line"])
PY

# 2. Reverse-move every slice in slices[] order
git mv .specify/specs/<parent>/slices/<slug-a> .specify/specs/<slug-a>
git mv .specify/specs/<parent>/slices/<slug-b> .specify/specs/<slug-b>

# 3. Restore every live-rewrite carrier and the parent merge-manifest.json (index + worktree)
PINNED=<pinned_commit>
git restore --source="$PINNED" --staged --worktree -- \
  .specify/specs/<parent>/merge-manifest.json .specify/register.md .specify/features/<ID>.md <other carriers>

# 4. Runtime face (git-ignored .specify/state/**): reverse-write each runtime row's after -> before,
#    per the manifest's references.runtime[].updates[]; leave spine_state and stage readings untouched

# 5. Remove the manifest apply created
git rm -f --cached .specify/specs/<parent>/archive-manifest.json
rm .specify/specs/<parent>/archive-manifest.json

# 6. Completion check: zero tree diff against the pinned commit, clean status
git diff --exit-code "$PINNED" -- \
  .specify/specs/<parent> .specify/specs/<slug-a> .specify/specs/<slug-b> <live carriers>
git status --porcelain
```

If the archive batch was already committed, the equivalent form is a single `git revert <archive-commit>`. Neither form touches changes outside the archive batch, and the completion check must also re-verify each `references.rows[]` `before` / `after` pair line by line.

## Retirement admission

The engine's `archive-gate` action is the single owner of the retirement admission query ("only `Sealed` may be retired"). It is consumed by the existing retirement lanes — `/speckit.sanitize`'s retirement path and `manage-features`' archive-pointer action — which query it before acting and refuse by name when the answer is negative, pointing back to `/speckit.seal`. **Slice archival is a different lane**: it is not retirement, it never queries `archive-gate`, never reads or writes `.specify/archive/`, and runs whether the seal judgment ends `Sealed` or in named blocking. The seal command defines the admitted state; it performs no retirement, moving or deletion.

## Boundaries

- `/speckit.feature` keeps ownership of the feature-registry reconcile and its declaration semantics; the seal run writes only its own transition and records.
- `/speckit.review` owns review records and verdicts — the seal run reads them.
- `/speckit.sanitize` and `/speckit.docs` keep ownership of retirement and documentation-space actions.
- `/speckit.goal migrate-archive` keeps ownership of spec-local goal/team tree migration; seal neither migrates nor deletes those trees.

## Related

- Engine contract: `.specify/specs/099-speckit-seal/contracts/seal-engine.contract.md`; records and boundaries: `.specify/specs/099-speckit-seal/contracts/records-and-boundaries.contract.md`
- Archive actions contract: `.specify/specs/100-seal-slice-archive/contracts/archive-actions.contract.md`; manifest schema: `.specify/specs/100-seal-slice-archive/contracts/archive-manifest.contract.md`
- Status owner: `shared/workflow/acceptance-hardening.md`; integration protocol: `shared/workflow/feature-integration.md`
- Walkthroughs: `.specify/specs/099-speckit-seal/quickstart.md`; slice-archive run: `.specify/specs/100-seal-slice-archive/quickstart.md`
