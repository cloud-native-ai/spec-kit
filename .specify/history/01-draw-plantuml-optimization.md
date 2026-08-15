# 主题：draw-plantuml 技能持续优化（多 Agent 闭环）

覆盖会话：ee7d6b0a (2026-07-02)、fe67eaef (2026-07-02)、037a7e53 (2026-07-07)、c243363f (2026-07-13)、eac5d261 (2026-07-14)、c10b41cf (2026-07-17)。相关：[[00-cross-cutting-lessons]]、[[02-sdd-feature-lifecycle]]（经验固化为 spec 的部分）。

## 1. 关键决策与理由

- **编排形态四代演进**：双角色（draw+score）→ EEI 三角（optimizer→drawer→scorer，每轮重载最新技能，`/goal` Stop hook 执法）→ 进化 workflow（population=3 精英循环，正确性 60/美观 40 rubric）→ team-loop 锦标赛（`draw-plantuml-optimizer` 团队，每代 3 变体并行 + 留优/汰劣/嫁接）。综合效果 49 → 91 分（`17-k8s-infra-v17.png`, C:97/A:82）。
- **评分基准先固定**：基线渲染 + rubric + 期望元素 checklist 先于第一轮；用户偏好风格（ortho 直角线 v4）明确计入评分。权重两次调整：正确性60/美观40 → 美观60（尺寸/布局/配色各 20）/正确性40 → team 版 美观0.40/清晰0.30/正确0.20/心智0.10，后重平衡为 UML保真0.35。
- **核心技能突破 = Step 3 Semantic Layout Planning**：写图前按 Hub/Edge/Peer/Entry/Sink 语义角色分析组件关系推导初始位置；eac5d261 的对应设计是 draw agent 从规范图出发仅 reshape（内容恒定，消除正确性噪声）。
- **离线渲染栈**（037a7e53）：远程 PlantUML 服务器不可达 → 本地 PlantUML 1.2026.6 jar（Maven Central，GitHub CDN 不可靠）+ Noto Sans CJK（~8MB，小字体出豆腐块）放 `~/.local`，`render-plantuml.sh` 自动探测回退。
- **淘汰的方案及理由**：TTB 布局（ortho 下箭头路由更差）、package 分组（内部过宽）、note 补连线（渲染错位拉低分）、隐藏脚手架 hidden link（嵌套 cluster 下净增益 +0.005）、ELK 探针（退回竖版）、文本外置浮动 note（嵌套簇中甩页边）、icon-forward 变体（打平 ~0.900 冗余编码）、1.8MB 小 CJK 字体、Gantt zoom 4（zoom 3 更优）。
- **技能沉淀全部抽象化去基准**：通用占位、删运行数据；拆分 `diagram-principles.md`（通用）与 `large-diagram-playbook.md`（大图专项），SKILL.md 重写为 8 步工作流。
- **外部补丁同步用 `git apply` 而非整份覆盖**（fe67eaef）：/tmp 快照基于更旧基线，整份复制会摧毁本地新增的 Step 0 Semantic Analysis 等特性。

## 2. 可复用经验 / 踩坑

- `render-plantuml.sh` 尺寸根因：scale/dpi 注入只匹配 `@startuml`，专项图（`@startwbs` 等）一直 1:1 出图；修为任意 `@start…` + `-DPLANTUML_LIMIT_SIZE=16384` 后成图 400–850px → 2121–4091px。
- PlantUML 单行 `<style>` 块静默丢弃 `BackGroundColor`——自定义类一行一属性多行写。
- 强制注入 `skinparam monochrome true` 的保色配方：显式 `monochrome false` + legend 内 `<color:>` + 输入输出异名。
- `skinparam linetype ortho` 在嵌套 cluster + 边指向 cluster 节点时确定性崩 GraphViz（回退 spline / 边连叶子）；无 dot 时回退 Smetana；`!pragma layout smetana` 换引擎致退化；服务端不支持 `!$` 变量。
- 箭头方向决定框架位置（`kl --> api` 把 API Server 拉到 kubelet 下方导致 Control Plane 倒置）；hidden link `-[hidden]->` 强制定位、`together{}` 分组、虚线 `..>` 区分控制/数据流。
- 大图必用 SVG（PNG 4096px 硬上限）；结构收缩 > 尺寸压缩；«×N» 语义折叠（1 代表元素+堆叠阴影）优于 N 个同级盒（canvas −18%）。
- SVG 含字符 ≠ PNG 有字形，必须看渲染 PNG 才能发现豆腐块。
- "不确定的自由度是稳定性的敌人"：机械化规则（每行≤5 否则折 2×N 网格、四级字号阶梯）使 3 次重绘极差 0.08 → ~0.01。
- 进化平台期（3 代无提升）= 变异策略池穷尽，须换策略族（如合并跨集群边、拆 legend），加轮数无效。
- 多 agent 产图集须专做一致化 pass（编号冲突/配色/页脚/交叉引用/字号）。

## 3. 未完成 / 待办

- 最终评分图在 `/tmp/plantuml-gallery/`（易失），拷入 `skills/draw-plantuml/examples/` 的提议未执行。
- Gantt 图型两轮均最低 91 分（「封版窗口」标签贴边、右半区拥挤），最值得再补轮。
- `optimization-goals.md` 曾引用不存在的 `docs/team/draw-plantuml-optimization-case.md`（已在 2a38dcaf 修复，见 [[03-framework-mechanics]]）。
- 下一轮持续优化需新基准图 + 新方向；遗留想法：`!include` + 变量做模板参数化复用样式骨架。

## 4. 关键交互流程

- EEI 质量门循环：optimizer 改技能（环境+执行体）→ drawer 重读技能绘图 → scorer 评分 → <阈值继续环，反馈逐轮传递。
- 进化循环（eac5d261）：coordinator → 3 mutator（策略目录选不重复者）→ draw → score → 淘汰最低/克隆胜者；sandbox-then-apply（循环全在 `tmp/evolution/`，胜者复制到双副本后用仓库脚本重渲染验证 bit-identical）。
- team-loop（c10b41cf）：`/speckit.team` → create-team（goal → roster+pattern → 确认 → 持久化）→ run 走 preview→confirm→execute 门 → 每代锦标赛 → 蒸馏进技能指南 → `diff -rq` 三副本校验 → dated run report → 分类提交。

## 5. 用户 ↔ 模型的冲突/分歧点

- 用户主张技能缺全局语义规划、需先做组件语义分析并按 v4 风格调高评分；模型原本只做局部布局微调；最终新增语义布局规划步骤。
- 用户（Stop hook）主张必须严格 >90 分才停；模型认为 89.8 加 ±2-3 波动已"实质达标"；最终迭代至 91.0。
- 用户主张成图太小、美观权重应 60%、尺寸计入、再跑 ≥5 轮；模型原本首轮全 >90 即视为完成；最终修 scale/dpi 根因并重跑 78-agent 工作流。
- 用户主张 gen-3 后应从 UML 语义层提升而非继续绘图技巧；打分标准可能有缺陷需人工核对全部 17 张淘汰图；视觉语义应为一等权重；技能修改必须全抽象无基准专属；多会话反复出现"用户要语义/抽象，模型停在局部/具体"的同构分歧。
- 用户中断 GitHub CDN 下载 jar，要求先激活 venv；最终改 Maven Central。
