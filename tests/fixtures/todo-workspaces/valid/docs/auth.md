# Authentication Service

## Overview
The auth service handles user authentication and token management.

```SPECKIT TODO
Refactor authentication flow to support JWT tokens:
- Replace OAuth2 flow with JWT-based authentication
- Update login endpoint to return both access_token and refresh_token
- Add token validation middleware
- Update tests to verify JWT signature and expiration
```

## Current Implementation
Currently using OAuth2 with Google as the provider.
