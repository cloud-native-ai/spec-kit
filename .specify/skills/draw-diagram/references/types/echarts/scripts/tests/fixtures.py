"""Generic synthetic fixtures for the ECharts readback/normalizer tests.

The topology is intentionally small and generic (two root zones, one nested zone,
four elements with a duplicate label, three relations including one container
endpoint). No private business graph, counts or absolute paths are encoded.
"""

from __future__ import annotations

import copy
import json
import math


def semantics():
    return {
        "title": "Synthetic topology",
        "elements": [
            {"id": "a1", "label": "Alpha", "zone": "zA"},
            {"id": "a2", "label": "Beta", "zone": "zA"},
            {"id": "b1", "label": "Gamma", "zone": "zB"},
            {"id": "b2", "label": "Beta", "zone": "zB"},
        ],
        "zones": [
            {"id": "zA", "label": "Zone A", "parent": None},
            {"id": "zB", "label": "Zone B", "parent": None},
            {"id": "zC", "label": "Zone C", "parent": "zB"},
        ],
        "relations": [
            {"id": "r1", "from": "a1", "to": "a2", "color": "#aa0000"},
            {"id": "r2", "from": "a2", "to": "b1", "label": "calls", "color": "#00aa00"},
            {"id": "r3", "from": "b1", "to": "zC", "color": "#0000aa"},
        ],
        "counts": {"elements": 4, "zones": 3, "relations": 3},
    }


ZONE_RECTS = {
    "zA": [20, 20, 280, 180],
    "zB": [320, 20, 580, 380],
    "zC": [340, 220, 560, 360],
}

NODES = [
    {"id": "a1", "name": "Alpha", "category": 0, "x": 90, "y": 70, "w": 60, "h": 30},
    {"id": "a2", "name": "Beta", "category": 0, "x": 210, "y": 70, "w": 60, "h": 30},
    {"id": "b1", "name": "Gamma", "category": 1, "x": 450, "y": 80, "w": 70, "h": 30},
    {"id": "b2", "name": "Beta", "category": 1, "x": 450, "y": 160, "w": 70, "h": 30},
]

ARROWS = {
    "r1": {"center": [172, 70], "rotate": -90, "color": "#aa0000", "coords": [[120, 70], [170, 70]]},
    "r2": {"center": [450, 103], "rotate": 0, "color": "#00aa00", "coords": [[210, 85], [210, 110], [450, 110], [450, 105]]},
    "r3": {"center": [520, 272], "rotate": 180, "color": "#0000aa", "coords": [[485, 80], [520, 80], [520, 270]]},
}

LABELS = {"r2": {"text": "calls", "point": [330, 110]}}

ARROW_SYMBOL = "path://M0,-10 L6,6 L0,2 L-6,6 Z"


def option():
    categories = []
    for index, zone in enumerate(semantics()["zones"]):
        categories.append({
            "name": zone["label"],
            "zoneId": zone["id"],
            "zoneLabel": zone["label"],
            "parent": zone["parent"],
            "itemStyle": {"color": "#eeeeee", "borderColor": "#999999", "borderWidth": 1},
        })
    data = []
    for node in NODES:
        data.append({
            "id": node["id"],
            "name": node["name"],
            "kind": "component",
            "x": node["x"],
            "y": node["y"],
            "symbol": "roundRect",
            "symbolSize": [node["w"], node["h"]],
            "category": node["category"],
            "itemStyle": {"color": "#eeeeee", "borderColor": "#999999", "borderWidth": 2},
            "label": {"show": True, "position": "inside"},
        })
    data.append({
        "id": "zC",
        "name": "Zone C",
        "kind": "container-endpoint",
        "x": 520,
        "y": 280,
        "symbolSize": 1,
        "category": 2,
        "itemStyle": {"opacity": 0},
        "label": {"show": False},
        "silent": True,
        "zoneId": "zC",
    })
    for x, y, anchor_id in ((0, 0, "__anchor_tl"), (600, 0, "__anchor_tr"), (0, 400, "__anchor_bl"), (600, 400, "__anchor_br")):
        data.append({
            "id": anchor_id,
            "name": anchor_id,
            "kind": "layout-anchor",
            "x": x,
            "y": y,
            "symbolSize": 0,
            "itemStyle": {"opacity": 0},
            "label": {"show": False},
            "silent": True,
        })
    links = []
    for relation in semantics()["relations"]:
        link = {"source": relation["from"], "target": relation["to"], "semanticId": relation["id"]}
        if relation.get("label"):
            link["name"] = relation["label"]
            link["semanticLabel"] = relation["label"]
        links.append(link)
    graphic = []
    for zone in semantics()["zones"]:
        x1, y1, x2, y2 = ZONE_RECTS[zone["id"]]
        graphic.append({
            "id": f"zone-rect-{zone['id']}",
            "type": "rect",
            "left": x1,
            "top": y1,
            "shape": {"width": x2 - x1, "height": y2 - y1},
        })
        graphic.append({"id": f"zone-title-{zone['id']}", "type": "text", "style": {"text": zone["label"]}})
    return {
        "meta": {"canvasWidth": 600, "canvasHeight": 400},
        "legend": {"show": True, "data": [zone["label"] for zone in semantics()["zones"]]},
        "graphic": graphic,
        "series": [
            {
                "id": "components",
                "type": "graph",
                "layout": "none",
                "zoom": 1,
                "nodeScaleRatio": 0,
                "categories": categories,
                "data": data,
                "links": links,
            },
            {
                "id": "edge-lines",
                "type": "lines",
                "polyline": True,
                "data": [
                    {
                        "name": f"{rel['from']} -> {rel['to']}",
                        "coords": ARROWS[rel["id"]]["coords"],
                        "lineStyle": {"color": ARROWS[rel["id"]]["color"], "width": 1.6},
                        "srcId": rel["from"],
                        "dstId": rel["to"],
                        "semanticId": rel["id"],
                    }
                    for rel in semantics()["relations"]
                ],
            },
            {
                "id": "edge-arrows",
                "type": "scatter",
                "symbol": ARROW_SYMBOL,
                "symbolSize": [12, 16],
                "data": [
                    {
                        "value": ARROWS[rel["id"]]["center"],
                        "symbolRotate": ARROWS[rel["id"]]["rotate"],
                        "itemStyle": {"color": ARROWS[rel["id"]]["color"]},
                        "srcId": rel["from"],
                        "dstId": rel["to"],
                        "semanticId": rel["id"],
                    }
                    for rel in semantics()["relations"]
                ],
            },
            {
                "id": "edge-labels",
                "type": "scatter",
                "symbolSize": 1,
                "label": {"show": True, "formatter": "{b}"},
                "data": [
                    {
                        "value": LABELS[rel["id"]]["point"],
                        "name": LABELS[rel["id"]]["text"],
                        "srcId": rel["from"],
                        "dstId": rel["to"],
                        "semanticId": rel["id"],
                    }
                    for rel in semantics()["relations"]
                    if rel["id"] in LABELS
                ],
            },
        ],
    }


def mutate_option(fn):
    data = copy.deepcopy(option())
    fn(data)
    return data


def served_html(option_data):
    payload = json.dumps(option_data, ensure_ascii=False)
    return (
        "<!DOCTYPE html><html><head><title>synthetic</title></head><body>"
        "<div id=\"chart\"></div><script>\n"
        f"var OPTION = {payload};\n"
        "(function boot() { var chart = echarts.init(document.getElementById('chart'));"
        " chart.setOption(OPTION); })();\n"
        "</script></body></html>\n"
    )


def _matrix(center, rotate, sx=6.0, sy=8.0):
    theta = math.radians(-rotate)
    cos_t, sin_t = math.cos(theta), math.sin(theta)
    a = sx * cos_t
    b = sx * sin_t
    c = -sy * sin_t
    d = sy * cos_t
    return f"matrix({_fmt(a)},{_fmt(b)},{_fmt(c)},{_fmt(d)},{_fmt(center[0])},{_fmt(center[1])})"


def _fmt(value):
    return f"{value:.6f}".rstrip("0").rstrip(".") if isinstance(value, float) else str(value)


def svg(option_data=None):
    data = option_data or option()
    sem = semantics()
    texts = []
    for zone in sem["zones"]:
        texts.append(zone["label"])
    for node in NODES:
        texts.append(node["name"])
    for label in LABELS.values():
        texts.append(label["text"])
    for zone in sem["zones"]:
        texts.append(zone["label"])
    arrow_paths = []
    arrows_series = next(s for s in data["series"] if s["id"] == "edge-arrows")
    for item in arrows_series["data"]:
        arrow_paths.append(
            f'<path d="M0 -1L1 1L0 0.5L-1 1Z" transform="{_matrix(item["value"], item["symbolRotate"])}" '
            f'fill="{item["itemStyle"]["color"]}"></path>'
        )
    text_nodes = "".join(f"<text>{text}</text>" for text in texts)
    return (
        '<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">'
        f'<g>{text_nodes}</g><g>{"".join(arrow_paths)}</g></svg>\n'
    )


def svg_with_arrow_mutated(semantic_id, rotate):
    data = option()
    arrows_series = next(s for s in data["series"] if s["id"] == "edge-arrows")
    for item in arrows_series["data"]:
        if item["semanticId"] == semantic_id:
            item["symbolRotate"] = rotate
    return svg(data)


def svg_without_label(text):
    content = svg()
    return content.replace(f"<text>{text}</text>", "", 1)
