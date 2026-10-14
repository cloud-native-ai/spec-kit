---
id: "20261012T123030Z-skill-summarize-project"
unit_id: "skill:summarize-project"
unit_type: "skill"
run_id: "summary-refresh-command-logic-as-classified-skills-20261012"
scope: "local"
probe: "skill-summarize-project-wrapup"
kind: "internal"
slice: "skills"
disposition: "processed"
partial: false
created: "2026-10-12T12:30:30Z"
summary: "summarize-project 刷新运行（goal command-logic-as-classified-skills,非交互）:五章节报告+四态 WBS 落盘,check-coherence FAIL=0;运行中发现 build-summary-input.py 对含「空格+冒号」的 team.md frontmatter 解析失败并静默回退(身份误标/描述截断/Scope 未声明),本次"
introspection_ref: "introspection-20261013T155006Z#F-02"
disposition_reason: "introspection:introspection-20261013T155006Z#F-02"
---

## Review
summarize-project 刷新运行（goal command-logic-as-classified-skills,非交互）:五章节报告+四态 WBS 落盘,check-coherence FAIL=0;运行中发现 build-summary-input.py 对含「空格+冒号」的 team.md frontmatter 解析失败并静默回退(身份误标/描述截断/Scope 未声明),本次按 tracked 工件手工修正并留痕;台账并发追加触发两态交接重折叠,机制按预期收敛。

## Optimization Points
- ## Feedback
- **发现（correctness / 工具健壮性）**：`skills/internal/create-team/scripts/build-summary-input.py` 对本团队 team.md 的 frontmatter YAML 解析失败（non_path 流式映射条目内含「空格+冒号」形如 `…lessons.md :17`，PyYAML 报 ParserError）→ 生成器整体回退：goal 身份误标 inferred、project_desc 取内联 goal 且截断、roster Write Scope 记未声明。本次刷新已按 team.md/goal.md 手工修正并在 roster.md 留更正记录，但生成器对含 `: ` 的 frontmatter 团队会稳定产出退化元数据——建议生成器对 flow-mapping 解析失败时 fail loud（而非静默回退），或对 non_path 值加引号约定。
- **出处纪律边界（授权留痕）**：S1–S3 完成事件在刷新开始时仅有 git-ignored 工作区 progress.md 记录（台账仅 1 行），刷新中团队 cycle 并发落盘了 TI-0002..TI-0005 显式行；已按「每次从全部团队台账重新折叠」重新装载，仅 S-layer 仍以推断身份呈现（出处 progress.md，经调度方授权）。两态交接机制按预期收敛。
- marker: correctness
