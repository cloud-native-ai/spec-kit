# Verification Log — 041-refactor-feedback-probe

# -- Baseline (recorded once, BEFORE any /speckit.implement work changes the tree) --
baseline_commit=3634815f (pre-run HEAD; T001 suite ran before any engine edit)
baseline_date=2026-08-14
baseline_branch=041-refactor-feedback-probe
baseline_failed_tests=38 (name list: baseline-failed.txt)
baseline_embed_points=49 (18 command templates + 31 skills, embed-inventory.txt)
baseline_probe_objects=0
baseline_legacy_entries=140
baseline_engine_actions=7 (record/status/list/mark-submitted/reindex/package/upstream)

# -- /speckit.implement results --
implementation_date=2026-08-14
post_change_commit=fa9a70a8..(final polish commit)
post_change_failed_tests=38 (zero new vs baseline; comm -13 empty at every phase boundary + final)
post_change_embed_points=50 (19 + 31; feedback.md 自身第 50 点)
post_change_probe_objects=50 internal + external via inject
post_change_legacy_entries=0 (migrated, migration-log.md 140 rows)
post_change_engine_actions=13 (+dispose/cleanup/probes/map/migrate-legacy/probe-inject)
post_change_new_contract_tests=27 (registry 14 + cli 13[map5+filter/dispose5+cleanup3... 见测试文件] + entry-schema 6 + command-template 6 — 按文件计 4 文件 42 用例全绿)

# -- Success Criteria --
SC-001_status=pass
SC-001_value=49/49 既有双向零缺漏 + 第 50 点同变更登记;reconcile exit 0 (50 objects ↔ 50 embeds)
SC-001_note=证据 verification-scratch/sc-001.txt(probes --validate/--reconcile 实跑输出 + live grep 18+31→19+31)
SC-002_status=pass
SC-002_value=record 自动解析 probe/kind/slice;fixture 断言 frontmatter/index 双写;legacy(无注册表)回退不产生无归属新条目于已升级工作区
SC-002_note=tests/contract/test_feedback_probe_entry_schema.py 6 用例;engine-cli C-1.1 strict-when-registry 语义
SC-003_status=pass
SC-003_value=probe-map.md 双重建逐字节一致(diff 空);受控修改差异仅限对应条目(测试断言覆盖=真源)
SC-003_note=证据 verification-scratch/sc-003.txt(55 mermaid 节点=1+2+3+49,明细 49 行,零对象类标注)
SC-004_status=pass
SC-004_value=--slice 一步过滤,结果不含其它切片(单切片命中)
SC-004_note=test_list_filter_by_slice + 手动 QA sc-007-mode12.txt(filter commands count=1)
SC-005_status=pass
SC-005_value=140 条全部处置(140 delete/0 re-register);legacy_remaining=0;计数重算为 0 不触发提示
SC-005_note=用户确认处置计划 2026-08-14(134 已随上送包处置 + 6 会话条目已落入提交);证据 sc-005.txt + migration-log.md 140 行
SC-006_status=pass
SC-006_value=网络传输 0 次——引擎 stdlib 仅用 zipfile/json 无网络模块;全部动作本地文件操作
SC-006_note=代码路径审计:feedback-utils.py 无 import socket/urllib/http;package 产物本地 zip;QA 全程零网络
SC-007_status=pass
SC-007_value=模式一无参数 50↔50 一致;模式二全闭环(清理后活跃库 0,包内留档 1,log 留痕);模式三注入闭环(定义落源+可区分条目)
SC-007_note=证据 sc-007-mode12.txt + sc-008.txt(T021/T030 scratch 项目实跑);模式三证据同 sc-008(inject→ext 条目)
SC-008_status=pass
SC-008_value=上送包内容流式断言 kind:"external" 出现 0 次;MANIFEST 无 external 行;excluded_external=1;--kind external 单独过滤命中
SC-008_note=证据 sc-008.txt;GATE-6 同口径(unzip -p 内容流 + MANIFEST 核查)

# -- Notes --
notes=实施期事实修正:工具副本面实测 4(.claude/.github/.qoder/.opencode;codex/hermes 由 specify init 下游分发)→ plan/contracts/tasks 已同步修正。事故与恢复:T021 首跑漏 --workspace-root 致引擎自定位锚定真实库(package+cleanup 误触)→ git restore 完整恢复,重跑显式传参通过——证实 resolve_workspace_root 自定位优先级高于 CWD,QA 脚本必须显式传参。既有边界:now_iso 秒级精度使与 mark-submitted 同秒记录的条目落 pending 窗口外(既有语义,测试跨秒处理)。ENGINE_ACTIONS 钉死随人口扩展逐相位更新(Pin Hygiene 规则 3)。
deferred_tasks=none
