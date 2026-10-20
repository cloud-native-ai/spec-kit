#!/usr/bin/env bash
# stub-cli.sh — controlled phase CLI for stream/runner fixtures.
#
# Modes:
#   stream     (default) emit NDJSON events, ending with a terminal result
#   no-stream  emit buffered text; --output-format is unsupported and rejected
#   fail       emit events then exit non-zero
#   no-result  emit non-terminal events, exit 0 without a result event
#
# Common options: --output-format <fmt>, --delay <seconds>, --sentinel <text>,
# --help. --help deliberately does NOT advertise --output-format so capability
# probing sees a CLI that lacks stream support.
set -u

MODE="stream"
DELAY=0
SENTINEL="PLAN-DONE"
OUTPUT_FORMAT=""

while [ $# -gt 0 ]; do
  case "$1" in
    --mode) MODE="$2"; shift 2 ;;
    --delay) DELAY="$2"; shift 2 ;;
    --sentinel) SENTINEL="$2"; shift 2 ;;
    --output-format) OUTPUT_FORMAT="$2"; shift 2 ;;
    --help)
      cat <<'EOF'
stub-cli.sh — controlled phase CLI

Usage: stub-cli.sh [--mode stream|no-stream|fail|no-result] [--delay N]
                   [--sentinel TEXT]
EOF
      exit 0
      ;;
    *) shift ;;
  esac
done

if [ "$MODE" = "no-stream" ]; then
  if [ -n "$OUTPUT_FORMAT" ]; then
    printf 'stub-cli: unsupported option --output-format\n' >&2
    exit 3
  fi
  printf 'buffered stage output\n'
  printf '%s\n' "$SENTINEL"
  exit 0
fi

if [ -n "$OUTPUT_FORMAT" ] && [ "$OUTPUT_FORMAT" != "stream-json" ]; then
  printf 'stub-cli: unknown output format %s\n' "$OUTPUT_FORMAT" >&2
  exit 2
fi

emit() {
  printf '%s\n' "$1"
  if [ "$DELAY" -gt 0 ] 2>/dev/null; then sleep "$DELAY"; fi
}

emit '{"type":"system","subtype":"init","session_id":"fixture"}'
emit '{"type":"assistant","message":{"content":[{"type":"text","text":"working; this text mentions '"$SENTINEL"' but is not terminal"}]}}'

case "$MODE" in
  stream)
    emit '{"type":"assistant","message":{"content":[{"type":"text","text":"more progress"}]}}'
    printf '{"type":"result","subtype":"success","is_error":false,"result":"stage finished\\nthe final line is exact\\n%s"}\n' "$SENTINEL"
    exit 0
    ;;
  fail)
    printf '{"type":"result","subtype":"error","is_error":true,"result":"stage failed"}\n'
    printf 'stub-cli: stage failed\n' >&2
    exit 7
    ;;
  no-result)
    emit '{"type":"assistant","message":{"content":[{"type":"text","text":"no terminal result will follow"}]}}'
    exit 0
    ;;
  *)
    printf 'stub-cli: unknown mode %s\n' "$MODE" >&2
    exit 2
    ;;
esac
