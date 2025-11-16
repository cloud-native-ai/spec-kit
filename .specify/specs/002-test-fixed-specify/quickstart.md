# Quick Start Guide

## Prerequisites

- Python 3.11 or higher
- PostgreSQL 14 or higher
- Docker and Docker Compose (optional, for containerized deployment)

## Local Development Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-org/your-project.git
cd your-project
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the project root:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/your_database
SECRET_KEY=your-secret-key-here
JWT_EXPIRATION_MINUTES=60
OAUTH_GOOGLE_CLIENT_ID=your-google-client-id
OAUTH_GITHUB_CLIENT_ID=your-github-client-id
```

### 5. Initialize the database
```bash
# Run database migrations
python -m alembic upgrade head

# Or if using raw SQL setup
psql -f scripts/init_db.sql
```

### 6. Start the development server
```bash
uvicorn src.main:app --reload --port 8000
```

## Core User Journeys

### Register a new user
```bash
curl -X POST http://localhost:8000/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securePassword123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Log in with email/password
```bash
curl -X POST http://localhost:8000/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securePassword123"
  }'
```

### Get current user profile (requires authentication)
```bash
curl -X GET http://localhost:8000/v1/users/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Update user profile
```bash
curl -X PATCH http://localhost:8000/v1/users/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane"
  }'
```

### Log out (invalidate session)
```bash
curl -X POST http://localhost:8000/v1/auth/logout \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Testing

Run all tests:
```bash
pytest
```

Run unit tests only:
```bash
pytest tests/unit/
```

Run contract tests:
```bash
pytest tests/contract/
```

## Key Implementation Details

- **Authentication**: JWT tokens with 60-minute expiration
- **Password Security**: bcrypt hashing with salt
- **Database**: PostgreSQL with connection pooling
- **API Documentation**: Automatic OpenAPI docs at `/docs`
- **Error Handling**: Standardized error responses with error codes
- **Validation**: Pydantic models for request/response validation

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `SECRET_KEY` | JWT signing secret | Required |
| `JWT_EXPIRATION_MINUTES` | Token expiration time | 60 |
| `OAUTH_GOOGLE_CLIENT_ID` | Google OAuth client ID | Optional |
| `OAUTH_GITHUB_CLIENT_ID` | GitHub OAuth client ID | Optional |

## Next Steps

1. Implement email verification workflow
2. Add password reset functionality
3. Set up monitoring and logging
4. Configure production deployment
5. Add rate limiting for authentication endpoints