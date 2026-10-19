# 源需求归档（dated record）— Feature 062 Humanize Command（人性化改写命令）

- **归档日期**: 2026-10-19
- **性质**: dated record — 需求语义权威与源需求原文在 requirements 修复轮 1（D-01 裁定）的逐字存档；本文件归档后不再更新。当前需求语义以 [../requirements.md](../requirements.md) 及其 `## Clarifications` 为准。
- **来源**: `/tmp/sdd-humanize/brief.md`（requirements 阶段的语义权威）与 `/tmp/req.txt`（源需求原文，brief § 源需求原文逐字收录）。两份 `/tmp` 路径为临时目录，仅在此保留为 provenance 注记；仓内权威引用一律指向本文件。
- **收录方式**: 下方两节为两个源文件在归档时刻的逐字内容（fenced block 原样保留，不做任何改写或增删）。

## brief.md（2026-10-19 快照，逐字收录）

````markdown
# Brief — 新增 `/speckit.humanize` 命令（requirements 阶段输入）

## 任务

在目标项目 `/storage/project/cloud-native-ai/spec-kit` 中开发一个新的框架命令 `/speckit.humanize`。
主要功能：将一些内容、结论或外部文档进行**人性化描述改写**（humanize）。
本阶段（REQUIREMENTS）只产出本特性的 `requirements.md` 与质量检查单，不进入实现。

## 源需求原文（/tmp/req.txt，逐字收录）

在 AI、内容创作和数据报告的语境下，**"humanize"（拟人化 / 人性化）** 确实被广泛用来指代你所描述的这个过程。

具体来说，将机器输出的内容 "humanize" 通常包含以下几个核心操作，完全契合你的理解：

### 1. 语气与风格的自然化 (Naturalizing Tone)
*   **去除机械感**：消除 AI 常见的套话（如 "In conclusion", "It is important to note"）、过度重复的句式或过于绝对/冷漠的表达。
*   **注入情感或个性**：根据目标读者，调整为专业、幽默、同理心或口语化的语气，使其读起来像是一个有经验的真人专家写的。

### 2. 细节补充与逻辑连贯 (Contextual Enrichment)
*   **填补逻辑跳跃**：机器生成的报告有时缺乏背景信息。Humanize 的过程会补充必要的上下文、具体的例子或过渡句，让推导过程更符合人类的思维习惯。
*   **化抽象为具体**：将干瘪的数据或术语，转化为带有业务场景或实际意义的描述。

### 3. 格式与视觉体验优化 (Formatting for Readability)
*   **符合人类视觉习惯**：机器有时会输出大段密集的文字。Humanize 会主动将其拆分为短段落，合理使用**加粗**、*斜体*、项目符号（Bullet points）和清晰的标题层级。
*   **突出重点**：将核心结论前置（如采用金字塔原理），而不是让读者在长篇大论中寻找答案。

### 4. 降低 "AI 痕迹" (Reducing AI Footprint)
*   在当前的实际应用中，"humanize" 还经常特指修改文本，使其在词汇多样性（Burstiness）和句子长度变化（Perplexity）上更接近真人写作，从而更好地通过各类 "AI 内容检测器" 的审查。

---

### 💡 相关的实用表达与工具名称
如果你在实际工作或搜索中需要使用这个概念，可以参考以下地道表达：
*   **AI Humanizer**：目前市面上有很多专门做这个功能的工具，就直接叫这个名字（AI 文本拟人化工具）。
*   **Human-like text / Human-sounding text**：类人文本 / 听起来像真人写的文本。
*   **Polish and humanize the report**：润色并使报告更具人性化（非常地道的职场指令）。
*   **Make it sound more natural/human**：让它听起来更自然/更像人话（日常沟通中最常用的说法）。

**总结**：你的直觉非常敏锐，完全抓住了这个词在当前技术语境下的核心精髓。只要记住正确的拼写是 **humanize** 即可！

## 入口意图解读（供 requirements 提炼，不是既定设计）

- 命令名固定为 `/speckit.humanize`。
- 输入形态至少覆盖：用户直接给出的一段内容/结论/报告；指向某个外部文档的路径（Markdown、纯文本等，具体范围由 requirements 裁定）。
- 输出：改写后的人性化文本；是否原地覆盖、是否写出新文件，由 requirements 给出明确行为与安全默认。
- 改写的四个维度来自源需求：语气与风格自然化、上下文与逻辑补全、格式与可读性优化、降低 AI 痕迹（以词汇与句式多样性实现，不承诺任何检测器必然通过）。
- 语气/受众应当可由调用者指定（专业、幽默、共情、口语化等），未指定时有合理默认。
- **保真底线**：不得改变原文的事实、数字、结论与引用关系；补充上下文不得编造事实；与"降低 AI 痕迹"冲突时保真优先。
- 输入语言保持：中文输入输出中文，英文输入输出英文（混合语言按主语言处理）。
- 该命令属于 spec-kit 框架自身能力，需遵循现有命令架构、文档与测试惯例，并登记进特性注册表。

## 项目上下文与约束

- 目标项目是 spec-kit 框架源码仓库，同时拥有 `.specify/` 客户端运行时（"两顶帽子"纪律见 AGENTS.md / 宪法 XI）。
- 命令体系现行架构：`templates/commands/*.md` 是命令模板；命令作为薄入口，执行流委派给 `skills/`（external 或 internal）下的技能（057 命令技能化分解的既有做法）。新增命令必须与既有模式一致，而不是发明新机制。
- 文档：`docs/reference/commands/` 是逐命令文档的落点；根文档索引与 Documentation Map 可能需要同步（由 plan/tasks 裁定）。
- 测试：`tests/contract/`、`tests/integration/` 等；宪法 IV 要求测试先行，命令/模板类特性可按 VII 的 template-only 门正当化。
- 注册与分发：命令模板需要随 `specify init` 分发到各受支持 AI 工具；相关拷贝/注册机制需在 requirements/plan 中查明（不要臆造）。
- 宪法要点：XIV 单一事实源（引用而非复述）、XV 用户可理解输出、IX 框架非运行时（不新增运行时服务）、XI Dogfooding（本次开发即自应用）。
- 不新增外部服务、网络依赖或第三方包；改写由执行该命令的 AI agent 自身完成。

## 本阶段完成判据

- 在 `.specify/specs/<新分支>/requirements.md` 写出可验证的 requirements（用户故事、FR、SC、边界与假设）。
- 运行项目既有的 requirements 校验器并修复到通过。
- 产出质量检查单（按命令工作流）。
- 只提交本特性产物；不 push；不改动无关文件。
````

## req.txt（2026-10-19 快照，逐字收录）

````text
在 AI、内容创作和数据报告的语境下，**"humanize"（拟人化 / 人性化）** 确实被广泛用来指代你所描述的这个过程。

具体来说，将机器输出的内容 "humanize" 通常包含以下几个核心操作，完全契合你的理解：

### 1. 语气与风格的自然化 (Naturalizing Tone)
*   **去除机械感**：消除 AI 常见的套话（如 "In conclusion", "It is important to note"）、过度重复的句式或过于绝对/冷漠的表达。
*   **注入情感或个性**：根据目标读者，调整为专业、幽默、同理心或口语化的语气，使其读起来像是一个有经验的真人专家写的。

### 2. 细节补充与逻辑连贯 (Contextual Enrichment)
*   **填补逻辑跳跃**：机器生成的报告有时缺乏背景信息。Humanize 的过程会补充必要的上下文、具体的例子或过渡句，让推导过程更符合人类的思维习惯。
*   **化抽象为具体**：将干瘪的数据或术语，转化为带有业务场景或实际意义的描述。

### 3. 格式与视觉体验优化 (Formatting for Readability)
*   **符合人类视觉习惯**：机器有时会输出大段密集的文字。Humanize 会主动将其拆分为短段落，合理使用**加粗**、*斜体*、项目符号（Bullet points）和清晰的标题层级。
*   **突出重点**：将核心结论前置（如采用金字塔原理），而不是让读者在长篇大论中寻找答案。

### 4. 降低 "AI 痕迹" (Reducing AI Footprint)
*   在当前的实际应用中，"humanize" 还经常特指修改文本，使其在词汇多样性（Burstiness）和句子长度变化（Perplexity）上更接近真人写作，从而更好地通过各类 "AI 内容检测器" 的审查。

---

### 💡 相关的实用表达与工具名称
如果你在实际工作或搜索中需要使用这个概念，可以参考以下地道表达：
*   **AI Humanizer**：目前市面上有很多专门做这个功能的工具，就直接叫这个名字（AI 文本拟人化工具）。
*   **Human-like text / Human-sounding text**：类人文本 / 听起来像真人写的文本。
*   **Polish and humanize the report**：润色并使报告更具人性化（非常地道的职场指令）。
*   **Make it sound more natural/human**：让它听起来更自然/更像人话（日常沟通中最常用的说法）。

**总结**：你的直觉非常敏锐，完全抓住了这个词在当前技术语境下的核心精髓。只要记住正确的拼写是 **humanize** 即可！
````
