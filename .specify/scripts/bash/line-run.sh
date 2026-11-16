#!/usr/bin/env bash
# line-run.sh — register a line, run one command, close the line (feature 102).
#
# Semantics and the exit-status table are owned by the contract
# `.specify/specs/102-line-registry-registration/contracts/line-run.contract.md` (C-01…C-19).
# The registration criterion — when a long task MUST use this wrapper — is owned by
# `shared/guidelines/reporting-obligations.md` § 九; this file implements the carrier only.
#
# Registry writes go only through the engine `line-registry.py`. This wrapper writes no state
# itself, keeps no heartbeat file and installs no signal trap: it emits exactly two engine
# events (the registration and the close), so a wrapper killed by an uncatchable signal leaves
# its entry `active` and the digest reports it instead of showing nothing-running.
#
# Usage: line-run.sh --line-id <slug> --run-id <id> -- <command> [args...]
#
# side-effects: registers the composed id `<line-id>-<run-id>` as active through the engine,
#   then runs the command with inherited stdin/stdout/stderr/cwd/environ and closes the line as
#   `completed` (child exit 0) or `failed` (any other status); the answering flags write nothing.
# exit-codes: 0 the command succeeded and the line closed; <N> the command's own status; the
#   engine's status when registration is refused or the close fails with the child at 0; 2 a
#   usage error; 4 no git toplevel or no readable engine.

set -u

SCRIPT_DIR="$(CDPATH="" cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# script-interface: the sourceable guard block (086) lives in script-interface.sh and sits
# above this file's own parsing and above every read and write, which is what keeps `-h`,
# `--help` and `--version` free of side effects.
# Authority: shared/definitions/script-interface-definitions.md section 4.
SCRIPT_INTERFACE_LIB="$SCRIPT_DIR/script-interface.sh"
if [ -f "$SCRIPT_INTERFACE_LIB" ]; then
    # shellcheck source=/dev/null
    . "$SCRIPT_INTERFACE_LIB"
    script_interface_guard entry
    script_interface_guard define name="$0" \
        usage="--line-id <slug> --run-id <id> -- <command> [args...]" \
        effects="registers <line-id>-<run-id> as active through line-registry.py, runs the command, then closes the line as completed or failed; the flags write nothing" \
        codes="0 the command succeeded and the line closed; N the command's own status; the engine status when registration or close fails; 2 a usage error; 4 no git toplevel or no readable engine" \
        -- --line-id --run-id
    script_interface_guard guard "$@"
fi

usage_error() {
    printf 'error: line-run.sh: %s\n' "$1" >&2
    printf 'usage: line-run.sh --line-id <slug> --run-id <id> -- <command> [args...]\n' >&2
    exit 2
}

line_id=""
run_id=""
have_separator=0

while [ "$#" -gt 0 ]; do
    case "$1" in
        --)
            have_separator=1
            shift
            break
            ;;
        --line-id)
            [ "$#" -ge 2 ] || usage_error "missing value for --line-id"
            [ "$2" = "--" ] && usage_error "missing value for --line-id"
            line_id="$2"
            shift 2
            ;;
        --run-id)
            [ "$#" -ge 2 ] || usage_error "missing value for --run-id"
            [ "$2" = "--" ] && usage_error "missing value for --run-id"
            run_id="$2"
            shift 2
            ;;
        *)
            usage_error "unexpected argument: $1"
            ;;
    esac
done

[ "$have_separator" -eq 1 ] || usage_error "missing the bare -- separator"
[ "$#" -gt 0 ] || usage_error "empty command after --"
[ -n "$line_id" ] || usage_error "--line-id is required"
[ -n "$run_id" ] || usage_error "--run-id is required"

# Identity (C-06): the repository toplevel, never the caller's $PWD.
project_root="$(git rev-parse --show-toplevel 2>/dev/null)" || project_root=""
if [ -z "$project_root" ]; then
    printf 'error: line-run.sh: cannot resolve the git toplevel of the working directory\n' >&2
    printf 'line-run.sh: the line was not registered and the command was not run\n' >&2
    exit 4
fi

# Engine resolution (C-07 / A-17): the wrapper's own ../.., moved up one level when that
# directory is the framework's runtime projection `.specify`. Two ordered candidates, first
# readable wins; a PATH lookup or a third candidate is never used.
repo_root="$(CDPATH="" cd "$SCRIPT_DIR/../.." 2>/dev/null && pwd)" || repo_root=""
if [ -z "$repo_root" ]; then
    printf 'error: line-run.sh: cannot resolve the repository root from %s\n' "$SCRIPT_DIR" >&2
    exit 4
fi
if [ "${repo_root##*/}" = ".specify" ]; then
    repo_root="$(CDPATH="" cd "$repo_root/.." && pwd)"
fi

engine_candidate_1="$repo_root/skills/external/sdd-loop-driver/scripts/line-registry.py"
engine_candidate_2="$repo_root/.specify/skills/sdd-loop-driver/scripts/line-registry.py"

if [ -r "$engine_candidate_1" ]; then
    engine="$engine_candidate_1"
elif [ -r "$engine_candidate_2" ]; then
    engine="$engine_candidate_2"
else
    printf 'error: line-run.sh: no readable registry engine; tried:\n  %s\n  %s\n' \
        "$engine_candidate_1" "$engine_candidate_2" >&2
    printf 'line-run.sh: the line was not registered and the command was not run\n' >&2
    exit 4
fi

composed_id="${line_id}-${run_id}"

# Register before the command starts, and fail closed: a refused registration means the run
# would be invisible, so the command must not run at all (C-08 / C-09).
register_payload="$(python3 "$engine" --action register \
    --line-id "$composed_id" --run-id "$run_id" \
    --project-dir "$project_root" --repo-root "$project_root" \
    --state active 2>&1)"
register_status=$?
if [ "$register_status" -ne 0 ]; then
    printf 'error: line-run.sh: register failed for %s (engine exit %s):\n' \
        "$composed_id" "$register_status" >&2
    printf '%s\n' "$register_payload" >&2
    printf 'line-run.sh: the command was not run\n' >&2
    exit "$register_status"
fi

# Execute (C-10): the command after `--` owns this process's stdio, cwd and environment, and
# its status is captured verbatim — never parsed, quoted or rewritten.
"$@"
child_status=$?

# Close with the one reason the contract's closed set names for each outcome (C-11 / C-12).
if [ "$child_status" -eq 0 ]; then
    close_reason="completed"
else
    close_reason="failed"
fi

close_payload="$(python3 "$engine" --action deregister \
    --line-id "$composed_id" --reason "$close_reason" 2>&1)"
close_status=$?

# A-24 / C-13 / C-14: the child's numeric result is never masked. When both sides fail, the
# child's status wins the exit code and the close failure is written to stderr; when only the
# close fails, its engine status becomes this wrapper's status.
if [ "$close_status" -ne 0 ]; then
    if [ "$child_status" -ne 0 ]; then
        printf 'error: line-run.sh: close failed for %s (engine exit %s) after the command exited %s:\n' \
            "$composed_id" "$close_status" "$child_status" >&2
        printf '%s\n' "$close_payload" >&2
        exit "$child_status"
    fi
    printf 'error: line-run.sh: close failed for %s (engine exit %s):\n' \
        "$composed_id" "$close_status" >&2
    printf '%s\n' "$close_payload" >&2
    exit "$close_status"
fi

exit "$child_status"
