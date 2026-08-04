# Quickstart: Team Summary 信息管理机制

**Requirement → Feature**: `036-team-summary` → Feature 027 Team Management
**Audience**: 实现者与验收者。本文件的每条命令要么已在 Phase 0 对真实团队执行过,要么标注为待实现接口并由契约测试钉住。

## 1. 认识输入面(可立即执行)

被调技能的唯一输入是表单。先看空白模板,理解团队侧要填什么:

```bash
python3 skills/summarize-project/scripts/validate-project-input.py --blank-form | head -20
```

R 档只有三条:`project.project_name`、`project.baseline_date`,以及 `work_items` 与 `milestones` **至少一组非空**。团队侧的映射目标就是让这三条恒定成立。

## 2. 手工复现 Phase 0 的可行性验证(已执行,可重跑)

在实现生成器之前,可以用手写表单证明"团队工件足以满足 R 档"。下列四步在 `cws-workspace-cluster` 上实测通过:

```bash
S=skills/summarize-project/scripts
D=/tmp/tsv                      # 任意临时交付目录
mkdir -p $D/data
# 手工按团队 tracked 工件填 $D/data/project-input.yaml
#   project_name  ← team.md frontmatter name
#   baseline_date ← 本次 cycle 时间戳(yyyy-mm-dd)
#   work_items    ← STATE.md 被跟踪条目;source 指向 STATE.md 锚点
#   milestones    ← goal 中的可验证成功判据;source 指向 team.md#goal
#   people        ← members[] 的 role/slug

python3 $S/validate-project-input.py --input $D/data/project-input.yaml --json | head -20
python3 $S/project-db.py --db $D/data/project.db --load $D/data/project-input.yaml
python3 $S/project-db.py --db $D/data/project.db --check
python3 $S/progress-engine.py --db $D/data/project.db > $D/data/engine-out.json
```

**预期**:四步退出码全为 `0`;校验输出 `status: ready` 且 `missing_required: []`;装载报告 `完整性体检:ok`。

**若把某个 `item_id` 写成含空格或中文的字符串**,装载会以退出码 `3` 拒绝并打印:

```
约束违规（数据库拒绝写入）：work_items(item_id='…')：… 不是合法标识 ——
DDL 约束 entity_ids.entity_id 只允许字母/数字/`_`/`-`/`.`，且以字母或数字开头。
```

这条实测结论决定了 ID 文法:显式 `TI-<nnnn>`、推断 `TIX-<8hex>`,中文标题必须先哈希。

## 3. 观察引擎已经替你兜住的降级

```bash
python3 -c "
import json; d=json.load(open('/tmp/tsv/data/engine-out.json'))
print('progress_pct :', d['project']['progress']['progress_pct'])
print('reason       :', d['project']['progress']['reason'])
print('gantt bars   :', d['gantt']['bar_count'])
print('has_planned  :', d['gantt']['schedule_material']['has_planned_dates'])
print('coverage     :', d['coverage'])
"
```

**预期**:`progress_pct` 为 `None`(不是 0)并附 `reason`;`bar_count` 为 0、`has_planned_dates` 为 `False`(无排期材料时甘特不出图);`coverage` 为 `None`。

最后一项是**必须处理的**:`coverage` 为空时,一旦报告含功能分解图就会在落盘门禁 CG-COVERAGE 上 FAIL。因此生成器必须恒定产出 `coverage` 块。

## 4. 待实现接口(由契约测试钉住)

```bash
# 由本规格新增;接口定义见 contracts/team-project-form.contract.md
python3 skills/create-team/scripts/build-summary-input.py --goal <goal-slug> --json
python3 skills/create-team/scripts/build-summary-input.py --team <team-slug> --json   # 解析其 goal 后聚合该 goal 全部团队
```

退出码约定:`0` 已产出表单;`3` 该 goal 下无任何执行材料(对应状态行 `declined(no-material)`);`2` 输入错误。

**聚合层的 ID 前缀是硬要求(实测)**:N 个团队的台账装载进同一个 `project.db`,而 `entity_ids` 是全局 ID 命名空间。两个团队各自的 `TI-0001` 同时入库会被拒:

```
约束违规（数据库拒绝写入）：work_items(item_id='TI-0001')：item_id='TI-0001' 在本实体内重复
  —— DDL 约束 PRIMARY KEY（同一实体不得两行同号）。
```

加团队命名空间前缀(`team-a.TI-0001`)后实测装载通过。故生成器折叠时必须加前缀,而团队台账内部仍写不带前缀的 ID。

## 5. 验收路径(对应 Success Criteria)

| 验收 | 做法 | 判据 |
|------|------|------|
| SC-001 / SC-002 | 四模式各取一个团队跑生成器 + 第 2 节四步 | 退出码 0、`missing_required: []`、零人工编辑表单 |
| SC-003 | 刷新前后比对变更集与 SC-003 所列五组内容指纹 | 变更 100% 落在 goal 交付目录;`.specify/teams/**` / 被监控目标 / 技能自身文件 / `.specify/agents/**` / `.specify/project/` 既有产物零变更 |
| SC-004 | 程序扫描派生数据出处字段非空率与路径可达性 | 非空率 100%、抽样路径 100% 可达且 tracked |
| SC-005 | 同一团队在 K 与 2K 次运行水位各采一次注入量 | 增长倍数 < 2 |
| SC-006 | 构造 report-only 档情景 | 跳过率 100%、正常收尾率 100%、跳过被记录率 100% |
| SC-007 | 同一 goal 连续刷新两次,第一次后手工加批注 | 当前总结恒为 1 份;批注保留率 100% |
| SC-011 | 两次刷新前后对身份键集合做差集 | 重复 0、静默丢失 0、推断标记率 100% |
| SC-012 | 选取累积条目超阈值的团队 | 分解图节点数 ≤ 15(深度 ≥2);数据层保留率 100% |
| SC-013 | 双团队同 `goal_slug` 夹具 + 一次 goal 正文改写 + 一次推断→显式迁移 | 同值团队 100% 落同一目录;正文改写后路径变化 0;推断标记率 100%;并列目录数 0 |
| SC-014 | 只刷新其中一个团队,再核对另一团队贡献 | 各团队工作项出现率 100%;历史贡献丢失 0;归属可机器判定率 100% |
| SC-015 | 让两个团队邻近触发刷新 | 当前总结恒为 1 份;丢失更新 0;半写产物 0;被跳过者留状态行 100% |

**存量团队现状**:仓内 4 个团队为 2 个 `continuous`(`cws-workspace-cluster`、`requirement-implement-monitor`)+ 2 个 `iteration`(`draw-plantuml-optimizer`、`summarize-project-optimizer`),且**均未声明 `goal_slug`**(全部走 FR-034 的推断路径)。SC-001 的 `serial` 与 `parallel` 两格、以及 SC-013/014/015 的"双团队同 goal"场景**均无存量团队可用**,需在 `tests/fixtures/` 构造夹具团队。

## 6. 镜像同步(改任何 canonical 源之后)

```bash
python3 scripts/python/sync-mirrors.py --check    # exit 2 = 存在漂移
python3 scripts/python/sync-mirrors.py --write    # 同步镜像 + 再生 per-tool 命令副本
```

需同步的源见 [plan.md](plan.md) § Mirror Obligations。**不要**手工编辑镜像或 per-tool 副本。
