---
id: "introspection-20261106T081504Z"
created: "2026-11-06T08:15:04Z"
status: "confirmed"
scope_filter: "disposition=open --format json (5 entries; framework hat; 0 pending bundles)"
scope_entries: ["20261106T075030Z-speckit-review", "20261106T075035Z-skill-review-sdd-process", "20261106T075040Z-skill-review-feature-quality", "20261106T075045Z-skill-code-review", "20261106T075537Z-skill-sdd-loop-driver"]
supersedes: ""
confirmed_at: "2026-11-06T08:26:39Z"
---

# Introspection Report: introspection-20261106T081504Z

范围：本地库 5 条 open 条目（全部 `kind: internal`；0 个待处理入站包；框架帽子，Path A）。
核验方式：5 条均来自 086 的 review/driver wrap-up，条目内的事实已在本轮运行中被复核（review.md、code-review.md、test-evidence、runner 源码与 line-registry 源码）；按主根因聚类，一条目只归属一个问题。

## Findings

### F-01: Review command claims are prose rules with no engine surface

- **根因**: `/speckit.review` 的 closure 消费、expected-set 分母、receipt 前置与 wrap-up 追踪都只有散文规则，没有可执行入口，执行者只能手工复核并自证。
- **证据锚点**: `templates/commands/review.md` § Segment 2（expected set 由 stage rules + plan 手工推导）、§ 2.4（ARC 记录 copied not recomputed）、§ Wrap-up steps 4/6；`scripts/python/closure-acceptance-check.py` 只读 `verification.md`，仓库中无消费 `--names-out` 对的 action；`skills/internal/code-review/SKILL.md` 要求 receipt，但 review 模板未把 receipt 是否运行作为 transition 前置。
- **成员条目**: 20261106T075030Z-speckit-review(成立)
- **分流决定**: local-sink(speckit-requirements)
- **优化方案**: 以新需求补三个确定性入口——(a) closure-slot 消费/复核 action（读两次 `--names-out` 文件，输出双向差集与耗时，不重跑）；(b) expected-set 分母推导 helper（从 stage rules + plan 生成并打印成员表）；(c) transition 前置读取 code-review receipt 的存在性；wrap-up steps 4/6 各补一条可登记的输出行。
- **建议处置**: 20261106T075030Z-speckit-review:processed

### F-02: Task and status gates measure declarations before evidence exists

- **根因**: tasks/status/budget 三类门只校验声明（carrier 被命名、状态被写入、ledger 有行），不校验被命名文件在声明时是否存在、状态写入是否在 checker verdict 之后、ledger 行是否对应真实运行；"narrowed surface" 无声明字段。
- **证据锚点**: `templates/tasks-template.md` § Mutation Leg Carriers；`scripts/python/validate-tasks.py`（只查 carrier 是否被认领）；`templates/feature-details-template.md` 状态字段无 pre-write 规则；`scripts/python/audit-test-budget.py` 只读 ledger；086 `tasks.md` T037/T054 与 `review.md` F2/F3/F6；`test-evidence/parallel-safety-attribution.md` 的 M-18 leg 证明链条可被判红但无前置门。
- **成员条目**: 20261106T075035Z-skill-review-sdd-process(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 在 tasks 模板增加 `[narrowed: <what> — <why>]` 行词汇并让 validate-tasks 输出所有 narrowed 行；carrier 声明要求文件存在或显式 `[backfilled]` 标记；feature-details 禁止在 checker verdict 前写状态（或要求 `status_basis=<verdict>`）；budget ledger 行增加 run-id/exit-code 自校验；为“repo 内 sandbox worktree”增加前移 guard。
- **建议处置**: 20261106T075035Z-skill-review-sdd-process:processed

### F-03: One pointer string cannot serve both hats, and the guard sees only the source form

- **根因**: STR-003 固定框架源形态 `shared/guidelines/...`，出厂模板使用运行时形态 `.specify/shared/...`；`rewrite_paths` 只重写路径首段，六面 guard 只断言源字符串，因此下游运行时形态漂移不可见。
- **证据锚点**: `templates/constitution-template.md:331`、`templates/instructions-template.md:126`（`.specify/shared/...`）；`requirements.md` STR-003（`shared/guidelines/...`）；`src/specify_cli/__init__.py` `rewrite_paths`（只前缀路径首段）；`shared/guidelines/test-execution-efficiency.md:3`（源形态）；`tests/contract/test_test_execution_efficiency.py`（六面 guard 只查源字符串）；`test-evidence/downstream-init.txt` 未注明 init 消费了哪份模板副本；`review.md` F10/F11/F12。
- **成员条目**: 20261106T075040Z-skill-review-feature-quality(成立)
- **分流决定**: local-sink(speckit-requirements)
- **优化方案**: 统一指针形态的帽子规则（框架源文件用源形态，出厂模板/生成物用运行时形态），据此重钉 STR-003 与 SC-002/SC-003 文本；六面 guard 增加“渲染后形态”断言；init 证据注明消费的模板副本路径；downstream probe 强制写入 repo 外。
- **建议处置**: 20261106T075040Z-skill-review-feature-quality:processed

### F-04: Code-review record cannot distinguish substantive judgement from acknowledgement

- **根因**: `code-review.md` 的 113 行只有 `verdict=reviewed`，无“判断依据”字段；base 的 tier 与 resolved commit 分处两地；framework-hat 的 client capture 以 `none` 呈现而非 `not-applicable`；severity 与 ownership 不齐。
- **证据锚点**: `skills/internal/code-review/SKILL.md` 报告 schema 与 receipt；`.specify/specs/086-efficient-test-execution/code-review.md`（113 行仅 verdict）；`review.md` § 2.1（base tier 与 resolved commit）；§ 2.1 capture 行。
- **成员条目**: 20261106T075045Z-skill-code-review(成立)
- **分流决定**: local-sink(improve-skills)
- **优化方案**: 每文件行增加 `basis`（judged why）字段；记录 base tier 与 resolved commit 于同一行；framework-hat capture 使用 `not-applicable` 闭集值；为 finding 增加 `owning_surface` 字段，使 severity/ownership 对齐。
- **建议处置**: 20261106T075045Z-skill-code-review:processed

### F-05: Environment rules are prose while the fallbacks are silent

- **根因**: worktree 路径、解释器解析、GATE 解释器与 init probe 写入位置由散文约束，失败时静默回退或写入错误位置，导致沙箱污染与不可复现读数。
- **证据锚点**: `skills/external/sdd-loop-driver/scripts/line-registry.py`（worktree 必须在 repo 外）与 085 C-008（`.specify/.tmp/`）不一致；`scripts/bash/run-tests.sh` `resolve_python`（相对 `SPECKIT_PYTHON` 静默回退）；086 `tasks.md` GATE-6 的 `python3 -c "import tomllib"` 在 3.9 上不可运行；`test-evidence/downstream-init.txt` 的 `specify init probe086` 写入 repo 内；`review.md` F12。
- **成员条目**: 20261106T075537Z-skill-sdd-loop-driver(成立)
- **分流决定**: local-sink(direct-fix)
- **优化方案**: 对齐 085 C-008 与 line-registry 的 worktree 根（或更新 C-008 为 repo 外）；`resolve_python` 对显式不可执行的 `SPECKIT_PYTHON` 报具名错误而非回退；GATE-6 改用项目解释器或版本无关 reader；init/mutation probe 一律写入 repo 外并在证据中记录绝对路径。
- **建议处置**: 20261106T075537Z-skill-sdd-loop-driver:processed

## Excluded

无
