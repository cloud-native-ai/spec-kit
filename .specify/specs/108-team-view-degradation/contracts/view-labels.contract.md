# Contract — Rendering Label Vocabulary (single live owner)

**Owner statement**: this file is the **single live owner** of the `/speckit.team view` rendering label vocabulary. It carries the members inherited from `.specify/specs/103-team-view/data-model.md` § Rendering Line Types plus the members 108 adds or amends. The 103 table is demoted to a dated record and MUST NOT be cited as a live owner after this feature lands; it is not edited (dated records are never rewritten).
**Pinning tests**: `tests/contract/test_team_view_degradation_contract.py` (closure of the program's label constants against this table; presence of the new forms), `tests/integration/test_team_view_degradation.py` (behavioural rendering of each member).
**Not owned here**: the degradation reason ids and exit map (`contracts/team-view-program.contract.md` C-104), report naming (`skills/internal/create-team/SKILL.md` § Report contract), per-group obligations (`contracts/presentation.contract.md`).

**C-401** Single owner and closure.

Every state or declaration label the default rendering emits MUST be a member of this file's tables, and every member MUST have at least one emitting site in the program; a label outside these tables or a table member with no emitter is a defect. Tests assert the closure in both directions. (FR-024)

**C-402** Missing-state subset (carried).

`缺失` (file/directory absent) · `为空` (present but zero entries) · `不可读` (present but parse/read failed) · `未记录` (an upstream segment was not recorded). The four MUST NOT be substituted for one another and a missing fact never renders as `0` or a fabricated value. (FR-010)

**C-403** Declaration subset (carried).

`已声明` (optional key present) · `未声明` (optional key absent; always accompanied by the owner's default pointer, rendered today as `未声明（默认值见 create-mode.md § Schema notes）`). (FR-024)

**C-404** Derived labels (carried).

`定义损坏` · `形态异常` · `悬空（dangling）` · `已列出` · `已聚合` · `本次无嵌套 SDD 调用` · `未声明 → active`. Meanings are the 103 ones, preserved verbatim. (FR-024)

**C-405** New derived labels (added by 108).

| Label | Meaning and emitting site |
|-------|---------------------------|
| `未识别（unrecognized）` | residue line (count + bounded examples) and the run-report state when only residue exists ("仅残留，最新不可确定") |
| `辅助产物（auxiliary）` | the auxiliary-artifact line (count + bounded examples) |
| `不可比对（not comparable）` | `roster_delta` state when the two rosters cannot be compared, always with a reason |
| `按声明 pattern 不适用` | a missing continuous-spine file under a declared non-`continuous` pattern |
| `适用性不可判定` | spine applicability when the pattern is undeclared (owner declares no default) |
| `goal 需归一为 anchor_slug` | the named state for a declared `goal` key (repair pointers accompany it) |
| `降级（degraded）` | the trailing non-group block heading listing active reasons (reason ids themselves are owned by the program contract) |

(FR-004, FR-008, FR-013, FR-016, FR-024)

**C-406** Residue line form.

The residue line reads `未识别（unrecognized）: 共 N 份；示例: <name>, …（省略 K）` (examples ≤ 3, omitted count always present when K > 0). The only-residue run-report state reads `未识别（unrecognized）—— 仅残留，最新不可确定`. (FR-004, FR-005)

**C-407** Roster not-comparable form.

`roster_delta` renders `不可比对（not comparable）（原因：<reason>）`; the `未记录` label MUST NOT stand for this state. (FR-016)

**C-408** Substitution prohibition.

A missing-state member MUST NOT be replaced by a derived label or vice versa; no catch-all word (e.g. `其他` / `未知`) may stand for an enumerated state; no label may be emitted with an empty reason where this contract requires one. (FR-010, FR-019)

**C-409** Existing lines unchanged for healthy inputs.

For a team satisfying the FR-022 healthy predicate, no line carrying these labels changes: the four-state lines, declaration lines and derived labels render exactly as the baseline program renders them (byte-identical stdout; see `contracts/team-view-program.contract.md` C-107). (FR-022, FR-025)
