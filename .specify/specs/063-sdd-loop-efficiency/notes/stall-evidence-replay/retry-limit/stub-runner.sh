#!/usr/bin/env bash
set -u
scenario="$1"
dir="$2"
attempt="$3"
printf 'pid=%s at=%s\n' "$$" "$(date +%s)" > "$dir/pid-$attempt"
printf '%s' "$(date +%s)" > "$dir/heartbeat-$attempt"
: > "$dir/log-$attempt.log"
case "$scenario" in
  timeout)
    sleep "${STUB_TIMEOUT_SLEEP:-2}"
    printf 'runner_rc=124\n' > "$dir/runner-rc-$attempt"
    exit 124
    ;;
  retry-limit)
    printf 'exit=1 at=%s sentinel=0\n' "$(date +%s)" > "$dir/status-$attempt.tmp"
    mv "$dir/status-$attempt.tmp" "$dir/status-$attempt"
    printf 'runner_rc=1\n' > "$dir/runner-rc-$attempt"
    exit 1
    ;;
  fake-done)
    printf 'exit=0 at=%s sentinel=0\n' "$(date +%s)" > "$dir/status-$attempt.tmp"
    mv "$dir/status-$attempt.tmp" "$dir/status-$attempt"
    printf 'runner_rc=0\n' > "$dir/runner-rc-$attempt"
    exit 0
    ;;
  success)
    printf 'exit=0 at=%s sentinel=1\n' "$(date +%s)" > "$dir/status-$attempt.tmp"
    mv "$dir/status-$attempt.tmp" "$dir/status-$attempt"
    printf 'FIXTURE-DONE\n' > "$dir/log-$attempt.log"
    printf 'runner_rc=0\n' > "$dir/runner-rc-$attempt"
    exit 0
    ;;
  *)
    printf 'runner_rc=2\n' > "$dir/runner-rc-$attempt"
    exit 2
    ;;
esac
