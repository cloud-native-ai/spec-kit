# Contract: Safe Command Execution (Pure Bash Implementation)

## Overview
This document defines the contract for the system's ability to execute user-provided commands safely, handling special characters and Unicode text correctly. **The implementation will be in pure Bash, with no external dependencies.**

## Input
- **`user_prompt`**: A string containing the user's command, which may include any valid UTF-8 characters and Bash special characters. This input is received as a positional argument or via stdin to the Bash script.

## Output
- **`stdout`**: The standard output of the executed command, which should reflect the literal interpretation of the `user_prompt`.
- **`stderr`**: The standard error of the executed command, or an error message from the system if the input is invalid (e.g., too long, malformed UTF-8).
- **`exit_code`**: 0 for successful execution, non-zero for errors.

## Error Conditions
- **`INPUT_TOO_LONG`**: If the `user_prompt` exceeds 10,000 characters.
- **`INVALID_ENCODING`**: If the `user_prompt` contains invalid or malformed UTF-8 sequences. (The script will run with `LC_ALL=C.UTF-8` to enforce this).
- **`COMMAND_EXECUTION_FAILED`**: If the underlying command fails for reasons unrelated to input handling (e.g., command not found).

## Implementation Mechanism
- **Special Character Handling**: The script will use the Bash built-in `printf '%q'` to safely escape the `user_prompt` before execution.
- **Unicode Handling**: The script will ensure it runs in a `C.UTF-8` locale to correctly process and pass through Unicode characters.

## Examples

### Example 1: Special Characters
- **Input**: `echo "Price is $100 & it's 50% off!" | grep '50%'`
- **Expected Output (`stdout`)**: `Price is $100 & it's 50% off!`

### Example 2: Unicode Characters
- **Input**: `echo "Hello 世界! 👋"`
- **Expected Output (`stdout`)**: `Hello 世界! 👋`

### Example 3: Combined Input
- **Input**: `echo "The price in 中国 is $100 & it's 50% off! 🎉"`
- **Expected Output (`stdout`)**: `The price in 中国 is $100 & it's 50% off! 🎉`