---
id: "20260911T055209Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "improve-skills-browser-utils-focus-safe-20260911"
scope: "local"
probe: "skill-improve-skills-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-09-11T05:52:09Z"
summary: "Ran a full assisted improvement loop on skills/browser-utils for a user-passed requirement (automation browser windows must not contend for system focus). The loop's own discipline held where it matte"
---

## Review
Ran a full assisted improvement loop on skills/browser-utils for a user-passed requirement (automation browser windows must not contend for system focus). The loop's own discipline held where it mattered: research-before-edit produced a note that every keep/change decision traced to; the canonical owner was correctly resolved to skills/ (framework source) rather than the .specify/skills mirror, and mirrors were regenerated through sync-mirrors.py rather than hand-edited; new detail landed in L2/L3 (one new reference + one new deterministic probe script) while SKILL.md gained only a rewritten Strict Requirement, two Resources entries and one scoped convention, keeping skill-shape.py at exit 0 with body 4233/5000 tokens and no new findings; the duplicated and self-contradictory launch-mode claims in the claude-code and copilot guides were converted to pointers rather than re-worded. Verification was real, not asserted: the probe script was executed across all five resolution branches plus a reverse case and a usage-error case, its emitted F1 wrapper was run verbatim through bash against a real Playwright script, and the edited Mode 1 quickstart was extracted from the doc and run green. Contract tests went from a pre-change baseline of 1 failed / 68 passed to 69 passed. Two weaknesses surfaced in this skill's own gates and are filed as optimization points: Hard Constraint 7 fired too late for an API name written from memory into a new reference (page.accessibility.snapshot(), undefined on the installed Playwright 1.61.1, caught only by a dispatched subagent rather than by step 8), and the mandatory RED-GREEN pressure re-test was non-discriminative on this host because both arms chose headless for environment reasons, so it passed in form while proving nothing about focus theft.

## Optimization Points
- # Optimization points — improve-skills run (target: skill:browser-utils)
- ## Point 1 — Hard Constraint 7 fires too late for newly authored API claims
- **Observed**: this loop wrote a brand-new reference doc (`focus-safe-launch.md`) that named
- `page.accessibility.snapshot()` as an API that "works headless". The name was written from memory
- during the step-5 edit pass. It is wrong — `page.accessibility` is `undefined` on the installed
- Playwright 1.61.1, and it threw at runtime. The error was caught only because a dispatched
- GREEN pressure subagent happened to call it; step 8's own validation would not have caught it,
- since the gate as written checks that *changed snippets and scripts* run, and a prose sentence
- naming an API is neither a snippet nor a script.
- **Why the current wording permits it**: Hard Constraint 6 ("capability verified before it is
- documented") names "a delegation path, data table, or coverage claim" — an inline API name in a
- sentence matches none of those three shapes, so the constraint reads as not applicable. Constraint
- 7 then defers to "any snippet or script added/changed", which a prose API reference also escapes.
- The two constraints leave a gap exactly where the mistake happened.
- **Proposed change**: extend Hard Constraint 6's enumerated shapes to include *a named
- library/framework API, method, option, or flag*, and state the cheap deterministic check that
- discharges it — probe the installed version for existence (`typeof obj.method`, `--help`,
- `dir()`, `hasattr`) rather than reasoning about it. One sentence closes the gap without adding a
- step: naming an API in a doc is a capability claim, and capability claims are probed on the
- version actually installed.
- **Value**: this is the second class of "written from memory, false on the installed version"
- defect in this skill's domain (the first being a nonexistent CLI flag, `--start-minimized`, which
- a `strings` probe caught before it was documented). Both were caught by probing; only one was
- caught before publication.
- ## Point 2 — Step 8 mandates a pressure re-test but not a discriminative one
- **Observed**: the behavior-changing edit triggered the mandatory RED-GREEN pressure re-test. Both
- arms chose `chromium.launch({ headless: true })`. RED chose it because the host has no `$DISPLAY`
- and a window is therefore physically impossible — it never encountered the trade-off the edit
- governs. The test passed in form and proved nothing about the target behaviour, because the harm
- (window focus theft) is unobservable on a headless container.
- **Why the current wording permits it**: `create-skills/references/pressure-testing.md` requires
- "a pass requires observed compliance, not a plausibility argument", but it never requires that the
- scenario be *capable* of distinguishing RED from GREEN on the host it runs on. A loop can satisfy
- every letter of the method with a scenario whose discriminating observation the environment cannot
- produce, and report a green pressure test.
- **Proposed change**: add to the pressure-testing method a pre-dispatch requirement — before
- dispatching, state the single observation that would distinguish a non-compliant RED from a
- compliant GREEN, and confirm this host can actually produce it. When it cannot, declare the test
- **inconclusive** and say which environment would discriminate, rather than reporting a pass. The
- RED step already contains the seed of this ("if the subagent already behaves correctly without the
- skill, the skill may be unnecessary — surface this"), but that branch attributes a null result to
- the skill being unneeded, when the more common cause is that the scenario cannot discriminate.
- **Value**: prevents a null pressure test from being laundered into evidence of improvement, which
- directly protects the "no claim of fixed without before/after" constraint this skill already holds.
