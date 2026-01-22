# GymBuddy - System Design Document

## Overview
GymBuddy is an AI-powered gym partner matching app that uses collaborative filtering to recommend workout partners.

## Architecture

### High-Level Architecture
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   Frontend      │────▶│   FastAPI       │────▶│   SQLite/       │
│   (Next.js)     │     │   Backend       │     │   PostgreSQL    │
│                 │◀────│                 │◀────│                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
     Client              REST API + JWT              Database
```

### Tech Stack Choice

#### Why FastAPI?
- **Performance**: Built on Starlette/Pydantic, one of fastest Python frameworks
- **Type Safety**: Native type hints with automatic validation
- **Auto Docs**: Swagger/OpenAPI documentation out of the box
- **Async Support**: Ready for high-concurrency workloads
- **ML Integration**: Easy to integrate scikit-learn for recommendations

#### Why Relational DB (SQLite → PostgreSQL)?
- **Structured Data**: User profiles, gym data have clear relationships
- **ACID Compliance**: Critical for user auth and transactions
- **Migrations**: Alembic provides robust schema versioning
- **Scalability**: Easy migration path to PostgreSQL in production

## Authentication Structure

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   Client    │───▶│   /auth/*    │───▶│   bcrypt    │
│             │    │   endpoints  │    │   hashing   │
└─────────────┘    └──────────────┘    └─────────────┘
                          │
                          ▼
                   ┌──────────────┐
                   │   JWT Token  │
                   │   (HS256)    │
                   └──────────────┘
                          │
                          ▼
                   ┌──────────────┐
                   │  Protected   │
                   │  Endpoints   │
                   └──────────────┘
```

### Auth Flow
1. **Register**: Email + password → bcrypt hash → store in DB
2. **Login**: Validate credentials → issue JWT (access + refresh)
3. **Protected Routes**: Bearer token → decode JWT → get_current_user dependency
4. **Refresh**: Use refresh token to get new access token

### Token Structure
- **Access Token**: 30 min expiry, type="access"
- **Refresh Token**: 7 days expiry, type="refresh"
- **Payload**: user_id (sub), email, exp, type

## Database Schema

See ER Diagram: `docs/er_diagram.md`

## API Endpoints

| Prefix | Endpoints | Auth Required |
|--------|-----------|---------------|
| `/auth` | register, login, refresh | No |
| `/users` | me (GET/PUT), /{id} | Yes (except public profile) |
| `/profiles` | me (GET/PUT) | Yes |

## Future Considerations
- PostgreSQL for production
- Redis for token blacklisting
- Celery for async ML jobs
- WebSocket for real-time chat
