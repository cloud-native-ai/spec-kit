# Project Glossary (项目词汇表)

> **Note**: This file is initialized by `/speckit.instructions` and lives beside `constitution.md` / `features.md`. It is the project's single, project-wide vocabulary anchor: it corrects voice/dictated input (homophones, easily-confused words) and doubles as a lightweight domain-knowledge dictionary. It is loaded as ambient context by every `/speckit.*` command via the Documentation Map. See `.specify/shared/workflow/glossary.md` for the correction / enrichment / conflict protocol.

## Authoring Rules

- **Common words are NOT recorded** — only project-specific / domain terms that carry special meaning here.
- **User edits are authoritative (以用户输入为准)** — manual entries win over automatic proposals and are preserved across regenerations; automatic proposals MUST NOT silently overwrite a `user` entry.
- **Conflicts require confirmation** — a new term that collides with an existing entry (same term/different meaning, or a homophone/near-duplicate) is written only after the user confirms the resolution.

## Column Definitions

| Column | Meaning |
|--------|---------|
| Canonical | The agreed project term (unique, case-insensitive). |
| Variants | Comma-separated homophones / easily-confused / dictation-error forms that anchor back to Canonical; `-` when none. |
| Meaning | Brief one-line domain definition. |
| Origin | `auto` (framework-proposed) or `user` (manually authored/confirmed). |
| Status | `proposed` (awaiting confirmation) or `confirmed`. |

## Glossary

| Canonical | Variants | Meaning | Origin | Status |
|-----------|----------|---------|--------|--------|
| Spec Kit | speckit, spec-kit, speck it | The SDD CLI toolkit distributed as specify-cli | user | confirmed |
| SDD | - | Spec-Driven Development: specifications drive implementation | user | confirmed |
| Constitution | - | Project governance principles at .specify/memory/constitution.md | auto | proposed |
| Feature Index | - | Single source of truth for project capabilities at .specify/memory/features.md | auto | proposed |
| Reconcile Engine | - | Diff-and-converge engine used by Spec Kit commands to align artifacts with desired state | auto | proposed |
| Task Complexity Rubric | - | Tiered effort-calibration framework embedded in .specify/instructions.md | auto | proposed |
| 程序优先 (Program-First) | program first, 程序优先原则 | Token 效率纪律之一:可用固定规则表达的文本/数据判断交由确定性程序执行,不送入大模型 | auto | proposed |
| 摘要优先 (Summary-First) | summary first, 摘要化访问 | Token 效率纪律之一:机器管理数据文件原文不整体注入大模型上下文,例行消费摘要/投影/节选 | auto | proposed |
| 升级阶梯 (Escalation Ladder) | escalation ladder, 访问升级阶梯 | 数据访问逐级放宽路径:摘要 → 定向节选 → 有界整读(整读须满足例外情形或记录理由) | auto | proposed |
