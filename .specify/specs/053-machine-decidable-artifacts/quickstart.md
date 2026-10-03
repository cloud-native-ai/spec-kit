# Quickstart: 机器可判定的制品命题(Machine-Decidable Artifact Propositions)

**Requirement**: `053-machine-decidable-artifacts` → Feature 053  
**Date**: 2026-10-02  
**用途**:给 `/speckit.tasks` 与 `/speckit.implement` 一份**可照跑**的验证剧本。每个场景标注它是**改前可实跑**(本轮已实跑,真实输出已粘贴)还是**改前不可实跑**(依赖尚未创建的制品;逐例给出所依赖的前提,使实现者知道该**重测**哪些事实而不是继承它们)。

**免责形态说明**:本文件**不使用**文件级免责声明。凡未实跑的例子,其免责与前提清单**逐例**写在该例子正下方。凡已实跑的例子,粘贴的是本轮真实输出,不是预期值。

**通用约束**:破坏副本与演练产物 MUST 建在临时目录(`mktemp -d`),MUST NOT 落在 `.specify/specs/` 下;每个场景的清理步骤与建立步骤同标准核验(场景 12)。

---

## 场景 1: 改前基线采集(四组)——**改前可实跑,本轮已实跑**

四组基线在实现开工时冻结并落盘本特性目录(D-18、C-21/C-23 of `neutrality-budget.md`)。

```bash
# 1a 全量测试的名字级失败集(SC-012)
bash .specify/scripts/bash/run-tests.sh --names-out <spec-dir>/baseline-failed.txt -q tests/

# 1b 门控 total(FR-045 / SC-012)
python3 scripts/python/scan-confirmation-gates.py --summary

# 1c 条款形态普查(FR-022 / SC-006)——分类器见 notes/clause-form-census.md
python3 - <<'PY'
import glob, re, collections
c = collections.Counter()
for p in glob.glob('.specify/specs/*/contracts/*'):
    s = open(p, encoding='utf-8', errors='replace').read()
    if p.endswith(('.yaml', '.yml')):
        c['yaml-openapi' if ('openapi:' in s and 'paths:' in s)
          else 'yaml-assertions' if re.search(r'^\s+- id:', s, re.M) else 'yaml-other'] += 1
    else:
        b = bool(re.search(r'\*\*C-\d+(?:\.\d+)*\*\*', s))
        o = bool(re.search(r'\*\*C-\d+', s))
        h = bool(re.search(r'^#{1,6}\s+C-\d+', s, re.M))
        c['md-bold-closed' if b else 'md-bold-paren' if o else 'md-heading' if h else 'md-none'] += 1
print(sum(c.values()), dict(c))
PY

# 1d goal 与 teams 的字节校验和(FR-034 / SC-007)
find .specify/goal .specify/teams -type f | sort | xargs sha256sum | sha256sum
```

**本轮真实输出**

- **1b**:`blocking confirmation gates: 23` / `destructive: 13` / `governance_kept: 10` / `violations (reversible gates still blocking): 0`
- **1c**(实跑两次:**2026-09-24** 于本特性 `contracts/` 落盘前、**2026-10-02** 于落盘后;值随本特性自己的契约落盘而变——这正是场景 6 要守的命题):
  - 在本特性 `contracts/` 落盘**之前**:`110 {'md-bold-closed': 21, 'md-heading': 25, 'md-none': 53, 'yaml-openapi': 9, 'yaml-assertions': 1}`(21+25+53+9+1 = **110** ✓)
  - 落盘**之后**(同一命令):文件数 `117`,差值恰为 **+7 文件**,即本特性自己的 7 份契约;**条款 id 的差值 MUST NOT 在此写死**——它随本特性契约的每次编辑而变(写作本行时为 +182),需要时现场跑 `notes/clause-form-census.md` 的命令
  ⇒ **冻结基线时 MUST 记下 as-of**(哪个提交之前/之后),否则「110」与「117」两个都对而互相矛盾。两个值均由 `notes/clause-form-census.md` 拥有。
- **1d**:`751e5df220adef18c79b1aa3…`;`.specify/goal/` 下 **1** 个 goal 目录、`.specify/teams/` 下 **7** 个目录(6 个团队 + `.work/`)
- **1a**(本轮在 `/speckit.clarify` 收尾时实跑,可作改前参考值,**实现开工时 MUST 重新冻结**):`65 failed, 2927 passed, 2 skipped`,名字集 65 行,与 052 冻结基线 md5 相同(`02177c0e6e5961c880f73d932007df92`)

---

## 场景 2: FR-014 债务的改前状态与偿清判据——**改前可实跑,本轮已实跑**

```bash
t=shared/constants/clarify-taxonomy.md
grep -c 'ORDER BREAK: %s after %s' $t        # 过渡 awk 块的判别式
grep -c 'Until that validator ships' $t      # 待删的句子
grep -c 'shares one implementation' $t       # 被 test_c4 :338 钉住的措辞
```

**本轮真实输出**:`1` / `1` / `1`

**偿清后的判据**(US1 落地时):第 1、2 项 MUST 变为 **0**;第 3 项 MUST **仍 ≥ 1** 但语义从「宣告将来共享」改为「指名现在共享的实现」(`requirements-checker.md` C-22…C-27)。

**注意——两个 awk 围栏块,只有一个是待删的**:`grep -n '```bash' $t` → `:100` 与 `:108`。`:100` 那块是「陈旧计数残留 grep」的示例,**不在** FR-014 范围内;待删的是 `:108-112`(文档序不变量的过渡抽取式)。裸 `grep -c 'awk'` 会给 **2**(awk 命令跨 `:109` 与 `:111` 两行),故 MUST 用上面的判别式而不是 `awk` 一词。

**同一提交内 MUST 改写的两个测试**(否则它们会红):

```bash
grep -n 'the interim extraction block is gone\|shares one implementation' \
  tests/contract/test_clarify_semantic_completeness.py
```

**本轮真实输出**:`324:` 与 `338:` 两处。`:324` 的断言消息逐字就是「the interim extraction block is gone from the document-order invariant」——即该测试**当前把过渡副本的在场当作通过条件**。

---

## 场景 3: US1 检查器对真实规格跑通 + 四份破坏副本——**改前不可实跑**

```bash
python3 scripts/python/validate-requirements.py .specify/specs/053-machine-decidable-artifacts/requirements.md
python3 scripts/python/validate-requirements.py <spec-dir>/requirements.md --json
```

> **本例改前不可实跑**——`validate-requirements.py` 尚不存在。所依赖的前提(实现时 MUST 逐条重测,MUST NOT 继承):
> - 脚本名与落点为 `scripts/python/validate-requirements.py`(D-4;标识符零碰撞已在规格现状锚点实测)
> - 入口形态为 `main(argv=None) -> int`,可被 `importlib` 载入直接调用(与 `validate-tasks.py:280` 同形)
> - 位置参数为**一个**制品路径;`--json` 为 `store_true`(与 `validate-tasks.py:289-291` 同形)
> - 检查项标签集为 5 项:`id-contiguous` / `doc-order` / `ref-resolvable` / `marker-count` / `dup-id`(D-5)
> - 退出码为 `0` 无 error / `1` ≥1 error / `2` 缺失或不可解析或无内容行;**无第四码**(D-6)
> - 消息前缀为 `<lineno>: <label>: `(与 `validate-tasks.py:140` 等同形)
> - `--json` 含逐项 verdict 数组(**新造**形态,先例只有 `file`/`errors`/`warnings`/`status` 四键)

**预期结果**(改后 MUST 实测并粘贴真实输出,不得沿用本行):对本规格跑,5 项检查全部执行、`0 error(s), 0 warning(s)`、exit **0**。

**四份破坏副本(SC-001 的 4/4 且零交叉遮蔽)**:每份只破坏一类命题,各自只报出对应那一类。

```bash
tmp=$(mktemp -d); src=.specify/specs/053-machine-decidable-artifacts/requirements.md
# 破坏 1:编号跳号(删掉 FR-030 的定义行)
# 2026-10-03 实现期订正:原先删 FR-023。实测 FR-023 被 FR-026 与 FR-028 两行**散文引用**,
# 删掉它的定义行会同时触发 ref-resolvable,即 SC-001 要求排除的「交叉遮蔽」——而该场景的
# 前提块此前只核过「缺号确实出现」,没核过「只有一类检查会报」。FR-030 经实测零散文引用。
grep -v '^- \*\*FR-030\*\*' $src > $tmp/b1.md
# 破坏 2:文档序(把 SC-002 的定义行移到 SC-005 之后)——可复跑的重排命令,不手改
python3 - "$src" "$tmp/b2.md" <<'REORDER_EOF'
import sys, re
src_lines = open(sys.argv[1], encoding='utf-8').read().split('\n')
row = next(l for l in src_lines if l.startswith('- **SC-002**'))
out = [l for l in src_lines if not l.startswith('- **SC-002**')]
i5 = next(i for i, l in enumerate(out) if l.startswith('- **SC-005**'))
out.insert(i5 + 1, row)
open(sys.argv[2], 'w', encoding='utf-8').write('\n'.join(out))
seq = [int(x) for x in re.findall(r'^- \*\*SC-(\d+)\*\*', '\n'.join(out), re.M)]
print("SC order:", seq, "ORDER BREAK:", [(a, b) for a, b in zip(seq, seq[1:]) if b < a])
REORDER_EOF
# 破坏 3:引用不可解析(把一个 [[STR-005]] 改成 [[STR-999]])
sed 's/\[\[STR-005\]\]/[[STR-999]]/' $src > $tmp/b3.md
# 破坏 4:活动标记(插入一个带冒号、未被反引号包裹的标记)
sed '0,/^## Overview/s//## Overview\n\n[NEEDS CLARIFICATION: probe]/' $src > $tmp/b4.md
for f in $tmp/b1.md $tmp/b2.md $tmp/b3.md $tmp/b4.md; do
  python3 scripts/python/validate-requirements.py "$f"; echo "EXIT=$?"
done
```

> **这四份破坏副本的构造命令本身改前即可实跑**(本轮已实跑),但**用检查器验证它们**改前不可实跑。构造命令所依赖的前提:被破坏的源文件是本规格自己的 `requirements.md`(48 FR / 12 SC 连续,故删掉 FR-030 的定义行恰好制造一个缺号;FR-030 经实测无任何散文引用,故 b1 只触发 `id-contiguous` 一类——原选的 FR-023 被两行散文引用,会同时触发 `ref-resolvable` 而构成交叉遮蔽);四份副本各自**只**含一类缺陷,本轮实跑复核为 `b1` FR 缺号 = `[30]`、`b2` SC 文档序 = `[1,3,4,5,2,6,…]` 且 `ORDER BREAK` 对 = `[(5,2)]`、`b3` 悬挂 `STR-999` = 1 处、`b4` 活动标记 = 1 个,四者互不污染——这正是 SC-001「4/4 且零交叉遮蔽」可被验证的前提。清理:`\rm -rf $tmp` 后残留计数 MUST 为 0(本轮实测 0)。

**预期结果**(检查器部分改后 MUST 实测并粘贴真实输出,MUST NOT 沿用本行):`b1` → `id-contiguous` 且 exit 1;`b2` → `doc-order`,输出 STR-002 形态的 `ORDER BREAK: SC-002 after SC-005`,exit 1;`b3` → `ref-resolvable` 点名 `STR-999` 与行号且 exit 1;`b4` → `marker-count` 报 1 且 exit 1(或按 D-6 的 verdict 表达);**每份只报出自己那一类**(零交叉遮蔽)。

---

## 场景 4: US2 的假告警——改前**即可复现**,改后 MUST 消失

这是本特性最有价值的一个场景:**改前就能实跑并看到缺陷**。

```bash
tmp=$(mktemp -d)
# 正样本对照:两行 [P] 写同一真实路径 → 必须 WARN(证明检查会触发)
cat > $tmp/pos.md <<'EOF'
# Tasks: probe
## Phase 1: Setup
- [ ] T001 [P] Write the thing in docs/a.md
- [ ] T002 [P] Write another thing in docs/a.md
EOF
# 假告警样本:两行 [P] 写不同文件,但 [green:] 指向同一契约
cat > $tmp/neg.md <<'EOF'
# Tasks: probe
## Phase 1: Setup
- [ ] T001 [P] Write the thing in docs/a.md [green: contracts/x.md#C-1]
- [ ] T002 [P] Write another thing in docs/b.md [green: contracts/x.md#C-2]
EOF
python3 scripts/python/validate-tasks.py $tmp/pos.md; echo "POS_EXIT=$?"
python3 scripts/python/validate-tasks.py $tmp/neg.md; echo "NEG_EXIT=$?"
\rm -rf $tmp; ls -d $tmp 2>/dev/null | wc -l
```

**本轮真实输出(改前)**

```text
POS: WARN  3: parallel-safe: [P] tasks T001 (line 3) and T002 (line 4) both WRITE ['docs/a.md']
     in phase `## Phase 1: Setup` — [P] requires different write targets; …
     PASS (with warnings): …/pos.md — 0 error(s), 1 warning(s)          POS_EXIT=0
NEG: WARN  3: parallel-safe: [P] tasks T001 (line 3) and T002 (line 4) both WRITE
     ['contracts/x.md'] in phase `## Phase 1: Setup` — …                ← 假告警
     PASS (with warnings): …/neg.md — 0 error(s), 1 warning(s)          NEG_EXIT=0
残留计数: 0
```

`docs/a.md` 与 `docs/b.md` 本不相同,告警点名的却是**标签内的契约路径**。机理见 `green-point-claim.md` C-21/C-23。

**改后判据**:`NEG` 的 `parallel-safe` 命中数 MUST 为 **0**,而 `POS` MUST **仍报** WARN——后者是反空真哨兵,证明修复没有把检查削弱掉。**MUST 先跑 POS 再判 NEG**:本特性 plan 期的第一次探针让 T001 漏掉 `[P]`(而 `parallel-safe` 只在两个 `[P]` 行之间触发),因而误得「无告警」并一度判该缺陷不存在(`checker-form.md` C-21)。

---

## 场景 5: US2 四项新检查的逆样本——**改前不可实跑**

```bash
tmp=$(mktemp -d)   # 逆样本 MUST 建在临时目录:MUST NOT 落在 `.specify/specs/` 下,
                   # 演练后残留计数 MUST 为 0(checker-form.md C-17、FR-041)
python3 scripts/python/validate-tasks.py $tmp/<case>.md --json
```

> **(2026-10-04 订正)** 本场景原先把样本路径写成 `<spec-dir>/notes/samples/<case>.md`,与 `contracts/checker-form.md` C-17「逆样本 MUST 建在临时目录,MUST NOT 落在 `.specify/specs/` 下」直接冲突——按原路径落地会在被校验的 spec 目录里留下 7 份坏制品,正是 SC-001 Source 的反空真哨兵要区分的残留。改为 `mktemp -d`,并在收尾以 `\rm -rf $tmp; ls -d $tmp 2>/dev/null | wc -l` → **0** 取证。

> **本例改前不可实跑**——四项检查尚不存在。所依赖的前提:
> - 新标签为 `green-dangling`(ERROR)、`green-cross-phase`(WARN)、`green-clause-collision`(WARN)、`green-path-divergence`(WARN)(D-5)
> - `validate-tasks.py` 的标签集由既有 **6** 项变为 **10** 项;`EXPECTED_CHECKS`(`test_validate_tasks_parallel_safety.py:75-82`)与脚本 docstring 的枚举段 MUST 在同一提交内同步扩充,因为 `:312` 从 **docstring** 抽取标签、`:314` 断言二者集合相等(C-25 of `green-point-claim.md`)
> - 归属声明解析为四元组 `(契约文件, 条款 id, 任务 id, 所处阶段)`;`#` 之后至 `]` 前全部视为条款 id(容许 `C-3.4` 一类形态)
> - 跨阶段判定用单调行序 `order`(`:123`/`:171`/`:181`),**不是**数值阶段索引(该脚本没有);直接先例是 `:229-233` 的 `blockedBy` 前向依赖 WARN(D-8)
> - 仅 WARN 时退出码仍为 **0**;悬空归属为 **1**(既有表只有两档,被 `test_c5_exit_code_table:353,356` 钉住)

**四份逆样本 + 一份正样本**(逐项对应,共 ≥ 4 份;`green-path-divergence` MUST 成对):

| 样本 | 构造 | 预期 |
|---|---|---|
| `dangling-file` | `[green: contracts/nope.md#C-1]`,该文件不存在 | `green-dangling`,exit **1** |
| `dangling-clause` | 契约文件存在但无该 id | `green-dangling`,exit **1** |
| `cross-phase` | 认领 C-2 的行位于认领 C-1 的行**之前**的阶段 | `green-cross-phase` ≥1,exit **0** |
| `clause-collision` | 两行都声明 `[green: contracts/x.md#C-1]` | `green-clause-collision` ≥1 且点名两行,exit **0** |
| `path-divergence` **正** | 两核验行同一测试路径、绿点**不同** | `green-path-divergence` ≥1,exit **0** |
| `path-divergence` **反** | 两核验行同一测试路径、绿点**相同** | 该标签 **0** 命中——证明它认的是**分歧**而非**共用** |
| `fenced` | 声明写在 ```` ``` ```` 围栏内 | 解析出的声明数为 **0**(FR-020) |

**分列判据**:构造一份只触发 `green-clause-collision` 的样本,`green-path-divergence` 的命中数 MUST 为 **0**,反之亦然(FR-018、C-17 of `green-point-claim.md`)。

---

## 场景 6: US3 的条款形态普查与 owner 声明——普查**改前可实跑**,owner 部分不可

普查命令与真实输出见**场景 1c**。补充两项**改前可实跑**的证据:

```bash
# 第五形态(括注后闭合)的实例证据
grep -c '\*\*C-[0-9]* (' .specify/specs/031-task-complexity-rubric/contracts/rubric-section.md
# owner 缺位的证明
grep -rniE "clause (id|identifier|numbering|syntax)|条款(编号|语法|形态)" templates/ shared/ docs/ \
  --include=*.md | grep -v docs/public | wc -l
find templates -iname "*contract*" -o -iname "*clause*" | wc -l
```

**本轮真实输出**:`10` / `0` / `0`

即:该契约用 `- **C-1 (heading)**` 一类形态共 **10** 条,闭合粗体正则 `\*\*C-\d+(?:\.\d+)*\*\*` **不命中**它们;而全仓对条款语法的定义**零命中**、`templates/` 下无任何 contracts 模板。

> **owner 文档与核算脚本部分改前不可实跑**——`shared/definitions/contract-clause-definitions.md` 与 `scripts/python/account-clause-coverage.py` 尚不存在。所依赖的前提:
> - owner 文档落 `shared/definitions/`,命名从该目录既有 **8** 份 `*-definitions.md` 的体例(该目录共 **9** 个文件,第 9 个是 `framework-map.md`,不匹配 `*-definitions.md`——两个数不可混用)(D-1,经用户裁定)
> - 该文档**从第一稿起就在门控扫描面内**(`SCAN_DIRS` 含 `shared`),措辞 MUST 对 `BLOCKING_PATTERNS`(**17** 条)零命中,而整数余量为 **0**
> - 核算脚本输出的两个数(可解析文件数 + 点名跳过数)之和 MUST 等于**本次实扫的文件总数**(关系式哨兵;MUST NOT 写成字面 `110`,理由见 `contracts/clause-coverage.md` C-7)
> - `.yaml` 抽取 MUST 手写行级解析,**不引入 PyYAML**(`pyproject.toml` 六项依赖无一为 YAML;先例 `gate-check.py:48`)
> - OpenAPI 的条款全集 = `paths:` 下的 HTTP 方法键(实测 **39** 个);**MUST NOT** 以字面 `operations:` 键探测(9 份文件内无该键)
> - 结构化形的条款全集 = `^\s+- id:` 的取值(实测 **6** 条:`no-tool-discovery-step`、`no-tool-template-boilerplate`、`no-mandatory-tool-manifests`、`no-refresh-tools-in-script`、`mirror-parity`、`no-tool-manifest-in-checklist`)
> - 可解析面与条款全集的**当前值由 `notes/clause-form-census.md` 拥有**,本例不复写(该值随本特性自己的契约落盘与每次编辑而变;唯一可安全引用的字面量是**改前基线** 110 文件 / 508 id,落盘后的值 MUST 现场跑命令)

**预期结果**(改后 MUST 实测并粘贴真实输出,**MUST NOT 沿用本行的任何数字**):全量扫描印出「可解析 N₁ / 点名 N₂ / **本次实扫总数 N₃**」三个数且 **N₁ + N₂ == N₃**——哨兵是**关系式**而不是字面量,理由见 `contracts/clause-coverage.md` C-7(本特性自己的 7 份契约就在被扫描面内,任何写死的总数都会在其落盘那一刻自我证伪)。点名清单默认折叠为计数、展开需显式旗标。
>
> 参考量级(as-of **2026-10-02**,由 `notes/clause-form-census.md` 拥有):六形态全认时可解析 **64** / 点名 **53** / 总数 **117**;只认闭合粗体时可解析 **28** / 点名 **89** / 总数 **117**(注意 **28** 而非 21:本特性自己的 7 份契约也用闭合粗体形,故落在可解析侧;初版在此把 110-基底的 21 与 117-基底的总数混用,已被委托评审查出)。

---

## 场景 7: US3 的冻结基线与 `comm -13` 比对——习语**改前可实跑**,核算基线不可

习语本身可用 052 的两份真实名字集演示(**改前可实跑**):

```bash
b=.specify/specs/052-fast-fail-principle/baseline-failed.txt
c=.specify/specs/052-fast-fail-principle/current-failed.txt
wc -l < $b; wc -l < $c
comm -13 <(sort -u $b) <(sort -u $c) | wc -l
```

**本轮真实输出**:`76` / `65` / `0`

即:基线 76 条、当前 65 条、**新增失败 0 条**。注意 `76 − 65 = 11` 是「治好了 11 条」,而不是「少了 11 条新增失败」——**只有 `comm -13` 的 0 才是判据**,计数差不是(这正是 SC-005/SC-010/SC-012 一律要求按名字比对的理由)。

> **覆盖基线部分改前不可实跑**——`account-clause-coverage.py` 与 `<spec-dir>/coverage-baseline.txt` 尚不存在。所依赖的前提:
> - 基线文件形态与 `run-tests.sh --names-out` 同构(每行一个名字、已排序),使 `comm -13` 可直接消费(D-10)
> - `run-tests.sh` 本身**不**存基线、**不**跑 `comm`(`:41` 写文件、`:42` 印 `# failed-name list written:`、`:43` 透传 pytest 退出码),故比对留给调用方
> - 基线 MUST 连同**当轮 owner 声明覆盖哪些形态**一起记录,否则「可解析文件数」在两个 owner 定义之间不可比
> - MUST NOT 复制 `scan-confirmation-gates.py --baseline` 的比较形态(它读基线**顶层** `total` 而冻结值嵌在 `confirmationGates` 下,退出码只反映 `violations`,作为相等门不可用;该缺陷已记录两次而上游仍未修)

**预期结果**(改后 MUST 实测):`comm -13 .specify/specs/053-machine-decidable-artifacts/coverage-baseline.txt <(当前未覆盖集)` 为空 **且** 同一轮印出的「本特性已认领条款数」非空——两条成对才构成通过(C-21 于 2026-10-03 增:未覆盖集为空而认领为零,是「空因为盲」不是「空因为对」)。基线 MUST 在**排除本特性自己目录**的语料上冻结(FR-027 § 基线面),故 053 自己的条款与 FR 恒在基线之外、只能被认领不能被豁免;基线内既有项不阻断,但每轮印出其计数。

---

## 场景 8: US4 的 `run-checks` 五项 verdict 与零写入——**改前不可实跑**,改前基线可

**改前可实跑的部分**(本轮已实跑):

```bash
python3 scripts/python/goal-utils.py --help 2>&1 | grep -oE '\{[a-z,-]+\}' | head -1
grep -c 'sub.add_parser' scripts/python/goal-utils.py
sed -n '44,47p' scripts/python/goal-utils.py
grep -rn "EXIT_[A-Z_]* = 5" scripts/python/ ; echo "exit=$?"
grep -rn "goal_utils.EXIT" tests/ ; echo "exit=$?"
find .specify/goal .specify/teams -type f | sort | xargs sha256sum | sha256sum
```

**本轮真实输出**

```text
{create,validate,check-statement,list,status,objective,criteria,migrate,targets}
9
EXIT_OK = 0 / EXIT_INPUT_ERROR = 2 / EXIT_NOT_FOUND = 3 / EXIT_INVALID = 4
(码 5:无命中,exit=1)          ← 5 空闲
(goal_utils.EXIT:无命中,exit=1) ← 退出码表当前无任何钉子
751e5df220adef18c79b1aa3…       ← 零写入的改前校验和
```

> **`run-checks` 调用部分改前不可实跑**——该 action 尚不存在。所依赖的前提:
> - action 名为 STR-005 `run-checks`,`sub.add_parser` 计数由 **9** 变 **10**,`--help` 的 choices 集合同步变化
> - 五项 check 的 verdict 全部由既有代码产出(`resolve_team_goal_identity` `:607-620`、`preview_target_check` `:626-676` 内的 `:634-637`/`:639-645`/`:654-657`/`:659-662`/`:663-667`/`:668-674`/`:646-651`),MUST NOT 重写第二套文法
> - `preview_target_check(repo_root, team_slug, reference)` 的 `reference` 是**必需位置参数**,故无 `--target` 时第①项不可达;实现 MUST 新增薄封装,无 target 时 ②③④ 记 `not-evaluated`、①⑤ 仍评估(D-11)
> - 退出码为 STR-007 `0=ok / 2=input-error / 3=not-found / 4=invalid / 5=blocked`,即既有四码**原义不变** + 新增 `EXIT_BLOCKED = 5`
> - `--json` 已由共享父解析器提供(`:794`),新 action MUST 经 `_emit(result, args.json)`(`:1000`)输出,MUST NOT 自行 `print(json.dumps(...))`
> - `--help` 行 MUST 以 `read:` 起首(既有约定,由 `test_goal_definition.py:245-257` 的 `line.split()[1].startswith(("read","write"))` 强制)
> - check 的 `name` 与 `verdict` 是**两个词表**:无字面量名为 `goal-binding`,第①项的 verdict 是 `no-goal-definition`

**预期结果**(改后 MUST 实测):

```bash
python3 scripts/python/goal-utils.py run-checks <team-slug> --json; echo "EXIT=$?"
find .specify/goal .specify/teams -type f | sort | xargs sha256sum | sha256sum   # MUST 与场景 1d 相等
```

顶层键为 `team_slug`/`goal_slug`/`identity_kind`/`resolution`/`checks`/`verdict`/`blocked`,`checks` 长度 **5**;校验和**逐字相等**(FR-034)。

**⚠ 真实样本可能不可得**:实测 `.specify/goal/` 下只有 **1** 个 goal(`draw-two-layer-structure`),`.specify/teams/` 下 6 个团队中只有它与一个 goal 定义绑定,且**其 goal 未必处于终态**。故 SC-007 的「对一个 goal 已终态的真实团队跑」这一支若找不到真实样本,MUST 在临时仓库副本里构造,MUST NOT 改动真实 goal 或团队定义;若两者都不可得,MUST 记为不可得并说明理由,MUST NOT 编造 verdict(SC-007 Source)。

---

## 场景 9: US4 的钉子——**改前可实跑其缺失证明**,改后需新钉子

**改前可实跑**(见场景 8:`goal_utils.EXIT` 在 `tests/` 零命中,即退出码表**当前无钉子**;`test_goal_definition.py:245-257` 的 roster 是**硬编码 9 元组且非封闭**,故新增 action 不会使它转红)。

要抄的房子形态(**改前可实跑**):

```bash
sed -n '48p;292p;395p' tests/contract/test_trigger_engine.py
```

> **新钉子部分改前不可实跑**。所依赖的前提:
> - 形态抄 `test_trigger_engine.py:48` 的 `EXIT_CODES = {…}` 常量表 + `:292` 逐 action 循环 + `:395` 的 `assert sorted(action.choices) == sorted(ACTIONS)`(**封闭** roster 断言)
> - `test_goal_definition.py` 的 9 元组 MUST 在同一提交内扩为 **10** 元
> - `goal-utils.py:16-30` 的读/写动作 roster 与 `:32` 的退出码表(`0 ok | 2 input error | 3 not found | 4 validation failed`)MUST 同步扩充以含 `run-checks` 与码 5
> - 该脚本 docstring 的 Program-First 归属是**内联括注**形态(`:6-7`),而 FR-002 只辖新增检查器,故 MUST NOT 把它改写成 `validate-tasks.py:4-6` 的点名 owner 形态

---

## 场景 10: US5 的指代形——**改前不可实跑**,脆弱性证据改前可实跑

US5 要消灭的脆弱性有**实证**(**改前可实跑**):

```bash
sed -n '15p;36p;37p' .specify/goal/draw-two-layer-structure/goal.md | cut -c1-120
grep -n "glob\|\*/\|directory-reference\|<dir>\|rglob\|iterdir" shared/definitions/goal-definitions.md; echo "exit=$?"
```

**本轮真实输出**

```text
:15  1. 七个绘图技能（draw-diagram 与 draw-{d3js,drawio,echarts,excalidraw,mermaid,plantuml}）在交付产物后…
:36  - 2026-09-16 — criteria changed; prior value: 六个绘图技能（draw-diagram 与 draw-{d3js,echarts,excalidraw,mermaid,plantuml}）…
:37  - 2026-09-17 — criteria changed; prior value: 七个绘图技能（draw-diagram 与 draw-{d3js,drawio,…}）…
(指代形/glob:无命中,exit=1)
```

同一条判据随成员集变化被**反复改写**(六个 → 七个),而 `shared/definitions/goal-definitions.md`(137 行)里**无任何** glob 或目录指代形态——这正是 US5 的缺口本体。

> **指代形解析部分改前不可实跑**。所依赖的前提:
> - 字面为 `[subjects: <glob>]`,glob 相对仓根、在**解析那一刻**导出成员集(D-14)
> - 该形式落进 `shared/definitions/goal-definitions.md` 的**新增一节**;该文件是概念 owner 而非被解析对象(程序化触点仅 `goal-utils.py:13` docstring、`test_goal_targets_engine.py:296`+`:357`、`test_confirmation_gates_sweep.py:169`、`test_goal_reference.py:150`),故 MUST NOT 重写其既有节
> - 路径不存在 → 可区分错误;路径存在但成员为空 → 前缀 STR-010 `SUBJECT EMPTY:`
> - 冲突判据为「`[subjects:]` 与花括号展开 `\{[^}]*,[^}]*\}` 同行同现」;**诚实边界**:不带花括号的散文枚举检不出,该边界 MUST 记入 owner 文档
> - 该文件在门控扫描面内且整数余量为 **0**,新节措辞 MUST 对 `BLOCKING_PATTERNS` 零命中
> - 第二解析器 `skills/create-team/scripts/build-summary-input.py:354-391` **刻意**不 import(`:356-360`「cross-tree import breaks once installed」),故 MUST 显式处置它, MUST NOT 沉默

**SC-009 的取证形态**(改后 MUST 实测):对同一主体集合分别用指代形与成员枚举写两条判据,在目录里增删一个成员后,指代形导出的集合随之变化而枚举形不变;增删 MUST 在临时副本里做,MUST NOT 改动真实 skills 目录。

**SC-010 的反空真哨兵**(改后 MUST 实测):当前全集只有 **1** 份 goal 定义,故「失败集合按名字比对为空」近乎空真,MUST 同时断言被扫描的 goal 定义数 ≥ **1** 且解析器确实产出了成员集。

---

## 场景 11: 收尾三判据——**改前基线可实跑**,改后需重跑

```bash
# 11a 名字级回归(SC-012):新增失败集为空
bash .specify/scripts/bash/run-tests.sh --names-out <spec-dir>/current-failed.txt -q tests/
comm -13 <(sort -u <spec-dir>/baseline-failed.txt) <(sort -u <spec-dir>/current-failed.txt)

# 11b 门控中立(FR-045 / SC-012):total 仍为 23、violations 为 0
python3 scripts/python/scan-confirmation-gates.py --summary

# 11c 镜像无新增漂移(FR-047):逐对给出判据,不用全树绝对判据
for p in scripts/python shared/definitions shared/guidelines shared/constants \
         templates/tasks-template.md templates/commands templates skills \
         skills/create-team/references/execution-guide.md \
         skills/create-team/references/goal.md \
         skills/create-team/scripts/build-summary-input.py; do
  out=$(python3 scripts/python/sync-mirrors.py --check --only "$p" 2>&1); code=$?
  printf '%-30s EXIT=%s\n' "$p" "$code"
done
python3 scripts/python/regen-command-copies.py --check; echo "regen EXIT=$?"
```

**改前真实输出(本轮实测,逐对)**

| 对 | 改前 EXIT | 判据形态 |
|---|---|---|
| `scripts/python` | **2**(既有 `.specify/scripts/python/trigger-utils.py` DIFF) | **相对**:无新增漂移 |
| `shared/definitions` | 0 `ok (9 files)` | 绝对 |
| `shared/guidelines` | 0 `ok (13 files)` | 绝对 |
| `shared/constants` | 0 `ok (3 files)` | 绝对 |
| `templates/tasks-template.md` | 0 `ok (1 files)` | 绝对 |
| `templates/commands` | 0 | 绝对 |
| `templates`(整对;2026-10-03 由第二轮 `/speckit.analyze` 补测) | **2** —— **2** 处 DIFF(`.specify/templates/proactive-trigger-seed.json`、`.specify/templates/skills-template.md`,皆先于本特性,最后提交 2026-09-20) | **相对**:无新增漂移(本特性不写这两个文件;T023 的 `--write --only templates` 会把它们一并同步,见 plan.md 订正记录 4) |
| `skills`(整对;2026-10-03 由 `/speckit.analyze` 补测——初版**从未测过这一对**,因为它不在计划表里) | **2** —— **30** 处 DIFF(皆先于本特性,含同目录的 `operating-loops.md`、`summary-mapping.md`) | **相对**:无新增漂移 |
| `skills/create-team/references/execution-guide.md`、`.../references/goal.md`、`.../scripts/build-summary-input.py`(2026-10-03 补测) | 三个**单文件**各自 **0** —— 当前与各自镜像逐字节相同 | 绝对;这三处正是 T034/T041 的写入面 |
| **全树**(不带 `--only`) | **2** DRIFT,实测 **33** 处 = `skills` **30** + `templates` **2** + `scripts/python` **1**(初版记为「三处」并把余下 30 处全归给 `skills`,漏了 `templates` 对里的 2 处) | MUST NOT 用绝对判据 |
| `regen-command-copies.py --check` | **0**「OK: all per-tool command copies match the source templates.」 | 绝对 |

**⚠ 测量陷阱(本轮踩到并已订正)**:经 `| tail` 取 `$?` 得到的是 `tail` 的退出码而非脚本的——第一次测量因此把 `scripts/python` 的 EXIT=2 误报为 0。MUST 用 `PIPESTATUS` 或如上例那样先赋值再取码。

**11a 的反空真哨兵**:MUST 同时报出基线条数与当前条数,使「`comm -13` 为空」可被区分于「两边都是空文件」。本轮的参考实例:基线 **76** / 当前 **65** / 差集 **0**(见场景 7)。

**订正一处旧结论**:052 的 plan 记录称 `regen-command-copies.py --check`「有大量既有待再生项」;本轮实测为 **EXIT=0** 全清。故本特性 MUST NOT 继承那句旧结论,镜像判据一律以本轮逐对实测为准。

---

## 场景 12: 演练残留清零——**改前可实跑,每轮收尾 MUST 跑**

```bash
D=.specify/specs/053-machine-decidable-artifacts
# A. 本特性目录内的**未跟踪**演练产物(破坏副本 / 逆样本 / 演练文件)
git status --porcelain --untracked-files=all "$D/" | grep -E '^\?\?' \
  | grep -E '/(b[0-9]+\.md|.*sample.*\.md|.*drill.*|.*broken.*)$' | wc -l
# B. 本轮自己创建的每个 mktemp 目录:创建时记下路径,收尾逐个复核其已不存在
for d in "${DRILL_DIRS[@]}"; do [ -d "$d" ] && echo "RESIDUE $d"; done | wc -l
# C. 反空真哨兵:先证明 A 会红,再复原
printf 'drill\n' > "$D/b9.md"
git status --porcelain --untracked-files=all "$D/" | grep -E '^\?\?' \
  | grep -E '/(b[0-9]+\.md|.*sample.*\.md|.*drill.*|.*broken.*)$' | wc -l   # MUST 为 1
\rm -f "$D/b9.md"
ls "$D/b9.md" 2>/dev/null | wc -l                                            # MUST 为 0
```

**本轮真实输出**:A = `0` · B = `0`(场景 3/4/5 的临时目录均已 `\rm -rf` 并复核)· C = `1` 然后 `0`(哨兵确实会红,复原后确实归零)

**判据**:A 与 B MUST 为 **0**;C MUST 先为 **1** 再为 **0**——**C 不是可选的**,没有它,A 的 `0` 无法与「模式写错了、什么都匹配不到」区分。破坏副本 MUST NOT 落在 `.specify/specs/` 下(SC-001 Source);变异演练的临时产物残留计数 MUST 为 0(FR-041、SC-011)。删除 MUST 用 alias-proof 形式(`\rm -f` / `\rm -rf`)并在删后复核——交互式别名(`rm -i`)会静默吞掉非交互删除而看起来成功。

**⚠ 两个 MUST NOT 使用的判据形态**(初版正是这样写的,委托评审查出其在当前树上**不可满足**,即一条永久红的检查):

- `git status --porcelain .specify/specs/ | wc -l` MUST 为 0 —— 不可满足:本特性自己的 7 份契约与 5 份设计制品在提交前都是未跟踪的,实测 **15** 条。该命题把「本特性的正常产物」当成了残留。
- `find .specify/specs -name '*probe*' | wc -l` MUST 为 0 —— 不可满足:仓内既有 **4** 个**已跟踪**文件名含 `probe`,且都是合法的既有制品(`044-reduce-confirmation-flows/contracts/gate-probe-protocol.md`、`041-refactor-feedback-probe/` 及其 `contracts/probe-registry.md` 等,提交于 2026-08)。该命题把别的特性的正常文件名当成了本特性的残留。

修法即上面的 A:**只看未跟踪**、**只在本特性目录内**、**只匹配本特性的演练命名**。一条永远为红的检查与一条永远为绿的检查同样无用——前者训练下一个人忽略它,后者什么也没证明。

---

## 场景覆盖表

| 场景 | 对应 | 改前可实跑? |
|---|---|---|
| 1 | 四组基线(SC-012、FR-045、FR-022、FR-034) | ✅ 已实跑 |
| 2 | FR-014 债务 + 两个待改测试 | ✅ 已实跑 |
| 3 | US1 检查器 + 四份破坏副本(SC-001) | ❌ 逐例前提已列 |
| 4 | US2 假告警:改前复现 / 改后消失(FR-019) | ✅ **改前即可复现**,已实跑 |
| 5 | US2 四项新检查的逆样本(SC-003、SC-004) | ❌ 逐例前提已列 |
| 6 | US3 形态普查 + owner 声明(SC-006) | ◐ 普查已实跑;owner 部分前提已列 |
| 7 | US3 冻结基线与 `comm -13`(FR-027、SC-005) | ◐ 习语已实跑;核算基线前提已列 |
| 8 | US4 五项 verdict + 零写入(SC-007、SC-008) | ◐ 改前基线已实跑;action 部分前提已列 |
| 9 | US4 钉子(FR-046) | ◐ 缺失证明已实跑;新钉子前提已列 |
| 10 | US5 指代形(SC-009、SC-010) | ◐ 脆弱性证据已实跑;解析部分前提已列 |
| 11 | 收尾三判据(SC-012、FR-045、FR-047) | ✅ 改前基线已实跑(逐对) |
| 12 | 演练残留清零(FR-041、SC-011) | ✅ 已实跑 |

**合计 12 个场景**(计数命令 MUST 用 `grep -c '^## 场景 [0-9]'`;裸 `'^## 场景'` 会同时匹配下面的 `## 场景覆盖表` 而给出 **13**——该失效模式在 052 plan 期已实测过一次,本轮复现):按上表标记,**✅ 全可实跑 5 个**(场景 1、2、4、11、12)+ **◐ 部分可实跑 5 个**(场景 6、7、8、9、10)= **10 个场景含改前已实跑的真实输出**;**❌ 纯不可实跑 2 个**(场景 3、5)。全文共 **8** 处逐例免责块(`grep -cE '^> \*\*.*改前不可实跑' quickstart.md` → 8:7 处纯「不可实跑」+ 场景 3 那处「构造命令可实跑、但用检查器验证不可」的混合式),每处都携「所依赖的前提」清单,无文件级免责。
