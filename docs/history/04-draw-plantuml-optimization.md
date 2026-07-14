# 04 · draw-plantuml 技能长期优化

> 覆盖会话:`ee7d6b0a`(k8s 打分迭代 + EEI 特性起源)、`037a7e53`(五种专项图 + 离线渲染)、`eac5d261`(精英进化 + team/sdd-workflow 衍生)、`c243363f`(复杂图进化起点)、`fe67eaef`(跨机 patch 同步)。时间跨度 2026-07-02 → 2026-07-14。
>
> 这是最富含**可复用 PlantUML 技巧**的主题。与 [[reference_plantuml-offline-render]]、[[feedback_plantuml-layout-techniques]] 两条记忆强相关。

## 一、工作方法:打分-迭代 / 精英进化循环

统一模式——用多 subagent 做"绘制 → 打分 → 改技能"的闭环迭代:

- **三角色分工**:drawer(执行绘制)/ scorer(打分)/ optimizer(改技能本身)。**上下文隔离**是关键:评估者不看执行者的 prompt,执行者每轮重新加载最新技能。→ 这套三角色循环后来被抽象为 Spec Kit 的 **EEI(Executor-Evaluator-Improver)三元组特性**(Feature 022,见 [[01-agent-system-evolution]])。
- **评分维度**:正确性 60% + 美观 40%(整洁=对齐+嵌套,归入美观);<60 判失败必须改技能重画;>90 停止。用固定 `RUBRIC.md` + expected-element checklist 保证 scorer 一致性。
- **draw agent 只"重塑"canonical 图不改内容**(eac5d261/c243363f):保持元素恒定,剔除正确性噪声,专注优化布局/美观(真正目标)。
- **精英进化**(eac5d261):每轮淘汰最低分,用最高分 agent 复制+换优化方法,≥5 代,收敛(连续 2 代无提升)或达标才停。

### 重要事实:分数是波动的

不同 scorer agent 之间同一版本可能 ±2–3 分甚至更大(81.6 vs 67.2)。**不能靠单次分数判断趋势,要看多轮均值。** 模型曾因"89-90 + 打分波动 ≈ 达标"想收尾,被用户/Stop-hook 否决后继续迭代到真正 >90(见冲突点)。

## 二、可复用 PlantUML 技巧(已验证,已写入技能)

### 布局(layout)
- **横向(LTR)布局对 k8s 这类中心-边缘图始终优于纵向(TTB)**:反复验证的稳定结论。TTB 下 ortho 箭头路由更差(reconcile 弧线跑出框、ClusterIP 对角穿框)。
- **语义驱动布局(核心突破)**:绘图前先做组件语义角色分类(Hub/Edge/Peer/Entry/Sink),由"中心-节点一对多"语义自然推导布局,而非写完 PlantUML 再被动调。加入后正确性一次突破 90。→ 已作为 SKILL.md "Step 3: Semantic Layout Planning" / "Step 0: Semantic Analysis"。
- **方向/宽高比先决**:宽浅结构→`top to bottom`,深窄→`left to right`(layout.md 决策表)。
- **近方形网格列数公式** `C ≈ round(√(N×1.3))`。
- **过量空白是首要美观扣分点**:baseline SVG viewBox 曾达 37837×35450 极度稀疏,逼迫 PNG 缩小使文字变小。"一条长边会拉伸整个画布"——跨集群长边(如 `apiserver→kubelet`)是画布畸变主因,有诊断表。
- **嵌套清晰规则**:每层固定容器类型、嵌套 ≤4 层、每容器单一方向、消除单子节点容器、容器标题简短。
- **合并对称重复元素**(如两个 worker node 合成一个代表节点)可把箭头数减半,显著降拥堵。

### 连线与分组
- `-[hidden]->` **隐藏连线**:强制元素定位/分层顺序而不产生可见线。
- `..>` **虚线**:区分控制信号 vs 数据流(report/弱依赖用虚线)。
- `together{}`:把同层 peer 紧凑分组,缩短跨组箭头(如 `together{sched, cm}` 让 Scheduler+ControllerManager 纵向堆叠)。
- `linetype ortho` + 加大 `nodesep`/`ranksep`:工程制图风格;但箭头多时正交线会在节点周围拥堵,需靠间距疏解。

### 专项图(037a7e53:WBS/Gantt/MindMap/JSON/YAML)
- **WBS**:平衡要作用在根的直接子节点(第二层);宽单行根节点可桥接左右两半消除分离感。
- **Gantt**:`zoom 3`(1.38:1 密实)优于 `zoom 4`(空白被摊开);满幅背景带用中浅档(100~200 级)色而非极浅(50 级几乎不可见);跨阶段重叠任务填充瀑布三角空白。
- **MindMap**:`legend top` 色块图例;连线用中灰+略粗+继承主干色。

## 三、渲染管线的坑(高价值)

- **`render-plantuml.sh` 样式注入只匹配 `@startuml`**:专项图以 `@startwbs`/`@startgantt` 开头,导致 `scale`/`dpi` **从未生效**,专项图一直原始 1:1 出图(400–850px);且 `strip_style` 还会删掉作者手写的 `scale`。修复:在任意 `@start…` 标签后注入 scale/dpi。`scale 3 + dpi 200` 可得 2000–4000px。
- **本地 jar 4096px 截断**:需设 `-DPLANTUML_LIMIT_SIZE=16384` 解除,大图才不被 clamp。
- **PlantUML `<style>` 单行块静默丢弃 `BackGroundColor`**:JSON 图自定义高亮类写成单行会丢背景色,**必须每属性一行(多行块)**。
- **渲染脚本会强制注入 `monochrome true`**,覆盖源码颜色;专项图(`@start*` 非 uml)需**跳过 monochrome 注入**保留原生语义配色。
- **PlantUML 服务器兼容性**:`!$` 变量、`<<Stereotype>>` 内联注释在服务器上会渲染失败,不能靠 curl 直连保留彩色代码。
- **中文字体豆腐块**:1.8MB 不完整 Noto 字体渲染成 tofu 方块,需完整 CJK 字体(8.3MB / 31036 glyphs)+ `fc-cache` 重建。**SVG 永远含字符,必须看 PNG 验证**是真字形还是豆腐。
- **离线渲染兜底**:远程服务器不可达时,下载 PlantUML jar(从 Maven Central,比 GitHub CDN 可靠)+ Noto Sans CJK 到 `~/.local`,给 `render-plantuml.sh` 加本地 jar 回退后端(自动探测服务器,失败即回退)。这五种专项图不依赖 Graphviz。放弃了 PicoWeb server 模式(不支持 POST)和 Playwright CJK 管线(更复杂)。详见 [[reference_plantuml-offline-render]]。
- **抓官方文档**:plantuml.com 代码示例在 `<textarea>` 而非 `<pre>`;WebFetch 被屏蔽,用 curl。

## 四、用户 ↔ 模型的冲突/分歧点

| 会话 | 用户主张 | 模型原本 | 最终 |
|------|----------|----------|------|
| ee7d6b0a | 绘图前先做语义布局规划,偏好 v4 风格且打分向其倾斜 | "写完再调布局"的被动方式,盲目试错 | 采纳语义角色分析作为新增 Step;分数突破 90 |
| ee7d6b0a | 条件是">90 分",89.8 不达标(经 Stop hook) | 认为"89-90 + 波动 ≈ 达标"想结束 | 承认不达标,迭代到 v17=91.0 才停 |
| ee7d6b0a | 扩展为覆盖微服务/MQ/CQRS 的通用模板,每个 howto 都优化 | 只写进 best-practices 并反问"需要我做吗" | 落地 3 套架构模板 + 7 个 howto 全优化 |
| 037a7e53 | 成图太小,美观权重提到 60% 且尺寸计入,再跑 ≥5 轮 | 首轮五图均 >90 已达标 | 先定位小图根因(脚本 scale 从未生效),修复后重跑,放大 3–9.6× |
| 037a7e53 | 确认"他人能否复现同等质量" | 认为改动合入源目录即可 | 诚实指出 gap(jar/CJK 字体在 `~/.local` 不进 repo),补写离线环境准备文档并做 clean-room 复现验证 |
| eac5d261 | goal 应能对已存在 team 修改 | 把 goal 定为"Invariant 不变式" | 改为"Deliberately revisable, never drifting"(运行期稳定不漂移,modify 模式可重定义并 realign) |

> 反复出现的模式:**模型倾向"差不多就收尾",用户坚持更高标准并要求定位根因**。多数情况下用户是对的(如小图根因是脚本 bug 而非无法优化)。

## 五、最终产出

- **k8s 架构图**(ee7d6b0a,commit `3b5a21d`):最佳 `output/k8s-arch/17-k8s-infra-v17.png`(91.0 分);SKILL.md 加 Step 3 语义布局;best-practices 加语义驱动布局/隐藏连线/虚线语义章节;3 套架构模板 + 7 个 howto 全升级。
- **五种专项图**(037a7e53,commit `b0e6f30`):WBS 93 / Gantt 91 / MindMap 96 / JSON 94 / YAML 91;5 份 howto(13-17)+ 5 份官方文档缓存;`render-plantuml.sh` 离线硬化;`howto/12 §1.0` 离线环境准备说明。
- **复杂图进化**(eac5d261,未提交):`skills/draw-plantuml/` 的 SKILL.md/layout.md/content.md 更新;胜出图源 `tmp/diagram.puml`;byte-identical 重渲验证。
- **跨机 patch 同步**(fe67eaef):见下节。

## 六、跨机 patch 同步的关键教训(fe67eaef)

在另一台机器上用别的工具优化了 draw-plantuml,产出 patch。**关键发现:`/tmp` 快照是从更旧的 base 分叉的**,本项目 SKILL.md 已有本地新特性(Step 0 语义分析、image-replication triggers、`00-semantic-analysis.md`)是 `/tmp` 没有的。

> **教训:发现"外来快照基于更旧 base"时,绝不能整体覆盖——会摧毁本地新功能。应只 apply patch 的增量(`git apply`,自动吸收 Step 0 造成的行偏移),而非 wholesale copy。** 两份 git 副本(`skills/` + `.specify/skills/`)都要 apply,校验字节一致。

## 七、未完成 / 待办

- ee7d6b0a:EEI 特性 SC-001(收敛率指标)仅 partial(需真实使用数据);分支 `022-eei-agent-triad` 未 push。
- 037a7e53:五张最终 PNG 仍在 `/tmp/plantuml-gallery/`(重启会丢),模型提议拷入 `skills/draw-plantuml/examples/` 长期保留,**用户未回应,未执行**;代码已提交未推送。
- eac5d261:进化产出未提交 git;通用模板可进一步用 `!include` + 变量参数化(已提出未实现)。
- c243363f:该会话进化 workflow 刚启动就被用户中断 `/exit`(后由 eac5d261 接续)。

---

**相关**:[[00-cross-cutting-lessons]] · [[01-agent-system-evolution]](EEI 三元组)· [[05-docs-and-governance]](team goal/sdd-workflow)· [[reference_plantuml-offline-render]] · [[feedback_plantuml-layout-techniques]]
