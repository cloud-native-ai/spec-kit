---
id: "20260810T092231Z-speckit-skills"
unit_id: "/speckit.skills"
unit_type: "command"
run_id: "create-docs-hugo-layer-20260810"
scope: "local"
feature: "037"
partial: false
created: "2026-08-10T09:22:31Z"
summary: "improve path on create-docs: added a Hugo presentation layer so the Markdown library publishes as a static site. docs/ doubles as the Hugo project root with content mounted-never-copied (index.md -> _"
---

## Review
improve path on create-docs: added a Hugo presentation layer so the Markdown library publishes as a static site. docs/ doubles as the Hugo project root with content mounted-never-copied (index.md -> _index.md branch-bundle remaps + Markdown-excluding static mounts for media), repo-native relative .md/image links resolved by render hooks, deterministic scaffold-hugo.py (scaffold/check/mounts/build; stdlib-only; zero-churn; never clobbers user edits), skill assets/reference, contract C-13..C-17, and CI delivered as documentation guidance per the user's decision. Verified end-to-end: 17 new tests green incl. a real hugo v0.141.0 build; dogfooded on spec-kit's own docs (82 pages, docs-utils validate zero new violations); full suite diffed against a pristine HEAD baseline (44 baseline vs 38 current failures) proving zero new failures, with the two apparent regressions traced to test-suite self-pollution (__pycache__ / .migration-backups) and reproduced on the untouched baseline.

## Optimization Points
- Re-verify a "tool is absent" verdict before designing around it: the first `hugo version` probe returned "command not found" (PATH-less shell), which nearly drove a build-less design; `command -v hugo` in the next call found /usr/local/bin/hugo v0.141.0. Rule for this command: confirm negative environment probes with `command -v` (and check the user's stated premise) before treating a capability as unavailable.
- Structural checks cannot replace running the real pipeline for third-party config semantics. Three defects surfaced only from live Hugo runs: (1) the `[uglyURLs]` per-kind map is silently ignored by Hugo 0.141 (fixed by resolving links through the page graph in a render hook instead); (2) relative image paths break under pretty URLs (fixed with an image render hook + Markdown-excluding static mounts); (3) a no-op re-run rewrote hugo.toml on a trailing-newline diff, violating the anti-churn rule (fixed by comparing only the managed block). Extend the existing end-to-end lesson explicitly to "assume nothing about an external tool's config key without a live run".
- Dogfooding on the real docs/ tree found a latent content defect that no structural test covered: 17 imported `theme={null}` code-fence artifacts in docs/reference/skills/specification.md broke the build. Site-layer work should always be validated against the project's own documentation, not only synthetic fixtures.
- token-efficiency: reading docs-utils.py in full (429 lines) was the justified edit-target read and established that the site layer needs zero engine changes (no `.md` added, so validate is untouched); the layouts/CSS were shipped as skill assets driven by a deterministic script rather than re-derived by the LLM on each run, removing recurring HTML-generation cost from every future docs run.
