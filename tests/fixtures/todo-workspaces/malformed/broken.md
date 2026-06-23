# Malformed TODO blocks for testing error handling

## Unclosed fence
```SPECKIT TODO
This block has no closing fence
The content continues
But never closes


## Nested fence attempt
```markdown
Some code
```SPECKIT TODO
This TODO is inside another fence
Should be detected as malformed


## Unparseable content
```SPECKIT TODO
```
This opening fence is immediately closed
Malformed by definition
