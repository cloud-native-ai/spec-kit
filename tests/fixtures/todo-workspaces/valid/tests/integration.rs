// Integration tests for the API
use reqwest;

#[tokio::test]
async fn test_user_creation() {
    // ...
}

```SPECKIT TODO
Expand integration test coverage:
- Add tests for error cases (404, 500, etc.)
- Test concurrent request handling
- Verify database transaction rollback on failure
- Add performance benchmarks for high-load scenarios
```
