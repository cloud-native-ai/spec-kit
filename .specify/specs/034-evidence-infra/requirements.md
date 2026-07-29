# Requirements Specification: 公共证据采集基础设施(Better Harness 能力移植)+ improve-* 证据驱动改造

**Requirement Branch**: `034-evidence-infra`  
**Created**: 2026-07-29  
**Status**: Draft  
**Input**: User description: "@/cws_work/spec-kit/draft/2026-07-29-better-harness-evidence-port-plan.md 按照这个方案进行试试,将better-harness项目的功能移植到本项目. 在分析过程中可以参考/cws_work/better-harness项目的this session: qodercli --resume 1261e61e-614e-4380-98d1-a8a54eef4bf5这个session提取历史分析信息(使用一个subagent)"

## Related Feature *(mandatory)*

**Feature ID**: 038  
**Feature Name**: Evidence Infrastructure

## Overview

将 Better Harness 项目(源仓库 `/cws_work/better-harness`,commit `b2e621d`,MIT 许可)的**证据采集与规范化能力**移植为 Spec Kit 的**基础设施级公共流程**,并据此改造 `improve-skills` / `improve-agent` / `improve-team` 三个优化技能为"先证据、后优化"的标准范式。整体设计遵循已评审的方案文档 `draft/2026-07-29-better-harness-evidence-port-plan.md`(Draft v2),其三项已定决策直接约束本需求:

- **D1 源码复制托管**:采集子集的源码复制到 `scripts/js/better-harness/` 由 Spec Kit 自行进行代码管理(含溯源台账与许可证),不采用 submodule 或包依赖;
- **D2 多 CLI 扩展自有演进**:复制托管后,平台适配器成为 Spec Kit 的自有演进面,逐步覆盖全部八种受支持 AI 工具;
- **D3 Spec Kit 执行工件入证据**:teams 运行工件(`runs/`、`STATE.md`、`run-log.jsonl`)与 `.specify/memory/feedback/` 条目升格为一等证据泳道。

架构分两层:**公共证据层**(采集编排技能 + 确定性泳道编排引擎,产出统一 `findings.json` 证据合同,对消费者中立、不含优化观点)与**消费层**(improve-* 等技能按证据状态分拣缺陷候选后再走各自既有优化流程)。方法论内核为四条证据纪律:配置存在 ≠ 观察到使用;未观察保持 Unobserved 不推断;计数只路由检查不产生发现;隐私上语义面片不出原文。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 采集引擎源码落库与托管(D1) (Priority: P1)

作为 Spec Kit 维护者,我把 Better Harness 的采集能力子集(会话分析、项目画像、资产清单、资产基线检查,以及可选的依赖治理信号)以源码复制方式落到 `scripts/js/better-harness/`,附带上游溯源台账(UPSTREAM.md)与 MIT 许可证副本,并摘取对应的上游测试;此后该子集由 Spec Kit 独立演进,与上游的再同步是手动、按文件、diff 驱动的。

**Why this priority**: 引擎是全部证据能力的物理基础;没有它,后续泳道、合同、消费改造都无从谈起。可独立交付并在本仓库手工产出原始采集 JSON 验证。

**Independent Test**: 复制完成后,在 Spec Kit 仓库内直接运行会话分析与项目画像的入口 CLI,能产出原始 JSON;摘取的引擎子集测试全部通过;UPSTREAM.md 记录源 commit、复制日期与子集清单。

**Acceptance Scenarios**:

1. **Given** 上游仓库处于基线 commit, **When** 按方案 §3.1 的子集边界执行复制, **Then** `scripts/js/better-harness/` 下仅包含约定的能力目录(明确排除裁决/呈现层:lead 分析器、evidence-bundle 门面、渲染链、checkup 变更器、根门面/打包/hooks/建议目录),且子集内部依赖闭合、零 npm 外部依赖(仅 Node 内置模块)。
2. **Given** 复制完成, **When** 查看 `scripts/js/better-harness/`, **Then** 存在 UPSTREAM.md(源仓库、commit、复制日期、子集清单、本地修改日志)与 LICENSE(MIT)。
3. **Given** 子集落库, **When** 运行摘取到 `tests/js/` 的引擎测试, **Then** 全部通过;后续任何本地修改都在 UPSTREAM.md 追加记录(文件、动机、是否可回馈上游)。
4. **Given** Spec Kit 仓库自身作为被采集对象, **When** 手动调用会话分析与项目画像 CLI, **Then** 产出结构合法的原始 JSON(会话不存在时如实报告而非报错崩溃)。

---

### User Story 2 - 统一证据合同与泳道编排引擎 (Priority: P1)

作为技能/命令作者,我通过一个确定性的 Python 编排引擎(`evidence-utils.py`,stdlib-only)采集证据:它探测本机能力(doctor)、按泳道调度采集(collect)、管理历史证据运行(list/latest)并支持前后对比(compare);所有泳道的产出规范化为统一的 `findings.json` 证据合同,带 evidenceState 七态标签,落盘到 `.specify/memory/evidence/<run-id>/`。

**Why this priority**: 证据合同是公共层与消费层的边界;与 US1 合并即构成最小可用的证据基础设施(session/project/assets 三条 Node 泳道)。

**Independent Test**: 在本仓库运行 `--action collect --lanes session,project,assets`,产出通过合同校验(pytest contract 测试)的 findings.json;在无 Node 环境下 doctor 正确报告三条 Node 泳道不可用且不崩溃。

**Acceptance Scenarios**:

1. **Given** 本机具备 Node 环境与本地会话数据, **When** 执行 collect, **Then** 产出 `findings.json + lanes/*.json + manifest.json`(含 findingsDigest 校验和),每条证据带泳道、evidenceState、摘要、不可逆引用与信号计数。
2. **Given** 某条泳道不可用(如无 Node、无会话落盘), **When** 执行 collect, **Then** 该泳道在 manifest 标 [[STR-010]],相应证据保持 [[STR-006]],其余泳道照常采集——显式降级,不静默不编造。
3. **Given** 证据合同, **When** 校验字段, **Then** 合同只含证据事实,上游的严重度评分、修复建议、支持轨道等裁决字段一律不出现;evidenceState 使用全量七态词汇([[STR-001]]~[[STR-007]]),消费方不得裁剪或重定义语义。
4. **Given** 历史上存在同一目标的证据运行, **When** 执行 latest, **Then** 返回最近一次 findings.json 路径,超过时效阈值(默认 7 天)给出超龄警告。
5. **Given** 引擎落盘证据, **When** 检查内容, **Then** 不含原始 prompt、原始命令、私有绝对路径或密钥(引擎侧脱敏漏斗 + Python 侧落盘前二次过滤),`.specify/memory/evidence/` 被排除出 feedback 打包范围。

---

### User Story 3 - Spec Kit 自有泳道:runs 与 feedback(D3) (Priority: P2)

作为 Spec Kit 维护者,我把项目已有的最真实执行证据源接入证据层:runs 泳道(纯 Python)读取 `.specify/teams/<slug>/runs/`、STATE.md 的 Post-Run Critique 与 run-log.jsonl;feedback 泳道(纯 Python)读取 `.specify/memory/feedback/` 的索引与条目,重复出现的优化点以 recurrence 信号呈现——补上反馈"只写不读"的缺口。

**Why this priority**: 这是 D3 决策的落地,也是纯 Python 环境下证据层的最低可用性保障(无 Node 时仍有两条泳道可用);依赖 US2 的合同先就绪。

**Independent Test**: 对既有 teams 运行工件与全部存量 feedback 条目(动态计数)执行 collect,两条泳道的证据出现在 findings.json 中且经过脱敏;compare 能对同一目标前后两次 findings 产出差异摘要。

**Acceptance Scenarios**:

1. **Given** 项目存在 teams 运行工件, **When** 采集 runs 泳道, **Then** 团队级执行结果(运行报告、Critique 要点)规范化为证据条目,manifest 记录扫描的团队数。
2. **Given** 存量 feedback 条目中同一优化点重复出现 N 次, **When** 采集 feedback 泳道, **Then** 对应证据条目带 recurrence 信号,引用指向条目相对路径。
3. **Given** 无 Node 环境, **When** 执行 collect --lanes all, **Then** runs/feedback 两条泳道正常产出,三条 Node 泳道显式降级——公共流程在纯 Python 环境保有最低可用性。

---

### User Story 4 - collect-evidence 公共技能与标准证据步骤 (Priority: P2)

作为任意上层技能/命令的使用者,我可以调用 `collect-evidence` 技能完成一次证据采集编排:解析范围(目标单元、泳道、时间窗、深度、平台)→ doctor 呈现能力表 → collect 呈现按 evidenceState 分布的摘要 → 明确申明 Unobserved 项与不可用泳道。同时,`.specify/shared/workflow/evidence-step.md` 以单一事实源定义与 feedback-step 对偶的标准"证据步骤"块,供全部消费技能引用。

**Why this priority**: 这是证据层的公共入口与消费约定;依赖 US2/US3,但独立于任何具体消费者可验证。

**Independent Test**: 技能独立运行一次完整编排并输出边界申明;技能自身不解读证据、不提任何优化建议;`skills/` 与 `.specify/skills/` 双镜像 `diff -rq` 通过;Skills 注册表登记。

**Acceptance Scenarios**:

1. **Given** 用户调用技能并指定目标单元, **When** 编排执行, **Then** 依次完成范围解析、doctor 能力表展示、collect 与摘要呈现、边界申明四步,并以标准 feedback-step 收尾。
2. **Given** 采集结果含 Unobserved 项或不可用泳道, **When** 技能输出, **Then** 边界申明如实列出,不出现任何"缺陷/建议/严重度"表述(证据层对消费者中立红线)。
3. **Given** 技能落库, **When** 校验格式, **Then** 符合技能格式规范(frontmatter、Path Conventions、Resources、Dependencies、500 行内、双镜像一致)。

---

### User Story 5 - improve-* 三技能接入证据驱动范式 (Priority: P2)

作为技能优化流程的执行者,我使用改造后的 improve-skills / improve-agent / improve-team:优化前先走标准证据步骤(采集或复用 7 天内证据),按 evidenceState 分拣候选(Exercised/Outcome-supported 负向证据 → 缺陷候选;Missing → 机制缺失候选;Present/Wired 未 Exercised → 配而未用候选;Unobserved → 只记录禁止当缺陷修),候选清单冻结后进入各技能自有的根因分析与定向修改流程;improve-team 不再自行解析原始运行工件,改为消费 runs 泳道证据。

**Why this priority**: 这是移植的直接业务价值——把 improve 流程从"LLM 回忆"升级为"证据驱动";依赖 US2~US4 全部就绪。

**Independent Test**: 对 improve-skills 自身跑一次完整"采集 → 分拣 → 优化 → 验证"闭环;三技能的 SKILL.md 均含证据步骤与 Unobserved 红线;既有失败模式分类法、最小变更、双镜像等纪律不受破坏。

**Acceptance Scenarios**:

1. **Given** 三技能改造完成, **When** 检查 SKILL.md, **Then** 均引用 evidence-step.md 单一事实源(不复制定义),均写明"Unobserved 不得当缺陷修"红线,且行数不超过 500 行、双镜像一致。
2. **Given** 一次 improve 运行, **When** 证据审读完成、候选清单冻结, **Then** 后续步骤不得增删候选(防"想修什么就把什么说成证据");计数类信号不得直接生成优化点。
3. **Given** improve-team 改造后, **When** 执行团队优化, **Then** 其运行工件输入全部来自 runs 泳道证据,不再直接解析 STATE.md / run-log.jsonl 原文。
4. **Given** 三技能既有能力, **When** 对比改造前后, **Then** 各自保留项(失败模式八分类、六节结构分析法、Refinement Map、结构保持编辑等)全部完好。

---

### User Story 6 - 纵向验证闭环(干预台账 + 前后对比) (Priority: P3)

作为优化质量的守门人,我要求每次 improve 定向修改后记录干预台账(目标发现、变更、基线运行、预期信号);下一轮同目标证据采集后用 compare 对比前后 findings:预期信号改善则干预标注 Outcome-supported,无可比数据则保持 Unobserved——任何干预不得在缺乏证据对比时自称"已修复"。

**Why this priority**: 补上 Spec Kit 最大的方法论缺口(优化效果从未被纵向验证);依赖两轮真实 improve 运行,故排在核心链路之后。

**Independent Test**: 第一轮 improve 产出干预台账;第二轮同目标采集后 compare 引用第一轮干预并给出 Outcome-supported / Unobserved 判定。

**Acceptance Scenarios**:

1. **Given** 一次定向修改完成, **When** 写入干预台账, **Then** 台账含目标发现、变更描述、基线运行标识与预期信号四要素。
2. **Given** 第二轮同目标证据就绪, **When** 执行 compare, **Then** 输出前后差异摘要;预期信号改善 → 干预标 [[STR-004]];无可比数据 → 保持 [[STR-006]],流程不得输出"已修复"结论。

---

### User Story 7 - 多 CLI 平台适配器扩展(D2,持续) (Priority: P4)

作为 Spec Kit 维护者,我按"先用 doctor 探测各工具本地落盘现状再定序"的原则,逐个自研缺失平台的会话适配器与资产 provider(候选顺序 opencode → Qwen → iFlow → Hermes → Copilot;Claude 的会话适配器与资产 provider 上游代码已存在但官方未背书,定位为**核实与补齐缺口**而非从零自研),使 doctor 能力表逐步点亮八种受支持工具;探测不到本地落盘的工具,session 泳道直接如实标不可用。

**Why this priority**: 长尾持续演进项,不阻塞核心链路;每个适配器可独立交付、独立验证。**本需求(spec 034)的交付边界止于 US1–US6 + 本故事的 doctor 探测报告与定序建议**;新适配器的实现属后续独立迭代,不作为本需求的完成判定条件(引擎自带的 qoder/codex/claude/cursor 适配器按现状使用)。

**Independent Test**: 每个新适配器附最小 fixture 测试;其输出走既有脱敏漏斗(不得绕过);能力缺口显式标注(如时间戳覆盖 partial)。

**Acceptance Scenarios**:

1. **Given** 一个新平台适配器交付, **When** 运行其 fixture 测试与一次真实采集, **Then** 输出符合证据合同、经过脱敏、缺口字段显式标注。
2. **Given** 某工具本地不落盘会话, **When** doctor 探测, **Then** 该平台 session 泳道标 [[STR-010]],不虚构证据。

---

### Edge Cases

- **上游分叉漂移**:复制即分叉,上游修 bug 不自动获益——UPSTREAM.md 锚定基线 commit,定期(建议每季度)对采集子集 diff 审阅、按文件择优回移;禁止追求自动合并。
- **子集边界侵蚀**:后续有人"顺手"复制上游渲染/评分/裁决代码——证据纪律文档写明"采集子集只进事实,不进观点",UPSTREAM.md 子集清单作为审计依据。
- **Node 环境缺失**:三条 Node 泳道显式降级,runs/feedback 纯 Python 泳道保底;doctor 如实报告,collect 不崩溃。
- **证据超龄**:latest 返回超过时效阈值的证据时必须警告;消费方可选择复用或重采,但不得静默使用超龄证据。
- **空证据源**:目标单元无任何会话/运行/反馈数据时,各泳道如实产出空证据集(状态 available、证据数 0)或 unavailable,不得编造样例证据。
- **隐私穿透**:新适配器绕过脱敏漏斗直接输出原文——评审红线,任何泳道落盘前经引擎侧脱敏 + Python 侧白名单二次过滤双闸。
- **消费层越界**:collect-evidence 技能或证据引擎输出优化建议/严重度——违反两层分离判据,证据层对消费者保持中立。
- **候选清单事后膨胀**:improve 流程在候选冻结后新增"证据"——红线,防止"想修什么就把什么说成证据"。
- **镜像漂移**:`skills/` 与 `.specify/skills/` 双镜像、`scripts/js/` 与 `.specify/scripts/js/` 全量镜像(FR-014)——任何一侧单改即为缺陷,验收用 `diff -rq` 校验。
- **root 属主目录**:当前 `scripts/js/` 为 root 属主空目录,落库前需以当前用户重建,避免不可写(既有环境 gotcha)。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 框架 MUST 将 Better Harness 采集子集以源码复制方式托管于 `scripts/js/better-harness/`,保持上游相对路径结构(使交叉导入原样成立);子集范围 MUST 限于证据事实采集能力(会话分析、项目画像/历史信号、资产清单 provider、资产基线三信封 lint/inventory/integrity、可选依赖治理),MUST NOT 包含上游裁决/呈现层(lead 分析器、evidence-bundle 门面、渲染链、checkup 变更器、根门面、打包、hooks、建议目录);子集 MUST 零 npm 外部依赖(仅 Node 内置模块)。
- **FR-002**: 托管目录 MUST 含 UPSTREAM.md(源仓库、基线 commit `b2e621d`、复制日期、子集清单、本地修改日志——每次本地修改追加一行:文件、动机、是否可回馈上游)与上游 LICENSE(MIT)副本;与上游的再同步 MUST 为手动、按文件、diff 驱动。
- **FR-003**: 框架 MUST 提供确定性证据编排引擎(`.specify/scripts/python/evidence-utils.py`,Python stdlib-only,风格与 feedback-utils.py 一致),命令面至少含:doctor(能力表:Node 版本、按支持矩阵探测的可用平台、五泳道可用性)、collect(按泳道/目标/时间窗/深度/平台采集)、list(历史证据运行)、latest(最近一次 findings 路径,时效阈值默认 7 天、超龄警告)、compare(同目标前后两次 findings 差异摘要);对 Node 子进程的调用 MUST 使用参数数组且不经 shell。
- **FR-004**: 证据产出 MUST 规范化为统一合同并落盘 `.specify/memory/evidence/<run-id>/`:findings.json(schemaVersion、kind [[STR-011]]、目标单元、runId、时间窗、实际采集平台、五泳道状态、证据条目数组、findingsDigest 校验和)+ lanes/*.json + manifest.json,并维护存储索引;每条证据 MUST 含泳道、evidenceState、摘要、不可逆引用(哈希或相对路径)、信号计数;合同 MUST NOT 含上游裁决字段(五维评分、严重度、修复建议、支持轨道)。
- **FR-005**: evidenceState MUST 全量采用七态词汇 [[STR-001]]~[[STR-007]](语义随证据纪律文档移植上游定义),任何消费方 MUST NOT 裁剪或重定义状态语义;泳道状态 MUST 采用 [[STR-008]]/[[STR-009]]/[[STR-010]] 三值,某泳道失败时 MUST 显式标注后继续(放宽上游"一泳道失败即整束失败"),MUST NOT 静默降级或编造。
- **FR-006**: 五泳道 MUST 为:session(会话执行行为)、project(仓库结构/历史信号)、assets(已配置资产清单与 lint)三条经 Node 引擎采集;runs(teams 运行工件:runs/ 报告、STATE.md Post-Run Critique、run-log.jsonl)与 feedback(`.specify/memory/feedback/` 条目,重复优化点带 recurrence 信号)两条为纯 Python 原生实现——无 Node 环境时后两条 MUST 保持可用。
- **FR-007**: 全部证据落盘 MUST 满足隐私纪律:不含原始 prompt/命令原文/私有绝对路径/密钥;Node 泳道走上游三层脱敏漏斗,runs/feedback 泳道经 Python 侧脱敏(密钥模式、绝对路径掩码),落盘前 MUST 施加字段白名单二次过滤;`.specify/memory/evidence/` MUST 排除出 feedback 打包范围。
- **FR-008**: 框架 MUST 提供 `collect-evidence` 公共技能(符合技能格式规范、双镜像、注册表登记),编排范围解析 → doctor → collect → 边界申明(明示 Unobserved 项与不可用泳道)并以标准 feedback-step 收尾;技能 MUST NOT 解读证据或输出优化建议/严重度(证据层中立红线);MUST 提供证据合同人读版与证据纪律参考文档(四纪律 + 七态词汇表)。
- **FR-009**: 框架 MUST 在 `.specify/shared/workflow/evidence-step.md` 以单一事实源定义标准证据步骤(采集或复用时效内证据 → 按 evidenceState 分拣候选 → 候选冻结),各消费技能 MUST 仅引用不复制;分拣规则 MUST 为:Exercised/Outcome-supported 负向证据 → 缺陷候选;Missing → 机制缺失候选;Present/Wired 未 Exercised → 配而未用候选(先查路由再考虑裁撤);Unobserved → 只记录,MUST NOT 当缺陷修;候选清单冻结后 MUST NOT 增删;计数信号 MUST NOT 直接生成优化点。
- **FR-010**: improve-skills / improve-agent / improve-team MUST 接入标准证据步骤(各自 30~60 行级改动,遵守 500 行上限与双镜像校验),既有自有流程(失败模式分类法、六节结构分析法、Refinement Map、最小变更、结构保持编辑等)MUST 保留;improve-team 的运行工件读取 MUST 下沉为消费 runs 泳道证据,MUST NOT 再直接解析原始工件;严重度/建议体系 MUST 由消费层自有定义,上游五维评分体系 MUST NOT 移植。
- **FR-011**: 每次 improve 定向修改后 MUST 写入干预台账(目标发现、变更、基线运行标识、预期信号);下一轮同目标证据采集后 MUST 经 compare 判定:预期信号改善 → 干预标 [[STR-004]];无可比数据 → 保持 [[STR-006]];MUST NOT 在缺乏前后证据对比时宣称"已修复"。
- **FR-012**: 平台适配器扩展 MUST 作为自有演进面持续推进:新会话适配器 MUST 实现既定分析器扩展点并优先采用上游较新的 provider-runner 模式,新资产 provider MUST 注册进既有分发表;每个新适配器 MUST 走既有脱敏漏斗、显式标注能力缺口、附最小 fixture 测试;实施顺序 MUST 以 doctor 对各工具本地落盘现状的探测结果定序(候选顺序 opencode → Qwen → iFlow → Hermes → Copilot);各平台的现有支持程度 MUST 以上游**源码探测结果**为判定依据,MUST NOT 依赖上游 roadmap 文档声明(二者已知不一致:Claude 的会话适配器与资产 provider 源码均已存在并注册,而上游文档称其缺失)。
- **FR-013**: 测试 MUST 双轨:上游摘取的引擎子集测试落 `tests/js/`(node --test 风格,可由包装脚本纳入 CI);pytest 侧 MUST 增加合同测试(doctor/collect 产出的 findings.json 合同校验),主测试栈保持 pytest。
- **FR-014**: `scripts/js/` MUST 遵循现行镜像模型全量双写:`scripts/js/better-harness/` ↔ `.specify/scripts/js/better-harness/`,零例外规则,以 `diff -rq` 校验字节一致;引擎体积(约 1.0 MB 纯文本)不构成例外理由——下游项目经框架安装获得的是 `.specify/` 侧拷贝,全量镜像是证据引擎随框架分发的前提。

### Key Entities

- **采集引擎子集(Engine Subset)**: 从上游复制托管的 Node 采集能力集合,受 UPSTREAM.md 溯源台账与子集边界约束;只产证据事实,不产观点。
- **证据运行(Evidence Run)**: 一次采集的产物单元,目录 `.specify/memory/evidence/<run-id>/`,含 findings.json、lanes/*.json、manifest.json;由存储索引统一管理。
- **证据合同(findings.json)**: 公共层与消费层的边界契约:目标单元、时间窗、平台、五泳道状态、证据条目(泳道、evidenceState、摘要、不可逆引用、信号)、findingsDigest;剥离一切裁决字段。
- **evidenceState 七态**: 证据观察状态词汇([[STR-001]]~[[STR-007]]),全量移植、语义不可重定义;消费方只可自定义响应方式。
- **泳道(Lane)**: 证据来源通道,共五条(session/project/assets/runs/feedback),各自带 [[STR-008]]/[[STR-009]]/[[STR-010]] 状态;runs/feedback 为 Spec Kit 自有一等泳道。
- **证据步骤(Evidence Step)**: 共享工作流约定(单一事实源),定义消费技能"采集/复用 → 分拣 → 候选冻结"的标准流程与 Unobserved 红线。
- **干预台账(Intervention Ledger)**: 每次 improve 定向修改的记录(目标发现、变更、基线运行、预期信号),是纵向验证(compare → Outcome-supported 判定)的输入。
- **平台适配器(Platform Adapter)**: 各 AI 工具的会话适配器与资产 provider;Spec Kit 自有演进面,受脱敏漏斗、缺口显式标注与 fixture 测试约束。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 引擎子集落库后,摘取的 `tests/js/` 子集测试 100% 通过;在 Spec Kit 仓库手动运行会话分析与项目画像 CLI 各一次均产出合法 JSON;UPSTREAM.md 与 LICENSE 存在且清单与实际目录一致。
- **SC-002**: `collect --lanes all` 产出的 findings.json 100% 通过 pytest 合同测试;抽查证据条目中裁决字段(评分/严重度/建议)零出现;evidenceState 取值 100% 落在七态词汇内。
- **SC-003**: 无 Node 环境演练:doctor 正确报告三条 Node 泳道不可用,collect 仍产出含 runs/feedback 证据的 findings.json,全程零崩溃、零编造(降级泳道 100% 显式标注)。
- **SC-004**: 存量证据源接入:采集时点实际存在的全部 feedback 条目(以反馈索引动态计数为准)与既有 teams 运行工件 100% 进入 findings(经脱敏抽查零原文泄漏);重复优化点的 recurrence 信号与人工盘点结果一致。
- **SC-005**: collect-evidence 技能独立运行一次完整编排,输出含边界申明;技能文本中优化建议类表述零出现;`diff -rq` 双镜像校验通过;技能格式规范逐项符合。
- **SC-006**: 对 improve-skills 自身完成一次"采集 → 分拣 → 优化 → 台账"完整闭环;三技能 SKILL.md 100% 引用 evidence-step.md 且含 Unobserved 红线;改造后三技能各自既有保留项经 diff 复核 100% 完好;improve-team 运行中对原始工件的直接解析零出现。
- **SC-007**: 第二轮同目标 improve 运行中,compare 成功引用第一轮干预台账并给出 Outcome-supported 或 Unobserved 判定;全程"已修复"类无证据结论零出现。
- **SC-008**: 本需求交付边界内:doctor 对八种受支持工具的本地落盘现状产出探测报告与扩展定序建议,一次通过。后续迭代口径(不计入本需求完成判定):每个新交付的平台适配器 fixture 测试 100% 通过、脱敏漏斗零绕过、能力缺口字段显式存在,doctor 能力表准确反映其上线状态。

### Measurement Sources & Collection Methods

- **SC-001 Source**: `tests/js/` 运行输出 + 两次手动 CLI 演练记录 + UPSTREAM.md 清单与实际目录 diff 核对。
- **SC-002 Source**: pytest 合同测试(`pytest -m contract`)输出 + findings.json 字段抽查记录(verification 记录)。
- **SC-003 Source**: 隔离环境(无 Node)演练记录:doctor 输出、collect 产物与 manifest 泳道状态核对。
- **SC-004 Source**: 采集产物与 `.specify/memory/feedback/` 索引条数比对 + 脱敏抽查记录 + recurrence 信号与人工盘点对照表。
- **SC-005 Source**: 技能演练记录 + `diff -rq skills/collect-evidence .specify/skills/collect-evidence` 输出 + 技能格式核查单。
- **SC-006 Source**: improve-skills 闭环演练记录 + 三技能 SKILL.md 静态扫描(引用存在性 + 红线文本)+ 改造前后 SKILL.md diff 复核。
- **SC-007 Source**: 两轮 improve 运行的干预台账与 compare 输出存档(verification 记录)。
- **SC-008 Source**: 各适配器 fixture 测试输出 + 采集产物脱敏抽查 + doctor 能力表快照。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "Present" | FR-005、证据合同、纪律参考文档、合同测试 |
| `STR-002` | "Wired" | FR-005、证据合同、纪律参考文档、合同测试 |
| `STR-003` | "Exercised" | FR-005/FR-009、证据合同、合同测试 |
| `STR-004` | "Outcome-supported" | FR-005/FR-011、证据合同、compare 判定、合同测试 |
| `STR-005` | "Missing" | FR-005/FR-009、证据合同、合同测试 |
| `STR-006` | "Unobserved" | FR-005/FR-009/FR-011、红线表述、合同测试 |
| `STR-007` | "Not applicable" | FR-005、证据合同、合同测试 |
| `STR-008` | "available" | FR-005、manifest 泳道状态、合同测试 |
| `STR-009` | "partial" | FR-005、manifest 泳道状态、适配器缺口标注 |
| `STR-010` | "unavailable" | FR-005、manifest 泳道状态、降级演练断言 |
| `STR-011` | "speckit.evidence-findings" | FR-004、findings.json kind 字段、合同测试 |

**Citation convention**: 下游产物引用以上字面量时写 `[[STR-NNN]]`,不重新誊写。

## Assumptions

- **方案文档为已评审设计输入**:`draft/2026-07-29-better-harness-evidence-port-plan.md`(Draft v2)的三项已定决策(D1/D2/D3)、子集边界(§3.1)与不移植清单(§8)作为本需求的既定约束直接采纳,不再重新开放讨论;方案中的剩余开放问题按下列口径处理。
- **走完整 SDD 流程**(方案开放问题 3):用户以 `/speckit.requirements` 启动即为决断——按规格 → 计划 → 任务的完整链路推进,而非直接 P1 起步。
- **证据时效阈值默认 7 天**(方案开放问题 2):作为默认值采纳,允许调用方覆盖;若后续实践证明不合适再调整,不作为澄清项。
- **平台扩展顺序以 doctor 探测定序**(方案开放问题 4):候选顺序仅为初始假设,最终以各工具本地落盘现状的探测结果为准(已纳入 FR-012)。
- **历史会话为分析参考而非事实源**:用户指定的 better-harness 历史会话(1261e61e)已经 subagent 提取核实——方案的子集边界、零 npm 依赖、交叉导入、七态词汇、分发表与扩展点声明均属实;修正两点:平台支持现状以源码探测为准(上游文档滞后,见 FR-012),扣除不复制的 checkup 后子集实际约 1.0 MB。
- **存量计数为时点值**:"48+ 条 feedback""既有 teams 运行"等数字是撰写时点观测值,验收时 MUST 以运行时动态探测的实际数量为准,不得硬编码计数断言(既有测试基线纪律)。
- **上游许可证兼容**:上游为 MIT 许可,源码复制托管附 LICENSE 与溯源记录即满足合规要求。
- **`scripts/js/` 现状**:该目录当前为空(root 属主),无既有内容冲突;落库前需以当前用户重建目录权限(既有环境 gotcha)。
- **术语对齐**:"泳道(Lane)""证据合同(Evidence Contract)""干预台账(Intervention Ledger)"为本需求新引入术语,待词汇表收尾提案;"双镜像""feedback-step""调谐"沿用项目既有语义。

## Clarifications

<!-- 
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->

### Session 2026-07-29

- Q: 本需求应绑定哪个 Feature(索引中无证据基础设施相关条目)? → A: 新建 Feature 038 "Evidence Infrastructure"(Status: Draft);028 Feedback / 027 Team Management / 013 Skills 作为数据源/消费者关联而非归属。
- Q: `scripts/js/` 引擎子集的镜像策略(全量镜像 vs 例外规则 vs 反向单源)? → A: 全量镜像 `scripts/js/` ↔ `.specify/scripts/js/`,零例外——下游项目安装获得 `.specify/` 侧拷贝,全量镜像是引擎随框架分发的前提;体积(约 1.0 MB)不构成例外理由(FR-014 已定稿)。
- Q: 本需求的交付验收边界(US7 平台扩展定界)? → A: 核心链路 + 零新增适配器——US1–US6 为交付边界,US7 仅交付 doctor 探测报告与定序建议;新适配器实现留后续独立迭代(引擎自带 qoder/codex/claude/cursor 适配器按现状使用);SC-008 相应拆分为边界内/后续迭代两段口径。
