import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET


SCRIPT = Path(__file__).resolve().parents[1] / "architecture.py"


def fixture():
    return {
        "title": "三层架构 & 编辑源",
        "canvas": {"w": 1000, "h": 700},
        "fidelity_intent": "reproduction",
        "layout_policy": "optimize",
        "zones": [
            {"id": "outer", "label": "外层", "box": {"x": 20, "y": 20, "w": 960, "h": 660}},
            {"id": "middle", "label": "中层", "parent": "outer", "box": {"x": 50, "y": 80, "w": 600, "h": 540}},
            {"id": "deep", "label": "内层", "parent": "middle", "box": {"x": 80, "y": 140, "w": 520, "h": 400}},
            {"id": "other", "label": "侧区", "parent": "outer", "box": {"x": 700, "y": 80, "w": 230, "h": 540}},
        ],
        "elements": [
            {"id": "a", "label": "入口", "zone": "deep", "box": {"x": 110, "y": 220, "w": 100, "h": 60}},
            {"id": "obstacle", "label": "障碍", "zone": "deep", "box": {"x": 300, "y": 210, "w": 100, "h": 120}},
            {"id": "b", "label": "出口", "zone": "deep", "box": {"x": 450, "y": 220, "w": 110, "h": 60}},
            {"id": "c", "label": "消费者", "zone": "other", "box": {"x": 750, "y": 260, "w": 100, "h": 60}},
        ],
        "relations": [
            {"id": "ab", "from": "a", "to": "b", "label": "调用", "source_side": "right", "target_side": "left"},
            {"id": "ac", "from": "a", "to": "c", "source_side": "bottom", "target_side": "left"},
            {"id": "zones", "from": "deep", "to": "other", "source_side": "right", "target_side": "left"},
        ],
        "uncertain": ["未确认关系不编译为边"],
    }


class ArchitectureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("architecture", SCRIPT)
        cls.arch = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.arch)
        root = Path(os.environ["DRAW_DIAGRAM_TEST_OUTPUT"])
        if not root.is_dir():
            raise RuntimeError("DRAW_DIAGRAM_TEST_OUTPUT must be an existing directory")
        cls.output = Path(tempfile.mkdtemp(prefix="architecture-tests-", dir=str(root)))

    def setUp(self):
        self.data = fixture()

    def compiled(self):
        xml, report = self.arch.compile_diagram(self.data)
        self.assertEqual(report["status"], "pass", report)
        return xml

    def rejected_mutation(self, mutate, category):
        root = ET.fromstring(self.compiled())
        mutate(root)
        report = self.arch.validate_diagram(self.data, ET.tostring(root, encoding="unicode"))
        self.assertEqual(report["status"], "fail", report)
        self.assertTrue(report[category], report)

    def test_roundtrip_counts_and_native_cells(self):
        xml = self.compiled()
        report = self.arch.validate_diagram(self.data, xml)
        self.assertEqual(report["status"], "pass", report)
        self.assertEqual(report["counts"]["actual"], {"elements": 4, "zones": 4, "relations": 3})
        self.assertEqual(report["semantic_differences"], [])
        self.assertEqual(report["visual_validation"], "not_performed")
        self.assertNotIn("image=", xml)
        self.assertIn("source=\"deep\"", xml)

    def test_deterministic_and_order_independent(self):
        first = self.compiled()
        self.assertEqual(first, self.compiled())
        for key in ("zones", "elements", "relations"):
            self.data[key].reverse()
        self.assertEqual(first, self.compiled())

    def test_three_level_lca_and_relative_coordinates(self):
        root = ET.fromstring(self.compiled())
        self.assertEqual(root.find(".//mxCell[@id='ab']").get("parent"), "deep")
        self.assertEqual(root.find(".//mxCell[@id='ac']").get("parent"), "outer")
        self.assertEqual(root.find(".//mxCell[@id='zones']").get("parent"), "outer")
        g = root.find(".//mxCell[@id='a']/mxGeometry")
        self.assertEqual((float(g.get("x")), float(g.get("y"))), (30, 80))
        g = root.find(".//mxCell[@id='deep']/mxGeometry")
        self.assertEqual((float(g.get("x")), float(g.get("y"))), (30, 60))
        points = root.findall(".//mxCell[@id='ab']/mxGeometry/Array/mxPoint")
        self.assertGreaterEqual(len(points), 2)
        self.assertTrue(all(float(p.get("x")) < 520 for p in points))

    def test_deleted_edge(self):
        self.rejected_mutation(lambda r: r.find(".//root").remove(r.find(".//mxCell[@id='ab']")), "semantic_differences")

    def test_reversed_edge(self):
        def mutate(root):
            edge = root.find(".//mxCell[@id='ab']")
            edge.set("source", "b")
            edge.set("target", "a")
        self.rejected_mutation(mutate, "semantic_differences")

    def test_wrong_vertex_parent(self):
        self.rejected_mutation(lambda r: r.find(".//mxCell[@id='a']").set("parent", "middle"), "semantic_differences")

    def test_wrong_edge_parent(self):
        self.rejected_mutation(lambda r: r.find(".//mxCell[@id='ab']").set("parent", "1"), "semantic_differences")

    def test_through_box(self):
        def mutate(root):
            array = root.find(".//mxCell[@id='ab']/mxGeometry/Array")
            array.clear()
            array.set("as", "points")
            ET.SubElement(array, "mxPoint", x="160", y="110")
            ET.SubElement(array, "mxPoint", x="340", y="110")
        self.rejected_mutation(mutate, "geometry_errors")

    def test_nonorthogonal(self):
        self.rejected_mutation(lambda r: r.find(".//mxCell[@id='ab']/mxGeometry/Array/mxPoint").set("y", "111.7"), "geometry_errors")

    def test_moved_box(self):
        self.rejected_mutation(lambda r: r.find(".//mxCell[@id='a']/mxGeometry").set("x", "200"), "geometry_errors")

    def test_duplicate_xml_id(self):
        self.rejected_mutation(lambda r: r.find(".//root").append(copy.deepcopy(r.find(".//mxCell[@id='a']"))), "errors")

    def test_input_rejections(self):
        cases = []
        d = fixture(); d["relations"][0]["to"] = "missing"; cases.append(d)
        d = fixture(); d["zones"][0]["parent"] = "deep"; cases.append(d)
        d = fixture(); d["elements"][0]["id"] = "deep"; cases.append(d)
        d = fixture(); d["elements"][0]["box"]["x"] = float("nan"); cases.append(d)
        d = fixture(); d["style"] = {"unknown": 1}; cases.append(d)
        d = fixture(); d["elements"][0]["box"]["w"] = -1; cases.append(d)
        for data in cases:
            with self.subTest(data=data):
                xml, report = self.arch.compile_diagram(data)
                self.assertIsNone(xml)
                self.assertEqual(report["status"], "fail")

    def test_overlap_and_containment(self):
        for field, value in (("x", 300), ("y", 145), ("w", 1000)):
            d = fixture()
            d["elements"][0]["box"][field] = value
            xml, report = self.arch.compile_diagram(d)
            self.assertIsNone(xml)
            self.assertTrue(report["geometry_errors"], report)

    def test_no_solution_no_fallback(self):
        self.data["elements"][2]["box"] = {"x": 408, "y": 230, "w": 100, "h": 60}
        self.data["relations"] = [self.data["relations"][0]]
        xml, report = self.arch.compile_diagram(self.data)
        self.assertIsNone(xml)
        self.assertEqual(report["status"], "fail")
        self.assertTrue(report["errors"], report)

    def test_preserve_requires_explicit_route(self):
        self.data.pop("layout_policy")
        xml, report = self.arch.compile_diagram(self.data)
        self.assertIsNone(xml)
        self.assertEqual(report["status"], "fail")
        self.data["relations"] = []
        self.assertIsNotNone(self.compiled())

    def test_explicit_preserved_route_and_via(self):
        self.data["relations"] = [self.data["relations"][0]]
        self.data["relations"][0]["via"] = [{"x": 230, "y": 250}, {"x": 230, "y": 370}, {"x": 430, "y": 370}, {"x": 430, "y": 250}]
        self.data["layout_policy"] = "preserve"
        self.compiled()
        self.data["layout_policy"] = "optimize"
        self.compiled()
        self.data["relations"][0]["via"] = [{"x": 350, "y": 250}]
        xml, report = self.arch.compile_diagram(self.data)
        self.assertIsNone(xml)
        self.assertEqual(report["status"], "fail")

    def test_parallel_edges_get_distinct_ports(self):
        self.data["relations"] = [self.data["relations"][0]]
        extra = dict(self.data["relations"][0], id="ab2", label="另一关系")
        self.data["relations"].append(extra)
        root = ET.fromstring(self.compiled())
        styles = [root.find(".//mxCell[@id='%s']" % rid).get("style") for rid in ("ab", "ab2")]
        self.assertNotEqual(styles[0], styles[1])

    def test_crossing_and_collinear_metrics(self):
        report = self.arch.route_warnings({"a": [(0, 10), (20, 10)], "b": [(10, 0), (10, 20)], "c": [(5, 10), (15, 10)]}, 8)
        self.assertGreater(report["metrics"]["crossings"], 0)
        self.assertGreater(report["metrics"]["collinear_length"], 0)
        self.assertTrue(report["warnings"])

    def test_cli_compile_validate_and_no_overwrite(self):
        directory = Path(tempfile.mkdtemp(prefix="cli-", dir=str(self.output)))
        source = directory / "fixture.json"
        with source.open("x", encoding="utf-8") as handle:
            json.dump(self.data, handle, ensure_ascii=False)
        output = directory / "fixture.drawio"
        report = directory / "compile.json"
        result = subprocess.run([sys.executable, str(SCRIPT), "compile", "--input", str(source), "--output", str(output), "--report", str(report)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        original = output.read_bytes()
        validation = directory / "validate.json"
        result = subprocess.run([sys.executable, str(SCRIPT), "validate", "--input", str(source), "--diagram", str(output), "--report", str(validation)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(validation.read_text())["status"], "pass")
        for target in (source, output):
            result = subprocess.run([sys.executable, str(SCRIPT), "compile", "--input", str(source), "--output", str(target), "--report", str(directory / "never.json")], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
        self.assertEqual(original, output.read_bytes())
        self.assertFalse((directory / "never.json").exists())
        print("fixture:", output)

    def test_cli_help_version_and_unknown_option(self):
        for flag in ("--help", "--version"):
            result = subprocess.run([sys.executable, str(SCRIPT), flag], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
        result = subprocess.run([sys.executable, str(SCRIPT), "--not-an-option"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)

    def test_hidden_cell_and_changed_arrow_rejected(self):
        self.rejected_mutation(lambda r: r.find(".//mxCell[@id='a']").set("visible", "0"), "errors")
        def mutate(root):
            edge = root.find(".//mxCell[@id='ab']")
            edge.set("style", edge.get("style").replace("endArrow=classic", "endArrow=none"))
        self.rejected_mutation(mutate, "semantic_differences")

    def test_title_barrier_and_impossible_route(self):
        self.data = {
            "title": "Barrier", "canvas": {"w": 400, "h": 300},
            "fidelity_intent": "reproduction", "layout_policy": "optimize",
            "zones": [{"id": "z", "label": "Zone", "box": {"x": 0, "y": 0, "w": 400, "h": 300}}],
            "elements": [
                {"id": "a", "label": "A", "zone": "z", "box": {"x": 40, "y": 100, "w": 60, "h": 40}},
                {"id": "wall", "label": "Wall", "zone": "z", "box": {"x": 180, "y": 35, "w": 40, "h": 265}},
                {"id": "b", "label": "B", "zone": "z", "box": {"x": 300, "y": 100, "w": 60, "h": 40}},
            ],
            "relations": [{"id": "ab", "from": "a", "to": "b"}],
        }
        xml, report = self.arch.compile_diagram(self.data)
        self.assertIsNone(xml)
        self.assertIn("no safe orthogonal route", " ".join(report["errors"]))

    def test_title_crossing_readback(self):
        def mutate(root):
            array = root.find(".//mxCell[@id='ab']/mxGeometry/Array")
            array.clear()
            array.set("as", "points")
            for x, y in ((150, 110), (150, 10), (350, 10), (350, 110)):
                ET.SubElement(array, "mxPoint", x=str(x), y=str(y))
        self.rejected_mutation(mutate, "geometry_errors")

    def test_port_capacity_and_grid_budget(self):
        self.data["style"] = {"edgeSpacing": 100}
        self.data["relations"] = [self.data["relations"][0], dict(self.data["relations"][0], id="ab2")]
        xml, report = self.arch.compile_diagram(self.data)
        self.assertIsNone(xml)
        self.assertIn("port spacing", " ".join(report["errors"]))
        old = self.arch.MAX_GRID
        try:
            self.arch.MAX_GRID = 1
            xml, report = self.arch.compile_diagram(fixture())
            self.assertIsNone(xml)
            self.assertIn("grid budget", " ".join(report["errors"]))
        finally:
            self.arch.MAX_GRID = old

    def test_numeric_and_schema_fail_closed(self):
        cases = []
        d = fixture(); d["canvas"]["w"] = 10 ** 1000; cases.append(d)
        d = fixture(); d["uncertain"] = [float("inf")]; cases.append(d)
        d = fixture(); d["elements"][0]["box"]["w"] = True; cases.append(d)
        d = fixture(); d["zones"][0]["parent"] = "a"; cases.append(d)
        d = fixture(); d["relations"][0]["color"] = "none"; cases.append(d)
        d = fixture(); d["relations"][0]["from"] = "ab"; cases.append(d)
        for data in cases:
            with self.subTest(data=data):
                xml, report = self.arch.compile_diagram(data)
                self.assertIsNone(xml)
                self.assertTrue(report["errors"])

    def test_cli_invalid_paths_duplicate_keys_and_existing_report(self):
        directory = Path(tempfile.mkdtemp(prefix="invalid-cli-", dir=str(self.output)))
        source = directory / "source.json"
        with source.open("x", encoding="utf-8") as handle:
            json.dump(self.data, handle)
        source_bytes = source.read_bytes()
        result = subprocess.run([sys.executable, str(SCRIPT), "compile", "--input", str(source), "--output", str(directory / "not-created.drawio"), "--report", str(source)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(source_bytes, source.read_bytes())
        self.assertFalse((directory / "not-created.drawio").exists())
        for name, input_path, output_path in (
            ("missing-input", directory / "missing.json", directory / "missing.drawio"),
            ("missing-parent", source, directory / "absent" / "file.drawio"),
        ):
            result = subprocess.run([sys.executable, str(SCRIPT), "compile", "--input", str(input_path), "--output", str(output_path), "--report", str(directory / (name + ".json"))], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output_path.exists())
        with self.assertRaises(self.arch.DiagramError):
            json.loads('{"x":1,"x":2}', object_pairs_hook=self.arch.unique_object)

    def test_crossings_at_bends_and_shared_terminal(self):
        report = self.arch.route_warnings({"a": [(0, 10), (10, 10), (10, 20)], "b": [(10, 0), (10, 10), (20, 10)]}, 8)
        self.assertEqual(report["metrics"]["crossings"], 1)
        report = self.arch.route_warnings({"a": [(0, 0), (10, 0)], "b": [(0, 0), (0, 10)]}, 8)
        self.assertEqual(report["metrics"]["crossings"], 0)

    def test_zone_to_descendant(self):
        self.data["relations"] = [{"id": "container", "from": "deep", "to": "a", "source_side": "left", "target_side": "left"}]
        root = ET.fromstring(self.compiled())
        self.assertEqual(root.find(".//mxCell[@id='container']").get("parent"), "middle")

    def test_default_layer_lca(self):
        self.data["zones"] = [row for row in self.data["zones"] if row["id"] != "outer"]
        self.data["zones"][0].pop("parent")
        self.data["zones"][2].pop("parent")
        root = ET.fromstring(self.compiled())
        self.assertEqual(root.find(".//mxCell[@id='ac']").get("parent"), "1")
        self.assertEqual(root.find(".//mxCell[@id='ab']").get("parent"), "deep")

    def test_unknown_xml_visual_attributes(self):
        self.rejected_mutation(lambda r: r.find(".//mxGraphModel").set("backgroundImage", "unexpected"), "errors")
        self.rejected_mutation(lambda r: r.find(".//mxCell[@id='a']/mxGeometry").set("relative", "1"), "errors")
        self.rejected_mutation(lambda r: r.find(".//mxCell[@id='a']").set("value", "changed"), "semantic_differences")

    def test_label_style_geometry_and_jump_contract(self):
        root = ET.fromstring(self.compiled())
        edge = root.find(".//mxCell[@id='ab']")
        style = self.arch.parse_style(edge.get("style"))
        self.assertEqual(style["fontSize"], "16")
        self.assertEqual(style["horizontal"], "1")
        self.assertEqual(style["labelBackgroundColor"], "#ffffff")
        self.assertEqual(style["labelPadding"], "4")
        self.assertEqual(style["jumpStyle"], "arc")
        geometry = edge.find("mxGeometry")
        self.assertTrue(-1 <= float(geometry.get("x")) <= 1)
        self.assertEqual(geometry.get("y"), "0")
        self.assertIsNotNone(geometry.find("mxPoint[@as='offset']"))

    def test_label_auto_clear_and_deterministic(self):
        xml, report = self.arch.compile_diagram(self.data)
        self.assertEqual(report["label_placement"]["unresolved"], 0, report)
        label = report["label_placement"]["labels"]["ab"]
        self.assertEqual(label["issues"], [])
        self.assertEqual(label["orientation"], "horizontal")
        self.assertEqual(report, self.arch.compile_diagram(self.data)[1])
        self.assertEqual(self.arch.validate_diagram(self.data, xml)["semantic_differences"], [])

    def test_label_explicit_override_and_collision(self):
        _, report = self.arch.compile_diagram(self.data)
        label = report["label_placement"]["labels"]["ab"]
        self.data["relations"][0]["label_position"] = {"x": label["x"], "offset": dict(label["offset"])}
        self.compiled()
        self.data["relations"][0]["label_position"]["offset"]["x"] += 350 - label["center"][0]
        self.data["relations"][0]["label_position"]["offset"]["y"] += 260 - label["center"][1]
        xml, report = self.arch.compile_diagram(self.data)
        self.assertIsNone(xml)
        self.assertTrue(report["errors"] or report["geometry_errors"])
        self.data["relations"][0]["label_position"]["x"] = 2
        self.assertIsNone(self.arch.compile_diagram(self.data)[0])

    def test_label_changes_do_not_change_business_geometry(self):
        labelled = ET.fromstring(self.compiled())
        self.data["relations"][0]["label"] = ""
        plain = ET.fromstring(self.compiled())
        for ident in ("outer", "middle", "deep", "other", "a", "b", "c", "obstacle"):
            path = ".//mxCell[@id='%s']/mxGeometry" % ident
            self.assertEqual(ET.tostring(labelled.find(path)), ET.tostring(plain.find(path)))
        for ident in ("ab", "ac", "zones"):
            path = ".//mxCell[@id='%s']/mxGeometry/Array" % ident
            self.assertEqual(ET.tostring(labelled.find(path)), ET.tostring(plain.find(path)))

    def test_label_unresolved_retains_relation_and_warns(self):
        self.data["relations"][0]["label"] = "W" * 1000
        xml, report = self.arch.compile_diagram(self.data)
        self.assertIsNotNone(xml)
        self.assertEqual(report["label_placement"]["unresolved"], 1)
        self.assertTrue(any(w["code"] == "label_unresolved" for w in report["warnings"]))
        self.assertEqual(report["counts"]["actual"]["relations"], 3)

    def test_label_mutation_not_missing_edge(self):
        root = ET.fromstring(self.compiled())
        root.find(".//mxCell[@id='ab']/mxGeometry/mxPoint[@as='offset']").set("x", "5000")
        report = self.arch.validate_diagram(self.data, ET.tostring(root, encoding="unicode"))
        self.assertEqual(report["counts"]["actual"]["relations"], 3)
        self.assertEqual(report["semantic_differences"], [])
        self.assertGreater(report["label_placement"]["unresolved"], 0)

    def test_svg_label_compatibility_and_rotation(self):
        _, report = self.arch.compile_diagram(self.data)
        model = self.arch.Model(self.data)
        routes = self.arch.route_all(model, model.ports())
        svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg")
        translated = ET.SubElement(svg, "g", transform="translate(-8,-39)")
        for ident, row in model.elements.items():
            group = ET.SubElement(translated, "g", {"data-cell-id": ident})
            b = row["box"]
            ET.SubElement(group, "rect", x=str(b["x"]), y=str(b["y"]), width=str(b["w"]), height=str(b["h"]))
        label = report["label_placement"]["labels"]["ab"]
        group = ET.SubElement(translated, "g", {"data-cell-id": "ab", "font-size": "16px", "text-anchor": "middle"})
        b = label["bounds"]
        ET.SubElement(group, "rect", x=str(b[0]), y=str(b[1]), width=str(b[2] - b[0]), height=str(b[3] - b[1]), fill="#ffffff")
        node = ET.SubElement(group, "text", x=str(label["center"][0]), y=str(label["center"][1] + 5))
        node.text = "调用"
        rendered = self.arch.validate_rendered_labels(model, routes, report["label_placement"]["labels"], ET.tostring(svg, encoding="unicode"))
        self.assertEqual(rendered["status"], "pass", rendered)
        directory = Path(tempfile.mkdtemp(prefix="svg-check-", dir=str(self.output)))
        source, diagram, rendered_file, report_file = [directory / name for name in ("input.json", "diagram.drawio", "render.svg", "report.json")]
        with source.open("x", encoding="utf-8") as handle:
            json.dump(self.data, handle)
        with diagram.open("x", encoding="utf-8") as handle:
            handle.write(self.compiled())
        with rendered_file.open("x", encoding="utf-8") as handle:
            handle.write(ET.tostring(svg, encoding="unicode"))
        result = subprocess.run([sys.executable, str(SCRIPT), "validate", "--input", str(source), "--diagram", str(diagram), "--rendered-svg", str(rendered_file), "--report", str(report_file)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(report_file.read_text())["render_validation"]["status"], "pass")
        doctype = '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
        rendered = self.arch.validate_rendered_labels(model, routes, report["label_placement"]["labels"], doctype + ET.tostring(svg, encoding="unicode"))
        self.assertEqual(rendered["status"], "pass", rendered)
        rendered = self.arch.validate_rendered_labels(model, routes, report["label_placement"]["labels"], '<!DOCTYPE svg [<!ENTITY x "bad">]>' + ET.tostring(svg, encoding="unicode"))
        self.assertEqual(rendered["status"], "fail")
        group.set("font-size", "12px")
        rendered = self.arch.validate_rendered_labels(model, routes, report["label_placement"]["labels"], ET.tostring(svg, encoding="unicode"))
        self.assertEqual(rendered["status"], "fail")
        group.set("font-size", "16px")
        group.set("transform", "rotate(90)")
        rendered = self.arch.validate_rendered_labels(model, routes, report["label_placement"]["labels"], ET.tostring(svg, encoding="unicode"))
        self.assertEqual(rendered["status"], "fail")

    def test_proper_crossings_exclude_contacts_and_overlap(self):
        routes = {"a": [(0, 10), (20, 10)], "b": [(10, 0), (10, 20)], "c": [(0, 0), (0, 10)], "d": [(5, 10), (15, 10)]}
        crossings = self.arch.proper_crossings(routes)
        self.assertEqual([item["ids"] for item in crossings], [["a", "b"], ["b", "d"]])
        self.assertTrue(all(item["point"] == [10, 10] for item in crossings))

    def test_svg_missing_padding_or_displaced_background_rejected(self):
        _, report = self.arch.compile_diagram(self.data)
        model = self.arch.Model(self.data)
        routes = self.arch.route_all(model, model.ports())
        label = report["label_placement"]["labels"]["ab"]
        svg = ET.Element("svg")
        node = ET.SubElement(svg, "g", {"data-cell-id": "a"})
        ET.SubElement(node, "rect", x="110", y="220", width="100", height="60")
        group = ET.SubElement(svg, "g", {"data-cell-id": "ab", "font-size": "16px", "text-anchor": "middle"})
        node = ET.SubElement(group, "text", x=str(label["center"][0]), y=str(label["center"][1] + 5))
        node.text = "调用"
        background = ET.SubElement(group, "rect", x=str(label["bounds"][0]), y=str(label["center"][1] - 9), width="44", height="18", fill="#ffffff")
        rendered = self.arch.validate_rendered_labels(model, routes, report["label_placement"]["labels"], ET.tostring(svg, encoding="unicode"))
        self.assertEqual(rendered["status"], "fail")
        background.set("height", "32")
        background.set("x", "900")
        rendered = self.arch.validate_rendered_labels(model, routes, report["label_placement"]["labels"], ET.tostring(svg, encoding="unicode"))
        self.assertEqual(rendered["status"], "fail")
        background.set("x", str(label["bounds"][0]))
        background.set("y", str(label["bounds"][1]))
        node.set("y", "5000")
        rendered = self.arch.validate_rendered_labels(model, routes, report["label_placement"]["labels"], ET.tostring(svg, encoding="unicode"))
        self.assertEqual(rendered["status"], "fail")

    def test_xml_entities_and_malformed_rejected(self):
        for xml in ("<invalid>", '<!DOCTYPE a [<!ENTITY x "payload">]><mxfile/>'):
            report = self.arch.validate_diagram(self.data, xml)
            self.assertEqual(report["status"], "fail")
            self.assertTrue(report["errors"])

    def test_zone_border_crossing_rule(self):
        model = self.arch.Model(self.data)
        zone = model.boxes["other"]
        self.assertFalse(self.arch.crosses_border((720.0, 100.0, 760.0, 120.0), zone))
        self.assertFalse(self.arch.crosses_border((690.0, 100.0, 700.0, 120.0), zone))
        self.assertTrue(self.arch.crosses_border((690.0, 100.0, 720.0, 120.0), zone))
        self.assertIn("zone_border:other", self.arch.label_conflicts(model, (690.0, 100.0, 720.0, 120.0), {}, {}))

    def test_explicit_label_on_zone_border_rejected(self):
        row = self.data["relations"][1]
        row["label"] = "边界"
        _, report = self.arch.compile_diagram(self.data)
        self.assertEqual(report["status"], "pass", report)
        model = self.arch.Model(self.data)
        routes = self.arch.route_all(model, model.ports())
        record = self.arch.label_record(row, self.arch.simplify(routes["ac"]), {"x": 0, "offset": {"x": 0, "y": 0}})
        row["label_position"] = {"x": 0, "offset": {"x": 700 - record["center"][0], "y": 0}}
        xml, report = self.arch.compile_diagram(self.data)
        self.assertIsNone(xml)
        self.assertTrue(any("zone_border:other" in item for item in report["errors"]), report["errors"])

    def test_auto_labels_avoid_zone_borders(self):
        _, report = self.arch.compile_diagram(self.data)
        self.assertTrue(report["label_placement"]["labels"])
        for ident, record in report["label_placement"]["labels"].items():
            self.assertEqual([issue for issue in record["issues"] if issue.startswith("zone_border:")], [], (ident, record))

    def test_shared_segment_metric_and_pair_detection(self):
        routes = {"p": [(0.0, 10.0), (40.0, 10.0)], "q": [(10.0, 10.0), (30.0, 10.0)], "r": [(10.0, 20.0), (30.0, 20.0)]}
        report = self.arch.route_warnings(routes, 10)
        self.assertGreater(report["metrics"]["collinear_length"], 0)
        self.assertTrue(any(row["ids"] == ["p", "q"] and row["collinear_length"] > 0 for row in report["warnings"]))

    def test_shared_segment_pairs_skip_shared_terminals(self):
        model = self.arch.Model(self.data)
        disjoint = {"ab": [(0.0, 0.0), (100.0, 0.0)], "zones": [(20.0, 0.0), (80.0, 0.0)]}
        self.assertEqual([pair[:2] for pair in self.arch.shared_segment_pairs(model, disjoint)], [("ab", "zones")])
        model.relations["zones"]["from"] = "a"
        self.assertEqual(self.arch.shared_segment_pairs(model, disjoint), [])

    def test_repair_accepts_only_strictly_better_routes(self):
        model = self.arch.Model(self.data)
        base = {"ab": [(0.0, 0.0), (100.0, 0.0)], "zones": [(20.0, 0.0), (80.0, 0.0)]}
        original = self.arch.route_relation
        try:
            calls = []
            def better(model_arg, ident, ports, occupied, overlap_scale=1.0):
                calls.append((ident, overlap_scale))
                return [(20.0, 12.0), (80.0, 12.0)]
            self.arch.route_relation = better
            repaired = self.arch.repair_shared_segments(model, {key: list(value) for key, value in base.items()})
            self.assertEqual(repaired["zones"], [(20.0, 12.0), (80.0, 12.0)])
            self.assertEqual(repaired["ab"], base["ab"])
            self.assertEqual(calls[0], ("zones", 8.0))
            self.assertEqual(self.arch.shared_segment_pairs(model, repaired), [])
            self.arch.route_relation = lambda model_arg, ident, ports, occupied, overlap_scale=1.0: [(20.0, 4.0), (80.0, 4.0)]
            unchanged = self.arch.repair_shared_segments(model, {key: list(value) for key, value in base.items()})
            self.assertEqual(unchanged["zones"], base["zones"])
            self.arch.route_relation = lambda model_arg, ident, ports, occupied, overlap_scale=1.0: [(20.0, 0.0), (20.0, -10.0), (80.0, -10.0)]
            traded = self.arch.repair_shared_segments(model, {key: list(value) for key, value in base.items()})
            self.assertEqual(traded["zones"], [(20.0, 0.0), (20.0, -10.0), (80.0, -10.0)])
        finally:
            self.arch.route_relation = original

    def test_compiled_plan_has_no_shared_segments_or_border_labels(self):
        xml, report = self.arch.compile_diagram(self.data)
        self.assertIsNotNone(xml)
        self.assertEqual(report["status"], "pass", report)
        self.assertEqual(report["metrics"]["collinear_length"], 0)
        for ident, record in report["label_placement"]["labels"].items():
            self.assertFalse([issue for issue in record["issues"] if issue.startswith("zone_border:")], (ident, record))
