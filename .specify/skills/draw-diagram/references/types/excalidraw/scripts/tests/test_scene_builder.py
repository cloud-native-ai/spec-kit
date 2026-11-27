"""Engine-local tests: programmatic scene generation (generic fixtures only).

These tests import the engine scripts directly and assert the *native* scene:
counts/ids, genuine container bindings in both directions, zone-endpoint
preservation, group memberships, label-anchor safety, deterministic output,
semantics rejection, and the CLI contract (--help/--version/unknown flag/
overwrite refusal).
"""
import copy
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1]
BUILDER = SCRIPTS / "scene_builder.py"
GENERATE = SCRIPTS / "generate-scene.py"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sb = _load("scene_builder_under_test", BUILDER)


def fixture():
    return {
        "title": "Fixture Title",
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
def built():
    scene, report = sb.generate_scene(fixture())
    return scene, report


def by_id(scene):
    return {e["id"]: e for e in scene["elements"]}


def test_counts_and_ids_preserved(built):
    scene, report = built
    ids = by_id(scene)
    data = fixture()
    for element in data["elements"]:
        assert element["id"] in ids
    for zone in data["zones"]:
        assert zone["id"] in ids
    for rel in data["relations"]:
        assert rel["id"] in ids
    assert report["counts"] == {"elements": 6, "zones": 4, "relations": 5, "labels": 1}


def test_component_labels_are_genuinely_bound(built):
    scene, _ = built
    ids = by_id(scene)
    for element in fixture()["elements"]:
        rect = ids[element["id"]]
        texts = [b for b in rect["boundElements"] if b["type"] == "text"]
        assert len(texts) == 1, element["id"]
        text = ids[texts[0]["id"]]
        assert text["containerId"] == element["id"]
        assert text["text"] == element["label"]
        assert text["textAlign"] == "center" and text["verticalAlign"] == "middle"


def test_relation_endpoints_and_reciprocals(built):
    scene, _ = built
    ids = by_id(scene)
    for rel in fixture()["relations"]:
        arrow = ids[rel["id"]]
        assert arrow["startBinding"]["elementId"] == rel["from"]
        assert arrow["endBinding"]["elementId"] == rel["to"]
        for target in (rel["from"], rel["to"]):
            assert any(b["id"] == rel["id"] for b in ids[target]["boundElements"]), (rel["id"], target)


def test_zone_endpoint_stays_zone_not_member(built):
    scene, _ = built
    ids = by_id(scene)
    arrow = ids["r_zone_end"]
    assert arrow["endBinding"]["elementId"] == "z_east_sub"
    # reciprocal registration on the zone rectangle itself
    assert any(b["id"] == "r_zone_end" for b in ids["z_east_sub"]["boundElements"])
    assert arrow["endBinding"]["elementId"] not in {e["id"] for e in fixture()["elements"]}


def test_relation_label_is_genuinely_bound_to_its_arrow(built):
    scene, report = built
    ids = by_id(scene)
    arrow = ids["r_labeled"]
    refs = [b for b in arrow["boundElements"] if b["type"] == "text"]
    assert len(refs) == 1
    text = ids[refs[0]["id"]]
    assert text["containerId"] == "r_labeled"
    assert text["text"] == "调用链"
    # the written position agrees with the renderer anchor (middle vertex)
    points = [(arrow["x"] + p[0], arrow["y"] + p[1]) for p in arrow["points"]]
    anchor = sb.label_anchor(points)
    assert text["x"] + text["width"] / 2.0 == pytest.approx(anchor[0], abs=0.6)
    assert text["y"] + text["height"] / 2.0 == pytest.approx(anchor[1], abs=0.6)
    assert report["label_problems"] == []


def test_groups_cover_components_and_ancestor_zones(built):
    scene, _ = built
    ids = by_id(scene)
    for element in fixture()["elements"]:
        rect = ids[element["id"]]
        label = ids[f"label-{element['id']}"]
        assert f"cg-{element['id']}" in rect["groupIds"]
        assert set(rect["groupIds"]) & set(label["groupIds"])
        assert f"zg-{element['zone']}" in rect["groupIds"]
    # nested zone element carries both its zone group and the ancestor group
    child = ids["child_1"]
    assert "zg-z_east_sub" in child["groupIds"] and "zg-z_east" in child["groupIds"]


def test_hard_geometry_is_clean(built):
    _, report = built
    assert report["edge_through_component"] == []
    assert report["label_problems"] == []
    assert report["binding_problems"] == []
    for rid, box in report["label_boxes"].items():
        assert box[2] > 0 and box[3] > 0, rid


def test_deterministic_output():
    one, _ = sb.generate_scene(copy.deepcopy(fixture()))
    two, _ = sb.generate_scene(copy.deepcopy(fixture()))
    assert json.dumps(one, sort_keys=True) == json.dumps(two, sort_keys=True)


@pytest.mark.parametrize("mutate,fragment", [
    (lambda d: d["elements"].append(dict(d["elements"][0])), "duplicate element id"),
    (lambda d: d["relations"][0].update({"to": "nope"}), "unknown"),
    (lambda d: d["zones"][1].update({"parent": "z_east_sub"}), "cycle"),
    (lambda d: d["relations"][0].update({"to": d["relations"][0]["from"]}), "self loop"),
    (lambda d: d["counts"].update({"elements": 99}) if "counts" in d else d.update({"counts": {"elements": 99}}), "counts"),
])
def test_invalid_semantics_rejected(mutate, fragment):
    data = fixture()
    mutate(data)
    with pytest.raises(sb.SemanticsError) as exc:
        sb.validate_semantics(data)
    assert fragment in str(exc.value)


def run_cli(args, cwd):
    return subprocess.run([sys.executable, str(GENERATE)] + args, cwd=cwd,
                          capture_output=True, text=True, timeout=120)


def test_cli_help_and_version(tmp_path):
    help_run = run_cli(["--help"], tmp_path)
    assert help_run.returncode == 0 and "exit codes" in help_run.stdout
    version_run = run_cli(["--version"], tmp_path)
    assert version_run.returncode == 0 and "generate-scene.py" in version_run.stdout


def test_cli_rejects_unknown_flag(tmp_path):
    out = run_cli(["--semantics", "x", "--output", "y", "--bogus"], tmp_path)
    assert out.returncode != 0


def test_cli_refuses_overwrite(tmp_path):
    sem = tmp_path / "sem.json"
    sem.write_text(json.dumps(fixture()), encoding="utf-8")
    target = tmp_path / "scene.excalidraw"
    target.write_text("{}", encoding="utf-8")
    out = run_cli(["--semantics", str(sem), "--output", str(target)], tmp_path)
    assert out.returncode == 2
    assert "refusing to overwrite" in out.stderr


def test_cli_writes_scene_and_report(tmp_path):
    sem = tmp_path / "sem.json"
    sem.write_text(json.dumps(fixture()), encoding="utf-8")
    scene = tmp_path / "scene.excalidraw"
    report = tmp_path / "report.json"
    out = run_cli(["--semantics", str(sem), "--output", str(scene), "--report", str(report)], tmp_path)
    assert out.returncode == 0, out.stderr
    assert scene.is_file() and report.is_file()
    payload = json.loads(scene.read_text(encoding="utf-8"))
    assert payload["type"] == "excalidraw"
