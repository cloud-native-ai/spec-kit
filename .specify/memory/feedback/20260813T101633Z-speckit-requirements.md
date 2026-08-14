---
id: "20260813T101633Z-speckit-requirements"
unit_id: "/speckit.requirements"
unit_type: "command"
run_id: "040-agent-metadata-portability-2026-08-13"
scope: "local"
feature: "040-agent-metadata-portability"
partial: false
created: "2026-08-13T10:16:33Z"
summary: "本次运行完成了从用户输入到可交付需求规格的全链路:编号发现(识别并排除了 community/4059 分支导致的 059 假阳性)、分支与 spec 骨架创建、以源码实测为准的现状锚点取证(7 个预置 agent 的 11 键 frontmatter、_AGENT_LINK_DIRS 逐文件软链接机制、sync-mirrors 镜像对、两处以 qoder 命名的契约测试、三个 agent 目录的"
---

## Review
本次运行完成了从用户输入到可交付需求规格的全链路:编号发现(识别并排除了 community/4059 分支导致的 059 假阳性)、分支与 spec 骨架创建、以源码实测为准的现状锚点取证(7 个预置 agent 的 11 键 frontmatter、_AGENT_LINK_DIRS 逐文件软链接机制、sync-mirrors 镜像对、两处以 qoder 命名的契约测试、三个 agent 目录的实际形态)、5 个故事 27 条 FR 8 条 SC 的规格撰写、Shared Strings 六行闭环、以及一轮质量验证(对 FR-005/FR-013/FR-021 做了可测性收紧)。规格保留 3 个 NEEDS CLARIFICATION 标记(元信息载体形态、每工具目标目录矩阵、是否物理重命名消除 templates 多义),恰好等于上限且均满足保留条件。关键风险(本仓库无每工具 agent 格式文档)已由 FR-010 与 SC-003 显式兜住,未让猜测的字段名进入规格。

## Optimization Points
- **编号发现步骤的正则太宽,会被无关远程分支污染**:Outline step 2 只说"find highest number across remote/local branches and specs dirs matching `[0-9]+-<short-name>`"。本次实测 `git branch -a` 里的 `remotes/origin/community/4059-add-specassay-bundle-e876f4121967e2e9` 被裸三位数匹配读成 `059`,若直接采信就会把本应为 040 的需求编到 060。建议把编号匹配锚定到分支名段首(`(^|/)[0-9]{3}-`)并显式提示"社区/上游分支名里的长数字是已知假阳性源",而不是让每次运行都靠人工复核发现。
- **"house conventions" 靠每次抽样重新发现,事实上的必备小节没有沉淀**:Outline step 4 只要求抽样最高编号 spec 的 heading 结构。但本项目近期 spec 稳定使用四个模板里没有的小节 —— `## Overview`、`### 现状锚点(以源码实测为准)`、`## Out of Scope`、`## Assumptions`,且正文语言为中文。这些已经是事实约定,却要靠每次抽样重新推断,存在漂移风险且浪费一次读取。建议把它们沉淀为 `requirements-template.md` 的可选骨架小节或 `requirements-guidelines.md` 的一条约定,抽样退化为校验而非发现。
- **质量清单缺"外部格式/契约假设的依据来源"检查项**:本需求的最大落地风险是"六家 AI agent CLI 各自的 agent frontmatter 格式在本仓库无成文依据",极易在 FR 里写出猜测的字段名当事实。这次是靠 AGENTS.md 的通则(不要猜 flags/config keys)才被兜住,并手工补出 FR-010 + SC-003 的"依据来源 / 待核实归零"机制。`requirements-guidelines.md` 的 Requirement Completeness 清单里应增加一条:凡需求依赖外部系统的格式、字段或协议,必须标注依据来源与核实状态 —— 这类缺陷比 [NEEDS CLARIFICATION] 更隐蔽,因为它看起来像已确定的需求。
- **token-efficiency**:本次现状调研用一个 Explore 子代理一次性带回 7 个问题的答案(含路径与行号),避免了主上下文里逐个 grep/read 的展开;`grep -c` / `grep -o | sort -u` 的程序化计数替代了人工数 FR/SC/场景条目与核对 `[[STR-NNN]]` 闭环。可避免的开销主要在一处:预置 agent 的 frontmatter 已由子代理报告"7 文件键集完全一致",随后仍全量 dump 了 7 个文件的 frontmatter 做二次确认 —— 该确认本可收敛为一次"键集差异为空"的程序化断言而非全文注入。
