"""Scoped tests for references/types/plantuml/scripts/native-readback.py.

All fixtures are synthetic and generic. The immutable private baseline is only
read when the caller supplies PLANTUML_BASELINE_DIR / PLANTUML_BASELINE_SEMANTICS
environment variables; nothing private is embedded here.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "native-readback.py"

SEMANTICS = {
    "zones": [
        {"id": "z_outer", "label": "Outer", "parent": None},
        {"id": "z_inner", "label": "Inner", "parent": "z_outer"},
    ],
    "elements": [
        {"id": "a", "label": "Alpha", "zone": "z_outer"},
        {"id": "b", "label": "Beta", "zone": "z_inner"},
        {"id": "c", "label": "Gamma", "zone": "z_inner"},
        {"id": "d", "label": "Gamma", "zone": "z_outer"},
    ],
    "relations": [
        {"id": "R1", "from": "a", "to": "b", "label": "calls", "color": "#112233"},
        {"id": "R2", "from": "c", "to": "d", "color": "#445566"},
    ],
}

AUTHORIZED_LEGEND = {
    "legend": [{"color": "#112233", "text": "calls path"}],
}

SOURCE = """@startuml
skinparam monochrome false
legend right
| <color:#112233>●</color> | calls path |
endlegend
package "Outer" as z_outer <<zone>> {
  component "Alpha" as a <<el>>
  component "Gamma" as d <<el>>
  package "Inner" as z_inner <<sub>> {
    component "Beta" as b <<el>>
    component "Gamma" as c <<el>>
  }
}
a -[#112233]down-> b : calls
c -[#445566]-> d
@enduml
"""

SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400">
  <g class="cluster" data-qualified-name="z_outer" id="ent1">
    <rect x="10" y="10" width="520" height="320" fill="none" style="stroke:#37474F;stroke-width:3;"/>
    <text x="20" y="35" font-size="16" textLength="50">Outer</text>
  </g>
  <g class="cluster" data-qualified-name="z_outer.z_inner" id="ent2">
    <rect x="200" y="90" width="260" height="180" fill="none" style="stroke:#607D8B;stroke-width:2;"/>
    <text x="210" y="115" font-size="16" textLength="45">Inner</text>
  </g>
  <g class="entity" data-qualified-name="z_outer.a" id="ent3">
    <rect x="40" y="60" width="80" height="40" fill="#EEEEEE" style="stroke:#78909C;stroke-width:1.2;"/>
    <text x="50" y="85" font-size="16" textLength="40">Alpha</text>
  </g>
  <g class="entity" data-qualified-name="z_outer.d" id="ent4">
    <rect x="40" y="210" width="80" height="40" fill="#EEEEEE" style="stroke:#78909C;stroke-width:1.2;"/>
    <text x="50" y="235" font-size="16" textLength="45">Gamma</text>
  </g>
  <g class="entity" data-qualified-name="z_outer.z_inner.b" id="ent5">
    <rect x="240" y="140" width="80" height="40" fill="#EEEEEE" style="stroke:#78909C;stroke-width:1.2;"/>
    <text x="250" y="165" font-size="16" textLength="35">Beta</text>
  </g>
  <g class="entity" data-qualified-name="z_outer.z_inner.c" id="ent6">
    <rect x="240" y="220" width="80" height="40" fill="#EEEEEE" style="stroke:#78909C;stroke-width:1.2;"/>
    <text x="250" y="245" font-size="16" textLength="45">Gamma</text>
  </g>
  <g class="link" data-entity-1="ent3" data-entity-2="ent5" data-link-type="dependency" id="lnk1">
    <path d="M120,80 L240,150" fill="none" style="stroke:#112233;stroke-width:1.2;"/>
    <polygon fill="#112233" points="240,150,232,142,236,136" style="stroke:#112233;stroke-width:1.2;"/>
    <text x="150" y="85" font-size="10" textLength="30">calls</text>
  </g>
  <g class="link" data-entity-1="ent6" data-entity-2="ent4" data-link-type="dependency" id="lnk2">
    <path d="M240,230 L120,230" fill="none" style="stroke:#445566;stroke-width:1.2;"/>
    <polygon fill="#445566" points="120,230,128,226,128,234" style="stroke:#445566;stroke-width:1.2;"/>
  </g>
  <g class="legend">
    <text x="600" y="60" font-size="16" textLength="20">●</text>
    <text x="630" y="60" font-size="16" textLength="80">calls path</text>
  </g>
</svg>
"""


def run_tool(tmp_path, source=SOURCE, semantics=None, svg=SVG, extra_args=(), output_name="report.json"):
    source_path = tmp_path / "diagram.puml"
    semantics_path = tmp_path / "semantics.json"
    output_path = tmp_path / output_name
    source_path.write_text(source, encoding="utf-8")
    semantics_path.write_text(json.dumps(semantics if semantics is not None else SEMANTICS), encoding="utf-8")
    args = [sys.executable, "-B", str(SCRIPT), "--source", str(source_path),
            "--semantics", str(semantics_path), "--output", str(output_path)]
    if svg is not None:
        svg_path = tmp_path / "diagram.svg"
        svg_path.write_text(svg, encoding="utf-8")
        args += ["--svg", str(svg_path)]
    args += list(extra_args)
    proc = subprocess.run(args, capture_output=True, text=True)
    report = None
    if output_path.exists():
        try:
            report = json.loads(output_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            report = None
    return proc, report


def codes(report, axis="semantic"):
    return {finding["code"] for finding in report[axis]["findings"]}


def test_positive_supported_syntax_and_authorized_legend(tmp_path):
    proc, report = run_tool(tmp_path, semantics={**SEMANTICS, **AUTHORIZED_LEGEND})
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert report["semantic"]["status"] == "pass"
    assert report["visual"]["status"] == "pass"
    assert report["status"] == "pass"
    assert report["records"]["source"]["elements"][0]["qualified_name"] == "z_outer.a"
    assert report["records"]["svg"]["counts"] == {"entities": 4, "clusters": 2, "links": 2}
    assert report["legend"]["authorization"]["authorized"] is True
    assert report["records"]["source"]["relations"][0]["color"] == "#112233"
    assert report["diff"]["duplicate_labels"]["match"] is True


def test_changed_alias_is_detected(tmp_path):
    source = SOURCE.replace('component "Alpha" as a', 'component "Alpha" as alpha2')
    source = source.replace("a -[#112233]", "alpha2 -[#112233]")
    proc, report = run_tool(tmp_path, source=source, semantics={**SEMANTICS, **AUTHORIZED_LEGEND})
    assert proc.returncode == 1
    assert {"element_missing", "element_extra"} <= codes(report)


def test_changed_parent_membership_is_detected(tmp_path):
    source = SOURCE.replace('package "Inner" as z_inner', 'package "Inner" as z_other')
    proc, report = run_tool(tmp_path, source=source, semantics={**SEMANTICS, **AUTHORIZED_LEGEND})
    assert proc.returncode == 1
    assert "zone_missing" in codes(report) or "zone_extra" in codes(report)
    assert "element_missing" in codes(report) or "element_extra" in codes(report)


def test_changed_endpoint_is_detected(tmp_path):
    source = SOURCE.replace("a -[#112233]down-> b", "a -[#112233]down-> c")
    proc, report = run_tool(tmp_path, source=source, semantics={**SEMANTICS, **AUTHORIZED_LEGEND})
    assert proc.returncode == 1
    assert "relation_endpoint_mismatch" in codes(report)
    assert "svg_link_missing" in codes(report, "visual")


def test_changed_relation_label_is_detected(tmp_path):
    source = SOURCE.replace(": calls", ": pings")
    proc, report = run_tool(tmp_path, source=source, semantics={**SEMANTICS, **AUTHORIZED_LEGEND})
    assert proc.returncode == 1
    assert "relation_label_mismatch" in codes(report)
    assert "svg_link_label_mismatch" in codes(report, "visual")


def test_invented_source_legend_is_rejected(tmp_path):
    proc, report = run_tool(tmp_path, semantics=SEMANTICS)  # no authorization
    assert proc.returncode == 1
    assert report["legend"]["authorization"]["authorized"] is False
    finding = next(f for f in report["semantic"]["findings"] if f["code"] == "unauthorized_legend_meaning")
    assert any("calls path" in row for row in finding["offending_rows"])
    assert "#112233" in finding["colors"]
    assert "unauthorized_visible_legend" in codes(report, "visual")


def test_extra_visible_svg_legend_text_is_rejected(tmp_path):
    svg = SVG.replace(
        '<text x="630" y="60" font-size="16" textLength="80">calls path</text>',
        '<text x="630" y="60" font-size="16" textLength="80">calls path</text>'
        '<text x="630" y="90" font-size="16" textLength="140">invented meaning</text>',
    )
    proc, report = run_tool(tmp_path, svg=svg, semantics={**SEMANTICS, **AUTHORIZED_LEGEND})
    assert proc.returncode == 1
    finding = next(f for f in report["visual"]["findings"] if f["code"] == "visible_legend_text_extra")
    assert finding["offending_text"] == "invented meaning"


def test_unsupported_diagram_type_is_partial_not_corruption(tmp_path):
    source = "@startwbs\n* Root\n** Leaf\n@endwbs\n"
    proc, report = run_tool(tmp_path, source=source, svg=None, semantics=SEMANTICS)
    assert proc.returncode == 3
    assert report["status"] == "partial"
    assert report["semantic"]["findings"] == []
    assert any(item["kind"] == "unsupported_diagram_type" for item in report["unsupported"])


def test_overwrite_refused(tmp_path):
    output_path = tmp_path / "report.json"
    output_path.write_text("keep me", encoding="utf-8")
    proc, _ = run_tool(tmp_path, semantics={**SEMANTICS, **AUTHORIZED_LEGEND})
    assert proc.returncode == 2
    assert output_path.read_text(encoding="utf-8") == "keep me"


def test_unknown_flag_rejected(tmp_path):
    proc, _ = run_tool(tmp_path, semantics={**SEMANTICS, **AUTHORIZED_LEGEND}, extra_args=["--bogus"])
    assert proc.returncode == 2


def test_help_and_version_are_non_acting():
    for flag in ("--help", "--version"):
        proc = subprocess.run([sys.executable, "-B", str(SCRIPT), flag], capture_output=True, text=True)
        assert proc.returncode == 0
        assert proc.stdout.strip()


@pytest.mark.skipif(
    not (os.environ.get("PLANTUML_BASELINE_DIR") and os.environ.get("PLANTUML_BASELINE_SEMANTICS")),
    reason="caller-provided baseline paths not supplied",
)
def test_private_baseline_rejected_for_real_legend_defect(tmp_path):
    baseline = Path(os.environ["PLANTUML_BASELINE_DIR"])
    semantics = Path(os.environ["PLANTUML_BASELINE_SEMANTICS"])
    output_path = tmp_path / "baseline.json"
    proc = subprocess.run([
        sys.executable, "-B", str(SCRIPT),
        "--source", str(baseline / "architecture.puml"),
        "--semantics", str(semantics),
        "--svg", str(baseline / "architecture.svg"),
        "--output", str(output_path),
    ], capture_output=True, text=True)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    report = json.loads(output_path.read_text(encoding="utf-8"))
    assert report["status"] == "fail"
    assert report["unsupported"] == []
    assert report["diff"]["elements_missing"] == []
    assert report["diff"]["elements_extra"] == []
    assert report["diff"]["zones_missing"] == []
    assert report["diff"]["zones_extra"] == []
    assert report["diff"]["element_label_mismatch"] == []
    assert report["diff"]["zone_label_mismatch"] == []
    assert report["records"]["svg"]["counts"]["entities"] == 82
    assert report["records"]["svg"]["counts"]["clusters"] == 24
    assert report["records"]["svg"]["counts"]["links"] == 46
    finding = next(f for f in report["semantic"]["findings"] if f["code"] == "unauthorized_legend_meaning")
    assert any("采集 / 上报链路" in row for row in finding["offending_rows"])
    assert "#d12f32" in finding["colors"]
    visible = next(f for f in report["visual"]["findings"] if f["code"] == "unauthorized_visible_legend")
    assert any("采集 / 上报链路" in text for text in visible["visible_texts"])
