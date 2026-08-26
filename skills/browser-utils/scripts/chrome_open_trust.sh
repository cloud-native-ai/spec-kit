#!/usr/bin/env bash
# chrome_open_trust — generic trusted-browser launcher (source this file).
#
# Opens a URL in a Chrome instance with web-security relaxed for trusted
# internal/test origins. Fully portable: no machine-specific dependencies.
# Origin: frozen from a profiles-style `declare -f chrome_open_trust`, with
# the launcher made self-contained (self-resolving Chrome binary).
#
# Login-state reuse convention:
#   The caller MUST define a global CHROME_USER_DATA_AGENT environment
#   variable pointing to a Chrome profile directory that already holds the
#   target site's login state, and pass it via --user-data-dir. If it is
#   unset or invalid, stop and ask the user to define it — never fall back
#   to a throwaway profile silently.
#
# Usage:
#   source ${SKILL_HOME}/scripts/chrome_open_trust.sh
#   check_chrome_user_data_agent || return 1
#   chrome_open_trust --user-data-dir="${CHROME_USER_DATA_AGENT}" --new-window <site-url>

# Validation for the CHROME_USER_DATA_AGENT environment variable.
check_chrome_user_data_agent() {
  if [[ -z "${CHROME_USER_DATA_AGENT:-}" || ! -d "${CHROME_USER_DATA_AGENT}" ]]; then
    echo "[browser-utils] CHROME_USER_DATA_AGENT is unset or not a directory." >&2
    echo "[browser-utils] Define this global environment variable to point to a Chrome profile directory containing the site's login state, then retry." >&2
    return 1
  fi
}

chrome_open_trust() {
  local url="" a; local -a args=()
  if [ $# -gt 0 ] && [[ "${1}" != -* ]]; then url="${1}"; shift; fi
  local has_profile="false"
  for a in "$@"; do case "${a}" in --user-data-dir=*) has_profile="true";; esac; done
  [ -n "${url}" ] && args+=("${url}" "--unsafely-treat-insecure-origin-as-secure=${url}")
  args+=(--allow-running-insecure-content --reduce-security-for-testing --test-type)
  [ "${has_profile}" = "false" ] && args+=("--user-data-dir=${HOME}/tmp")
  args+=("$@")
  # Portable launcher (replaces machine-local chrome_open): self-resolve the
  # Chrome binary; override with CHROME_MACOS when the host keeps it elsewhere.
  local chrome_bin="${CHROME_MACOS:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
  nohup "${chrome_bin}" "${args[@]}" >/dev/null 2>&1 &
}
