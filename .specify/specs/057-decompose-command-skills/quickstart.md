# Quickstart: 057-decompose-command-skills

三个场景覆盖 US1/US2/US3 的主旅程。**执行-验证状态逐例标注**:标注「已执行」的命令在本规划期实跑(浓缩结果见 plan.md § Technical Context Constraints 与下表);标注「实现后验证」的命令依赖本特性产物,按 premises 清单在 /speckit.implement 重测——每个未执行示例的 premises 逐一列明,不许文件级免责。

## 场景 A — run-skills 运行未注册技能(US1,实现后验证)

用户对一个宿主未发现的技能(例:新草稿技能 `my-draft`)直接调用 run-skills:

```text
run-skills my-draft
```

- **Premises(实现期重测)**:①调用语法 `run-skills <名称|路径>` 由契约 C-3 钉住;②解析顺序 = data-model § Skill Location Search Order(canonical 优先,已裁定);③`my-draft` 位于某已知位置集内且带合法 SKILL.md;④零命中时输出逐项列出 4 个已搜索位置(FR-004)。
- **预期**:解析披露所选路径 → 加载并按其 SKILL.md 正文执行 → 转述该技能产出;若目标已被宿主发现,附「可能可直接斜杠调用」非阻断提示(FR-007 尽力检测)。
- **边界**:越界显式路径 / SKILL.md 无效 / 非 Spec-Kit 部署下 internal 目标 → 快速失败并给可行动错误(FR-004/FR-008)。

## 场景 B — /speckit.team run 经 run-team(US2,实现后验证)

命令面调用不变,行为平价:

```text
/speckit.team run <slug>
```

- **Premises**:①路由行 run → [[STR-002]](C-4);②P-1…P-10 义务逐条 equal 或更严(对映真源 contracts/run-team-parity.md);③五查预检仍由 `goal-utils.py run-checks` 唯一判定(P-2,退出码语义不变)。
- **预期**:预检通过 → 目标重述 → 双结构渲染 → present & execute → 运行报告落 `runs/`(含 Target 指派字段);对照变更前同 slug 的运行输出,义务面无差异。
- **平价对照法**:实现期对同一团队(或最小 fixture 团队)各跑一次变更前/后 run,比对报告结构字段与 Target 指派行形态。

## 场景 C — /speckit.skills 路由全族(US3,实现后验证)

```text
/speckit.skills run my-draft      # run 意图 → run-skills([[STR-001]])
/speckit.skills merge <a> <b>     # merge 意图 → merge-skills(既有)
/speckit.skills think <name>      # 思想演练意图 → think-skills(既有)
```

- **Premises**:①路由表 5 行形态由 C-3 钉住;②merge/think 两意图词形以既有技能描述中的触发词为准(实现期以 grep 核对技能描述,不发明新词);③run 行 runtime path 实存(C-1)。
- **预期**:三个意图各自路由到既有技能且不内联实现(goal T-003)。

## 规划期已实跑的基线命令(证据见 plan.md § Technical Context)

| 命令 | 已执行结果(2026-10-14) |
|------|------------------------|
| `python3 scripts/python/sync-mirrors.py --check` | EXIT=2,恰 1 条既有 DIFF(`.specify/skills/git-workspace/scripts/git_fleet.py`) |
| `python3 scripts/python/regen-command-copies.py --check` | OK:全部 per-tool 副本与源一致 |
| `python3 .specify/scripts/python/scan-confirmation-gates.py` | total 23(16 destructive + 7 governance_kept),violations 0 |
| `python3 scripts/python/probe-utils.py --action compile-embeds --check` | 69 单元零漂移 |

实现收尾重跑同一组命令,判据 = 相对基线无新增(镜像恰仍那 1 条;门控 total 仍 23;probe 71 单元零漂移;regen 仍全 OK)。
