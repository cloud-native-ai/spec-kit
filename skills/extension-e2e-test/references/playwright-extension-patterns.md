# Playwright Chrome Extension Testing Patterns

Complete code patterns for testing each Chrome extension surface with Playwright.
All patterns assume the extension is loaded via `launchPersistentContext` with
`--load-extension` (see SKILL.md Step 3).

## Table of Contents

1. [Extension Launch & Teardown](#1-extension-launch--teardown)
2. [Service Worker Testing](#2-service-worker-testing)
3. [Popup Page Testing](#3-popup-page-testing)
4. [Options Page Testing](#4-options-page-testing)
5. [Content Script Testing](#5-content-script-testing)
6. [Keyboard Command Testing](#6-keyboard-command-testing)
7. [Chrome Storage Testing](#7-chrome-storage-testing)
8. [Multi-Tab Testing](#8-multi-tab-testing)
9. [CDP Session — bringToFront](#9-cdp-session--bringtofront)
10. [Login State Reuse](#10-login-state-reuse)
11. [Network Mocking (Read-only Safety)](#11-network-mocking-read-only-safety)

---

## 1. Extension Launch & Teardown

Base pattern for every test — launches Chrome for Testing with the extension loaded.

```javascript
const { chromium } = require('playwright');
const path = require('path');

const EXTENSION_PATH = path.resolve(__dirname, '../../dist');  // or absolute path
const USER_DATA_DIR = '/tmp/extension-e2e-profile';

let context;

async function launchExtension() {
  context = await chromium.launchPersistentContext(USER_DATA_DIR, {
    channel: 'chromium',     // Chrome for Testing — supports --load-extension
    headless: false,         // Extensions require headed mode
    args: [
      `--disable-extensions-except=${EXTENSION_PATH}`,
      `--load-extension=${EXTENSION_PATH}`,
    ],
  });
  return context;
}

async function getExtensionId(context) {
  let [serviceWorker] = context.serviceWorkers();
  if (!serviceWorker) {
    serviceWorker = await context.waitForEvent('serviceworker', { timeout: 10000 });
  }
  // Service worker URL format: chrome-extension://<id>/background.js
  return serviceWorker.url().split('/')[2];
}

async function teardown() {
  if (context) {
    await context.close();
    context = null;
  }
}

// Usage:
(async () => {
  try {
    const ctx = await launchExtension();
    const extensionId = await getExtensionId(ctx);
    console.log('Extension ID:', extensionId);
    // ... run tests ...
  } finally {
    await teardown();
  }
})();
```

---

## 2. Service Worker Testing

The MV3 service worker is the extension's background script. Playwright provides
direct access via `context.serviceWorkers()`.

```javascript
async function testServiceWorker(context) {
  let [sw] = context.serviceWorkers();
  if (!sw) {
    sw = await context.waitForEvent('serviceworker', { timeout: 10000 });
  }

  // Evaluate code inside the service worker context
  const manifest = await sw.evaluate(async () => {
    // Access chrome.runtime APIs inside the service worker
    const manifest = chrome.runtime.getManifest();
    return {
      name: manifest.name,
      version: manifest.version,
      manifestVersion: manifest.manifest_version,
      permissions: manifest.permissions,
    };
  });
  console.log('Manifest:', JSON.stringify(manifest, null, 2));

  // Send a message to the service worker
  const response = await sw.evaluate(async () => {
    return new Promise((resolve) => {
      chrome.runtime.sendMessage({ type: 'PING' }, (response) => {
        resolve(response);
      });
    });
  });
  console.log('Service worker response:', response);

  // MV3 service workers suspend after ~30s of inactivity.
  // Playwright automatically handles this — the same Worker object
  // stays valid across suspend/restart cycles.
  // Just issue new evaluate() calls; they will wait for restart if needed.
}
```

---

## 3. Popup Page Testing

The popup page runs as an extension page. Navigate to it directly via its
`chrome-extension://` URL.

```javascript
async function testPopup(context, extensionId) {
  const popupPage = await context.newPage();
  await popupPage.goto(`chrome-extension://${extensionId}/popup.html`, {
    waitUntil: 'load',
  });

  // Read popup title
  const title = await popupPage.title();
  console.log('Popup title:', title);

  // Read popup content
  const bodyText = await popupPage.locator('body').innerText();

  // Find and interact with UI elements
  // Example: find a button by text and click it
  const buttons = popupPage.locator('button');
  const count = await buttons.count();
  console.log(`Found ${count} buttons in popup`);

  // Click a specific button
  // await popupPage.click('button:has-text("配置")');

  // Fill form inputs
  // await popupPage.fill('input[name="region"]', 'oss-cn-hangzhou');

  // Take a screenshot for debugging
  await popupPage.screenshot({ path: '/tmp/extension-popup-screenshot.png' });

  await popupPage.close();
}
```

---

## 4. Options Page Testing

The options page is a standard extension page. Same approach as popup.

```javascript
async function testOptionsPage(context, extensionId) {
  const optionsPage = await context.newPage();
  await optionsPage.goto(`chrome-extension://${extensionId}/options.html`, {
    waitUntil: 'load',
  });

  // Read options page content
  const title = await optionsPage.title();
  console.log('Options title:', title);

  // Test form interactions
  // Example: fill OSS configuration fields
  // await optionsPage.fill('input#region', 'oss-cn-hangzhou');
  // await optionsPage.fill('input#bucket', 'test-bucket');
  // await optionsPage.fill('input#stsUrl', 'https://sts.example.com');
  // await optionsPage.click('button:has-text("Save")');

  // Verify saved values
  // const savedRegion = await optionsPage.inputValue('input#region');
  // assert(savedRegion === 'oss-cn-hangzhou');

  await optionsPage.screenshot({ path: '/tmp/extension-options-screenshot.png' });
  await optionsPage.close();
}
```

---

## 5. Content Script Testing

Content scripts are injected into web pages matching `manifest.json`'s
`content_scripts.matches` pattern. Navigate to a matching URL to trigger injection.

> **This project**: only `static/js/main.js` and `static/js/clipper.js` are declared
> content scripts (auto-injected on `<all_urls>` at `document_end`). The per-platform
> scripts (`asiops/aone/qianzhou/cc/work/splc`) are **injected on demand** by the
> service worker via `chrome.scripting` when a command fires — navigating to a platform
> URL will **not** inject them. To test those, drive the command path (§6).

```javascript
async function testContentScript(context, targetUrl) {
  const page = await context.newPage();
  await page.goto(targetUrl, { waitUntil: 'load', timeout: 30000 });

  // Content scripts execute in an isolated world.
  // To verify injection, check for side effects on the page DOM.
  // For example, if the content script adds a floating button:
  // const injectedButton = await page.locator('#xuanji-float-btn').count();
  // if (injectedButton > 0) {
  //   console.log('Content script injected successfully');
  // }

  // Or check for global variables set by the content script
  // Note: content scripts run in isolated world, so page.evaluate()
  // cannot directly access their variables. Look for DOM side effects instead.

  // Listen for console messages from the content script
  page.on('console', (msg) => {
    if (msg.type() === 'log') {
      console.log('[content script console]:', msg.text());
    }
  });

  // Take a screenshot to verify visual state
  await page.screenshot({ path: '/tmp/extension-content-script.png' });

  await page.close();
}
```

---

## 6. Keyboard Command Testing

> ⚠️ **Synthetic key presses do NOT trigger `chrome.commands.onCommand`.**
> The extension's shortcuts (`fetch_asiops_data`=Ctrl+Shift+F,
> `clip_handle_selection`=Ctrl+Shift+S, `fetch_splc_data`=Ctrl+Shift+L) are
> **browser-level** bindings. `page.keyboard.press('Control+Shift+F')` reaches the
> page, not the browser command dispatcher, so it will **not** fire the handler.
> This is a known limitation — see `docs/testing/e2e-browser-testing-research.md` §5.1.

Use one of the equivalent trigger paths below instead.

### 6a. Invoke the command handler in the service worker (recommended)

The service worker's `chrome.commands.onCommand` listener does the real work: it
injects the platform script and then `chrome.tabs.sendMessage`s the active tab with a
`WindowMessageType`. Invoke that listener directly to cover the shortcut branch without
relying on synthetic keys.

```javascript
async function triggerCommand(context, command) {
  // command ∈ 'fetch_asiops_data' | 'clip_handle_selection' | 'fetch_splc_data'
  let [sw] = context.serviceWorkers();
  if (!sw) sw = await context.waitForEvent('serviceworker', { timeout: 10000 });

  // Make sure the target tab is the active one — the handler queries
  // chrome.tabs.query({ active: true, currentWindow: true }).
  await sw.evaluate((cmd) => {
    // chrome.commands.onCommand cannot be dispatched programmatically, but the
    // background registers its listener as `command_listener`; call it directly.
    // Fallback: if not exposed, replay the message the handler would send.
    return globalThis.command_listener
      ? globalThis.command_listener(cmd)
      : Promise.reject(new Error('command_listener not exposed on globalThis'));
  }, command);

  console.log(`Dispatched command: ${command}`);
}
```

> If `command_listener` is not on `globalThis`, either expose it from
> `src/service/background.ts` for testability, or use the message-replay path (6b).

### 6b. Replay the equivalent message to the content script

The handler ultimately sends `chrome.tabs.sendMessage(tabId, { type, attachment })`.
You can replay that exact message from the service worker against the active tab:

```javascript
async function replayCommandMessage(context, page) {
  let [sw] = context.serviceWorkers();
  if (!sw) sw = await context.waitForEvent('serviceworker', { timeout: 10000 });
  await page.bringToFront(); // ensure it is the active tab the handler would target

  await sw.evaluate(async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    // WindowMessageType values (from src/common/message.ts). Include the attachment
    // shape the real handler builds (e.g. { ossConfig, fetchTypes } for asiops).
    await chrome.tabs.sendMessage(tab.id, {
      type: 'FETCH_ASIOPS_DATA',
      attachment: { /* ossConfig, fetchTypes — mock or real */ },
    });
  });
}
```

### 6c. Trigger via the popup UI (closest to a real user)

If the popup exposes equivalent buttons, clicking them drives the same
`WindowMessageType` message chain and is the most faithful E2E path:

```javascript
// await popupPage.click('button:has-text("获取数据")');
```

---

## 7. Chrome Storage Testing

Test `chrome.storage` API through the popup or options page context, which has
access to the extension's storage.

```javascript
async function testChromeStorage(context, extensionId) {
  const page = await context.newPage();
  await page.goto(`chrome-extension://${extensionId}/popup.html`, {
    waitUntil: 'load',
  });

  // Read from chrome.storage.local
  const storageData = await page.evaluate(async () => {
    return new Promise((resolve) => {
      chrome.storage.local.get(null, (items) => {
        resolve(items);
      });
    });
  });
  console.log('Current storage:', JSON.stringify(storageData, null, 2));

  // Write to chrome.storage.local
  await page.evaluate(async () => {
    return new Promise((resolve) => {
      chrome.storage.local.set({
        'test-key': 'test-value',
        'test-config': { region: 'oss-cn-hangzhou', bucket: 'test' },
      }, () => {
        resolve(true);
      });
    });
  });

  // Verify the write
  const value = await page.evaluate(async () => {
    return new Promise((resolve) => {
      chrome.storage.local.get('test-key', (items) => {
        resolve(items['test-key']);
      });
    });
  });
  console.log('Verified storage value:', value);

  // Clean up test data
  await page.evaluate(async () => {
    return new Promise((resolve) => {
      chrome.storage.local.remove(['test-key', 'test-config'], () => {
        resolve(true);
      });
    });
  });

  await page.close();
}
```

---

## 8. Multi-Tab Testing

Test that the extension works independently across multiple tabs.

```javascript
async function testMultiTab(context) {
  const page1 = await context.newPage();
  await page1.goto('https://example.com', { waitUntil: 'load' });

  const page2 = await context.newPage();
  await page2.goto('https://example.org', { waitUntil: 'load' });

  // Verify extension is active on both tabs
  // (Check for content script side effects on each page)

  // Switch between tabs using bringToFront (see CDP pattern below)
  await page1.bringToFront();
  console.log('Page 1 is now active');

  await page2.bringToFront();
  console.log('Page 2 is now active');

  await page1.close();
  await page2.close();
}
```

---

## 9. CDP Session — bringToFront

For finer control over tab switching, use Chrome DevTools Protocol (CDP).

```javascript
async function bringPageToFront(page) {
  const client = await page.context().newCDPSession(page);
  await client.send('Page.bringToFront');
  await client.detach();
}

// Usage: needed when popup interaction must target the content page's tab
// e.g., set timer in popup -> verify timer appears on content page
async function testPopupContentInteraction(context, extensionId) {
  // 1. Open content page
  const contentPage = await context.newPage();
  await contentPage.goto('https://example.com', { waitUntil: 'load' });

  // 2. Open popup in a new tab
  const popupPage = await context.newPage();
  await popupPage.goto(`chrome-extension://${extensionId}/popup.html`);

  // 3. Bring content page to front (so popup messages target it)
  await bringPageToFront(contentPage);

  // 4. Trigger action in popup
  // await popupPage.click('button:has-text("获取数据")');

  // 5. Verify result on content page
  // await contentPage.waitForSelector('.xuanji-result', { timeout: 10000 });

  await popupPage.close();
  await contentPage.close();
}
```

---

## 10. Login State Reuse

Reuse an existing Chrome profile with login state for testing against
authenticated internal platforms.

```javascript
const path = require('path');

async function launchWithLoginState() {
  // Use existing profile with login state
  // WARNING: This will load the extension alongside existing profile extensions.
  // Use --disable-extensions-except to isolate.
  const userDataDir = '/Users/<user>/data/chrome/agent';  // existing profile
  const extensionPath = path.resolve(__dirname, '../../dist');

  const context = await chromium.launchPersistentContext(userDataDir, {
    channel: 'chromium',
    headless: false,
    args: [
      `--disable-extensions-except=${extensionPath}`,
      `--load-extension=${extensionPath}`,
    ],
  });

  // The context now has:
  // - Login cookies for *.alibaba-inc.com (from existing profile)
  // - The extension loaded (from --load-extension)

  return context;
}

// Navigate to authenticated platform
async function testAuthenticatedPlatform(context) {
  const page = await context.newPage();
  await page.goto('https://asiops.alibaba-inc.com/', { waitUntil: 'load' });

  // Verify login state
  const title = await page.title();
  console.log('Platform title:', title);
  // If title contains login prompt, login state was not preserved

  await page.close();
}
```

---

## 11. Network Mocking (Read-only Safety)

Per the project Constitution the extension is **read-only** toward internal platforms
and writes **only** to OSS. A real E2E collection sends live GET requests to
`*.alibaba-inc.com` and may write to OSS. Mock these at the context level so tests are
offline, deterministic, and never touch real storage. Reuse the fixtures under
`test/data/` (`asiops/`, `splc/`, `qianzhou/`).

```javascript
const fs = require('fs');
const path = require('path');

async function mockInternalNetwork(context) {
  // 1. Stub internal platform reads with recorded fixtures. Real fixtures include
  //    test/data/asiops/{app,product,template,version,version_manifest,workload}.json
  //    and test/data/splc/pageGoveDetails.json — pick the one matching the endpoint.
  await context.route(/.*(alibaba-inc\.com|aliyun-inc\.com)\/.*/, async (route) => {
    // Resolve from the project root (process.cwd()), since the test script runs from /tmp.
    const fixture = path.resolve(process.cwd(), 'test/data/asiops/app.json');
    if (fs.existsSync(fixture)) {
      return route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: fs.readFileSync(fixture, 'utf-8'),
      });
    }
    return route.fulfill({ status: 200, contentType: 'application/json', body: '{}' });
  });

  // 2. Intercept OSS writes so nothing is persisted to real buckets.
  await context.route(/.*\.aliyuncs\.com\/.*/, (route) => {
    // PUT/POST = write attempt — swallow it and return success.
    return route.fulfill({ status: 200, body: '' });
  });
}
```

> Call `mockInternalNetwork(context)` right after `launchPersistentContext`, before
> navigating or triggering any command. Only bypass mocking in a controlled, authorized
> smoke-test environment.

---

## Troubleshooting

### Extension not loaded

- Verify `EXTENSION_PATH` points to the build output containing `manifest.json`.
- Check that the build is up to date: `pnpm build:devel`.
- Ensure `channel: 'chromium'` is set (not `'chrome'` which uses branded Chrome).
- Check console output for Chrome errors about manifest parsing.

### Service worker not found

- MV3 service workers start asynchronously. Use `waitForEvent('serviceworker')`.
- If using MV2, look for `target.type() === 'service_worker'` in browser targets
  instead.
- Service workers auto-suspend after ~30s. Playwright handles this transparently —
  the same Worker object remains valid across suspend/restart.

### Popup page blank

- Some extensions load popup content dynamically. Use `waitUntil: 'networkidle'`.
- Check for JavaScript errors: `page.on('pageerror', (err) => console.log(err))`.
- Verify the extension ID is correct — it changes on each profile reset.

### Content script not injected

- Check `manifest.json` `content_scripts.matches` covers the target URL.
- Content scripts run at `document_end` by default (per this project's manifest).
  Wait for page load to complete before checking for injection.
- Content scripts execute in an isolated world — `page.evaluate()` cannot access
  their variables directly. Look for DOM side effects instead.
