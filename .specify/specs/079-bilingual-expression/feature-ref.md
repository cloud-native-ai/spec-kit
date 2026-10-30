# Feature Reference: 双语表述（Bilingual Expression）

**Bound Feature**: Feature 079 双语表述（Bilingual Expression）——`.specify/memory/features/079.md`，索引行 `.specify/memory/features.md`
**Spec**: `.specify/specs/079-bilingual-expression/` | **Date**: 2026-10-30
**本 plan 的映射**：18 条 FR → 设计落点；5 条 SC → 证据来源。Feature 状态由本阶段推进 `Draft → Planned`（`Implemented` 归 `/speckit.implement`）。

## FR → 设计落点

| FR | 落点 |
|----|------|
| FR-001 | owner 文档 [[STR-001]]（implement 新建，`contracts/owner-document.md` C-001/C-002 钉结构与 owner 声明；消费方指针纪律由 C-007 钉） |
| FR-002 | owner 文档 § 定义处与可判定信号（S1…S4，`contracts/owner-document.md` C-003/C-004；检查器取信号行 `contracts/checker.md` C-005） |
| FR-003 | owner 文档 § 方向规则与唯一形态（`contracts/owner-document.md` C-005/C-006；机械判定 `contracts/checker.md` C-007） |
| FR-004 | owner 文档 § 豁免面（封闭集，`contracts/owner-document.md` C-007；机械跳过 `contracts/checker.md` C-004） |
| FR-005 | owner 文档 § 一致性与词汇表（一致性基准指针 `.specify/memory/glossary.md`；census 判定 `contracts/checker.md` C-011） |
| FR-006 | owner 文档 § 迁移边界（`contracts/owner-document.md` C-009；存量不入分母 `contracts/checker.md` C-010） |
| FR-007 | owner 文档 § 覆盖定义面（封闭集，`contracts/owner-document.md` C-007；coverage 判定 `contracts/checker.md` C-008） |
| FR-008 | `templates/instructions-template.md` ambient 小节（`contracts/distribution.md` C-003；形态守卫 C-006(iii)） |
| FR-009 | `scripts/python/bilingual-expression-check.py`（行为契约 `contracts/checker.md` C-001…C-012） |
| FR-010 | 运行入口/退出码/挂接面 = `contracts/checker.md` C-001…C-003（研究记录 research.md R-10） |
| FR-011 | 框架源编辑面与镜像纪律（`contracts/distribution.md` C-001/C-002；刷新 C-005） |
| FR-012 | 模板中立性（`contracts/distribution.md` C-003/C-004） |
| FR-013 | owner 文档 § 与相邻纪律的交界（`contracts/owner-document.md` C-008） |
| FR-014 | 漂移守卫 = 契约测试（`contracts/distribution.md` C-006） |
| FR-015 | Scope：交付物清单即 owner 文档 + ambient + 检查器 + 测试 + 登记（plan § Project Structure；无运行时/服务） |
| FR-016 | 存量差异清单化（E6，`data-model.md`；`contracts/checker.md` C-010；测量 `contracts/measurement.md` C-003/C-006） |
| FR-017 | Feature 登记（本阶段 `features.md` 079 行 `Draft → Planned` + `features/079.md` 阶段记录） |
| FR-018 | ID 登记（`register.md` 登记 T-013…T-016 与四份契约 35 条 C- 条款号，`contracts/measurement.md` C-008） |

## SC → 证据来源

| SC | 证据来源（测量程序见 `contracts/measurement.md`） |
|----|------|
| SC-001 | E7 交付日快照 + review 期关键词扫描实跑（C-001/C-002；快照落 `test-evidence/`） |
| SC-002 | 检查器 `scan --scope changed` 输出 + review 面程序抽样复核（C-003/C-004） |
| SC-003 | 临时树 instructions 生成实跑（C-005；plan 期管道冒烟 `test-evidence/s4-pilot-pipeline-smoke.txt`，ambient 断言 Pinned by 契约测试） |
| SC-004 | 本特性全部提交的 `git diff --stat` 白名单审计（C-006） |
| SC-005 | 检查器 `census` 全量输出（C-007；100% census，R-11） |

## 绑定关系

- Feature 079 为新建 Feature（requirements § Related Feature 绑定，reuse-first 复核 014/018/Glossary/instructions 机制/069 均无归属）。
- 本 plan 不新建/合并/废弃其他 Feature；`features.md` 只改 079 行的 Status 与 Last Updated。
- 规格路径保持 `.specify/specs/079-bilingual-expression/requirements.md` 不变。
