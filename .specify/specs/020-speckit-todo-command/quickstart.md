# Quickstart — `/speckit.todo`

## 0. Prerequisites

- A Spec Kit workspace already initialized (`.specify/` present).
- One of the supported AI agents (Copilot, Claude Code, Qwen, opencode, Qoder, Hermes, iFlow) with the `/speckit.*` command set available.

---

## 1. Add a marked TODO block

Create `src/auth/login.md` with a fenced `SPECKIT TODO` block:

```markdown
# Login Service

Current implementation uses legacy session tokens.

```SPECKIT TODO
Migrate session store to the new refresh-token schema:
- Update the login endpoint to return both access_token and refresh_token
- Modify session validation middleware to check refresh_token rotation
- Update unit tests in tests/auth/test_login.py
- Update integration tests in tests/integration/test_session_flow.py
```

The endpoint currently lives in src/auth/endpoints/login.py.
```

The opening fence line must contain the exact substring `SPECKIT TODO` (case-sensitive). The block body contains your actionable work instruction.

---

## 2. Add a second block in another file

Create `docs/deploy.md` with another block:

```markdown
# Deployment Guide

Production runs on Kubernetes 1.28.

```SPECKIT TODO
Bump the deployment target to Kubernetes 1.30:
- Update k8s/production/deployment.yaml apiVersion from apps/v1beta2 to apps/v1
- Update CI pipeline in .github/workflows/deploy.yml to use kubectl v1.30
- Update README.md version references
- Verify compatibility with current ingress controller
```

Staging environment already runs 1.30 successfully.
```

Now you have two TODO blocks in two different files. The command will group them by topic during planning.

---

## 3. Trigger the command

Open your AI agent's chat interface and run:

```
/speckit.todo
```

No arguments needed. The command scans the workspace, discovers all marked blocks, and generates a grouped execution plan.

---

## 4. Review the generated plan

The agent responds with a structured plan:

```markdown
## /speckit.todo — Execution Plan

**Discovery summary**: 2 blocks discovered, 2 files scanned, 0 malformed.

---

### Group A — Authentication service (2 blocks)

**Source files**:
- `src/auth/login.md` (lines 5–12)
- `docs/deploy.md` (lines 4–10)

**Planned work**:

1. **Migrate session store to refresh-token schema**
   - Source: `src/auth/login.md`
   - Outcome: Update login endpoint to return access_token + refresh_token, modify validation middleware, update unit and integration tests
   - Safety: Modifies authentication logic; requires test coverage verification
   - Validation: Run `pytest tests/auth/test_login.py tests/integration/test_session_flow.py`

2. **Bump Kubernetes deployment target to 1.30**
   - Source: `docs/deploy.md`
   - Outcome: Update deployment manifest apiVersion, CI pipeline kubectl version, README references, verify ingress compatibility
   - Safety: Production deployment change; staging already validated
   - Validation: Run `kubectl apply --dry-run=client -f k8s/production/deployment.yaml`

---

### Review & confirm

Reply `yes` to execute both items, or `skip 1` to defer the first item.
```

Read the plan carefully. The command groups related work (both items touch authentication/deployment concerns) and provides source references, intended outcomes, safety notes, and validation steps.

---

## 5. Confirm and execute

Reply with one of:

- `yes` — execute all items in the plan
- `execute` — same as yes
- `confirm batch 1` — explicit batch confirmation (used when >10 blocks trigger batching)
- `skip 1` — defer item 1, execute the rest
- `no` — cancel execution

**Example confirmation**:

```
yes
```

**Agent execution**:

```markdown
## Executing plan (2 items)

**Item 1/2**: Migrate session store to refresh-token schema
- Modified: `src/auth/endpoints/login.py` (updated response structure to include refresh_token)
- Modified: `src/auth/middleware/session_validator.py` (added refresh_token rotation check)
- Modified: `tests/auth/test_login.py` (updated 3 test cases for new token format)
- Modified: `tests/integration/test_session_flow.py` (added refresh_token rotation test)
- Validation: `pytest tests/auth/test_login.py tests/integration/test_session_flow.py` ✓ passed

**Item 2/2**: Bump Kubernetes deployment target to 1.30
- Modified: `k8s/production/deployment.yaml` (apiVersion updated to apps/v1)
- Modified: `.github/workflows/deploy.yml` (kubectl version pinned to 1.30)
- Modified: `README.md` (updated version references)
- Created: `docs/k8s-1.30-compatibility.md` (ingress controller compatibility notes)
- Validation: `kubectl apply --dry-run=client -f k8s/production/deployment.yaml` ✓ passed

✓ Plan complete: 2/2 items executed successfully.
```

The agent applies changes to each affected file and runs the specified validation commands.

---

## 6. Verify the result

After execution, verify the work:

- [ ] Run the affected tests: `pytest tests/auth/` and `pytest tests/integration/test_session_flow.py`
- [ ] Inspect modified files: `git diff src/auth/endpoints/login.py k8s/production/deployment.yaml`
- [ ] Re-run `/speckit.todo` — the plan should report "0 blocks discovered" (the TODO markers remain in your files, but the command tracks execution state)
- [ ] Commit the changes: `git add -A && git commit -m "feat: refresh-token schema + k8s 1.30 upgrade"`

If any validation failed during execution, the agent will have reported the failure and stopped. Fix the issue manually, then re-run `/speckit.todo` to retry the failed item.

---

## 7. Edge cases worth knowing

- **Malformed blocks**: If a TODO block is missing its closing fence, the command reports the file and approximate line number, then excludes it from execution. Fix the fence syntax and re-run.

- **More than 10 blocks**: The command batches them into groups of 10 and asks for confirmation per batch (`confirm batch 1`, `confirm batch 2`, etc.). This prevents overwhelming the agent with too many simultaneous changes.

- **Destructive or out-of-scope TODOs**: If a TODO block appears to request destructive operations (e.g., `rm -rf /`, dropping production databases) or secret-exposing changes, the command rejects the item and explains why. Edit the TODO to be more specific or break it into safer steps.

- **Mixed-case markers do NOT match**: Only the exact substring `SPECKIT TODO` (all caps, with a space) is recognized. `speckit todo`, `Speckit Todo`, or `SPECKIT-TODO` will be ignored.

- **No TODO blocks found**: If the workspace contains no marked blocks, the command reports "0 blocks discovered" and performs no planning work. Add a TODO block and re-run.
