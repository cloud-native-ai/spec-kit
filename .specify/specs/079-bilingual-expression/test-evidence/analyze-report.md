# Analyze Findings Report — 078 双语表述（Bilingual Expression）

**Stage**: `/speckit.analyze`（只读质量门；2026-10-30）
**Verdict**: 0 CRITICAL / 0 HIGH → 门通过；8 MEDIUM / 6 LOW 转入 implement 指引。

> 本文件是 analyze 阶段报告正文的留档（只读阶段不改产物；报告即产物）。原始报告由执行子代理在阶段回传中输出，此处在收口前按其内容逐条转录。

## Findings

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| F-01 | inconsistency | MEDIUM | requirements FR-001 vs FR-004/FR-007 | FR-001 禁止其他位置复述枚举，但 FR-004/FR-007 内联枚举且未声明 requirements 是播种层 | 上游补一句「requirements 枚举为 seed，唯一 owner 归 owner 文档」 |
| C-01 | underspecification | MEDIUM | FR-009/FR-010；checker C-002 | scan 全量无非功能包络（墙钟/输入规模） | owner 文档或契约补一行 |
| C-02 | underspecification | MEDIUM | FR-001；plan Chapter Tree | owner 文档自身定义行是否必须示范双语形态未规定 | 成文声明（是/否均可） |
| C-03 | underspecification | MEDIUM | Shared Strings | STR 表维护 ownership 未指定 | 补维护协议一句 |
| C-04 | underspecification | MEDIUM | Edge Cases 首条；data-model S4 | 段落级方向判定信号未操作化 | 补段落级信号或声明保守缺省 |
| C-05 | underspecification | MEDIUM | FR-004；checker C-004/C-012 | 自带括号/混合文字第三方专名与检测器的碰撞未定义 | 契约补输出形态 |
| C-06 | underspecification | MEDIUM | FR-003 | 主语言非 zh/en 的文档无方向规则 | 补范围声明 |
| C-07 | underspecification | MEDIUM | checker C-002 | 检查器故障模式未覆盖 | 补退出语义 |
| B-01 | ambiguity | LOW | FR-002 | 无自足的「定义处 vs 提及处」示例 | owner 文档给一例 |
| E-01 | traceability | LOW | FR-002/Edge Cases | 「首次定义」无登记机制 | review 阶段定轻量登记面或显式接受 |
| E-02 | process gap | LOW | owner-document C-003 | 信号清单补登记的操作者未命名 | 点名责任人 |
| I-01 | assumption monitoring | LOW | A2/A4 | 重开条件无监控 owner | closure 挂既有回看机制或显式 inert-by-design |
| G-01 | stage-recording | LOW | features/078.md | 阶段记录止于 plan | implement/closure 回填 |
| F-02 | inconsistency | LOW | quickstart S4 vs tasks T002 | ambient 断言被双测试文件钉住 | 任一侧加注释互指或 review 核对 |

## Coverage / Linkage

- `account-clause-coverage.py`：status ok；claimed clauses 35/35；FR 18/18。
- FR→tasks 18/18；SC→tasks 5/5；unmapped tasks 无。
- Feature 078 绑定在位；唯一漂移 G-01（LOW）。

## Constitution Alignment

无冲突；plan Constitution Check 18 项 Pass；抽查 IV / IX / XIV / XVIII 与制品一致。

## Metrics

Total Reqs 18 FR / 5 SC / 4 US / 3 STR；Tasks 19；Coverage 100%；Findings CRITICAL 0 · HIGH 0 · MEDIUM 8 · LOW 6；验证波未触发（无 CRITICAL/HIGH）。

## 记账

run-determination + exec-quant + feedback（`--feature 078-bilingual-expression`）齐备；只读证明：除记账外零写入。
