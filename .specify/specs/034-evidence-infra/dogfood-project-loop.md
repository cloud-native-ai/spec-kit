# Dogfood 自我优化闭环记录(project 级,2026-07-29)

按 dogfooding 理念对 spec-kit 自身运行证据机制(evidence-step A→B→C/D→E→compare)。

## Step A 采集

- 基线运行:`ev-20260729-093344-project`(五泳道:session Unobserved / project+assets Present / runs partial+Exercised / feedback available)。

## Step B 分拣(候选冻结)

| 证据 | 状态 | 分拣 |
|------|------|------|
| ev-004 assets "3 lint finding(s)" | Present(负向异常) | **缺陷候选** ——直接查看引擎原始 envelope 发现实为 16 条:evidence-utils.py 的 assets 泳道把上游 findings 信封字典 `{items,total,omitted}` 当列表数,`len(dict)` 恒等于 3,掩蔽了 13 条真实发现 |
| ev-001 session Unobserved | Unobserved | 只记录(红线:不当缺陷修) |
| ev-005/006 runs | Exercised | 中性团队执行记录,无负向信号,不取 |
| ev-002/003 project | Present | 仓库事实,无候选 |
| ev-007 feedback (60 条, 0 重复主题) | Present | 只记录(计数不产生发现) |

候选冻结:唯一缺陷候选 = **assets 泳道 lintFindings 计数缺陷**(证据层自身缺陷,dogfood 的理想标的)。

## Step C/D 定向修改(最小变更)

- `evidence-utils.py` `collect_assets_lane`:findings 为 dict 时取 `items` 长度,为 list 时取列表长度;双镜像同步。
- 回归钉点:`TestAssetsLintCount`(tests/contract/test_evidence_utils_cli.py)。

## Step E 台账 + compare 判定

- `intervention.json` 写入基线运行目录(targetFinding=ev-004, expectedSignal=lintFindings improve)。
- 第二轮采集 `ev-20260729-093755-project` → compare:lintFindings **3 → 16**,判定 **Outcome-supported**(由 compare 写回台账)。

## 冻结外记录项(不在本轮修,留待人工/后续)

1. **上游 lint 的 `${SKILL_HOME}` 误报**:16 条中 4 条 cli-setup "missing local reference" 指向的文件实际存在——上游 linter 不认识 spec-kit 的 `${SKILL_HOME}` 路径约定。属引擎适配缺口(可回馈上游或本地修改,须记 UPSTREAM.md),非资产缺陷。
2. **`.specify/skills/draw-echarts/yuque-workspace/` 镜像单侧内容**(7 月 16 日入库,源侧无):按"调查先于删除"纪律列为待人工决策,不自动清理。
3. 长技能建议(create-team 685 行 / document-utils 1492 行等):advisory 级,交由各技能 improve 流程按证据处理。

## 回归

- evidence 合同测试 35/35 通过;全套失败集相对基线零新增(见提交)。
