"""Contract test: introspection report schema (req 047).

Pins contracts/introspection-report.md C-1..C-12 and data-model.md V-1..V-5
against the engine's parse/validate helpers (feedback_utils.parse_report /
feedback_utils.validate_report).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.contract.helpers_introspection import _record, _report_text, _write_report
from tests.script_api import feedback_utils


@pytest.mark.contract
class TestReportLocationAndNaming:
    """C-1/C-2: reports live under introspection/ subdir only."""

    def test_report_at_store_root_rejected(self, feedback_store: Path):
        eid = _record(feedback_store, "run-a")
        path = _write_report(feedback_store, "introspection-20260828T000000Z",
                             _report_text("introspection-20260828T000000Z", [eid]),
                             subdir=False)
        with pytest.raises(feedback_utils.FeedbackError):
            feedback_utils.parse_report(path)

    def test_report_in_subdir_accepted(self, feedback_store: Path):
        eid = _record(feedback_store, "run-b")
        path = _write_report(feedback_store, "introspection-20260828T000001Z",
                             _report_text("introspection-20260828T000001Z", [eid]))
        report = feedback_utils.parse_report(path)
        assert report["meta"]["id"] == "introspection-20260828T000001Z"
        assert len(report["findings"]) == 1


@pytest.mark.contract
class TestFrontmatter:
    """C-4/C-5: exact seven fields; id matches filename; no duplicate scope entries."""

    def test_missing_field_rejected(self, feedback_store: Path):
        eid = _record(feedback_store, "run-c")
        text = _report_text("introspection-20260828T000002Z", [eid]).replace(
            'scope_filter: "disposition=open"\n', "")
        path = _write_report(feedback_store, "introspection-20260828T000002Z", text)
        with pytest.raises(feedback_utils.FeedbackError):
            feedback_utils.parse_report(path)

    def test_unknown_field_rejected(self, feedback_store: Path):
        eid = _record(feedback_store, "run-d")
        text = _report_text("introspection-20260828T000003Z", [eid]).replace(
            "confirmed_at: null", "confirmed_at: null\nextra_field: 1")
        path = _write_report(feedback_store, "introspection-20260828T000003Z", text)
        with pytest.raises(feedback_utils.FeedbackError):
            feedback_utils.parse_report(path)

    def test_id_filename_mismatch_rejected(self, feedback_store: Path):
        eid = _record(feedback_store, "run-e")
        path = _write_report(feedback_store, "introspection-20260828T000004Z",
                             _report_text("introspection-99999999T999999Z", [eid]))
        with pytest.raises(feedback_utils.FeedbackError):
            feedback_utils.parse_report(path)

    def test_duplicate_scope_entries_rejected(self, feedback_store: Path):
        eid = _record(feedback_store, "run-f")
        text = _report_text("introspection-20260828T000005Z", [eid]).replace(
            f'scope_entries: ["{eid}"]', f'scope_entries: ["{eid}", "{eid}"]')
        path = _write_report(feedback_store, "introspection-20260828T000005Z", text)
        with pytest.raises(feedback_utils.FeedbackError):
            feedback_utils.parse_report(path)


@pytest.mark.contract
class TestFindingStructure:
    """C-6..C-9: section order, finding fields, five-element completeness."""

    def test_missing_excluded_section_rejected(self, feedback_store: Path):
        eid = _record(feedback_store, "run-g")
        text = _report_text("introspection-20260828T000006Z", [eid]).replace(
            "## Excluded", "## Gone")
        path = _write_report(feedback_store, "introspection-20260828T000006Z", text)
        with pytest.raises(feedback_utils.FeedbackError):
            feedback_utils.parse_report(path)

    def test_missing_five_element_rejected(self, feedback_store: Path):
        eid = _record(feedback_store, "run-h")
        text = _report_text("introspection-20260828T000007Z", [eid]).replace(
            "- **根因**: 根因陈述\n", "")
        path = _write_report(feedback_store, "introspection-20260828T000007Z", text)
        with pytest.raises(feedback_utils.FeedbackError):
            feedback_utils.parse_report(path)

    def test_unknown_finding_field_rejected(self, feedback_store: Path):
        eid = _record(feedback_store, "run-i")
        text = _report_text("introspection-20260828T000008Z", [eid],
                            findings_extra="- **臆造字段**: x\n")
        path = _write_report(feedback_store, "introspection-20260828T000008Z", text)
        with pytest.raises(feedback_utils.FeedbackError):
            feedback_utils.parse_report(path)

    def test_optional_fields_accepted(self, feedback_store: Path):
        eid = _record(feedback_store, "run-j")
        text = _report_text("introspection-20260828T000009Z", [eid],
                            findings_extra=(f"- **建议处置**: {eid}:processed\n"
                                            "- **用户覆盖**: upstream-bound → local-sink\n"))
        path = _write_report(feedback_store, "introspection-20260828T000009Z", text)
        report = feedback_utils.parse_report(path)
        finding = report["findings"][0]
        assert finding["suggestions"] == {eid: "processed"}
        assert finding["override"] is not None


@pytest.mark.contract
class TestSemanticValidation:
    """V-1 coverage, V-3 existence, V-4 external constraint, C-10 supersession."""

    def _parse(self, workspace: Path, report_id: str, text: str):
        path = _write_report(workspace, report_id, text)
        return feedback_utils.parse_report(path)

    def test_coverage_gap_rejected(self, feedback_store: Path):
        e1 = _record(feedback_store, "run-k")
        e2 = _record(feedback_store, "run-l")
        # scope declares e1+e2 but finding covers only e1 → V-1 violation
        text = _report_text("introspection-20260828T000010Z", [e1]).replace(
            f'scope_entries: ["{e1}"]', f'scope_entries: ["{e1}", "{e2}"]')
        report = self._parse(feedback_store, "introspection-20260828T000010Z", text)
        violations = feedback_utils.validate_report(feedback_store, report)
        assert any("V-1" in v for v in violations)

    def test_unknown_entry_rejected(self, feedback_store: Path):
        e1 = _record(feedback_store, "run-m")
        text = _report_text("introspection-20260828T000011Z",
                            ["20990101T000000Z-nonexistent"]).replace(
            'scope_entries: ["20990101T000000Z-nonexistent"]',
            f'scope_entries: ["20990101T000000Z-nonexistent", "{e1}"]')
        text = text.replace("## Excluded\n\n无",
                            f"## Excluded\n\n- {e1} — 排除")
        report = self._parse(feedback_store, "introspection-20260828T000011Z", text)
        violations = feedback_utils.validate_report(feedback_store, report)
        assert any("V-3" in v for v in violations)

    def test_external_member_upstream_rejected(self, feedback_store: Path):
        e1 = _record(feedback_store, "run-n")
        e2 = _record(feedback_store, "run-o", kind="external")
        text = _report_text("introspection-20260828T000012Z", [e1, e2])
        report = self._parse(feedback_store, "introspection-20260828T000012Z", text)
        violations = feedback_utils.validate_report(feedback_store, report)
        assert any("V-4" in v for v in violations)

    def test_supersedes_nonexistent_rejected(self, feedback_store: Path):
        e1 = _record(feedback_store, "run-p")
        text = _report_text("introspection-20260828T000013Z", [e1],
                            supersedes="introspection-20990101T000000Z")
        report = self._parse(feedback_store, "introspection-20260828T000013Z", text)
        violations = feedback_utils.validate_report(feedback_store, report)
        assert any("C-10" in v for v in violations)

    def test_clean_report_zero_violations(self, feedback_store: Path):
        e1 = _record(feedback_store, "run-q")
        report = self._parse(feedback_store, "introspection-20260828T000014Z",
                             _report_text("introspection-20260828T000014Z", [e1]))
        assert feedback_utils.validate_report(feedback_store, report) == []


@pytest.mark.contract
class TestUnicode:
    """C-3: CJK content survives parse round-trip unescaped."""

    def test_cjk_content_preserved(self, feedback_store: Path):
        e1 = _record(feedback_store, "run-r")
        report_id = "introspection-20260828T000015Z"
        report = feedback_utils.parse_report(_write_report(
            feedback_store, report_id, _report_text(report_id, [e1])))
        assert report["findings"][0]["root_cause"] == "根因陈述"
