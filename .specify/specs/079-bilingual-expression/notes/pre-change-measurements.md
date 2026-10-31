# 实测前提冻结 — 079 双语表述（Bilingual Expression）

**冻结日期**：2026-10-30（tasks 阶段 § Measured Premises 生成时实测，HEAD `5a4dc5a4`）
**核对日期**：2026-10-30（implement 起点复核，HEAD `cc508bfe`）
下列各行逐条复现 `tasks.md` § Measured Premises 的命令与真实输出，implement 期不得凭印象更新。

## FR / SC / 故事 / Shared Strings 定义行

| 前提 | 重导命令 | 实测输出 |
|------|----------|----------|
| FR 定义行 | `grep -cE '^- \*\*FR-[0-9]{3}\*\*:' .specify/specs/079-bilingual-expression/requirements.md` | `18` |
| SC 定义行 | `grep -cE '^- \*\*SC-[0-9]{3}\*\*:' .specify/specs/079-bilingual-expression/requirements.md` | `5` |
| 用户故事数 | `grep -cE '^### User Story' .specify/specs/079-bilingual-expression/requirements.md` | `4` |
| Shared Strings | `grep -cE '^\| .STR-[0-9]{3}.' .specify/specs/079-bilingual-expression/requirements.md` | `3` |

## 契约条款

| 前提 | 重导命令 | 实测输出 |
|------|----------|----------|
| 契约文件数 | `ls .specify/specs/079-bilingual-expression/contracts/*.md \| wc -l` | `4` |
| 契约条款定义 | `python3 scripts/python/clause_extract.py .specify/specs/079-bilingual-expression/contracts/*.md \| grep -c '^  C-'` | `35`（owner-document 9 + checker 12 + distribution 6 + measurement 8） |
| 条款计数陷阱形（提及数非定义数） | `grep -oh 'C-[0-9]\{2,3\}' .specify/specs/079-bilingual-expression/contracts/*.md \| wc -l` | `71` |

## 交付物与基线

| 前提 | 重导命令 | 实测输出 |
|------|----------|----------|
| 五个交付物路径不在树 | `ls shared/guidelines/bilingual-expression.md scripts/python/bilingual-expression-check.py tests/contract/test_bilingual_expression.py tests/fixtures/bilingual .specify/specs/079-bilingual-expression/notes` | 五行 `No such file or directory`（红先行起点） |
| 生成器输入模板 | `grep -n 'TEMPLATE_FILE=' scripts/bash/generate-instructions.sh` | `TEMPLATE_FILE=".specify/templates/instructions-template.md"` |
| ambient 插入位置锚点 | `grep -n '^## Grounded Naming' templates/instructions-template.md` | 在场（唯一锚点） |
| 确认门基线 | `tail -3 .specify/specs/079-bilingual-expression/test-evidence/plan-scan-confirmation-gates.txt` | blocking 27 / violations 0 |
| 镜像基线 | `tail -2 .specify/specs/079-bilingual-expression/test-evidence/plan-sync-mirrors-baseline.txt` | 六对全 ok（2026-10-30 实测） |
| coverage 基线 | `head -2 .specify/specs/079-bilingual-expression/coverage-baseline.txt` | plan 期已冻结（不重冻结） |
| 任务行预算 | `grep -cE '^- \[ \] T[0-9]{3}' .specify/specs/079-bilingual-expression/tasks.md` | `19`（T001–T019）≤ 40 |
| 任务行预算陷阱形 | `grep -oE 'T[0-9]{3}' .specify/specs/079-bilingual-expression/tasks.md \| wc -l` | 远大于 19（提及数非定义数） |
