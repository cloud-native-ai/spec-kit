#!/usr/bin/env bash

set -e

# Load common helpers for Unicode support and shared functions

# script-interface: the sourceable guard block (086) lives in script-interface.sh
# It sits above this script's own parsing and above `source common.sh`: a shared
# library's top-level checks would otherwise turn `--help` into a non-zero exit, and
# the flags must win over any write. Authority: .specify/shared/definitions/
# script-interface-definitions.md section 4.
SCRIPT_INTERFACE_LIB="$(CDPATH="" cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/script-interface.sh"
if [ -f "$SCRIPT_INTERFACE_LIB" ]; then
    # shellcheck source=/dev/null
    . "$SCRIPT_INTERFACE_LIB"
    script_interface_guard entry
    script_interface_guard define name="$0" \
        usage="[--json] [--short-name <name>] [--force] [<feature_description>]" \
        effects="creates a feature branch and scaffolds requirements.md; the flags write nothing" \
        codes="0 created or answered; 1 a prerequisite is missing; 2 an unrecognized option" \
        writes=--force \
        -- --json --short-name --force
    script_interface_guard guard "$@"
fi

main() {

    # The caller's own LC_ALL, captured before any helper can rewrite it. An explicit pin is
    # a deliberate choice about character classification, so the UTF-8 convenience below must
    # not silently override it (upstream acf43471b, "respect LC_ALL").
    local caller_lc_all="${LC_ALL:-}"

    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ -f "$SCRIPT_DIR/common.sh" ]; then
        # shellcheck source=/dev/null
        source "$SCRIPT_DIR/common.sh"
        # Ensure UTF-8 locale for better Unicode handling — unless the caller pinned LC_ALL.
        if [ -z "$caller_lc_all" ]; then
            ensure_utf8_locale || true
        fi
    fi

    # Fallback: if common.sh wasn't sourced or locale still isn't UTF-8, set a UTF-8 locale.
    # Skipped when the caller pinned LC_ALL, for the same reason as above.
    if [ -z "$caller_lc_all" ] && ! locale 2>/dev/null | grep -qi 'utf-8'; then
        if locale -a 2>/dev/null | grep -qi '^C\.utf8\|^C\.UTF-8$'; then
            export LC_ALL=C.UTF-8
            export LANG=C.UTF-8
        elif locale -a 2>/dev/null | grep -qi '^en_US\.utf8\|^en_US\.UTF-8$'; then
            export LC_ALL=en_US.UTF-8
            export LANG=en_US.UTF-8
        fi
    fi

    JSON_MODE=false
    SHORT_NAME=""
    FORCE=false
    END_OPTS=0
    ARGS=()
    i=1
    while [ $i -le $# ]; do
        arg="${!i}"
        if [ "$END_OPTS" = "1" ]; then
            ARGS+=("$arg")
            i=$((i + 1))
            continue
        fi
        case "$arg" in
            --json) 
                JSON_MODE=true 
                ;;
            --force)
                FORCE=true
                ;;
            --short-name)
                if [ $((i + 1)) -gt $# ]; then
                    echo 'Error: --short-name requires a value' >&2
                    exit 1
                fi
                i=$((i + 1))
                next_arg="${!i}"
                # Check if the next argument is another option (starts with --)
                if [[ "$next_arg" == --* ]]; then
                    echo 'Error: --short-name requires a value' >&2
                    exit 1
                fi
                SHORT_NAME="$next_arg"
                ;;
            --help|-h) 
                echo "Usage: $0 [--json] [--short-name <name>] [<feature_description>]"
                echo ""
                echo "Options:"
                echo "  --json              Output in JSON format"
                echo "  --short-name <name> Provide a custom short name (2-4 words) for the branch"
                echo "  --force             Overwrite an existing requirements.md with the template"
                echo "                      (default: no-clobber — an existing spec file is kept)"
                echo "  --help, -h          Show this help message"
                echo ""
                echo "Behavior:"
                echo "  - If feature_description is provided as argument, creates a new feature specification"
                echo "  - If no arguments provided but input is available on stdin, creates a new feature specification from stdin content"
                echo ""
                echo "Examples:"
                echo "  $0 'Add user authentication system' --short-name 'user-auth'"
                echo "  $0 'Implement OAuth2 integration for API'"
                echo "  echo 'Price is \$100' | $0 --json"
                exit 0
                ;;
            --)
                END_OPTS=1
                ;;
            *) 
                ARGS+=("$arg") 
                ;;
        esac
        i=$((i + 1))
    done

    FEATURE_DESCRIPTION="${ARGS[*]}"

    # Read from stdin if available, regardless of arguments
    STDIN_INPUT=""
    if [ ! -t 0 ]; then
        STDIN_INPUT=$(cat)
    fi

    # Combine arguments and stdin
    if [ -n "$FEATURE_DESCRIPTION" ] && [ -n "$STDIN_INPUT" ]; then
        # Both provided: use newline separator
        FEATURE_DESCRIPTION="$FEATURE_DESCRIPTION"$'\n\n'"$STDIN_INPUT"
    elif [ -z "$FEATURE_DESCRIPTION" ] && [ -n "$STDIN_INPUT" ]; then
        # Only stdin provided
        FEATURE_DESCRIPTION="$STDIN_INPUT"
    fi

    if [ -z "$FEATURE_DESCRIPTION" ]; then
        echo "Usage: $0 [--json] [--short-name <name>] <feature_description>" >&2
        exit 1
    fi

    # A description of only whitespace is no description (upstream 6757c90db). The test is
    # non-mutating on purpose: master combines argv and stdin into one possibly multi-line
    # description, so upstream's per-line `sed` trim would also strip the indentation of
    # every interior line and corrupt the Markdown that lands in requirements.md.
    # printf keeps an option-like description ("-n"/"-e"/"-E") text, not options
    # (upstream 5eb3d1478 + 3be2bd9b4).
    if [ -z "$(printf '%s' "$FEATURE_DESCRIPTION" | tr -d '[:space:]')" ]; then
        echo "Error: Feature description cannot be empty or contain only whitespace" >&2
        exit 1
    fi

    # True when stdin carries a byte outside ASCII printable+control, i.e. non-ASCII text.
    # LC_ALL=C makes the class byte-wise so the answer does not depend on the locale.
    contains_non_ascii() {
        LC_ALL=C grep -q '[^[:print:][:cntrl:]]'
    }

    # Pick the locale used for Unicode character classification. POSIX [:alnum:] differs by
    # platform, so a candidate is accepted only when it demonstrably keeps a non-ASCII letter
    # and replaces a non-letter (upstream acf43471b). An explicit caller pin is the only
    # candidate; otherwise the UTF-8 locale selected above is preferred.
    UNICODE_LOCALE=""
    local locale_candidates=("C.UTF-8" "C.utf8" "en_US.UTF-8" "en_US.utf8" "${LC_CTYPE:-${LANG:-}}")
    if [ -n "$caller_lc_all" ]; then
        locale_candidates=("$caller_lc_all")
    fi
    local locale_candidate
    for locale_candidate in "${locale_candidates[@]}"; do
        if [ -n "$locale_candidate" ] &&
            [ "$(printf 'é。' | LC_ALL="$locale_candidate" sed 's/[^[:alnum:]]/-/g' 2>/dev/null)" = 'é-' ]; then
            UNICODE_LOCALE="$locale_candidate"
            break
        fi
    done
    if [ -z "$UNICODE_LOCALE" ]; then
        # No usable UTF-8 locale. ASCII names still work on the shell fast path; a Unicode
        # name cannot be classified correctly, so say so instead of emitting a degenerate
        # suffix such as "045-" (upstream acf43471b).
        UNICODE_LOCALE=C
        if printf '%s' "${SHORT_NAME:-$FEATURE_DESCRIPTION}" | contains_non_ascii; then
            if [ -n "$caller_lc_all" ]; then
                echo "Error: A UTF-8 locale is required to create a Unicode feature name; LC_ALL=$caller_lc_all is not usable" >&2
            else
                echo "Error: A UTF-8 locale is required to create a Unicode feature name" >&2
            fi
            exit 1
        fi
    fi

    # Split a name into words, replacing every character that is not a Unicode letter or
    # decimal digit with the separator. Non-ASCII text is classified by Python 3 because
    # POSIX character classes vary across platforms and locales; pure ASCII stays on the
    # shell fast path so an ASCII name needs no interpreter at all. LC_ALL=C on that path
    # keeps [^a-z0-9] a byte range rather than a collation range, which in a UTF-8 locale
    # would let accented lowercase letters survive (upstream acf43471b + 18ea13fdc).
    # SPECKIT_PYTHON is this project's interpreter override convention (run-tests.sh).
    unicode_words() {
        local name="${1//$'\n'/ }"
        local separator="$2"
        if printf '%s' "$name" | contains_non_ascii; then
            local python_cmd=""
            local override="${SPECKIT_PYTHON:-}"
            if [ -n "$override" ] && command -v "$override" >/dev/null 2>&1 &&
                "$override" -c 'import sys; raise SystemExit(sys.version_info.major != 3)' >/dev/null 2>&1; then
                python_cmd="$override"
            elif command -v python3 >/dev/null 2>&1; then
                python_cmd="python3"
            fi
            if [ -z "$python_cmd" ]; then
                echo "Error: Python 3 is required to create a Unicode feature name" >&2
                return 1
            fi
            printf '%s' "$name" | "$python_cmd" -c '
import sys
value = sys.stdin.buffer.read().decode("utf-8")
lower = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")
result = "".join(
    char if char.isalpha() or char.isdecimal() else sys.argv[1]
    for char in value.translate(lower)
)
sys.stdout.buffer.write(result.encode("utf-8"))
' "$separator"
        else
            printf '%s' "$name" | LC_ALL=C tr '[:upper:]' '[:lower:]' | LC_ALL=C sed "s/[^a-z0-9]/$separator/g"
        fi
    }

    # Clean an explicit --short-name into a branch suffix. `--*` rather than the GNU-only
    # `\+`, which POSIX/BSD sed reads as a literal '+' and so leaves repeated separators
    # uncollapsed on macOS (upstream 18ea13fdc).
    clean_branch_name() {
        local name="$1"
        local cleaned
        cleaned=$(unicode_words "$name" '-') || return 1
        printf '%s\n' "$cleaned" | sed 's/--*/-/g' | sed 's/^-//' | sed 's/-$//'
    }

    # Byte length of a name. GitHub's branch-name limit is measured in BYTES, and a Unicode
    # suffix holds fewer characters than bytes (upstream acf43471b).
    branch_byte_count() {
        printf '%s' "$1" | wc -c | tr -d '[:space:]'
    }

    # Escape a string for safe embedding in a JSON value (RFC 8259): backslash and quote
    # first, then the named control escapes, then any remaining U+0001-U+001F encoded as
    # \uXXXX — encoded, never stripped, so the value round-trips (upstream 9c0c1446e +
    # 2e55bdd3f). Defined here because no escaper is reachable from this script: common.sh
    # publishes none, and common-todo.sh keeps json_escape_string inside its own main(),
    # which sourcing does not publish.
    json_escape() {
        local s="$1"
        s="${s//\\/\\\\}"
        s="${s//\"/\\\"}"
        s="${s//$'\n'/\\n}"
        s="${s//$'\t'/\\t}"
        s="${s//$'\r'/\\r}"
        s="${s//$'\b'/\\b}"
        s="${s//$'\f'/\\f}"
        # LC_ALL=C makes ${#s} count bytes and ${s:$i:1} yield single bytes, so multi-byte
        # UTF-8 sequences pass through intact instead of being split into \u escapes.
        # U+0000 cannot appear in a bash string, hence the code >= 1 guard.
        local LC_ALL=C
        local i char code
        for (( i=0; i<${#s}; i++ )); do
            char="${s:$i:1}"
            printf -v code '%d' "'$char" 2>/dev/null || code=256
            if (( code >= 1 && code <= 31 )); then
                printf '\\u%04x' "$code"
            else
                printf '%s' "$char"
            fi
        done
    }

    # Function to find the repository root by searching for existing project markers
    find_repo_root() {
        local dir="$1"
        while [ "$dir" != "/" ]; do
            if [ -d "$dir/.git" ] || [ -d "$dir/.specify" ]; then
                echo "$dir"
                return 0
            fi
            dir="$(dirname "$dir")"
        done
        return 1
    }

    # Search upward for the `.specify` marker only — spec-kit's own project marker.
    # The path is normalised to absolute first so a relative start cannot loop forever,
    # and `cd --` tolerates a directory name that begins with '-' (upstream b1ba97297).
    find_specify_root() {
        local dir="${1:-$(pwd)}"
        dir="$(CDPATH="" cd -- "$dir" 2>/dev/null && pwd)" || return 1
        local prev_dir=""
        while true; do
            if [ -d "$dir/.specify" ]; then
                printf '%s\n' "$dir"
                return 0
            fi
            if [ "$dir" = "/" ] || [ "$dir" = "$prev_dir" ]; then
                break
            fi
            prev_dir="$dir"
            dir="$(dirname "$dir")"
        done
        return 1
    }

    # Resolve the repository root. The `.specify` marker outranks git: when spec-kit is
    # initialised in a subdirectory of a larger repository, `git rev-parse --show-toplevel`
    # answers with the OUTER root and the scaffold would land in the wrong project
    # (upstream b1ba97297). Git stays the second choice so a plain git repository without
    # `.specify` resolves exactly as before, and the marker walk from the script's own
    # directory remains the last resort for --no-git projects.
    #
    # This resolution is local to this script on purpose: common.sh publishes the host
    # library's git-first `git_repo_root`, a different contract owned elsewhere, and that
    # helper is left untouched.
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    REPO_ROOT="$(find_specify_root "$(pwd)" || true)"
    if [ -z "$REPO_ROOT" ] && git rev-parse --show-toplevel >/dev/null 2>&1; then
        REPO_ROOT=$(git rev-parse --show-toplevel)
    fi
    if [ -z "$REPO_ROOT" ]; then
        REPO_ROOT="$(find_repo_root "$SCRIPT_DIR" || true)"
    fi
    if [ -z "$REPO_ROOT" ]; then
        echo "Error: Could not determine repository root. Please run this script from within the repository." >&2
        exit 1
    fi

    # Git counts as available only when the resolved root is itself a work tree. A parent
    # repository's git must not create branches on behalf of a nested non-git project
    # (upstream b1ba97297 `has_git`). `.git` may be a file, as in worktrees and submodules.
    HAS_GIT=false
    if command -v git >/dev/null 2>&1 && [ -e "$REPO_ROOT/.git" ] &&
        git -C "$REPO_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        HAS_GIT=true
    fi

    cd "$REPO_ROOT"

    SPECS_DIR="$REPO_ROOT/.specify/specs"
    mkdir -p "$SPECS_DIR"

    # Derive the next feature number. Number sources (each keeps its number
    # reserved — missing any of them can reuse a number):
    #   1. top-level spec dirs under .specify/specs/
    #   2. archived spec dirs under .specify/specs/.archive/ (archived specs keep
    #      their numbers; a globally-max archived number would otherwise collide)
    #   3. git branch names in the exact top-level <NNN>-<slug> form. For remote
    #      branches exactly ONE remote-name segment is stripped first; slash-
    #      namespaced branches (e.g. origin/community/4059-*, origin/fix/4198-*)
    #      are NOT spec numbering — their trailing digits must be excluded, or
    #      the next number gets inflated (e.g. 200 instead of 045).
    HIGHEST=0
    consider_number_candidate() {
        local name="$1"
        local number
        # ERE '+' rather than the GNU-only BRE '\+', which POSIX/BSD grep does not
        # guarantee — the same portability defect as the sed separator collapse below
        # (upstream 18ea13fdc; upstream's own numbering uses `grep -Eo '^[0-9]+'`).
        number=$(printf '%s' "$name" | grep -Eo '^[0-9]+' || echo "0")
        number=$((10#$number))
        if [ "$number" -gt "$HIGHEST" ]; then HIGHEST=$number; fi
    }
    if [ -d "$SPECS_DIR" ]; then
        for dir in "$SPECS_DIR"/* "$SPECS_DIR"/.archive/*; do
            [ -d "$dir" ] || continue
            consider_number_candidate "$(basename "$dir")"
        done
    fi
    if [ "$HAS_GIT" = true ]; then
        # Local branches: top-level form only (any slash → not spec numbering).
        while IFS= read -r branch; do
            [ -n "$branch" ] || continue
            case "$branch" in */*) continue ;; esac
            consider_number_candidate "$branch"
        done < <(git branch --format='%(refname:short)' 2>/dev/null)
        # Remote branches: strip exactly the remote-name segment, then apply the
        # same top-level rule (a remaining slash means slash-namespaced → skip).
        while IFS= read -r branch; do
            [ -n "$branch" ] || continue
            branch="${branch#*/}"
            case "$branch" in */*) continue ;; esac
            consider_number_candidate "$branch"
        done < <(git branch -r --format='%(refname:short)' 2>/dev/null)
    fi

    NEXT=$((HIGHEST + 1))
    FEATURE_NUM=$(printf "%03d" "$NEXT")

    # Function to generate branch name with stop word filtering and length filtering
    generate_branch_name() {
        local description="$1"

        # Common stop words to filter out
        local stop_words="^(i|a|an|the|to|for|of|in|on|at|by|with|from|is|are|was|were|be|been|being|have|has|had|do|does|did|will|would|should|could|can|may|might|must|shall|this|that|these|those|my|your|our|their|want|need|add|get|set)$"

        # Lowercase and split into words, keeping Unicode letters and digits instead of
        # stripping every non-ASCII character (which left a Chinese description with an
        # empty suffix). A UTF-8 locale is needed for character-safe length checks
        # (upstream acf43471b).
        local -x LC_ALL="$UNICODE_LOCALE"
        local clean_name
        clean_name=$(unicode_words "$description" ' ') || return 1

        # Filter words: remove stop words and words shorter than 3 chars (unless they're
        # uppercase acronyms in original, or non-ASCII words, which are often 1-2 characters)
        local meaningful_words=()
        local word
        for word in $clean_name; do
            # Skip empty words
            [ -z "$word" ] && continue

            # Keep words that are NOT stop words AND (length >= 3 OR non-ASCII OR acronyms).
            # The stop-word probe is case-sensitive under LC_ALL=C: the words are already
            # lowercased, and ASCII word boundaries match the Python twin's lookarounds.
            if ! printf '%s\n' "$word" | LC_ALL=C grep -qE "$stop_words"; then
                if [ ${#word} -ge 3 ] || printf '%s' "$word" | contains_non_ascii; then
                    meaningful_words+=("$word")
                # Keep short words that appear as an uppercase acronym in the original.
                # Uppercase via tr and match with grep -qw (both portable) rather than
                # bash 4+ "^^" case expansion (a "bad substitution" on macOS bash 3.2) and
                # "\b" (which BSD grep reads as a backspace, so the probe silently failed).
                # Adapted from upstream 4038d370b.
                elif printf '%s' "$description" | LC_ALL=C grep -qw -- "$(printf '%s' "$word" | LC_ALL=C tr '[:lower:]' '[:upper:]')"; then
                    meaningful_words+=("$word")
                fi
            fi
        done

        # If we have meaningful words, use first 3-4 of them
        if [ ${#meaningful_words[@]} -gt 0 ]; then
            local max_words=3
            if [ ${#meaningful_words[@]} -eq 4 ]; then max_words=4; fi

            local result=""
            local count=0
            for word in "${meaningful_words[@]}"; do
                if [ $count -ge $max_words ]; then break; fi
                if [ -n "$result" ]; then result="$result-"; fi
                result="$result$word"
                count=$((count + 1))
            done
            printf '%s\n' "$result"
        else
            # Fallback to original logic if no meaningful words found: first three cleaned
            # tokens, Unicode included, so a non-Latin description still yields a suffix.
            local fallback
            fallback=$(clean_branch_name "$description") || return 1
            printf '%s\n' "$fallback" | tr '-' '\n' | grep -v '^$' | head -3 | tr '\n' '-' | sed 's/-$//'
        fi
    }

    # Fit "<NNN>-<suffix>" inside GitHub's 244-BYTE branch-name limit. The bound is bytes,
    # not characters, so the truncation point is a binary search over character counts
    # measured in bytes — `cut -c` would overshoot on a multi-byte suffix and could also
    # split a character (upstream acf43471b). The prefix length is computed rather than
    # assumed to be 4, so a four-digit feature number still fits.
    fit_branch_name() {
        local feature_num="$1"
        local branch_suffix="$2"
        local branch_name="${feature_num}-${branch_suffix}"
        local max_branch_length=244

        if [ "$(branch_byte_count "$branch_name")" -le "$max_branch_length" ]; then
            printf '%s' "$branch_name"
            return 0
        fi

        local prefix_length=$(( ${#feature_num} + 1 ))
        local max_suffix_length=$((max_branch_length - prefix_length))
        local -x LC_ALL="$UNICODE_LOCALE"
        local low=0 high=${#branch_suffix} mid
        if [ "$high" -gt "$max_suffix_length" ]; then
            high=$max_suffix_length
        fi
        while [ "$low" -lt "$high" ]; do
            mid=$(( (low + high + 1) / 2 ))
            if [ "$(branch_byte_count "${branch_suffix:0:$mid}")" -le "$max_suffix_length" ]; then
                low=$mid
            else
                high=$((mid - 1))
            fi
        done
        local truncated_suffix="${branch_suffix:0:$low}"
        truncated_suffix="${truncated_suffix%-}"
        printf '%s' "${feature_num}-${truncated_suffix}"
    }

    # Generate branch name
    if [ -n "$SHORT_NAME" ]; then
        # Use provided short name, just clean it up
        BRANCH_SUFFIX=$(clean_branch_name "$SHORT_NAME")
    else
        # Generate from description with smart filtering
        # Truncate to first 500 chars to avoid performance issues with very long descriptions
        BRANCH_DESC_SHORT="${FEATURE_DESCRIPTION:0:500}"
        BRANCH_SUFFIX=$(generate_branch_name "$BRANCH_DESC_SHORT")
    fi

    # An empty suffix would silently produce a degenerate branch name such as "045-".
    # Warn and point at the remedy; the scaffold still proceeds (upstream 8629796da,
    # wording updated by acf43471b now that letters need not be ASCII).
    if [ -z "$BRANCH_SUFFIX" ]; then
        echo "[specify] Warning: Feature name is empty after removing unsupported characters. Use --short-name with letters or digits (for example, user-auth)." >&2
    fi

    BRANCH_NAME="${FEATURE_NUM}-${BRANCH_SUFFIX}"

    # GitHub enforces a 244-byte limit on branch names: validate and truncate if necessary.
    ORIGINAL_BRANCH_NAME="$BRANCH_NAME"
    BRANCH_NAME=$(fit_branch_name "$FEATURE_NUM" "$BRANCH_SUFFIX")
    if [ "$BRANCH_NAME" != "$ORIGINAL_BRANCH_NAME" ]; then
        >&2 echo "[specify] Warning: Branch name exceeded GitHub's 244-byte limit"
        >&2 echo "[specify] Original: $ORIGINAL_BRANCH_NAME ($(branch_byte_count "$ORIGINAL_BRANCH_NAME") bytes)"
        >&2 echo "[specify] Truncated to: $BRANCH_NAME ($(branch_byte_count "$BRANCH_NAME") bytes)"
    fi

    if [ "$HAS_GIT" = true ]; then
        # In JSON mode, prevent any git messages from polluting output
        if $JSON_MODE; then
            if ! git checkout -b "$BRANCH_NAME" >/dev/null 2>&1; then
                >&2 echo "[specify] Error: Failed to create and switch to branch '$BRANCH_NAME'"
                exit 1
            fi
        elif ! git checkout -b "$BRANCH_NAME" 2>/dev/null; then
            # Name the actual remedy: an existing branch is a different problem from a git
            # misconfiguration (upstream 6757c90db). Upstream also suggests --number, which
            # this script does not offer, so that half of the message is not carried over.
            if git branch --list "$BRANCH_NAME" | grep -q .; then
                >&2 echo "Error: Branch '$BRANCH_NAME' already exists. Please use a different feature name."
            else
                >&2 echo "Error: Failed to create git branch '$BRANCH_NAME'. Please check your git configuration and try again."
            fi
            exit 1
        fi
    else
        >&2 echo "[specify] Warning: Git repository not detected; skipped branch creation for $BRANCH_NAME"
    fi

    REQUIREMENTS_DIR="$SPECS_DIR/$BRANCH_NAME"
    mkdir -p "$REQUIREMENTS_DIR"

    TEMPLATE="$REPO_ROOT/.specify/templates/requirements-template.md"
    SPEC_FILE="$REQUIREMENTS_DIR/requirements.md"
    if [ -f "$SPEC_FILE" ] && [ "$FORCE" != true ]; then
        # No-clobber guard: re-entering the flow on an existing spec dir (e.g. a
        # manually scaffolded spec) MUST NOT destroy the existing specification.
        >&2 echo "[specify] Warning: $SPEC_FILE already exists — kept unchanged (no-clobber). Pass --force to overwrite with the template."
    elif [ -f "$TEMPLATE" ]; then 
        cp "$TEMPLATE" "$SPEC_FILE"

        # Replace placeholder with actual description
        # Use python for robust multi-line string replacement if available
        if command -v python3 >/dev/null 2>&1; then
            export SPEC_CONTENT="$FEATURE_DESCRIPTION"
            # The path travels through the environment too: interpolating it into the
            # Python source would break on a repository path containing a quote, the same
            # quoting hazard the JSON escaping below closes (upstream 9c0c1446e family).
            export SPEC_PATH="$SPEC_FILE"
            # We use python to avoid sed/awk escaping hell with multiline complex text
            # The template contains literal "$ARGUMENTS" which we replace with the content
            python3 -c "import sys, os; content=os.environ.get('SPEC_CONTENT', ''); path=os.environ['SPEC_PATH']; template=open(path, encoding='utf-8').read(); open(path, 'w', encoding='utf-8').write(template.replace('\$ARGUMENTS', content))"
        fi
    else 
        touch "$SPEC_FILE"
        # printf, not echo: a description of "-n"/"-e"/"-E" is text, not an option
        # (upstream 5eb3d1478 + 3be2bd9b4).
        printf '%s\n' "$FEATURE_DESCRIPTION" > "$SPEC_FILE"
    fi

    # Set the SPECIFY_FEATURE environment variable for the current session
    export SPECIFY_FEATURE="$BRANCH_NAME"

    if $JSON_MODE; then
        # Values are JSON-escaped; the key names and their order are this script's contract
        # with its consumers and are unchanged (upstream 9c0c1446e + 2e55bdd3f).
        printf '{"BRANCH_NAME":"%s","SPEC_FILE":"%s","FEATURE_NUM":"%s"}\n' \
            "$(json_escape "$BRANCH_NAME")" \
            "$(json_escape "$SPEC_FILE")" \
            "$(json_escape "$FEATURE_NUM")"
    else
        echo "BRANCH_NAME: $BRANCH_NAME"
        echo "SPEC_FILE: $SPEC_FILE"
        echo "FEATURE_NUM: $FEATURE_NUM"
        echo "SPECIFY_FEATURE environment variable set to: $BRANCH_NAME"
    fi

}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    main "$@"
fi
