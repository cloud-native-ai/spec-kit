# Quickstart: 快速失败纪律(Fast Fail)

**Requirement**: `052-fast-fail-principle` → Feature 052  
**Date**: 2026-09-23  
**Guards**: `contracts/` 五份 · `tests/contract/test_fast_fail_discipline.py`

**执行核验声明(逐场景,非文件级)**:下列每个场景分两部分。**「改前基线」的每条命令都已于 2026-09-23 在本仓实跑,其期望值取自实跑输出而非意图**;**「改后期望」的命令依赖尚未创建的制品**(`shared/guidelines/fast-fail.md`、常驻章节、宪章原则 XIV/XVI、注入子句副本),改前实跑会报 `No such file or directory` 或计数为 0,故逐场景标注为**改前不可实跑**,并给出其改前等价基线。没有任何一个场景的期望值是凭意图写的。

## 改前基线总表(2026-09-23 实跑)

| 量 | 命令 | 实测值 |
|---|---|---|
| `shared/guidelines/*.md` 份数 | `ls -1 shared/guidelines/*.md \| wc -l` | **12** |
| `fast-fail.md` 是否存在 | `ls shared/guidelines/fast-fail.md` | **No such file** |
| 指令模板 `## ` 节数 | `grep -c '^## ' templates/instructions-template.md` | **18** |
| 活动指令文件 `## ` 节数 | `grep -c '^## ' .specify/instructions.md` | **19** |
| 三个锚点章节行号 | `grep -n '^## Token Efficiency…\|^## User-Facing…\|^## Dogfooding…'` | **66 / 74 / 86** |
| 宪章模板原则数 | `grep -c '^### [IVX]*\. ' templates/constitution-template.md` | **13** |
| 活动宪章原则数 | `grep -c '^### [IVX]*\. ' .specify/memory/constitution.md` | **15** |
| 命令 `MUST include` 条目数 | `grep -c 'MUST include' templates/commands/constitution.md` | **7** |
| 活动宪章版本 | `grep -n '^\*\*Version\*\*' .specify/memory/constitution.md` | **1.12.0**(`:254`) |
| 门控扫描 total | `python3 scripts/python/scan-confirmation-gates.py` | **23**(destructive 13 / governance_kept 10 / violations 0) |
| `len(BLOCKING_PATTERNS)` | importlib 载入后取真 | **17** |
| `len(POLICY_DOCS)` | 同上 | **2** |
| 出厂 Agent 预设份数 | `ls -1 agents/*.agent.md \| wc -l` | **2** |
| Per-Agent Payload 字段行数 | awk 取表区间后数 `^\| \`` | **5** |
| 子句定界符在框架目录的命中文件数 | `grep -rIl 'fast-fail-clause:begin' templates shared skills agents` | **0** |
| `fast-fail-clause` 在框架目录的出现次数 | `grep -rIo 'fast-fail-clause' templates shared skills agents` | **0** |
| 清单条目语法 `FF-n` / `RP-n` 命中 | `grep -rIo '^- \*\*FF-[0-9]' …` | **0 / 0** |
| `[fast-fail]` 标记的反馈条目检索 | `feedback-utils.py --action list --contains "[fast-fail]" --format json` | **`count: 0` / `matches: []`**(实际输出为多行 pretty-printed JSON,此处记其值而非字面排版) |
| UFC 类映射表行数 / 去重规则真源路径数 | 解析该表,**按「规则真源」列取路径**(口径同 `test_user_facing_comprehension_doc.py:394-397`;若按整行取则得 9,口径不同不可混用) | **11 行 / 8 个** |
| UFC 类 ⑪ 行 | 同上 | `\| ⑪ \| 失败如实报告 \| \`shared/guidelines/confirmation-gates.md\` \| — \|` |
| `test_user_facing_comprehension_doc.py` 的 C-14 钉子 | `grep -n 'len(deduped) == 8'` | **`:400`** |
| 双落点四钉 | `grep -n 'TEMPLATE_COUNT = \|LIVE_COUNT = \|COMMAND_COUNT = \|MIN_VERSION = '` | **`:65` 13 / `:66` 15 / `:67` 7 / `:68` (1, 12)** |
| `sync-mirrors.py --check --only shared` | 实跑 | **EXIT=2**,恰 2 条 DIFF(`feedback-step.md`、`runtime-mode.md`) |
| `sync-mirrors.py --check --only agents` | 实跑 | **`ok  agents/ == .specify/agents/templates/ (2 files)`** |
| 活动指令文件字节数 / 预算 | `wc -c` / `generate-instructions.sh:38` | **28168 / 32768**(余量 4600) |

---

## 场景 1 — 真源文档存在且与镜像逐字节相等(US2 / SC-003)

**改前基线(已实跑)**:
```bash
cd /storage/project/cloud-native-ai/spec-kit
ls -1 shared/guidelines/*.md | wc -l
ls shared/guidelines/fast-fail.md
```
**期望**:份数 = **12**;第二条报 `No such file or directory`(制品尚未创建)。

**改后期望(改前不可实跑——依赖 `fast-fail.md`)**:
```bash
cd /storage/project/cloud-native-ai/spec-kit
ls -l shared/guidelines/fast-fail.md .specify/shared/guidelines/fast-fail.md
cmp shared/guidelines/fast-fail.md .specify/shared/guidelines/fast-fail.md && echo "BYTE-IDENTICAL"
ls -1 shared/guidelines/*.md | wc -l
```
**期望**:两个文件均存在;输出 `BYTE-IDENTICAL`(`cmp` 静默即相等);份数 = **13**(12 + 1)。

> *改前可实跑的等价基线是份数 = 12;改后判据为 13 且 `cmp` 静默。该场景由 `discipline-doc.md` C-1 / C-2 钉住。*

---

## 场景 2 — 常驻章节各出现一次且位置合法(US2 / SC-004)

**改前基线(已实跑)**:
```bash
cd /storage/project/cloud-native-ai/spec-kit
grep -c '^## ' templates/instructions-template.md
grep -c '^## ' .specify/instructions.md
grep -c '^## Fast Fail Discipline' templates/instructions-template.md .specify/instructions.md
grep -n '^## Token Efficiency Discipline\|^## User-Facing Comprehension\|^## Dogfooding Practice' templates/instructions-template.md
```
**期望**:**18** / **19** / 两处各 **0**(章节尚不存在)/ 三个锚点在 **66 / 74 / 86**。

**改后期望(改前不可实跑——依赖新章节与再生)**:
```bash
cd /storage/project/cloud-native-ai/spec-kit
grep -c '^## Fast Fail Discipline' templates/instructions-template.md .specify/instructions.md
grep -n '^## Token Efficiency Discipline\|^## User-Facing Comprehension\|^## Fast Fail Discipline\|^## Dogfooding Practice' templates/instructions-template.md
grep -c '^## ' templates/instructions-template.md; grep -c '^## ' .specify/instructions.md
grep -c 'shared/guidelines/fast-fail.md' templates/instructions-template.md
```
**期望**:两处各 **1**(各出现且仅出现一次);四个标题的行号**严格递增**且 `Fast Fail` 落在 `User-Facing Comprehension` 与 `Dogfooding Practice` 之间;节数 **19** / **20**;指针行 **1**。

> *位置判据由 `ambient-section.md` C-5 钉住,其依据是既有 `test_user_facing_comprehension_section.py:207-218` 断言的是**严格排序**而非相邻——插入本节不破坏该钉子。改后 MUST 实跑既有 `test_c7` / `test_c8` 确认二者仍绿。*

---

## 场景 3 — 宪章双落点与四钉同批上调(US3 / SC-006)

**改前基线(已实跑)**:
```bash
cd /storage/project/cloud-native-ai/spec-kit
grep -c '^### [IVX]*\. ' templates/constitution-template.md
grep -c '^### [IVX]*\. ' .specify/memory/constitution.md
grep -c 'MUST include' templates/commands/constitution.md
grep -n '^\*\*Version\*\*' .specify/memory/constitution.md
grep -n 'TEMPLATE_COUNT = \|LIVE_COUNT = \|COMMAND_COUNT = \|MIN_VERSION = ' tests/contract/test_constitution_double_landing.py
grep -c 'Fast Fail' templates/constitution-template.md templates/commands/constitution.md
```
**期望**:**13** / **15** / **7** / `:254` **1.12.0** / 四钉在 `:65,66,67,68` 值为 `13 / 15 / 7 / (1, 12)` / 两处各 **0**。

**改后期望(改前不可实跑——依赖新原则)**:
```bash
cd /storage/project/cloud-native-ai/spec-kit
grep -c '^### [IVX]*\. ' templates/constitution-template.md
grep -c '^### [IVX]*\. ' .specify/memory/constitution.md
grep -c 'MUST include' templates/commands/constitution.md
grep -n '^\*\*Version\*\*' .specify/memory/constitution.md
grep -c 'Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest)' templates/constitution-template.md templates/commands/constitution.md
awk '/^### XIV\./,/^## \[SECTION_2_NAME\]/' templates/constitution-template.md | awk 'length > 99 {n++} END {print "over-100-char lines:", n+0}'
python3 -m pytest tests/contract/test_constitution_double_landing.py -q 2>&1 | tail -3
```
**期望**:**14** / **16** / **8** / 版本 **1.13.0** / 两处各 **1**(双落点标题逐字一致)/ 超长行 **0** / pytest 全绿。

> *`plan-template.md` MUST 零改动而下游 plan 门控行数由 15 增至 16(动态枚举);其零改动由 `constitution-export.md` C-16 钉住,并配 C-17 的反空真哨兵。*

---

## 场景 4 — 门控预算中立(US6 / SC-005)

**改前基线(已实跑)**:
```bash
cd /storage/project/cloud-native-ai/spec-kit
python3 scripts/python/scan-confirmation-gates.py
python3 - << 'PY'
import importlib.util
s=importlib.util.spec_from_file_location("m","scripts/python/scan-confirmation-gates.py")
m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
print("BLOCKING_PATTERNS:", len(m.BLOCKING_PATTERNS))
print("POLICY_DOCS:", [str(p) for p in m.POLICY_DOCS])
print("SELF_REL:", str(m.SELF_REL))
PY
git diff --stat -- scripts/python/scan-confirmation-gates.py
```
**期望**:`total` **23** / destructive **13** / governance_kept **10** / violations **0**;`BLOCKING_PATTERNS:` **17**;`POLICY_DOCS:` 恰两项(`shared/patterns/reconcile-pattern.md`、`shared/patterns/interview-pattern.md`);`SELF_REL:` `shared/guidelines/confirmation-gates.md`;`git diff --stat` 输出**为空**。

**改后期望(改前即可实跑,且不依赖新制品)**:
```bash
cd /storage/project/cloud-native-ai/spec-kit
python3 scripts/python/scan-confirmation-gates.py
python3 - << 'SCANPY'
import json, subprocess
frozen = json.load(open(".specify/specs/050-proactive-flow-trigger/baseline-gates.json"))["confirmationGates"]["total"]
out = subprocess.run(["python3", "scripts/python/scan-confirmation-gates.py", "--json"], capture_output=True, text=True).stdout
p = json.loads(out)
print("frozen:", frozen, "live:", p["total"], "violations:", len(p["violations"]))
print("TOTAL-EQUAL" if p["total"] == frozen and not p["violations"] else "FAIL")
SCANPY
git diff --stat -- scripts/python/scan-confirmation-gates.py
python3 -m pytest tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged -q 2>&1 | tail -2
```
**期望**:`total` 仍为 **23**(相等,非 ≤)、violations **0**;第二段输出 `frozen: 23 live: 23 violations: 0` 与 **`TOTAL-EQUAL`**;`git diff --stat` 仍**为空**;该测试 **passed**。

> ⚠️ **`--baseline` 旗标 MUST NOT 用作相等判据(实现期变异演练实证,2026-09-23)**。本场景初版印的是 `scan-confirmation-gates.py --baseline <050 基线>; echo "EXIT=$?"` 并期望 `EXIT=0`。实测该形式**双重失明**:① 旗标读基线文件的**顶层** `total` 键,而 050 基线把该值嵌在 `confirmationGates` 之下,故其 `baseline delta total` 恒为 `+23`(实为与 `0` 相比);② 其退出码逻辑是 `if args.baseline and violations: return 2`——**只反映 violations,完全不反映 total**。变异演练:把冻结值改成 `99` 后,`--baseline` 形式仍 `EXIT=0`,而上面第二段的直接比较正确报 `FAIL`。该旗标的这两个缺陷属**上游**(`scripts/` 在本特性零改动面内),MUST 单独上报,MUST NOT 由本特性改写扫描器。

> *本场景是全部场景中唯一"改后判据在改前即可完整实跑"的一个——因为它的判据是**不变量**(total 相等、扫描器零改动)。这也是它最危险的地方:新增文本里任何一行命中即 +1,同时打爆 `gate-neutrality.md` C-10 枚举的全部既有钉子(其位置与形态由该条单点拥有,本行不重抄)。两类必踩陷阱见 `gate-neutrality.md` C-6 / C-7。*

---

## 场景 5 — 注入子句:一份拥有者、两份字节相等的副本(US4 / SC-011)

**改前基线(已实跑)**:
```bash
cd /storage/project/cloud-native-ai/spec-kit
ls -1 agents/*.agent.md | wc -l
awk '/^Per-Agent Payload:/,/^Context Isolation Rules:/' skills/create-team/references/patterns.md | grep -c '^| `'
grep -rIl 'fast-fail-clause:begin' templates shared skills agents 2>/dev/null | wc -l
```
**期望**:预设 **2**;载荷字段行 **5**;定界符命中文件数 **0**。

**改后期望(改前不可实跑——依赖子句与三处落点)**:
```bash
cd /storage/project/cloud-native-ai/spec-kit
grep -c 'fast-fail-clause:begin' shared/guidelines/fast-fail.md
grep -c 'fast-fail-clause:begin' agents/skill-verifier.agent.md agents/structure-adjuster.agent.md
python3 - << 'PY'
import pathlib, re
def clause(p):
    t = pathlib.Path(p).read_text(encoding="utf-8")
    m = re.search(r"<!-- fast-fail-clause:begin -->(.*?)<!-- fast-fail-clause:end -->", t, re.S)
    return m.group(1) if m else None
owner = clause("shared/guidelines/fast-fail.md")
print("owner lines/bytes:", len(owner.splitlines()), len(owner.encode()))
for p in ("agents/skill-verifier.agent.md", "agents/structure-adjuster.agent.md"):
    print(p, "byte-identical:", clause(p) == owner)
PY
awk '/^Per-Agent Payload:/,/^Context Isolation Rules:/' skills/create-team/references/patterns.md | grep -c '^| `'
cmp agents/skill-verifier.agent.md .specify/agents/templates/skill-verifier.agent.md && echo "MIRROR-OK"
```
**期望**:拥有者文件中定界符 **1** 对;两份预设各 **1** 对;`owner lines/bytes` ≤ **10 / 1200**(实测草稿为 8 / 933);两行 `byte-identical: True`;载荷字段行 **6**(5 + 1);`MIRROR-OK`。

> *⚠️ 载荷字段行的 **6** 是本特性落地时点(2026-09-23)的值。2026-09-24 复核:该表此后由**本特性之外**的改动增入 `incremental_landing` 一行,今实测为 **7**;守卫 `test_i13` 已同批把钉子改为 7 并要求 `fast_fail_clause` 与 `incremental_landing` 两行同时在场(故本场景的判据仍绿,只是行数的拥有者已是该守卫而非本行)。*

> *副本属"守卫钉死的合法重复",**不是**机器可再生副本——无引擎会再生 `patterns.md` 或 `.agent.md`(`research.md` D-9)。故字节相等的修复路径是从拥有者手工重灌,由 `dispatch-injection.md` C-10 / V2 断言。*

---

## 场景 6 — 派发前自检的变异演练(US4 / SC-012)

本场景是**行为类**义务的取证(通道一的内联提示不落盘,无契约测试可断言),故 MUST 以变异演练取证,而不是"当前树上通过"。

**演练对象是通道一的 outgoing 提示**(编排者当场撰写、即将发出的那一份),**不是**通道二的 Agent 定义制品——`dispatch-injection.md` C-24 第 1 行指定的是前者。演练的是**检测逻辑**(子句标识在不在),而非"自检发生在派发之前"这一**时序**属性:时序属程序性义务,由真源文档载明 + 评审强制(FR-062),本场景 MUST NOT 声称已证明它。

**改前基线(已实跑)**:
```bash
cd /storage/project/cloud-native-ai/spec-kit
grep -rIo 'fast-fail-clause' templates shared skills agents 2>/dev/null | wc -l
```
**期望**:**0**(框架目录中该字面量尚不存在,故演练今天无对象)。

**改后期望(改前不可实跑——依赖子句)**:
```bash
cd /storage/project/cloud-native-ai/spec-kit
# 0) 从拥有者取出子句,写入一份模拟的 outgoing 提示(通道一形态)
mkdir -p /tmp/ffdrill
python3 - << 'INNER'
import pathlib, re
owner = pathlib.Path("shared/guidelines/fast-fail.md").read_text(encoding="utf-8")
clause = re.search(r"<!-- fast-fail-clause:begin -->.*?<!-- fast-fail-clause:end -->", owner, re.S).group(0)
prompt = f"你是一名只读检测代理。任务:审计 X 并回传发现。\n\n{clause}\n"
pathlib.Path("/tmp/ffdrill/outgoing-prompt.md").write_text(prompt, encoding="utf-8")
print("prompt bytes:", len(prompt.encode()))
INNER
# 1) 反空真哨兵:自检 MUST 先证明它能找到子句
grep -c 'fast-fail-clause' /tmp/ffdrill/outgoing-prompt.md
# 2) 弄坏被守物:移除子句标识,再跑同一条自检
sed -i 's/fast-fail-clause/REDACTED-probe/g' /tmp/ffdrill/outgoing-prompt.md
grep -c 'fast-fail-clause' /tmp/ffdrill/outgoing-prompt.md    # 期望 0 —— 自检 MUST 报缺失,派发 MUST NOT 发出
# 3) 复原并确认恢复
python3 -c "import pathlib,re;o=pathlib.Path('shared/guidelines/fast-fail.md').read_text(encoding='utf-8');c=re.search(r'<!-- fast-fail-clause:begin -->.*?<!-- fast-fail-clause:end -->',o,re.S).group(0);p=pathlib.Path('/tmp/ffdrill/outgoing-prompt.md');p.write_text(p.read_text(encoding='utf-8').replace('REDACTED-probe','fast-fail-clause'),encoding='utf-8');print('restored')"
grep -c 'fast-fail-clause' /tmp/ffdrill/outgoing-prompt.md    # 期望 ≥1 —— 自检 MUST 通过
# 4) 删净演练制品并复核计数归零
rm -rf /tmp/ffdrill; ls /tmp/ffdrill 2>&1 | tail -1
```
**期望**:步骤 0 输出 `prompt bytes: <非零>`;步骤 1–4 依次为 **≥1 → 0 → `restored` 且 ≥1 → `No such file or directory`**;演练目录计数归零。

> *步骤 2 的"0"与步骤 4 的"No such file"都是**负面命题**,故本场景自身 MUST 配反空真哨兵:步骤 1 的 ≥1 就是它——若步骤 1 也是 0,则步骤 2 的 0 不证明自检能发现缺失,只证明演练对象本来就没有子句。*
>
> *步骤 0 从**拥有者**取子句而非从通道二制品取,是因为通道一提示的内容来源就是拥有者字面量;若改从 `agents/*.agent.md` 取,演练的将是通道二,与 C-24 第 1 行指定的对象不符(该缺陷在本计划的质量门中被查出并已订正)。*

---

## 场景 7 — 两份清单的条目语法与 7 项点名覆盖(US1 / SC-002)

**改前基线(已实跑)**:
```bash
cd /storage/project/cloud-native-ai/spec-kit
grep -rIo '^- \*\*FF-[0-9]' templates shared skills 2>/dev/null | wc -l
grep -rIo '^- \*\*RP-[0-9]' templates shared skills 2>/dev/null | wc -l
```
**期望**:**0 / 0**(两份清单尚不存在)。

**改后期望(改前不可实跑——依赖两份清单)**:
```bash
cd /storage/project/cloud-native-ai/spec-kit
grep -cE '^- \*\*(FF|RP)-[0-9]+ ' shared/guidelines/fast-fail.md
grep -cE '^- \*\*(FF|RP)-[0-9]+ .*判据:' shared/guidelines/fast-fail.md
for n in 2 3 4 5 6 7 8; do printf 'FF-%s: ' "$n"; grep -c "^- \*\*FF-$n " shared/guidelines/fast-fail.md; done
```
**期望**:第一条 ≥ **15**(FF 侧 ≥9 + RP 侧 ≥6);第二条与第一条**相等**(每条都携判据);`FF-2`…`FF-8` 七项各 **1**(盲检四成因 + `git diff` 三形态逐项可定位)。

> *两条计数相等是 FR-076 的机械化:若第二条小于第一条,则有清单条目缺判据,"每条携判据"就退化成了"该节非空"——那正是 STR-006 禁止的空转断言。清单总条数**不设钉子**(可生长),但点名的 7 项 MUST 逐项可定位。*

---

## 场景 8 — 观察标记可检索,且三个标记互不为子串(US5 / SC-007)

**改前基线(已实跑)**:
```bash
cd /storage/project/cloud-native-ai/spec-kit
python3 .specify/scripts/python/feedback-utils.py --action list --contains "[fast-fail]" --format json
python3 - << 'PY'
lit = {"obs":"[fast-fail]", "clause":"fast-fail-clause", "ret":"ANOMALY:", "path":"shared/guidelines/fast-fail.md"}
ks=list(lit); bad=[(a,b) for i,a in enumerate(ks) for b in ks[i+1:] if lit[a] in lit[b] or lit[b] in lit[a]]
print("substring violations:", bad if bad else "none")
PY
```
**期望**:`{"count": 0, "matches": []}`(尚无带该标记的条目);`substring violations: none`。

**改后期望(第一条改前不可实跑——依赖一条带标记的条目;第二条改前即可实跑)**:
```bash
cd /storage/project/cloud-native-ai/spec-kit
# 演练 MUST 在一次性 workspace 中进行,绝不写入真实存据
rm -rf /tmp/ffdrill && mkdir -p /tmp/ffdrill
python3 .specify/scripts/python/feedback-utils.py --action record --workspace-root /tmp/ffdrill \
  --unit-id "/speckit.plan" --unit-type command --run-id "drill:marker:$(date -u +%Y%m%dT%H%M%SZ)" \
  --feature "052-fast-fail-principle" \
  --review "[fast-fail] 演练条目:验证标记可被检索。" --points "演练用"
python3 .specify/scripts/python/feedback-utils.py --action list --workspace-root /tmp/ffdrill \
  --contains "[fast-fail]" --format json | head -5
# 反空真哨兵:真实存据 MUST 未被污染
python3 .specify/scripts/python/feedback-utils.py --action list --contains "[fast-fail]" --format json | head -4
# 清理:移除一次性 workspace,并复核其不存在
rm -rf /tmp/ffdrill; ls /tmp/ffdrill 2>&1 | tail -1
```
**期望**:`record` 返回一个 `id` 与 `path`;一次性 workspace 内 `list` 的 `count` ≥ **1**;**真实存据仍为 `{"count": 0, "matches": []}`**(即改前基线未被污染);末行 `No such file or directory`。

> *⚠️ **MUST NOT 用 `--action cleanup` 清理演练条目**:实测该 action 要求 `--package <zip|latest>`(`scripts/python/feedback-utils.py:1390` `raise FeedbackError("--package <zip-path|latest> is required.")`),其作用域严格限于**已打包**的批次;一条未打包的演练条目会让它抛错。`--action dispose` 亦不适用——它只翻元数据,`body never rewritten`,条目文件仍在。本计划初版曾开出这条不可用的清理命令,若不订正,照它执行会把一条演练条目**永久留在真实存据里**,从而**伪化本文件基线总表第 18 行的 `count: 0`**,让下一个执行者撞上一条他自己没造成的基线冲突。故改为 `--workspace-root` 隔离:该形态已于 2026-09-23 实跑验证(一次性根内 `count: 1`、真实存据仍 `count: 0`、`rm -rf` 后目录不存在)。*
>
> ***第二条(互斥性)是纯字符串运算,不依赖任何制品**,故它在 red-first 阶段即可断言——这是 `discipline-doc.md` C-20 特意选它作首条可断言条款的原因。*

---

## 场景 9 — 类 ⑪ 登记与 Feature 051 的钉子上调(跨纪律 / SC-003)

**改前基线(已实跑)**:
```bash
cd /storage/project/cloud-native-ai/spec-kit
grep -n '^| ⑪ |' shared/guidelines/user-facing-comprehension.md
grep -n 'len(deduped) == 8' tests/contract/test_user_facing_comprehension_doc.py
python3 -m pytest tests/contract/test_user_facing_comprehension_doc.py -q 2>&1 | tail -2
```
**期望**:类 ⑪ 行为 `| ⑪ | 失败如实报告 | \`shared/guidelines/confirmation-gates.md\` | — |`;钉子在 **`:400`**;pytest 全绿(改前基线)。

**改后期望(改前不可实跑——依赖登记与上调)**:
```bash
cd /storage/project/cloud-native-ai/spec-kit
grep -n '^| ⑪ |' shared/guidelines/user-facing-comprehension.md
grep -n 'len(deduped) == 9' tests/contract/test_user_facing_comprehension_doc.py
grep -c 'fast-fail.md' shared/guidelines/user-facing-comprehension.md
grep -n '^| ⑪ |' shared/guidelines/user-facing-comprehension.md | grep -c '—'
python3 -m pytest tests/contract/test_user_facing_comprehension_doc.py -q 2>&1 | tail -2
```
**期望**:类 ⑪ 行的规则真源列**同时含** `confirmation-gates.md` 与 `fast-fail.md`;钉子上调为 **9**;`fast-fail.md` 在该文件命中 **1**;`reader_baseline_override` 列仍为 `—`(故 `test_c18a` 的上限 2 不受影响);pytest 全绿。

> *这是本特性对 Feature 051 拥有制品的**唯一**改动,已由 `constitution-export.md` C-19…C-23 显式列为跨纪律改动并在四处留痕(plan.md › Feature List Review、feature-ref.md、`features/051.md`、`features/052.md`)。MUST NOT 默默发生。*

---

## 场景 10 — 回传缺异常行被判为不完整(US4 / SC-013 编排者侧)

`dispatch-injection.md` C-24 第 2 行要求的演练。构造三种回传,断言分类逻辑把第三种判为**不完整**而非干净。

**改前基线(已实跑)**:
```bash
cd /storage/project/cloud-native-ai/spec-kit
grep -rIo 'ANOMALY:' templates shared skills agents 2>/dev/null | wc -l
```
**期望**:**0**(该前缀在框架目录尚不存在)。

**改后期望(改前不可实跑——依赖判据文本)**:
```bash
cd /storage/project/cloud-native-ai/spec-kit
mkdir -p /tmp/ffdrill && python3 - << 'INNER'
import pathlib, re
doc = pathlib.Path("shared/guidelines/fast-fail.md").read_text(encoding="utf-8")
PREFIX, CLEAN = "ANOMALY:", "未发现异常"
def classify(ret: str) -> str:
    if any(l.startswith(PREFIX) for l in ret.splitlines()): return "anomaly-halt"
    if any(CLEAN in l for l in ret.splitlines()):            return "clean"
    return "incomplete"
cases = {
  "有异常":   "任务完成。\nANOMALY: 前提被证伪 —— 计数实测为 9 而非 5。",
  "无异常":   "任务完成。未发现异常。",
  "缺异常行": "任务完成。",
  "行内提及": "任务完成。子代理被要求以 `ANOMALY:` 前缀回传。",
}
for k, v in cases.items(): print(f"{k}: {classify(v)}")
print("doc carries the rule:", PREFIX in doc and CLEAN in doc)
INNER
rm -rf /tmp/ffdrill; ls /tmp/ffdrill 2>&1 | tail -1
```
**期望**:四例依次为 **anomaly-halt / clean / incomplete / clean-or-incomplete 中判为 incomplete 者不得为 clean**;末行 `doc carries the rule: True`;`No such file or directory`。

> *第四例「行内提及」是 FR-063 / D-6 的判据落点:前缀出现在**行内反引号引用**里,MUST NOT 被判为异常停——这正是"行首锚定"而非"全文子串"的理由。若该例被判为 `anomaly-halt`,说明判据写成了子串匹配,C-20 的互斥要求已被违反。*
> *`doc carries the rule: True` 是本场景的反空真哨兵:若它为 False,则前三例的分类结果只证明了演练脚本自己的逻辑,与本纪律无关。*

---

## 场景 11 — 异常停 MUST NOT 被原样重派(US4 / SC-014)

`dispatch-injection.md` C-24 第 3 行要求的演练。

**改前基线(已实跑)**:
```bash
cd /storage/project/cloud-native-ai/spec-kit
grep -c '异常停' shared/guidelines/*.md 2>/dev/null | grep -v ':0' || echo "(no guideline mentions it yet)"
```
**期望**:`(no guideline mentions it yet)`(真源文档尚不存在)。

**改后期望(改前不可实跑)**:
```bash
cd /storage/project/cloud-native-ai/spec-kit
python3 - << 'INNER'
import pathlib
doc = pathlib.Path("shared/guidelines/fast-fail.md").read_text(encoding="utf-8")
ALLOWED = {"surface-to-user", "record-as-pending"}
FORBIDDEN = {"re-dispatch", "retry-as-is"}
def next_action(ret: str) -> str:
    return "surface-to-user" if any(l.startswith("ANOMALY:") for l in ret.splitlines()) else "consume"
a = next_action("ANOMALY: 前提被证伪。")
print("next action:", a, "| allowed:", a in ALLOWED, "| forbidden:", a in FORBIDDEN)
# 三条被排除的既有失败规则 MUST 在真源文档中被点名
for needle in ("两振", "派发失败", "非并行"):
    print(f"doc names {needle!r}:", needle in doc)
INNER
```
**期望**:`next action: surface-to-user | allowed: True | forbidden: False`;三条 `doc names …: True`(FR-071 要求排除覆盖既有的**全部**失败规则,故三者都 MUST 被点名)。

> *三个 `doc names` 断言是本场景的反空真哨兵:若真源文档没有点名这三条规则,则"异常停不算失败"在既有规则面前就没有落点,演练脚本的 `ALLOWED` 集合只是它自己的发明。*

---

## 场景 12 — 干净运行也显式说一句(US2 / SC-009)

`dispatch-injection.md` C-24 第 4 行要求的演练。

**改前基线(已实跑)**:
```bash
cd /storage/project/cloud-native-ai/spec-kit
grep -rIo '未发现异常' templates shared skills 2>/dev/null | wc -l
```
**期望**:**0**。

**改后期望(改前不可实跑)**:
```bash
cd /storage/project/cloud-native-ai/spec-kit
python3 - << 'INNER'
import pathlib
doc = pathlib.Path("shared/guidelines/fast-fail.md").read_text(encoding="utf-8")
MARK = "未发现异常"
def wrapup(repairs: int, fails: int) -> str:
    if repairs == 0 and fails == 0: return f"{MARK},无就地修复。"
    return f"本轮 {repairs} 处顺手修复、{fails} 次快速失败(逐项见下)。"
for r, f in ((0, 0), (2, 0), (0, 1)):
    line = wrapup(r, f)
    print(f"repairs={r} fails={f} -> explicit-statement-present: {MARK in line}")
print("doc owns the literal:", MARK in doc)
INNER
```
**期望**:三行依次为 **True / False / False**(只有干净运行需要该显式陈述);`doc owns the literal: True`。

> *第一行的 True 与第二、三行的 False **合起来**才是判据:若三行全为 True,说明该陈述被无条件加上,它对"干净"就没有判别力;若全为 False,说明义务根本没落地。`doc owns the literal` 是反空真哨兵。*

---

## 场景覆盖表

| 场景 | US | SC | 契约条款 | 改前可实跑? |
|---|---|---|---|---|
| 1 真源文档与镜像 | US2 | SC-003 | discipline-doc C-1, C-2 | 基线可,判据不可 |
| 2 常驻章节与位置 | US2 | SC-004 | ambient-section C-1…C-7 | 基线可,判据不可 |
| 3 宪章双落点 | US3 | SC-006 | constitution-export C-1…C-18 | 基线可,判据不可 |
| 4 门控预算中立 | US6 | SC-005 | gate-neutrality C-1…C-11 | **全部可**(判据是不变量) |
| 5 注入子句与副本 | US4 | SC-011 | dispatch-injection C-1…C-14 | 基线可,判据不可 |
| 6 派发前自检演练 | US4 | SC-012 | dispatch-injection C-24, C-25 | 基线可,演练不可 |
| 7 清单语法与 7 项 | US1 | SC-002 | discipline-doc C-13…C-15 | 基线可,判据不可 |
| 8 标记检索与互斥 | US5 | SC-007 | discipline-doc C-18, C-20 | **互斥性可**(纯字符串运算) |
| 9 类 ⑪ 登记 | 跨纪律 | SC-003 | constitution-export C-19…C-23 | 基线可,判据不可 |
| 10 缺异常行判为不完整 | US4 | SC-013(编排者侧) | dispatch-injection C-20, C-24 | 基线可,判据不可 |
| 11 异常停不被重派 | US4 | SC-014 | dispatch-injection C-21, C-24 | 基线可,判据不可 |
| 12 干净运行显式陈述 | US2 | SC-009 | discipline-doc C-17(d);dispatch-injection C-24 | 基线可,判据不可 |

**未被 quickstart 覆盖的 SC 及其取证方式**:SC-001(双评审者一致性)与 SC-008(读者测试)要求**未参与本特性实现的评审者**,单会话不可得,由实现期的独立子代理评审取证(051 对同类 SC 记为 `[~]` 的先例);SC-013 的子代理侧与 SC-015 的三个数为**度量而非门禁**,由实跑聚合记入报告,不设通过阈值;SC-014(异常停不被重派)为行为类,由**场景 11** 取证;SC-013 的编排者侧由**场景 10** 取证;SC-009 的干净运行显式陈述由**场景 12** 取证。四者合起来满足 `dispatch-injection.md` C-24 要求的四条演练(初版只有场景 6 一条,该缺口在本计划的质量门中被查出并已补齐)。
