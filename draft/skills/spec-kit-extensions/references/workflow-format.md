# Workflow format reference

Workflows are multi-step, **resumable** automation pipelines defined in YAML. The engine executes steps in order, dispatches commands to AI integrations, runs shell commands, evaluates control flow, and pauses at human review gates. State persists after each step, so a run resumes from the exact point of interruption. Installed under `.specify/workflows/<id>/workflow.yml`.

> Adapted from upstream `main:workflows/README.md`, `main:workflows/ARCHITECTURE.md`, `main:workflows/speckit/workflow.yml`.

## Manifest structure

```yaml
schema_version: "1.0"
workflow:
  id: "speckit"
  name: "Full SDD Cycle"
  version: "1.0.0"
  author: "GitHub"
  description: "Runs specify → plan → tasks → implement with review gates"

requires:
  speckit_version: ">=0.8.5"
  integrations:
    any: ["claude", "copilot", "gemini", "opencode"]   # advisory, non-exhaustive hint

inputs: {...}    # typed, coerced from CLI strings
steps: [...]     # ordered list of steps
```

`requires.integrations.any` is an **advisory** compatibility hint, not a closed set — the workflow runs against whatever integration the project was initialized with, as long as it provides the commands referenced in `steps`.

## Inputs

Inputs are type-checked and coerced from CLI string values:

```yaml
inputs:
  spec:
    type: string
    required: true
    prompt: "Describe what you want to build"
  task_count:
    type: number
    default: 5
  dry_run:
    type: boolean
    default: false
  scope:
    type: string
    default: "full"
    enum: ["full", "backend-only", "frontend-only"]
```

| Type | Accepts / coercion | Example |
|------|--------------------|---------|
| `string` | Pass-through | `"user-auth"` |
| `number` | `float()` → `int()` if whole | `"42"` → `42` |
| `boolean` | `true`/`1`/`yes` → `True`; `false`/`0`/`no` → `False` | `"true"` → `True` |
| `enum` | Validated against allowed values | `["full", "backend-only"]` |

Missing required inputs raise an error. Fields with `default` use it when unset. Provide values on the CLI: `--input spec="…" --input scope="backend-only"`.

## The 11 step types

`command` is the default type (an entry with a `command:` key and no `type:`). All others set `type:`.

### command (default)

Invoke an installed `speckit.*` command via the integration CLI.

```yaml
- id: specify
  command: speckit.specify
  input:
    args: "{{ inputs.spec }}"
  integration: claude                    # optional: override workflow default
  model: "claude-sonnet-4-20250514"      # optional: override model
```

### prompt

Send an arbitrary inline prompt — no command file needed.

```yaml
- id: security-review
  type: prompt
  prompt: "Review {{ inputs.file }} for security vulnerabilities"
  integration: claude
```

### shell

Run a shell command and capture output (`steps.<id>.output.exit_code`, `.stdout`, `.stderr`).

```yaml
- id: run-tests
  type: shell
  run: "cd {{ inputs.project_dir }} && npm test"
```

### init

Bootstrap a project like `specify init` (scaffolds templates, scripts, agent integration). Runs non-interactively (`--ignore-agent-tools`).

```yaml
- id: bootstrap
  type: init
  here: true                       # or: project: my-project
  integration: copilot             # optional: defaults to workflow integration
  integration_options: "--skills"  # optional
  script: sh                       # optional: sh or ps
  force: true                      # optional: needed if target dir exists
  preset: healthcare-compliance    # optional preset id
```

### gate

Pause for human review. The run resumes on `specify workflow resume`.

```yaml
- id: review-spec
  type: gate
  message: "Review the generated spec before planning."
  options: [approve, edit, reject]
  on_reject: abort
```

### if

Conditional branching. Returns nested `next_steps`.

```yaml
- id: check-scope
  type: if
  condition: "{{ inputs.scope == 'full' }}"
  then:
    - id: full-plan
      command: speckit.plan
  else:
    - id: quick-plan
      command: speckit.plan
      options: { quick: true }
```

### switch

Multi-branch dispatch on an expression value.

```yaml
- id: route
  type: switch
  expression: "{{ steps.review.output.choice }}"
  cases:
    approve:
      - id: plan
        command: speckit.plan
    reject:
      - id: log
        type: shell
        run: "echo 'Rejected'"
  default:
    - id: fallback
      type: gate
      message: "Unexpected choice"
```

### while

Repeat while a condition is truthy.

```yaml
- id: retry
  type: while
  condition: "{{ steps.run-tests.output.exit_code != 0 }}"
  max_iterations: 5
  steps:
    - id: fix
      command: speckit.implement
```

### do-while

Run the body at least once, then repeat while the condition holds.

```yaml
- id: refine
  type: do-while
  condition: "{{ steps.review.output.choice == 'edit' }}"
  max_iterations: 3
  steps:
    - id: revise
      command: speckit.specify
```

### fan-out

Dispatch a step template for each item in a collection (sequential).

```yaml
- id: parallel-impl
  type: fan-out
  items: "{{ steps.tasks.output.task_list }}"
  max_concurrency: 3
  step:
    id: impl
    command: speckit.implement
```

Inside a fan-out, `{{ item }}` is the current iteration item.

### fan-in

Aggregate results from a fan-out.

```yaml
- id: collect
  type: fan-in
  wait_for: [parallel-impl]
  output: {}
```

Inside a fan-in, `{{ fan_in }}` holds the aggregated results.

### Step-type summary

| Type | Purpose | Returns `next_steps`? |
|------|---------|-----------------------|
| `command` | Invoke a `speckit.*` command | No |
| `prompt` | Inline prompt to integration | No |
| `shell` | Run shell, capture output | No |
| `init` | Bootstrap a project | No |
| `gate` | Human review checkpoint | No (pauses) |
| `if` | Conditional then/else | Yes |
| `switch` | Multi-branch dispatch | Yes |
| `while` | Loop while truthy | Yes (if true) |
| `do-while` | Loop, body ≥ 1× | Yes (always) |
| `fan-out` | Per-item dispatch | No (engine expands) |
| `fan-in` | Aggregate fan-out results | No |

## `{{ }}` expressions

Definitions use Jinja2-like `{{ expression }}` syntax. A lone `{{ expr }}` returns a typed value; a mixed string (`"text {{ expr }} more"`) returns an interpolated string.

| Feature | Example |
|---------|---------|
| Input access | `{{ inputs.spec }}` |
| Step outputs | `{{ steps.specify.output.file }}` |
| Comparisons | `{{ steps.run-tests.output.exit_code != 0 }}` (`==`, `!=`, `>`, `<`, `>=`, `<=`) |
| Boolean logic | `{{ items and status == 'ok' }}` (`and`, `or`, `not`) |
| Membership | `{{ 'error' not in status }}` |
| Literals | `{{ true }}`, `{{ [1, 2] }}` |

### Namespace

| Key | Source | Available when |
|-----|--------|----------------|
| `inputs` | Resolved workflow inputs | Always |
| `steps` | Accumulated step results | After first step |
| `item` | Current iteration item | Inside fan-out |
| `fan_in` | Aggregated results | Inside fan-in |
| `context.run_id` | Current run id (8-char hex or operator id; empty outside a run) | Always |

### Filters

`default`, `join`, `contains`, `map`, `from_json`:

```yaml
message: "{{ status | default('pending') }}"
list:    "{{ items | join(', ') }}"
check:   "{{ text | contains('sub') }}"
parsed:  "{{ steps.emit.output.stdout | from_json }}"
```

## Gates and `on_reject`

A gate pauses the run. Both `approve` and `reject` return `COMPLETED`; `on_reject` controls only what happens on reject:

| `on_reject` | Behavior |
|-------------|----------|
| `abort` (default) | Reject → `FAILED` with `output.aborted = True`, halts the run. |
| `skip` | Reject → `COMPLETED`; the run continues. The **author** must branch downstream on `{{ steps.<gate-id>.output.choice }}` — `skip` does not auto-skip sibling steps. |
| `retry` | Reject → `PAUSED`; the next `specify workflow resume` re-runs the gate. |

Gates never automatically re-run a failed step; express retries via custom gate options + downstream branching, or by wrapping the failing step in a loop. In CI (non-interactive), a gate pauses the run for later resume.

## Error handling

By default any step returning `FAILED` (commonly a non-zero `shell`/`command` exit) halts the run. Set `continue_on_error: true` to record the result and continue to the next sibling:

```yaml
- id: heavy-thing
  type: command
  command: speckit.heavy-thing
  continue_on_error: true

- id: check-result
  type: if
  condition: "{{ steps.heavy-thing.output.exit_code != 0 }}"
  then:
    - id: review
      type: gate
      message: "Step failed (exit {{ steps.heavy-thing.output.exit_code }}). Approve to recover."
      on_reject: skip
```

Notes:
- The flag must be a **literal** boolean (`true`/`false`); coerced strings like `"true"` are rejected at validation.
- Scope is **returned failures only** (`status=FAILED`). Unhandled exceptions raised out of a step abort the run regardless — a step must catch and return `FAILED` with the failure encoded in `output` for the flag to cover it.
- Gate aborts (`on_reject: abort`) always halt; `continue_on_error` does not override deliberate operator decisions.
- Structural validation runs up front — invalid definitions are rejected before a run is created.

## State persistence and resume

Every run persists to `.specify/workflows/runs/<run_id>/` (`state.json`, `inputs.json`, `log.jsonl`). Lifecycle:

```
created → running → completed | paused | failed | aborted
              ↑___________________|  (resume re-enters running)
```

```bash
specify workflow status            # list all runs with status
specify workflow status <run_id>   # inspect one run
specify workflow resume <run_id>   # resume a paused gate, or retry from a failed step
```

Resume tracking is at the **top-level step index** only. If a nested step (inside `if`/`switch`/`while`) pauses, resume re-runs the parent control-flow step and its nested body (exact nested resume is a planned enhancement).

## Running & catalog

```bash
specify workflow search
specify workflow add speckit
specify workflow run speckit --input spec="Build a user auth system with OAuth"
specify workflow run ./workflow.yml --input spec="…" --input scope="backend-only"
specify workflow info speckit
specify workflow catalog list
```

| Variable | Effect |
|----------|--------|
| `SPECKIT_WORKFLOW_CATALOG_URL` | Replace the catalog URL (all defaults). |

| Config file | Scope |
|-------------|-------|
| `.specify/workflow-catalogs.yml` | Project catalog stack. |
| `${HOME}/.specify/workflow-catalogs.yml` | User catalog stack. |
