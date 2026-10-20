# Analyze Repair-1 — Disposition Record（2026-10-20）

**Scope**: analyze 门回环第 1 轮。输入为 `/tmp/sdd-064/log-064-subagent-concurrency-analyze.log`（0 CRITICAL / 3 HIGH / 25 MEDIUM / 2 LOW）与入口指令指定的直接相关 MEDIUM 清单。本文件记录修复、裁决、证据与延后项；不替代 analyze 报告的只读记录。

## 1. 修复清单

### HIGH

| ID | 修复内容 | 落点 |
|----|----------|------|
| I-02（pre-merge 状态与 U6/集成顺序） | 选定 `completed` 为唯一 pre-merge 状态；补 FR-006 六同步点（U0.5/U2/U3/U4/U5/U6）的唯一状态值；集成结果记录为 `integration_result` 且状态保持 `completed`；U6 在集成结果之后关闭；worktree 仅由 merged 的集成序列移除；`waiting` 晋级以「持线者集成合并并 U6 closed / 显式放弃 / 路径拆分」为条件 | requirements FR-006/FR-021/FR-025/FR-026/FR-057、Assumptions、Edge Cases、Clarifications；data-model E1/V-LR-9/V-LR-10/状态迁移/E7/V-IQ-3/V-IQ-4；contracts/workspace-isolation WI-06/WI-14/Integration Protocol；contracts/lifecycle LC-16；tasks T041 |
| I-04（镜像基数） | 统一为「每线写 Registry；镜像/命令副本由集成者每批一次」；逐线序列删除「更新镜像」 | requirements FR-026、US2 AS4、clarify 记录；data-model V-IQ-4；contracts/workspace-isolation WI-14/Integration Protocol；plan D-15 |
| I-15（租约续期） | 续租周期 MUST ≤ `ttl_seconds/3`（缺省 ≤200s），U2/U3/U4/U5 各续租一次；存活 = 心跳未过期且 PID/token 匹配；PID 活 + token 匹配 + 心跳过期 = `suspected-alive`，不得自动夺取/破除，只允许 `--override` 并留痕 | requirements FR-049；data-model E4/V-DL-2/3/4；contracts/lifecycle LC-05/LC-06/Reattach Sequence；contracts/line-registry `lease-break --override`；tasks T038 |

### 直接相关 MEDIUM

| ID | 修复内容 | 落点 |
|----|----------|------|
| I-08（063 合并守卫与保留边界） | CLP-08 写明输出模式吞吐默认归 063、档案只记录事实；删除 CLP-11/13 对 CP-07/CP-08 的活引用；CLP-17 与 T063 改为仓库级残余扫描；notes 补输出模式 owner 边界 | contracts/cli-profiles CLP-08/11/13/17；notes/063-overlap-adjudication §2.3/§2.7；requirements FR-037、US4 AS3；tasks T063 |
| I-11（T065 `--only`） | T065 拆为两条 scoped `--write --only`，明确禁止无范围 `--write` | tasks T065 |
| I-14（Probe fallback） | 主落点 `skill-wrapup + skill:sdd-loop-driver + wrap-up` 为唯一落点（实测 `probes --validate` 通过）；删除不可执行的 `custom:` fallback | requirements FR-040、Clarifications；contracts/cli-profiles CLP-12；research R10；notes/063-overlap-adjudication §2.3 |
| U-04（运行时集合） | FR-022 声明集合封闭并引用 E8 唯一枚举；E8 新增 Excluded stores 表（evidence/history/trigger）与理由；WI-09 只引用 | requirements FR-022；data-model E8；contracts/workspace-isolation WI-09 |
| G-02（NG-03 测试） | T068 增加 NG-03 守卫（063 裁决表完整、每条迁移条款有 064 承载）；NG 追溯表补 NG-03 具名测试 | contracts/non-regression-and-tests；tasks T068 |
| I-16（覆盖声明与条款正文） | WI-21 补第四项之外的第五项（运行时归档一次 + 镜像/命令副本每批一次）；NG 追溯表逐条化并明确 FR-065 由 LR-08/LC-17 承载；EN-13 补具名测试；feature-ref 补 SC-001/002/006 度量分量 | contracts/workspace-isolation WI-21；contracts/non-regression-and-tests Traceability；contracts/line-envelope-and-ingress Traceability；feature-ref §3/§4；tasks T008 |

### 随 I-02 一并关闭

| ID | 说明 |
|----|------|
| I-03（waiting 晋级的 "holder closed"） | 晋级条件收紧为「持线者完成集成合并并 U6 收尾 / 显式放弃 / 路径拆分」；stale 清理产生的 `closed` 不等于显式释放，仍需 `release-ownership` |

## 2. 裁决记录

- **pre-merge 状态**：`completed`（非 `active + merge_ready`）。理由：`active` 与脊 `running/retrying` 绑定，若允许 `active + done` 会同时破坏 V-LR-9 与「活动线」入口语义（活动线 = active/waiting）；`completed` 已在封闭集中且与脊 `done` 一一对应。完整裁决见 requirements § Clarifications「Session 2026-10-20 — analyze repair-1」与 plan D-15。
- **U6/集成顺序**：集成先行、U6 收尾。merged 时 worktree 由集成序列移除；failed/显式放弃保留。plan D-15 / LC-16 / WI-14 / FR-057。
- **租约节奏**：`ttl/3` 上限 + 阶段推进点续租 + `suspected-alive` 保护。plan D-16。
- **Probe 落点**：单一主落点，不保留 fallback。plan D-10 修订。
- **运行时集合**：E8 为唯一 owner，排除表给理由。plan D-17。

## 3. 延后项（按入口指令留待 implement 或后续 repair 轮）

以下 analyze findings 未在本轮修改，理由为不在「3 HIGH + 直接相关 MEDIUM」范围内，或需要独立裁定/行为测试：

| ID | 严重级 | 延后理由 |
|----|--------|----------|
| I-01 | MEDIUM | `legacy` 分类的多线消费规则需独立裁定（影响 058 兼容边角）；主路径已被 EN-16 限定为未提供参数的兼容调用 |
| I-05 | MEDIUM | LR-13/NG-07 的注册失败 carve-out 属文本修正，未列入本轮直接相关清单 |
| I-06 | MEDIUM | FR-030 与 FR-050 的「先 `--once`」顺序已在 LC-08/V-ID-4 解析；需求正文的措辞收口留待后续 |
| I-07 | MEDIUM | `identity=unknown` 与 stale/stalled 优先级需独立映射表，未列入本轮清单 |
| I-09 | MEDIUM | FR-013 的 cwd/branch 必查与 macOS 豁免需在 Assumptions 记录；未列入本轮清单 |
| I-10 | MEDIUM | 信封载体字段（`at`/`stage`/`event`）补齐属契约文本修正；未列入本轮清单 |
| I-12 | MEDIUM | Provenance `feedback_id` 事后回填、U4 缓冲比对、多事件反馈规则；未列入本轮清单 |
| I-13 | MEDIUM | standalone feedback 例外需 requirements 批准；本轮仅删除了 CLP-11 的 CP-07 引用，异常仍记录在案 |
| U-01 | MEDIUM | E1/E9 字段补齐（`run_history`、`profile_version`、R1 引用、cap usage）；未列入本轮清单 |
| U-02 | LOW | `line_id` slug 归一化定义；留待 implement 的 T004 用例 |
| U-03 | MEDIUM | reservation PID 语义（launcher/runner/cli）；留待 US3 实现时明确 |
| U-05 | MEDIUM | `resources.active_count/cap` 字段与报告时点；未列入本轮清单 |
| G-01 | MEDIUM | FR-012 的 SC 度量缺口；本轮仅在 T008 补了 EN-13 具名断言，SC 级度量留待后续 |
| G-04 | MEDIUM | SC-002/003/005 的测量分母与非 own 事件覆盖；留待后续 |
| G-05 | MEDIUM | SC-009 的 N 值与写-读交错断言；留待后续 |
| G-06 | MEDIUM | SC-004 的比较层级（队列日志/树哈希/提交 SHA）；留待后续 |
| A-01 | MEDIUM | 「安全缺省派发」定义与 061 矩阵合成；留待后续 |
| F-01 | LOW | feature detail 未记录 checklist 阶段、Related Files 未列 checklist；留待 feature 登记维护时处理 |

checklists/concurrency.md 的 24 项 FAIL 保持原样（dated record）；本轮未改写清单判定，由 analyze 重跑重新评估。

## 4. 裁决假设

- 「只读线」沿用 Assumptions 的既有定义（可独立只读视图，不写）；其 `completed` 不置 `merge_ready`，U6 直接关闭，不进入集成队列。
- `integration_result.status=failed` 后不自动重试、不自动关闭；等待显式重试（重新 enqueue）或显式放弃（→ U6）。
- 远端持有者的 lease：PID 证据经远端探针获取；拿不到 PID 证据不构成 `suspected-alive`，按心跳过期与状态脊证据处置（V-DL-2）。

## 5. Validator / 结构证据

- `python3 .specify/scripts/python/validate-requirements.py .specify/specs/064-subagent-concurrency/requirements.md` → exit 0，`scanned: 362 lines, 78 definition rows, 4 shared strings`，0 error / 0 warning。
- `python3 .specify/scripts/python/validate-tasks.py .specify/specs/064-subagent-concurrency/tasks.md` → PASS，0 error / 0 warning。
- `python3 .specify/scripts/python/glossary-utils.py --action validate --root .` → `valid: true`。
- 结构计数：FR 68、SC 10、V-* 59、契约条款 98（LR 13 + EN 16 + WI 21 + LC 18 + CLP 17 + NG 13）、任务 T001–T082 连续且 82 行。
- 未降低判据：本轮未删除任何失败项或条款；checklist 保持 24 FAIL 原记录。

**运行异常：未发现异常。**
