#!/usr/bin/env bash
# install.sh — cold-start bootstrap installer for the Specify CLI (spec-kit).
#
# Ownership: this script IS the single source of truth for cold-start install
# logic — python resolution ladder, pip index pairing, source fallback, the
# opt-in uv fast path, and post-install verification. Downstream wrappers
# (e.g. cws-lib-bash scripts/313_specify.sh specify_install) only locate or
# fetch this file and delegate; they must not re-implement any logic below.
#
# Ground layer (assumed present, NEVER auto-installed): bash + python3 (with
# pip) + git + network. Intranet-first: the internal GitLab source is tried
# first and the only pip index contacted is the one pip is actually
# configured with; public mirrors (gitee/github) are probed only when the
# internal source is unreachable, and `uv` is an opt-in accelerator for
# machines that already have it — never installed here.
#
# Exit codes: 0 ok | 2 environment prerequisite missing (python/pip/git/uv)
# | 3 no viable source x index combination | 5 post-install verification
# failed.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ---------------------------------------------------------------- logging --
log() { printf '[install.sh] %s: %s\n' "$1" "$2" >&2; }
log_info() { log info "$1"; }
log_warn() { log warn "$1"; }
log_error() { log error "$1"; }

die() { # die <exit_code> <message>
  log_error "$2"
  exit "$1"
}

# ----------------------------------------------------------- default sources
# Intranet-first ordering. Entry format: "<pip source spec>|<git host>|<scope>"
# scope: intranet | public (public entries are dropped by --intranet-only).
# This list is the authoritative bootstrap source list — wrappers may keep a
# fetch-only copy to obtain this very script, but install order lives here.
DEFAULT_SOURCE_SPECS=(
  "git+https://gitlab.alibaba-inc.com/cloud-native-ai/spec-kit.git@master|gitlab.alibaba-inc.com|intranet"
  "git+https://gitee.com/cloud-native-ai/spec-kit.git@master|gitee.com|public"
  "git+https://github.com/cloud-native-ai/spec-kit.git@master|github.com|public"
)
DEFAULT_INDEX="https://pypi.org/simple/"
PROBE_TIMEOUT=10
PIP_TIMEOUT=20
MIN_PYTHON="3.8"

# --------------------------------------------------------------- arg parsing
OPT_DRY_RUN=false
OPT_NO_PROBE=false
OPT_INTRANET_ONLY=false
OPT_USE_UV=false
OPT_LOCAL=false
OPT_SOURCE_URL=""
OPT_INDEX_URL=""
OPT_PYTHON=""

usage() {
  cat <<'EOF'
install.sh — cold-start bootstrap installer for the Specify CLI (spec-kit)

Usage:
  bash install.sh [options]

Options:
  --python PATH    Pin the interpreter. Default resolution ladder:
                   --python / SPECIFY_PYTHON env, then $PWD/.venv/bin/python,
                   then the python of an existing specify on PATH (upgrade-
                   in-place), then PATH python3 (then python), then the newest
                   python3* in standard bin dirs.
  --index-url URL  pip index for dependency resolution. Default precedence:
                   --index-url > PIP_INDEX_URL env > pip config > pypi.org.
                   The index host is probed together with each git source
                   ("source x index" pairing): an unreachable index fails
                   fast because dependency resolution always needs it.
  --source-url X   Install from this single source only: a pip spec
                   (git+https://...) or a local checkout directory. Skips
                   the intranet-first fallback loop.
  --local          Editable install (pip install -e) of the checkout this
                   script lives in — the self-hosting / dev path.
  --uv             Opt-in uv fast path: uv tool install with the resolved
                   python and index. uv must already exist on PATH; this
                   script NEVER installs uv. (Or SPECIFY_INSTALLER=uv.)
  --intranet-only  Internal GitLab only; zero public network contact.
  --no-probe       Skip reachability probes; attempt sources in order.
  --dry-run        Print the full plan (python resolution, index pairing,
                   per-source preflight, commands) without mutating anything.
  -h, --help       Show this help.

Exit codes: 0 ok | 2 missing prerequisite (python/pip/git/uv) | 3 no viable
source x index (unreachable, or install failed on all sources) | 5 post-
install verification failed.

Upgrade semantics: install is a clean reinstall — an existing specify-cli
in the resolved environment is uninstalled first, so re-running this script
upgrades in place. When no --python / cwd .venv pins the destination and a
specify is already on PATH, the ladder prefers that installation's python
(upgrade-in-place) to avoid installing a duplicate into an unrelated env.

Ground layer (never auto-installed): bash, python3 with pip, git, network.
Intranet-first: internal GitLab is tried before public mirrors; the only pip
index contacted is the one pip is configured with (explicit override wins).
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --python)
      [ $# -ge 2 ] || die 2 "--python requires a value"
      OPT_PYTHON="$2"
      shift 2
      ;;
    --python=*)
      OPT_PYTHON="${1#*=}"
      shift
      ;;
    --index-url)
      [ $# -ge 2 ] || die 2 "--index-url requires a value"
      OPT_INDEX_URL="$2"
      shift 2
      ;;
    --index-url=*)
      OPT_INDEX_URL="${1#*=}"
      shift
      ;;
    --source-url)
      [ $# -ge 2 ] || die 2 "--source-url requires a value"
      OPT_SOURCE_URL="$2"
      shift 2
      ;;
    --source-url=*)
      OPT_SOURCE_URL="${1#*=}"
      shift
      ;;
    --local)
      OPT_LOCAL=true
      shift
      ;;
    --uv)
      OPT_USE_UV=true
      shift
      ;;
    --intranet-only)
      OPT_INTRANET_ONLY=true
      shift
      ;;
    --no-probe)
      OPT_NO_PROBE=true
      shift
      ;;
    --dry-run)
      OPT_DRY_RUN=true
      shift
      ;;
    -h | --help)
      usage
      exit 0
      ;;
    *)
      die 2 "unknown option: $1 (see --help)"
      ;;
  esac
done

[ "${OPT_LOCAL}" = true ] && [ -n "${OPT_SOURCE_URL}" ] &&
  die 2 "--local and --source-url are mutually exclusive"
if [ -n "${SPECIFY_INSTALLER:-}" ] && [ "${SPECIFY_INSTALLER}" = "uv" ]; then
  OPT_USE_UV=true
fi

# ---------------------------------------------------------- python ladder --
# Levels: --python / SPECIFY_PYTHON > $PWD/.venv (caller's cwd context) >
# existing installation's python (upgrade-in-place) > PATH python3/python >
# newest system python3*. The upgrade-in-place level exists because this
# script doubles as the UPGRADE path (clean reinstall): when a specify is
# already on PATH and no cwd-venv or pin applies, upgrading the python that
# owns that installation prevents duplicate installs into unrelated envs.
resolve_python() {
  # Sets the globals PY_BIN / PY_ORIGIN (command substitution would swallow
  # PY_ORIGIN — assignments inside $() do not propagate to the parent shell).
  PY_BIN=""
  PY_ORIGIN=""
  if [ -n "${OPT_PYTHON}" ]; then
    [ -x "${OPT_PYTHON}" ] || die 2 "--python is not executable: ${OPT_PYTHON}"
    PY_BIN="${OPT_PYTHON}"
    PY_ORIGIN="flag --python"
    return 0
  fi
  if [ -n "${SPECIFY_PYTHON:-}" ]; then
    [ -x "${SPECIFY_PYTHON}" ] || die 2 "SPECIFY_PYTHON is not executable: ${SPECIFY_PYTHON}"
    PY_BIN="${SPECIFY_PYTHON}"
    PY_ORIGIN="env SPECIFY_PYTHON"
    return 0
  fi
  if [ -x "${PWD}/.venv/bin/python" ]; then
    PY_BIN="${PWD}/.venv/bin/python"
    PY_ORIGIN="cwd .venv"
    return 0
  fi
  # Upgrade-in-place: an existing specify on PATH whose bin dir carries a
  # sibling python (venv layout). Non-venv installs (uv tool dirs without a
  # python sibling) fall through to the next levels.
  local existing="$(command -v specify || true)"
  if [ -n "${existing}" ]; then
    local existing_bin="$(dirname "${existing}")"
    if [ -x "${existing_bin}/python" ]; then
      PY_BIN="${existing_bin}/python"
      PY_ORIGIN="existing installation (upgrade-in-place): ${existing}"
      return 0
    fi
  fi
  local p
  p="$(command -v python3 || true)"
  if [ -z "${p}" ]; then
    p="$(command -v python || true)"
  fi
  if [ -n "${p}" ]; then
    PY_BIN="${p}"
    PY_ORIGIN="PATH"
    return 0
  fi
  # Level: newest python3* across standard bin dirs.
  local best="" candidate dir
  for dir in /usr/bin /usr/local/bin /opt/homebrew/bin /opt/local/bin; do
    for candidate in "${dir}"/python3*; do
      [ -x "${candidate}" ] || continue
      case "${candidate##*/}" in
        python3 | python3.[0-9]*) ;;
        *) continue ;;
      esac
      if [ -z "${best}" ] ||
        [ "$(printf '%s\n%s\n' "${best}" "${candidate}" | sort -V | tail -n 1)" = "${candidate}" ]; then
        best="${candidate}"
      fi
    done
  done
  if [ -n "${best}" ]; then
    PY_BIN="${best}"
    PY_ORIGIN="system newest"
    return 0
  fi
  return 1
}

if ! resolve_python; then
  die 2 "no python interpreter found (ladder: --python / SPECIFY_PYTHON / \$PWD/.venv/bin/python / PATH python3 / system python3*). Python is a ground-layer prerequisite; this script never installs it."
fi

"${PY_BIN}" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' ||
  die 2 "python at ${PY_BIN} is older than ${MIN_PYTHON} (specify-cli requires >= ${MIN_PYTHON})"

"${PY_BIN}" -m pip --version >/dev/null 2>&1 ||
  die 2 "pip unavailable via '${PY_BIN}' -m pip. pip is a ground-layer prerequisite; this script never installs it."

# Upgrade transparency: this script is also the UPGRADE path (clean
# reinstall). When an existing specify lives in a different environment than
# the resolved one, say so — the old installation stays in place.
EXISTING_SPECIFY="$(command -v specify || true)"
if [ -n "${EXISTING_SPECIFY}" ] &&
  [ "$(dirname "${EXISTING_SPECIFY}")" != "$(dirname "${PY_BIN}")" ]; then
  log_warn "existing specify at ${EXISTING_SPECIFY} is in a different environment; this run installs into $(dirname "${PY_BIN}") and leaves the old one untouched (uninstall it explicitly if the new one should replace it)"
fi

# ---------------------------------------------------------------- index ----
INDEX_ORIGIN="flag --index-url"
if [ -z "${OPT_INDEX_URL}" ]; then
  if [ -n "${PIP_INDEX_URL:-}" ]; then
    OPT_INDEX_URL="${PIP_INDEX_URL}"
    INDEX_ORIGIN="env PIP_INDEX_URL"
  else
    cfg="$("${PY_BIN}" -m pip config get global.index-url 2>/dev/null || true)"
    if [ -n "${cfg}" ]; then
      OPT_INDEX_URL="${cfg}"
      INDEX_ORIGIN="pip config"
    else
      OPT_INDEX_URL="${DEFAULT_INDEX}"
      INDEX_ORIGIN="default"
    fi
  fi
fi
INDEX_URL="${OPT_INDEX_URL}"
TRUSTED_HOST=""
case "${INDEX_URL}" in
  http://*)
    th="${INDEX_URL#http://}"
    th="${th%%\?*}"
    th="${th%%/*}"
    TRUSTED_HOST="${th}"
    ;;
esac

# ---------------------------------------------------------------- probes ---
probe_url() { # probe_url <url> — exit 0 when the host answers anything
  local url="$1"
  if command -v curl >/dev/null 2>&1; then
    curl -sI --max-time "${PROBE_TIMEOUT}" "${url}" >/dev/null 2>&1
    return $?
  fi
  "${PY_BIN}" - "${url}" <<'PYEOF' >/dev/null 2>&1
import sys, ssl, urllib.error, urllib.request
url = sys.argv[1]
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
try:
    urllib.request.urlopen(url, timeout=10, context=ctx)
except urllib.error.HTTPError:
    sys.exit(0)  # any HTTP response proves the host reachable
except Exception:
    sys.exit(1)
sys.exit(0)
PYEOF
}

# run_bounded <seconds> <cmd...> — portable wall-clock bound (macOS ships no
# `timeout`); the alarm(2) timer survives exec, so git is killed on expiry.
run_bounded() {
  local secs="$1"
  shift
  if command -v perl >/dev/null 2>&1; then
    perl -e 'alarm shift; exec @ARGV' "${secs}" "$@"
    return $?
  fi
  "$@"
}

# probe_git_source <pip spec> — host reachability, then authoritative
# git ls-remote (credential-free works only if the repo allows it; prompt is
# disabled so an auth-requiring source fails fast instead of hanging).
probe_git_source() {
  local spec="$1"
  local url="${spec#git+}"
  url="${url%@*}" # strip pip's @ref suffix for raw git operations
  local scheme="${url%%://*}"
  local rest="${url#*://}"
  local host="${rest%%/*}"
  if [ "${OPT_NO_PROBE}" != true ]; then
    probe_url "${scheme}://${host}" || return 1
  fi
  run_bounded 25 env GIT_TERMINAL_PROMPT=0 git ls-remote --exit-code "${url}" HEAD >/dev/null 2>&1
}

# --------------------------------------------------------------- sources ---
SOURCE_SPECS=()
SOURCE_SCOPES=()
SOURCE_MODE="fallback"

if [ "${OPT_LOCAL}" = true ]; then
  SOURCE_MODE="local-editable"
elif [ -n "${OPT_SOURCE_URL}" ]; then
  case "${OPT_SOURCE_URL}" in
    git+* | https://* | http://*)
      SOURCE_MODE="single-git"
      SOURCE_SPECS=("${OPT_SOURCE_URL}")
      SOURCE_SCOPES=("explicit")
      ;;
    *)
      [ -d "${OPT_SOURCE_URL}" ] || die 2 "--source-url is neither a git spec nor an existing directory: ${OPT_SOURCE_URL}"
      [ -f "${OPT_SOURCE_URL}/pyproject.toml" ] ||
        die 2 "--source-url directory has no pyproject.toml (not a spec-kit checkout?): ${OPT_SOURCE_URL}"
      SOURCE_MODE="single-dir"
      ;;
  esac
else
  spec_entry=""
  scope=""
  for spec_entry in "${DEFAULT_SOURCE_SPECS[@]}"; do
    scope="${spec_entry##*|}"
    if [ "${OPT_INTRANET_ONLY}" = true ] && [ "${scope}" = "public" ]; then
      continue
    fi
    SOURCE_SPECS+=("${spec_entry%%|*}")
    SOURCE_SCOPES+=("${scope}")
  done
  [ "${#SOURCE_SPECS[@]}" -gt 0 ] ||
    die 2 "no install source selected (check --intranet-only / --source-url)"
fi

NEED_GIT=false
case "${SOURCE_MODE}" in
  fallback | single-git) NEED_GIT=true ;;
esac
if [ "${NEED_GIT}" = true ]; then
  command -v git >/dev/null 2>&1 ||
    die 2 "git not found. git is a ground-layer prerequisite for git+ sources; this script never installs it."
fi

if [ "${OPT_USE_UV}" = true ]; then
  command -v uv >/dev/null 2>&1 ||
    die 2 "--uv / SPECIFY_INSTALLER=uv requested but uv is not on PATH. This script never installs uv; install uv manually or drop the flag to use pip."
fi

MODE_DESC="pip"
[ "${OPT_USE_UV}" = true ] && MODE_DESC="uv (opt-in)"

# ------------------------------------------------------- index preflight ---
INDEX_OK=true
if [ "${OPT_NO_PROBE}" != true ]; then
  log_info "Probing pip index: ${INDEX_URL} (origin: ${INDEX_ORIGIN})"
  if probe_url "${INDEX_URL}"; then
    log_info "pip index reachable"
  else
    INDEX_OK=false
    log_warn "pip index unreachable: ${INDEX_URL}"
  fi
fi

index_remediation() {
  cat >&2 <<'EOF'
No viable source x index combination: dependency resolution always needs the
pip index (only the specify-cli tree itself comes from the git source).
Remediation:
  - pass an explicit reachable index:  bash install.sh --index-url <url>
    (intranet: http://yum.tbsite.net/pypi/simple/ ; public: https://pypi.org/simple/)
  - or fix pip.conf / network and retry
EOF
}

if [ "${INDEX_OK}" != true ]; then
  if [ "${OPT_DRY_RUN}" = true ]; then
    printf '==== install.sh plan (dry-run) ====\n'
    printf 'mode:            %s\n' "${MODE_DESC}"
    printf 'python:          %s  (origin: %s)\n' "${PY_BIN}" "${PY_ORIGIN}"
    printf 'pip index:       %s  (origin: %s)\n' "${INDEX_URL}" "${INDEX_ORIGIN}"
    printf 'index probe:     UNREACHABLE — real run would fail fast (exit 3)\n'
    printf '==== end plan ====\n'
    exit 0
  fi
  index_remediation
  exit 3
fi

# ------------------------------------------------------- source selection --
CHOSEN_SOURCE=""
CHOSEN_LABEL=""
CHOSEN_INDEX=0
SOURCE_STATUSES=()

case "${SOURCE_MODE}" in
  local-editable)
    CHOSEN_SOURCE="${REPO_ROOT}"
    CHOSEN_LABEL="local checkout (editable)"
    ;;
  single-dir)
    CHOSEN_SOURCE="${OPT_SOURCE_URL}"
    CHOSEN_LABEL="local directory"
    ;;
  *)
    i=0
    for spec in "${SOURCE_SPECS[@]}"; do
      i=$((i + 1))
      status="ok"
      if [ "${OPT_NO_PROBE}" != true ]; then
        host="${spec#*://}"
        host="${host%%/*}"
        log_info "Probing source ${i}/${#SOURCE_SPECS[@]}: ${host} [${SOURCE_SCOPES[$((i - 1))]}]"
        if probe_git_source "${spec}"; then
          status="ok"
        else
          status="unreachable"
        fi
      else
        status="unprobed"
      fi
      SOURCE_STATUSES+=("${status}")
      if [ -z "${CHOSEN_SOURCE}" ] && [ "${status}" != "unreachable" ]; then
        CHOSEN_SOURCE="${spec}"
        CHOSEN_LABEL="${SOURCE_SCOPES[$((i - 1))]}"
        CHOSEN_INDEX="${i}"
      fi
    done
    ;;
esac

source_remediation() {
  cat >&2 <<EOF
All install sources failed (unreachable or install failed). Remediation:
  - check network / VPN and retry
  - pass an explicit source:  bash install.sh --source-url <git+... | local dir>
  - public mirrors are skipped by --intranet-only; drop the flag if public
    fallback is acceptable in this environment
EOF
}

if [ -z "${CHOSEN_SOURCE}" ]; then
  if [ "${OPT_DRY_RUN}" = true ]; then
    printf '==== install.sh plan (dry-run) ====\n'
    printf 'mode:            %s\n' "${MODE_DESC}"
    printf 'python:          %s  (origin: %s)\n' "${PY_BIN}" "${PY_ORIGIN}"
    printf 'pip index:       %s  (origin: %s)\n' "${INDEX_URL}" "${INDEX_ORIGIN}"
    printf 'sources:         all unreachable/unprobed — real run would fail (exit 3)\n'
    printf '==== end plan ====\n'
    exit 0
  fi
  source_remediation
  exit 3
fi

# ------------------------------------------------------------- commands ----
BIN_DIR="$(dirname "${PY_BIN}")"
INSTALL_ARGS=(--timeout "${PIP_TIMEOUT}" --no-input --index-url "${INDEX_URL}")
if [ -n "${TRUSTED_HOST}" ]; then
  INSTALL_ARGS+=(--trusted-host "${TRUSTED_HOST}")
fi

if [ "${OPT_USE_UV}" = true ]; then
  UV_CMD=(uv tool install --force --python "${PY_BIN}")
  if [ "${SOURCE_MODE}" = "local-editable" ]; then
    UV_CMD+=(--editable)
  fi
  UV_CMD+=("${CHOSEN_SOURCE}")
else
  PIP_UNINSTALL_CMD=("${PY_BIN}" -m pip uninstall -y specify-cli)
  PIP_INSTALL_CMD=("${PY_BIN}" -m pip install)
  if [ "${SOURCE_MODE}" = "local-editable" ]; then
    PIP_INSTALL_CMD+=(-e)
  fi
  PIP_INSTALL_CMD+=("${INSTALL_ARGS[@]}" "${CHOSEN_SOURCE}")
fi

print_plan() {
  printf '==== install.sh plan (dry-run) ====\n'
  printf 'mode:            %s\n' "${MODE_DESC}"
  printf 'python:          %s  (origin: %s)\n' "${PY_BIN}" "${PY_ORIGIN}"
  printf 'bin dir:         %s\n' "${BIN_DIR}"
  printf 'pip index:       %s  (origin: %s)\n' "${INDEX_URL}" "${INDEX_ORIGIN}"
  if [ -n "${TRUSTED_HOST}" ]; then
    printf 'trusted-host:    %s\n' "${TRUSTED_HOST}"
  fi
  case "${SOURCE_MODE}" in
    fallback)
      printf 'sources (in order):\n'
      i=0
      for spec in "${SOURCE_SPECS[@]}"; do
        i=$((i + 1))
        printf '  %d. %s  [%s]  probe: %s\n' "${i}" "${spec}" "${SOURCE_SCOPES[$((i - 1))]}" "${SOURCE_STATUSES[$((i - 1))]}"
      done
      ;;
    single-git)
      printf 'source:          %s  [single, explicit]\n' "${CHOSEN_SOURCE}"
      ;;
    *)
      printf 'source:          %s  [%s]\n' "${CHOSEN_SOURCE}" "${CHOSEN_LABEL}"
      ;;
  esac
  printf 'chosen source:   %s\n' "${CHOSEN_SOURCE}"
  printf 'would run:\n'
  if [ "${OPT_USE_UV}" = true ]; then
    printf '  UV_DEFAULT_INDEX=%s UV_INDEX_URL=%s' "${INDEX_URL}" "${INDEX_URL}"
    if [ -n "${TRUSTED_HOST}" ]; then
      printf ' UV_INSECURE_HOST=%s' "${TRUSTED_HOST}"
    fi
    printf ' %s\n' "${UV_CMD[*]}"
  else
    printf '  %s\n' "${PIP_UNINSTALL_CMD[*]}"
    printf '  %s\n' "${PIP_INSTALL_CMD[*]}"
  fi
  if [ "${OPT_USE_UV}" = true ]; then
    printf '  %s check\n' "$(uv tool dir 2>/dev/null)/bin/specify"
  else
    printf '  PATH=%s:$PATH %s/specify check\n' "${BIN_DIR}" "${BIN_DIR}"
  fi
  printf '==== end plan ====\n'
}

if [ "${OPT_DRY_RUN}" = true ]; then
  print_plan
  exit 0
fi

# ------------------------------------------------------------ real install -
log_info "Installing with ${MODE_DESC} from: ${CHOSEN_SOURCE}"

if [ "${OPT_USE_UV}" = true ]; then
  export UV_DEFAULT_INDEX="${INDEX_URL}"
  export UV_INDEX_URL="${INDEX_URL}"
  if [ -n "${TRUSTED_HOST}" ]; then
    export UV_INSECURE_HOST="${TRUSTED_HOST}"
  fi
  log_info "Running: ${UV_CMD[*]}"
  if ! "${UV_CMD[@]}"; then
    die 3 "uv tool install failed from: ${CHOSEN_SOURCE}"
  fi
  SPECIFY_BIN="$(uv tool dir 2>/dev/null)/bin/specify"
else
  log_info "Clean reinstall: removing any previous specify-cli"
  "${PIP_UNINSTALL_CMD[@]}" >/dev/null 2>&1 || true
  log_info "Running: ${PIP_INSTALL_CMD[*]}"
  if ! "${PIP_INSTALL_CMD[@]}"; then
    log_warn "pip install failed from: ${CHOSEN_SOURCE}"
    # fall through only when the failed source was from the fallback list
    if [ "${SOURCE_MODE}" != "fallback" ]; then
      die 3 "install failed from the single requested source: ${CHOSEN_SOURCE}"
    fi
    next=""
    idx=$((CHOSEN_INDEX))
    while [ "${idx}" -lt "${#SOURCE_SPECS[@]}" ]; do
      idx=$((idx + 1))
      spec="${SOURCE_SPECS[$((idx - 1))]}"
      if [ "${SOURCE_STATUSES[$((idx - 1))]}" = "unreachable" ]; then
        continue
      fi
      next="${spec}"
      CHOSEN_INDEX="${idx}"
      break
    done
    if [ -z "${next}" ]; then
      source_remediation
      exit 3
    fi
    log_warn "Retrying with next reachable source: ${next}"
    CHOSEN_SOURCE="${next}"
    PIP_INSTALL_CMD=("${PY_BIN}" -m pip install "${INSTALL_ARGS[@]}" "${CHOSEN_SOURCE}")
    log_info "Running: ${PIP_INSTALL_CMD[*]}"
    if ! "${PIP_INSTALL_CMD[@]}"; then
      source_remediation
      exit 3
    fi
  fi
  SPECIFY_BIN="${BIN_DIR}/specify"
fi

# --------------------------------------------------------------- verify ----
if [ ! -x "${SPECIFY_BIN}" ]; then
  die 5 "specify binary not found after install (expected: ${SPECIFY_BIN})"
fi
log_info "Verifying installation: ${SPECIFY_BIN} check"
if ! "${SPECIFY_BIN}" check; then
  die 5 "specify check failed — installation incomplete"
fi

if [ "${OPT_USE_UV}" = true ]; then
  log_info "Installed (uv tool): $(uv tool list 2>/dev/null | grep -i 'specify' || echo specify-cli)"
  log_info "Ensure the uv tool bin dir is on PATH: $(uv tool dir 2>/dev/null)/bin"
else
  log_info "Installed version: $("${PY_BIN}" -m pip show specify-cli 2>/dev/null | grep '^Version' || echo unknown)"
fi
log_info "Done. Binary: ${SPECIFY_BIN}"
