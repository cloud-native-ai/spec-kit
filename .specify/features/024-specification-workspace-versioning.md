# Feature Detail: Specification Workspace Versioning

**Feature ID**: 024  
**Name**: Specification Workspace Versioning  
**Description**: Version management and migration support for .specify/ workspace structure across CLI releases.  
**Status**: Ready for Review  
**Created**: 2026-06-05  
**Last Updated**: 2026-11-25（plan：slice 105 runtime-store layout 产出 plan/design 工件并推进 `Draft → Planned`；父状态保持 `Ready for Review`；tasks：slice 105 产出 43 行任务清单（27 FR / 9 SC；`validate-tasks.py` 0 error / 0 warning；FR universe 27），状态维持 `Planned`；implement：slice 105 完成 43/43 任务、closure `accept`（final_path 6/6）、`Planned → Implemented`，父状态保持 `Ready for Review`；review：slice 105 四段评审 + ARC 完成，code record `not-evaluated` / 0 `blocking` / gate `allow`，slice 行 `Implemented → Ready for Review` landed，父状态保持 `Ready for Review`）

## Overview

The `.specify/` workspace is the runtime home for all generated artifacts — instructions, memory, skills, scripts, specs, and templates. As the CLI evolves, workspace structure changes (new directories, renamed files, moved content) can break existing projects. This feature covers introducing a workspace version marker and migration tooling so projects can safely upgrade across CLI releases without manual intervention.

## Latest Review

Gap identified during project-intrinsic analysis. The CLI version is tracked in `pyproject.toml` but the workspace structure has no independent version. Changes like the skills layout migration (007-skill-install-layout) were handled ad-hoc with backup guardrails rather than through a versioned migration system.

2026-11-10 (plan, `/speckit.migrate` 097): the version-marker premise was superseded by a declaration-driven design — the expected state is projected from the currently installed CLI's assets and declarations, so no `.specify/version` marker and no version→migration registry are needed. Bound sub-spec: `.specify/specs/097-speckit-migrate-command/` (requirements → plan: 3 contracts, 9 entities, 14 work packages).

2026-11-10 (review, `/speckit.review` 097): four segments + Acceptance Reality Check complete — process report `.specify/specs/097-speckit-migrate-command/review.md`, code record `code-review.md` (123 changed / 97 judged / 26 generated-skipped / 0 gap; 1 `blocking`). `Implemented → Ready for Review` **refused — `blocking-unresolved`**: the current code-segment record carries a blocking entry (unfailable zero-write test, `tests/integration/test_migrate_us2_safety.py:273`) and the feature still claims `Planned` (the `Planned → Implemented` flip was never landed although the checker returns `accept` with `final_path` pass 4/4), so the transition has no matching From-state. Status left unchanged; no waiver presented. ARC record: pass 4 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 4.

2026-11-10 (review-repair r1, 097): the blocking defect and the eight P1 findings were repaired. The zero-write probe test is now an observable guard (sentinel transient directory + workspace chdir, plus a fifth red-ability mutation; two-variant red-base drill in `test-evidence/red-base-probe-guard-2026-11-10.txt`); the smoke record was re-executed verbatim (105 passed, `final-suite.txt`); C-1/docs/template converged to `--help`; the receipt `workspace` key landed (C-4/E-2/E-3); SC-002/SC-007/DoD-4 wording, quickstart status and tasks DoD status refreshed. `closure-acceptance-check.py` on the repaired tree: verdict `accept`, reasons none, `final_path` pass 4/4, all four `Planned → Implemented` conditions true → **`Planned → Implemented` landed** (registry row and this detail agree). `Implemented → Ready for Review` remains pending a re-run of `/speckit.review` against this tree.

2026-11-11 (review r2, `/speckit.review` 097): full re-run of the four segments + Acceptance Reality Check against `da34a3d44`; every round-1 P0/P1 repair anchor re-verified (status flip, zero-write probe guard with both red variants, smoke literal byte-identical to the executed command, SC-007 pointer, `--help`/-h convergence, receipt `workspace` key). Segment conclusions: process **P1×3 / P2×4** (framework-level recommendations, no P0), artifact **pass** (9/9, A1–A9 closed), implementation **pass** (smoke 105 passed / exit 0 / `final-suite.txt`), code record **`not-evaluated`** with 0 `blocking` / 0 `important` / 6 `suggestion` / 1 `nitpick` / 1 `praise` (147 changed / 107 judged / 40 generated-skipped / 0 gap; gate `allow`). ARC: claim `Implemented`, verdict `accept`, `final_path` pass 4 / blocked 0 / deferred 0 / partial 0 / fail 0 / unknown 0 / total 4. `Implemented → Ready for Review` **landed** (all four conjunctive conditions hold; no waiver). Process report `review.md`, archived round-1 records `review-097-speckit-migrate-command.md` and `code-review-20261110T161419Z.md`.

2026-11-25 (plan, 105): second sub-spec planned — runtime stores leave `.specify/memory/` for top-level `.specify/<store>/` roots and the container is retired. Design: one new `store-layout` dimension appended to `specify migrate` (five 097 tokens kept as the ordered prefix; 097's dated E-8 not rewritten), per-store manifest-first relocation with digest/from→to recovery, dual-content refusal through the clarified authoritative-entry predicate, receipt v2, and a single machine declaration (`runtime-store-layout.yaml`) replacing seven per-consumer root lists. Artifacts: `.specify/specs/105-runtime-store-layout/` — 4 contracts, 10 entities, 15 work packages, 9 quickstart scenarios (scenarios 0–8; the earlier "8" was corrected in `fa2de626a`); six Decision Tensions recorded in its `plan.md` (dimension extension, seed rename, SC-007 baseline reading, docs dated boundary, manifest-as-archive, declaration ownership).

2026-11-25 (tasks, 105): dependency-ordered task list landed at `.specify/specs/105-runtime-store-layout/tasks.md` — 43 rows across Setup / Foundational / US1–US6 / Polish, all 15 planned WPs mapped, FR coverage map 27/27 and SC map 9/9, test-first obligations with the named red-first landing point. Deterministic readings: `validate-tasks.py` 0 error / 0 warning, `pre-analyze-check.py --stage tasks` decision=pass errors=0, `account-clause-coverage.py` claimed clauses 8 and clause-uncovered beyond baseline 0 (its FR lane reads 6/27 because the M/P/L contracts are `form=md-none`; FR universe 27, FR ownership is proven by the task-row map and the pre-analyze check). No new Feature, no deprecation, no status transition: slice 105 stays `Planned`, parent stays `Ready for Review`.

2026-11-25 (implement, `/speckit.implement` 105): slice 105 implemented — 42 crew writebacks + spec-side T039, all 43 rows `[X]`; `verification.md` SC-001…SC-009 pass (final-path 6/6), one smoke triple exit 0; `closure-acceptance-check.py` verdict `accept`. Full fast tier vs the 748-name entry baseline: NEW=0 / repaired=531 (217 named pre-existing reds remain); mirrors `sync-mirrors --check` rc 0 / zero drift and `regen-command-copies --check` rc 0; dogfood migrated 12 stores and removed `.specify/memory`; bounded P5R closes the crash→resume→third-apply idempotence gap read-only. `Planned → Implemented` landed; parent stays `Ready for Review`. Review pending.

2026-11-25 (review, `/speckit.review` 105): four segments + Acceptance Reality Check complete against `f261f6bac` — process report `.specify/specs/105-runtime-store-layout/review.md` (process: P0×0 / P1×1 / P2×6; artifact: 9/9 expected members, P0×1 + P2×2 — the P0 is T017's red-first claim without a red run, validated by direct re-read because the review assignment forbids subagent dispatch; implementation: `pass`, smoke re-run exit 0); code record `code-review.md` (4342 changed / 262 judged / 4080 generated-or-non-code skipped / 0 gap; verdict `not-evaluated` with 0 `blocking` / 1 `important` answered in the record / 1 `suggestion` / 1 `praise`; gate `allow`; archive `none`). ARC: claim `Implemented`, verdict `accept`, `final_path` pass 6 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 6 → `agree`; no failed condition, no fixed item. `Implemented → Ready for Review` **landed** (all four conjunctive conditions hold; no waiver): deferred tasks none, both review records on disk, current code record has no `blocking` entry, every `final`-path criterion `pass`. Parent status stays `Ready for Review`; no new Feature, no deprecation.

## Key Changes

1. `specify migrate` CLI 子命令：默认零写入干跑，`--apply` 进入写入模式；四类结局 `clean` / `planned` / `applied` / `blocked` 配稳定退出码（0/1/0/3，输入错误 2）。
2. 期望态 = 当前已安装版本的声明与资产：五维只读探测（模板与生成物、锚点布局、兼容链接、镜像一致性、迁移残留）复用 init 迁移分支、`sanitize-utils.py` 检查器与 `anchor-layout-migrate.py`，不按源版本号选择路径。
3. `/speckit.migrate` 运行期模板：同一 CLI 引擎的薄投影，不复制任何检查或处置逻辑。
4. 处置安全：六值封闭集（FR-014 of 097）；移动/替换/合并/移除一律 archive-first，逐运行回执落 `.specify/memory/migrate/receipts/`；`--apply` 是唯一写入授权，可归档恢复的处置按可逆动作自动执行；旧新锚点冲突由引擎合并并保留双方，只有不可合并的结构性冲突才 `refuse` / `blocked`。
5. 跨版本一次直达 N→N+k：无中间版本步骤；失败语义为前向续跑 + 逐项归档找回（不提供全局回滚）。
6. 取代 024 早期设想的 `.specify/version` 标记、版本→迁移注册表与 `specify upgrade` 命令（097 requirements FR-005/FR-020 记录裁定）。

## Implementation Notes

- 工作区双形态：框架源工作区（`skills/external/` 存在）把镜像/生成副本维度委托 `sync-mirrors.py --check` 与 `regen-command-copies.py --check`；客户端工作区用 init 投影得到的临时参照树对照（097 plan T-002）。
- 客户端期望态是 init 投影形态（`rewrite_paths` 后），与仓库自身的 sync-mirrors 字节形态不同——不得用单一比较语义（097 research R-3）。
- 迁移必须幂等（apply 后重跑为 clean 且零写入）；中断后可凭 `status=running` 回执续做，已归档对象不二次搬移。
- 不依赖网络（资产来自已安装包）与 git（非 git 目录/detached HEAD 可用）。
- 用户自建技能、项目专属扩展、`site/` 运行时数据永不入选残留清单；手改框架文件替换前先归档。
- goal/team 档案迁移仍归 `/speckit.goal` 的 `migrate-archive`，本能力只输出静止指针。
- `/speckit.sanitize` 保持周期性治理；其 Migration wrap-up lane 改为「周期复检兜底」定位。

## Future Evolution Suggestions

- Support workspace "profiles" for different team configurations.
- ~~Add dry-run mode for migrations to preview changes before applying.~~ Delivered as the default mode in the 097 plan (`specify migrate` is zero-write by default).
- Consider workspace health checks as part of `/speckit.checklist`.

## Related Files

- Feature Index: .specify/features.md
- Feature Detail: .specify/features/024-specification-workspace-versioning.md

### Related Specifications

- `.specify/specs/097-speckit-migrate-command/requirements.md` — 本 Feature 的首个子规格（slice 行 097，`Ready for Review`）：声明驱动的一次性工作区收敛（plan → apply → archive-first → 回执）。
- `.specify/specs/105-runtime-store-layout/requirements.md` — 第二个子规格（slice 行 105，`Planned`；2026-11-25 `/speckit.plan`）：把 session/knowledge/feedback/evidence 等运行期存储迁出 `.specify/memory/` 到顶层存储根，并复用本 Feature 的 `specify migrate` 迁移/拒绝面（新增 `store-layout` 维度）；父行状态保持 `Ready for Review`，不回退。
- Cross-referenced Feature: .specify/memory/features/045.md (Framework Source Provenance, Draft 2026-08-17) — the source/provenance axis, orthogonal to this schema-version axis; its stamp must NOT take this Feature's envisioned `.specify/version` marker path.

## Status Tracking

- **Draft**: Gap identified; no workspace versioning exists.
- **Planned**: One-shot migration design planned — the expected state is projected from the currently installed CLI's assets and declarations (the `.specify/version` marker and version→migration registry premise was superseded; see Latest Review 2026-11-10).
- **Implemented**: `specify migrate` functional — zero-write dry-run plan, confirmation-gated apply with archive-not-delete and per-run receipts; 097's final-path criteria pass and its smoke record is green.
- **Blocked**: Tasks closed and at least one `final`-path criterion is not `pass`.
- **Ready for Review**: Migration tests pass; existing workspaces upgradable.
- **Completed**: Workspace versioning is the standard upgrade path across CLI releases.
