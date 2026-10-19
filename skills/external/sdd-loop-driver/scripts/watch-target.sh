#!/usr/bin/env bash
# watch-target.sh — unified, read-only watch primitive for sdd-loop-driver.
#
# One call blocks for a bounded window, samples signals cheaply, and returns as
# soon as a terminal verdict is reached. Window expiry returns RUNNING, never
# TIMEOUT; only the stage deadline produces TIMEOUT.
#
# Signals are positive evidence only:
#   completion  = exact sentinel last line (necessary) or exit record rc=0
#   liveness    = pid file + kill -0 (plus /proc start-ticks / zombie check)
#   progress    = log tail; heartbeat proves the runner shell is alive
# Absence (process gone, pgrep zero matches, quiet log) is never completion.
#
# The watcher's watch path NEVER kills processes, writes project state, or
# mutates the tree; --self-test only cleans up its own fixtures.

set -u

SELF="$0"

EXIT_DONE=0
EXIT_RUNNING=10
EXIT_ANOMALY=11
EXIT_FAILED=12
EXIT_DEAD=13
EXIT_TIMEOUT=14
EXIT_INCOMPLETE=15
EXIT_NO_SIGNAL=16
EXIT_USAGE=2

usage() {
  cat <<'EOF'
watch-target.sh — bounded long-poll watcher (read-only)

Single target:
  watch-target.sh --label L --pid-file P --status-file S --log G \
                  [--sentinel STAGE-DONE] [--heartbeat H] \
                  [--hook-fifo F | --hook-done F] \
                  [--deadline-epoch E | --timeout T] \
                  [--window N] [--interval N] [--start-grace N] \
                  [--heartbeat-max-age N] [--once] [--verbose]

Manifest (one target per line: label|pid|status|log|sentinel|heartbeat|deadline):
  watch-target.sh --manifest FILE [--window N] [--interval N] [--start-grace N]

  Use '-' for an empty manifest field. Paths must not contain '|'.
  In manifest mode, every line is reported and the exit code is the highest
  severity among terminal verdicts.

Verdicts / exit codes:
  0 DONE           sentinel or clean exit record; still requires independent U4 check
  10 RUNNING       no terminal signal; re-enter another window immediately
  11 ANOMALY       final line is ANOMALY: ... (process ended / exit record present)
  12 FAILED        exit record has non-zero rc
  13 DEAD          pid recorded but process dead, zombie, or pid reused
  14 TIMEOUT       stage deadline reached (the only timeout source)
  15 INCOMPLETE    exit rc=0 but sentinel missing (fake-done candidate)
  16 NO_SIGNAL     no pid/status within start grace
  2 USAGE          bad arguments

Defaults: window=300s, interval=3s, start-grace=30s, heartbeat-max-age=120s.
Set the host tool timeout to window + 30s so the watcher can return first.
--timeout T is relative to THIS invocation; for multi-window stages pass
--deadline-epoch (absolute stage deadline) instead, or each window resets it.
The watcher must run as the same identity as the runner (kill -0 permission).
--hook-fifo F: block on F for each interval instead of sleep; a line is an
              early completion signal only (hook=observed), never a verdict.
--hook-done F: a non-empty F is a persistent early signal (same rule).
Both are supplementary: sentinel/status/exit-record remain authoritative.
--self-test runs zero-match / dead / zombie / pid-reuse / fake-done /
anomaly / exit-code / timeout / hook / manifest regression cases.
EOF
}

die_usage() {
  printf 'watch-target: %s\n' "$*" >&2
  usage >&2
  exit "$EXIT_USAGE"
}

is_uint() {
  case "${1:-}" in
    ''|*[!0-9]*) return 1 ;;
    *) return 0 ;;
  esac
}

now_epoch() { date +%s; }

file_mtime() {
  stat -c %Y "$1" 2>/dev/null || stat -f %m "$1" 2>/dev/null || echo 0
}

one_line() {
  printf '%s' "${1:-}" | tr '\n\r' '  ' | cut -c1-300
}

LABEL="line"
PID_FILE=""
STATUS_FILE=""
LOG_FILE=""
SENTINEL=""
HEARTBEAT=""
DEADLINE_EPOCH=0
TIMEOUT=""
WINDOW=300
INTERVAL=3
START_GRACE=30
HEARTBEAT_MAX_AGE=120
HOOK_FIFO=""
HOOK_DONE=""
HOOK_EVENT_SEEN=0
ONCE=0
MANIFEST=""
VERBOSE=0
SELF_TEST=0
START_EPOCH=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --label) [ "$#" -ge 2 ] || die_usage "--label needs a value"; LABEL="$2"; shift 2 ;;
    --pid-file) [ "$#" -ge 2 ] || die_usage "--pid-file needs a value"; PID_FILE="$2"; shift 2 ;;
    --status-file) [ "$#" -ge 2 ] || die_usage "--status-file needs a value"; STATUS_FILE="$2"; shift 2 ;;
    --log) [ "$#" -ge 2 ] || die_usage "--log needs a value"; LOG_FILE="$2"; shift 2 ;;
    --sentinel) [ "$#" -ge 2 ] || die_usage "--sentinel needs a value"; SENTINEL="$2"; shift 2 ;;
    --heartbeat) [ "$#" -ge 2 ] || die_usage "--heartbeat needs a value"; HEARTBEAT="$2"; shift 2 ;;
    --hook-fifo) [ "$#" -ge 2 ] || die_usage "--hook-fifo needs a value"; HOOK_FIFO="$2"; shift 2 ;;
    --hook-done) [ "$#" -ge 2 ] || die_usage "--hook-done needs a value"; HOOK_DONE="$2"; shift 2 ;;
    --deadline-epoch) [ "$#" -ge 2 ] || die_usage "--deadline-epoch needs a value"; DEADLINE_EPOCH="$2"; shift 2 ;;
    --timeout) [ "$#" -ge 2 ] || die_usage "--timeout needs a value"; TIMEOUT="$2"; shift 2 ;;
    --window) [ "$#" -ge 2 ] || die_usage "--window needs a value"; WINDOW="$2"; shift 2 ;;
    --interval) [ "$#" -ge 2 ] || die_usage "--interval needs a value"; INTERVAL="$2"; shift 2 ;;
    --start-grace) [ "$#" -ge 2 ] || die_usage "--start-grace needs a value"; START_GRACE="$2"; shift 2 ;;
    --heartbeat-max-age) [ "$#" -ge 2 ] || die_usage "--heartbeat-max-age needs a value"; HEARTBEAT_MAX_AGE="$2"; shift 2 ;;
    --manifest) [ "$#" -ge 2 ] || die_usage "--manifest needs a value"; MANIFEST="$2"; shift 2 ;;
    --once) ONCE=1; shift ;;
    --verbose) VERBOSE=1; shift ;;
    --self-test) SELF_TEST=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) die_usage "unknown argument: $1" ;;
  esac
done

for name in WINDOW INTERVAL START_GRACE HEARTBEAT_MAX_AGE; do
  value="${!name}"
  is_uint "$value" || die_usage "$name must be a non-negative integer, got '$value'"
done
[ "$INTERVAL" -gt 0 ] || die_usage "--interval must be > 0"
if [ -n "$MANIFEST" ] && { [ -n "$HOOK_FIFO" ] || [ -n "$HOOK_DONE" ]; }; then
  die_usage "hook flags are single-target only"
fi
if [ -n "$TIMEOUT" ]; then
  is_uint "$TIMEOUT" || die_usage "--timeout must be a non-negative integer"
  [ "$DEADLINE_EPOCH" -eq 0 ] || die_usage "use either --timeout or --deadline-epoch, not both"
fi
is_uint "$DEADLINE_EPOCH" || die_usage "--deadline-epoch must be a non-negative integer"

P_PID=""
P_START=""

read_pid_file() {
  local f="$1" pid="" start=""
  P_PID=""; P_START=""
  [ -n "$f" ] && [ -f "$f" ] || return 0
  pid=$(sed -n 's/^pid=\([0-9][0-9]*\).*/\1/p' "$f" | head -n 1)
  start=$(sed -n 's/.*start=\([0-9][0-9]*\).*/\1/p' "$f" | head -n 1)
  if [ -z "$pid" ]; then
    pid=$(awk 'NR==1{print $1}' "$f" 2>/dev/null)
    case "$pid" in ''|*[!0-9]*) pid="" ;; esac
  fi
  P_PID="$pid"
  P_START="$start"
}

PID_STATE="missing"

is_alive() {
  local pid="$1" expected="$2" state actual
  PID_STATE="missing"
  [ -n "$pid" ] || return 1
  if ! kill -0 "$pid" 2>/dev/null; then
    PID_STATE="dead"
    return 1
  fi
  if [ -r "/proc/$pid/stat" ]; then
    state=$(awk '{print $3}' "/proc/$pid/stat" 2>/dev/null)
    if [ "$state" = "Z" ]; then
      PID_STATE="zombie"
      return 1
    fi
    if [ -n "$expected" ]; then
      actual=$(awk '{print $22}' "/proc/$pid/stat" 2>/dev/null)
      if [ -n "$actual" ] && [ "$actual" != "$expected" ]; then
        PID_STATE="reused"
        return 1
      fi
    fi
  fi
  PID_STATE="alive"
  return 0
}

S_EXISTS=0
S_RC=""
S_SENT=""

read_status_file() {
  local f="$1" line=""
  S_EXISTS=0; S_RC=""; S_SENT=""
  [ -n "$f" ] && [ -f "$f" ] || return 0
  line=$(grep -m 1 '^exit=' "$f" 2>/dev/null || true)
  [ -n "$line" ] || return 0
  S_EXISTS=1
  S_RC=$(printf '%s\n' "$line" | sed -n 's/^exit=\([0-9][0-9]*\).*/\1/p')
  S_SENT=$(printf '%s\n' "$line" | sed -n 's/.*sentinel=\([01]\).*/\1/p')
  is_uint "$S_RC" || S_RC=0
}

last_nonempty_line() {
  local f="$1" line=""
  [ -n "$f" ] && [ -f "$f" ] || { printf ''; return 0; }
  line=$(tail -n 50 "$f" 2>/dev/null | awk 'NF { last=$0 } END { print last }')
  printf '%s' "$line" | tr -d '\r' | sed 's/[[:space:]]*$//'
}

V_LABEL=""; V_VERDICT=""; V_CODE=0; V_REASON=""
V_PID=""; V_HB=""; V_HOOK="none"; V_SENT=""; V_RC=""; V_LAST=""; V_STATUS_RAW=""; V_ELAPSED=0; V_ANOMALY="no"

evaluate() {
  local label="$1" pidf="$2" statf="$3" logf="$4" sent="$5" hbf="$6" dl="$7"
  local now pid start pid_alive=0 pid_state="missing" hb_state="na" sent_state="na"
  local last="" anomaly=0 s_exists=0 s_rc="" s_sent=""
  local verdict="RUNNING" code="$EXIT_RUNNING" reason="" age=0 mt=0

  now=$(now_epoch)
  read_pid_file "$pidf"; pid="$P_PID"; start="$P_START"
  if [ -n "$pid" ]; then
    if is_alive "$pid" "$start"; then pid_alive=1; fi
    pid_state="$PID_STATE"
  fi

  read_status_file "$statf"; s_exists="$S_EXISTS"; s_rc="$S_RC"; s_sent="$S_SENT"
  last=$(last_nonempty_line "$logf")
  case "$last" in ANOMALY:*) anomaly=1 ;; esac

  if [ -n "$sent" ]; then
    if [ "$last" = "$sent" ] || [ "$s_sent" = "1" ]; then
      sent_state="yes"
    else
      sent_state="no"
    fi
  fi

  if [ -n "$hbf" ]; then
    if [ -f "$hbf" ]; then
      mt=$(file_mtime "$hbf")
      if is_uint "$mt" && [ "$mt" -gt 0 ]; then
        age=$((now - mt))
        if [ "$age" -gt "$HEARTBEAT_MAX_AGE" ]; then hb_state="stale"; else hb_state="fresh"; fi
      else
        hb_state="missing"
      fi
    else
      hb_state="missing"
    fi
  fi

  # Hook events are an early signal only; they never decide a verdict.
  local hook_state="none"
  if [ -n "$HOOK_DONE" ] && [ -s "$HOOK_DONE" ]; then HOOK_EVENT_SEEN=1; fi
  [ "$HOOK_EVENT_SEEN" -eq 1 ] && hook_state="observed"

  if [ "$s_exists" -eq 1 ]; then
    if [ -n "$sent" ]; then
      if [ "$anomaly" -eq 1 ]; then
        verdict="ANOMALY"; code="$EXIT_ANOMALY"; reason="anomaly-line"
      elif [ "$sent_state" = "yes" ]; then
        verdict="DONE"; code="$EXIT_DONE"; reason="exit-record-sentinel"
      elif is_uint "$s_rc" && [ "$s_rc" -ne 0 ]; then
        verdict="FAILED"; code="$EXIT_FAILED"; reason="exit-record-rc"
      else
        verdict="INCOMPLETE"; code="$EXIT_INCOMPLETE"; reason="exit-record-no-sentinel"
      fi
    else
      if [ "$anomaly" -eq 1 ]; then
        verdict="ANOMALY"; code="$EXIT_ANOMALY"; reason="anomaly-line"
      elif is_uint "$s_rc" && [ "$s_rc" -ne 0 ]; then
        verdict="FAILED"; code="$EXIT_FAILED"; reason="exit-record-rc"
      else
        verdict="DONE"; code="$EXIT_DONE"; reason="exit-record-ok"
      fi
    fi
  else
    if [ -n "$sent" ] && [ "$sent_state" = "yes" ]; then
      verdict="DONE"; code="$EXIT_DONE"; reason="sentinel"
    elif [ "$anomaly" -eq 1 ] && [ "$pid_alive" -eq 0 ]; then
      verdict="ANOMALY"; code="$EXIT_ANOMALY"; reason="anomaly-line"
    elif [ "$pid_state" = "dead" ] || [ "$pid_state" = "zombie" ] || [ "$pid_state" = "reused" ]; then
      verdict="DEAD"; code="$EXIT_DEAD"; reason="pid-$pid_state"
    elif [ "$pid_state" = "alive" ]; then
      verdict="RUNNING"; code="$EXIT_RUNNING"; reason="alive"
    else
      if [ "$((now - START_EPOCH))" -ge "$START_GRACE" ]; then
        verdict="NO_SIGNAL"; code="$EXIT_NO_SIGNAL"; reason="pid-missing"
      else
        verdict="RUNNING"; code="$EXIT_RUNNING"; reason="starting"
      fi
    fi
  fi

  if { [ "$verdict" = "RUNNING" ] || [ "$verdict" = "NO_SIGNAL" ]; } \
     && is_uint "$dl" && [ "$dl" -gt 0 ] && [ "$now" -ge "$dl" ]; then
    verdict="TIMEOUT"; code="$EXIT_TIMEOUT"; reason="deadline"
  fi

  V_LABEL="$label"; V_VERDICT="$verdict"; V_CODE="$code"; V_REASON="$reason"
  V_PID="$pid_state"; V_HB="$hb_state"; V_HOOK="$hook_state"; V_SENT="$sent_state"
  V_RC="${s_rc:-na}"; V_LAST="$last"; V_STATUS_RAW=""
  [ "$anomaly" -eq 1 ] && V_ANOMALY="observed" || V_ANOMALY="no"
  [ "$s_exists" -eq 1 ] && V_STATUS_RAW="exit=$s_rc sentinel=${s_sent:-na}"
  V_ELAPSED=$((now - START_EPOCH))
}

format_verdict() {
  printf 'WATCH label=%s verdict=%s pid=%s heartbeat=%s hook=%s anomaly=%s sentinel=%s rc=%s elapsed=%s reason=%s' \
    "$V_LABEL" "$V_VERDICT" "$V_PID" "$V_HB" "$V_HOOK" "$V_ANOMALY" "$V_SENT" "$V_RC" "$V_ELAPSED" "$V_REASON"
}

format_evidence() {
  local last
  last=$(one_line "$V_LAST" | tr '"' "'")
  printf 'EVIDENCE label=%s last="%s" status="%s"' "$V_LABEL" "$last" "$V_STATUS_RAW"
}

emit_single() {
  format_verdict; printf '\n'
  if [ "$V_CODE" -ne "$EXIT_RUNNING" ] || [ "$VERBOSE" -eq 1 ]; then
    format_evidence; printf '\n'
  fi
}

normalize_field() {
  if [ "$1" = "-" ]; then printf ''; else printf '%s' "$1"; fi
}

run_single() {
  START_EPOCH=$(now_epoch)
  if [ -n "$TIMEOUT" ]; then DEADLINE_EPOCH=$((START_EPOCH + TIMEOUT)); fi
  [ "$ONCE" -eq 1 ] && WINDOW=0
  local window_end=$((START_EPOCH + WINDOW)) now remaining sleep_for
  while :; do
    evaluate "$LABEL" "$PID_FILE" "$STATUS_FILE" "$LOG_FILE" "$SENTINEL" "$HEARTBEAT" "$DEADLINE_EPOCH"
    if [ "$V_CODE" -ne "$EXIT_RUNNING" ]; then
      emit_single
      exit "$V_CODE"
    fi
    now=$(now_epoch)
    if [ "$now" -ge "$window_end" ]; then
      emit_single
      exit "$EXIT_RUNNING"
    fi
    remaining=$((window_end - now))
    sleep_for=$INTERVAL
    [ "$sleep_for" -gt "$remaining" ] && sleep_for=$remaining
    if [ -n "$HOOK_FIFO" ] && [ -p "$HOOK_FIFO" ] && [ "$sleep_for" -gt 0 ]; then
      if read -t "$sleep_for" _hook_line <> "$HOOK_FIFO"; then
        HOOK_EVENT_SEEN=1
      fi
    else
      [ "$sleep_for" -gt 0 ] && sleep "$sleep_for"
    fi
  done
}

severity() {
  case "$1" in
    "$EXIT_ANOMALY") echo 9 ;;
    "$EXIT_FAILED") echo 8 ;;
    "$EXIT_DEAD") echo 7 ;;
    "$EXIT_INCOMPLETE") echo 6 ;;
    "$EXIT_TIMEOUT") echo 5 ;;
    "$EXIT_NO_SIGNAL") echo 4 ;;
    "$EXIT_DONE") echo 3 ;;
    *) echo 1 ;;
  esac
}

run_manifest() {
  local file="$1"
  [ -f "$file" ] || die_usage "manifest not found: $file"
  M_LABEL=(); M_PID=(); M_STATUS=(); M_LOG=(); M_SENT=(); M_HB=(); M_DL=()
  local a b c d e f g
  while IFS='|' read -r a b c d e f g; do
    case "${a:-}" in ''|\#*) continue ;; esac
    M_LABEL+=("$a")
    M_PID+=("$(normalize_field "${b:-}")")
    M_STATUS+=("$(normalize_field "${c:-}")")
    M_LOG+=("$(normalize_field "${d:-}")")
    M_SENT+=("$(normalize_field "${e:-}")")
    M_HB+=("$(normalize_field "${f:-}")")
    M_DL+=("$(normalize_field "${g:-}")")
  done < "$file"
  [ "${#M_LABEL[@]}" -gt 0 ] || die_usage "manifest has no targets"

  START_EPOCH=$(now_epoch)
  [ "$ONCE" -eq 1 ] && WINDOW=0
  local window_end=$((START_EPOCH + WINDOW)) now remaining sleep_for i
  local -a result_lines evidence_lines
  local any_terminal worst worst_sev sev
  while :; do
    result_lines=(); evidence_lines=(); any_terminal=0; worst="$EXIT_RUNNING"; worst_sev=1
    for i in "${!M_LABEL[@]}"; do
      local dl="${M_DL[$i]}"
      is_uint "$dl" || dl=0
      evaluate "${M_LABEL[$i]}" "${M_PID[$i]}" "${M_STATUS[$i]}" "${M_LOG[$i]}" \
        "${M_SENT[$i]}" "${M_HB[$i]}" "$dl"
      result_lines+=("$(format_verdict)")
      [ "$V_CODE" -ne "$EXIT_RUNNING" ] && evidence_lines+=("$(format_evidence)")
      if [ "$V_CODE" -ne "$EXIT_RUNNING" ]; then
        any_terminal=1
        sev=$(severity "$V_CODE")
        if [ "$sev" -gt "$worst_sev" ]; then worst_sev=$sev; worst="$V_CODE"; fi
      fi
    done
    if [ "$any_terminal" -eq 1 ]; then
      for i in "${!result_lines[@]}"; do printf '%s\n' "${result_lines[$i]}"; done
      for i in "${!evidence_lines[@]}"; do printf '%s\n' "${evidence_lines[$i]}"; done
      exit "$worst"
    fi
    now=$(now_epoch)
    if [ "$now" -ge "$window_end" ]; then
      for i in "${!result_lines[@]}"; do printf '%s\n' "${result_lines[$i]}"; done
      exit "$EXIT_RUNNING"
    fi
    remaining=$((window_end - now))
    sleep_for=$INTERVAL
    [ "$sleep_for" -gt "$remaining" ] && sleep_for=$remaining
    [ "$sleep_for" -gt 0 ] && sleep "$sleep_for"
  done
}

# ---------------------------------------------------------------- self-test

ST_TMP=""
ST_SPAWNED=()

cleanup_selftest() {
  local p
  if [ -n "${ST_TMP:-}" ]; then
    for p in "${ST_SPAWNED[@]:-}"; do
      [ -n "$p" ] && kill "$p" 2>/dev/null
    done
    rm -rf "$ST_TMP"
  fi
}

self_test() {
  local pass=0 fail=0
  ST_TMP=$(mktemp -d "${TMPDIR:-/tmp}/watch-target-selftest.XXXXXX") || {
    echo "SELF-TEST: cannot create temp dir" >&2
    return 1
  }
  ST_SPAWNED=()
  trap cleanup_selftest EXIT

  ok() { pass=$((pass + 1)); printf 'ok %s\n' "$1"; }
  bad() { fail=$((fail + 1)); printf 'FAIL %s — %s\n' "$1" "$2" >&2; }

  check() {
    local name="$1" want_rc="$2" want_verdict="$3" rc="$4" out="$5"
    if [ "$rc" -ne "$want_rc" ]; then
      bad "$name" "exit $rc != $want_rc; output: $out"
    elif ! printf '%s\n' "$out" | grep -q "verdict=$want_verdict"; then
      bad "$name" "missing verdict=$want_verdict; output: $out"
    else
      ok "$name"
    fi
  }

  check_hook() {
    local name="$1" want="$2" out="$3"
    if printf '%s\n' "$out" | grep -q "hook=$want"; then
      ok "$name"
    else
      bad "$name" "missing hook=$want; output: $out"
    fi
  }

  watch() {
    local out rc
    out=$("$SELF" "$@" 2>&1); rc=$?
    printf '%s\n' "$rc"
    printf '%s\n' "$out"
  }

  local base="$ST_TMP/base"
  mkdir -p "$base"

  # 1. DONE via exit record + sentinel
  printf 'working\nPLAN-DONE\n' > "$base/log1"
  printf 'exit=0 at=1 sentinel=1\n' > "$base/status1"
  : > "$base/pid1"
  local r; r=$(watch --label 'done' --pid-file "$base/pid1" --status-file "$base/status1" \
    --log "$base/log1" --sentinel PLAN-DONE --window 1 --start-grace 0)
  check 'done' 0 DONE "${r%%$'\n'*}" "${r#*$'\n'}"

  # 2. exit rc=0 but no sentinel => INCOMPLETE (fake-done)
  printf 'working\n' > "$base/log2"
  printf 'exit=0 at=1 sentinel=0\n' > "$base/status2"
  r=$(watch --label fake --pid-file "$base/pid1" --status-file "$base/status2" \
    --log "$base/log2" --sentinel PLAN-DONE --window 1 --start-grace 0)
  check fake-done 15 INCOMPLETE "${r%%$'\n'*}" "${r#*$'\n'}"

  # 3. anomaly line
  printf 'ANOMALY: spec conflict\n' > "$base/log3"
  printf 'exit=0 at=1 sentinel=0\n' > "$base/status3"
  r=$(watch --label anomaly --pid-file "$base/pid1" --status-file "$base/status3" \
    --log "$base/log3" --sentinel PLAN-DONE --window 1 --start-grace 0)
  check anomaly 11 ANOMALY "${r%%$'\n'*}" "${r#*$'\n'}"

  # 4. non-zero exit
  printf 'boom\n' > "$base/log4"
  printf 'exit=2 at=1 sentinel=0\n' > "$base/status4"
  r=$(watch --label failed --pid-file "$base/pid1" --status-file "$base/status4" \
    --log "$base/log4" --sentinel PLAN-DONE --window 1 --start-grace 0)
  check failed 12 FAILED "${r%%$'\n'*}" "${r#*$'\n'}"

  # 4b. contradictory record: sentinel flag set but final line is ANOMALY => fail safe
  printf 'ANOMALY: contract contradiction\n' > "$base/log4b"
  printf 'exit=0 at=1 sentinel=1\n' > "$base/status4b"
  r=$(watch --label contradiction --pid-file "$base/pid1" --status-file "$base/status4b" \
    --log "$base/log4b" --sentinel PLAN-DONE --window 1 --start-grace 0)
  check anomaly-precedence 11 ANOMALY "${r%%$'\n'*}" "${r#*$'\n'}"

  # 5. dead pid, no exit record
  sleep 0.2 & local deadpid=$!
  disown "$deadpid" 2>/dev/null || true
  ST_SPAWNED+=("$deadpid")
  wait "$deadpid" 2>/dev/null || true
  printf 'pid=%s start=\n' "$deadpid" > "$base/pid5"
  r=$(watch --label dead --pid-file "$base/pid5" --status-file "$base/none5" \
    --log "$base/none5" --sentinel PLAN-DONE --window 1 --start-grace 0)
  check dead 13 DEAD "${r%%$'\n'*}" "${r#*$'\n'}"

  # 6. running process, no terminal signal
  sleep 3 & local live=$!
  disown "$live" 2>/dev/null || true
  ST_SPAWNED+=("$live")
  local ticks=""
  [ -r "/proc/$live/stat" ] && ticks=$(awk '{print $22}' "/proc/$live/stat")
  printf 'pid=%s start=%s\n' "$live" "$ticks" > "$base/pid6"
  r=$(watch --label running --pid-file "$base/pid6" --status-file "$base/none6" \
    --log "$base/none6" --sentinel PLAN-DONE --window 1 --interval 1 --start-grace 0)
  check running 10 RUNNING "${r%%$'\n'*}" "${r#*$'\n'}"

  # 7. stage deadline => TIMEOUT, not window expiry
  r=$(watch --label timeout --pid-file "$base/pid6" --status-file "$base/none6" \
    --log "$base/none6" --sentinel PLAN-DONE --timeout 1 --window 3 --interval 1 --start-grace 0)
  check timeout 14 TIMEOUT "${r%%$'\n'*}" "${r#*$'\n'}"

  # 8. no signals at all => NO_SIGNAL (zero-match path must not fake completion)
  r=$(watch --label nosignal --pid-file "$base/none8" --status-file "$base/none8" \
    --log "$base/none8" --sentinel PLAN-DONE --window 0 --start-grace 0)
  check no-signal 16 NO_SIGNAL "${r%%$'\n'*}" "${r#*$'\n'}"

  # 9. stale heartbeat with live pid => RUNNING + heartbeat=stale
  printf 'pid=%s start=%s\n' "$live" "$ticks" > "$base/pid9"
  : > "$base/hb9"
  touch -t 200001010000 "$base/hb9" 2>/dev/null || true
  r=$(watch --label stale-hb --pid-file "$base/pid9" --status-file "$base/none9" \
    --log "$base/none9" --sentinel PLAN-DONE --heartbeat "$base/hb9" \
    --heartbeat-max-age 1 --window 0 --start-grace 0)
  check stale-heartbeat 10 RUNNING "${r%%$'\n'*}" "${r#*$'\n'}"
  printf '%s\n' "${r#*$'\n'}" | grep -q 'heartbeat=stale' || bad "stale-heartbeat-flag" "heartbeat not stale: $r"

  # 10. pid reuse guard
  printf 'pid=%s start=1\n' "$$" > "$base/pid10"
  r=$(watch --label reused --pid-file "$base/pid10" --status-file "$base/none10" \
    --log "$base/none10" --sentinel PLAN-DONE --window 1 --start-grace 0)
  check pid-reuse 13 DEAD "${r%%$'\n'*}" "${r#*$'\n'}"

  # 10b. zombie process (requires a non-reaping parent; /proc state check)
  if command -v python3 >/dev/null 2>&1; then
    python3 - "$base/zpid" <<'PY' &
import os, sys, time
pid = os.fork()
if pid == 0:
    os._exit(0)
with open(sys.argv[1], "w") as f:
    f.write(str(pid))
time.sleep(3)
PY
    local zparent=$!
    disown "$zparent" 2>/dev/null || true
    ST_SPAWNED+=("$zparent")
    local i=0
    while [ ! -s "$base/zpid" ] && [ "$i" -lt 50 ]; do sleep 0.1; i=$((i+1)); done
    local zpid
    zpid=$(cat "$base/zpid" 2>/dev/null || true)
    printf 'pid=%s start=\n' "$zpid" > "$base/zpid10b"
    r=$(watch --label zombie --pid-file "$base/zpid10b" --status-file "$base/none10b" \
      --log "$base/none10b" --sentinel PLAN-DONE --window 1 --start-grace 0)
    check zombie 13 DEAD "${r%%$'\n'*}" "${r#*$'\n'}"
  else
    printf 'skip zombie (python3 not found)\n'
  fi

  # 11. sentinel without exit record
  printf 'PLAN-DONE\n' > "$base/log11"
  r=$(watch --label sentinel --pid-file "$base/pid5" --status-file "$base/none11" \
    --log "$base/log11" --sentinel PLAN-DONE --window 0 --start-grace 0)
  check sentinel-only 0 DONE "${r%%$'\n'*}" "${r#*$'\n'}"

  # 12. async-script mode: exit rc=0, no sentinel configured
  printf 'finished\n' > "$base/log12"
  printf 'exit=0 at=1 sentinel=0\n' > "$base/status12"
  r=$(watch --label async --pid-file "$base/pid1" --status-file "$base/status12" \
    --log "$base/log12" --window 0 --start-grace 0)
  check async-exit-ok 0 DONE "${r%%$'\n'*}" "${r#*$'\n'}"

  # 13. manifest: one DONE + one RUNNING, both reported
  printf 'PLAN-DONE\n' > "$base/logm1"
  printf 'exit=0 at=1 sentinel=1\n' > "$base/statusm1"
  printf 'm1|%s|%s|%s|PLAN-DONE|-|0\nm2|%s|-|-|PLAN-DONE|-|0\n' \
    "$base/pid1" "$base/statusm1" "$base/logm1" "$base/pid6" > "$base/manifest"
  r=$(watch --manifest "$base/manifest" --window 1 --interval 1 --start-grace 0)
  local mrc="${r%%$'\n'*}" mout="${r#*$'\n'}"
  if [ "$mrc" -ne 0 ] || ! printf '%s\n' "$mout" | grep -q 'label=m1 verdict=DONE' \
     || ! printf '%s\n' "$mout" | grep -q 'label=m2 verdict=RUNNING'; then
    bad "manifest" "rc=$mrc out=$mout"
  else
    ok "manifest"
  fi

  # 14. hook done file: observed is an early signal, DONE still comes from the
  # exit record + sentinel
  printf 'PLAN-DONE\n' > "$base/log14"
  printf 'exit=0 at=1 sentinel=1\n' > "$base/status14"
  printf '{"hook_event_name":"Stop"}\n' > "$base/done14"
  r=$(watch --label hookdone --pid-file "$base/pid1" --status-file "$base/status14" \
    --log "$base/log14" --sentinel PLAN-DONE --hook-done "$base/done14" \
    --window 0 --start-grace 0)
  check hook-done 0 DONE "${r%%$'\n'*}" "${r#*$'\n'}"
  check_hook hook-done-flag observed "${r#*$'\n'}"

  # 15. hook FIFO event wakes the wait; it never fabricates a verdict
  if command -v mkfifo >/dev/null 2>&1; then
    sleep 5 & local hlive=$!
    disown "$hlive" 2>/dev/null || true
    ST_SPAWNED+=("$hlive")
    local hticks=""
    [ -r "/proc/$hlive/stat" ] && hticks=$(awk '{print $22}' "/proc/$hlive/stat")
    printf 'pid=%s start=%s\n' "$hlive" "$hticks" > "$base/pid15"
    mkfifo "$base/hook15.fifo"
    ( sleep 0.5; printf 'STOP test 1\n' > "$base/hook15.fifo" ) &
    local hwriter=$!
    disown "$hwriter" 2>/dev/null || true
    ST_SPAWNED+=("$hwriter")
    r=$(watch --label hookfifo --pid-file "$base/pid15" --status-file "$base/none15" \
      --log "$base/none15" --sentinel PLAN-DONE --hook-fifo "$base/hook15.fifo" \
      --window 2 --interval 1 --start-grace 0)
    check hook-fifo 10 RUNNING "${r%%$'\n'*}" "${r#*$'\n'}"
    check_hook hook-fifo-flag observed "${r#*$'\n'}"
  else
    printf 'skip hook-fifo (mkfifo not found)\n'
  fi

  # 16. demonstrate the pgrep -c zero-match trap (regression knowledge; the
  # watcher itself never uses pgrep for liveness)
  if command -v pgrep >/dev/null 2>&1; then
    local zero
    zero=$(pgrep -c '__watch_target_no_such_process__' 2>/dev/null || echo 0)
    if [ "$zero" = "$(printf '0\n0')" ]; then
      ok "pgrep-zero-match-trap-reproduced"
    else
      bad "pgrep-zero-match-trap-reproduced" "expected two 0 lines, got: $zero"
    fi
  fi

  if [ "$fail" -eq 0 ]; then
    printf 'SELF-TEST: %s passed, 0 failed\n' "$pass"
    return 0
  fi
  printf 'SELF-TEST: %s passed, %s failed\n' "$pass" "$fail" >&2
  return 1
}

if [ "$SELF_TEST" -eq 1 ]; then
  self_test
  exit $?
fi

if [ -n "$MANIFEST" ]; then
  [ -z "$PID_FILE$STATUS_FILE$LOG_FILE" ] || die_usage "use --manifest or single-target flags, not both"
  run_manifest "$MANIFEST"
else
  [ -n "$PID_FILE$STATUS_FILE$LOG_FILE" ] || die_usage "at least one of --pid-file/--status-file/--log is required"
  run_single
fi
