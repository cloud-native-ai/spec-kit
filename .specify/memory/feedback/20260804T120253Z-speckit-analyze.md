---
id: "20260804T120253Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "036-team-summary-analyze-20260804T195000Z"
scope: "local"
feature: "036-team-summary"
partial: false
created: "2026-08-04T12:02:53Z"
summary: "对 036-team-summary 做实现前的跨工件一致性分析(requirements 36 FR / 15 SC / 6 US、plan、tasks 120 任务 / 9 相、4 份契约、research、data-model、quickstart、feature-ref、feature 记忆)。达成命令声明目的:找出 9 条发现(0 CRITICAL / 1 HIGH / 7 MEDIUM"
---

## Review
对 036-team-summary 做实现前的跨工件一致性分析(requirements 36 FR / 15 SC / 6 US、plan、tasks 120 任务 / 9 相、4 份契约、research、data-model、quickstart、feature-ref、feature 记忆)。达成命令声明目的:找出 9 条发现(0 CRITICAL / 1 HIGH / 7 MEDIUM / 1 LOW),Feature 绑定 027 经索引行、明细文件、spec path、状态语义四项核对全部一致。

按 §5.5 对两条 HIGH 各派独立只读子代理复核(仅给结论与证据位置、不给我的推理):H1 确认并额外找出第五处引用与一个假绿失效模式;H2 降级为 MEDIUM 并附更强推理,同时发现第三处枚举漂移。

最有价值的发现是机械的而非语义的——`templates/teams/` 目录在仓库中根本不存在(真实路径 `skills/create-team/templates/teams/`),五处引用会使 T047 在 implement 期直接失败;且因 `sync-mirrors.py` 的 `templates/` → `.specify/templates/` 映射,照字面创建该路径会导致编辑同步到错误镜像、真实预设毫无改动、而 T092 的 `diff -q` 仍然通过(假绿)。

用户批准后应用了四项机械修复(五处幻影路径、T100 的 SC 区间 SC-012→SC-015、不变量分组三处计数统一为五并把 SC-003 立为单一事实源、两处相位编号漂移),修复过程中顺带补上 SC-003 原本漏掉的 `.specify/agents/**` 分组——即枚举漂移掩盖了一个真实的验收缺口。

修复后复验:36 FR 集合完整无重复(文档顺序为主题分组、非数字序,属有意)、15 SC 与 Source 15/15 配对、120 任务 ID 唯一、86 处 blockedBy 零悬空、零 DAG 环、幻影路径零残留、全部编辑目标路径存在。

三处过程瑕疵已记入优化点:路径核对脚本因跳过 glob 而一度漏掉该 HIGH;§5.5 的校验者应一次并行派发而我串行派了两次;首次记录本反馈时把含反引号的 review 放进双引号参数,导致 bash 命令替换吃掉了其中的路径(已删除该条并改用 `--review-file` 重录)。

## Optimization Points
- 六个 Detection Passes(A 重复 / B 歧义 / C 欠规格 / D 章程 / E 覆盖 / F 不一致 / G Feature)全部是**语义**判定,没有一条要求做"被引用路径是否真实存在"的机械核对。而本次唯一的 HIGH 发现恰恰是机械的:`templates/teams/` 这个目录在仓库中不存在(真实路径是 `skills/create-team/templates/teams/`),被 plan.md ×2、tasks.md ×2、feature-ref.md ×1 共五处引用。讽刺的是 `/speckit.tasks` 命令自己的 Pin Hygiene 已明令"surface-file lists must be real…每个路径在编写时都要做存在性核对",但 analyze 没有对应的复核关口,于是这条规则在下游无人复查。建议新增一个机械 Pass:对所有工件中出现的仓库内路径做 `os.path.exists` 批量核对,把"编辑目标不存在"判为 HIGH(它必然在 implement 期失败)。
- 与上一条相连的一个具体陷阱:我第一版路径核对脚本**跳过了含 `{}`/`*` 的 glob 形式**,而这五处引用恰好都写成 `templates/teams/{a,b,c}.md` 与 `templates/teams/*.md`,于是被静默跳过、核对报告"全部存在"。是靠另一次针对性 grep 才发现的。建议该 Pass 明确要求:跳过 glob 展开时仍 MUST 核对 glob 的**基目录**是否存在。
- §5.5 的独立校验子代理这一步产生了远超"确认/驳回"的价值,值得在命令中把这层收益写明以免被当成形式步骤。本次两个 HIGH:H1 的校验者不仅确认,还额外找出我漏掉的第五处引用,并推导出一个我没想到的**假绿**失效模式(`sync-mirrors.py` 把 `templates/` 映射到 `.specify/templates/`,因此若有人照字面创建该幻影路径,编辑会被同步到错误镜像、真实预设毫无改动、而 T092 的 `diff -q` 仍然通过);H2 的校验者给出比我更强的推理并正确降级为 MEDIUM,同时又发现第三处枚举漂移(T072 说"三组"、SC-003 说"四者"、契约表列五组)。建议把"校验者可提出**新**发现与失效模式,而不仅裁决原发现"写进该节。
- 覆盖检测目前是 ID 子串匹配,把两种不同问题混为一谈:FR-008 在语义上已被 T020 + FG-1/FG-3 完全覆盖,只是没有任务**引用它的编号**;而 SC-008 是真的没有验证任务。前者是可追溯性瑕疵,后者是覆盖缺口,处置完全不同。建议 Pass E 拆成两问:①有无实现它的任务(覆盖)②有无任务引用其编号(可追溯性),分别定级。
- 命令没有"数量/枚举一致性"检查,而规格类文档极易出现同一集合在多处被数成不同个数。本次实测到三处不一致(3/4/5 组不变量),且顺带暴露 SC-003 原本**漏了 `.specify/agents/**` 这一组**(plan.md 的预置约束块与写入面契约都有,SC 却没有)——也就是说枚举漂移不只是措辞问题,它掩盖了一个真实的验收缺口。建议新增 Pass:对"the N X / N 组 / N 者"这类基数断言做跨工件比对。
- 我自己的一处流程偏差:§5.5 要求"validate findings in one parallel dispatch wave",我却分两次串行派发了 H1 与 H2 的校验者,多花一轮往返且违背了该节明写的批处理要求。原因是我在拿到 H1 结果后才补充确认 H2 的证据——但正确做法是先把两条证据都定位好再一次派发。
- token-efficiency: 覆盖映射、DAG 环路与前向依赖、路径存在性、ID 连续性、枚举计数全部用 python/grep 一次性批量判定,未重读任何工件全文;两个 HIGH 的复核交给 fresh-context 子代理,使我的主上下文不被校验推理污染。可改进点见上条(串行派发多花一轮);另外我在核对枚举时先 grep 出 `三组/四组/五者` 五处命中,其中两处("三组 .puml/.svg/.png"图表)属不同概念,需逐条看上下文才能排除——若一开始就把模式限定为"组内容指纹|byte-invariance groups"可少一轮。
