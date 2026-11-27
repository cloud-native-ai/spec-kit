# Feature Reference — 111-general-best-practices

## Binding

| Field | Value |
|-------|-------|
| Requirement key | `111-general-best-practices` |
| Bound Feature | **111 — General Best Practices（通用最佳实践）** |
| Binding basis | The module is a shipped framework content layer: observations ride the existing feedback engine by pointer, the knowledge-recording obligation stays with its existing owner, and the module manifest owns the promotion procedure and generality criterion (requirements A-22). Feature 111 is a new standalone feature (no parent slice) per the stage brief. The source registry binding (ai-harness Feature 040) is not reused — the target registry has no equivalent entry, and a hard rebind would misstate ownership (requirements A-3). |
| Registry posture | No Feature 111 row and no detail file exist today. This stage does **not** edit `.specify/features.md` or `.specify/features/111-*.md`: the stage brief forbids registry edits, and FR-009 names the later feature-registration stage as the sole exception. The `Draft → Planned` advance therefore lands with that later stage, not here. |
| Feature detail | `.specify/features/111-general-best-practices.md` — to be created by the feature-registration stage |
| Source plan set | `/storage/project/cloud-native-ai/ai-harness/.ah/specs/087-general-best-practices/` (content source; its contract clause ids are not reused) |

## Delivery surface (framework source → runtime mirror)

| # | Source path | Role | Mirror / copies |
|---|-------------|------|-----------------|
| 1 | `shared/best-practices/README.md` | Manifest: closed four-category set (sole table), reader/scope, entry shape, accumulation (observation by pointer + module-owned promotion procedure and criterion), seed pointer | `.specify/shared/best-practices/README.md` (sync-mirrors) |
| 2 | `shared/best-practices/programming-languages.md` | Category owner file — [[STR-006]] placeholder at delivery | mirror (sync-mirrors) |
| 3 | `shared/best-practices/system-interfaces.md` | Category owner file — [[STR-006]] placeholder at delivery | mirror (sync-mirrors) |
| 4 | `shared/best-practices/programming-frameworks.md` | Category owner file — [[STR-006]] placeholder at delivery | mirror (sync-mirrors) |
| 5 | `shared/best-practices/programming-tools.md` | Category owner file — seed entry [[STR-007]] | mirror (sync-mirrors) |
| 6 | `shared/definitions/framework-map.md` | One registration row for `.specify/shared/best-practices/` (Where + Feature 111 + README pointer + framework-source pointer) | `.specify/shared/definitions/framework-map.md` (sync-mirrors) |
| 7 | `tests/contract/test_general_best_practices.py` | The feature's only new test file: six legs (a)–(f) + module-read prelude (residue, cited-path existence) | none |

Not touched: `src/` (no CLI or packaging change), `templates/` (no template change), `.specify/instructions.md` (its Framework Map section is already a pointer), `.specify/.gitignore` (no new runtime directory), `scripts/python/` (no engine), `shared/definitions/decision-definitions.md` and its checker (no decision items), `.specify/features.md` / `.specify/features/111-*.md` (deferred), `.specify/glossary.md` (deferred).

## FR → surface map

| FR | Delivering surface |
|----|--------------------|
| FR-001 | Manifest `README.md` (closed set table, readers/scope, entry shape, change process) + `manifest.contract.md` + guard legs (a)(f) |
| FR-002 | Four owner files + `entry-shape.contract.md` + guard leg (b) |
| FR-003 | Seed entry in `programming-tools.md` + `entry-shape.contract.md` C-204 + guard leg (c) |
| FR-004 | Manifest accumulation section (observation pointer + module-owned promotion procedure and criterion) + `accumulation.contract.md` + guard leg (d) |
| FR-005 | Framework-map row (source + mirror) + `distribution-guard.contract.md` C-403 + guard leg (e) |
| FR-006 | Existing init copy + existing mirror pair + `distribution-guard.contract.md` C-401/C-402/C-407 + existing parity suite |
| FR-007 | `tests/contract/test_general_best_practices.py` per C-404 |
| FR-008 | Adaptation in the ported text + guard module-read prelude (residue + cited paths) per C-404/C-405 |
| FR-009 | Containment per C-406; measured by `git diff --name-only 0419adae5..HEAD` at review |

## SC → evidence map

| SC | Evidence |
|----|----------|
| SC-001 | Guard legs (a)(b)(f): five-file set, four-row sole table, 4/4 links, placeholder ⇔ zero entries |
| SC-002 | Guard leg (c): the three seed facts + the SSH extension |
| SC-003 | Guard leg (d): pointer chain 2/2 resolves (record action, knowledge-recording owner), [[STR-001]] present, zero `best-practices*.py` engine files; the manifest owns the promotion procedure and criterion (A-22) |
| SC-004 | Guard leg (e) (row in source and mirror); `sync-mirrors.py --check` zero DIFF; init proof per C-407; `git diff --numstat 0419adae5..HEAD -- src/` = zero lines |
| SC-005 | Guard module-read prelude: three residue-literal counts = 0; cited-path existence output |
| SC-006 | `git diff --name-only 0419adae5..HEAD` set difference against FR-009, with the per-entry accounting-body predicate; review re-check |
| SC-007 | The runner's exit code + red-first capture + name-level baseline comparison in the implement stage record |

## Supersession and dated records

- The source module at `ai-harness/shared/best-practices/` is the **content source**, not a live owner in this repository; its settled text ports in substance with the FR-008 adaptations. This target module supersedes nothing in spec-kit (no prior `best-practices/` exists).
- The source spec artifacts (requirements / plan / tasks / contract / verification) remain dated records in the source repository; this feature's contract face is `contracts/` here, and the source clause ids are not reused.
- No framework-map row and no instructions pointer existed in the source repository; the target adds exactly one map row because its directory governance requires same-change registration, and adds no instructions pointer because the existing Framework Map section is already a pointer.

## Handoff to `/speckit.tasks`

- **Tests Mode**: ON (execution class, Principle IV). The guard is written first and must fail before the module exists; the module, the map row and the mirror regeneration follow; the mirror parity suite is reused, never duplicated.
- **Work packages**: guard; five documents; US1 mirror establishment (T007A) + map row + final write-mode mirror regeneration (T012); stage closure evidence (init drill, red-first/green record, containment reading).
- **Re-measure list**: `research.md` § Re-measure list 1–6 (source residue lines, mirror baseline, feedback action set + knowledge-recording owner, pytest availability, map sibling-row style, baseline commit + run id).
- **Wrap-up duties**: targeted set through `scripts/bash/run-tests.sh` with `--names-out`; red-first capture kept; name-level new-failure comparison; containment reading per FR-009; no registry edit (deferred to the feature-registration stage).