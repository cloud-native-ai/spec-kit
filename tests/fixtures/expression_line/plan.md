# Implementation Plan: expression-line pilot (fixture)

**Spec**: [requirements.md](requirements.md)

## Summary

一条夹具线的 plan：它不交付任何运行时能力，用途是让八条阶段算子在一条**真实声明为表达类**的线上各跑一次，并把结果留给 `tests/integration/test_expression_line_pilot.py` 断言。

## Constitution Check

| Principle | Compliance | Evidence |
|-----------|------------|----------|
| I | Pass | 夹具只被一个集成测试读取，不进任何分发面 |

## Decision Tensions

### T-001 — 交付文档的顶层章节以 plan 的章节树为准，而不是以落文目录为准

- **decision**: 交付文档的顶层章节以 `## Document Structure` 的章节树表为准，implement 只按这张表落文。
- **antithesis**: 直接以交付文档的标题树为准，不必先写计划表；当文档只有一个读者、结构随手可改时，它确实少一步。
- **binding_constraints**:
  - pole_a: 结构判定必须只读计划表即可完成，否则 implement 期无法在落笔之前判对错。
  - pole_b: 计划表必须与落文可比对，否则计划与产物会各说一套。
- **discriminating_evidence**: 把章节树里的一节删掉后重跑结构子步，数「是否点名缺失的一节」；结果二值——点名（是／否）。
- **expected_sacrifice**: SC-001 Source ↓ 结构判定多了一道「先写计划」的前置，单篇小改也要先填表。
- **revision_trigger**: 两个迭代内出现 ≥2 次「为一行文案被迫先写整棵章节树」→ 重开，改为只对多章节文档要求计划表。

## Project Structure

```text
.specify/specs/777-expression-line-pilot/   # 本线规格
docs/                                       # 交付文档所在
```

## Document Structure

### Chapter Tree

| 节名 | 父节 | 目的 | 边界 |
|------|------|------|------|
| 概览 | — | 读者读完决定是否继续读下一节 | 本节不覆盖判定细节 |
| 判定 | 概览 | 读者读完决定用哪条命令复核 | 本节不覆盖模板接线 |

### Reader Baseline

**Readers**: 第一次接手这条夹具线的维护者，需要在十分钟内判断门禁是否真的跑过。
**Reading scenario**: 复跑集成测试之前，对照本文核对命令与期望。

### Evidence List

| 断言 | 证据等级 | as-of | source |
|------|----------|-------|--------|
| 这条夹具线被声明为表达类 | 实测 | 2026-10-30 | `flow-class-check.py --action lookup --unit-id spec:777-expression-line-pilot` |

### Fact Owners

| 事实 | owner 路径 | 章节锚 |
|------|------------|--------|
| 类别取值只有封闭二值 | `shared/definitions/flow-class-definitions.md` | § 取值 |
