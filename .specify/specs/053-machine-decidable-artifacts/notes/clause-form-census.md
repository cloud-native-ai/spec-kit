# 契约条款形态普查(初次分类 2026-09-24;重导与自指修正 2026-10-02,`/speckit.plan` Phase 0 探查轮)

本文件是 `requirements.md` 现状锚点「条款语法的实测分布」一行、FR-022 的实测依据、
FR-023 的实测代价与 SC-006 Source 基线值的**唯一取证落点**。数字 MUST 由下面的命令重导,
MUST NOT 手抄。

## 本文件是这些数字的唯一拥有者

`requirements.md`(现状锚点行、FR-022、FR-023、SC-006 与其 Source 行)、`research.md` D-2、
`data-model.md` E-5a、`contracts/clause-coverage.md`、`quickstart.md` 场景 1c/6 与 `plan.md`
均**引用本文件**,MUST NOT 各自复写计数。凡需要数字处以「见 `notes/clause-form-census.md`」引用。

## ⚠ 自指修正:本特性自己的 7 份契约在被扫描面内

第一次普查(2026-09-24 早于本特性 `contracts/` 落盘)得 **110 份文件 / 508 个条款 id**。
本特性自己的 **7** 份契约落盘后,同一命令的文件数与条款 id 数**都会增长**,增长量恰为本特性自己的产出。
**这两个增长后的值 MUST NOT 在任何文件里写成字面量**——本文件初版写了,数小时后即被自己追加的两条条款推翻。
需要时跑下方的命令(从仓根)。实测(命令输出):

| 扫描面 | 文件数 | 条款 id 数 | 稳定性 |
|---|---|---|---|
| 排除 `053-machine-decidable-artifacts/` 后(**= 改前基线**) | **110** | **508** | **稳定**——本特性不改动其它 spec 的契约 |
| 仅 053 自己的 7 份契约 | **7** | 见下方命令 | **不稳定**——每次编辑本特性的契约就变 |
| 全部 `.specify/specs/*/contracts/*`(含 053 自己的) | **117** | 见下方命令 | **不稳定**,同上 |

**「含 053 自己的」那一行 MUST NOT 被写成字面量。** 本文件初版曾印 687,而在 `contracts/checker-form.md`
追加 C-33 后即刻变为 688——一个被本文件自己的编辑推翻的数字。凡需要该值处 MUST 现场跑命令:

```bash
python3 - <<'CENSUS_EOF'
import glob, re
def census(paths):
    f = i = 0
    for p in paths:
        s = open(p, encoding='utf-8', errors='replace').read(); f += 1
        if p.endswith(('.yaml', '.yml')):
            i += (len(re.findall(r'^\s{4}(?:get|post|put|delete|patch|head|options):\s*$', s, re.M))
                  if ('openapi:' in s and 'paths:' in s) else len(re.findall(r'^\s+- id:', s, re.M)))
        else:
            i += (len(set(re.findall(r'\*\*(C-\d+(?:\.\d+)*)\*\*', s)))
                  or len(set(re.findall(r'\*\*(C-\d+)', s)))
                  or len(set(re.findall(r'^#{1,6}\s+(C-\d+(?:\.\d+)*)', s, re.M))))
    return f, i
allf = sorted(glob.glob('.specify/specs/*/contracts/*'))
excl = [x for x in allf if '/053-machine-decidable-artifacts/' not in x]
print('excl-053 (baseline):', census(excl))
print('053 own            :', census([x for x in allf if x not in excl]))
print('all                :', census(allf))
CENSUS_EOF
```

**该命令 MUST 从仓根运行**(glob `.specify/specs/*/contracts/*` 是仓根相对路径;从本 spec 目录运行会静默返回 `(0, 0)` 而不是报错——本轮实测到该失效并已在此注明)。

本轮实跑输出(仓根):`excl-053 (baseline): (110, 508)` —— **只有这一组可以被当作字面量引用**。另两组(`053 own`、`all`)本文件刻意**不印出数值**:初版印了 `(7, 180)` 与 `(117, 688)`,随后追加 C-28/C-29 两条条款即把它们推翻为 `(7, 182)` 与 `(117, 690)`——一个被本文件自己的编辑推翻过两次的数字,不该以字面量形式出现在本文件里。需要时现场跑上面的命令。

**(2026-10-03 实现期订正:508 这个字面量本身也错了,正确值是 507。)** 上面那条命令用的是**整文粗扫**(`\*\*(C-\d+(?:\.\d+)*)\*\*` 在全文任意位置命中即计数),而条款语法的 owner 文档(`shared/definitions/contract-clause-definitions.md`,FR-022 指定)声明的规则更严:只有**行首标记**或**表格首格**的 id 是条款声明,出现在其它位置的 id 是交叉引用。两者在语料上恰好差 **1** 条——`051-user-facing-comprehension` 的 gate-neutrality 契约里有一处写在表格**非首格**的 `**C-13**`,它引用的是**另一份**契约的条款,粗扫把它算成了本文件的第 8 条。按 owner 规则用 `scripts/python/clause_extract.py` 重导:`excl-053 (110, **507**)`、`053 own (7, 182)`、`all (117, **689**)`;文件数与形态分布不变(110/117、六形态计数逐一相符)。**故本文件的 id 计数从此以 `clause_extract.py` 为准**,上面那条粗扫命令只用于文件数与形态分布;507 取代 508 成为唯一可安全引用的改前基线字面量(它不随本特性编辑变动)。

两个后果,都必须在下游制品里成立:

1. **SC-006 的反空真哨兵 MUST 是关系式而不是字面量**——「可解析文件数 + 点名跳过数 == 本次实扫的文件总数」,
   其中总数由命令在运行时导出。把它写成字面 `110` 会在本特性自己的契约落盘那一刻**自我证伪**,
   而这正是本特性要消灭的缺陷形态(一份声称「110/110」的核算在分母已经变成 117 时依然报绿)。
2. **110 / 508 是「改前基线」,不是「当前现实」**。引用它时 MUST 带 as-of 限定
   (2026-09-24,在本特性 `contracts/` 落盘**之前**);引用当前现实时 MUST 现场跑命令,MUST NOT 抄一个曾见过的数字。

**053 自己的全部条款因此进入覆盖核算面**(条数由 `feature-ref.md` § 覆盖统计拥有,本文件不复写)。
判据(**2026-10-03 由 `/speckit.analyze` 订正**,原文写作「它们是 FR-027 冻结基线**之后**的新增项」——那是假的:认领(T045)在 Polish 阶段落地、基线(T026)在 US3 阶段冻结,**冻结永远早于认领**,所以若基线含自身项,`comm -13` 对任何认领结果都报空,那是一道永不变红的门):
现行为 **基线面排除本特性自己的 spec 目录**(FR-027 § 基线面 + `clause-coverage.md` C-21),故 053 的条款与 FR 恒在基线**之外**——MUST 被本特性自己的 `tasks.md` 逐条 green-claim、MUST NOT 被基线豁免,且「未覆盖集为空」MUST 由一个 MUST 非空的已认领计数配对。这是本特性对自己的一次真实自举。

## 为什么重测

`/speckit.clarify` 轮(同日早些时候)印出「可解析面 31 / 110、其余 79 份 `.md` 无任何机器
可抽取形态」。该数**为假**:它只承认 `**C-N**` 闭合粗体一种形态,把 `## C-N` 标题形(25 份)
与 `**C-N (标签)**` 括注形(1 份)算进了「无形态」。79 = 100 − 21,即「`.md` 中不含闭合粗体者」,
而不是「无任何机器可抽取形态者」。已按追加方式订正,并把残余数改写为 owner 覆盖面的函数。

## 分类命令与逐形态计数

分类器:对 `.specify/specs/*/contracts/*` 逐文件判定,`.yaml` 按 `openapi:`+`paths:` /
`^\s+- id:` 二分,`.md` 按四种正则判定(闭合粗体、括注粗体、标题形、皆无)。

| 形态 | 判据 | 文件数 | 条款 id 数 |
|---|---|---|---|
| `**C-N**` 闭合粗体 | `\*\*C-\d+(?:\.\d+)*\*\*` | **21** | **312** |
| ↳ 表格单元 / 项目符号 / 行首裸粗体 | `^\|\s*\*\*C-` / `^-\s+\*\*C-` / `^\*\*C-` | 5 / 6 / 10 | — |
| `**C-N (标签)**` 括注后闭合 | `\*\*C-\d+` 命中但闭合粗体不命中 | **1** | **10** |
| `## C-N` 标题形 | `^#{1,6}\s+C-\d+` | **25** | **141** |
| ↳ id 位宽 | 1 位 / 3 位 | — | 126 / 15 |
| OpenAPI `.yaml` | `openapi:` 且 `paths:` | **9** | **39** path-operation |
| 结构化 `.yaml` | `^\s+- id:` | **1** | **6** |
| 皆无的 `.md` | 以上 `.md` 判据全不命中 | **53** | 0 |
| **合计** | | **110** | |

复核:21 + 1 + 25 + 9 + 1 + 53 = **110** ✓;四种 `.md` 形态互斥(分类器用 elif 链),
且 `md-bold+head` 同现文件数为 **0**。

## 残余数是 owner 覆盖面的函数

| owner 声明覆盖的形态 | 可解析文件数 | 被 FR-023 点名的文件数 |
|---|---|---|
| 只认 `**C-N**` 闭合粗体 | 21 | **89** |
| 认全部 `.md` 三形态 + 两种 `.yaml` | 57 | **53** |

故 FR-022 要求 owner「声明其覆盖的形态」不是装饰:**SC-006 的「可解析文件数」在两个 owner
定义之间不可比**,基线 MUST 与当轮 owner 的覆盖面声明一起记录。

## 括注形的实例(第五形态的证据)

`.specify/specs/031-task-complexity-rubric/contracts/rubric-section.md` 用
`- **C-1 (heading)**` … `- **C-10 (mirror parity)**`,闭合 `**` 在括注之后,
故 `\*\*C-\d+(?:\.\d+)*\*\*` 不命中而 `\*\*C-\d+` 命中。任何抽取器若只写闭合粗体正则,
会把这 10 条条款静默漏掉——正是 FR-025 要区分的「空因为盲」在单形态粒度上的形态。

## 无 owner 的证明

`grep -rniE "clause (id|identifier|numbering|syntax)|条款(编号|语法|形态)|C-N (form|syntax|convention)" templates/ shared/ docs/ --include=*.md`
→ 无命中(exit 1)。`templates/` 下无任何 contracts 模板
(`find templates -iname "*contract*" -o -iname "*clause*"` → 空)。
最接近约定的是 `.specify/specs/052-fast-fail-principle/feature-ref.md:21`
「条款引用形态为 `<contract-file> C-N`」与 `templates/requirements-template.md:173`
的 `contracts/xxx.md C-N` 示例——二者都是**用法**,不是定义。
