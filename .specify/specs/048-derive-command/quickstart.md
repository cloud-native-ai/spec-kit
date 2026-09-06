# Quickstart: /speckit.derive 走查(需求 048 / Feature 049)

三个端到端走查,对应 US1/US2/US3 与 US3 的降级分支。每条命令与每段 JSON 都可直接复制执行,其 flag 与 payload 形态由 `contracts/derive-engine.md`(C-8 flag 表、C-37 `--help` 一致性)钉死,防止文档漂移。

约定:`E` 指引擎,`W` 指一次性工作区 —— 三个走查各用自己的 `W`,**不触碰本仓已有的真实算子库与真实推导档案**(它们是累积资本,见文末)。

```bash
E=scripts/python/derive-utils.py          # 或其字节一致镜像 .specify/scripts/python/derive-utils.py
```

记录形状的唯一定义点是概念锚 `shared/definitions/derivation-definitions.md`(§Source Record / §Reasoning Move / §Derivation Chain / §Derived Architecture / §Self-Audit);本文件只给出**可跑通的实例**,不复述其字段语义。URL 一律用 RFC 2606 的 `.invalid`,使走查离线可复现;自己的运行里换成 handed-in 清单的真实 URL。

## 走查 1:happy path —— 从空工作区到 exit 0 的可溯源架构(US1+US2+US3,SC-002/SC-003)

```bash
W=/tmp/derive-qs1 && rm -rf $W && mkdir -p $W

# 1) 脚手架:档案 + 项目级算子库(库仅在此刻不存在时创建)
python3 $E --action init --slug api-versioning --workspace-root $W --format json
# → exit 0 · payload.created 两项(derive.md、moves.md)· clobbered=false · maxSteps=12
```

预期可观测结果:`$W/.specify/derive/api-versioning/derive.md` 存在且含八节固定节序;`$W/.specify/derive/moves.md` 存在且**零数据行**,携带标题行、引擎写入标记行、逐字表头与分隔行;`## Self-Audit` 预填 14 行、全部 `pending`。

```bash
# 2) 探测一小份 URL 清单(零写入:它是证据供给者,不是档案作者)
cat > $W/urls.json <<'JSON'
{"urls": ["https://specs.example.invalid/v1", "https://guide.example.invalid/compat"]}
JSON
python3 $E --action probe-links --file $W/urls.json --workspace-root $W --format json
# → exit 0 · payload.probed=2 · results[].access ∈ {live, wayback:<ts>, dead, paywalled, unknown}
#   在 SOCKS 代理环境(本机即是)全为 unknown,并附两条 notes:降级说明 + 指名 ALL_PROXY
```

预期可观测结果:**exit 恒为 0**,离线也不例外。全 `unknown` 时 `notes[]` 明说「这不是来源已死的证据」—— 落地证据由宿主 agent 自己的 fetch/search 工具取得并写进 `verification` 列,探测只做旁证。`results[].evidence` 是可直接抄进产物的具体串,不是 `verified` 一类裸断言。

```bash
# 3) 把分级来源表写进 ## Sources(agent 判 grade,引擎算 title_mismatch)
```

写入 `$W/.specify/derive/api-versioning/derive.md` 的 `## Sources`(表头由脚手架给出,勿改列序):

```markdown
| S-001 | Versioning REST APIs | Versioning REST APIs | false | primary | https://specs.example.invalid/v1 | live | direct | host fetch returned HTTP 200 with full body on 2026-09-05 |
| S-002 | Compatibility Guidance | Compatibility Guidance | false | authoritative-secondary | https://guide.example.invalid/compat | live | direct | host fetch returned HTTP 200 on 2026-09-05; publisher is the standards body |
```

预期可观测结果:`## Unverifiable Sources` 保持脚手架占位行(本次无 `unverified` 来源);`title_mismatch` 两行都是引擎按归一化比对算出的 `false`,agent 写什么都会被重算覆盖。

```bash
# 4) 追加两个算子(camelCase,intent=new,anchor 为跨主题限定形式)
cat > $W/moves.json <<'JSON'
{
  "moves": [
    {
      "name": "Locate-the-binding-constraint",
      "inferenceForm": "Given a system `S` believed to be limited by factor `F`, identify the resource `R` whose per-unit cost actually grows with load; the binding constraint is `R`, not `F`.",
      "prevents": "designing against a bottleneck that stopped being true, and treating a capacity claim as an architectural justification",
      "appliesWhen": "a scaling or capacity claim justifies a structural choice AND a measurable per-unit resource cost can be named; NOT licensed when no resource curve is observable",
      "anchor": "api-versioning.S-001",
      "intent": "new"
    },
    {
      "name": "Demote-by-counterexample",
      "inferenceForm": "Given a rule `P` stated as universal, exhibit one case `C` where `P` fails and demote `P` to a conditional scoped away from `C`.",
      "prevents": "inheriting a rule whose stated scope is wider than the evidence supports",
      "appliesWhen": "a normative claim is inherited from a secondary source AND a concrete counter-case is available; NOT licensed when the counter-case is hypothetical",
      "anchor": "api-versioning.S-002",
      "intent": "new"
    }
  ]
}
JSON
python3 $E --action moves-add --file $W/moves.json --workspace-root $W --format json
# → exit 0 · payload.requested=2 appended=2 deduped=0 superseded=0
#   issued=["M-001","M-002"] · dispositions=[{M-001,new},{M-002,new}] · duplicates=[]
```

预期可观测结果:`moves.md` 新增两行,`status` 均为 `active`,`anchor` 为限定形式;`M-` 由引擎项目级单调发放(`M-001` 起)。把 `anchor` 写成裸 `S-001` 会被 **exit 2** 整批拒绝(`moves-add` 不带 topic,无从限定),且**零写入**。

```bash
# 5) 消费投影,而不是整读库
python3 $E --action moves-list --name-contains constraint --status active --workspace-root $W --format json
# → exit 0 · total=2 returned=1 projection=true
#   librarySize={lines,bytes} · fullReadAllowed=true · moves[] 每行七字段投影
```

预期可观测结果:过滤器 AND 组合,零命中也是 exit 0(`returned=0`)。`fullReadAllowed` 是程序判定,阈值数值本身不出现在输出里。

```bash
# 6) 写两步链 + 两个架构元素(agent 动作)
```

`## Reasoning Moves Applied` 用**裸身份引用**(恒合法);`## Derivation Chain`:

```markdown
### D-1
- premises: S-001
- leads: S-002
- move: M-001
- derivation: S-001 states the constraint as a compatibility promise to clients, not as a URL shape. Instantiating M-001 with `S` = the public API, `F` = the URI template, `R` = the client's compiled-in expectation of a response body: the resource whose per-client cost grows is the expectation, so the version boundary belongs where expectations change, not where paths change.
- conclusion: A version boundary belongs at the point where a client's compiled-in expectation of a response changes, not at the URI path.
- falsification: A client that survives a removed required response field without any code change, while its request path is held constant.
- confidence: derived

### D-2
- premises: S-002, D-1
- move: M-002
- derivation: S-002 states as universal that additive changes are always backward compatible. M-002 demotes it by counter-case `C` = a client that enumerates an enum-valued field and fails closed on an unknown member: additive changes are compatible only for clients that ignore unknown members, so the rule is conditional on the client's parsing posture rather than on the change's shape.
- conclusion: Additive changes are backward compatible only for clients that ignore unknown members; compatibility is a property of the client's parsing posture.
- falsification: An enumerated-field client that fails closed on an unknown member and nonetheless continues to operate after a new member is added.
- confidence: derived
```

`## Termination` 改为 `- condition: a` + `- steps: 2 / 12`;`## Derived Architecture`:

```markdown
### A-1 Version at the expectation boundary
- statement: Expose one URI space and mark a new version only where a client's compiled-in expectation of a response body changes.
- derived-from: D-1
- confidence: derived

### A-2 Compatibility is a client property
- statement: Document additive changes as compatible only for clients that ignore unknown members, and treat fail-closed clients as a separate compatibility contract.
- derived-from: D-2
- confidence: derived
```

预期可观测结果:`D-2` 的前提含更早的 `D-1`(前向引用与自引用都会被拒);每步恰一个算子;元素 `confidence` **等于**其 `derived-from` 各步的最小秩,不是「不大于」。

```bash
# 7) 自审第一趟:必然 exit 4 —— 脚手架的 14 行还是 pending
python3 $E --action validate --slug api-versioning --workspace-root $W --format json
# → exit 4 · ok=false · semanticChecksPending=["A11","A14"]
#   errors[]: 12 条 A0/audit-result-diverges(A1..A10、A12、A13 逐行)
#   payload.audit.engine 全为 "pass" · payload.audit.semantic 为 {A11:"pending",A14:"pending"}
```

预期可观测结果:**这是收敛过程,不是缺陷**。`validate` 零写入,A1–A10/A12/A13 的结果由 `errors[]` 派生,产物里的行必须等于派生值,否则报 `audit-result-diverges`。

```bash
# 8) 转写 + 背书,再跑第二趟收敛
```

把 `payload.audit.engine` 逐值抄进 A1–A10/A12/A13 的 `result`(`method` 保持 `engine`);A11/A14 由 agent 显式背书,`result` 置 `attested`,`method` 必须是**可核查的一句话**(空 / `engine` / `n/a` 会触发 `attestation-method-degenerate` 警告):

```markdown
| A11 | online grounding actually happened this run | both URLs were fetched with the host fetch tool this run and each outcome recorded with its HTTP status in the verification column | attested |
| A14 | the artifact states the sources' way of thinking, not a summary of their content | M-001 and M-002 are recorded as inference schemas with named slots, and D-1/D-2 instantiate those slots instead of restating either source | attested |
```

```bash
python3 $E --action validate --slug api-versioning --workspace-root $W --format json
# → exit 0 · ok=true · errors=[] · warnings=[]
#   steps={total:2, anchorable:2, budget:12, budgetReached:false}
#   elements={total:2, untraceable:0} · moves={cited:2, resolved:2, missing:[]}
#   audit.engine 全 pass · audit.semantic={A11:"attested",A14:"attested"}
```

预期可观测结果:两趟收敛完成。**判据读 `ok` 与退出码,不读审计表** —— 未被任何 A 行映射的违例(一步挂两个算子、confidence 出枚举、derivation 短于 40 码点)会 exit 4 而 `audit.engine` 仍全 `pass`。

```bash
# 9) 计数与分布
python3 $E --action stats --slug api-versioning --workspace-root $W --format json
# → exit 0 · moves={total:2, byStatus:{active:2,superseded:0}, duplicateIds:0, duplicateForms:0}
#   archives={total:1, topics:["api-versioning"]} · lastRun={slug, generatedAt}
```

预期可观测结果:`duplicateIds` / `duplicateForms` 恒为 0(SC-003 的机械锚点);不带 `--slug`/`--file` 也合法(库级统计,`lastRun=null`)。

> **已知冲突(照实记录)**:`stats` 的运行相对处置分量按 `contracts/derive-engine.md` C-23 取自档案 `## Reasoning Moves Applied` 的 `move_id|disposition` 表,但同节里任何匹配 `^\| M-\d{3,} \|` 的行按 `contracts/move-library.md` C-25 都是**复写行** —— 连续写该表 → `validate` exit 4(`unmarked-move-copy`);插入投影标记让它过 A9 → 表的连续性被破坏,`stats` 读到全 0。二者当前不可兼得,故本走查用裸身份引用,`dispositions` 读 0。SC-003 的第二次运行测量需先裁定该节的物理形态。

## 走查 2:催生本特性的缺陷 —— handed-in 清单里的死链与社区改标题(US1,SC-001)

```bash
W=/tmp/derive-qs2 && rm -rf $W && mkdir -p $W
python3 $E --action init --slug api-contracts --workspace-root $W >/dev/null
cat > $W/moves.json <<'JSON'
{"moves": [{
  "name": "Demote-by-counterexample",
  "inferenceForm": "Given a rule `P` stated as universal, exhibit one case `C` where `P` fails and demote `P` to a conditional scoped away from `C`.",
  "prevents": "inheriting a rule whose stated scope is wider than the evidence supports",
  "appliesWhen": "a normative claim is inherited AND a concrete counter-case is available; NOT licensed when the counter-case is hypothetical",
  "anchor": "api-contracts.S-001",
  "intent": "new"
}]}
JSON
python3 $E --action moves-add --file $W/moves.json --workspace-root $W --format json
# → exit 0 · issued=["M-001"]
```

预期可观测结果:库就绪。下面三行来源就是 handed-in 清单的落地形态 —— 一个活的一手源、一个被社区改过标题的源、一个死链。

`## Sources`:

```markdown
| S-001 | Contract Test Design | Contract Test Design | false | primary | https://origin.example.invalid/contract-test | live | direct | host fetch returned HTTP 200 with the full body on 2026-09-05, publisher's own site |
| S-002 | 10 Tips for API Contracts (aggregator headline) | Contract Test Design Notes | true | community | https://aggregator.example.invalid/10-tips | live | websearch | search: origin.example.invalid/notes result #2 resolved the publisher's own copy; HTTP 200 on 2026-09-05 |
| S-003 | The Deprecated Wire Format |  | false | unverified | https://dead.example.invalid/wire-format | dead | wayback | host fetch returned HTTP 404 on 2026-09-05; archive availability API returned no snapshot |
```

`## Unverifiable Sources`(替换占位行 —— 死链必须留痕,不能静默消失):

```markdown
- **S-003** — HTTP 404 at the cited location and **no archived snapshot**, so the Dead-Link Protocol's first two steps both miss. The handed-in list presented it as a normative reference without disclosing that it is dead.
```

预期可观测结果:两个缺陷都被**记录**下来 —— 改标题者 `title_mismatch: true` 且**双标题并存**(`claimed_title` 是交进来的原话,`resolved_title` 是实际存在的);死链者进 `## Unverifiable Sources` 并带理由。`title_mismatch` 由引擎算,agent 写错值会被判 A1。

`## Derivation Chain`(注意 `premises` 只有 S-001,两个缺陷源都落在 `leads`):

```markdown
### D-1
- premises: S-001
- leads: S-002, S-003
- move: M-001
- derivation: S-001 states the rule as universal — every provider change is caught by a contract test. Instantiating M-001 with `P` = that universality and `C` = a provider change inside a field the consumer never reads: the test suite still passes while the contract has changed, so the rule holds only over the fields a consumer actually depends on. S-002 and S-003 are leads toward that scoping argument, but S-002 arrives under an aggregator's headline and S-003 is unreachable, so neither is used as a premise.
- conclusion: A contract test catches provider changes only over the response fields a consumer actually depends on; coverage is a property of the consumer's read set.
- falsification: A provider change confined to a field no consumer reads that nonetheless fails the existing contract test suite.
- confidence: derived
```

`## Termination` 写 `- condition: b` + `- steps: 1 / 12`(下一步需要的前提只能来自 S-002/S-003,二者都不是锚定级);`## Derived Architecture`:

```markdown
### A-1 Scope contract tests to the consumer read set
- statement: Generate contract assertions from the fields consumers actually read, and treat changes outside that set as unverified rather than covered.
- derived-from: D-1
- confidence: derived
```

`## Self-Audit` 按走查 1 的两趟法收敛(A11/A14 的 `method` 写成本次真实做过的事)。

```bash
python3 $E --action validate --slug api-contracts --workspace-root $W --format json
# → exit 0 · ok=true · payload.sources.titleMismatch=1
#   byGrade={primary:1, community:1, unverified:1} · steps={total:1, anchorable:1}
#   warnings=[unresolved-title @ S-003.resolved_title]
```

预期可观测结果:链在**唯一真正落地的那个来源**上完成了。`unresolved-title` 是警告不是错误 —— 只有一个标题时报「不一致」会把「无从核实」误报成「被改标题」,恰好掩盖 SC-001 要检出的缺陷之一。

```bash
# 把 community 源提升为前提(并把 A2 行同步改成 fail,以免 A0 抢话)
python3 - <<'PY'
from pathlib import Path
p = Path('/tmp/derive-qs2/.specify/derive/api-contracts/derive.md'); t = p.read_text()
t = t.replace("- premises: S-001\n- leads: S-002, S-003", "- premises: S-001, S-002\n- leads: S-003")
t = t.replace("| A2 | no step anchored on community/unverified; every unverified source recorded | engine | pass |",
              "| A2 | no step anchored on community/unverified; every unverified source recorded | engine | fail |")
p.write_text(t)
PY
python3 $E --action validate --slug api-contracts --workspace-root $W --format text
# → exit 4 · error [C1/premise-grade-ineligible] D-1.premises:S-002 — grade 'community' cannot anchor
#            error [A3/resolved-title-not-cited] D-1.derivation:S-002 — 必须逐字引用 resolved_title
```

预期可观测结果:**改标题的源锚不住步**,而且一旦进入 `premises`,A3 就要求 `derivation` 逐字引用 `resolved_title`(引用交进来的那个标题等于把改标题洗白)。把 `S-002` 换成死链 `S-003` 同样 exit 4(`premise-grade-ineligible`,`grade 'unverified'`),且 `steps.anchorable` 掉到 0。两者退回 `leads` 后恢复 exit 0 —— 「怎么找到的」可以留痕,「为什么成立」不行。

## 走查 3:无线上能力 —— 诚实降级,以及伪造一步的代价(US3,SC-005)

```bash
W=/tmp/derive-qs3 && rm -rf $W && mkdir -p $W
python3 $E --action init --slug service-mesh --workspace-root $W >/dev/null
cat > $W/urls.json <<'JSON'
{"urls": ["https://a.example.invalid/spec", "https://b.example.invalid/design", "https://c.example.invalid/guide"]}
JSON
python3 $E --action probe-links --file $W/urls.json --workspace-root $W --format json
# → exit 0 · online=false degraded=true · 三条 access 全 unknown · notes[] 两条
```

预期可观测结果:探测跑不动 ≠ 来源已死。下面三行来源全部 `unverified`,`verification` 归一化后**等于** `no-online-capability`([[STR-007]] 字面量),这是降级判据的硬条件。

`## Sources` 三行同形(逐行只换 id / 标题 / URL):

```markdown
| S-001 | Sidecar Data Plane Design |  | false | unverified | https://a.example.invalid/spec | unknown |  | no-online-capability |
| S-002 | Control Plane Reconciliation |  | false | unverified | https://b.example.invalid/design | unknown |  | no-online-capability |
| S-003 | Ambient Mesh Field Report |  | false | unverified | https://c.example.invalid/guide | unknown |  | no-online-capability |
```

`## Unverifiable Sources` 逐条列出三行并附同一理由;`## Reasoning Moves Applied` 写「None」(没读到任何论证,从标题里抽算子等于拿书目造算子);`## Derivation Chain` 与 `## Derived Architecture` **不写任何 `D-` / `A-` 块**;`## Termination` 写 `- condition: b` + `- steps: 0 / 12`;`## Self-Audit` 的 A1–A10/A12/A13 抄 `pass`,A11 置 `not-attested`、A14 置 `pending`(两者都是合法背书值,`pending` 是待办不是失败)。

```bash
python3 $E --action validate --slug service-mesh --workspace-root $W --format json
# → exit 0 · ok=true · payload.degraded=true
#   steps={total:0, anchorable:0} · elements={total:0, untraceable:0}
#   warnings 含 degraded-run @ ## Sources · notes=["no-online-capability: degraded run, chain not built"]
```

预期可观测结果:**诚实的空产物 exit 0**。判成错误会诱导 agent 编造核实来「变绿」,那是本命令存在的唯一理由的反面。另有 6 条来源级警告(`unresolved-title` ×3、`verification-evidence-token-absent` ×3),都是警告不是错误。

```bash
# 在同一份档案里硬塞一步
python3 - <<'PY'
from pathlib import Path
p = Path('/tmp/derive-qs3/.specify/derive/service-mesh/derive.md'); t = p.read_text()
t = t.replace("No step. Every premise would be `unverified`, and `unverified` cannot anchor.", """### D-1
- premises: S-001
- move: M-001
- derivation: Sidecars place the data plane in a per-pod process, which costs a hop and a memory floor per pod; the argument for ambient mode is that this cost is not per-workload-necessary.
- conclusion: A per-pod sidecar imposes a cost that not every workload needs to pay.
- falsification: A workload measured to require its own data-plane process for isolation reasons.
- confidence: derived""")
t = t.replace("- steps: 0 / 12", "- steps: 1 / 12")
p.write_text(t)
PY
python3 $E --action validate --slug service-mesh --workspace-root $W --format json
# → exit 4 · ok=false · payload.degraded 翻回 false · degraded-run 警告消失
#   error [C1/premise-grade-ineligible] D-1.premises:S-001 — grade 'unverified' cannot anchor
#   error [C1/premise-grade-ineligible] ## Derivation Chain — 无锚定级来源,故一步都不许有
#   error [A9/move-not-in-library] — 本次运行未发放过任何 M-
```

预期可观测结果:降级契约**不是绕过锚定规则的后门**。零步的空产物 exit 0,加一步立刻 exit 4 —— 两者的差别恰好就是「诚实」与「编造」的差别。

## 真实 dogfood 运行(可直接查阅的成品)

本仓已有一次真跑,不是夹具:`.specify/derive/rest-architecture/derive.md`。 handed-in 的 REST/Web 架构清单六个来源,只有 **一个**落地(`primary`,`access: live`),两个 404 且无存档快照,三个源站 403;因此链上只有一步 `D-1`、架构只有一个 `A-1`、其余全部作为 `Q-1` 记录而非发明。

```bash
python3 $E --action validate --slug rest-architecture --workspace-root . --format json
# → exit 0 · ok=true · sources.total=6 byGrade.primary=1 · steps={total:1, anchorable:1}
#   audit.engine 全 pass · audit.semantic={A11:"attested",A14:"attested"}
```

该档案末尾的 `## Defects this run surfaced` 记了四条真跑才暴露的缺陷(SOCKS 环境下探测无法出网、清单自身的可靠性声明不成立、畸形 moves 输入被高声拒绝、裸 `S-<nnn>` 锚点不可接受),是理解引擎当前形态最快的入口。

## 验收对照

| SC | 走查 |
|----|------|
| SC-001 | 走查 2(双标题并存 + 死链留痕,静默丢弃 0) |
| SC-002 | 走查 1 exit 0 + 走查 2 的两次 exit 4(community/unverified 锚定步骤数 0、缺 derived-from 元素数 0) |
| SC-003 | 走查 1 第 4/9 步(重复 id 与重复归一化形状恒 0;处置分量见该节已知冲突) |
| SC-004 | 走查 1 第 8 步的 `errors[]` 判据(禁用字面量注入 → exit 4 且定位 C3) |
| SC-005 | 走查 3(可锚定步骤 0、unverified = 全部来源、建链前停止、`## Derived Architecture` 为空、含降级说明) |
