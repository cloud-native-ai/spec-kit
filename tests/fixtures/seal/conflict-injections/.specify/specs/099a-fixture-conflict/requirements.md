# Requirements Specification: fixture alpha conflict slice

**Requirement Branch**: `099a-fixture-conflict`
**Status**: Implemented

## Parent Mapping（父条目逐条映射）

**读法**: 左列是本切片的本地编号，右列是父规格 `.specify/specs/099-fixture-parent/requirements.md` 的原编号。

| Slice ID | Parent ID |
|----------|-----------|
| `FR-001` | `FR-001` |

### Declared Section Rewrites

- `plan.md` § `Execution Model`

## Functional Requirements

- **FR-001**: Alpha phrasing of parent requirement one.
- **FR-002**: Alpha requirement that carries no parent mapping row.

## Shared Strings *(optional)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `"conflict-a"` | same number as the parent, different literal |
| `STR-002` | `"conflict-a-two"` | cross-registry ambiguity leg (alpha value) |
