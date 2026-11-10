# Analyze Repair Dispositions r3 — 097-speckit-migrate-command

**Stage**: analyze 修复轮 r3（analyze 门 round-2 的 3 条 HIGH 经独立验证波 confirm 后自主修复；无人值守规则：修复后直接续跑 analyze）· **Date**: 2026-11-10
**Input**: `test-evidence/analyze-merged-round2-2026-11-10.md` §0.2/§2 + `test-evidence/analyze-validation-round2-2026-11-10.md`（confirm 3 / downgrade 0 / reject 0）
**Authority**: 本特性 spec 全目录 + `.specify/constitution.md`（L223 载体 `verification.log`）+ `.specify/skills/internal/analyze-artifacts/SKILL.md`
**Method**: 逐条重读 finding 锚点与 owner（tasks.md DoD-1/DoD-3/pkg07/T013/T048、宪法 VII、`.gitignore` L37 `*.log`、`git check-ignore` 实测、contracts/migrate-engine.md C-5 守卫表），先判 confirm/reject 再做最小修复；每条修复以实测读数复核。
**Summary**: `confirm=4, reject=0`；`fixed=4`（W3-18 为 W3-16 指令内嵌核查项，按独立 finding ID 单列，不静默合并）。

| ID | 原严重度 | 复核裁定 | 处置 | 文件:行（修复后锚点） | 一句话理由 |
|----|----------|----------|------|------------------------|------------|
| W3-09 | HIGH | confirm | fixed | `tasks.md:35`（DoD-3）、`tasks.md:154`（T013） | 原句「任一复制实现被移除时转红」方向与 no-second-engine 相反（违例是新增第二实现）且 Check 只跑套件无法验证变异主张；改为可执行等价断言——五类守卫（补齐 C-5 的 obsolete roster，共五类）以 callable 作用于源文本并钉住非空 migrate 段，每类附测试内注入变异（合成第二实现必须被判违例，漏检即套件转红），Check 保持同一套件命令、变异与 clean 断言同次运行，读数随 T046 的 `test-evidence/final-suite.txt` 留档。 |
| W3-15 | HIGH | confirm | fixed | `tasks.md:33`（DoD-1） | 原红判据「删除任一任务行的 FR 引用必须使计数 <25」机械不成立（23/25 个 FR 由 ≥2 行点名）；改为按 FR 判定——删除任一 FR 的**全部**行内引用后该 FR 必须从去重集合消失、计数降为 24，并保留 2026-11-10 实测读数（单点 FR-004@T016、FR-008@T015 删除后 =24；FR-001 双引用须两处全删才 =24，单删一处 =25 属预期不判红）。 |
| W3-16 | HIGH | confirm | fixed | `tasks.md:113`（pkg07 写域） | `verification.md` 全文件仅存于 pkg07 写域一处，与 T048/DoD-7/GATE-4/宪法 VII 的 `verification.log` 冲突；pkg07 写域改为 `verification.log` 后 `grep -c 'verification\.md' tasks.md` = 0，同一事实全部副本闭合。 |
| W3-18 | MEDIUM | confirm | fixed | `.gitignore:38-39`（负规则）、`tasks.md:264`（T048） | `git check-ignore -v` 实测确认根 `.gitignore` L37 `*.log` 吞掉 `verification.log`（`.specify/.gitignore` 无 `*.log`，根规则为唯一来源）；根 `.gitignore` 增窄负规则 `!.specify/specs/*/verification.log`（仅放行宪法 VII 闭包载体），T048 行文本写入「载体 MUST 受版本控制 + `git check-ignore -q` MUST exit 1」的验收命令；实测负规则生效后 `git check-ignore -q` exit=1（不再忽略）。 |

## 复核证据（2026-11-10 实测）

- DoD-1：任务行 48、FR 去重 25；`sed '175s/FR-004//'` → 24、`sed '171s/FR-008//'` → 24、FR-001 双删（L170+L175）→ 24、FR-001 单删 → 25（预期，不判红）。完整读数见 `analyze-repair-gates-r3-2026-11-10.txt` EXTRA 段。
- W3-18：修复前 `git check-ignore -v` 命中 `.gitignore:37:*.log`；修复后命中 `.gitignore:39:!.specify/specs/*/verification.log`，`git check-ignore -q` exit=1。
- W3-16：`grep -c 'verification\.md' tasks.md` = 0（spec 目录内其余命中仅为 test-evidence 历史记录）。
- W3-09：T013 行为实测含五类守卫 token（no second path-rewrite regex / command renderer / link roster / mirror-pair roster / obsolete roster）。

## 门禁复跑（全绿）

validate-requirements 0 error/0 warning；pre-analyze stage=requirements/plan/tasks 均 decision=pass（0 error）；decomposition mode=tasks decision=proceed（fr_count 25 / task_count 48）；validate-tasks 0 error/0 warning。完整读数：`analyze-repair-gates-r3-2026-11-10.txt`。

## 边界与残差（不静默丢弃）

- 本轮只处置 3 条 HIGH 及其内嵌的 W3-18；round-2 其余 open MEDIUM/LOW（W3-04…W3-14、W3-17、W3-19 与 W1/W2 各条）保持 deferred，不在 C/H 修复轮范围。
- 机制侧残差不变（accepted upstream observation）：`templates/tasks-template.md`、`shared/workflow/acceptance-hardening.md`、`shared/workflow/feature-integration.md` 仍用 `verification.md`；`.specify/.gitignore` 为框架安装模板，本修复未触及，根 `.gitignore` 负规则是本仓（client 帽）修复。
- 本轮未运行测试套件：Tasks Mode ON 的测试行尚未实现（`tests/contract/test_migrate_engine_contract.py` 不存在），测试内注入变异断言属实现阶段义务；本轮保证其可执行形态与 Check 命令一致。
