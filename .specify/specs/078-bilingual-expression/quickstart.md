# Quickstart: 双语表述（Bilingual Expression）

**Spec**: `.specify/specs/078-bilingual-expression/` | **Date**: 2026-10-30
**执行-verify 说明**：本文件每个命令示例标注「本次实测」（本 plan 会话已原样执行，输出摘录）或「Pinned by」（尚不存在实现，由具名契约测试钉住，premises 已列出）。检查器在 plan 期不存在，其示例一律 Pinned by `tests/contract/test_bilingual_expression.py`（red-first，implement 交付）。

## S1 约定核对（读者面，无命令）

打开 [[STR-001]]，按四步核对一处定义行：① 它是否命中 owner 文档的可判定信号（S1…S4）；② 文档主语言（S4）决定方向；③ 形态是否为 owner 登记的逐字形态（半角、紧贴）；④ 是否落在豁免面。四步全过即合规。

## S2 检查器形态判定（implement 后可用）

- 合规行通过：
  `python3 scripts/python/bilingual-expression-check.py --action scan --path tests/fixtures/bilingual/compliant-definition.md`
  期望：退出码 0，无 finding 行。
  **Pinned by** `tests/contract/test_bilingual_expression.py::test_scan_compliant_fixture`。
  *premises：脚本路径 `scripts/python/bilingual-expression-check.py`；动作名 `scan`；夹具路径 `tests/fixtures/bilingual/compliant-definition.md`；退出码契约 0/1/2（contracts/checker.md C-002）；夹具为 zh 主语言、含 S3 加粗定义行。*
- 全角违规行判红并定位：
  同一命令扫 `tests/fixtures/bilingual/fullwidth-definition.md`。
  期望：退出码 1，输出 `tests/fixtures/bilingual/fullwidth-definition.md:7 [full-width-parens] ...`（行号以夹具实际为准，测试只钉码与定位形态）。
  **Pinned by** `tests/contract/test_bilingual_expression.py::test_scan_fullwidth_fixture_red`。
  *premises：同上 + finding 码封闭四值含 `full-width-parens`（C-009）。*
- 括号语言同向判红：
  夹具 `same-language-definition.md`（en 主语言文档，括号内仍为英文）。期望退出码 1，码 `same-language-bracket`。
  **Pinned by** `::test_scan_same_language_fixture_red`。
  *premises：同上 + 主语言判定走 S4 缺省（C-007）。*

## S3 覆盖面核验（implement 后可用）

`python3 scripts/python/bilingual-expression-check.py --action coverage`
期望：退出码 0；若某定义面缺失则退出码 1 且逐条输出 `coverage-missing` 缺失项清单（C-008）。
**Pinned by** `tests/contract/test_bilingual_expression.py::test_coverage_action`。
*premises：动作 `coverage` 不接受 `--path`（C-001）；覆盖面清单来自 [[STR-001]]，脚本只读取不内嵌清单副本。*

## S4 下游 instructions 生成（SC-003 管道；ambient 断言 Pinned by）

**本次实测（管道机制，2026-10-30）**：在受认可临时根建 pilot（`git init` + `.specify/templates/instructions-template.md` + `.specify/scripts/`，即 init 载荷），运行
`bash scripts/bash/generate-instructions.sh`（在 pilot 目录内以框架源脚本绝对路径调用）→ `success Instructions generated/updated at .specify/instructions.md`，产物 28,005 B / 30 个顶级小节；pilot 已 `rm -rf` 拆除。完整输出：`test-evidence/s4-pilot-pipeline-smoke.txt`。
**ambient 断言（implement 后）**：用含新 ambient 模板的框架重复上述管道，断言 `grep -c '^## Bilingual Expression' .specify/instructions.md` = 1 且小节内四组枚举关键词零命中。
**Pinned by** `tests/contract/test_instructions_section_propagation.py` 的增补用例（test_bilingual_expression.py 同步钉模板侧形态）。
*premises：生成脚本路径 `scripts/bash/generate-instructions.sh`；ambient 标题字面量 `## Bilingual Expression (双语表述)`；init 载荷含 `.specify/scripts/`；pilot 必须拆除（teardown 已随实测验证）。*

## S5 镜像零新增漂移（本次实测）

`python3 scripts/python/sync-mirrors.py --check`
本次实测（plan 期基线，2026-10-30）：退出码 0，六对全 `ok`（templates 22 / skills/external 406 / skills/internal 136 / agents 3 / scripts 117 / shared 60），per-tool 命令副本 `OK`。原始输出 `test-evidence/plan-sync-mirrors-baseline.txt`。
implement 收口判据：本特性触碰的 shared / templates / scripts 三对相对此基线**无新增漂移**（contracts/distribution.md C-002），不以绝对「全绿」为判据。

## S6 结构面零新增（本次实测）

`python3 .specify/skills/create-docs/scripts/docs-utils.py --action validate`
本次实测（2026-10-30）：violations = 4（broken-link 3 + note-frontmatter 1，既有漂移非本特性引入）。原始输出 `test-evidence/plan-docs-utils-validate-baseline.txt`。收口判据：相对此基线零新增。

## S7 SC-001 关键词扫描（implement 后）

关键词表由程序从 [[STR-001]] 四组枚举列表项派生（contracts/measurement.md C-001），在 `shared/`、`templates/`、`.specify/`（排除 specs/history）检索，排除 owner 文档自身与含 owner 指针的行后期望命中数 0。
**Pinned by** `tests/contract/test_bilingual_expression.py::test_sc001_keyword_snapshot` + review 阶段一次实跑留档（E7 快照）。
*premises：owner 文档四组枚举为 Markdown 列表（C-002）；快照冻结于交付日（E7）。*

## S8 SC-005 census（implement 后）

`python3 scripts/python/bilingual-expression-check.py --action census`
期望：退出码 0（不一致处数 0）；总体 = 词汇表全部双语 Canonical 词条，100% census（R-11）。
**Pinned by** `tests/contract/test_bilingual_expression.py::test_census_action` + review 阶段实跑留档。
*premises：`.specify/memory/glossary.md` 为词条唯一来源；中文侧逐字比对（C-011）。*
