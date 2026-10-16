# Quickstart: Feature 059 执行量化记录(Recording Only)

**Spec**: `.specify/specs/059-exec-quant-recording/requirements.md` | **Date**: 2026-10-16

五个场景走通「执行 → 落库 → 审计 → 打分 → 边界与非回归」闭环。引擎(`scripts/python/exec-quant.py`)在 `/speckit.implement` 前尚不存在——**逐示例免责**适用于下文每一条引擎命令:实现完成后按各示例的**前提清单**逐项复核(路径、旗标、字面量),并由指名的契约测试钉定(执行-验证规则 route b)。

## 场景 1:一次执行落恰好一条记录(SC-001 / US1)

```bash
# 步骤 0(前置,一次性):注册行落定后再生编译面——顺序固定
python3 scripts/python/probe-utils.py --action compile-embeds
python3 scripts/python/regen-command-copies.py
python3 scripts/python/sync-mirrors.py --write

# 步骤 1:真实执行任一受测单元(如 /speckit.clarify),其 wrap-up 含新步骤行:
#   N. Exec Quant — `python3 .specify/scripts/python/exec-quant.py --action collect \
#        --unit-id "/speckit.clarify" --unit-type command`
#   (执行该行;判定记录存在则携带其四轴)

# 步骤 2:查询与审计
python3 .specify/scripts/python/exec-quant.py --action list-records \
  --unit-id "/speckit.clarify" --format json | jq 'length'        # 期望:1
python3 .specify/scripts/python/exec-quant.py --action list-records \
  --unit-id "/speckit.clarify" --format json | jq '.[0].kind'     # 期望:"speckit.exec-quant"
```

> **免责(适用于步骤 0–2 全部命令)**:引擎与注册行未实现,命令不可执行。前提清单:① 动作封闭集 argparse `choices=["collect", "list-records", "score"]` 与 `--unit-id/--unit-type/--run-id/--format` 旗标形如 `contracts/exec-quant-cli.md`;② 记录 kind 字面量 = `speckit.exec-quant`([[STR-001]]);③ 存储路径 `.specify/memory/exec-quant/records.jsonl`;④ compile→regen→sync 顺序;⑤ wrap-up 行标签 "Exec Quant" 由 handler_id 机械派生。钉定:`tests/contract/test_exec_quant_engine.py`(动作集/存储路径/kind 字面量/退出码)+ `tests/contract/test_probe_engine_action_sets.py` 扩展。

## 场景 2:未采标记覆盖审计(SC-002)

```bash
python3 .specify/scripts/python/exec-quant.py --action list-records --format json \
  | jq '[.[] | .. | objects | select(. == "not_evaluated")] | length'   # 期望:> 0(已实测宿主存在采不到字段)
python3 .specify/scripts/python/exec-quant.py --action list-records --format json \
  | jq '[.[] | .. | select(type == "null" or . == "")] | length'        # 期望:0(零空缺)
```

> **免责**:同场景 1 前提 ①②;另加 ⑥ 值域词形 `not_evaluated` 逐字([[STR-002]],复用运行判定既有词形);⑦ 本宿主已知采不到字段集以简报 §3 dated 清单为基准(生效端点权威值、未设 effort)。钉定:`test_exec_quant_engine.py` 的字段二值律断言(V2:零 null/零空串、provenance 封闭词域)。

## 场景 3:补打分与来源区分(US2)

```bash
python3 .specify/scripts/python/exec-quant.py --action score \
  --unit-id "/speckit.clarify" --run-id "<场景1记录的run_id>" --score 4 --note "手测通过"
python3 .specify/scripts/python/exec-quant.py --action list-records \
  --unit-id "/speckit.clarify" --format json | jq '.[0].scores'   # 期望:含 provenance=="user-given" 的一条
```

> **免责**:同场景 1;另加 ⑧ score 前置 = 目标 `(unit_id, run_id)` 已在 records.jsonl(无记录 → 退出码 2);⑨ 分值 1–5 通道约定;⑩ scores 落 `scores.jsonl`、list 时 join、与 carried 满意度凭 provenance 区分。钉定:`test_exec_quant_engine.py` 的 score 动作断言(append-only、越界退出码 2、来源标注)。

## 场景 4:边界隔离(SC-004 / US3)

```bash
# 打包产物零量化记录(结构性排除:package 只读 feedback store)
python3 .specify/scripts/python/feedback-utils.py --action package
unzip -l feedback/feedback-*.zip | grep -c "exec-quant"   # 期望:0

# 凭据零出现
python3 .specify/scripts/python/exec-quant.py --action list-records --format json \
  | jq '[.[] | tostring | test("(?i)(api[_-]?key|token|secret|authorization)")]' \
  | jq 'any'                                              # 期望:false
```

> **免责**:feedback package 命令为既有引擎(可执行),但其行为前提须实现期复核:⑪ package 前置 = feedback store 存在 pending 条目,空 store 行为(优雅空包 vs 报错)以 `feedback-utils.py --action package --help` 与既有集成测试为准;⑫ 验证用临时 zip 在验证后移除,不与真实打包产物混淆;⑬ 凭据判定以**值**级防御扫描为准(引擎内置,D9),此 grep 仅为人读复核。钉定:`test_exec_quant_engine.py`(凭据扫描/白名单 origin)+ 既有 `tests/integration/test_feedback_*.py`(打包行为)。

## 场景 5:非回归与基线比对(SC-003 / US3)

```bash
# 实现开工日冻结基线(T1 义务,049/050/051 先例):
python3 -m pytest tests/contract tests/integration -q 2>&1 \
  | grep "^FAILED" | sort > /tmp/baseline-failed.txt
# 实现完成后同命令重跑,房式判据:
python3 -m pytest tests/contract tests/integration -q 2>&1 \
  | grep "^FAILED" | sort > /tmp/current-failed.txt
comm -13 /tmp/baseline-failed.txt /tmp/current-failed.txt   # 期望:空(零新增失败)
```

> **免责**:pytest 调用形态为仓库标准;基线内容**以冻结日实测为准,禁止预写**(运行判定「测量而非印象」)。非回归基面逐文件清单见 `data-model.md` §4;`test_probe_engine_action_sets.py` 的**有意扩展**必须先于比对落定(扩展后自身须绿),否则其新增失败会被误判为回归。
