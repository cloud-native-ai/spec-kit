# Research Findings: Support for Complex Prompts and Unicode (Pure Bash)

## Decision: Use `printf '%q'` for safe argument passing

**Rationale**: The `printf '%q'` command in Bash is a built-in feature that formats its arguments in a way that they can be safely reused as shell input. It performs the necessary escaping and quoting to prevent command injection and misinterpretation of special characters. This is the pure-Bash equivalent of Python's `shlex.quote()` and directly addresses FR-003 and FR-004.

**Alternatives considered**:
- **Manual escaping with parameter expansion**: While possible, it's complex and error-prone to cover all edge cases correctly.
- **Using `eval` with careful quoting**: Highly discouraged due to significant security risks if not done perfectly.
- **External tools like `sed` or `awk`**: Unnecessary, as Bash provides a built-in, robust solution with `printf '%q'`.

## Decision: Enforce and rely on UTF-8 locale in Bash

**Rationale**: Bash, when run in a UTF-8 locale (e.g., `C.UTF-8` or `en_US.UTF-8`), can correctly handle and pass through Unicode characters. The existing `common.sh` script already includes a function `ensure_utf8_locale` which can be leveraged and enhanced. All string operations and file I/O within the script will respect the locale's encoding.

**Alternatives considered**:
- **Byte-level manipulation**: Complex and unnecessary, as the shell's locale handling is sufficient for passing data through to commands.
- **External iconv tool**: Adds an unnecessary dependency when the shell can handle it natively with the correct locale.

## Decision: Implement input validation with Bash built-ins

**Rationale**: To handle edge cases like input length (SC-004), Bash provides built-in parameter expansion for string length (`${#var}`) and pattern matching for basic validation. This allows for efficient and dependency-free input checking.

**Alternatives considered**:
- **Using `wc -c`**: Would require a subprocess and is less efficient for simple length checks.
- **Complex regex with `grep`**: Overkill for the simple validation needs (length and basic structure).
