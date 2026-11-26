"""Engine-local tests: independent native readback (positive + negative fixtures).

Each negative case mutates a generated native scene in one specific way and
asserts that the readback reports the matching hard discrepancy. The readback
must detect changed IDs, endpoint/direction changes, membership/parent changes,
label changes, broken genuine binding, hidden legend text and geometry defects.
"""
import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1]
BUILDER = SCRIPTS / "scene_builder.py"
READBACK = SCRIPTS / "native-readback.py"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sb = _load("scene_builder_for_readback_tests", BUILDER)
rb = _load("native_readback_under_test", READBACK)


def fixture():
    return {
        "title": "Readback Fixture",
        "elements": [
            {"id": "svc_a", "label": "服务甲", "zone": "z_west"},
            {"id": "svc_b", "label": "worker", "zone": "z_west"},
            {"id": "db_1", "label": "存储一", "zone": "z_east"},
            {"id": "db_2", "label": "缓存二", "zone": "z_east"},
            {"id": "child_1", "label": "子组件", "zone": "z_east_sub"},
            {"id": "ext_1", "label": "外部", "zone": "z_isolated"},
        ],
        "zones": [
            {"id": "z_west", "label": "西区", "parent": None},
            {"id": "z_east", "label": "东区", "parent": None},
            {"id": "z_east_sub", "label": "东子区", "parent": "z_east"},
            {"id": "z_isolated", "label": "隔离区", "parent": None},
        ],
        "relations": [
            {"id": "r_labeled", "from": "svc_a", "to": "db_1", "label": "调用链", "color": "#334155"},
            {"id": "r_plain", "from": "svc_b", "to": "db_2", "color": "#d12f32"},
            {"id": "r_nested", "from": "db_1", "to": "child_1", "color": "#16824b"},
            {"id": "r_zone_end", "from": "ext_1", "to": "z_east_sub", "color": "#334155"},
            {"id": "r_zone_src", "from": "db_2", "to": "z_west", "color": "#334155"},
        ],
    }


@pytest.fixture(scope="module")
def base():
    scene, _report = sb.generate_scene(fixture())
    return scene


def element(scene, eid):
    return next(e for e in scene["elements"] if e["id"] == eid)


def codes(report):
    return [issue["code"] for issue in report["issues"]]


def test_positive_scene_reads_back_clean(base, tmp_path):
    path = tmp_path / "scene.excalidraw"
    path.write_text(json.dumps(base, ensure_ascii=False), encoding="utf-8")
    report, status = rb.readback(path, copy.deepcopy(fixture()))
    assert codes(report) == []
    assert report["semantic"]["status"] == "pass"
    assert report["geometry"]["status"] == "pass"
    assert status == "partial"  # no SVG evidence requested -> partial, never pass
    assert report["binding_summary"]["relation_labels_genuine"] == 1
    assert report["binding_summary"]["component_labels_bound"] == 6
    assert report["svg"]["provided"] is False


def test_detects_changed_element_id(base, tmp_path):
    scene = copy.deepcopy(base)
    element(scene, "svc_a")["id"] = "svc_renamed"
    path = tmp_path / "scene.excalidraw"
    path.write_text(json.dumps(scene, ensure_ascii=False), encoding="utf-8")
    report, status = rb.readback(path, copy.deepcopy(fixture()))
    assert "element-missing" in codes(report)
    assert "element-extra" in codes(report)
    assert status == "fail"


def test_detects_reversed_direction(base, tmp_path):
    scene = copy.deepcopy(base)
    arrow = element(scene, "r_plain")
    arrow["startBinding"], arrow["endBinding"] = arrow["endBinding"], arrow["startBinding"]
    path = tmp_path / "scene.excalidraw"
    path.write_text(json.dumps(scene, ensure_ascii=False), encoding="utf-8")
    report, _ = rb.readback(path, copy.deepcopy(fixture()))
    assert "direction-reversed" in codes(report)


def test_detects_label_change(base, tmp_path):
    scene = copy.deepcopy(base)
    element(scene, "label-db_1")["text"] = "被篡改"
    path = tmp_path / "scene.excalidraw"
    path.write_text(json.dumps(scene, ensure_ascii=False), encoding="utf-8")
    report, _ = rb.readback(path, copy.deepcopy(fixture()))
    assert "label-mismatch" in codes(report)


def test_detects_broken_genuine_arrow_label_binding(base, tmp_path):
    scene = copy.deepcopy(base)
    arrow = element(scene, "r_labeled")
    arrow["boundElements"] = [b for b in arrow["boundElements"] if b["type"] != "text"]
    path = tmp_path / "scene.excalidraw"
    path.write_text(json.dumps(scene, ensure_ascii=False), encoding="utf-8")
    report, _ = rb.readback(path, copy.deepcopy(fixture()))
    assert "relation-label-not-genuinely-bound" in codes(report)


def test_detects_unbound_component_label(base, tmp_path):
    scene = copy.deepcopy(base)
    element(scene, "label-svc_b")["containerId"] = None
    path = tmp_path / "scene.excalidraw"
    path.write_text(json.dumps(scene, ensure_ascii=False), encoding="utf-8")
    report, _ = rb.readback(path, copy.deepcopy(fixture()))
    assert "label-unbound" in codes(report)


def test_detects_zone_membership_change(base, tmp_path):
    scene = copy.deepcopy(base)
    rect = element(scene, "db_1")
    west = element(scene, "z_west")
    rect["x"] = west["x"] + 10
    rect["y"] = west["y"] + 40
    path = tmp_path / "scene.excalidraw"
    path.write_text(json.dumps(scene, ensure_ascii=False), encoding="utf-8")
    report, _ = rb.readback(path, copy.deepcopy(fixture()))
    assert "zone-membership-mismatch" in codes(report)


def test_detects_zone_parent_change(base, tmp_path):
    scene = copy.deepcopy(base)
    sub = element(scene, "z_east_sub")
    sub["x"] = 5.0
    sub["y"] = 5.0
    path = tmp_path / "scene.excalidraw"
    path.write_text(json.dumps(scene, ensure_ascii=False), encoding="utf-8")
    report, _ = rb.readback(path, copy.deepcopy(fixture()))
    assert "zone-parent-mismatch" in codes(report)


def test_detects_hidden_legend_text(base, tmp_path):
    scene = copy.deepcopy(base)
    scene["elements"].append({
        "id": "legend-x", "type": "text", "x": 10, "y": 10, "width": 80, "height": 18,
        "text": "红色=采集链路", "fontSize": 16, "containerId": None, "groupIds": [],
        "boundElements": [], "customData": {"role": "legend"},
    })
    path = tmp_path / "scene.excalidraw"
    path.write_text(json.dumps(scene, ensure_ascii=False), encoding="utf-8")
    report, _ = rb.readback(path, copy.deepcopy(fixture()))
    assert "extra-text" in codes(report)
    items = next(i for i in report["issues"] if i["code"] == "extra-text")["items"]
    assert any("红色" in item["text"] for item in items)


def test_detects_zone_endpoint_expanded_to_member(base, tmp_path):
    scene = copy.deepcopy(base)
    arrow = element(scene, "r_zone_end")
    arrow["endBinding"]["elementId"] = "child_1"
    element(scene, "child_1")["boundElements"].append({"id": "r_zone_end", "type": "arrow"})
    path = tmp_path / "scene.excalidraw"
    path.write_text(json.dumps(scene, ensure_ascii=False), encoding="utf-8")
    report, _ = rb.readback(path, copy.deepcopy(fixture()))
    found = codes(report)
    assert "endpoint-mismatch" in found
    assert "endpoint-expanded-to-member" in found


def test_detects_edge_through_component(base, tmp_path):
    scene = copy.deepcopy(base)
    target = element(scene, "db_1")
    arrow = element(scene, "r_plain")
    arrow["x"] = target["x"] - 150
    arrow["y"] = target["y"] + target["height"] / 2.0
    arrow["points"] = [[0, 0], [400, 0]]
    path = tmp_path / "scene.excalidraw"
    path.write_text(json.dumps(scene, ensure_ascii=False), encoding="utf-8")
    report, _ = rb.readback(path, copy.deepcopy(fixture()))
    assert "edge-through-component" in codes(report)


def test_detects_label_over_component(base, tmp_path):
    scene = copy.deepcopy(base)
    target = element(scene, "db_2")
    arrow = element(scene, "r_labeled")
    arrow["x"] = target["x"] + target["width"] / 2.0 - 100
    arrow["y"] = target["y"] + target["height"] / 2.0
    arrow["points"] = [[0, 0], [100, 0], [200, 0]]
    path = tmp_path / "scene.excalidraw"
    path.write_text(json.dumps(scene, ensure_ascii=False), encoding="utf-8")
    report, _ = rb.readback(path, copy.deepcopy(fixture()))
    assert "label-over-component" in codes(report)


def test_detects_endpoint_off_boundary(base, tmp_path):
    scene = copy.deepcopy(base)
    arrow = element(scene, "r_plain")
    arrow["x"] = 3000
    arrow["y"] = 3000
    arrow["points"] = [[0, 0], [100, 0]]
    path = tmp_path / "scene.excalidraw"
    path.write_text(json.dumps(scene, ensure_ascii=False), encoding="utf-8")
    report, _ = rb.readback(path, copy.deepcopy(fixture()))
    assert "endpoint-off-boundary" in codes(report)


def run_cli(args, cwd):
    return subprocess.run([sys.executable, str(READBACK)] + args, cwd=cwd,
                          capture_output=True, text=True, timeout=120)


def test_cli_contract(tmp_path):
    help_run = run_cli(["--help"], tmp_path)
    assert help_run.returncode == 0 and "exit codes" in help_run.stdout
    version_run = run_cli(["--version"], tmp_path)
    assert version_run.returncode == 0 and "native-readback.py" in version_run.stdout
    unknown = run_cli(["--source", "a", "--semantics", "b", "--output", "c", "--nope"], tmp_path)
    assert unknown.returncode == 2


def test_cli_refuses_overwrite_and_reports_partial(base, tmp_path):
    scene_path = tmp_path / "scene.excalidraw"
    scene_path.write_text(json.dumps(base, ensure_ascii=False), encoding="utf-8")
    sem_path = tmp_path / "sem.json"
    sem_path.write_text(json.dumps(fixture(), ensure_ascii=False), encoding="utf-8")
    report_path = tmp_path / "report.json"
    first = run_cli(["--source", str(scene_path), "--semantics", str(sem_path),
                     "--output", str(report_path)], tmp_path)
    assert first.returncode == 3, first.stderr  # partial: SVG evidence missing
    assert report_path.is_file()
    second = run_cli(["--source", str(scene_path), "--semantics", str(sem_path),
                      "--output", str(report_path)], tmp_path)
    assert second.returncode == 2
    assert "refusing to overwrite" in second.stderr


def _duplicate_label_fixture():
    data = fixture()
    for element in data["elements"]:
        if element["id"] == "svc_b":
            element["label"] = "MCP"
    for rel in data["relations"]:
        if rel["id"] == "r_labeled":
            rel["label"] = "MCP"
        if rel["id"] == "r_plain":
            rel["label"] = "第二标注"
    return data


def _svg_for(scene, semantics, shift=(-50.0, -43.9), swap_fills=False, include_rects=True):
    """Synthesize an SVG that mirrors the scene under a constant export shift.

    Relation labels are drawn in the arrow colour; component labels in black.
    With swap_fills the duplicate label string is given the other colour, which
    must defeat a naive content-only match. include_rects=False omits every
    shape, simulating a parser/format limitation.
    """
    by_id = {e["id"]: e for e in scene["elements"]}
    zone_ids = {z["id"] for z in semantics["zones"]}
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4000 3000">']
    for e in scene["elements"]:
        if e.get("type") != "rectangle" or not include_rects:
            continue
        parts.append(f'<rect x="{e["x"] + shift[0]:.2f}" y="{e["y"] + shift[1]:.2f}" '
                     f'width="{e["width"]:.2f}" height="{e["height"]:.2f}" fill="#ffffff"/>')
    for e in scene["elements"]:
        cd = e.get("customData") or {}
        if e.get("type") != "text":
            continue
        role = cd.get("role")
        if role == "component-label":
            container = by_id[e["containerId"]]
            cx = container["x"] + container["width"] / 2.0
            cy = container["y"] + container["height"] / 2.0
            color = "#334155" if swap_fills else "#1e1e1e"
        elif role == "relation-label":
            arrow = by_id[cd["labelFor"]]
            pts = [(arrow["x"] + p[0], arrow["y"] + p[1]) for p in arrow["points"]]
            cx, cy = rb.label_anchor(pts)
            color = "#1e1e1e" if swap_fills else (arrow.get("strokeColor") or "#334155")
        else:
            cx = e["x"] + e["width"] / 2.0
            cy = e["y"] + e["height"] / 2.0
            color = e.get("strokeColor") or "#1e1e1e"
        x = cx + shift[0]
        y = cy + shift[1] - e["fontSize"] * 1.25 / 2.0
        parts.append(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{e["fontSize"]}px" '
                     f'fill="{color}" text-anchor="middle">{e["text"]}</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def test_svg_duplicate_label_is_matched_by_arrow_colour(tmp_path):
    semantics = _duplicate_label_fixture()
    scene, _ = sb.generate_scene(copy.deepcopy(semantics))
    scene_path = tmp_path / "scene.excalidraw"
    scene_path.write_text(json.dumps(scene, ensure_ascii=False), encoding="utf-8")
    svg_path = tmp_path / "scene.svg"
    svg_path.write_text(_svg_for(scene, semantics), encoding="utf-8")
    report, status = rb.readback(scene_path, copy.deepcopy(semantics), svg_path)
    assert codes(report) == []
    assert report["svg"]["status"] == "pass"
    assert report["svg"]["anchor_shift_consistent"] is True
    assert status == "pass"


def test_svg_swapped_duplicate_colours_are_detected(tmp_path):
    semantics = _duplicate_label_fixture()
    scene, _ = sb.generate_scene(copy.deepcopy(semantics))
    scene_path = tmp_path / "scene.excalidraw"
    scene_path.write_text(json.dumps(scene, ensure_ascii=False), encoding="utf-8")
    svg_path = tmp_path / "scene.svg"
    svg_path.write_text(_svg_for(scene, semantics, swap_fills=True), encoding="utf-8")
    report, status = rb.readback(scene_path, copy.deepcopy(semantics), svg_path)
    detected = ("svg-label-over-component" in codes(report)
                or "svg-label-over-component-mapped" in codes(report)
                or any(s.get("code") == "renderer-anchor-shift-inconsistent" for s in report["soft_issues"]))
    assert detected and status != "pass"


def test_svg_unmatched_component_boxes_are_reported_not_clean(tmp_path):
    semantics = _duplicate_label_fixture()
    scene, _ = sb.generate_scene(copy.deepcopy(semantics))
    scene_path = tmp_path / "scene.excalidraw"
    scene_path.write_text(json.dumps(scene, ensure_ascii=False), encoding="utf-8")
    svg_path = tmp_path / "scene.svg"
    svg_path.write_text(_svg_for(scene, semantics, include_rects=False), encoding="utf-8")
    report, status = rb.readback(scene_path, copy.deepcopy(semantics), svg_path)
    assert report["svg"]["component_box_check"].startswith("unsupported")
    assert any(s.get("code") == "svg-component-boxes-unmatched" for s in report["soft_issues"])
    assert status == "partial"
