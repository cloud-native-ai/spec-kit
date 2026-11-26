"""Positive/negative tests for native-readback.py on generic synthetic data.

The fixture is a small generic graph (no private business content). The SVG is
built from the actual native file under test, so the visual checks compare
rendered geometry with the file's own native geometry.
"""
import importlib.util
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET


HERE = Path(__file__).resolve().parents[1]
READBACK = HERE / "native-readback.py"
COMPILER = HERE / "architecture.py"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def base_plan():
    return {
        "title": "读回测试图",
        "canvas": {"w": 620, "h": 420},
        "fidelity_intent": "reproduction",
        "layout_policy": "optimize",
        "zones": [
            {"id": "outer", "label": "外区", "box": {"x": 10, "y": 10, "w": 600, "h": 400}},
            {"id": "inner", "label": "内区", "parent": "outer", "box": {"x": 300, "y": 70, "w": 280, "h": 310}},
        ],
        "elements": [
            {"id": "a", "label": "甲", "zone": "outer", "box": {"x": 60, "y": 90, "w": 100, "h": 50}},
            {"id": "b", "label": "乙", "zone": "inner", "box": {"x": 380, "y": 130, "w": 100, "h": 50}},
            {"id": "c", "label": "丙", "zone": "outer", "box": {"x": 60, "y": 300, "w": 100, "h": 50}},
            {"id": "d", "label": "丁", "zone": "inner", "box": {"x": 380, "y": 300, "w": 100, "h": 50}},
        ],
        "relations": [
            {"id": "r1", "from": "a", "to": "b", "label": "调用", "color": "#334155"},
            {"id": "r2", "from": "b", "to": "c", "color": "#334155"},
            {"id": "r3", "from": "c", "to": "d", "color": "#334155"},
        ],
    }


def semantics_of(plan):
    relations = []
    for row in plan["relations"]:
        entry = {"id": row["id"], "from": row["from"], "to": row["to"]}
        if row.get("label"):
            entry["label"] = row["label"]
        if row.get("color"):
            entry["color"] = row["color"]
        relations.append(entry)
    return {
        "elements": [{"id": row["id"], "label": row["label"], "zone": row["zone"]} for row in plan["elements"]],
        "zones": [{"id": row["id"], "label": row["label"], "parent": row.get("parent")} for row in plan["zones"]],
        "relations": relations,
    }


class ReadbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readback = load(READBACK, "native_readback")
        cls.compiler = load(COMPILER, "architecture_under_readback_test")
        root = Path(os.environ["DRAW_DIAGRAM_TEST_OUTPUT"])
        if not root.is_dir():
            raise RuntimeError("DRAW_DIAGRAM_TEST_OUTPUT must be an existing directory")
        cls.output = Path(tempfile.mkdtemp(prefix="readback-tests-", dir=str(root)))

    def workspace(self):
        return Path(tempfile.mkdtemp(prefix="case-", dir=str(self.output)))

    def compile_case(self, plan=None, name="native"):
        directory = self.workspace()
        xml, report = self.compiler.compile_diagram(plan or base_plan())
        self.assertEqual(report["status"], "pass", report)
        native = directory / (name + ".drawio")
        native.write_text(xml, encoding="utf-8")
        semantics = directory / "semantics.json"
        semantics.write_text(json.dumps(semantics_of(plan or base_plan()), ensure_ascii=False), encoding="utf-8")
        return directory, native, semantics, xml

    def write(self, directory, name, content):
        path = directory / name
        path.write_text(content, encoding="utf-8")
        return path

    def build_svg(self, native_path, name="render", overrides=None, offset=(-9.0, -13.0)):
        native = self.readback.parse_native(native_path)
        cells = native["cells"]
        boxes = {ident: tuple(record["box"]) for ident, record in cells.items() if record["kind"] != "edge"}
        ox, oy = offset
        root = ET.Element("svg", xmlns="http://www.w3.org/2000/svg")
        layer = ET.SubElement(root, "g", transform="translate(%g,%g)" % (ox, oy))
        for ident in sorted(boxes):
            record, box = cells[ident], boxes[ident]
            group = ET.SubElement(layer, "g", {"data-cell-id": ident})
            if record["kind"] == "zone":
                path = ET.SubElement(group, "path", fill="none", stroke="#444444")
                path.set("d", "M %g %g L %g %g L %g %g L %g %g Z" % (box[0], box[1], box[2], box[1], box[2], box[3], box[0], box[3]))
            else:
                ET.SubElement(group, "rect", x=str(box[0]), y=str(box[1]), width=str(box[2] - box[0]), height=str(box[3] - box[1]), fill="#ffffff", stroke="#444444")
        for ident, record in sorted(cells.items()):
            if record["kind"] != "edge":
                continue
            start, end = self.readback.route_of(record, boxes)
            parent = record["parent"]
            parent_offset = boxes[parent][:2] if parent != "1" and parent in boxes else (0.0, 0.0)
            points = [start] + [(x + parent_offset[0], y + parent_offset[1]) for x, y in record["waypoints_relative"]] + [end]
            override = (overrides or {}).get(ident, {})
            body = override.get("points", points)
            group = ET.SubElement(layer, "g", {"data-cell-id": ident})
            inner = ET.SubElement(group, "g")
            body_path = ET.SubElement(inner, "path", fill="none", stroke="#334155")
            body_path.set("d", "M " + " L ".join("%g %g" % (point[0], point[1]) for point in body))
            tip = override.get("arrow_tip", body[-1])
            tail = body[-2] if len(body) > 1 else body[0]
            ax, ay = tip[0] - tail[0], tip[1] - tail[1]
            length = math.hypot(ax, ay) or 1.0
            ux, uy = ax / length, ay / length
            base = (tip[0] - 8 * ux, tip[1] - 8 * uy)
            arrow = ET.SubElement(inner, "path", fill="#334155", stroke="#334155")
            arrow.set("d", "M %g %g L %g %g L %g %g Z" % (tip[0], tip[1], base[0] - 3 * uy, base[1] + 3 * ux, base[0] + 3 * uy, base[1] - 3 * ux))
            if record["label"]:
                center = override.get("label_center") or self.readback.native_label_center(record, boxes)
                width, height = 44.0, 32.0
                label_group = ET.SubElement(group, "g")
                text_group = ET.SubElement(label_group, "g", {"font-size": "16px", "text-anchor": "middle"})
                ET.SubElement(text_group, "rect", x=str(center[0] - width / 2), y=str(center[1] - height / 2), width=str(width), height=str(height), fill="#ffffff")
                text = ET.SubElement(text_group, "text", x=str(center[0]), y=str(center[1] + 5))
                text.text = record["label"]
        for extra in (overrides or {}).get("_extra_cells", []):
            group = ET.SubElement(layer, "g", {"data-cell-id": extra["id"]})
            ET.SubElement(group, "rect", x=str(extra["x"]), y=str(extra["y"]), width="90", height="24", fill="#ffffff")
            text = ET.SubElement(group, "text", x=str(extra["x"] + 4), y=str(extra["y"] + 16))
            text.text = extra["text"]
        return self.write(native_path.parent, name + ".svg", ET.tostring(root, encoding="unicode"))

    def mutate(self, xml_text, mutate_fn):
        root = ET.fromstring(xml_text)
        mutate_fn(root)
        return ET.tostring(root, encoding="unicode")

    def run_readback(self, directory, source, semantics, svg=None, name="report.json"):
        output = directory / name
        command = [sys.executable, str(READBACK), "--source", str(source), "--semantics", str(semantics), "--output", str(output)]
        if svg is not None:
            command.extend(["--svg", str(svg)])
        result = subprocess.run(command, capture_output=True, text=True)
        report = json.loads(output.read_text(encoding="utf-8")) if output.exists() else None
        return result, report

    def test_positive_native_and_rendered(self):
        directory, native, semantics, _ = self.compile_case()
        result, report = self.run_readback(directory, native, semantics)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["overall"], "pass", report["semantic"]["differences"])
        self.assertEqual(report["counts"]["native"], {"elements": 4, "zones": 2, "relations": 3})
        self.assertEqual(report["visual"]["status"], "not_performed")
        svg = self.build_svg(native)
        result, report = self.run_readback(directory, native, semantics, svg=svg, name="report-svg.json")
        self.assertEqual(result.returncode, 0, (result.stderr, report["visual"]["issues"]))
        self.assertEqual(report["visual"]["status"], "pass", report["visual"])
        self.assertEqual(report["visual"]["checks"]["edges_checked"], 3)
        self.assertEqual(report["geometry_native"]["metrics"]["shared_segments"], [])

    def test_changed_cell_id_detected(self):
        directory, native, semantics, xml = self.compile_case()
        def rename(root):
            for cell in root.iter("mxCell"):
                if cell.get("id") == "b":
                    cell.set("id", "b-renamed")
                if cell.get("source") == "b":
                    cell.set("source", "b-renamed")
                if cell.get("target") == "b":
                    cell.set("target", "b-renamed")
        mutated = self.write(directory, "renamed.drawio", self.mutate(xml, rename))
        result, report = self.run_readback(directory, mutated, semantics, name="report.json")
        self.assertEqual(result.returncode, 1)
        codes = {(row["code"], row.get("id")) for row in report["semantic"]["differences"]}
        self.assertIn(("missing", "b"), codes)
        self.assertIn(("extra_element", "b-renamed"), codes)

    def test_changed_direction_and_endpoints_detected(self):
        directory, native, semantics, xml = self.compile_case()
        def swap(root):
            edge = root.find(".//mxCell[@id='r1']")
            edge.set("source", "b")
            edge.set("target", "a")
        mutated = self.write(directory, "reversed.drawio", self.mutate(xml, swap))
        result, report = self.run_readback(directory, mutated, semantics, name="report.json")
        self.assertEqual(result.returncode, 1)
        self.assertTrue(any(row["code"] == "endpoints_changed" and row["id"] == "r1" for row in report["semantic"]["differences"]))

    def test_changed_membership_detected(self):
        directory, native, semantics, xml = self.compile_case()
        def reparent(root):
            root.find(".//mxCell[@id='b']").set("parent", "1")
        mutated = self.write(directory, "reparented.drawio", self.mutate(xml, reparent))
        result, report = self.run_readback(directory, mutated, semantics, name="report.json")
        self.assertEqual(result.returncode, 1)
        self.assertTrue(any(row["code"] == "element_zone_changed" and row["id"] == "b" for row in report["semantic"]["differences"]))

    def test_changed_label_detected(self):
        directory, native, semantics, xml = self.compile_case()
        def relabel(root):
            root.find(".//mxCell[@id='r1']").set("value", "改名")
        mutated = self.write(directory, "relabelled.drawio", self.mutate(xml, relabel))
        result, report = self.run_readback(directory, mutated, semantics, name="report.json")
        self.assertEqual(result.returncode, 1)
        self.assertTrue(any(row["code"] == "label_changed" and row["id"] == "r1" for row in report["semantic"]["differences"]))

    def test_hidden_extra_legend_detected(self):
        directory, native, semantics, xml = self.compile_case()
        def add_legend(root):
            cells = root.find(".//root")
            legend = ET.SubElement(cells, "mxCell", id="legend", value="红=采集链路", vertex="1", parent="1", style="rounded=0;")
            ET.SubElement(legend, "mxGeometry", x="20", y="20", width="120", height="30", attrib={"as": "geometry"})
        mutated = self.write(directory, "legend.drawio", self.mutate(xml, add_legend))
        result, report = self.run_readback(directory, mutated, semantics, name="report.json")
        self.assertEqual(result.returncode, 1)
        rows = {(row["code"], row.get("id")) for row in report["semantic"]["differences"]}
        self.assertIn(("extra_element", "legend"), rows)
        self.assertIn(("extra_cell_text", "legend"), rows)
        self.assertEqual(report["semantic"]["extra_cells"][0]["label"], "红=采集链路")

    def test_shared_unrelated_segments_detected(self):
        directory, native, semantics, xml = self.compile_case()
        def stretch(root):
            edge = root.find(".//mxCell[@id='r3']")
            array = edge.find("mxGeometry/Array")
            array.clear()
            array.set("as", "points")
            ET.SubElement(array, "mxPoint", x="150", y="105")
            ET.SubElement(array, "mxPoint", x="370", y="105")
        mutated_xml = self.mutate(xml, stretch)
        mutated = self.write(directory, "shared.drawio", mutated_xml)
        svg = self.build_svg(mutated)
        result, report = self.run_readback(directory, mutated, semantics, svg=svg, name="report.json")
        native_pairs = report["geometry_native"]["metrics"]["shared_segments"]
        visual_pairs = report["visual"]["metrics"]["shared_segments"]
        self.assertTrue(any(set(row["ids"]) == {"r1", "r3"} for row in native_pairs), native_pairs)
        self.assertTrue(any(set(row["ids"]) == {"r1", "r3"} for row in visual_pairs), visual_pairs)
        self.assertGreater(report["geometry_native"]["metrics"]["collinear_length"], 0)
        self.assertEqual(result.returncode, 0, "shared segments are measured warnings, not hard semantic failures")

    def test_border_crossing_label_detected(self):
        directory, native, semantics, _ = self.compile_case()
        svg = self.build_svg(native, name="crossing", overrides={"r1": {"label_center": (300.0, 100.0)}})
        result, report = self.run_readback(directory, native, semantics, svg=svg, name="report.json")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["visual"]["status"], "fail")
        self.assertTrue(any(row["code"] == "label_crosses_zone_border" and row["id"] == "r1" for row in report["visual"]["issues"]), report["visual"]["issues"])

    def test_arrow_off_target_and_body_start_detected(self):
        directory, native, semantics, _ = self.compile_case()
        svg = self.build_svg(native, name="arrow", overrides={"r2": {"arrow_tip": (300.0, 420.0)}})
        result, report = self.run_readback(directory, native, semantics, svg=svg, name="report-arrow.json")
        self.assertEqual(result.returncode, 1)
        codes = {row["code"] for row in report["visual"]["issues"]}
        self.assertIn("arrow_tip_off_target", codes)
        svg = self.build_svg(native, name="start", overrides={"r2": {"points": [(160.0, 100.0), (200.0, 200.0), (200.0, 325.0)]}})
        result, report = self.run_readback(directory, native, semantics, svg=svg, name="report-start.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("edge_rendered_start_off", {row["code"] for row in report["visual"]["issues"]})

    def test_extra_svg_legend_detected(self):
        directory, native, semantics, _ = self.compile_case()
        svg = self.build_svg(native, name="extra", overrides={"_extra_cells": [{"id": "legend", "x": 480, "y": 400, "text": "红色=采集"}]})
        result, report = self.run_readback(directory, native, semantics, svg=svg, name="report.json")
        self.assertEqual(result.returncode, 1)
        codes = {row["code"] for row in report["visual"]["issues"]}
        self.assertIn("extra_svg_cell", codes)
        self.assertIn("extra_svg_legend_text", codes)

    def test_unsupported_and_interface(self):
        directory, native, semantics, xml = self.compile_case()
        compressed = self.write(directory, "compressed.drawio", xml.replace('<mxfile compressed="false">', '<mxfile compressed="true">', 1))
        result, report = self.run_readback(directory, compressed, semantics, name="report-compressed.json")
        self.assertEqual(result.returncode, 3)
        self.assertEqual(report["overall"], "unsupported")
        bare = self.write(directory, "bare.drawio", "<mxGraphModel><root/></mxGraphModel>")
        result, report = self.run_readback(directory, bare, semantics, name="report-bare.json")
        self.assertEqual(result.returncode, 3)
        for flag in ("--help", "--version"):
            result = subprocess.run([sys.executable, str(READBACK), flag], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
        result = subprocess.run([sys.executable, str(READBACK), "--source", str(native), "--semantics", str(semantics), "--output", str(directory / "r.json"), "--bogus"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        existing = self.write(directory, "exists.json", "{}")
        result = subprocess.run([sys.executable, str(READBACK), "--source", str(native), "--semantics", str(semantics), "--output", str(existing)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(existing.read_text(encoding="utf-8"), "{}")
        result = subprocess.run([sys.executable, str(READBACK), "--source", str(directory / "missing.drawio"), "--semantics", str(semantics), "--output", str(directory / "r2.json")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
