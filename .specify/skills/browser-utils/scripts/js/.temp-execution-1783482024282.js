// Round-3 SPA traversal for xuan-ji.alibaba-inc.com — Tier 3 Mode 2 (real Chrome profile).
// Assembled per browser-utils skill: Step 0→4. Enhancements vs round-2:
//  - settleDynamicContent scrolls EACH dashboard iframe top→bottom AND expands collapsed
//    Grafana rows so lazy panels mount (fixes "(0 panels)").
//  - extractDoc captures: panel GROUPS (row header text w/ counts), individual panel
//    TITLES, live panel COUNT (DOM elements), template-variable NAMES (labels, not values).
//  - native depth preserved+extended: inputs with TYPE, checkboxes, pagination, selects+options.
const { chromium } = require('playwright');
const fs = require('fs');
const os = require('os');
const path = require('path');

const RUN_LOG = '/tmp/spa-run-log.json';
const CHECKPOINT = '/tmp/spa-traversal.json';
const DESIGN_DOC = '/tmp/spa-design-doc.md';
const SHOTS = '/tmp/xj-shots3';
const USER_DATA_DIR = path.join(os.homedir(), 'data/chrome/agent');
const TARGET_URL = 'http://xuan-ji.alibaba-inc.com/dashboard/#/';

// ---------- Step 0: login assertion + run log ----------
function assertNotOnLogin(page) {
  const url = page.url();
  if (/login[^/]*\.alibaba-inc\.com|passport|\/login(\b|\/|\?)|\/sso(\b|\/)/i.test(url)) {
    throw new Error(`Login state NOT loaded — landed on login page: ${url}`);
  }
  return url;
}
function openRunLog(runInfo) {
  const log = { startedAt: new Date().toISOString(), ...runInfo, modules: [] };
  fs.writeFileSync(RUN_LOG, JSON.stringify(log, null, 2));
  return log;
}
function saveRunLog(log) { fs.writeFileSync(RUN_LOG, JSON.stringify(log, null, 2)); }

// ---------- Step 1: enumerate routes ----------
async function enumerateRoutes(page, navSelector = 'nav, .ant-menu, aside') {
  for (let pass = 0; pass < 8; pass++) {
    const toggles = await page.locator(
      `${navSelector} [aria-expanded="false"], ` +
      `${navSelector} .ant-menu-submenu:not(.ant-menu-submenu-open) > .ant-menu-submenu-title`
    ).all();
    if (toggles.length === 0) break;
    let clicked = 0;
    for (const t of toggles) {
      try { await t.click({ timeout: 1000 }); clicked++; await page.waitForTimeout(150); } catch {}
    }
    if (clicked === 0) break;
  }
  const routes = await page.$$eval(`${navSelector} a[href*="#/"]`, (as) => {
    const seen = new Set(); const out = [];
    // also capture the nearest submenu group label for context
    for (const a of as) {
      const href = a.getAttribute('href') || '';
      const m = href.match(/#\/[^\s?]*/);
      if (!m) continue;
      const route = m[0];
      if (seen.has(route)) continue;
      seen.add(route);
      let group = '';
      let el = a.closest('.ant-menu-submenu');
      if (el) { const t = el.querySelector('.ant-menu-submenu-title'); if (t) group = (t.textContent||'').trim(); }
      out.push({ route, label: (a.textContent || '').trim(), group });
    }
    return out;
  });
  return routes;
}

// ---------- Step 2: SPA route wait ----------
async function gotoRoute(page, baseUrl, route, contentSelector = 'main, .ant-pro-page-container, #root > div') {
  const before = page.url();
  await page.evaluate((h) => { window.location.hash = h.replace(/^#/, ''); }, route);
  await page.waitForFunction((prev) => location.href !== prev, before, { timeout: 8000 }).catch(() => {});
  await page.waitForSelector(contentSelector, { timeout: 8000 }).catch(() => {});
  await page.waitForLoadState('networkidle', { timeout: 6000 }).catch(() => {});
  await page.waitForTimeout(400);
}

// ---------- Step 2.5: settle dynamic content ----------
const PANEL_SEL = '.panel-container, [data-panelid], [data-viz-panel-key], .react-grid-item, ' +
                  '[data-testid^="data-testid Panel header"]';

async function expandDashRows(frame) {
  // Expand ONLY collapsed Grafana rows so their panels mount (don't toggle open ones shut).
  try {
    const collapsed = await frame.locator(
      '.dashboard-row--collapsed .dashboard-row__title, ' +
      '[data-testid="dashboard-row-title"][aria-expanded="false"], ' +
      'button[aria-expanded="false"][data-testid^="data-testid dashboard row"]'
    ).all();
    for (const r of collapsed.slice(0, 40)) {
      await r.click({ timeout: 600 }).catch(() => {});
      await frame.page().waitForTimeout(120);
    }
  } catch {}
}

async function settleDynamicContent(page, { timeout = 15000 } = {}) {
  const dashFrames = async () => {
    const out = [];
    for (const f of page.frames()) {
      if (f === page.mainFrame()) continue;
      if (/grafana|dashboard|kibana|d-solo|\/d\//i.test(f.url())) { out.push(f); continue; }
      try { if (await f.locator(PANEL_SEL).count() > 0) out.push(f); } catch {}
    }
    return out;
  };
  const countPanels = async () => {
    let total = 0;
    for (const frame of page.frames()) { try { total += await frame.locator(PANEL_SEL).count(); } catch {} }
    return total;
  };
  const scrollDashFrames = async (frames) => {
    for (const frame of frames) {
      await expandDashRows(frame);
      try {
        await frame.evaluate(async () => {
          const doc = document.scrollingElement || document.documentElement;
          const step = Math.max(300, Math.floor(window.innerHeight * 0.8));
          for (let y = 0; y <= doc.scrollHeight; y += step) {
            window.scrollTo(0, y);
            await new Promise((r) => setTimeout(r, 150));
          }
          window.scrollTo(0, 0);
        });
      } catch {}
    }
  };
  const frames0 = await dashFrames();
  const hasDashboardFrame = frames0.length > 0;
  const deadline = Date.now() + timeout;
  let prev = -1, stable = 0;
  while (Date.now() < deadline) {
    if (hasDashboardFrame) await scrollDashFrames(await dashFrames());
    const n = await countPanels();
    if (n === 0 && !hasDashboardFrame && Date.now() - (deadline - timeout) > 1500) break;
    if (n > 0 && n === prev) { if (++stable >= 2) break; } else { stable = 0; }
    prev = n;
    await page.waitForTimeout(500);
  }
  for (const frame of page.frames()) {
    await frame.locator('.panel-loading, [aria-label="Panel loading bar"], [data-testid="Panel loading bar"], .ant-spin-spinning, .ant-skeleton')
      .first().waitFor({ state: 'hidden', timeout: 3000 }).catch(() => {});
  }
  await revealTabsAndRows(page);
}

async function revealTabsAndRows(page) {
  const tabs = await page.locator('.ant-tabs-tab:not(.ant-tabs-tab-active), [role="tab"]:not([aria-selected="true"])').all();
  for (const tab of tabs.slice(0, 12)) { await tab.click({ timeout: 800 }).catch(() => {}); await page.waitForTimeout(200); }
  const rowToggles = await page.locator('.ant-table-row-expand-icon-collapsed, [aria-label="Expand row"]').all();
  for (const r of rowToggles.slice(0, 20)) { await r.click({ timeout: 500 }).catch(() => {}); }
}

// ---------- Ant Select options (interaction-gated) ----------
async function readSelectOptions(page, { maxSelects = 10, maxOptions = 60 } = {}) {
  const selects = await page.locator('.ant-select:not(.ant-select-disabled)').all();
  const out = [];
  for (const sel of selects.slice(0, maxSelects)) {
    let placeholder = '';
    try {
      placeholder = ((await sel.locator('.ant-select-selection-placeholder, .ant-select-selection-item')
        .first().textContent({ timeout: 500 })) || '').trim();
    } catch {}
    let options = [];
    try {
      await sel.click({ timeout: 800 });
      await page.waitForTimeout(280);
      options = await page.locator('.ant-select-dropdown:not(.ant-select-dropdown-hidden) .ant-select-item-option-content').allTextContents();
      options = [...new Set(options.map((o) => o.trim()).filter(Boolean))].slice(0, maxOptions);
      await page.keyboard.press('Escape');
    } catch { await page.keyboard.press('Escape').catch(() => {}); }
    if (placeholder || options.length) out.push({ placeholder, options });
  }
  return out;
}

// ---------- Step 3: extract ----------
async function extractModule(page) {
  const extractDoc = () => {
    const txt = (el) => (el?.textContent || '').trim().replace(/\s+/g, ' ');
    const many = (sel) => Array.from(document.querySelectorAll(sel)).map(txt).filter(Boolean);
    const BTN_NOISE = /^(increase|decrease) value$|^(add panel|add row|add library panel|share|save dashboard|exit edit mode|search dashboards|搜索或跳转至\.\.\.|cmd\+k)$/i;
    // inputs with inferred type
    const inputs = [];
    Array.from(document.querySelectorAll('input')).forEach((i) => {
      const ph = i.getAttribute('placeholder') || '';
      let type = 'text';
      const t = (i.getAttribute('type') || '').toLowerCase();
      if (i.closest('.ant-picker')) type = 'date';
      else if (t === 'search' || i.closest('.ant-input-search')) type = 'search';
      else if (t === 'number' || i.closest('.ant-input-number')) type = 'number';
      else if (t === 'checkbox' || t === 'radio') return;
      if (ph) inputs.push({ placeholder: ph, type });
    });
    Array.from(document.querySelectorAll('textarea')).forEach((i) => {
      const ph = i.getAttribute('placeholder') || '';
      if (ph) inputs.push({ placeholder: ph, type: 'textarea' });
    });
    const checkboxes = [...new Set(many('.ant-checkbox-wrapper'))].slice(0, 30);
    const tables = Array.from(document.querySelectorAll('table, .ant-table')).slice(0, 10).map((t) => ({
      columns: Array.from(t.querySelectorAll('th, .ant-table-cell[role="columnheader"]')).map((h) => txt(h)).filter(Boolean).slice(0, 40),
    })).filter((t) => t.columns.length);
    const pagination = [...new Set(many('.ant-pagination'))].slice(0, 3);
    // Grafana panel GROUPS: any element whose text is "<title>(N panels)" (row headers).
    const groupSet = new Set();
    Array.from(document.querySelectorAll('button, .dashboard-row__title, [role="button"], span, a')).forEach((el) => {
      const s = txt(el);
      if (/^.{1,80}\((\d+)\s+panels?\)$/i.test(s)) groupSet.add(s);
    });
    const panelGroups = [...groupSet].slice(0, 80);
    // individual panel titles
    const panelTitles = [...new Set([
      ...many('.panel-title, h2.panel-title, [class*="panel-title"]'),
      ...Array.from(document.querySelectorAll('[data-testid^="data-testid Panel header"]'))
        .map((el) => (el.getAttribute('aria-label') || el.textContent || '').replace(/^data-testid Panel header\s*/i, '').trim()).filter(Boolean),
    ])].filter(Boolean).slice(0, 120);
    const panelCount = document.querySelectorAll('.panel-container, [data-viz-panel-key], [data-panelid], [data-testid^="data-testid Panel header"]').length;
    // template-variable NAMES (labels, not values)
    const variables = [...new Set([
      ...Array.from(document.querySelectorAll(
        '[data-testid^="data-testid Dashboard template variables submenu Label"], ' +
        '[data-testid^="data-testid template variable"] label'))
        .map((el) => (el.getAttribute('aria-label') || el.textContent || '').replace(/^data-testid.*Label\s*/i, '').trim()).filter(Boolean),
      ...many('.template-variable .template-variable__label, .gf-form-label--variable, .submenu-item > label'),
    ])].filter(Boolean).slice(0, 60);
    return {
      title: document.title,
      headings: [...many('h1'), ...many('h2'), ...many('h3')].slice(0, 20),
      breadcrumb: many('.ant-breadcrumb a, .ant-breadcrumb span').slice(0, 10),
      inputs: inputs.slice(0, 40),
      checkboxes,
      filters: [...many('.ant-form-item-label label'), ...many('.ant-select-selection-placeholder')].slice(0, 40),
      buttons: [...new Set(many('button, .ant-btn'))].filter((b) => b && !BTN_NOISE.test(b) && !/\(\d+\s+panels?\)$/i.test(b)).slice(0, 40),
      tabs: [...new Set(many('.ant-tabs-tab, [role="tab"]'))].slice(0, 20),
      tables,
      pagination,
      charts: document.querySelectorAll('canvas, svg.recharts-surface, .echarts-for-react').length,
      metrics: many('.ant-statistic, .ant-card-head-title, .ant-descriptions-item').slice(0, 30),
      panelGroups, panelTitles, panelCount, variables,
    };
  };

  const main = await page.evaluate(extractDoc);
  main.selects = await readSelectOptions(page);

  const frames = [];
  for (const frame of page.frames()) {
    if (frame === page.mainFrame()) continue;
    const src = frame.url();
    if (!src || src === 'about:blank') continue;
    let inner = null;
    try { inner = await frame.evaluate(extractDoc); } catch { inner = null; }
    frames.push({ src, sameOrigin: !!inner, inner });
  }
  return { ...main, frames };
}

// ---------- Step 4: drive + checkpoint ----------
function loadCheckpoint() { try { return JSON.parse(fs.readFileSync(CHECKPOINT, 'utf8')); } catch { return null; } }
function saveCheckpoint(cp) { fs.writeFileSync(CHECKPOINT, JSON.stringify(cp, null, 2)); }

function synthesizePurpose(route, label, info) {
  const entity = label || (info.headings && info.headings[0]) || info.title || route;
  const bits = [];
  const panelGroups = (info.frames || []).flatMap((f) => (f.inner && f.inner.panelGroups) || []).concat(info.panelGroups || []);
  const panelTitles = (info.frames || []).flatMap((f) => (f.inner && f.inner.panelTitles) || []).concat(info.panelTitles || []);
  const dashFrame = (info.frames || []).some((f) => /grafana|dashboard|kibana/i.test(f.src || '')) || panelGroups.length || panelTitles.length;
  if (dashFrame) {
    if (panelGroups.length) bits.push(`大盘分组: ${panelGroups.slice(0, 4).map((g)=>g.replace(/\(\d+.*/,'')).join('/')}`);
    else if (panelTitles.length) bits.push(`大盘面板: ${panelTitles.slice(0, 4).join('/')}`);
    else bits.push('Grafana 大盘（面板未读取）');
  }
  const cols = [...new Set((info.tables || []).flatMap((t) => t.columns || []).map((c) => (c || '').trim()).filter((c) => c && c.length <= 14))].slice(0, 4);
  if (cols.length) bits.push(`表格列: ${cols.join('/')}`);
  const actions = [...new Set((info.buttons || []).filter((b) => /查询|搜索|搜 索|查 询|诊断|诊 断|刷新|新增|新建|创建|添加|导入|导出|发布|下载|预览|复制|显示/.test(b)))].slice(0, 3);
  if (actions.length) bits.push(`操作: ${actions.join('/')}`);
  const inputs = (info.inputs || []).map((i) => i.placeholder).filter(Boolean).slice(0, 3);
  if (inputs.length && !cols.length) bits.push(`筛选: ${inputs.join('/')}`);
  const tabs = [...new Set((info.tabs || []).map((t) => (t || '').trim()).filter(Boolean))].slice(0, 5);
  if (tabs.length > 1) bits.push(`${tabs.length} 页签: ${tabs.join('/')}`);
  if (!bits.length) {
    if (info.charts) bits.push(`${info.charts} 个图表`);
    else if (info.metrics && info.metrics.length) bits.push(`展示 ${info.metrics.slice(0, 3).join('/')}`);
  }
  return bits.length ? `${entity} — ${bits.join('；')}` : entity;
}

function appendModuleDoc(route, label, info) {
  const lines = [ `\n## ${label || route}  \n\`${route}\``, `- **Purpose**: ${synthesizePurpose(route, label, info)}` ];
  if (info.inputs?.length) lines.push(`- **Inputs**: ${info.inputs.map((i)=>`${i.placeholder}[${i.type}]`).join(', ')}`);
  if (info.checkboxes?.length) lines.push(`- **Checkboxes**: ${info.checkboxes.join(' / ')}`);
  if (info.selects?.length) info.selects.forEach((s) => lines.push(`- **Select "${s.placeholder||'(unlabeled)'}"**: ${s.options.length?s.options.join(', '):'(no static options)'}`));
  if (info.buttons?.length) lines.push(`- **Buttons**: ${info.buttons.join(', ')}`);
  if (info.tabs?.length) lines.push(`- **Tabs**: ${info.tabs.join(' / ')}`);
  info.tables?.forEach((t, i) => lines.push(`- **Table ${i+1}**: ${t.columns.join(' | ')}`));
  if (info.pagination?.length) lines.push(`- **Pagination**: ${info.pagination.join(' ')}`);
  if (info.charts) lines.push(`- **Charts**: ${info.charts}`);
  for (const f of info.frames || []) {
    lines.push(`- **iframe**: ${f.src}${f.sameOrigin?'':' (cross-origin)'}`);
    const inner = f.inner;
    if (inner) {
      if (inner.title) lines.push(`  - Title: ${inner.title}`);
      if (inner.panelGroups?.length) lines.push(`  - PanelGroups(${inner.panelGroups.length}): ${inner.panelGroups.join('; ')}`);
      if (inner.panelCount) lines.push(`  - PanelCount: ${inner.panelCount}`);
      if (inner.panelTitles?.length) lines.push(`  - PanelTitles: ${inner.panelTitles.join('; ')}`);
      if (inner.variables?.length) lines.push(`  - Variables: ${inner.variables.join(', ')}`);
      if (inner.tables?.length) lines.push(`  - Table cols: ${inner.tables.map((t)=>t.columns.join(' | ')).join(' || ')}`);
    }
  }
  fs.appendFileSync(DESIGN_DOC, lines.filter(Boolean).join('\n') + '\n');
}

async function traverse(page, baseUrl, runInfo = {}) {
  await page.goto(baseUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await settleDynamicContent(page, { timeout: 8000 });
  const landingUrl = assertNotOnLogin(page);
  const runLog = openRunLog({ ...runInfo, baseUrl, landingUrl });

  let cp = loadCheckpoint();
  if (!cp) {
    const routes = await enumerateRoutes(page);
    cp = { visited: [], pending: routes, data: {} };
    saveCheckpoint(cp);
    if (!fs.existsSync(DESIGN_DOC)) fs.writeFileSync(DESIGN_DOC, `# SPA Design Doc — ${baseUrl}\n`);
    runLog.routeCount = routes.length; saveRunLog(runLog);
  }
  while (cp.pending.length) {
    const { route, label, group } = cp.pending[0];
    try {
      await gotoRoute(page, baseUrl, route);
      await settleDynamicContent(page, { timeout: 16000 });
      assertNotOnLogin(page);
      const info = await extractModule(page);
      const shot = `${SHOTS}/${String(cp.visited.length).padStart(2,'0')}_${route.replace(/[^a-z0-9]/gi,'_')}.png`;
      let screenshot = shot;
      try { await page.screenshot({ path: shot, fullPage: true }); }
      catch (se) { screenshot = null; console.error(`  screenshot failed ${route}: ${se.message}`); }
      appendModuleDoc(route, label, info);
      cp.data[route] = { label, group, info, screenshot };
      const dashPanels = (info.frames||[]).reduce((a,f)=>a+((f.inner&&f.inner.panelCount)||0),0);
      runLog.modules.push({ route, label, group, screenshot, panelCount: dashPanels, purpose: synthesizePurpose(route, label, info) });
      console.log(`OK ${cp.visited.length + 1}: ${label} ${route} [panels:${dashPanels}]${screenshot?'':' (NO SHOT)'}`);
    } catch (e) {
      console.error(`FAIL ${route}: ${e.message}`);
      cp.data[route] = { label, group, error: e.message };
      runLog.modules.push({ route, label, group, error: e.message });
    }
    cp.visited.push(cp.pending.shift());
    saveCheckpoint(cp);
    saveRunLog(runLog);
  }
  runLog.finishedAt = new Date().toISOString();
  runLog.missingScreenshots = runLog.modules.filter((m) => !m.error && !m.screenshot).length;
  saveRunLog(runLog);
  console.log(`Done: ${cp.visited.length} modules -> ${DESIGN_DOC} (log ${RUN_LOG})`);
}

(async () => {
  let context;
  try {
    context = await chromium.launchPersistentContext(USER_DATA_DIR, {
      headless: false,
      channel: 'chrome',
      ignoreDefaultArgs: ['--use-mock-keychain'],
      viewport: { width: 1600, height: 1000 },
      args: ['--no-first-run', '--no-default-browser-check'],
    });
    const page = context.pages()[0] || (await context.newPage());
    await traverse(page, TARGET_URL, { mode: 'mode2', profile: USER_DATA_DIR, profileFreePreflight: true });
  } catch (e) { console.error('FATAL:', e.message); }
  finally { if (context) await context.close(); }
})();
