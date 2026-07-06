# Playwright Automation Patterns (Tier 3)

Code examples and patterns for Playwright-based headless browser automation.
These patterns are used when Tier 1 (built-in browser) and Tier 2 (MCP connector)
are not available.

For the complete Playwright API reference, see [playwright-api.md](./playwright-api.md).

---

## JavaScript Patterns

### Basic Page Test

```javascript
// /tmp/playwright-test-page.js
const { chromium } = require('playwright');

const TARGET_URL = 'http://localhost:3001'; // Auto-detected or from user

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  await page.goto(TARGET_URL);
  console.log('Page loaded:', await page.title());

  await page.screenshot({ path: '/tmp/screenshot.png', fullPage: true });
  console.log('Screenshot saved to /tmp/screenshot.png');

  await browser.close();
})();
```

### Responsive Design Testing (Multiple Viewports)

```javascript
// /tmp/playwright-test-responsive.js
const { chromium } = require('playwright');

const TARGET_URL = 'http://localhost:3001';

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  const viewports = [
    { name: 'Desktop', width: 1920, height: 1080 },
    { name: 'Tablet', width: 768, height: 1024 },
    { name: 'Mobile', width: 375, height: 667 },
  ];

  for (const viewport of viewports) {
    console.log(`Testing ${viewport.name} (${viewport.width}x${viewport.height})`);
    await page.setViewportSize({ width: viewport.width, height: viewport.height });
    await page.goto(TARGET_URL);
    await page.waitForTimeout(1000);
    await page.screenshot({
      path: `/tmp/${viewport.name.toLowerCase()}.png`,
      fullPage: true,
    });
  }

  console.log('All viewports tested');
  await browser.close();
})();
```

### Login Flow

```javascript
// /tmp/playwright-test-login.js
const { chromium } = require('playwright');

const TARGET_URL = 'http://localhost:3001';

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  await page.goto(`${TARGET_URL}/login`);

  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'password123');
  await page.click('button[type="submit"]');

  await page.waitForURL('**/dashboard');
  console.log('Login successful, redirected to dashboard');

  await browser.close();
})();
```

### Form Filling and Submission

```javascript
// /tmp/playwright-test-form.js
const { chromium } = require('playwright');

const TARGET_URL = 'http://localhost:3001';

(async () => {
  const browser = await chromium.launch({ headless: false, slowMo: 50 });
  const page = await browser.newPage();

  await page.goto(`${TARGET_URL}/contact`);

  await page.fill('input[name="name"]', 'John Doe');
  await page.fill('input[name="email"]', 'john@example.com');
  await page.fill('textarea[name="message"]', 'Test message');
  await page.click('button[type="submit"]');

  await page.waitForSelector('.success-message');
  console.log('Form submitted successfully');

  await browser.close();
})();
```

### Broken Link Checker

```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  await page.goto('http://localhost:3000');

  const links = await page.locator('a[href^="http"]').all();
  const results = { working: 0, broken: [] };

  for (const link of links) {
    const href = await link.getAttribute('href');
    try {
      const response = await page.request.head(href);
      if (response.ok()) {
        results.working++;
      } else {
        results.broken.push({ url: href, status: response.status() });
      }
    } catch (e) {
      results.broken.push({ url: href, error: e.message });
    }
  }

  console.log(`Working links: ${results.working}`);
  console.log('Broken links:', results.broken);

  await browser.close();
})();
```

### Screenshot with Error Handling

```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  try {
    await page.goto('http://localhost:3000', {
      waitUntil: 'networkidle',
      timeout: 10000,
    });
    await page.screenshot({ path: '/tmp/screenshot.png', fullPage: true });
    console.log('Screenshot saved to /tmp/screenshot.png');
  } catch (error) {
    console.error('Error:', error.message);
  } finally {
    await browser.close();
  }
})();
```

### Inline Execution (Simple Tasks)

For quick one-off tasks, execute code inline without creating files:

```bash
cd ${SKILL_HOME}/scripts/js && node run.js "
const browser = await chromium.launch({ headless: false });
const page = await browser.newPage();
await page.goto('http://localhost:3001');
await page.screenshot({ path: '/tmp/quick-screenshot.png', fullPage: true });
console.log('Screenshot saved');
await browser.close();
"
```

**When to use inline vs files:**
- **Inline**: Quick one-off tasks (screenshot, check if element exists, get page title)
- **Files**: Complex tests, responsive design checks, anything user might want to re-run

---

## Python Patterns

### Basic Automation with Server Lifecycle

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:5173')
    page.wait_for_load_state('networkidle')
    # ... your automation logic
    browser.close()
```

### Reconnaissance-Then-Action Pattern

1. **Inspect rendered DOM**:
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **Identify selectors** from inspection results

3. **Execute actions** using discovered selectors

---

## Focus-Free Automation

When running Playwright in headed mode (`headless: false`), the browser window
steals OS-level desktop focus on every launch, tab switch, and `bringToFront()`
call. This disrupts the user's active work (typing, clicking, coding). Synthetic
keyboard/mouse events (`page.keyboard.press()`, `page.mouse.click()`) also enter
the OS input queue and can interfere with the user's active input flow.

### Launch Args to Prevent Focus Stealing

Add these Chromium flags to every headed `launchPersistentContext` or `launch`
call:

```javascript
const browser = await chromium.launch({
  headless: false,
  args: [
    '--window-position=-32000,-32000',  // move window off-screen
    '--window-size=1280,720',            // limit window size
    '--no-default-browser-check',        // suppress default-browser prompt
    '--no-first-run',                    // suppress first-run wizard
  ],
});
```

For `launchPersistentContext` (required for extension testing):

```javascript
const context = await chromium.launchPersistentContext(userDataDir, {
  channel: 'chromium',
  headless: false,
  args: [
    `--disable-extensions-except=${extensionPath}`,
    `--load-extension=${extensionPath}`,
    '--window-position=-32000,-32000',
    '--window-size=1280,720',
    '--no-default-browser-check',
    '--no-first-run',
  ],
});
```

### CDP-Based Operations (No Focus Required)

Prefer CDP sessions for operations that normally require window focus:

```javascript
// Screenshot without focusing the tab — CDP does not need an active window
async function cdpScreenshot(page, outPath) {
  const client = await page.context().newCDPSession(page);
  const { data } = await client.send('Page.captureScreenshot', { format: 'png' });
  require('fs').writeFileSync(outPath, Buffer.from(data, 'base64'));
  await client.detach();
}

// Bring tab to front without OS-level focus change
async function cdpBringToFront(page) {
  const client = await page.context().newCDPSession(page);
  await client.send('Page.bringToFront');
  await client.detach();
}
```

### Avoid Synthetic Input

| Instead of | Use | Reason |
|------------|-----|--------|
| `page.keyboard.press('Control+Shift+F')` | `sw.evaluate()` to dispatch the handler directly | Synthetic keys enter the OS input queue and can disrupt the user's active typing. Also, `chrome.commands.onCommand` ignores synthetic keys. |
| `page.mouse.click(x, y)` | `page.click(selector)` or `page.locator(selector).click()` | Coordinate-based clicks are fragile and the mouse event propagates to the OS. Selector-based clicks are scoped to the page DOM. |
| `page.mouse.move(x, y)` | `page.hover(selector)` | Same reason — avoid raw mouse movement. |
| `page.evaluate(() => document.activeElement.blur())` | `page.evaluate(() => document.activeElement?.blur())` | Safe programmatic blur without OS focus change. |

### Rule of Thumb

If an action can be expressed as `page.evaluate()`, `page.fill()`,
`page.click(selector)`, or a service-worker `sw.evaluate()` call, use that
instead of `page.keyboard.*` or `page.mouse.*`. The programmatic path is both
more reliable (no focus dependency) and less disruptive (no OS input queue
pollution).

---

## Prerequisite Service Checks

Before launching browser tests that depend on local services (STS endpoints,
dev servers, API stubs), verify availability. A missing dependency causes
cascading failures that are hard to diagnose from browser console errors alone.

### Pattern: curl-based pre-check

```javascript
const { execSync } = require('child_process');

function checkService(name, url, expectedStatus = 200) {
  try {
    const result = execSync(`curl -s -o /dev/null -w '%{http_code}' ${url}`, {
      timeout: 5000,
      encoding: 'utf-8',
    }).trim();
    if (result === String(expectedStatus) || (expectedStatus === 200 && result === '000' && url.startsWith('http://127.0.0.1'))) {
      // HTTP 000 with localhost means connection refused — treat as failure
      if (result === '000') {
        throw new Error(`${name} not reachable at ${url} (connection refused)`);
      }
      console.log(`[PREREQ] ${name}: OK (${result})`);
    } else {
      throw new Error(`${name} returned ${result}, expected ${expectedStatus}`);
    }
  } catch (e) {
    throw new Error(`[PREREQ FAILED] ${name}: ${e.message}. Start the service and retry.`);
  }
}

// Usage before browser launch:
checkService('STS endpoint', 'http://127.0.0.1:8900/api/v1/aliyun/sts');
checkService('Dev server', 'http://localhost:3001');
```

### Pattern: Chrome process cleanup

When reusing an existing Chrome profile, stale Chrome processes can lock the
profile and prevent `launchPersistentContext` from starting:

```javascript
const { execSync } = require('child_process');

function cleanupChromeProcesses() {
  try {
    // Kill Chrome for Testing processes that may hold the profile lock
    execSync('pkill -f "Google Chrome for Testing" 2>/dev/null || true', {
      timeout: 5000,
      encoding: 'utf-8',
    });
    // Wait for processes to fully exit and release locks
    setTimeout(() => {}, 2000);
  } catch (e) {
    // pkill exits non-zero if no processes found — safe to ignore
  }
  console.log('[CLEANUP] Chrome processes cleaned');
}

// Call before launchPersistentContext when reusing a profile
cleanupChromeProcesses();
```

---

## Cross-Language Patterns

### Taking Screenshots

**JavaScript:**
```javascript
await page.screenshot({ path: '/tmp/screenshot.png', fullPage: true });
await page.locator('.chart').screenshot({ path: '/tmp/chart.png' });
```

**Python:**
```python
page.screenshot(path='/tmp/screenshot.png', full_page=True)
page.locator('.chart').screenshot(path='/tmp/chart.png')
```

### Error Handling

**JavaScript:**
```javascript
try {
  await page.goto(url, { waitUntil: 'networkidle', timeout: 10000 });
} catch (error) {
  console.error('Error:', error.message);
  await page.screenshot({ path: '/tmp/error-screenshot.png' });
} finally {
  await browser.close();
}
```

**Python:**
```python
try:
    page.goto(url, wait_until='networkidle', timeout=10000)
except Exception as e:
    print(f'Error: {e}')
    page.screenshot(path='/tmp/error-screenshot.png')
finally:
    browser.close()
```

---

## Helper Functions

Optional utility functions in `${SKILL_HOME}/scripts/js/lib/helpers.js`:

```javascript
const helpers = require('./lib/helpers');

// Detect running dev servers (CRITICAL - use this first!)
const servers = await helpers.detectDevServers();

// Safe click with retry
await helpers.safeClick(page, 'button.submit', { retries: 3 });

// Safe type with clear
await helpers.safeType(page, '#username', 'testuser');

// Take timestamped screenshot
await helpers.takeScreenshot(page, 'test-result');

// Handle cookie banners
await helpers.handleCookieBanner(page);

// Extract table data
const data = await helpers.extractTableData(page, 'table.results');
```

---

## Custom HTTP Headers

Configure custom headers for all HTTP requests via environment variables.

### Single Header

```bash
PW_HEADER_NAME=X-Automated-By PW_HEADER_VALUE=playwright-skill \
  cd ${SKILL_HOME}/scripts/js && node run.js /tmp/my-script.js
```

### Multiple Headers (JSON)

```bash
PW_EXTRA_HEADERS='{"X-Automated-By":"playwright-skill","X-Debug":"true"}' \
  cd ${SKILL_HOME}/scripts/js && node run.js /tmp/my-script.js
```

### Using Headers in Scripts

```javascript
const context = await helpers.createContext(browser);
const page = await context.newPage();
// All requests include custom headers
```

For raw Playwright API:
```javascript
const context = await browser.newContext(
  getContextOptionsWithHeaders({ viewport: { width: 1920, height: 1080 } }),
);
```
