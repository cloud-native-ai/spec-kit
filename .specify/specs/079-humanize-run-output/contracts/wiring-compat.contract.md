# Contract: 接线与兼容（wiring-compat）

**Feature**: 062 扩展 | **规格**: `.specify/specs/079-humanize-run-output/requirements.md`
**性质**: 结构契约。判定命令模板、按工具副本、技能与技能引用、docs 页、Feature 登记、测试与门禁。
**覆盖**: 见文末可追溯性表。
**封闭集**: 「需手改的活接线面」的成员与计数拥有者是 requirements A11，落地清单由 `tasks.md`
实测冻结；本文件断言**性质**（每一项都到位），MUST NOT 复制该清单或计数。

---

## 命令模板

- **WC-01**: `templates/commands/humanize.md` MUST 在入口处声明破坏性变更：裸文本 = 待执行指令；改写既有文本 MUST 用 `[[STR-008]]` 或 `[[STR-009]]`；并给出一条迁移示例（FR-005）。
- **WC-02**: 模板 MUST 保持薄入口：委派节恰好命名一个技能（`.specify/skills/humanize/SKILL.md`），frontmatter 无 `scripts:` 块，正文无 `## Wrap-up`；MUST NOT 复制技能的运行模式 Stage 表或报告五节的细则（033/062 的薄入口不变式继续有效）（FR-026）。
- **WC-03**: 模板 MUST 保留 077 引入的类别接线小节（`## Outline` 内的 owner 指针 + 「命令模板不读取类别、不调用引擎」声明）；该小节的形态由 077 的契约拥有，本特性只要求它**仍逐字满足**该契约（FR-026, FR-027）。
- **WC-04**: 模板 MUST NOT 出现英文短语 `confirmation gate` / `after confirmation` / `Confirm before` / `stop and confirm`，也 MUST NOT 出现「确认门禁」「确认门控」——这些字面量命中门控扫描器的阻断模式；描述既有确认行为时另择措辞（FR-027）。

## 派生面（只再生成，不手改）

- **WC-05**: 四份按工具副本（`.claude/commands/speckit.humanize.md`、`.github/prompts/speckit.humanize.prompt.md`、`.opencode/command/speckit.humanize.md`、`.qoder/commands/speckit.humanize.md`）MUST 由 `scripts/python/regen-command-copies.py` 生成；MUST NOT 手改；`--check` MUST exit 0（FR-026）。
- **WC-06**: 技能源在 `skills/external/humanize/`（`SKILL.md` + `references/`），运行时镜像在 `.specify/skills/humanize/`，由 `scripts/python/sync-mirrors.py --write` 产出；MUST NOT 手改镜像；`--check` MUST exit 0（FR-026）。
- **WC-07**: `skills/external/humanize/SKILL.md` 的正文 MUST 保持 ≤ 5000 tokens（`skills/external/improve-skills/scripts/skill-shape.py` 判定 `pass`）；运行模式的细粒度步骤、载荷字段与报告形态 MUST 落在 `references/`，不塞进正文（Token 效率纪律；基线见 `test-evidence/stage-plan-baselines.txt` § 5）。

## docs

- **WC-08**: `docs/reference/commands/humanize.md` MUST 改写为新定位（跑一条指令 → 五节报告），并保留：旧内容模式的调用方式、迁移示例、默认零写入、不承诺检测器结果的声明、输入按数据处理（FR-026, FR-025）。
- **WC-09**: docs 页 MUST 说明 `--output` 在运行模式写完整报告（含会话回显摘要）、在内容模式只写改写文本（FR-024, FR-026）。

## Feature 登记

- **WC-10**: Feature 062 MUST 保持 `Implemented`；本阶段只在 `.specify/memory/features/062.md` 的 `## Latest Review` 与 `## Key Changes` 追加扩展记录，在 `.specify/memory/features.md` 的 062 行 `Last Updated` 追加扩展标记；MUST NOT 新建 Feature 行、MUST NOT 回退状态（FR-029）。
- **WC-11**: 062 行的名称/描述 MUST 已是「动作输出人类友好化」口径（clarify 阶段已改）；若发现未对齐，同批修正并保持状态不变（FR-029）。

## 测试

- **WC-12**: `tests/contract/test_humanize_command_surface.py` MUST 扩展为本特性的主契约测试：覆盖 IP-01…IP-17、EX-01…EX-21、RP-01…RP-20、CM-01…CM-10、WC-01…WC-15 的可判定部分；MUST NOT 删除既有断言、MUST NOT 以「计数变了」为由放宽断言（FR-028）。
- **WC-13**: `tests/contract/test_stage_class_wiring.py` 的 `UNCHANGED_SHA256["humanize"]` MUST 按新模板重新度量，并在该行注明日期与理由（模板已按 079 改写）；同时 MUST 保留「剥掉接线小节后等于基线」的判定形态（FR-028）。
- **WC-14**: 冻结面测试（`test_expression_gate_wiring.py`、`test_expression_gates_doc.py`、`test_expression_compatibility.py`、`test_flow_class_ledger.py`、`test_flow_class_correctness.py`、`test_feedback_command_classification.py`、`test_migration_distribution.py`、`test_run_skills_wiring.py`、`test_skill_layer_visibility_guards.py`）MUST 逐项核对：本特性只改 `humanize` 条目所指向的制品内容，MUST NOT 改它们的名册/计数；核对为「无需改动且仍绿」时 MUST 在实现证据中记录实测，而不是默默放过（FR-028）。
- **WC-15**: 本特性 MUST 新增行为夹具：运行模式的可确定指令（成功、失败、非动作、需确认、嵌套）、降级与并发场景各一例，落在 `tests/fixtures/humanize/run/`；历史语料（`tests/fixtures/humanize/` 既有文件）MUST NOT 被改写（A11, FR-028）。

## 门禁与运行时

- **WC-16**: MUST NOT 新增 `/speckit.*` 命令；命令名册（27 条模板）不变（FR-027）。
- **WC-17**: MUST NOT 新增阻断式确认门：`git diff 35ff11bc` 在扫描面上的新增行与 `scan-confirmation-gates.py` 的 BLOCKING_PATTERNS 交集 MUST 为 0；判法与基线见 `test-evidence/gate-newline-baseline.txt`（FR-027）。
- **WC-18**: MUST NOT 新增外部服务、网络调用、模型 API、第三方依赖或后台进程；`src/specify_cli/` 与 `scripts/` MUST 零改动（FR-027, 宪法 IX）。
- **WC-19**: 类别与注册面 MUST 保持不变：`/speckit.humanize` 与 `skill:humanize` 在流程台账仍为 `expression / reader-oracle`；probe 注册表无新增行，`probe-utils.py --action compile-embeds --check` MUST 仍为零漂移（A2, WC-14）。
- **WC-20**: 命令的复杂度分类 MUST 仍为 `Simple`（无 `scripts:` 块、无 `## Feedback` 步）；该判定与其理由见 plan § Decision Tensions T-003，MUST NOT 借本特性改写 027 的分类表（FR-027）。

## 可追溯性

| 条款 | FR | 测试（实现期） |
|------|-----|----------------|
| WC-01 | FR-005 | `test_wc01_template_declares_breaking_change` |
| WC-02 | FR-026 | `test_wc02_thin_entry_invariant` |
| WC-03 | FR-026, FR-027 | `test_wc03_wiring_card_preserved`（由 077 断言承载） |
| WC-04 | FR-027 | `test_wc04_no_blocking_literals` |
| WC-05 | FR-026 | `test_wc05_copies_regenerated`（`--check` 由证据承载） |
| WC-06 | FR-026 | `test_wc06_mirror_in_sync`（`sync-mirrors --check` 由证据承载） |
| WC-07 | FR-026 | `test_wc07_skill_body_budget` |
| WC-08 | FR-026, FR-025 | `test_wc08_docs_new_positioning` |
| WC-09 | FR-024, FR-026 | `test_wc09_docs_output_semantics` |
| WC-10 | FR-029 | `test_wc10_feature_062_status_held` |
| WC-11 | FR-029 | `test_wc11_feature_row_name_description` |
| WC-12 | FR-028 | `test_wc12_contract_suite_extended` |
| WC-13 | FR-028 | `test_wc13_stage_class_pin_remeasured` |
| WC-14 | FR-028 | `test_wc14_frozen_surfaces_unchanged` |
| WC-15 | FR-028 | `test_wc15_run_fixtures_present` |
| WC-16 | FR-027 | `test_wc16_command_roster_unchanged` |
| WC-17 | FR-027 | `test_wc17_new_line_gate_zero` |
| WC-18 | FR-027 | `test_wc18_no_runtime_surface_added` |
| WC-19 | A2 | `test_wc19_ledgers_unchanged` |
| WC-20 | FR-027 | `test_wc20_command_stays_simple` |
