# Contract: Probe 注册与编译面接线(Feature 059)

**Spec**: `.specify/specs/059-exec-quant-recording/requirements.md` | **Date**: 2026-10-16
**Truth source**: `shared/definitions/probe-definitions.md`(伞形注册表;本文件声明 059 落入其四表的目标行,由 `--action probes --validate` / `handlers --validate` 与契约测试钉住)

## 1. 注册表新增行(逐字目标)

### ## Classes(+1 行,scripts 切片)

```text
| exec-quant | internal | 受测单元执行的环境与质量遥测采集(agent 程序 / LLM 详细 / 质量指标;exec-quant durable store,Recording Only) | scripts | collect→durable-record | wrap-up | `scripts/python/exec-quant.py`:`ACTIONS`,`build_record`,`resolve_run_identity` |
```

### ## Objects(+4 行,unit = 引擎脚本路径)

```text
| eq-collect-execution | exec-quant | scripts/python/exec-quant.py | wrap-up |
| eq-probe-host-process | exec-quant | scripts/python/exec-quant.py | wrap-up |
| eq-probe-host-config | exec-quant | scripts/python/exec-quant.py | wrap-up |
| eq-probe-determination-link | exec-quant | scripts/python/exec-quant.py | wrap-up |
```

四 Object 与 data-model §1.4 采集面一一对应:主采集、宿主进程可得性、宿主配置面可得性、同 run 判定记录可得性。

### ## Handler(+1 行)

```text
| h-exec-quant | engine | collect | non-blocking | 15 | scripts/python/exec-quant.py |
```

- `action=collect` MUST 命中真实引擎 union(经 `_ENGINE_SIBLINGS` 扩展,见 §2)。
- `order=15`:同 lifecycle point 内唯一(10 = h-run-determination,20 = h-feedback-record),满足 FR-003「运行判定之后执行」。

### ## HandlerBinding(+1 行)

```text
| h-exec-quant | @point:wrap-up | all | 059 执行量化采集:每受测单元 wrap-up 落一条量化记录;在运行判定(order 10)之后、反馈记录(order 20)之前,同 run 携带不重测 |
```

scope=`all` ⇒ 69+ 单元全部生效,与 `h-run-determination` 同语义(FR-001 的 covered-unit 集合一致)。

## 2. 引擎注册代码侧改动(唯一一处)

`scripts/python/probe-utils.py` `_ENGINE_SIBLINGS`(L620–621)追加 `"exec-quant.py"`:

```python
_ENGINE_SIBLINGS = ("feedback-utils.py", "run-determination.py", "probe-utils.py",
                    "trigger-utils.py", "exec-quant.py")
```

效果:`_engine_action_union()` 经 argparse `choices=[...]` 分支实读 `scripts/python/exec-quant.py`(与 feedback/probe 引擎同路径;`ACTIONS` 元组分支仅 name-gated 于 run-determination/trigger-utils 两引擎,probe-utils L632),`h-exec-quant` 的 `collect` 命中 union,`handlers --validate` 通过。引擎的 choices 声明 MUST 与运行时 `--action` 校验一致。**MUST NOT** 手抄 action 清单进任何对账面(One Source of Truth:action 真源是引擎源码)。

## 3. engine-action-sets.md 对账面(056 契约,新增分区)

`.specify/specs/056-probe-handler-system/contracts/engine-action-sets.md` 增补分区节(既有 probe-utils/feedback-utils 两分区**逐字不动**):

```markdown
### exec-quant.py — 3 个 action

collect  list-records  score

- 059 新引擎;动作闭包自引擎 argparse choices 实读(choices 路径,与
  feedback/probe 同);exact-pin 与跨引擎动作名零交集断言钉住
  (test_probe_engine_action_sets.py 扩展)。
```

配套测试扩展(`tests/contract/test_probe_engine_action_sets.py`):union 构造追加 `_execquant_actions()`;新增 `test_exec_quant_action_set_exact()`(双向钉:choices == {collect, list, score});既有 `test_probe_utils_action_set_exact` / `test_feedback_utils_action_set_exact` 断言不动。

## 4. 编译面再生(传播固定顺序)

注册行落定后按固定顺序再生(`test_compile_propagation_order.py` 钉住):

1. `probe-utils.py --action compile-embeds` → 72 面(23 命令模板 + 49 技能 SKILL.md)的 `## Wrap-up` 各 +1 行:`N. Exec Quant — \`python3 .specify/scripts/python/exec-quant.py --action collect --unit-id "…" --unit-type …\``(标签机械派生,渲染器零改动;fingerprint 更新)。
2. `regen-command-copies.py` → per-tool 命令副本再生。
3. `sync-mirrors.py --write`(范围化:scripts/ shared/ templates/ skills/)→ 运行时镜像投影。

**行预算判据**(实测 2026-10-16:72 面 / 431 非空行 / 预算 853):再生后总行数 ≈ 503 ≤ 853,`test_wrap_up_line_budget.py` 无需 re-adjudicate;若实测突破预算,按该测试自身提示路径(re-adjudicate)走显式裁定,不静默放宽。

**宿主只读边界不变**:本特性不新增任何宿主侧写入面;外部 custom 单元经既有 probe-inject 途径获得 wrap-up 面后同样生效。
