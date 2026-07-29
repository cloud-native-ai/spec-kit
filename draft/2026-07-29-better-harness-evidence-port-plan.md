# Better Harness 能力移植方案:公共证据采集基础设施 + improve-* 优化流程改造

> 状态:**待审查(Draft v2)**
> 日期:2026-07-29
> 源项目:`/cws_work/better-harness`(commit `b2e621d`,v0.3.0,MIT)
> 目标项目:`/cws_work/spec-kit`
> v2 变更:复用策略定为**源码复制托管**(scripts/js/);多 CLI 扩展定位为自有代码演进;
> teams runs 与 feedback 升格为**一等证据泳道**。本文档是设计方案,未做任何代码变更。

---

## 1. 目标与已定决策

### 1.1 目标

1. 将 Better Harness 的**证据采集与规范化能力**移植为 spec-kit 的**基础设施级公共流程**:
   任何上层技能/命令均可调用,获得基于 Session、项目结构及 spec-kit 执行工件的统一规范化证据
   (核心为 `findings.json` 证据合同)。
2. **证据采集与后续用途分离**:证据层不预设"harness 优化"用途,消费方式由 spec-kit 侧定义。
3. **优化流程**合并进 `skills/improve-*`,标准范式为:
   **先调公共证据流程采集 → 再用各技能自有 improve 流程针对证据指出的缺陷优化修改**。

### 1.2 已定决策(本轮确认)

| 决策 | 内容 | 理由 |
| --- | --- | --- |
| **D1 源码复制托管** | 采集子集的 `.mjs` 源码复制到 `scripts/js/better-harness/`,由 spec-kit 直接进行代码管理,**不用** submodule/npm 松散依赖 | 证据采集是框架基础设施,不能依赖外部仓库的可用性与合同稳定性 |
| **D2 多 CLI 扩展基础** | 上游只完整支持 Qoder(Codex 部分,Claude/Cursor 更弱);spec-kit 需支持 Claude Code、Codex、Qoder、Copilot、opencode、Qwen、Hermes、iFlow 八种工具。复制托管后,平台适配器成为 spec-kit 自有演进面 | 上游 roadmap 不会按 spec-kit 的工具矩阵排优先级;自有代码才能自主补齐 |
| **D3 spec-kit 执行工件入证据** | teams 的 `runs/`、`STATE.md`、`run-log.jsonl` 与 `.specify/memory/feedback/` 条目作为一等证据泳道 | 它们是 spec-kit 已有的最真实"观察到的执行"证据源 |

### 1.3 移植的方法论内核(必须保留)

四条证据纪律作为 spec-kit 证据层公共合同:

| 纪律 | 来源 | 落点 |
| --- | --- | --- |
| **配置存在 ≠ 观察到使用** | `models/agent-work-loop.md:55` | 每条证据必须带 `evidenceState` 标签(§4.2) |
| **未观察保持 Unobserved,不推断** | README "deliberately honest" | improve 流程禁止把 `Unobserved` 当缺陷修 |
| **计数只路由检查,不产生发现** | `SKILL.md:57` | 资产/会话/运行计数不得直接生成优化点 |
| **隐私:语义面片,不出原文** | `privacy-safe-text.mjs` 三层漏斗 | 证据文件禁含原始 prompt/命令/私有路径/密钥 |

---

## 2. 总体架构:两层分离 + 五泳道

```text
┌────────────────────── 消费层(spec-kit 自有,自由定制) ──────────────────────────┐
│  improve-skills    improve-agent    improve-team    (未来: /speckit.analyze 等)  │
│      │ 读取             │ 读取           │ 读取                                   │
└──────┼─────────────────┼───────────────┼──────────────────────────────────────┘
       ▼                 ▼               ▼
┌────────────────────── 公共证据层(新增,基础设施) ──────────────────────────────┐
│  collect-evidence 技能(编排) + evidence-utils.py(确定性适配器/泳道编排器)     │
│  五泳道:                                                                        │
│    session   ─┐                                                                 │
│    project   ─┼─ subprocess(node, argv[]) → scripts/js/better-harness/*(D1)   │
│    assets    ─┘                                                                 │
│    runs      ── 纯 Python 读 .specify/teams/<slug>/runs/ + STATE.md(D3)        │
│    feedback  ── 纯 Python 读 .specify/memory/feedback/(D3)                     │
│  产出: .specify/memory/evidence/<run-id>/{findings.json, lanes/*.json, manifest} │
└──────┬───────────────────────────────────────────────────────────────────────────┘
       ▼
┌────────────────────── 采集引擎(源码托管于 spec-kit,D1/D2) ────────────────────┐
│  scripts/js/better-harness/   ← 从上游复制的采集子集 + spec-kit 自有平台适配器    │
└───────────────────────────────────────────────────────────────────────────────────┘
```

分离判据:

- **证据层对消费者中立**:`collect-evidence` 与 `evidence-utils.py` 不含优化语义;
  improve-* 只是消费者之一(summarize-project、code-review、未来 /speckit.* 均可消费)。
- **优化观点全部住在消费层**:严重度、修复方案、优先级、验收标准由 improve 流程生成。

---

## 3. 采集引擎:源码复制范围与代码管理(D1/D2)

### 3.1 复制子集(已核实内部依赖闭合)

从上游 `scripts/` 复制以下能力目录到 `scripts/js/better-harness/`(≈1.1 MB 源码,
**零 npm 依赖**——仅用 Node 内置模块;tree-sitter/esbuild WASM 只被爆炸半径/Canvas 使用,不在子集内):

| 目录 | 用途 | 依赖说明 |
| --- | --- | --- |
| `session-analysis/`(整目录,588K) | 会话发现、Episode 构建、脱敏、语义面片、平台适配器 | 被其他三个能力引用其 `fs.mjs/paths.mjs/cli.mjs`,必须整体复制 |
| `core-change-watch/`(120K) | 项目画像、历史信号、核心路径、diff 影响 | 依赖 `../session-analysis/{fs,paths}.mjs` |
| `agent-customize/`(148K) | 四宿主配置资产清单 providers | 同上 |
| `coding-agent-practices/`(仅 `asset-baseline.mjs`、`inventory/lint/integrity` 相关,**不含 `checkup/`**) | lint/inventory/integrity 三信封 | checkup 是变更器,超出证据范围,不复制 |
| `dependency-governance/`(36K,可选) | 依赖治理信号,补充 project 泳道 | 独立 |

**明确不复制**:`harness-analysis/`(1.1M,含 lead 分析器、report-source、渲染器——均为裁决/呈现层)、
`better-harness-cli/`(根门面)、`packaging/`、`hooks/`、`findings-recommend/`。
`evidence-bundle` 门面也不复制:它会拖入 lead 分析器(`evidence-bundle/index.mjs` 引用
`../report-run.mjs`),而 lead 的 `summaryFacts` 属于上游的分析观点。**泳道编排改由
`evidence-utils.py` 承担**——分别调用各能力的 `cli.mjs`,在 Python 侧合成泳道状态
(沿用 lane-status 语义:`available/partial/unavailable`)。

### 3.2 代码管理约定

- **目录布局**:`scripts/js/better-harness/{session-analysis,core-change-watch,agent-customize,coding-agent-practices,dependency-governance}/`,
  保持上游相对路径结构不变,使 `../session-analysis/...` 交叉导入原样成立,最小化复制改动;
- **溯源与许可**:`scripts/js/better-harness/UPSTREAM.md` 记录源仓库、commit(`b2e621d`)、
  复制日期、子集清单、本地修改日志;上游 `LICENSE`(MIT)复制为同目录 `LICENSE`;
- **本地修改纪律**:允许修改(这是 D1 的目的),但每次修改须在 UPSTREAM.md 追加一行
  (文件、动机、是否可回馈上游);与上游的重新同步是**手动、按文件、diff 驱动**的,不追求自动合并;
- **镜像**:遵循 spec-kit 镜像模型,`scripts/js/` 需同步 `.specify/scripts/js/`
  (与 `scripts/bash|python` ↔ `.specify/scripts/` 同规则);
- **测试**:从上游 `test/` 摘取采集子集对应的测试文件到 `tests/js/`(同为 `node --test` 风格),
  并在 pytest 侧加一个 contract 测试:调 `evidence-utils.py --action doctor/collect` 校验
  findings.json 合同(spec-kit 主测试栈仍是 pytest,Node 测试作为子集回归用,可由
  `tests/js/run.sh` 包装进 CI)。

### 3.3 多 CLI 扩展路线(D2)

平台支持现状(上游)与 spec-kit 目标:

| 工具 | 上游会话适配器 | 上游资产 provider | spec-kit 计划 |
| --- | --- | --- | --- |
| Qoder CLI | 完整 | 完整 | 直接使用 |
| Codex CLI | 可用(缺模型/Hook 证据) | 完整 | 直接使用,缺口标 `Unobserved` |
| Claude Code | 可用 | 无统一 provider | 使用会话适配器;资产 provider 为**首个自研补齐项** |
| Cursor | 弱(无时间戳) | 部分 | 低优先(不在 spec-kit 支持矩阵) |
| Copilot / opencode / Qwen / Hermes / iFlow | 无 | 无 | **spec-kit 自研适配器**,按各工具本地会话/配置存储逐个实现 |

扩展机制(这正是复制托管的价值所在):

- 新会话适配器 = 在 `session-analysis/platforms/` 新增一个继承 `SessionAnalyzer`
  (`analyzer.mjs:59-112` 五个虚方法:resolveScope/discoverSourceRoots/discoverSessions/readSession/normalizeEvent)的 `.mjs`;
  **优先走上游较新的 `provider-runner.mjs` 模式**(claude/cursor 已用),避免 qoder/codex 的内联旧模式;
- 新资产 provider = 在 `agent-customize/providers/` 新增采集函数并注册进 `providers/index.mjs:6-11` 的分发表;
- 每个新适配器必须:输出走既有脱敏漏斗(不得绕过 `privacy-safe-text`/`semantic-facets`)、
  能力缺口显式标注(学 Cursor 适配器的 `eventTimestampCoverage: "partial"` 做法)、附最小 fixture 测试;
- 建议实现顺序:opencode → Qwen(会话存储格式若类 Claude JSONL 可低成本仿写)→ iFlow → Hermes → Copilot
  (以各工具是否有稳定本地会话落盘为准,`doctor` 探测不到落盘的工具,session 泳道直接标 `unavailable`)。

---

## 4. 公共证据层设计

### 4.1 新增文件清单

| 路径 | 类型 | 职责 |
| --- | --- | --- |
| `scripts/js/better-harness/`(+ 镜像) | 复制托管的 Node 采集引擎 | §3 |
| `.specify/scripts/python/evidence-utils.py` | Python(stdlib-only,风格同 feedback-utils.py) | 泳道编排、subprocess 调 Node、runs/feedback 泳道原生实现、规范化落盘、索引、compare |
| `skills/collect-evidence/SKILL.md`(+ 双镜像) | 技能 | 采集编排:解析范围 → doctor → collect → 边界申明 |
| `skills/collect-evidence/references/evidence-contract.md` | 参考 | findings.json 合同人读版(§5) |
| `skills/collect-evidence/references/evidence-discipline.md` | 参考 | 四纪律 + evidenceState 词汇表,供所有消费技能引用 |
| `.specify/shared/workflow/evidence-step.md` | 共享工作流 | 与 feedback-step.md 对偶的标准"证据步骤"块(§6.1) |
| `.specify/memory/evidence/` | 存储 | run 目录 + `index.json`(仿 feedback 存储结构) |

### 4.2 `evidence-utils.py` 命令面

```bash
python3 .specify/scripts/python/evidence-utils.py --action <action> [...]

  doctor    # 能力表: node 版本、可用平台(按支持矩阵探测本地落盘)、五泳道可用性
  collect   # --lanes <session,project,assets,runs,feedback|all> --target <unit-id>
            #   --since/--until --depth <quick|normal> --platform <qoder|codex|claude|...>
            # session/project/assets → subprocess(node, [cli.mjs, ...], shell=False)
            # runs    → 读 .specify/teams/*/runs/、STATE.md Post-Run Critique、run-log.jsonl
            # feedback→ 读 .specify/memory/feedback/(index.json + 条目 frontmatter/要点)
            # 合成 findings.json + lanes/*.json + manifest.json(含 findingsDigest sha256)
  list      # 列历史证据运行(按 target/时间过滤)
  latest    # 取某 target 最近一次 findings.json 路径(时效阈值默认 7 天,超龄警告)
  compare   # 同 target 前后两次 findings 差异摘要(纵向验证, §6.4)
```

设计要点:

- **argv-array、shell=False**,沿袭两项目共同安全惯例;
- **降级语义显式化**:某泳道不可用照常运行,manifest 标 `unavailable`、相应证据标 `Unobserved`,
  不静默不编造(移植 lane-status 语义,但放宽上游"normal 一泳道失败即整束失败"为"标注后继续");
- **runs/feedback 泳道的脱敏**:teams 运行报告与 feedback 条目为 spec-kit 自产、面向框架的文本,
  风险低于用户会话,但落盘进 findings 前仍过一遍 Python 侧脱敏(密钥模式/绝对路径掩码),
  并把 `.specify/memory/evidence/` 加入 feedback `package` 打包排除项。

### 4.3 `collect-evidence` 技能(SKILL.md 骨架)

遵循 skill-format.md C-001~C-006(frontmatter、Path Conventions、Resources、Dependencies、
500 行内、双镜像):

1. **解析范围**:目标单元、泳道、时间窗、深度、平台;
2. **doctor**:向用户展示可用/缺失泳道与平台;
3. **collect**:呈现 run 目录与按 evidenceState 分布的摘要;
4. **边界申明**:明示 `Unobserved` 项与不可用泳道;
5. **Feedback**:标准 feedback-step(`skill:collect-evidence`)。

红线:技能自身**不解读证据、不提优化建议**。

---

## 5. 统一证据合同:spec-kit 版 `findings.json`

### 5.1 合同(剥离上游裁决字段,保留证据事实)

```jsonc
{
  "schemaVersion": 1,
  "kind": "speckit.evidence-findings",
  "target": "skill:improve-skills",          // unit_id 词汇沿用 feedback 约定
  "runId": "ev-20260729-143000-improve-skills",
  "window": { "since": "...", "until": "..." },
  "platforms": ["qoder"],                     // 本次实际采集到数据的平台
  "lanes": {
    "session":  { "status": "available" },
    "project":  { "status": "available" },
    "assets":   { "status": "available" },
    "runs":     { "status": "available", "teamsScanned": 2 },
    "feedback": { "status": "available", "entries": 48 }
  },
  "evidence": [
    {
      "id": "ev-001",
      "lane": "session",
      "evidenceState": "Exercised",           // 七态词汇, §5.2
      "summary": "3 个 Task Episode 中 2 个在技能第 4 步后出现重复人工修正",
      "evidenceRefs": ["qsr1-a1b2..."],       // 不可逆哈希 / 相对文件引用
      "signals": { "episodeCount": 3, "reworkCount": 2 },  // 计数只路由,不是结论
      "privacyNote": "redacted-semantic-facet"
    },
    {
      "id": "ev-014",
      "lane": "feedback",
      "evidenceState": "Exercised",
      "summary": "7 条历史 feedback 反复提到同一优化点: 引用提取步骤易漏文件",
      "evidenceRefs": [".specify/memory/feedback/2026...-improve-skills.md"],
      "signals": { "recurrence": 7 }
    }
  ],
  "findingsDigest": "sha256:..."
}
```

上游的五维评分、severity、aiFixPrompt、支持轨道**不进合同**——属于消费层观点。

### 5.2 evidenceState 七态词汇(全量移植,禁止裁剪或重定义)

`Present / Wired / Exercised / Outcome-supported / Missing / Unobserved / Not applicable`
(语义见上游 `models/agent-work-loop.md:97-103`;复制其定义节到 evidence-discipline.md)。
消费层可自定义如何响应各状态,不得重定义状态语义。

### 5.3 五泳道定义

| 泳道 | 实现 | spec-kit 语境 |
| --- | --- | --- |
| session | Node:`session-analysis facts` | 技能/agent/团队真实执行行为:卡壳、返工、工具失败、Episode 结构 |
| project | Node:`core-change-watch evidence-pack`(+ 可选 dependency-governance) | 仓库结构/历史信号:镜像漂移、热点路径、文档健康 |
| assets | Node:`asset-baseline`(lint/inventory/integrity) | 已配置技能/命令/agent 清单与 lint(configured 侧) |
| **runs**(D3) | Python 原生 | teams 运行工件:`runs/` 报告、`STATE.md` Post-Run Critique、`run-log.jsonl`——观察到的团队级执行结果 |
| **feedback**(D3) | Python 原生 | `.specify/memory/feedback/` 48+ 条自我反思——补上"只写不读"缺口,重复出现的优化点以 `recurrence` 信号呈现 |

runs 泳道从 improve-team 现行读取逻辑(SKILL.md 引用 STATE.md + run-log.jsonl)**下沉**而来:
improve-team 改为消费 findings.json,不再自行解析原始工件(v1 方案的开放问题 2 就此定案)。

---

## 6. 消费层改造:improve-* 三技能

### 6.1 标准 improve 范式(写入 `.specify/shared/workflow/evidence-step.md`)

```text
Step A 证据采集   evidence-utils.py --action collect --target <unit> --lanes all
                  (或 --action latest 复用 7 天内证据)
Step B 证据审读   按 evidenceState 分拣:
                  - Exercised/Outcome-supported 的负向证据 → 缺陷候选(可修)
                  - Missing → 机制缺失候选(可建)
                  - Present/Wired 但从未 Exercised → "配而未用"候选(先查路由再考虑裁撤)
                  - Unobserved → 只记录, 禁止当缺陷修(红线)
                  候选清单冻结后, 后续步骤不得增删候选(防"想修什么就把什么说成证据")
Step C 根因与方案 【各技能自有】现有失败模式分类法保留
Step D 定向修改   【各技能自有】最小变更、双镜像同步等现有纪律保留
Step E 验证+台账  现有验证 + 写 intervention.json(§6.4)
Step F Feedback   现有 feedback-step 不变
```

### 6.2 各技能改动

| 技能 | 改动 | 保留 |
| --- | --- | --- |
| improve-skills | Step 2"从历史度量执行效果"(现为 LLM 回忆)升级为 Step A+B:session 泳道拿 Episode 级返工/失败证据,feedback 泳道拿历史优化点复现信号 | 失败模式八分类、最小变更、codify-deterministic-logic、双镜像、回归 diff 纪律 |
| improve-agent | 同上;assets 泳道补模板 lint 证据;既有"不从通用最佳实践优化"红线与 `Unobserved` 红线合并表述 | 六节结构分析法、模板而非实例边界 |
| improve-team | 原 STATE.md/run-log 读取改为消费 runs 泳道证据;补 session/feedback 泳道 | Refinement Map、结构保持编辑 |

每技能改动 30-60 行,注意 500 行上限与 `diff -rq` 双镜像校验。

### 6.3 严重度与建议:spec-kit 自有(明确不移植)

五维评分/分数天花板/支持轨道/findings-recommend 目录不移植。若未来需分级,可参考上游
"低分必须有回链发现"的一致性思想另行设计。

### 6.4 纵向验证(补 spec-kit 最大方法论缺口)

移植 intervention ledger **思想**:Step D 后写 `intervention.json`
`{ targetFinding, change, baselineRunId, expectedSignal }`;下次同 target 的 Step A 后用
`--action compare` 对比前后 findings:预期信号改善 → 干预标 `Outcome-supported`;
无可比数据 → 保持 `Unobserved`,**不得自称"已修复"**。

---

## 7. 实施计划

| 阶段 | 内容 | 验收 |
| --- | --- | --- |
| P1 引擎落库 | 复制 §3.1 子集到 `scripts/js/better-harness/`(+ 镜像);UPSTREAM.md + LICENSE;摘取对应 node 测试到 `tests/js/`;跑通 `node .../session-analysis/cli.mjs facts` 与 `core-change-watch` | 子集测试通过;在 spec-kit 仓库手动产出 session/project 原始 JSON |
| P2 适配器与合同 | `evidence-utils.py`:doctor/collect(session+project+assets)/list/latest;findings.json 合同 + pytest contract 测试 | `collect` 产出合法 findings.json;无 Node 环境 doctor 正确降级 |
| P3 spec-kit 泳道 | runs 泳道 + feedback 泳道(纯 Python)+ compare | 48 条存量 feedback 与既有 team runs 出现在 findings 中且脱敏 |
| P4 公共技能 | collect-evidence SKILL.md + 双镜像 + Skills 注册表 + evidence-step.md | 技能独立运行,输出边界申明;diff -rq 通过 |
| P5 improve-* 接入 | 三技能插入 Step A/B/E;Unobserved 红线入 SKILL.md;improve-team 切换 runs 泳道 | 对 improve-skills 自身跑完整"采集→优化→台账"闭环 |
| P6 纵向闭环 | intervention.json + compare 驱动 Outcome-supported 判定 | 第二轮 improve 引用第一轮干预的前后对比 |
| P7+ 平台扩展(持续) | 按 §3.3 顺序自研 opencode/Qwen/iFlow/Hermes/Copilot 会话适配器与 Claude 资产 provider | 每个适配器带 fixture 测试;doctor 能力表逐步点亮 |

风险与对策:

- **复制即分叉**:上游修 bug 不自动获益 → UPSTREAM.md 记录 commit 基线,定期(如每季度)
  对采集子集做一次 diff 审阅,按文件择优回移;
- **Node 环境缺失**:session/project/assets 三泳道降级 `unavailable`,runs/feedback 泳道
  (纯 Python)仍可用——公共流程在纯 Python 环境保有最低可用性;
- **子集边界侵蚀**:后续有人想"顺手"复制渲染/评分代码 → evidence-discipline.md 写明
  "采集子集只进事实,不进观点",并由 UPSTREAM.md 清单约束;
- **隐私**:引擎侧三层脱敏保留;evidence-utils 落盘前字段白名单二次过滤;
  `.specify/memory/evidence/` 排除出 feedback package。

## 8. 有意不移植 / 简化清单

- 五维评分/天花板/支持轨道/建议目录(消费层观点,§6.3);
- lead 分析器与 `evidence-bundle` 门面(拖入裁决层;泳道编排改由 Python 承担,§3.1);
- Canvas/HTML 渲染链(呈现走 summarize-project / draw-plantuml);
- review-packet 完整引用白名单(简化为 findingsDigest;出现幻觉引用问题再升级);
- checkup 变更器与 hooks(超出证据范围);
- 上游 3 并行证据代理编排(spec-kit 侧采集是确定性 CLI,无需 LLM 子代理)。

## 9. 剩余开放问题

1. `scripts/js/` 是否同时镜像到 `.specify/scripts/js/`(按现行镜像模型应镜像,但 1.1MB 双份;
   可考虑仅镜像入口说明、运行时统一走 `scripts/js/`——需定一条与镜像模型兼容的例外规则);
2. 证据时效阈值 `latest` 默认 7 天是否合适;
3. 是否为本方案开 `/speckit.feature` 走完整 SDD(规格→计划→任务),还是按本文档直接 P1 起步;
4. P7 平台扩展的优先顺序是否与团队实际工具使用分布一致(建议先用 doctor 探测各工具本地
   落盘现状再定序)。
