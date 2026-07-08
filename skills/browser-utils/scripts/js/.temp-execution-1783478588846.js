// Recon: verify Mode 2 login state + enumerate left-nav routes
const { chromium } = require('playwright');
const os = require('os');
const path = require('path');
const fs = require('fs');

const USER_DATA_DIR = path.join(os.homedir(), 'data/chrome/agent');
const APP_ROOT = 'http://xuan-ji.alibaba-inc.com/dashboard/#/common_info/view';

async function enumerateRoutes(page, navSelector = 'nav, .ant-menu, aside, .ant-pro-sider') {
  for (let pass = 0; pass < 8; pass++) {
    const toggles = await page.locator(
      `${navSelector} [aria-expanded="false"], ${navSelector} .ant-menu-submenu-title`
    ).all();
    if (toggles.length === 0) break;
    let clicked = 0;
    for (const t of toggles) {
      try { await t.click({ timeout: 1000 }); clicked++; await page.waitForTimeout(120); }
      catch { /* already open */ }
    }
    if (clicked === 0) break;
  }
  const routes = await page.$$eval(`${navSelector} a[href*="#/"]`, (as) => {
    const seen = new Set();
    const out = [];
    for (const a of as) {
      const href = a.getAttribute('href') || '';
      const m = href.match(/#\/[^\s?]*/);
      if (!m) continue;
      const route = m[0];
      if (seen.has(route)) continue;
      seen.add(route);
      out.push({ route, label: (a.textContent || '').trim() });
    }
    return out;
  });
  return routes;
}

(async () => {
  let context;
  try {
    context = await chromium.launchPersistentContext(USER_DATA_DIR, {
      headless: false,
      channel: 'chrome',
      ignoreDefaultArgs: ['--use-mock-keychain'],
      viewport: { width: 1440, height: 900 },
      args: ['--no-first-run', '--no-default-browser-check'],
    });
    const page = context.pages()[0] || (await context.newPage());
    await page.goto(APP_ROOT, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
    await page.waitForTimeout(2000);
    console.log('FINAL_URL:', page.url());
    console.log('TITLE:', await page.title());
    await page.screenshot({ path: '/tmp/recon-root.png', fullPage: true }).catch(() => {});

    // Dump nav-ish structure for diagnosis
    const navInfo = await page.evaluate(() => {
      const sels = ['nav', '.ant-menu', 'aside', '.ant-pro-sider', '.ant-layout-sider'];
      const found = {};
      for (const s of sels) found[s] = document.querySelectorAll(s).length;
      const anchors = document.querySelectorAll('a[href*="#/"]').length;
      return { found, anchors };
    });
    console.log('NAV_INFO:', JSON.stringify(navInfo));

    const routes = await enumerateRoutes(page);
    console.log('ROUTE_COUNT:', routes.length);
    console.log(JSON.stringify(routes, null, 2));
    fs.writeFileSync('/tmp/spa-routes.json', JSON.stringify(routes, null, 2));
    await page.screenshot({ path: '/tmp/recon-expanded.png', fullPage: true }).catch(() => {});
  } catch (e) {
    console.error('ERROR:', e.message);
  } finally {
    if (context) await context.close();
  }
})();
