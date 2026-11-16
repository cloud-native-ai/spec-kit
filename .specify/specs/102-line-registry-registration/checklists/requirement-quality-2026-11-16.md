# Requirements Quality Checklist: 长任务 line 登记与 status 可见性（Line Registry Registration）

**Purpose**: 以「需求写作的单元测试」检验 `requirements.md` 的定义、量化、边界、可判定性与引用方向；不检验实现行为。
**Created**: 2026-11-16
**Feature (Requirement Scope)**: Feature 088「Speckit 框架可视化」— slice 行 102（`.specify/features/088-speckit-visualization.md`）
**Requirements (What)**: [requirements.md](../requirements.md)
**Specifications (How, context only)**: [plan.md](../plan.md) · [tasks.md](../tasks.md)（仅用于发现需求缺口，不作为被评对象）
**Depth**: Standard · **Audience**: Reviewer · **Focus**: 判据所有权与载体生命周期 · 扫描器的牙齿与单一 owner · 四个接线面的指针方向

**Note**: 本清单是这一轮新生成的文件；`checklists/requirements.md`（requirements 阶段产物）不被覆盖。每项在行尾给出本轮处置：`pass`（原文已满足）、`in-round fixed`（本轮做最小文内修正，见 § Round Notes）、`open`（本阶段未修平，随回传上报）。

## Requirement Completeness

- [ ] CHK001 Is the long-task obligation stated once in full — register at start, heartbeat at stage boundaries, close at end — together with the consequence of not registering? [Completeness, Req §FR-001]
- [ ] CHK002 Is the judgment owner of the 5-minute threshold named, so the criterion can be applied without inventing one? [Completeness, Req §FR-001, A-1] — in-round fixed（阈值判定者 = 运行者，启动时按预期时长）
- [ ] CHK003 Is the mechanical projection enumerated as a closed set with exactly one machine-readable owner, and does the owner-skip rule name how it is reported? [Completeness, Req §FR-002, A-15] — pass
- [ ] CHK004 Are all four delivery surfaces named with bounded duties, so no surface silently carries a second copy? [Completeness, Req §Overview 3, FR-017…FR-019] — pass
- [ ] CHK005 Is the evidence obligation written with a named recorder and a named location for both the live reading and the execution record? [Completeness, Req §FR-016, FR-021] — in-round fixed（记录者 = 测试经唯一入口；扫描器保持只读）
- [ ] CHK006 Is the obligation to ship automated tests for the wrapper's five lifecycle forms stated at requirement level rather than only implied by a success criterion? [Gap, Req §FR-021, SC-004] — in-round fixed（FR-021 增补五形态与扫描器三例的自动测试义务）
- [ ] CHK007 Does the scanner's runtime row cite every functional requirement whose capability it supplies? [Completeness, Req §Runtime Stack RS-001] — in-round fixed（FR-013/014/016 补入 RS-001 的 FR 列）

## Requirement Clarity

- [ ] CHK008 Is "空根" defined (zero entries vs zero judged files) and given an exit consequence distinct from a clean reading? [Clarity, Req §FR-013, A-21] — in-round fixed（空根 = 零个被判定文件；退出 2 并具名该根）
- [ ] CHK009 Is the header marker's role stated as a criterion hit rather than a compliance exemption, consistent with the compliance forms? [Ambiguity, Req §FR-014, Edge Cases] — in-round fixed
- [ ] CHK010 Is the wrapper invocation form stated as mandatory (`--` plus command) in agreement with its usage-error rule? [Clarity, Req §A-4] — in-round fixed
- [ ] CHK011 Is "运行期间" given a sampling rule, so the digest reading it asserts is reproducible? [Measurability, Req §US1 Independent Test, SC-001] — in-round fixed（命令须保持运行到采样完成）
- [ ] CHK012 Is a shell compatibility floor stated (or explicitly delegated) where the runtime table declares the shell contract? [Clarity, Req §RS-002] — in-round fixed（bash 3.2 及以上）
- [ ] CHK013 Is the `line_id` literal distinguished from the composed id value that the run report must carry? [Clarity, Req §STR-007, A-18, FR-017] — pass（STR-007 是字段名；A-18 的「值」指该字段的合成值，两者不冲突）
- [ ] CHK014 Is the placement of threshold/boundary text inside the owner document unambiguous? [Clarity, Req §FR-001, contracts C-01/C-03] — pass（tasks T028 把断言面钉在 § 九；既有 `## 判定边界` 仍是该文档的通则小节）

## Requirement Consistency

- [ ] CHK015 Does the wrapper's engine-event obligation agree with the adjudicated two-event rule and the contract's prohibition of intermediate events? [Consistency, Req §FR-009, A-19] — in-round fixed（删除永不可达的条件句；阶段 heartbeat 归 run-team）
- [ ] CHK016 Do the compliance-path statements agree across the criterion set, the compliance clause and the edge-case bullet? [Consistency, Req §FR-002, FR-014, Edge Cases] — in-round fixed（合规途径只有一条；标记只宣布不豁免）
- [ ] CHK017 Does the distribution-consistency criterion agree with the measured mirror baseline and the plan's no-new-drift rule? [Consistency, Req §SC-006, plan §Mirror Obligations] — in-round fixed（改为「相对基线无新增漂移」）
- [ ] CHK018 Is the identity-failure classification consistent between the fail-closed rule and the contract's dedicated exit code? [Consistency, Req §FR-006, A-17, A-18] — pass（需求只要求非零并可具名；契约把它窄化为 4，不构成矛盾）
- [ ] CHK019 Do the four wiring surfaces agree on one owner path and one carrier path? [Consistency, Req §FR-017…FR-019, contracts C-15] — pass
- [ ] CHK020 Is the digest's closed-line hiding compatible with the visibility criterion's observation route? [Consistency, Req §SC-001, FR-020, Clarifications] — pass

## Measurability & Acceptance Criteria

- [ ] CHK021 Is the mutation clause of the scanner criterion falsifiable for every constant it names? [Measurability, Req §SC-002] — in-round fixed（改为删除合规形态成员 / 使自声明不被识别时转红）
- [ ] CHK022 Does the comprehension criterion carry a binary pass rule and an executor? [Measurability, Req §SC-008] — in-round fixed（一名基准读者、两句都对照 pass/fail、不可执行记 not-evaluated）
- [ ] CHK023 Does every success criterion name a runnable measurement source, including who decides conditional applicability? [Measurability, Req §SC-006, Measurement Sources] — in-round fixed（适用性判定者 = 实现者，依据写进读数）
- [ ] CHK024 Does each acceptance scenario use a command shape able to observe the state it asserts? [Measurability, Req §US1 scenarios] — in-round fixed（`-- true` 改为保持运行的命令）
- [ ] CHK025 Are the five lifecycle outcomes (success / child failure / registration failure / double failure / SIGKILL residue) each stated with an observable result? [Completeness, Req §FR-004, FR-006…FR-008, A-24, SC-004] — pass
- [ ] CHK026 Are the `Path` markers used per their machine rule (last token, exactly once) on every criterion line? [Traceability, Req §SC-001…SC-009] — pass（validate-requirements `path-marker pass`）

## Coverage & Edge Cases

- [ ] CHK027 Are residue semantics defined for the run-team line as well as the wrapper line? [Coverage, Req §FR-017, A-10] — pass（引擎默认保留 active；本特性不增清理）
- [ ] CHK028 Is the wrapper's own signal behaviour bounded (catchable vs uncatchable), rather than only SIGKILL residue being stated? [Edge Case, Req §FR-008, Edge Cases] — pass（捕获即关闭、不可捕获即残留，两分支已写明）
- [ ] CHK029 Are scanner false-positive paths addressed (comments, documentation-only mentions, a runner that merely offers the long-task option)? [Coverage, Req §Edge Cases, A-21] — in-round fixed（误报小节措辞与合规语义对齐）
- [ ] CHK030 Are re-entry and concurrency outcomes defined without overwriting an existing entry? [Coverage, Req §A-9, A-18, Edge Cases] — pass
- [ ] CHK031 Is the boundary of observability (child hands off work and returns) stated and bounded? [Coverage, Req §A-13] — pass

## Dependencies & Assumptions

- [ ] CHK032 Is every load-bearing assumption (engine validates ids/reasons; refusal is surfaced; no wrapper-side grammar) testable from the text? [Assumption, Req §A-18, FR-004] — pass
- [ ] CHK033 Is the dependency on generators and the no-hand-edited-mirror rule stated per artifact, including the per-tool command copies? [Dependency, Req §FR-003, plan §Mirror Obligations] — pass
- [ ] CHK034 Are environment preconditions (git repo, writable registry, test entry) declared as premises rather than assumed? [Dependency, Req §RS-001…RS-006, plan §EP-001…EP-005] — pass

## Traceability & References

- [ ] CHK035 Do all referenced sections and paths resolve to targets that carry the claimed content? [Traceability, Req §FR-001, FR-017…FR-019, Edge Cases] — pass（§ 九 / § 十一、模板常驻小节、run-team §5–§7 均逐条核验）
- [ ] CHK036 Does every shared string carry consumers and match the literal its downstream surface uses? [Traceability, Req §Shared Strings] — pass（STR-007 的字段名/合成值分工见 CHK013）
- [ ] CHK037 Is the scope criterion's baseline referent and allowed-delta set mechanically derivable? [Traceability, Req §SC-009, feature-ref] — pass（分叉基线 = `git merge-base master HEAD` → cdc79cdb5；delta = feature-ref 的 24 路径清单；tasks T050 占位符已替换）

## Open Items

- [ ] CHK038 Is the scanner's "repository root" referent defined — how the default roots and `--root` values are resolved, and from which base (repo root vs invocation cwd)? [Ambiguity, Req §FR-013, data-model §E4] — open（本阶段不臆造解析规则；建议实现前由 plan 以 minor 补一句解析基准，或由驱动裁决豁免）

## Round Notes

- **清单类型**: 需求质量（UNIT TESTS FOR REQUIREMENTS WRITING）。所有条目问的是「文本是否写清/写全/可判定」，不运行产品。
- **同作者条件与检测分工**: `requirements.md` / `plan.md` / `tasks.md` 由同族代理的前序阶段运行产出（非本会话），按 `shared/workflow/objective-analysis-gate.md` 的同作者判据仍按委派执行：两路 fresh-context 只读检测器按不相交作用域分派（A = requirements 内部；B = plan/contracts/data-model/tasks 交叉），共 22 条候选；3 条经直接核验后驳回（Path 分类法 owner 在 `acceptance-hardening.md`；SC-009 的交付清单在 `feature-ref.md`；N-1 的条款计 11/9/5 属实），其余并入上述条目。
- **验证方式**: 检测后的验证为直接核验（逐条对照被引原文 + 机械探针），未再派第二组验证者；按 gate §5 记为「direct read validation」，不作为独立验证波。
- **本轮文内修正（最小必要）**: `requirements.md` 16 处（FR-001 / FR-009 / FR-013 / FR-014 / FR-015 / FR-016 / FR-021 / A-4 / Edge Cases 误报条 / US1 抽样说明 / US1 场景 1 / SC-002 / SC-006 / SC-008 / RS-001 的 FR 列 / RS-002 的 Pin 单元格）；`tasks.md` 7 处（T007 抽样窗口、T019 自声明与空根用例、T027 常量删除注入、T045 注入面扩到 status 与常驻 bullet 并引 SC-005、T048 引 SC-007、T050 基线占位符、环境前提复测行）。语义边界未改：FR/SC/STR 编号与数量不变（23 FR / 9 SC / 9 shared strings）。
- **plan-owned 工件**: 本轮未编辑任何 plan-owned 文件，PLAN-EDIT 计数 0。
- **门禁读数（修正后）**: `validate-requirements.py` `status: ok`（0 error / 0 warning；257 lines / 32 definition rows / 9 shared strings）；`validate-tasks.py` PASS（0 error / 0 warning）；`pre-analyze-check.py --stage tasks` `decision=pass`（errors=0 / advisories=62 / fr=23 / sc=9 / tasks=57）。
