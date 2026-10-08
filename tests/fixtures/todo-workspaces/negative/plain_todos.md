# Negative Test Cases

## Ordinary TODO comments (should be ignored)
TODO: Fix this bug
FIXME: Update this section
XXX: Review this code

## Code with TODO in comments
```python
# TODO: Add error handling
def process_data():
    pass
```

## Regular text mentioning TODO
The TODO list is on the project board.
See the TODO section in the README.

# SPECKIT TODO as a Markdown heading, not a comment block
Comment-form detection is disabled in Markdown-family files (D-9).

# speckit todo — wrong case, must not open a block

These should all be ignored since they're not SPECKIT TODO fenced blocks.
