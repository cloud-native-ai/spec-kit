# Requirements Specification: fixture alpha slice

**Requirement Branch**: `099a-fixture-alpha`
**Status**: Implemented

## Parent Mapping（父条目逐条映射）

**读法**: 左列是本切片的本地编号，右列是父规格 `.specify/specs/099-fixture-parent/requirements.md` 的原编号。

| Slice ID | Parent ID |
|----------|-----------|
| `FR-001` | `FR-001` |
| `SC-001` | `SC-001` |
| `STR-002` | `STR-002` |
| `C-001` | `C-001` |

## Functional Requirements

- **FR-001**: Alpha local phrasing of the parent alpha requirement.
- **FR-005**: Alpha-only requirement, appended by merge order.

## Success Criteria *(mandatory)*

- **SC-001**: Alpha local phrasing of the parent success criterion.

## Shared Strings *(optional)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-002` | `"parent-beta"` | shared with the parent registry |
| `STR-003` | `"alpha-only"` | slice-unique literal |
