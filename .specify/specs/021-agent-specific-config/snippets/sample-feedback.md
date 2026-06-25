# Agent Execution Feedback

**Source**: browser-utils
**Agent**: claude-code
**Timestamp**: 2026-06-25T14:30:00
**Outcome**: success-with-workaround

## Obstacle

WebFetch tool does not support `file://` URLs for local HTML testing. When attempting to validate a locally generated HTML file using the browser-utils skill, the `WebFetch` tool returned an error because it only supports `http://` and `https://` URLs.

## Workaround Applied

Used Playwright via the `Bash` tool instead of `WebFetch` to open and interact with the local HTML file. The Playwright script was written to `/tmp/playwright-test-local.js` and executed with `node run.js`.

## Suggested Improvement

Add a note in `skills/browser-utils/references/claude-code-guide.md` under Known Pitfalls documenting that `file://` URLs require Playwright, not `WebFetch`. Suggest a standard Playwright snippet for local file testing.
