# Data Model

## Entities

### User
**Description**: Represents a registered user in the system

**Fields**:
- `id`: UUID (Primary Key)
- `email`: string, unique, validated format
- `password_hash`: string, bcrypt hashed
- `first_name`: string, optional
- `last_name`: string, optional
- `created_at`: timestamp, UTC
- `updated_at`: timestamp, UTC
- `last_login`: timestamp, UTC, nullable
- `is_active`: boolean, default true
- `email_verified`: boolean, default false
- `data_retention_until`: timestamp, UTC (24 months from last activity)

**Validation Rules**:
- Email must be valid format and unique
- Password must be at least 8 characters
- First/last name limited to 100 characters each

### OAuthProvider
**Description**: Links users to their OAuth providers

**Fields**:
- `id`: UUID (Primary Key)
- `user_id`: UUID, foreign key to User.id
- `provider`: string (google, github, etc.)
- `provider_user_id`: string, unique per provider
- `access_token`: string, encrypted
- `refresh_token`: string, encrypted, nullable
- `expires_at`: timestamp, UTC, nullable
- `created_at`: timestamp, UTC
- `updated_at`: timestamp, UTC

**Validation Rules**:
- Combination of (user_id, provider) must be unique
- Provider must be from allowed list

### Session
**Description**: Tracks user sessions for authentication

**Fields**:
- `id`: UUID (Primary Key)
- `user_id`: UUID, foreign key to User.id
- `token`: string, unique, JWT format
- `ip_address`: string, nullable
- `user_agent`: string, nullable
- `created_at`: timestamp, UTC
- `expires_at`: timestamp, UTC
- `is_revoked`: boolean, default false

**Validation Rules**:
- Token must be unique
- expires_at must be after created_at

## Relationships

- **User** → **OAuthProvider** (One-to-Many): A user can have multiple OAuth provider links
- **User** → **Session** (One-to-Many): A user can have multiple active sessions
- **OAuthProvider** → **User** (Many-to-One): Each OAuth provider link belongs to one user
- **Session** → **User** (Many-to-One): Each session belongs to one user

## State Transitions

### User States
- **Created**: User registered but email not verified
- **Active**: Email verified and account active
- **Suspended**: Account temporarily disabled (admin action)
- **Deleted**: Account marked for deletion (soft delete)

### Session States
- **Active**: Valid session within expiration time
- **Expired**: Session past expiration time
- **Revoked**: Session explicitly invalidated by user or admin

## Indexes

- **Users**: email (unique), created_at, data_retention_until
- **OAuthProviders**: user_id, provider_user_id (unique compound)
- **Sessions**: user_id, token (unique), expires_at, is_revoked

## Constraints

- Soft delete pattern: Users are never hard-deleted, only marked as deleted
- Data retention: Records automatically purged after data_retention_until timestamp
- Referential integrity: All foreign key relationships enforced at database level
- Unique constraints: Email uniqueness, OAuth provider combinations, session tokens