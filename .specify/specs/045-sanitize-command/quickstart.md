# Quickstart: /speckit.sanitize 走查(需求 045 / Feature 047)

三个端到端走查,对应 US1/US3/US2。引擎 CLI 示例的 flags/arg 语法由 `tests/contract/test_sanitize_engine_contract.py` 钉死(实现期执行前以契约为准,防止文档漂移)。

## 走查 1:检查模式——真实过期残留检出(US1,SC-001)

前提:本仓 `.specify/memory/todo/20260812-evidence-session-backlog.md` 存在(声明五项未落地,实际已由 1a090c72 合入)。

```bash
# 1) 确定性检查 + 语义候选采集(写入仅落台账)
python3 scripts/python/sanitize-utils.py --action collect --workspace-root . --format json
# → semanticCandidates 含该 parked todo,claims 含"未落地"声明,
#   evidencePack.gitLog 含 1a090c72 提交行

# 2) agent 对证据包判定后并入台账(判定文件由命令流程产出)
python3 scripts/python/sanitize-utils.py --action record --file /tmp/sanitize-verdicts.json --workspace-root . --format json
# → 台账新增 stale-residue 发现:evidenceRefs 引用 1a090c72,state=pending

# 3) 台账摘要(零写入)
python3 scripts/python/sanitize-utils.py --action status --workspace-root . --format json
```

预期:该 todo 以 pending 状态入账,携带 commit 级证据引用;被检材料本体零变更(快照可验)。用户此时选择不清理——发现保留待后续处理。

## 走查 2:确认后清理——前置门控 + 状态更新 + 执行报告(US3,SC-003)

承接走查 1 的 pending 发现。

```bash
# 1) 命令流程归并清理计划(confirmed 初始为 false)
#    /speckit.sanitize 呈现计划 → 用户确认 → confirmed 置 true

# 2) 未确认直接 apply 被拒
python3 scripts/python/sanitize-utils.py --action apply --plan .specify/memory/sanitize/cleanup-plan.json --workspace-root . --format json
# → 退出码 2 {"error": "plan not confirmed"};零删除零移动

# 3) 确认后执行
python3 scripts/python/sanitize-utils.py --action apply --plan .specify/memory/sanitize/cleanup-plan.json --workspace-root . --format json
# → executed: [{findingId, disposition: "delete", outcome: "ok"}]
#   artifacts: [{change: "deleted", path: ".specify/memory/todo/20260812-...md"}]
#   状态 pending → resolved;执行报告三要素呈现
```

预期:确认前删除/移动数为 0;确认后该过期 todo 被删除、发现状态 resolved、执行报告含修改途径。

## 走查 3:正确性检查——四类确定性发现与移交分诊(US2,SC-004)

前提:夹具仓库 `tests/fixtures/sanitize/`(死引用材料、features 索引缺项、断链符号链接、未注册孤儿镜像目录、已注册孤儿镜像目录)。

```bash
python3 scripts/python/sanitize-utils.py --action collect --workspace-root tests/fixtures/sanitize/sample --format json
```

预期:

- dead-reference:材料引用的 `scripts/python/不存在.py`、`speckit.不存在` 命令、缺失技能目录各成发现;围栏代码块内的路径不计;
- index-inconsistency:features.md 行指向缺失文件、磁盘 `features/099.md` 无索引行,双向各一条;
- broken-symlink:`CLAUDE.md` 断链一条,处置 delegate(/speckit.instructions),不执行修复;
- mirror-drift:未注册孤儿镜像目录 severity=high(处置 delete),已注册者 severity=medium;
- 上述结论全部来自确定性程序输出,`detection=programmatic`;无任何 LLM 判定参与(SC-004)。

## 验收对照

| SC | 走查 |
|----|------|
| SC-001 | 走查 1 |
| SC-002 | 走查 1(快照比对) |
| SC-003 | 走查 2 |
| SC-004 | 走查 3 |
| SC-005 | 走查 1(证据不足候选计数,不入账)+ 证据引用抽检 |
