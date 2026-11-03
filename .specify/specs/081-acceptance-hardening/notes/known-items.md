# Review-Fix Item Dispositions — Feature 081, slice 081a

**What this file is**: the disposition of the review findings this fix deliberately did **not** turn
into code changes — plus the one that was cheap enough to fix. A finding recorded as "known" is a
finding someone owns later; a finding silently dropped is indistinguishable from one that was never
found, which is the failure mode this file exists to prevent.

**What it is not**: an acceptance claim, or a substitute for the finding's own severity. Two of the
three below are owned by a later slice of the same feature line, and the third is a mechanism with a
cost, not a defect with a fix inside this slice's scope.

| # | Finding | Disposition | Owner / mechanism |
|---|---------|-------------|-------------------|
| F12 | the smoke test rewrites a **tracked** evidence file | **recorded, no change** — the mechanism is intended | `tests/integration/test_acceptance_smoke.py` writes `.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt` on every successful run, and that path is tracked by git. The rewrite is **byte-identical** across runs (the smoke module states this; measured in 081c: the file's sha256 is unchanged and `git status` stays clean), so a clean tree is the expected reading and a **dirty** file means a sub-check's output moved — the signal, not routine drift. The alternative — writing to a gitignored path — would make the evidence unreachable to a reviewer of a committed tree, which is why the tracked path was chosen. Recorded so the dirt is read as evidence, not as drift; made visible in `quickstart.md` S8's premise (2). |
| F13 | `get_resource_path()`'s repo-root fallback (`MODULE_DIR.parent.parent`) | **fixed — one-line guard** | The fallback now also requires `<repo_root>/src/specify_cli/__init__.py`. "A grandparent that happens to carry `templates/`" is not the same fact as "this is the source checkout", and only the second licenses treating that directory as the repository root. Measured after the change: `get_resource_path()` still resolves to the checkout and `has_local_templates()` is `True`. |
| F14 | the implement-site gate is **prose + a test**, with no runtime enforcement on a real run | **deferred — 081d** | 081a's implement-site wiring is a command-template bullet plus the contract test that pins it (`tests/contract/test_gate_wiring_081.py`), which makes an *unwired* template red but cannot make a *skipped* invocation red. The runtime side of that question is `--audit-existing`'s territory (FR-020), a 081d deliverable: an audit over existing features is the first surface that can observe whether the judgement actually ran. Recording it here keeps "the gate exists" (081a, true) distinct from "the gate cannot be bypassed silently" (081d). |

## Why none of these blocks the slice's closure

Each is a statement about *how much* a wired gate proves, not about whether the slice's own claims
hold. `SC-001` is recorded `blocked` at 1/3 call sites and `SC-002` at `partial` precisely so that
this distinction stays visible: the slice delivers the implement call site and its test, and the
feature is not called `Implemented` on the strength of it.
