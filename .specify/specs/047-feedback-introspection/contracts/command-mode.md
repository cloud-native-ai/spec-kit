# Contract: `/speckit.feedback` 新增 introspect 模式(047)

命令模板(`templates/commands/feedback.md` + 镜像 + 4 份生成副本)新增第五个执行模式。契约条目 `C-N` 编号,供命令模板契约测试断言。

## 触发与定位

- **C-1**: 当 `$ARGUMENTS` 含 `introspect` [[STR-001]] 时进入本模式;与 Mode 1(无参数)/ Mode 2(处理)/ Mode 3(外部探针)/ Mode 4(`consume`,框架项目专属)并列,优先级低于 Mode 4 的框架门判定(同时含 `consume` 与 `introspect` 时按 Mode 4 处理并在报告中说明)。
- **C-2**: 本模式在任意客户项目可运行,**无** Mode 4 的框架项目门。
- **C-3**: 文档结构:`templates/commands/feedback.md` 的 Outline 中新增 `### Mode 5 — Introspect Feedback(自省)`,章节位置紧随 Mode 3、先于 Mode 4(Mode 4 为框架侧接收端,保持末尾);模式总览句(命令描述行)同步更新为"探测总览、处置、外部探针、自省、消费反馈包"。

## 执行流程(模板规定的步骤序)

- **C-4**: 模式流程 MUST 为下列五步,顺序不可换:
  1. **范围快照**:经 `--action list --disposition open --format json`(可附 `--slice/--kind/--since` 收窄)取条目摘要投影;零条目 → 报告"无可自省条目"并正常结束(不落空报告)。
  2. **场景化分析**:逐条目回到真实场景核验(调出被评单元当前定义/源码与引用上下文),给核验结论;同根因条目聚类为问题;每问题含五要素(data-model)。
  3. **报告产出**:按 `contracts/introspection-report.md` schema 落盘 draft 报告;先 `--action introspect-register`(不带 `--confirm`)完成结构校验与条目关联。
  4. **用户确认**:呈现报告摘要(问题清单 + 分流决定),用户可逐问题覆盖分流;确认后 `--action introspect-register --confirm` 生效批量处置。
  5. **后续路由建议**:列出本地下沉项的建议通道(直接修复 / improve-* / requirements)与上行候选;仅建议,不自动执行。
- **C-5**: 步骤 2 为 agent 推理,模板 MUST 明写 Token 效率纪律适用(摘要优先、升级阶梯;禁止整库原文注入)。

## 红线与边界

- **C-6**: 本模式 MUST NOT 自动修改代码/配置、MUST NOT 触发任何网络/传输;所有落地动作经既有通道由用户确认后执行。
- **C-7**: 外部 probe 条目参与自省时分流恒为 local-sink;模板 MUST 明写外部条目永不进入上行候选。
- **C-8**: 重复自省:范围内条目已有 `introspection_ref` 时,模板 MUST 指示先 `--action list` 核查既有报告,新报告声明 `supersedes` 承继而非平行重复。
- **C-9**: 打包集成:Mode 2 的 package 步骤文案更新——待打包条目存在 `introspection_ref` 时,默认提议 `--action package --include-introspection`,用户可拒绝且不阻断打包。

## 阈值提示语联动

- **C-10**: record 返回 `should_prompt=true` 时的非阻塞提示语可顺带一句"可先 `/speckit.feedback introspect` 自省再打包";提示语仍单条、非阻塞、绝不自动传输(Feature 046 非阻塞约束不变)。

## 示例(模板内嵌)

模板 MUST 内嵌一条最小可跑示例(造 2 条 open 条目 → list 快照 → 报告 → register → confirm → package --include-introspection),示例命令与 `quickstart.md` 场景一致。
