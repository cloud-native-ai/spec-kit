# Data Model: Support for Complex Prompts and Unicode (Pure Bash Context)

## Concept: UserInput

**Description**: In the context of a pure Bash implementation, there is no formal "entity" like in object-oriented languages. Instead, the user's input is treated as a raw string variable that must be processed with care.

### Input Constraints (Derived from Requirements)

- **`user_input`**: A shell variable containing the raw string provided by the user.
  - **Format**: Plain text string.
  - **Encoding**: Must be valid UTF-8. The script will operate in a UTF-8 locale to ensure correct handling.
  - **Content**: Can contain any character, including all Bash special characters (`$`, `"`, `'`, `\`, `|`, `;`, `&`, `*`, `?`, etc.).
  - **Length**: Maximum length of 10,000 characters (to align with SC-004).

### Processing Rules

- **FR-001 & FR-002**: The `user_input` variable, when used in a UTF-8 locale, will preserve all Unicode characters.
- **FR-003 & FR-004**: Before `user_input` is used in any command context, it **MUST** be passed through `printf '%q'` to generate a safely escaped version for execution.
- **SC-004**: The script must check `${#user_input}` and reject inputs longer than 10,000 characters.
- **Edge Case Handling**: The script should use `LC_ALL=C.UTF-8` to ensure consistent behavior and gracefully handle invalid UTF-8 by returning an error.