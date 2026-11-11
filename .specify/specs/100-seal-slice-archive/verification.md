# Verification Log — 100-seal-slice-archive

baseline_commit=f821daf8362a3050cb14909a820294f70f04d8a9
baseline_date=2026-11-11
baseline_branch=100-seal-slice-archive
implementation_date=2026-11-11
post_change_commit=f3bd72866 (P7b 收口；P8 的证据与闭包包由承载本文件的提交落盘)

# -- Smoke test record (exactly one per feature) --

smoke_command=bash scripts/bash/run-tests.sh tests/contract/test_seal_archive_plan.py tests/contract/test_seal_archive_manifest.py tests/contract/test_seal_archive_apply.py tests/integration/test_seal_archive_idempotency.py tests/integration/test_seal_archive_round.py -q
smoke_exit_code=0
smoke_evidence_path=.specify/specs/100-seal-slice-archive/test-evidence/us1-checkpoint.txt

# -- Joint acceptance (one row per `in-scope` runtime-stack row in requirements.md) --

RS-004_joint_acceptance=pass
RS-004_note=既有 seal 引擎与 non-disposable 处置 owner 就地扩展：动作集六值、写面数据表、C-111/C-113 边界审计全绿；未新建第二引擎或第二处置词表（test-evidence/structure-audit.txt、test-evidence/us4-checkpoint.txt）

# -- Per-SC status rows --

SC-001_status=pass
SC-001_value=074 真实验收成立：074a/074b 位于 .specify/specs/074-goal-team-sdd-unification/slices/ 下；归档前后 58/54 文件、逐文件 sha256 与相对路径集合相等；git diff --name-status -M HEAD 在移动路径集上 112 条 R、零 D；archive-manifest.json（744,331 B）存在且经引擎复核；注册状态与封装结论不变
SC-001_note=test-evidence/074-archive-round.txt（T042–T044 读数 + P7b 收敛记录）；test-evidence/us1-checkpoint.txt（52 passed）；notes/quickstart-run.md § S-2a

SC-002_status=pass
SC-002_value=零丢失与幂等成立：两次 apply 的重跑得到 already-archived 且相对重跑前零新增 diff（提交后 git diff --stat 零输出）；重跑 plan 零待移动、零未解析；内容变异由零丢失哈希检查捕获并按原字节恢复
SC-002_note=test-evidence/074-archive-round.txt（T044 重跑读数）；test-evidence/us1-checkpoint.txt；notes/quickstart-run.md § S-4

SC-003_status=pass
SC-003_value=引用完整性 fail closed：reference-matrix 上 live-rewrite=16、dated-preserved=14、unclassified=0、未解析 0/0；日期化载体字节不变且经清单 from→to 映射解析；注入悬空活引用或移除一条映射时检查转红
SC-003_note=test-evidence/us2-checkpoint.txt（四项计数 + 63 passed）；tests/contract/test_seal_archive_plan.py 的两个注入用例

SC-004_status=pass
SC-004_value=流程集成成立：封装阻断的 blocked-pair 夹具在 merge-apply 后的归档照常执行，归档前后 seal 阻断清单逐条一致（按 slices/ 前缀规范化后 4 = 4）；merge-apply 被拒绝的夹具不启动归档（merge-manifest-missing，exit 2，零持久化）；退出码封闭 0/1/2；COMMAND_BASELINE=31 不变
SC-004_note=test-evidence/us3-checkpoint.txt（53 passed）；notes/quickstart-run.md § S-5；tests/integration/test_seal_archive_round.py

SC-005_status=pass
SC-005_value=边界不越权：归档前后注册表行仅引文路径列变化、详情时间线字节相等（18,251 字符）、features.md 无 diff、父 spec seal.md 缺席态不变、合并结论/计数/冲突/retention 不变；引擎写面以数据表封闭，注入删除、注册表状态写入或 git push 时审计转红
SC-005_note=test-evidence/us4-checkpoint.txt（状态面快照 + 48 passed）；tests/contract/test_seal_boundaries.py::test_injected_push_delete_or_registry_write_turns_the_audit_red

SC-006_status=pass
SC-006_value=确定性成立：同输入两次 archive-plan 逐字节一致；成功 apply 重跑零 diff；排序键只取声明字段；反转目录枚举顺序时候选清单逐字节不变；清单无墙钟/环境字段（按返回时刻排序的变异会使确定性断言转红）
SC-006_note=test-evidence/us1-checkpoint.txt；tests/integration/test_seal_archive_idempotency.py（two_plans / sort_keys / reversed_enumeration / no_wallclock）

SC-007_status=pass
SC-007_value=清单完整性与闭环算术成立：三组算术两侧相等（扫描命中 = live+dated；runtime-updated + absent = 被声明载体数；移动行 = files 行）；删除台账一行或 checks 一行时检查转红；未知/缺失字段在读取侧 exit 2
SC-007_note=test-evidence/us1-checkpoint.txt；tests/contract/test_seal_archive_manifest.py（SC-007 删行变异 + 键集封闭）

SC-008_status=pass
SC-008_value=运行期 line registry 处置有效：present 载体记 runtime-updated 且改写行与归档路径一致；absent 载体记 absent + 非空 reason、零更新、不阻断（2 更新 + 1 缺席与 3 缺席两种环境算术均成立）
SC-008_note=test-evidence/us2-checkpoint.txt（runtime_carriers=3 算术）；tests/contract/test_seal_archive_apply.py::test_runtime_carriers_are_updated_and_absence_does_not_block

SC-009_status=pass
SC-009_value=单一机制与并发安全成立：仓库无本特性新增的第二套处置词表/第二归档引擎/第二份按 spec 清单/派生索引；两个夹具 spec 并行归档写入不同父 spec 下的不同清单路径且无锁文件；复制清单为共享聚合或建立缓存/第二映射表时审计转红
SC-009_note=test-evidence/structure-audit.txt；test-evidence/us4-checkpoint.txt；tests/contract/test_seal_boundaries.py（C-111 / C-312 组）

SC-010_status=pass
SC-010_value=回滚可执行：按 C-110 / quickstart S-6 配方逐字执行后 git diff --exit-code <pinned> 为空、工作树干净；省略 move / restore / runtime / manifest 任一步骤时完成判据转红
SC-010_note=test-evidence/074-archive-round.txt（rollback drill）；notes/quickstart-run.md § S-6；tests/integration/test_seal_archive_rollback.py

# -- Deferred tasks --

deferred_tasks=
deferred_reason_summary=
