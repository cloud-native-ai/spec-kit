# U5 上送件 — 097-speckit-migrate-command（analyze 二轮未清 HIGH）

**时间**: 2026-11-10T09:00Z · **线**: `097-speckit-migrate-command` · **run**: `r20261110T081104Z-b097`
**判定**: analyze 门一轮修复回环已用尽；第二轮 3 条 HIGH 经独立只读验证 **3/3 confirm**（W3-09 升格、W3-15 新增、W3-16 新增）→ 按规则停线（不可豁免）。

## 1. 发现了什么

| ID | 一句话（均经 fresh-context 验证确认） |
|----|--------------------------------------|
| W3-09 | DoD-3 的「移除变异断言」与其 Check（只跑套件取退出 0、无变异执行）不相交；T013 守卫清单为「无第二份 X」缺席断言，与 no-second-engine 的违反方向相反；按 closed-set-claims 判「不可测验收标准」HIGH 升格成立 |
| W3-15 | DoD-1「删除任一任务行的 FR 引用必须使计数 < 25」机械不成立：23/25 个 FR 由 ≥2 行点名，删多行后计数仍 25；仅单点 FR-004/FR-008 才降到 24 |
| W3-16 | pkg07 写域写 `verification.md`，而 T048/DoD-7/GATE-4/宪法 VII 的闭包载体是 `verification.log`——同一事实两个名字，执行者按写域无权写真正载体 |

完整事实与复测读数：`test-evidence/analyze-merged-round2-2026-11-10.md` §0.2/§2、`test-evidence/analyze-validation-round2-2026-11-10.md`。
另：round-1 的 11 条 C/H 已全部 fixed 并复核确认。

## 2. 为何吃重

- 三条均为**判据级**问题（可测性、计数逻辑、载体命名），修复会触发 DoD/GATE/tasks 三处同步改写与判据重定义；按门禁规则第二轮仍 C/H 不得豁免。
- 与 095 同期停线：两条线的停因同属「门禁判据 vs 文本字面」的系统性摩擦（详见各线框架观察），建议合并成一次框架级反馈处置。

## 3. 已产生的中间产物

- 分支：`097-speckit-migrate-command`；工作树：`.specify/.tmp/sdd-loop/worktrees/097-speckit-migrate-command`
- 规格全链：requirements / plan / tasks / checklists / contracts(migrate-cli|engine|template) / data-model / quickstart
- analyze 证据：`test-evidence/analyze-findings-W{1,2,3}.md`、`analyze-merged-2026-11-10.md`、`analyze-repair-dispositions-2026-11-10.md`、`analyze-repair-gates-2026-11-10.txt`、`analyze-findings-round2-W{1,2,3}.md`、`analyze-merged-round2-2026-11-10.md`、`analyze-validation-round2-2026-11-10.md`
- 状态脊：`.specify/state/097-speckit-migrate-command.md`（stalled）；registry `state=blocked`

## 4. 可选处置

- **A**：人工裁定三条（DoD-3 改为可执行变异读法 / DoD-1 计数判据改为单点 FR 或计数口径 / pkg07 写域改 `verification.log`），聚焦修复后**授权重开 analyze 门一次**。
- **B**：停在 Blocked，优先推进 096/098。
- **C**：把 097 的交付缩到「命令 + 引擎 + 模板」三契约本体，DoD 判据问题随框架级反馈统一处置。

## 5. 用户裁定（访谈 D-097，2026-11-10）

- **按建议修复**：处置 3 条已验证 HIGH（DoD-3 变异断言可测化 / DoD-1 计数判据 / pkg07 载体命名），随后重开 analyze 门一次。
