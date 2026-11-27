/* ============================================================
   d3js viewer — data join over the frozen SDS data block above.
   Absolute coordinates; no force simulation; no network calls.
   Identity contract: node-<id>/zone-<id>/edge-<id> ids plus
   data-node-id/data-zone-id/data-edge-id attributes.
   ============================================================ */
(function () {
  const data = SDS;
  const W = data.canvas.w, H = data.canvas.h;
  const TOP_FILL = data.zoneFill || {};

  const parentOf = new Map(data.zones.map(function (z) { return [z.id, z.parent]; }));
  const zoneLabel = new Map(data.zones.map(function (z) { return [z.id, z.label]; }));
  const elemLabel = new Map(data.elements.map(function (e) { return [e.id, e.label]; }));
  const elemZone = new Map(data.elements.map(function (e) { return [e.id, e.zone]; }));
  const relById = new Map(data.relations.map(function (r) { return [r.id, r]; }));

  function topOf(zid) {
    let cur = zid;
    while (parentOf.get(cur)) cur = parentOf.get(cur);
    return cur;
  }
  function nameOf(id) {
    return elemLabel.get(id) || ('分区 ' + zoneLabel.get(id));
  }

  const clean = new URLSearchParams(location.search).get('clean') === '1';
  if (clean) document.body.classList.add('clean');

  const svg = d3.select('#chart').append('svg')
    .attr('id', 'arch-svg')
    .attr('xmlns', 'http://www.w3.org/2000/svg')
    .attr('viewBox', '0 0 ' + W + ' ' + H)
    .attr('width', W)
    .attr('height', H)
    .attr('role', 'img')
    .attr('aria-label', data.title + '：' + data.elements.length + ' 个组件、'
      + data.zones.length + ' 个分区、' + data.relations.length + ' 条关系');

  svg.append('rect').attr('id', 'canvas-bg')
    .attr('x', 0).attr('y', 0).attr('width', W).attr('height', H).attr('fill', '#ffffff');

  const defs = svg.append('defs');
  const COLORS = Array.from(new Set(data.relations.map(function (r) { return r.color; })));
  COLORS.forEach(function (color, i) {
    defs.append('marker')
      .attr('id', 'arrow-' + i)
      .attr('viewBox', '0 0 10 10')
      .attr('refX', 8.8).attr('refY', 5)
      .attr('markerWidth', 6.5).attr('markerHeight', 6.5)
      .attr('orient', 'auto').attr('markerUnits', 'strokeWidth')
      .append('path').attr('d', 'M0,0.7 L10,5 L0,9.3 z').attr('fill', color);
  });
  const colorIndex = new Map(COLORS.map(function (c, i) { return [c, i]; }));

  const root = svg.append('g').attr('id', 'zoom-root');
  const gZones = root.append('g').attr('id', 'layer-zones');
  const gEdges = root.append('g').attr('id', 'layer-edges');
  const gPorts = root.append('g').attr('id', 'layer-ports');
  const gNodes = root.append('g').attr('id', 'layer-nodes');
  const gLabels = root.append('g').attr('id', 'layer-edge-labels');
  const gLegend = root.append('g').attr('id', 'layer-legend');

  /* ---------- zones (top-level first, nested on top) ---------- */
  const zonesSorted = data.zones.slice().sort(function (a, b) {
    return a.depth - b.depth || a.id.localeCompare(b.id);
  });
  const zoneSel = gZones.selectAll('g.zone')
    .data(zonesSorted, function (d) { return d.id; })
    .join('g')
    .attr('class', function (d) { return 'zone zone-depth-' + d.depth; })
    .attr('id', function (d) { return 'zone-' + d.id; })
    .attr('data-zone-id', function (d) { return d.id; })
    .attr('data-zone-label', function (d) { return d.label; })
    .attr('data-parent', function (d) { return d.parent || ''; });

  zoneSel.append('rect')
    .attr('class', 'zone-box')
    .attr('x', function (d) { return d.box.x; })
    .attr('y', function (d) { return d.box.y; })
    .attr('width', function (d) { return d.box.w; })
    .attr('height', function (d) { return d.box.h; })
    .attr('rx', function (d) { return d.depth === 0 ? 14 : 10; })
    .attr('fill', function (d) {
      return d.depth === 0 ? (TOP_FILL[topOf(d.id)] || '#f8fafc') : 'rgba(255,255,255,0.74)';
    })
    .attr('stroke', function (d) { return ['#37474f', '#607d8b', '#607d8b'][Math.min(d.depth, 2)]; })
    .attr('stroke-width', function (d) { return [2.5, 2.0, 2.0][Math.min(d.depth, 2)]; })
    .attr('data-tier', function (d) { return d.depth === 0 ? 'T1' : 'T2'; });

  zoneSel.append('text')
    .attr('class', 'zone-label')
    .attr('x', function (d) { return d.box.x + 16; })
    .attr('y', function (d) { return d.box.y + (d.depth === 0 ? 34 : 30); })
    .text(function (d) { return d.label; });

  /* ---------- nodes ---------- */
  const nodeSel = gNodes.selectAll('g.node')
    .data(data.elements, function (d) { return d.id; })
    .join('g')
    .attr('class', 'node')
    .attr('id', function (d) { return 'node-' + d.id; })
    .attr('data-node-id', function (d) { return d.id; })
    .attr('data-zone', function (d) { return d.zone; })
    .attr('transform', function (d) { return 'translate(' + d.box.x + ',' + d.box.y + ')'; });

  nodeSel.append('rect')
    .attr('class', 'node-box')
    .attr('width', function (d) { return d.box.w; })
    .attr('height', function (d) { return d.box.h; })
    .attr('rx', 9)
    .attr('data-tier', 'T2');

  nodeSel.append('text')
    .attr('class', 'node-label')
    .attr('x', function (d) { return d.box.w / 2; })
    .attr('y', function (d) { return d.box.h / 2 + 1; })
    .attr('text-anchor', 'middle')
    .attr('dominant-baseline', 'central')
    .text(function (d) { return d.label; });

  nodeSel.append('title').text(function (d) {
    return d.label + '（分区：' + zoneLabel.get(d.zone) + '）';
  });

  /* ---------- edges ---------- */
  function roundedPath(points, radius) {
    const r = radius || 8;
    if (!points || points.length < 2) return '';
    let d = 'M' + points[0].x + ',' + points[0].y;
    for (let i = 1; i < points.length - 1; i++) {
      const p0 = points[i - 1], p1 = points[i], p2 = points[i + 1];
      const l1 = Math.abs(p1.x - p0.x) + Math.abs(p1.y - p0.y);
      const l2 = Math.abs(p2.x - p1.x) + Math.abs(p2.y - p1.y);
      const rr = Math.min(r, l1 / 2, l2 / 2);
      const ax = p1.x - Math.sign(p1.x - p0.x) * rr;
      const ay = p1.y - Math.sign(p1.y - p0.y) * rr;
      const bx = p1.x + Math.sign(p2.x - p1.x) * rr;
      const by = p1.y + Math.sign(p2.y - p1.y) * rr;
      d += ' L' + ax + ',' + ay + ' Q' + p1.x + ',' + p1.y + ' ' + bx + ',' + by;
    }
    const last = points[points.length - 1];
    d += ' L' + last.x + ',' + last.y;
    return d;
  }

  function longestSegment(points) {
    let best = null;
    for (let i = 0; i < points.length - 1; i++) {
      const a = points[i], b = points[i + 1];
      const len = Math.abs(a.x - b.x) + Math.abs(a.y - b.y);
      if (!best || len > best.len) best = { len: len, a: a, b: b };
    }
    return best;
  }

  const edgeSel = gEdges.selectAll('g.edge')
    .data(data.relations, function (d) { return d.id; })
    .join('g')
    .attr('class', 'edge')
    .attr('id', function (d) { return 'edge-' + d.id; })
    .attr('data-edge-id', function (d) { return d.id; })
    .attr('data-from', function (d) { return d.from; })
    .attr('data-to', function (d) { return d.to; })
    .attr('data-color', function (d) { return d.color; });

  edgeSel.append('path')
    .attr('class', 'edge-line')
    .attr('data-role', 'line')
    .attr('d', function (d) { return roundedPath(d.route); })
    .attr('stroke', function (d) { return d.color; })
    .attr('marker-end', function (d) { return 'url(#arrow-' + colorIndex.get(d.color) + ')'; });

  edgeSel.append('path')
    .attr('class', 'edge-hit')
    .attr('data-role', 'hit')
    .attr('d', function (d) { return roundedPath(d.route); });

  edgeSel.append('title').text(function (d) {
    return d.id + '：' + nameOf(d.from) + ' → ' + nameOf(d.to) + (d.label ? '（' + d.label + '）' : '');
  });

  /* ---------- edge id labels (toggle) ---------- */
  const idLabelSel = gLabels.selectAll('text.edge-id-label')
    .data(data.relations, function (d) { return d.id; })
    .join('text')
    .attr('class', 'edge-id-label')
    .attr('data-edge-id', function (d) { return d.id; })
    .attr('text-anchor', 'middle')
    .each(function (d) {
      const seg = longestSegment(d.route);
      const mx = (seg.a.x + seg.b.x) / 2;
      const my = (seg.a.y + seg.b.y) / 2;
      const horizontal = seg.a.y === seg.b.y;
      d3.select(this)
        .attr('x', mx + (horizontal ? 0 : 14))
        .attr('y', my + (horizontal ? -6 : 4));
    })
    .text(function (d) { return d.id; });

  /* ---------- semantic edge labels (always visible) ---------- */
  const semLabelSel = gLabels.selectAll('text.edge-label')
    .data(data.relations.filter(function (r) { return !!r.label; }), function (d) { return d.id; })
    .join('text')
    .attr('class', 'edge-label')
    .attr('data-edge-id', function (d) { return d.id; })
    .attr('data-role', 'label')
    .attr('text-anchor', 'middle')
    .attr('x', function (d) { return d.labelPos.x; })
    .attr('y', function (d) { return d.labelPos.y; })
    .text(function (d) { return d.label; });

  /* ---------- ports (presentation only; not business elements) ---------- */
  gPorts.selectAll('circle.port')
    .data(data.ports || [])
    .join('circle')
    .attr('class', 'port')
    .attr('data-role', 'port')
    .attr('data-edge-id', function (d) { return d.edge; })
    .attr('cx', function (d) { return d.x; })
    .attr('cy', function (d) { return d.y; })
    .attr('r', 2.6)
    .attr('fill', '#ffffff')
    .attr('stroke', function (d) {
      const rel = relById.get(d.edge);
      return rel ? rel.color : '#64748b';
    });

  /* ---------- legend (declared rows; style/interaction notes only) ---------- */
  const L = data.legend;
  const legend = gLegend.append('g')
    .attr('id', 'legend-panel').attr('class', 'legend').attr('data-legend', '1');
  legend.append('rect')
    .attr('class', 'legend-box')
    .attr('x', L.x).attr('y', L.y).attr('width', L.w).attr('height', L.h).attr('rx', 10);
  legend.append('text')
    .attr('class', 'legend-title')
    .attr('x', L.x + 16).attr('y', L.y + 28)
    .text('图例');
  const items = [
    { kind: 'line', w: 2.5, color: '#37474f', text: '顶层分区边界 2.5px' },
    { kind: 'line', w: 2.0, color: '#607d8b', text: '嵌套分区 / 组件边界 2.0px' },
    { kind: 'line', w: 1.6, color: '#334155', text: '关系连线 1.6px，箭头指向终点' },
    { kind: 'port', text: '端口点：关系跨分区边界处' },
    { kind: 'text', text: '工具栏：常显编号 / 导出 / 复位' },
    { kind: 'text', text: '悬停高亮关联，点击固定选中' }
  ];
  items.forEach(function (item, i) {
    const y = L.y + 58 + i * 28;
    const row = legend.append('g')
      .attr('class', 'legend-item')
      .attr('data-legend-kind', item.kind === 'port' || item.kind === 'text' ? 'interaction' : 'style');
    if (item.color) row.attr('data-swatch-color', item.color);
    if (item.kind === 'line') {
      row.append('line')
        .attr('x1', L.x + 16).attr('y1', y - 4).attr('x2', L.x + 46).attr('y2', y - 4)
        .attr('stroke', item.color).attr('stroke-width', item.w);
    } else if (item.kind === 'port') {
      row.append('circle')
        .attr('cx', L.x + 31).attr('cy', y - 4).attr('r', 2.6)
        .attr('fill', '#ffffff').attr('stroke', '#64748b').attr('stroke-width', 1.3);
    }
    row.append('text')
      .attr('class', 'legend-text')
      .attr('x', L.x + 56).attr('y', y)
      .text(item.text);
  });

  /* ---------- interaction: hover / click / zoom ---------- */
  const tip = document.getElementById('arch-tooltip');
  const state = { hover: null, pinned: null };

  function incidentEdges(id) {
    return data.relations.filter(function (r) { return r.from === id || r.to === id; });
  }
  function tipForNode(d) {
    const edges = incidentEdges(d.id);
    const lines = [d.label, '分区：' + zoneLabel.get(d.zone)];
    if (edges.length) {
      edges.slice(0, 8).forEach(function (r) {
        lines.push(r.id + ' ' + (r.from === d.id ? '→ ' + nameOf(r.to) : '← ' + nameOf(r.from)));
      });
    } else {
      lines.push('当前描述中没有与其他组件的连线');
    }
    return lines.join('\n');
  }
  function tipForEdge(d) {
    const lines = [d.id + ' ' + nameOf(d.from) + ' → ' + nameOf(d.to)];
    if (d.label) lines.push(d.label);
    return lines.join('\n');
  }
  function moveTip(ev) {
    if (!tip) return;
    const pad = 16;
    const tw = tip.offsetWidth || 260;
    const th = tip.offsetHeight || 80;
    let x = ev.clientX + pad, y = ev.clientY + pad;
    if (x + tw > window.innerWidth - 8) x = ev.clientX - tw - pad;
    if (y + th > window.innerHeight - 8) y = ev.clientY - th - pad;
    tip.style.left = Math.max(8, x) + 'px';
    tip.style.top = Math.max(8, y) + 'px';
  }
  function showTip(text, ev) {
    if (!tip) return;
    tip.textContent = text;
    tip.classList.add('visible');
    moveTip(ev);
  }
  function hideTip() { if (tip) tip.classList.remove('visible'); }

  function applyHighlight() {
    const active = state.pinned || state.hover;
    let nodeSet = null, edgeSet = null, zoneSet = null;
    if (active) {
      if (active.type === 'node') {
        nodeSet = new Set([active.id]);
        edgeSet = new Set();
        incidentEdges(active.id).forEach(function (r) {
          edgeSet.add(r.id);
          nodeSet.add(r.from);
          nodeSet.add(r.to);
        });
        zoneSet = new Set([elemZone.get(active.id) || active.id]);
      } else {
        const r = relById.get(active.id);
        edgeSet = new Set([active.id]);
        nodeSet = new Set([r.from, r.to]);
        zoneSet = new Set();
      }
    }
    nodeSel
      .classed('hl', function (d) { return !!nodeSet && nodeSet.has(d.id); })
      .classed('dim', function (d) { return !!active && !(nodeSet && nodeSet.has(d.id)); });
    edgeSel
      .classed('hl', function (d) { return !!edgeSet && edgeSet.has(d.id); })
      .classed('dim', function (d) { return !!active && !(edgeSet && edgeSet.has(d.id)); });
    zoneSel
      .classed('hl', function (d) { return !!zoneSet && zoneSet.has(d.id); })
      .classed('dim', function (d) { return !!active && !(zoneSet && zoneSet.has(d.id)) && d.depth === 0; });
  }

  nodeSel
    .on('mouseenter', function (ev, d) {
      state.hover = { type: 'node', id: d.id };
      applyHighlight();
      showTip(tipForNode(d), ev);
    })
    .on('mousemove', function (ev) { moveTip(ev); })
    .on('mouseleave', function () {
      state.hover = null;
      applyHighlight();
      hideTip();
    })
    .on('click', function (ev, d) {
      ev.stopPropagation();
      state.pinned = (state.pinned && state.pinned.type === 'node' && state.pinned.id === d.id)
        ? null : { type: 'node', id: d.id };
      applyHighlight();
    });

  edgeSel
    .on('mouseenter', function (ev, d) {
      state.hover = { type: 'edge', id: d.id };
      applyHighlight();
      showTip(tipForEdge(d), ev);
    })
    .on('mousemove', function (ev) { moveTip(ev); })
    .on('mouseleave', function () {
      state.hover = null;
      applyHighlight();
      hideTip();
    })
    .on('click', function (ev, d) {
      ev.stopPropagation();
      state.pinned = (state.pinned && state.pinned.type === 'edge' && state.pinned.id === d.id)
        ? null : { type: 'edge', id: d.id };
      applyHighlight();
    });

  const zoom = d3.zoom()
    .scaleExtent([0.35, 5])
    .on('zoom', function (ev) { root.attr('transform', ev.transform); });
  svg.call(zoom).on('dblclick.zoom', null);
  svg.on('click', function () {
    state.pinned = null;
    applyHighlight();
  });

  function btn(id, handler) {
    const el = document.getElementById(id);
    if (el) el.addEventListener('click', handler);
  }
  btn('btn-zoom-in', function () { svg.transition().duration(180).call(zoom.scaleBy, 1.3); });
  btn('btn-zoom-out', function () { svg.transition().duration(180).call(zoom.scaleBy, 1 / 1.3); });
  btn('btn-zoom-reset', function () {
    svg.transition().duration(220).call(zoom.transform, d3.zoomIdentity);
  });
  btn('toggle-ids', function (ev) {
    const on = !!ev.target.checked;
    document.body.classList.toggle('show-edge-ids', on);
  });

  /* ---------- export (real page capability) ---------- */
  function chartCssText() {
    const node = document.getElementById('chart-css');
    return node ? node.textContent : '';
  }
  function serializeSVG() {
    const el = document.getElementById('arch-svg');
    const clone = el.cloneNode(true);
    clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    clone.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink');
    clone.querySelectorAll('.dim').forEach(function (x) { x.classList.remove('dim'); });
    clone.querySelectorAll('.hl').forEach(function (x) { x.classList.remove('hl'); });
    const style = document.createElementNS('http://www.w3.org/2000/svg', 'style');
    style.textContent = chartCssText();
    clone.insertBefore(style, clone.firstChild);
    return new XMLSerializer().serializeToString(clone);
  }
  function triggerDownload(url, filename) {
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
  }
  function exportSVG(filename) {
    const blob = new Blob([serializeSVG()], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    triggerDownload(url, filename || 'architecture.svg');
    setTimeout(function () { URL.revokeObjectURL(url); }, 60000);
  }
  function exportPNG(filename, scale) {
    const s = scale || 2;
    const svgText = serializeSVG();
    const img = new Image();
    img.onload = function () {
      const canvas = document.createElement('canvas');
      canvas.width = W * s;
      canvas.height = H * s;
      const ctx = canvas.getContext('2d');
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      triggerDownload(canvas.toDataURL('image/png'), filename || 'architecture.png');
    };
    img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgText);
  }
  btn('btn-export-svg', function () { exportSVG('architecture.svg'); });
  btn('btn-export-png', function () { exportPNG('architecture.png', 2); });

  window.__arch = {
    data: data,
    serializeSVG: serializeSVG,
    exportSVG: exportSVG,
    exportPNG: exportPNG,
    zoom: zoom,
    svg: svg,
    state: state
  };
  window.__chartReady = true;
})();
