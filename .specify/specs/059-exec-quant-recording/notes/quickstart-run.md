# Quickstart Run Log(Feature 059 实跑留痕)

各场景的真实命令与输出;执行日 2026-10-16,宿主 = 本机(简报 §3 dated 可行性清单所指宿主)。场景前置(①–⑬)逐项在对应节内复核。

## 场景 1:一次执行落恰好一条记录(SC-001 / US1)— T009

前置复核:① 动作封闭集(实测 `--action nonsense` 报 `choose from 'collect', 'list-records', 'score'`);② kind 字面量(实测记录 `kind: "speckit.exec-quant"`);③ 存储路径(实测 `.specify/memory/exec-quant/records.jsonl`);④ compile→regen→sync 顺序(实测三步 exit 0,注册表投影先行——见 tasks T008 备注);⑤ 标签机械派生(实测编译行 `2. Exec Quant — …`,位于 Run Determination 之后)。

执行的真实受测单元 = `/speckit.implement`(本特性实现命令自身),按其编译面 wrap-up 顺序实跑步骤 1–2(run_id 由调用方补参,既有约定):

```text
$ python3 .specify/scripts/python/run-determination.py --action determine \
    --unit-id "/speckit.implement" --unit-type command \
    --run-id "059-exec-quant-smoke" --complexity complex --qualification qualified
unit: /speckit.implement   run: 059-exec-quant-smoke
  token_consumption    not_evaluated (source_unavailable)
  elapsed              not_evaluated (source_unavailable)
  artifact_correctness not_evaluated (no_declared_checks)
  satisfaction         not_evaluated (pending_next_turn)
persisted: .specify/memory/session/20261016T051925Z-run-determination-speckit-implement-059-exec-quant-smoke.md
(determine exit=0)

$ python3 .specify/scripts/python/exec-quant.py --action collect \
    --unit-id "/speckit.implement" --unit-type command
exec-quant: recorded /speckit.implement run=059-exec-quant-smoke resolution=adopted \
  -> /storage/project/cloud-native-ai/spec-kit/.specify/memory/exec-quant/records.jsonl
(collect exit=0)
```

直读审计(`records.jsonl`,US1 期独立审计面 = 存储直读;列出动作 US2 落地后由 T012 复审计):

```text
total records: 1
records for (unit, run): 1                       # SC-001 恰一条
kind: speckit.exec-quant | schema_version: 1 | resolution: adopted
field groups present: ['agent', 'llm', 'quality']  # 三字段组齐备
null leaves: 0 | empty leaves: 0 | not_evaluated leaves: 5   # 零空缺
known-uncollectable checks: reasoning_effort = not_evaluated   # 未设 effort → 显式标记
config_source = {'value': '/home/agent/.qoder/settings.json', 'provenance': 'measured'}
agent resolution: resolved | model: {'value': 'gfmodel', 'provenance': 'measured'}
quality: {elapsed_ms/tokens/errors/satisfaction 均 not_evaluated}   # 判定记录无测量量,不携带
qualification: {'value': 'qualified', 'provenance': 'carried'}      # 自同 run 判定记录携带
V2 field binary law: PASS
```

SC-002 判定:已知采不到字段(未设置的 reasoning effort、生效端点权威值——后者本引擎只录候选与连接证据,不断言生效)100% 以显式标记落库;抽检零臆造值(elapsed/tokens 无判定测量即 not_evaluated,未推断)。

**US1 独立功能成立**:真实单元执行 → 恰好一条完全可审计的量化记录;存储边界与非阻塞行为可观察(collect exit 0,不劣化 determine)。

## 场景 2:未采标记覆盖审计(SC-002)— T012(经 list-records 机器可读形态复审计)

前提复核:⑥ `not_evaluated` 词形逐字([[STR-002]]);⑦ 本宿主已知采不到字段集以简报 §3 dated 清单为基准(生效端点权威值、未设 effort)。钉定测试:`test_exec_quant_engine.py` 字段二值律(V2)。

```text
$ exec-quant.py --action list-records --format json   # 全 store
not_evaluated count: 5 (expect > 0)      # 通过
null count: 0 | empty count: 0 (expect 0/0)   # 通过(零空缺)
```

## 场景 3:补打分与来源区分(US2)— T012

前提复核:⑧ score 前置 = 目标 `(unit_id, run_id)` 已在 records.jsonl;⑨ 分值 1–5 通道约定;⑩ scores 落 `scores.jsonl`、list 时 join、与 carried 满意度凭 provenance 区分。钉定测试:`test_exec_quant_engine.py` score 断言(append-only、越界退出码 2、来源标注)。

```text
$ exec-quant.py --action score --unit-id "/speckit.implement" \
    --run-id "059-exec-quant-smoke" --score 4 --note "手测通过"
exec-quant: scored /speckit.implement run=059-exec-quant-smoke score=4 \
  provenance=user-given -> .specify/memory/exec-quant/scores.jsonl
(score exit=0)

$ exec-quant.py --action list-records --unit-id "/speckit.implement" --format json
joined score: 4 | provenance: user-given | note: 手测通过
quality.satisfaction: not_evaluated (stays carried-or-marker, not overwritten)
```

来源区分判定:join 打分携带 `provenance == user-given`,`quality.satisfaction` 保持其自身来源(本记录为显式未采标记,判定记录推导时为 carried)——两字段互不覆写,FR-014 成立。记录本身未变(records.jsonl 未被触碰,score 仅追加 scores.jsonl)。

## 场景 4:边界隔离(SC-004 / US3)— T014

前提复核:⑪ package 前置 = feedback store 存在 pending 条目(实测 `--action status`:count_since_submission=39,非空);空 store 行为未单测(本 store 非空,行为前提以既有 `tests/integration/test_feedback_*.py` 套件为准——T015 全量运行覆盖)。**quickstart 路径前提勘正**:场景 4 所写 `unzip -l feedback/feedback-*.zip` 已过时——package 实际产物落 `.specify/memory/feedback/packages/feedback-<ts>.zip`(056 迁移后行为,以 `--action package` 实际输出为准),本节按实测路径执行。⑫ 验证 zip 于验证后移除,不与真实打包产物混淆(本 run 之前 packages/ 目录为空,移除后复归为空)。⑬ 凭据判定以值级防御扫描为准(引擎内置 D9);quickstart 的 jq 形态按字面会命中**字段名**(`quality.tokens` 含 "token")而非值级,故人读复核按值级适配执行(仅扫叶子字符串值,不扫键名),勘正记录于此。

```text
$ python3 .specify/scripts/python/feedback-utils.py --action package
Packaged 39 feedback entries (sources untouched):
  zip: .specify/memory/feedback/packages/feedback-20261016T053231Z.zip
(package exit=0)

$ unzip -l .specify/memory/feedback/packages/feedback-20261016T053231Z.zip
  ... 88512 bytes, 40 files
exec-quant hits in listing: 0        # 打包产物零量化记录(结构性排除)
entries mentioning quant: 0

$ exec-quant.py --action list-records --format json   # 值级凭据复核
records: 1 | credential-shaped value hits: 0 (expect 0)
```

(zip 已按 ⑫ 移除;打包来源条目 untouched。)

## 场景 5:非回归与基线比对(SC-003 / US3)— T015

基线 = T002 于 implement 开工日冻结的 `baseline-failed.txt`(canonical runner `--names-out` 形态;本 run 连续执行,基线不重冻——重冻会把特性引入的失败误作既有)。非回归基面 25 文件(20 contract + 5 integration,data-model §4)经 `--collect-only` 核实全部实际收集(433 项,无静默跳过);有意扩展的 `test_probe_engine_action_sets.py` 先于比对落定且自身绿(T004→T005→T008 链)。

```text
$ bash scripts/bash/run-tests.sh --names-out /tmp/current-failed-t015.txt \
    tests/contract tests/integration -q
10 failed, 3240 passed in (≈100s)

$ comm -13 baseline-failed.txt /tmp/current-failed-t015.txt
(空 — 零新增失败名)
$ comm -31 baseline-failed.txt /tmp/current-failed-t015.txt | wc -l
0   # 双向一致:失败集合与基线逐名完全相同
```

**SC-003 判定:通过** — name-level 房式判据(非计数),比对覆盖全部 contract + integration 套件(⊇ 基面 25 文件)。中途全量比对共执行 4 次(Phase 2 提交门两次、Phase 3 一次、本节末次),每次 `comm -13` 均为空。
