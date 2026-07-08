# Playwright Automation Patterns (Tier 3)

Code examples and patterns for Playwright-based headless browser automation.
These patterns are used when Tier 1 (built-in browser) and Tier 2 (MCP connector)
are not available.

For the complete Playwright API reference, see [playwright-api.md](./playwright-api.md).

---

## Run Modes (Tier 3)

Tier 3 has two mutually exclusive run modes. Pick the mode **before writing a script**
(see SKILL.md § Run Mode Selection). This section is the launch recipe for each.

### Mode 1 — Clean Test Browser (default)

Playwright's bundled Chromium / Chrome for Testing, fresh ephemeral context, default
`--use-mock-keychain`. Use for frontend/localhost automation and E2E testing. No real
login state — every run starts clean. This is the `chromium.launch()` used by every
example below (Basic Page Test, Responsive, Form Filling, etc.).

```javascript
const browser = await chromium.launch({ headless: false });
const page = await browser.newPage();
// ... test the app; nothing persists between runs
await browser.close();
```

### Mode 2 — Real Chrome Profile (reuse login state)

Drives the **real Google Chrome** against an existing user-data-dir so its cookies and
localStorage (logins) are reused. Required to reach authenticated/internal sites.

Three conditions must ALL hold, or login state silently fails:

1. **Profile not in use** — Chrome is single-instance per profile. If a Chrome is
   already running on `userDataDir`, the launch is handed off to that window and the
   controllable process exits immediately (`正在现有的浏览器会话中打开`). Preflight it.
2. **`channel: 'chrome'`** — must be the real Google Chrome binary, not bundled
   Chromium/Chrome for Testing. Cookies are encrypted with a macOS Keychain "Safe
   Storage" key that is *per-app*; a different binary cannot decrypt them.
3. **`ignoreDefaultArgs: ['--use-mock-keychain']`** — Playwright injects
   `--use-mock-keychain` by default, which bypasses the real keychain. Drop it so
   Chrome uses the real key that decrypts the profile's cookies.

**Preflight (bash) — verify the profile is free before launching:**

```bash
USER_DATA_DIR="$HOME/data/chrome/agent"   # the target profile
# Any process holding the profile? (non-empty ⇒ ask the user to close it)
ps aux | grep -F "user-data-dir=$USER_DATA_DIR" | grep -v grep
# Stale singleton lock present? (informational)
ls -la "$USER_DATA_DIR" | grep -i singleton
```

**Launch recipe (JavaScript):**

```javascript
// /tmp/playwright-test-profile.js
const { chromium } = require('playwright');
const os = require('os');
const path = require('path');

const USER_DATA_DIR = path.join(os.homedir(), 'data/chrome/agent');
const TARGET_URL = 'https://internal.example.com/dashboard';

(async () => {
  let context;
  try {
    context = await chromium.launchPersistentContext(USER_DATA_DIR, {
      headless: false,
      channel: 'chrome',                              // real Chrome → keychain key matches
      ignoreDefaultArgs: ['--use-mock-keychain'],     // use the REAL keychain to decrypt cookies
      viewport: { width: 1440, height: 900 },
      args: ['--no-first-run', '--no-default-browser-check'],
    });
    const page = context.pages()[0] || (await context.newPage());
    await page.goto(TARGET_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
    console.log('Final URL:', page.url());            // if it ends on a login page, login state did NOT load
    await page.screenshot({ path: '/tmp/profile-page.png', fullPage: true });
  } catch (e) {
    console.error('ERROR:', e.message);
  } finally {
    if (context) await context.close();
  }
})();
```

**Failure-symptom table:**

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Target page, context or browser has been closed` + `正在现有的浏览器会话中打开` | A Chrome is already running on the profile | Close it (preflight #1), then relaunch |
| Page redirects to the SSO/login page despite a logged-in profile | Bundled Chromium used, or `--use-mock-keychain` kept | Add `channel: 'chrome'` **and** `ignoreDefaultArgs: ['--use-mock-keychain']` |
| `kill EPERM` in browser logs on close | Handoff process couldn't be killed (side effect of #1) | Same as the handoff row — free the profile first |

> If the profile is in use and cannot be closed, an alternative is to launch Chrome
> yourself with `--remote-debugging-port=<port>` and attach via
> `chromium.connectOverCDP('http://127.0.0.1:<port>')`, which coexists with a manually
> opened window. Confirm this approach with the user first.

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
