# Contract — Distribution & Mirror Obligations

**Feature**: 084 Harness 三重结构 | **Date**: 2026-11-05
**This file is the plan-side list deliverable the spec's A9 asks for**: the asset roster `specify init` must carry and
the upgrade actions an existing client project goes through.

## A — Distribution (what `specify init` must deliver)

- **DM-01 Asset roster** — after an init on a tree produced by this branch, a client project carries:
  `shared/declarations/contract.yaml`, `shared/declarations/facts/*.yaml` (one file per fact),
  `shared/declarations/exclusions/*.yaml` (one file per reason, at most as many as there are reasons), and the owner
  document `shared/definitions/harness-triple-definitions.md` — all under `.specify/` in the created project.
  The roster is a directory contract, not a file list: a new fact file needs no roster edit.
- **DM-02 Mechanism: the existing one, unchanged.** `copy_local_templates()` already copies the whole `shared/` tree
  through `copy_tree_with_rewrite()`, and that copy is recursive: nested subdirectories arrive complete (verified on the
  source route — `shared/definitions/` arrived with 12 files, 62 Markdown files in total,
  `test-evidence/plan-readings.txt` § R6). Therefore `shared/declarations/` needs **no** new asset-list code, **no** new
  copy step, and **no** entry in the obsolete-asset registry. A second distribution mechanism is a violation of the
  Two Hats rule, not an implementation choice.
- **DM-03 The copy rewrites path references — declarations must survive it.** `rewrite_paths()` turns source-form
  references (`shared/…`, `scripts/…`, `skills/…`) into their `.specify/` form in every UTF-8 file it copies, YAML
  included. Two obligations follow and both are mechanical: (a) declaration path values stay in source form, and the
  reader strips one optional leading `.specify/` (schema DS-10); (b) the rewritten file MUST still be inside the YAML
  subset — the rewrite changes string content only, and the subset test runs on the client copy in the distribution
  verification below, not only on the framework source.
- **DM-04 Upgrade action for an existing project.** The copy is an additive merge (`dirs_exist_ok` semantics): the
  declarations arrive as new files and nothing existing is deleted. An upgraded project therefore gains the layer without
  a migration step of its own; a project that had hand-written declarations keeps them, and the checker's duplicate
  reading is what surfaces a clash. No deletion registry entry is added by this feature.
- **DM-05 Degraded mode (legacy project, directory absent).** Every consumer engine and the checker itself MUST
  annotate and continue: the checker exits 2 with an explicit input-error label naming the missing directory; an engine
  reading an absent fact annotates its output with the `[[STR-014]]` label. Neither may raise, and neither degradation
  may be read as a pass.
- **DM-06 Installation-route caveat, recorded not waived.** `get_resource_path()` prefers the installed package, so the
  console script on `PATH` distributes the **installed snapshot** (measured: 55 Markdown files) rather than the tree
  under edit (62). Distribution is therefore verified on the source route (`PYTHONPATH=<repo>/src`), and the console
  route's reading is kept as a dated observation. This is a property of the environment, not of this feature; the plan
  records it as a falsified premise with a decision (`EP-002`) instead of silently testing the wrong tree.

## B — Mirrors (what must land identically)

- **DM-07** `shared/` → `.specify/shared/` — the new `declarations/` subtree and the owner document are projected by the
  existing pair in `scripts/python/sync-mirrors.py`. The mirror is generated, never hand-edited.
- **DM-08** `scripts/python/harness-triple-check.py` and `scripts/python/declaration_reader.py` →
  `.specify/scripts/python/` — the `scripts` pair is **strict**: a mirror-only extra file fails, and a missing mirror is
  drift.
- **DM-09** The gate host `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` →
  `.specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py`, and every owner document this feature turns into a
  pointer (`shared/definitions/flow-class-definitions.md`, `shared/guidelines/better-harness.md`,
  `shared/workflow/feedback-step.md`, `shared/workflow/expression-gates.md`,
  `shared/workflow/acceptance-hardening.md`, `shared/definitions/framework-map.md`) → its `.specify/` twin.
- **DM-10 Verification criterion is drift-relative, because the baseline was measured.** Before any edit,
  `python3 scripts/python/sync-mirrors.py --check` exits 0 with all six pairs `ok` (119 script files, 62 shared files;
  `test-evidence/plan-readings.txt` § R4). The closure criterion is "no **new** drift on the pairs this feature touches",
  measured against that baseline — never a bare "all green" written before the run.
- **DM-11** New directory registration: `shared/declarations/` plus its two subdirectories are registered in
  `shared/definitions/framework-map.md` in the same change, and that registration is mirrored to
  `.specify/shared/definitions/framework-map.md` by DM-07 (a guard test reads both copies).
- **DM-12** No new top-level directory is created. Everything this feature adds lives under `shared/`, `scripts/`,
  `tests/`, `docs/` or `src/`.

## C — Documentation entry and release note

- **DM-13** `docs/` gains a pointer entry registered per `docs/concepts/documentation-model.md` (the page states what
  the layer is and routes to the owner document; it MUST NOT restate any value domain), and `CHANGELOG.md` gains one
  entry naming the feature and the three-layer change.

## D — Distribution verification procedure (route (b), per step)

No step below was run in the state this feature will produce, because the declarations do not exist yet. Each step's
premises are listed so the implement stage re-measures them instead of trusting this table.

| Step | Command shape | Premises |
|------|---------------|----------|
| 1. create a scratch project in a sanctioned root | `mkdir -p .specify/.tmp/084-init/ && cd .specify/.tmp/084-init` | `.specify/.tmp/` is matched by `.specify/.gitignore` (verified: `git check-ignore` resolves the rule at `.specify/.gitignore:30`); a bare `/tmp` or `~/tmp` is forbidden by the temp-directory discipline |
| 2. initialise from the source checkout | `PYTHONPATH=<repo>/src python3 -c "from specify_cli import main; main()" init demo --ai claude --script sh --no-git --ignore-agent-tools` | route B resolves the working tree (measured: `get_resource_path()` → repo root, exit 0); the console-script route resolves the installed snapshot and does **not** satisfy this step (DM-06) |
| 3. assert the roster | `test -f demo/.specify/shared/declarations/contract.yaml` and a directory listing of `facts/` and `exclusions/` | DM-01 is the roster; the assertion is per-file, not "the directory exists" |
| 4. assert the layer is usable in the client copy | `python3 demo/.specify/scripts/python/harness-triple-check.py --action verify --repo demo` | exit 0 expected only if the copied declarations are self-consistent after the DM-03 rewrite; a non-zero exit here is the finding this step exists to produce, and MUST be recorded rather than retried until green |
| 5. clean up | `rm -rf .specify/.tmp/084-init` | teardown is verified like setup: a second run of steps 1–2 must not inherit state from the first |
