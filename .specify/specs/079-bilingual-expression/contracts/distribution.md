# Contract: 分发与两顶帽子（Distribution）

**Feature**: 079-bilingual-expression
**Spec**: [requirements.md](../requirements.md)
**Owner 指针**：镜像对清单归 `scripts/python/sync-mirrors.py` 的 `MIRROR_PAIRS`（六对）；
instructions 生成归 `scripts/bash/generate-instructions.sh`；两顶帽子归
`shared/definitions/dogfooding-definitions.md` § 2.1。本契约只钉本特性的分发面义务。

## 编辑面（框架源）

- **C-001** 本特性的全部规则性变更 MUST 落在框架源：`shared/guidelines/bilingual-expression.md`（[[STR-001]]，新建）、`templates/instructions-template.md`（ambient 小节）、`scripts/python/bilingual-expression-check.py`（新建）、`tests/contract/`（契约测试，无镜像）。本仓 `.specify/` 运行时副本（shared/templates/scripts 三面）MUST 由 `sync-mirrors.py --write` 产出，MUST NOT 手改；`.specify/instructions.md` 与根 `AGENTS.md` MUST 由 `generate-instructions.sh` 产出，MUST NOT 手改。(FR-011, FR-015)

- **C-002** `sync-mirrors.py --check` 在 implement 收口 MUST 报本特性触碰的三对（shared / templates / scripts）相对 plan 期基线（`test-evidence/plan-sync-mirrors-baseline.txt`，2026-10-30 实测六对全 ok）**无新增漂移**；既有无关漂移不继承为失败、不顺手修复。命令副本面（regen-command-copies）本特性不触碰：命令模板与技能正文不加双语规则（显式排除项），只要求它们未来引用 owner 时走「路径 + 锚」形态（FR-001 消费纪律，不是本特性的编辑面）。(FR-011, FR-012)

## 模板中立性

- **C-003** `templates/instructions-template.md` 的 ambient 小节 MUST NOT 出现本仓专属路径（如 `.specify/` 绝对路径、本仓提交号、本仓专属文件名）；owner 指针一律写框架源相对路径（[[STR-001]]），由镜像机制解析到运行时位置。ambient 小节 MUST NOT 复述方向/形态/覆盖面/豁免的枚举，只承载一句话摘要 + owner 路径指针（FR-008）；小节标题自身按定义处双语形态书写（`## Bilingual Expression (双语表述)`），作为约定的首个示范实例。(FR-008, FR-012)

- **C-004** ambient 小节 MUST NOT 含阻断式确认句（确认门预算零整数余量，plan 期实测 blocking 27 / violations 0，见 `test-evidence/plan-scan-confirmation-gates.txt`）；落地后 `scan-confirmation-gates.py --summary` 的 blocking 计数相对该基线 MUST NOT 增加。(FR-012)

## instructions 运行时刷新

- **C-005** implement 阶段 MUST 运行 instructions 刷新（机制归 `generate-instructions.sh`）使 `.specify/instructions.md` 与根 `AGENTS.md` 携带新 ambient 小节，并留档生成器 size report 输出到 `test-evidence/`；模板实测 27,940 B / live 32,259 B（2026-10-30，R-5），超预算只报 warning，但报告 MUST 被捕获留档（Single-Run Evidence）。(FR-011, SC-003)

## 漂移守卫（FR-014 的 plan 期决定）

- **C-006** 漂移守卫形态 = **契约测试**（而非检查器动作）：新建 `tests/contract/test_bilingual_expression.py`（red-first），钉住 (i) [[STR-001]]/[[STR-002]]/[[STR-003]] 三字字面量与其在 owner 文档、ambient 小节、检查器常量中的唯一消费点；(ii) 镜像三面与框架源逐字一致（派生自 `MIRROR_PAIRS`，不硬编码第二份清单）；(iii) ambient 小节「摘要 + 指针」形态（枚举关键词在该小节内零命中）。检查器不做漂移守卫——它判定定义行形态，不判定「规则是否只有一份」。(FR-014)
