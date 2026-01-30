执行控制
有了 Skill 不代表 LLM 就会正确使用。实际跑起来会遇到几个问题：
●
该用的时候不用
●
不该用的时候乱用
●
用错了 Skill
﻿
具体措施
1.
Skill 推荐提示：根据关键词，提示 LLM「检测到 xxx 场景，建议使用 xxx Skill」，但不强制
2.
强制思考：调用 invoke_skill 前必须先用 think 工具说明为什么要用这个 Skill
3.
加载后校验：Skill 加载后，检查 description 和用户问题是否匹配
4.
简单查询识别：「xxx 的 QPS 是多少」这类清单查询，直接走数据查询，不触发 Skill

反思与局限
 7.1 效果层面的挑战
触发不稳定
尽管有 SkillHintProvider 主动推荐、关键词打分、Rerank 语义排序，Skill 的触发率仍然不稳定。LLM 选择不加载 Skill 而是直接查数据。原因很简单：最终决策权在 LLM 手里。我们只能「建议」，不能「强制」。强制加载会破坏 Agent 的灵活性，但不强制就得接受 LLM 的「任性」。有一个老外的分享忘记原文地址了，说他们的 SKILL 触发率不到 10%。。 详细使用 CC 的人也会遇到这个问题，最后就只能把 SKILL 转换成 Command..
不按流程执行
即使 Skill 加载成功，LLM 也不一定按流程走。最常见的问题：
●
跳过「查历史」直接查数据（省事但丢失了历史经验）
●
查到 Trace 列表后不看详情就下结论（「有 50 条慢 Trace」但不分析任何一条）
●
流程走完但结论仍是「可能是 xxx」（Skill 明确禁止的措辞）
Skill 本质是 Prompt，LLM 对 Prompt 的遵循度本身就不是 100%。
审核通过 ≠ 高质量
ReviewAgent 用 qwen-flash 做审核，但它只能检查「形式上是否完整」，无法判断「结论是否正确」。一份报告可能数据齐全、格式规范、逻辑自洽，但根因定位是错的 —— 审核 Agent 看不出来。
7.2 架构层面的局限
"LLM 审 LLM" 的先天问题
ReviewAgent 的设计初衷是避免「自我认同偏见」—— 用独立模型审核主 Agent 的输出。但本质上还是 LLM 审 LLM，存在几个问题：
●
审核模型（qwen-flash）能力弱于主模型，可能漏判
●
审核标准写在 Prompt 里，同样依赖 LLM 的理解和遵循
●
无法验证「事实正确性」，只能检查「形式完整性」
用一个不太恰当的类比：这相当于让实习生审核高级工程师的代码 —— 能查出格式问题，但查不出逻辑错误。
多层控制的复杂度代价
为了解决「该用不用、乱用、用错」的问题，我们加了多层控制： 
这么做本质上是在用工程试图弥补模型的缺陷。。引导
●
SkillHintProvider（推荐）
●
thought 参数（强制思考）
●
SkillMatchChecker（匹配校验）
●
ReviewAgent（输出审核）
每多一层，就多一个可能出错的环节。实际调试时，经常遇到「不知道是哪层的问题」—— 是 Skill 写得不好？是 LLM 没理解？还是审核标准太严/太松？
系统复杂度上去了，但效果提升不是线性的。
缺乏量化评估机制
目前没有一套完整的机制来回答：
●
这个 Skill 的触发率是多少？
●
触发后的执行完成率是多少？
●
用了 Skill 和没用 Skill，输出质量差多少？
没有量化数据，优化就靠「感觉」和「case by case」的人工评估，效率很低。
7.3 维护层面的成本
Skill 编写门槛高
写一个真正有用的 Skill，需要同时具备两种能力：
●
领域专家：知道「正确的诊断流程是什么」
●
Prompt 工程：知道「怎么写 LLM 才能理解和遵循」
这两种能力的交集很小。领域专家写的 Skill 往往太抽象（「分析依赖链路」），LLM 执行不了；Prompt 工程师写的 Skill 流程可能不对。
Skill 冲突与重叠
随着 Skill 数量增加，边界越来越模糊：
●
﻿root-cause-analysis 和 microservice-anomaly-diagnosis 什么时候用哪个？
●
﻿trace-analysis 是独立用还是作为 root-cause-analysis 的子流程？
LLM 的选择有时和我们预期不一致，但很难说谁对谁错。
调试定位困难
当输出质量不好时，定位问题很痛苦：
●
是 Skill 没触发？→ 查推荐日志
●
是 Skill 内容写得不好？→ 改 Skill 重测
●
是 LLM 没理解？→ 换措辞重测
●
是审核标准不对？→ 调审核 Prompt
经常改了 A 发现是 B 的问题，改了 B 又影响了 C。缺乏系统性的调试工具。
7.4 未解决的问题与方向
坦白说，以下问题目前没有好的解法：
问题
现状
困难在哪
如何保证 LLM 100% 遵循 Skill
做不到
Prompt 天然是「建议」不是「程序」
如何验证结论的事实正确性
只能查形式
需要领域知识 + 真实数据交叉验证
如何量化 Skill 的 ROI
没有数据
缺乏 A/B 测试基础设施
如何降低 Skill 编写门槛
依赖专家
自动生成 Skill 的尝试效果不好
一些可能的方向（但还没验证）：
1.
结构化执行：把 Skill 从「自然语言 SOP」改成「可执行的 DAG」，强制按节点执行。代价是失去灵活性，且改造成本高。
2.
事后评估替代事前审核：不在输出前拦截，而是事后收集用户反馈和真实效果，用数据驱动 Skill 迭代。问题是反馈闭环很难建立。
3.
分层 Skill：把大 Skill 拆成小的、可组合的「原子 Skill」，减少重叠和冲突。但会增加编排复杂度。
正因为有上面问题，所以个人觉得一个好的 SKILL 得有以下的元素：
这里就必须要说起 SuperBowel 系列的 SKILL(下面简称 SP)，每个都是精品，下面这几个店来自于这些 SKILL 里面的思考
1.
有硬门槛：因为 SKILL 是标准执行手册，所以必须有硬约束，什么情况下使用，什么情况下不能使用。这个硬约束加载 description 里面
2.
阶段化： 每一阶段有清晰的 action 以及目标，每一阶段有清晰的成功失败衡量标准
3.
可组合：SKILL 之间可以互相引用
4.
Red Flags红旗预警信号： 当发现 Agent 有跑偏信号出现，立刻终止。 这个怎么做得到的呢。SP 里面的做法是要 LLM 做一次思考，如果有以下特征，立刻终止：(不一一解释了)
If you catch yourself thinking:
- "Quick fix for now, investigate later": “先 quick fix，之后再查原因”：本质是把根因调查推迟，最后往往就永远不查了（技术债式修复）。
- "Just try changing X and see if it works" 这就是“叠修复”。多变量一起改，会导致你根本不知道哪一处起作用，下一次再坏更难定位。
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"  这就是“猜”。LLM 特别容易在证据不足时用语言把不确定包装成确定。
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals new problem in different place**
八、 SKILL 业内常见问题及应对
这里列一下业内（包括 Claude Code 用户）反馈的常见问题
问题一：该触发的时候不触发
这是最常见的问题。GitHub 上有用户反馈：明明请求和 Skill 描述完全匹配，Claude 却不调用 Skill，而是先做一堆探索性操作。
用户请求「用 Gitlab 跑测试」，Skill 描述写的就是「run tests via Gitlab pipeline」，结果 Claude 先去读文件、查配置，就是不用 Skill。
我们的应对：
●
﻿SkillHintProvider 在每轮请求时主动提示
●
关键词打分 + Rerank 模型重排序（使用 qwen3-rerank）
●
但不强制调用，最终还是 LLM 决定
问题二：描述太模糊，匹配不准
Skill 的 description 写得太泛，导致什么请求都能匹配上。
我们的应对：
●
要求 description 写明具体场景
●
增加 keywords 字段，显式列出触发关键词
●
增加 scene 字段，区分场景类型
问题三：启动时加载太多，浪费资源
有些实现会在启动时把所有 Skill 完整内容都加载进来，context 直接爆掉。
我们的应对：
●
启动时只加载元数据，约 200 tokens
●
调用时才加载完整内容
●
单次请求最多加载 5 个 Skill
问题四：简单问题被复杂化
用户只是问「QPS 是多少」，LLM 却加载了根因分析 Skill。
我们的应对：
●
识别清单类查询，跳过 Skill 推荐
●
强制 think：调用前说明理由
●
加载后校验：不匹配就放弃
问题五：执行了流程但结论没依据
LLM 按 Skill 流程走了一遍，但最后输出「可能是数据库慢」。
我们的应对：
●
Skill 正文里明确写：「结论必须有数据佐证」
●
﻿report_requirements.json 定义必须包含的报告结构
●
﻿review_analysis_report 在输出前审核
