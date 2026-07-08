// /tmp/xj-osgrafana-ceiling.js — Mode 2 (real Chrome profile) os-grafana ceiling probe.
// Goal: ONE more attempt to reach the 4 os-grafana login-redirect boards from the
// ~/data/chrome/agent profile. Warm SSO by hitting the os-grafana hosts directly, then
// re-visit each of the 4 xuanji routes and count panels in the embedded iframe.
const { chromium } = require('playwright');
const os = require('os');
const path = require('path');
const fs = require('fs');

const USER_DATA_DIR = path.join(os.homedir(), 'data/chrome/agent');
const BASE = 'http://xuan-ji.alibaba-inc.com/dashboard/';
const RUN_LOG = '/tmp/xj-osgrafana-ceiling-log.json';
const SHOTS = '/tmp/xj-shots5';
fs.mkdirSync(SHOTS, { recursive: true });

const OSG_HOSTS = [
  'https://os-grafana.alibaba-inc.com/',
  'https://os-grafana.alibaba.net/',
];
const BOARDS = [
  { route: '#/memory_baseline', label: '内存开销基线' },
  { route: '#/online_issue_static', label: '袋鼠线上问题统计' },
  { route: '#/kangaroo_market', label: '袋鼠服务大盘' },
  { route: '#/lingjun_business', label: '灵骏业务大盘' },
];

const PANEL_SEL = '.panel-container, [data-panelid], [data-viz-panel-key], .react-grid-item, ' +
  '[data-testid^="data-testid Panel header"]';

function assertNotOnLogin(url) {
  if (/passport|\/login(\b|\/|\?)|\/sso(\b|\/)/i.test(url)) {
    throw new Error('Login state NOT loaded — landed on: ' + url);
  }
  return url;
}

async function countPanels(page) {
  let total = 0, frameUrls = [];
  for (const f of page.frames()) {
    if (f === page.mainFrame()) continue;
    frameUrls.push(f.url());
    try { total += await f.locator(PANEL_SEL).count(); } catch { /* cross-origin */ }
  }
  return { total, frameUrls };
}

async function scrollFrames(page) {
  for (const f of page.frames()) {
    if (f === page.mainFrame()) continue;
    try {
      await f.evaluate(async () => {
        const doc = document.scrollingElement || document.documentElement;
        const step = Math.max(300, Math.floor(window.innerHeight * 0.8));
        for (let y = 0; y <= doc.scrollHeight; y += step) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
        window.scrollTo(0, 0);
      });
    } catch { /* cross-origin */ }
  }
}

(async () => {
  let context;
  const log = { startedAt: new Date().toISOString(), profile: USER_DATA_DIR, profileFreePreflight: true, ssoWarmup: [], boards: [] };
  try {
    context = await chromium.launchPersistentContext(USER_DATA_DIR, {
      headless: false,
      channel: 'chrome',
      ignoreDefaultArgs: ['--use-mock-keychain'],
      viewport: { width: 1440, height: 900 },
      args: ['--no-first-run', '--no-default-browser-check'],
    });
    const page = context.pages()[0] || (await context.newPage());

    // Step 0 — prove xuanji login state.
    await page.goto(BASE, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForLoadState('networkidle', { timeout: 12000 }).catch(() => {});
    log.landingUrl = assertNotOnLogin(page.url());
    console.log('xuanji landing (authenticated):', log.landingUrl);

    // Step 1 — SSO warmup: hit os-grafana hosts directly to trigger/carry SSO.
    for (const host of OSG_HOSTS) {
      try {
        await page.goto(host, { waitUntil: 'domcontentloaded', timeout: 30000 });
        await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});
        await page.waitForTimeout(1500);
        const finalUrl = page.url();
        const title = await page.title().catch(() => '');
        const onLogin = /\/login(\b|\/|\?)|passport|\/sso(\b|\/)/i.test(finalUrl);
        log.ssoWarmup.push({ host, finalUrl, title, onLogin });
        console.log(`SSO warmup ${host} → ${finalUrl} | title="${title}" | onLogin=${onLogin}`);
        await page.screenshot({ path: `${SHOTS}/osg-warmup-${OSG_HOSTS.indexOf(host)}.png` }).catch(() => {});
      } catch (e) {
        log.ssoWarmup.push({ host, error: e.message });
        console.log(`SSO warmup ${host} → ERROR ${e.message}`);
      }
    }

    // Step 2 — re-visit each of the 4 boards after warmup, count panels in iframe.
    for (const b of BOARDS) {
      try {
        // navigate to xuanji base then set hash (route re-render carries the iframe)
        await page.goto(BASE, { waitUntil: 'domcontentloaded', timeout: 30000 });
        await page.evaluate((h) => { window.location.hash = h.replace(/^#/, ''); }, b.route);
        await page.waitForTimeout(1500);
        await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});
        // settle: scroll iframe & poll panel count
        let prev = -1, stable = 0;
        const deadline = Date.now() + 15000;
        while (Date.now() < deadline) {
          await scrollFrames(page);
          const { total } = await countPanels(page);
          if (total > 0 && total === prev) { if (++stable >= 2) break; } else stable = 0;
          prev = total;
          await page.waitForTimeout(600);
        }
        const { total, frameUrls } = await countPanels(page);
        // read iframe src + inner title if same-origin
        let iframeSrc = frameUrls[0] || null, innerTitle = null, dashState = null;
        for (const f of page.frames()) {
          if (f === page.mainFrame()) continue;
          iframeSrc = f.url();
          try {
            innerTitle = await f.title();
            const href = f.url();
            if (/\/login(\b|\/|\?)/i.test(href)) dashState = 'login-redirect (needs secondary auth)';
          } catch { /* cross-origin */ }
        }
        const onLogin = /\/login(\b|\/|\?)|passport/i.test(iframeSrc || '');
        log.boards.push({ route: b.route, label: b.label, panelCount: total, iframeSrc, innerTitle, onLogin, dashState });
        console.log(`BOARD ${b.route} → panels=${total} | iframeSrc=${iframeSrc} | title="${innerTitle}" | onLogin=${onLogin}`);
        await page.screenshot({ path: `${SHOTS}/board-${b.route.replace(/[^a-z_]/gi, '')}.png`, fullPage: true }).catch(() => {});
      } catch (e) {
        log.boards.push({ route: b.route, label: b.label, error: e.message });
        console.log(`BOARD ${b.route} → ERROR ${e.message}`);
      }
    }

    log.finishedAt = new Date().toISOString();
    fs.writeFileSync(RUN_LOG, JSON.stringify(log, null, 2));
    console.log('\nRun log →', RUN_LOG);
    console.log('SUMMARY: os-grafana boards with panels =', log.boards.filter(b => b.panelCount > 0).length, '/ 4');
  } catch (e) {
    console.error('FATAL:', e.message);
    fs.writeFileSync(RUN_LOG, JSON.stringify({ ...log, fatal: e.message }, null, 2));
  } finally {
    if (context) await context.close();
  }
})();
