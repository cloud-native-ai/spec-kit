# Quick Start: Testing Complex Prompt and Unicode Support

This guide provides a quick way to verify that the implementation of the "Support for Complex Prompts and Unicode" feature is working correctly.

## Prerequisites
- A Linux environment with Bash.
- The `spec-kit` repository checked out on the `003-support-complex-unicode` branch.

## Test Commands

Run the following commands to test the key aspects of the feature. The expected output is shown after each command.

### Test 1: Basic Special Characters
```bash
# Command
echo 'echo "Price is $100 & it'\''s 50% off!"' | .specify/scripts/bash/create-new-feature.sh --json

# Expected stdout (JSON output)
# {"command_executed":true,"stdout":"Price is $100 & it's 50% off!","stderr":"","exit_code":0}
```

### Test 2: Basic Unicode
```bash
# Command
echo 'echo "Hello 世界! 👋"' | .specify/scripts/bash/create-new-feature.sh

# Expected stdout
Hello 世界! 👋
```

### Test 3: Combined Special Characters and Unicode
```bash
# Command
echo 'echo "The price in 中国 is $100 & it'\''s 50% off! 🎉"' | .specify/scripts/bash/create-new-feature.sh --json

# Expected stdout (JSON output)
# {"command_executed":true,"stdout":"The price in 中国 is $100 & it's 50% off! 🎉","stderr":"","exit_code":0}
```

### Test 4: Very Long Input (Edge Case)
```bash
# Command (This should fail gracefully)
LONG_INPUT=$(printf 'A%.0s' {1..10001}) # Creates a string of 10001 'A's
echo "echo '$LONG_INPUT'" | .specify/scripts/bash/create-new-feature.sh --json

# Expected behavior: The system should reject the input with an error message about exceeding maximum length
```

### Test 5: Invalid UTF-8 (Edge Case)
```bash
# Command (This should fail gracefully)
INVALID_UTF8=$(printf '\377\376')
echo "echo '$INVALID_UTF8'" | .specify/scripts/bash/create-new-feature.sh --json

# Expected behavior: The system should reject the input with an error message about invalid UTF-8 sequences
```

## Verification
For each test, inspect the output to ensure that:
1. The special characters are not interpreted by the shell (e.g., `$100` is not treated as a variable).
2. The Unicode characters are displayed correctly.
3. The combined input is handled correctly.
4. The system rejects inputs that exceed 10,000 characters.
5. The system rejects inputs with invalid UTF-8 sequences.
6. The system does not crash on edge cases.

If all tests pass as expected, the feature implementation meets all success criteria (SC-001 to SC-005).