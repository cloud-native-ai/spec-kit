# Phase 0 Research: 063-review-p1-governance（决策与实测记录）

**Date**: 2026-10-19 | **Method**: no standalone research input existed (`SPECS_DIR/research.md` absent at start); findings inlined-then-promoted here from a direct codebase exploration pass (Explore subagent sweep + targeted reads of every file this plan touches, 2026-10-19). No external-source evaluation was needed — every decision below was verified against this repo's sources.

## D-1 — F1 charset owner + extractor (C-1/C-2)

The owner (`shared/definitions/contract-clause-definitions.md` § 4 rule 2, the file's own header declares it the 唯一真源 for citation-group rules) declares block boundary, nesting tolerance, and range expansion — but never the delimiter charset. `clause_extract.py` `parentheticals()` (L125-140) is ASCII-only, depth-counter nesting, emits only depth-0 groups. Decision: declare `(`|`（` / `)`|`）` with same-width nesting and malformed-group reporting in the owner body; implement exactly that in the extractor; deterministic self-test samples go to `tests/contract/test_clause_forms.py` (the extractor's existing external self-test home — the file has no in-file `_selftest`).

## D-2 — F1 wiring + baseline freeze (C-5/C-6/C-7)

`account-clause-coverage.py` CLI (verified): positional target, `--spec-dir`, `--corpus-root`, `--baseline` (default `<spec-dir>/coverage-baseline.txt`, `BASELINE_NAME`), `--json`, `--list-named`, `--freeze` (prints the freeze document; usage redirects to file). Current live state measured: `--spec 062-humanize-command` → `status: baseline-missing`, 512 errors; `find .specify/specs -name coverage-baseline.txt` → only 053. Wiring lands in `analyze-artifacts/SKILL.md` (load table + fixed step, read-only run) + one command-face line in `templates/commands/analyze.md`; freeze duty lands in `create-tasks/SKILL.md` § Runtime-evidence landing points. Freeze target = the accountant's own default path (spec-dir root); baseline-missing surfaces with the remedy (re-run tasks), never silently skipped.

## D-3 — F2 analyze checklist awareness (C-3/C-4)

`analyze-artifacts/SKILL.md` § 2 load table (L62-68) enumerates requirements/plan/tasks/registry/constitution — no checklists row; `grep -c checklist` on the command template is 0. `Gap` is already a defined tag in `create-checklist/SKILL.md` § 5 (L97-99), so no new tag vocabulary is needed — the analyze side consumes what the checklist side already defines. Disposition markers are skill-defined and deterministic (raised-as-finding id / covered-by anchor); free prose never satisfies them.

## D-4 — F2 recheck + waiver owner points (C-8/C-9/C-10)

Verified against the clarify rulings: `create-checklist/SKILL.md` § 5 L94 already says "Each run creates a NEW file — never overwrite" (the seed of the recheck form); no recheck notion exists anywhere in skills/ yet. `implement-feature/SKILL.md` § Step 2 (L44-54) has exactly two branches (STOP/ask → waiver; all-complete → proceed) — the third branch (answered per recheck ⇒ counted answered) and the four-part waiver format land there, matching 061 REC-C5/C6's named targets.

## D-5 — F3 REC persistence (C-11..C-14)

`register.md` verified: pointer-row table `| 编号 | 含义(一行) | 权威路径(完整陈述) | 状态 |`, zero `REC-` rows. `instructions-template.md` § ID Register L165 enumerates D-/OI-/S/T-/F-/B- — gains `REC-`; the live `.specify/instructions.md` receives it via `scripts/bash/generate-instructions.sh` (the canonical generator; hand-editing the runtime copy is forbidden). `review-template.md` Replacement Rule 3 (L181) currently FORBIDS bare relative paths — the flip to repo-relative-primary is a deliberate inversion for REC targets (061's 134 machine-local absolute paths made its 22 RECs unresolvable; the report's own §0 documents why blob-URL form fails when the commit is unreachable). Feedback entry: the review report's "Mode 5 自省" label is historical — the live mechanism is `/speckit.feedback` → manage-feedback Path A digest § A3 自省(Introspection) (verified: the step exists, routes findings to local-sink channels incl. direct-fix, and is where the 2026-10-15 F-01 backlog entry actually came from; `feedback-step.md` itself contains no "Mode 5"). C-13 names A3, the current name of the same path.

## D-6 — F3/E2 transition row (C-15)

`feature-integration.md` transition table (L31-37): five rows; `/speckit.checklist` owns `Implemented → Ready for Review`; no review row; L29 rule "Each command owns exactly one transition". Adding the review row keeps the rule true (one row per command; two commands may own the same transition under different conditions). `test_neutrality_budget.py` pins the "Status State Machine" heading presence-only — safe. The intro command list (L7) gains `/speckit.review`.

## D-7 — F4 renderer/engines (C-20..C-24)

Renderer verified: `_render_call_line()` (probe-utils.py L874-886) emits only `--unit-id`/`--unit-type` for kind=engine; `_CALL_ENGINE_RE` (L913) anchors on `python3 <owner> --action <action>` so extended argument lines keep parsing; fingerprint = sha256[:12] of the registry wrap-up projection (L868-871) — a renderer change drifts all units until recompile (C-25 expects exactly that). Engine validations verified: `action_determine()` raises `--run-id` (L1390-1391) then `--complexity` (L1392-1397) sequentially; `action_record()` raises `--run-id` (L716-718) then non-empty review (L720-722) then points (L723-728); both exit 2 on input errors; idempotency duplicate-return at L1410-1413 stays untouched (E1). Mechanism decision: the rendered argument set is DERIVED from the engines (FR-030) — each wrap-up engine exposes a machine-readable args manifest (e.g. `--action args-manifest`) built from its own parser; `compile-embeds` fetches the manifest per handler at compile time; an engine/action pair without a manifest fails the compile loudly (fast fail — no silent unit-id-only fallback). Placeholder syntax: angle brackets (`<RUN_ID>`), convention declared in probe-definitions.md § Handler note and carried by a rendered convention line. The manifest action joins the engine action closed set (`contracts/engine-action-sets.md` + `test_probe_engine_action_sets.py` updated in the same change). `exec-quant.py` gets the manifest too (uniform mechanism) — its current face line already succeeds, so its rendered line is expected to stay argument-identical.

## D-8 — F4 backlog flip (C-25)

`backlog.md` line 89 verified live: dated 2026-10-15, route `direct-fix`, status `open(...)` with four named target files — exactly the fix this feature lands. Flips `closed` in the same commit as the recompiled units, with `--check` output as evidence.

## D-9 — F5/F8 carrier + citation owners (C-16..C-18)

`create-tasks/SKILL.md` item 2 (L202-206) verified: closed carrier enumeration is exactly "Per-phase prerequisites and `[~]` task notes"; the cross-artifact drift check (L211-214) is separate and untouched. `tasks-template.md` § Environment Prerequisites ACTION REQUIRED (L87-96) gains the ISO-date + pointer duty. F8 owner correction (disclosed): FR-025's conditional "where implement-feature/SKILL.md prescribes the red-first note's shape" has no referent — the note's shape is prescribed in `create-tasks/SKILL.md` § Runtime-evidence landing points (L364-365: command, real output, exit status). The verbatim-gate-quote duty lands at that actual owner (One Source of Truth: one shape owner); implement-feature gets no duplicate restatement. Corrected in passing from the requirement's named file; recorded here and at wrap-up.

## D-10 — F6 evidence binding (C-26..C-28)

`verification-log-template.md` verified: five sections, flat key-value, no per-sample slot. Hash algorithm decision (requirements left it to plan): SHA-256 over archived file bytes (`sha256sum`-compatible, deterministic, declarable in the template). Gate registration: `gate-implement-evidence-binding` ([[STR-001]]) as a `command-gate` row beside `gate-implement-checklist-waiver` (L117) + `h-gate-evidence` HandlerBinding at `@point:confirm-gate` — reusing the existing gate-probe mechanism (firing evidence via feedback engine `--lifecycle-point`), no new subsystem. Skill-side anchor: implement-feature Step 9 (the step that populates `verification.md` from the template) — the skill carries no per-feature `GATE-8` numbering (verified; GATE-8 is a tasks.md-local construct), so "在 GATE-8 旁" resolves to the verification-log step. Corrected in passing from the requirement's literal; recorded here and at wrap-up.

## D-11 — F7 pre-flight (C-19/C-29/C-30)

Verified: the re-freeze duty is declared only producer-side (`create-tasks` L373-378); `implement-feature/SKILL.md` and `templates/commands/implement.md` carry no consumer step; the skill's own Test-runs bullet writes `<spec-dir>/baseline-failed.txt` (root) while 062-style frozen baselines live under `<spec-dir>/notes/baseline-*` — location heterogeneity is real. Pre-flight design: the frozen-baseline set is directory-derived at run time (globs over `<spec-dir>/baseline-*` AND `<spec-dir>/notes/baseline-*`, plus the coverage baseline of D-2) — covering both locations without inventing a new normalization (FR-030 derived set; FR-022's `notes/baseline-*` letter honored). Classification adds `undecidable` to the review's three classes per the requirements' Assumptions; missing file = first-capture with provenance, never zero-drift. `create-tasks` § Re-freeze timing re-points at this consumer step (C-19).

## D-12 — Cross-cutting sync & baselines (FR-026/FR-027/FR-030)

Pre-change drift baselines measured 2026-10-19: `regen-command-copies.py --check` clean (all per-tool copies match); `sync-mirrors.py --check` reports **202 pre-existing DIFF entries** (incl. `shared/workflow/feature-integration.md` and `feedback-step.md`, both in this feature's edit set). Criterion for SC-013/FR-026: **no NEW drift on any pair**; for the pairs this spec touches, the tasks-stage `sync-mirrors.py --write --only <prefix>` lands source→mirror, which clears those pairs' pre-existing drift as a mandated side effect (source is authoritative under the two-hats rule) — pre-existing drift elsewhere is out of scope. Test baseline frozen before any change: 63 failed / 3954 passed (`notes/baseline-failed-tests.txt`, 63 sorted names). `compile-embeds --check` pre-change: 74 units, zero drift. Contract-test anchoring: `test_handler_registry.py` ([C2] closed sets), `test_probe_engine_action_sets.py` ([C4]), `test_neutrality_budget.py` (feature-integration heading, presence-only), `test_clause_forms.py`/`test_clause_coverage.py` — all updated alongside the mechanism they pin (FR-027).

## D-13 — Interview-grade openness check

All plan-level decisions above are mechanism-derivable from the requirements + codebase; none is a user-preference trade-off requiring the interview pattern. The two requirements-level decisions that COULD have forked (E1 idempotency; E2 transition ownership) were settled at clarify and are honored verbatim (C-24, C-15).
