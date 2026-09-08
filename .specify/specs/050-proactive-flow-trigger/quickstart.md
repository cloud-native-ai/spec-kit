# Quickstart — 主动触发机制(Proactive Flow Trigger)

**Requirement**: `050-proactive-flow-trigger` → Feature 050
**Date**: 2026-09-07
**Scenarios**: 6(每个场景对应一组 FR 与 SC,可独立走查)

> **CLI 示例的有效性钉桩**:引擎在本阶段尚未实现,故下列每条示例**无法被执行验证**。它们全部由 `contracts/trigger-engine.md` 的 C-9(action 封闭枚举,11 项)、C-10(flag 封闭集)、C-11(标识符格式)钉住,并由 `tests/contract/test_trigger_engine.py` 以"解析本文件代码块 → 逐条校验 action / flag / 标识符"的方式机械断言(见该契约末节)。实现期若需调整语法,**先改契约再改本文件**,不得反向。
>
> 所有示例假定 CWD 为项目根;`--workspace` 仅在跨根走查时显式给出。

---

## 场景 1 — 全 agent 必经路径覆盖(FR-001 / FR-003 / SC-001)

**目的**:验证触发段抵达**全部** agent 必经路径,含当前恒 `fail` 的 hermes 与 opencode。计数口径以 `trigger-section.md` **C-10 为唯一权威**:`_INSTRUCTIONS_FILE_MAP` 有 6 个 key、去重后 **5 个声明文件**(`codex` 与 `qoder` 共用 `AGENTS.md`),生成脚本共创建 **8 条 symlink**。

```bash
# 在干净的临时根上初始化(任一 agent 均可,路径集合与所选 agent 无关)
# --force 使 --here 在非空目录下不弹交互提示,保证走查可自动化;--ignore-agent-tools 跳过 CLI 探测
TMP=$(mktemp -d) && cd "$TMP" && git init -q .
specify init --here --ai qoder --force --ignore-agent-tools

# ① 5 个声明文件(_INSTRUCTIONS_FILE_MAP 去重后的值)
for p in CLAUDE.md AGENTS.md HERMES.md .github/copilot-instructions.md .opencode/instructions.md; do
  test -e "$p" && echo "OK   $p -> $(readlink -f "$p")" || echo "MISS $p"
done

# ② 另 3 条(QODER.md + 2 条 IDE 侧链接),与 ① 合计 8 条 symlink
for p in QODER.md .qoder/project_rules.md .claude/project_rules.md; do
  test -e "$p" && echo "OK   $p -> $(readlink -f "$p")" || echo "MISS $p"
done

# 触发段确实到达(经 symlink 读 canonical 源)
grep -c '^## Proactive Flow Trigger' AGENTS.md
```

**预期**:① 的 5 条与 ② 的 3 条**共 8 条全部 `OK`**,且都解析到 `.specify/instructions.md`;`grep -c` 输出 `1`。
**契约**:`trigger-section.md` C-1 / C-10 / C-12。**度量源**:SC-001。
**回归对照**:改动前 `HERMES.md` 与 `.opencode/instructions.md` 为 `MISS`,`_check_instructions` 对 hermes/opencode 返回 `fail`。

---

## 场景 2 — 冷启动首日建议(FR-022 / FR-006 / SC-013;US2 场景 12)

**目的**:验证一个**从未积累任何学习记录**的项目,第一天就能得到正确建议。

```bash
# 由出厂种子建状态(幂等;首次运行即创建 .specify/memory/trigger/)
python3 scripts/python/trigger-utils.py --action init

# 查看规则集:应看到 origin=seed 的规则已就位
python3 scripts/python/trigger-utils.py --action rules --format text

# 情境:只有 requirements.md 且含未决澄清标记 -> 应建议 /speckit.clarify
# --compliance-done 声明本回合的 constitution 合规分析已先行完成(缺省为 false,会如实报 ordering-violation)
python3 scripts/python/trigger-utils.py --action assess \
  --session s1 --turn-id s1-01 --compliance-done \
  --stage requirements-unclear --signal needs-clarification
```

**预期**:`payload.suggestion` 非空,`flow` 为 `/speckit.clarify`,`invocation` 为可直接复制的调用形式,`autoExecute` 为 `false`(尚无晋升);`telemetry.jsonl` 追加一行且 `suggested=true`、`complianceDone=true`。
**契约**:`trigger-engine.md` C-12 / C-14 / C-15;`seed-derivation.md` C-8(**13** 个命名情境全覆盖)。
**反例断言**:若把 `--stage` 换成词表外的值(如 `--stage bogus`),退出码 MUST 为 `4`(`EXIT_INVALID`),`errors[]` 含 `vocabulary-out-of-range`。

---

## 场景 3 — 每回合静默与探测升级率(FR-005 / FR-005a / FR-009② / SC-011;US2 场景 8/9/10)

**目的**:验证"每回合评估"付得起——无关回合零可见输出,且探测升级率有界。

```bash
# 连续 20 个与框架能力无关的回合:stage=non-feature 且无信号 -> 应恒无建议
for i in $(seq -w 1 20); do
  python3 scripts/python/trigger-utils.py --action assess \
    --session s2 --turn-id "s2-$i" --stage non-feature
done

# 汇总:探测升级率与静默性(SC-011 的两个判据)
python3 scripts/python/trigger-utils.py --action status --format json
```

**预期**:`status` 的 `payload.telemetry.turns` == 20、`payload.telemetry.escalationPct` == 0(未传 `--probe`)、`payload.telemetry.visibleOutputCount` == 0;`payload.probeBudgetPct` 回显上限 20 与实测 0 的对比。

```bash
# 环境信息不足时才升级:显式 --probe,由引擎做确定性探测并记 escalated=true
python3 scripts/python/trigger-utils.py --action assess \
  --session s3 --turn-id s3-01 --compliance-done \
  --stage implementing --signal open-tasks --probe
```

**预期**:该回合遥测行 `escalated=true`;引擎只回传摘要(单条 ≤ 200 字符),不回传制品正文。
**契约**:`trigger-engine.md` C-13(未传 `--probe` 时 MUST NOT 打开任何制品文件,以文件打开计数断言)/ C-14 / C-15。
**反模式守卫**:若实现让每个回合都隐式升级,`escalationPct` 会逼近 100 并突破 `probeBudgetPct`——这正是 SC-011 存在的理由(首轮 Q2=C 的护栏)。

---

## 场景 4 — 阈值晋升与破坏性豁免(FR-010 / FR-011 / FR-012 / SC-005 / SC-006;US3 场景 1/2/3)

**目的**:验证连续采纳达阈值后免确认自动执行,且破坏性流程**永不**晋升。

```bash
# 可逆流程:连续采纳 3 次(默认阈值)。每次采纳用独立 session —— 这既是真实形态
# (三次分别发生在三个场合),也避免 C-20 的会话级重复抑制把第 2/3 次的建议吞掉。
# 每次 record 前必须先 assess:V3.4 规定 record 的事件字段从同会话最近一次 assess 关联填充,
# 无在先 assess 即 EXIT_INPUT_ERROR(2) + errors:["no-prior-assess"]。
for i in 1 2 3; do
  python3 scripts/python/trigger-utils.py --action assess \
    --session "s4-$i" --turn-id "s4-$i-01" --compliance-done \
    --stage requirements-unclear --signal needs-clarification
  python3 scripts/python/trigger-utils.py --action record \
    --session "s4-$i" --rule r-001 --response accepted
done

# 第 4 次:应已晋升 -> autoExecute=true
python3 scripts/python/trigger-utils.py --action assess \
  --session s4-4 --turn-id s4-4-01 --compliance-done \
  --stage requirements-unclear --signal needs-clarification
```

**预期**:第 4 次 `payload.suggestion.autoExecute == true`;`rules` 中 `r-001` 的 `state` 为 `promoted`。

```bash
# 一次拒绝即重置计数(R2-Q3:晋升编码稳定的当前偏好)
python3 scripts/python/trigger-utils.py --action record \
  --session s4-4 --rule r-001 --response declined
python3 scripts/python/trigger-utils.py --action rules --format text
```

**预期**:`r-001` 的 `consecutive` 回到 `0`、`state` 回落 `active`、`autoExecute` 不再为 `true`;`promotion.resetBy` 指向该 `eventId`。

```bash
# 破坏性流程:连续采纳 10 次也绝不晋升(SC-005 零容忍判据;强于 SC-005 的 ≥5 次下限)
# r-006 = s06 = (tasks-ready, open-tasks) -> /speckit.implement,confirmationClass=destructive
for i in $(seq -w 1 10); do
  python3 scripts/python/trigger-utils.py --action assess \
    --session "s5-$i" --turn-id "s5-$i-01" --compliance-done \
    --stage tasks-ready --signal open-tasks
  python3 scripts/python/trigger-utils.py --action record \
    --session "s5-$i" --rule r-006 --response accepted
done
python3 scripts/python/trigger-utils.py --action assess \
  --session s5-11 --turn-id s5-11-01 --compliance-done \
  --stage tasks-ready --signal open-tasks
```

**预期**:`r-006`(`/speckit.implement`,`confirmationClass=destructive`)的 `promotion.promoted` 恒 `false`、`state` 恒 ≠ `promoted`;`assess` 返回的 `autoExecute` 恒 `false`。
**契约**:`trigger-engine.md` C-16 / C-17 / C-18。**分类来源**:`data-model.md` §命名情境表(存疑从严:`/speckit.implement` 虽 git 可回退,但影响面大 → `destructive`)。

```bash
# 用户复位与全局降级(FR-012 / FR-018 / SC-009)
python3 scripts/python/trigger-utils.py --action reset --rule r-001
python3 scripts/python/trigger-utils.py --action reset --all
python3 scripts/python/trigger-utils.py --action config --enabled false
python3 scripts/python/trigger-utils.py --action assess \
  --session s6 --turn-id s6-01 --stage requirements-unclear --signal needs-clarification
```

**预期**:关闭后 `payload.suggestion` 恒 `null`,建议产出数与自动执行数均为 0;该状态在 `/speckit.instructions` 再生后仍生效(状态与指令文件分离)。恢复用 `--action config --enabled true`。

---

## 场景 5 — 遥测有界与轮转零丢失(FR-009a / SC-015)

**目的**:验证遥测不会无限增长,且轮转**不清空**学习结果。

```bash
# 声明保留窗口(默认 200 回合)
python3 scripts/python/trigger-utils.py --action config --window 50

# 制造超过窗口的遥测行。注:stage=non-feature 且无信号,在删除 s14 后不匹配任何情境,
# 故 60 个回合都如实无建议(与场景 3 同源),这里只考察遥测的有界性。
for i in $(seq -w 1 60); do
  python3 scripts/python/trigger-utils.py --action assess \
    --session s7 --turn-id "s7-$i" --stage non-feature
  # V4.3 是「追加即截断」的恒真不变量:每次调用返回后行数都须 ≤ 窗口,
  # 因此无需等到 rotate 才可断言(每 10 回合抽查一次)
  if [ $((10#$i % 10)) -eq 0 ]; then
    n=$(wc -l < .specify/memory/trigger/telemetry.jsonl)
    [ "$n" -le 50 ] && echo "OK   after turn $i rows=$n (<=50)" || echo "FAIL after turn $i rows=$n"
  fi
done

# 轮转前记录晋升态,轮转后逐规则比对
python3 scripts/python/trigger-utils.py --action rules --format json > /tmp/rules-before.json
python3 scripts/python/trigger-utils.py --action rotate
python3 scripts/python/trigger-utils.py --action rules --format json > /tmp/rules-after.json
diff /tmp/rules-before.json /tmp/rules-after.json && echo "OK zero loss"
wc -l < .specify/memory/trigger/telemetry.jsonl
```

**预期**:循环内每次抽查都输出 `OK … rows≤50`(**不必等 rotate** —— V4.3 已由"轮转后不超窗"改为"追加即截断"的恒真不变量);`diff` 无输出(晋升计数与规则状态**逐一相等**);末尾 `wc -l` ≤ 50。
**契约**:`trigger-engine.md` C-6(原子写)/ `rotate` 行语义;`data-model.md` V4.3(恒真不变量)/ V4.4(轮转与截断均不触及 `index.json`)。
**该场景判别的具体缺陷**:① 若实现只在 `rotate` 时截断,循环内的抽查会在第 51 回合起 `FAIL`;② 若实现把晋升计数做成从原始遥测行重算,一次截断即清空全部学习结果——`diff` 会立刻暴露。

---

## 场景 6 — 漂移检出与调优批准(FR-015 / FR-016 / FR-017 / SC-007 / SC-013;US4)

**目的**:验证种子与 `## Handoffs` 的漂移被机械检出,且规则调优非经批准不生效。

```bash
# 6a 漂移检出:改写某命令模板的 Handoffs 而不同步种子 -> 契约测试必须失败
pytest tests/contract/test_trigger_seed_derivation.py -q
# 期望:全绿。随后做一次受控实验——临时把 templates/commands/clarify.md 的
# Handoffs 中 "/speckit.plan" 改为其他流程名,重跑:
pytest tests/contract/test_trigger_seed_derivation.py -q
# 期望:失败,且错误信息同时给出 ruleId、provenance.file 与缺失的 flow 值
```

**预期**:失败信息可直接定位到需同步的种子条目。**修复方式是同步种子文件,不是放宽测试**(`seed-derivation.md` C-7 与 `discipline-doc.md` `Maintenance Duties` ①)。

```bash
# 6b 漏报证据:用户手动调用了某流程而当回合无建议
python3 scripts/python/trigger-utils.py --action record-manual --flow /speckit.history

# 6c 证据聚合 -> 调优提议(确定性部分)
python3 scripts/python/trigger-utils.py --action tune --min-sample 5 --format json

# 6d 未经批准:规则集零变更
python3 scripts/python/trigger-utils.py --action rules --format json > /tmp/rules-pre.json

# 6e 用户批准后写回(留证据与痕迹)
python3 scripts/python/trigger-utils.py --action tune-apply \
  --proposal p-001 --reason "decline-rate 0.71 over 7 hits"
python3 scripts/python/trigger-utils.py --action rules --format json > /tmp/rules-post.json
diff /tmp/rules-pre.json /tmp/rules-post.json
```

**预期**:6c 的 `payload.proposals[]` 每条附证据(指标 + 样本数);`semanticJudgmentPending[]` 交回需 agent 判断的项(该不该采纳、新规则配哪条流程);`stats.hits < 5` 的规则**不出现**在提议中,且被跳过的规则在 `notes[]` 具名回显(小样本守卫);6d 与 6e 之间规则集零变更,`tune-apply` 后 `diff` 显示变更且 `tuning.{ratifiedAt, evidenceRef}` 可回查。
**契约**:`trigger-engine.md` C-3(信封)/ `tune`、`tune-apply` 行语义;`data-model.md` SM-2 与 §漏报检测。

---

## 走查顺序建议

场景 1 → 2 是 **MVP 验证**(US1 + US2,两个 P1);场景 3 验证首轮三项裁定的**可负担性前提**(每回合评估 + 近零默认预算);场景 4 → 5 → 6 依次验证 US3 与 US4。场景 4 的破坏性豁免段是本特性**安全边界**的判别走查,任何实现改动后都 MUST 重跑。

## 与既有门禁的联动核对(收尾必跑)

```bash
# 门控预算:total 必须仍为 23、violations 为 0(整数余量为 0)
python3 scripts/python/scan-confirmation-gates.py --summary

# 镜像:五对全绿(scripts 对为 STRICT)
python3 scripts/python/sync-mirrors.py --check

# 命令副本:本特性不改命令模板,故必须保持 exit 0
python3 scripts/python/regen-command-copies.py --check

# 章节传播:既有守卫 + 新契约
pytest tests/contract/test_instructions_section_propagation.py \
       tests/contract/test_proactive_trigger_section.py \
       tests/contract/test_proactive_trigger_discipline_doc.py \
       tests/contract/test_trigger_engine.py \
       tests/contract/test_trigger_seed_derivation.py \
       tests/unit/test_trigger_utils_units.py \
       tests/integration/test_trigger_promotion.py \
       tests/integration/test_trigger_telemetry.py \
       tests/integration/test_trigger_tuning.py -q
```
