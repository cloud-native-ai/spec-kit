# Verification Log — 104-agents-run

baseline_commit=b6907ee53
baseline_date=2026-11-24
baseline_branch=104-agents-run
implementation_date=2026-11-24
post_change_commit=8c39cdec0 (T021–T028 product slice; this file and the package-3 evidence land in the final package commit that follows it)

# -- Smoke test record (exactly one per feature) --

smoke_command=bash scripts/bash/run-tests.sh tests/contract/test_agents_run_command_contract.py -q --names-out .specify/specs/104-agents-run/test-evidence/smoke-failed.txt
smoke_exit_code=0
smoke_evidence_path=.specify/specs/104-agents-run/test-evidence/smoke-run.txt

# -- Evidence records (bind every `pass` claim to archived evidence) --

sample_id=SC-001
evidence_path=.specify/specs/104-agents-run/test-evidence/smoke-run.txt
evidence_sha256=c7d87a3619735b76dd4e4d9cb1d47ad855a536ff78aac3d12defca50f21d83d9
verdict=pass

sample_id=SC-002
evidence_path=.specify/specs/104-agents-run/test-evidence/final-targeted-suite.txt
evidence_sha256=bbde321969624ee35981a7f268c972fb76a23ed4aa65c9d558947d8aa0f3d5af
verdict=pass

sample_id=SC-003
evidence_path=.specify/specs/104-agents-run/test-evidence/guards-reading.txt
evidence_sha256=7035c3431359358d376d6716f4d1581274341ce365ca31f0a505b1b737647189
verdict=pass

sample_id=SC-004
evidence_path=.specify/specs/104-agents-run/test-evidence/us4-green.txt
evidence_sha256=81da82303e28e1b3f620c29e627d2f5093e5560f3ebb41f5e75a00f291188a89
verdict=pass

sample_id=SC-005
evidence_path=.specify/specs/104-agents-run/test-evidence/sc005-audit.txt
evidence_sha256=7a2ff82e4e6946f00698725c0595d6fc5d4664ac9a1e5e7d1ffc3059e76d433f
verdict=pass

sample_id=SC-006
evidence_path=.specify/specs/104-agents-run/test-evidence/mutation-drill.md
evidence_sha256=b4136834451f33e9636e5cdfb6498b324d3da51633a41db7ef52f310734f97dd
verdict=pass

sample_id=SC-007
evidence_path=.specify/specs/104-agents-run/test-evidence/final-targeted-suite.txt
evidence_sha256=bbde321969624ee35981a7f268c972fb76a23ed4aa65c9d558947d8aa0f3d5af
verdict=pass

# -- Success Criteria evaluation --

SC-001_status=pass
SC-001_value=三面语法逐字一致（模板 frontmatter `argument-hint`、skills/internal/run-agent 输入契约、docs Syntax 块均含 [[STR-001]]，C-01/C-06/C-07 绿）；路由样例集 7/7 逐条代理断言（C-08）；三条错误路径（[[STR-002]] / [[STR-003]] / [[STR-004]]）各自停止且零派发（C-10）。smoke：command-contract 模块 10 passed，rc 0，零失败名。
SC-001_note=命令：`bash scripts/bash/run-tests.sh tests/contract/test_agents_run_command_contract.py -q --names-out .specify/specs/104-agents-run/test-evidence/smoke-failed.txt`（rc=0）；证据：test-evidence/smoke-run.txt；全量定向读数见 test-evidence/final-targeted-suite.txt（216 passed）

SC-002_status=pass
SC-002_value=同父 + 双 label 夹具上只读 role-edge-check.py 报告 2 条子代边、深度 1、零违例；label 压成同一个时报告只剩 1 条边（红形演示）；重试即新 label 且旧 triplet 原样保留；迟到返回按 watch-model.md § 11 归因、不被当作当前结果。模块 4/4 绿，收口批次中亦绿。
SC-002_note=命令：`bash scripts/bash/run-tests.sh tests/contract/test_agents_run_multi_child_edges.py -q`（4 passed，读数见 notes/red-first-evidence.md § T010/T012）；收口批次：test-evidence/final-targeted-suite.txt

SC-003_status=pass
SC-003_value=派发面接线契约在位：技能文本含呈现三要素（superagent/root、child label、return channel）、七字段下行、四项注入、五要素上行、label 唯一性、SDD 探针适用条件、快速失败注入与反嵌套红线（C-11…C-22 全绿，模块 17 passed）；每一项都是具名 presence 断言，删除即令对应函数转红——删项敏感性由 SC-006 演练 M3（删七字段指针 → C-12 红）实证，其余函数为同形断言；四支既有守卫相对入口基线零新增名字级失败（3 条既有红逐条点名：fast_fail g9/i10/x22）。
SC-003_note=命令：`bash scripts/bash/run-tests.sh tests/contract/test_agents_run_skill_wiring.py -q`（17 passed，test-evidence/us5-green.txt）；守卫读数 test-evidence/guards-reading.txt（3 failed 全为基线成员，comm -13 为空）

SC-004_status=pass
SC-004_value=文档同源成立：`docs/reference/commands/agents.md` 的 `^# /speckit.agents` 计数 = 1（改前 3）；run 语法与 run 意图行在位；C-34 封闭谓词表（STR-005 / STR-006 / bold 变体 / STR-007 / STR-008 / ci generate role-based agents / ci generate project-aware role agents / ci generate seven / no-arguments+generate 行）在七个命名文件中的实时出现数全为 0；command-and-skills 为三能力且含按指针的 run-agent 小节；overview / design / 教程命令表行含 run；docs 契约 12/12 绿 + command 契约 C-06 绿（22 passed 同一批次）。
SC-004_note=命令：`bash scripts/bash/run-tests.sh tests/contract/test_agents_run_docs_contract.py tests/contract/test_agents_run_command_contract.py -q`（22 passed，rc 0，test-evidence/us4-green.txt）；计数读数见 notes/red-first-evidence.md § T021–T023

SC-005_status=pass
SC-005_value=变更集包含性成立：base `b6907ee53` 到 `8c39cdec0` 的比较单元（五类产品面根）内 19 条路径全部落在允许闭包，补集为空；结构审计零新增持久化根 / registry / 渲染器 / 调度器 / 队列（产品面根下新增文件仅五个声明测试模块）；scripts/src/shared/glossary 零改动；flow-class 92 单元 0 发现；scope 模块 9/9 绿；镜像与源逐字节一致（sync-mirrors --check exit 0）。
SC-005_note=命令与真实输出：test-evidence/sc005-audit.txt；scope 复跑 `bash scripts/bash/run-tests.sh tests/contract/test_agents_run_scope_contract.py -q`（9 passed，test-evidence/scope-green.txt）

SC-006_status=pass
SC-006_value=变异演练 4/4：① 删 `argument-hint` → C-01 红（2 failed），复原后 10 passed；② 删模板 run 意图行 → C-02 红（3 failed，含 C-08/C-09 同因），复原后 10 passed；③ 删七字段下行指针 → C-12 红（1 failed），复原后 17 passed；④ 复制第二份命令参考正文 → C-23 红（1 failed），复原后 12 passed。每项复原按精确反向替换 + 恢复字面量计数 = 1 + `git diff` 为空确认。
SC-006_note=证据：test-evidence/mutation-drill.md（红/绿读数逐项记录；M1 的 cp 交互别名事故已在演练记录中披露并修复）

SC-007_status=pass
SC-007_value=九模块定向集经唯一入口一次执行：216 passed / 3 failed，3 条失败全为 implement 入口基线成员（test_fast_fail_discipline g9 / i10 / x22，逐条点名），`comm -13 baseline current` 为空（零新增名字级失败）；同阶段 account-clause-coverage.py exit 0（claimed clauses 35、FR 24/24、uncovered beyond baseline 0；唯一告警为语料级既有 `clause-unparsable (108)`）。
SC-007_note=命令：`bash scripts/bash/run-tests.sh <九个模块> --names-out .specify/specs/104-agents-run/test-evidence/final-failed.txt`；证据：test-evidence/final-targeted-suite.txt、test-evidence/final-failed.txt、baseline-failed.txt（222 names）；覆盖读数见 notes/red-first-evidence.md § T032

# -- Joint acceptance (one row per `in-scope` runtime-stack row in requirements.md) --

RS-008_joint_acceptance=pass
RS-008_note=本特性自身修改的派发编排面：技能文本的语法 / 呈现 / 载荷 / 回传 / label / 边界指针全部在位（skill-wiring 17 passed），删项时对应检查转红（M3 实证 C-12；其余为同形 presence 断言）；镜像源与投影逐字节一致。

# -- Deferred tasks (mirrors `[~]` rows in tasks.md) --

deferred_tasks=
deferred_reason_summary=

# -- Gate bookkeeping --

gate_rejections_consecutive=0

# -- Free-form notes --

notes=本次收口包（T021–T033）无 plan-owned 面改动，零 PLAN-EDIT 声明。E3 stage-status 行写入 test-evidence/implement.jsonl；测试预算沿用 spine seq=1 的 implement 入口全量基线（rc=1 / 222 failed 名单），本包只跑定向集。P1 记录的镜像与 role-transition 两处 planned transient 已随 T028 再生成消解（guards-reading.txt 中 comm -13 为空）。既有脏文件（coaching-skills 两处、smoke-081.txt）与上游未跟踪证据文件未纳入本包任何提交。Feature 019 状态维持 Implemented（本阶段无状态迁移权）。closure 判定调用：`python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/104-agents-run --repo . --feature-detail .specify/features/019-agents-command.md` → verdict accept（final_path pass=2 / total=2），读数 test-evidence/closure-acceptance.txt。GATE-2 的 18 条 advisory 逐条裁定：17 条 external-clause 为 data-model INV-01…INV-12 与 plan/tasks 对它们的引用——INV 是 data-model 的不变量命名空间而非契约条款，advisory 系命名空间误报，接受不改；1 条 missing-path（plan.md `.specify/templates/commands/`）为 plan 源树引用的框架源路径形态差异，交付面以 `templates/commands/` 为准且该 plan 面本阶段无改动权，记录为 advisory-accepted。GATE-1 的 1 条 green-cross-phase 警告为 tasks.md 生成时已裁定的 C-06/C-10 单调序例外（tasks.md § Format 第 52 行记录）。