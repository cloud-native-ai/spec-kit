# Quickstart: 证据基础设施(spec 034 / Feature 038)

> 演练路径按实施后状态编写;CLI 示例以 `contracts/evidence-utils-cli.md` 为准,实施时须执行验证(plan 质量门)。

## 1. 能力探测(doctor)

```bash
python3 .specify/scripts/python/evidence-utils.py --action doctor
```

预期:JSON 输出 Node 版本与 satisfies 判定、引擎子集存在性(含 upstreamCommit b2e621d)、八工具本地会话落盘探测、五泳道可用性。Node 缺失 → session/project/assets 标 unavailable,runs/feedback 仍 available。

## 2. 全泳道采集(collect)

```bash
python3 .specify/scripts/python/evidence-utils.py --action collect \
  --target skill:improve-skills --lanes all --platform qoder
```

预期:产出 `.specify/memory/evidence/ev-<date>-<time>-improve-skills/{findings.json,manifest.json,lanes/}`;stdout 报 runId、各泳道状态、evidenceCount、findingsDigest。验证要点:findings 无裁决字段(C-F6)、evidenceState 全落七态(C-F4)、feedback 泳道 entries 数与 `.specify/memory/feedback/index.json` 动态一致。

## 3. 复用与对比(latest / compare)

```bash
python3 .specify/scripts/python/evidence-utils.py --action latest --target skill:improve-skills
python3 .specify/scripts/python/evidence-utils.py --action compare --target skill:improve-skills
```

latest 超 7 天报 stale 警告;compare 输出 signalDeltas,基线目录含 intervention.json 时给出 Outcome-supported / Unobserved 判定并写回。

## 4. 技能编排(collect-evidence)

对话中调用 collect-evidence 技能 → 范围解析 → doctor 能力表 → collect → 按 evidenceState 分布摘要 + 边界申明(Unobserved 项与不可用泳道)。红线验证:输出零优化建议/严重度表述。

## 5. improve 消费闭环(evidence-step)

以 improve-skills 为例:Step A 采集(或 latest 复用)→ Step B 按 evidenceState 分拣并冻结候选(Unobserved 只记录)→ 自有根因/修改流程 → 写 intervention.json → 下轮 compare 验证。SC-006/007 验收即走此路径。

## 6. 降级演练(无 Node)

```bash
PATH=/usr/bin-no-node python3 .specify/scripts/python/evidence-utils.py --action collect --target project --lanes all
```

预期:三条 Node 泳道 unavailable(manifest 附 reason),runs/feedback 正常产出,退出码 0,零崩溃零编造(SC-003)。

## 7. 引擎子集回归(tests/js)

```bash
bash tests/js/run.sh          # node --test;Node 缺失时 skip 退出 0
pytest -m contract -k evidence  # findings 合同 + CLI 表面 + evidence-step 合规
```
