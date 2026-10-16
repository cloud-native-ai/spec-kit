# Feature Reference: Feature 059 Agent+LLM 执行量化记录(Execution Quant Recording)

**Plan**: `plan.md` | **Date**: 2026-10-16

## Feature 绑定

- **Feature ID**: 059(本特性自身;binding 经 clarify Q1 同胞启发式核验裁定,候选 028/055/056 均无同类同胞)
- **Feature Index 行**: `.specify/memory/features.md` 行 67;**Feature 详情**: `.specify/memory/features/059.md`
- **状态推进**: 本 plan 阶段 Draft → Planned(`/speckit.implement` 拥有 Implemented 转换)
- **规格路径**: `.specify/specs/059-exec-quant-recording/requirements.md`(不变)

## FR → 设计落点映射

| FR | 落点 |
|----|------|
| FR-001(每执行恰一条记录) | `data-model.md` §1.1/§2-V1;`contracts/exec-quant-cli.md` collect 幂等;probe-registration.md §1 Binding(scope=all) |
| FR-002(确定性程序采集) | `contracts/exec-quant-cli.md` 全文(引擎三动作);plan D1 |
| FR-003(挂 wrap-up 点/非阻塞/判定之后/无新模板面无新门) | `contracts/probe-registration.md` §1 Handler(order 15)/§4;plan D10 |
| FR-004(注册契约入册) | `contracts/probe-registration.md` §1 四表行 + §2 `_ENGINE_SIBLINGS` + §3 对账面分区 |
| FR-005(agent 字段采集/降级) | `data-model.md` §1.1 来源约束表 agent 行;plan D8 |
| FR-006(LLM 字段候选/生效区分、显式未采) | `data-model.md` §1.1 llm 行 + §2-V2/V6;plan D6/D7 |
| FR-007(质量字段携带/错误来源/禁臆造) | `data-model.md` §1.1 quality 行 + §2-V7;plan D2/D5 |
| FR-008(逐字段来源标注) | `data-model.md` §1.1 编码统一规则(provenance 四元词域);plan D4 |
| FR-009(专属 durable 存储/append-only/不入 feedback) | `data-model.md` §1.3 + §2-V4;plan D3 |
| FR-010(白名单/凭据零现/封顶截断) | `data-model.md` §2-V5/V6;plan D9 |
| FR-011(结构性排除打包与上送) | `data-model.md` §1.3(实测依据 plan Phase 0 #4) |
| FR-012(非阻塞/失败可见) | `contracts/exec-quant-cli.md` 退出码;`data-model.md` §2-V8 |
| FR-013(list-records 过滤/机器可读/追溯) | `contracts/exec-quant-cli.md` 动作二 |
| FR-014(补打分/来源区分/显式无) | `contracts/exec-quant-cli.md` 动作三;`data-model.md` §1.2;plan D12 |
| FR-015(既有引擎零回归) | `data-model.md` §4 非回归基面;`contracts/probe-registration.md` §3(既有分区逐字不动) |

## SC → 验证方法映射

| SC | 方法 | 载体 |
|----|------|------|
| SC-001(恰一条/三组齐备/零空缺) | quickstart 场景 1(list + jq 审计) | `test_exec_quant_engine.py`(V1/V2/V3 断言) |
| SC-002(未采标记 100%/零臆造) | quickstart 场景 2 + 简报 §3 dated 基准比对 | `test_exec_quant_engine.py`(字段二值律) |
| SC-003(套件全绿/失败名单零新增) | quickstart 场景 5(基线冻结 + comm 房式判据) | `data-model.md` §4 清单为比对范围 |
| SC-004(打包零含量化/凭据零现) | quickstart 场景 4 | `test_exec_quant_engine.py` + 既有 feedback 集成测试 |

## Cross-cutting 记录

- **Shared Strings 消费**: `[[STR-001]]` speckit.exec-quant → 引擎 kind 常量 + 契约/测试;`[[STR-002]]` not_evaluated → 引擎未采标记 + V2 断言(复用运行判定词形,不新造词表)。
- **Tool 晋升评估(Constitution XII 后半)**: 引擎稳定后「执行量化采集/列出/打分」是否值得晋升 `.specify/memory/tools/` Tool 记录,留待 implement 期 wrap-up 以使用证据评估——本期不预建。
- **Out of Scope 守护**: 分析/报表/聚合/打分模型/保留策略/自动上送/会话文本采集——本设计未含任何对应实体;后续特性扩此数据集时须新开规格。
- **Feature 复审**: 本 plan 不新增 Feature、不废弃/合并既有 Feature;功能/非功能分类不变(059 为功能性观测能力)。
