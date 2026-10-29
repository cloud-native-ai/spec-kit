# Requirements: expression-line pilot (fixture)

**Feature Branch**: `777-expression-line-pilot`
**Created**: 2026-10-30
**Status**: Draft
**Flow Class**: expression
**Input**: Synthetic fixture line for `tests/integration/test_expression_line_pilot.py`. It is not a customer line and carries no delivery claim of its own.

> **fixture 说明**：本文件是 077 的**合成夹具线**，只为在真实门禁上跑完八条阶段算子。章节树、读者、证据与 owner 四项都是最小可用形态，不是任何真实需求。

## Related Feature *(mandatory)*

**Feature ID**: 777
**Feature Name**: expression-line pilot (fixture)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 本线的 `plan.md` MUST 在 `## Document Structure` 里给出章节树，且交付文档的顶层章节 MUST 与该表逐名一致。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 交付文档 MUST 通过四面门禁（`reader` / `evidence` / `duplicate` / `count` 全部 `pass`）与结构子步（零 finding），判定只读退出码与输出行。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 对交付文档跑 `doc-consistency-check.py --action verify --faces reader,evidence,duplicate,count --path <交付文档>` 与 `--action structure --spec-dir <spec 目录> --path <交付文档>`，只读退出码与 `faces:` / `status:` 行。
