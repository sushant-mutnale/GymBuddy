# GymBuddy - ER Diagram

## Entity Relationship Diagram

```
┌───────────────────────────────────────┐
│                 USERS                 │
├───────────────────────────────────────┤
│ id (PK)          VARCHAR(36)          │
│ email            VARCHAR(255) UNIQUE  │
│ hashed_password  VARCHAR(255)         │
│ full_name        VARCHAR(100)         │
│ avatar_url       VARCHAR(500)         │
│ is_active        BOOLEAN              │
│ is_verified      BOOLEAN              │
│ is_superuser     BOOLEAN              │
│ created_at       DATETIME             │
│ updated_at       DATETIME             │
└───────────────────────────────────────┘
                    │
                    │ 1:1
                    ▼
┌───────────────────────────────────────┐
│           FITNESS_PROFILES            │
├───────────────────────────────────────┤
│ id (PK)          VARCHAR(36)          │
│ user_id (FK)     VARCHAR(36) UNIQUE   │──────┐
│ fitness_level    VARCHAR(20)          │      │
│ goals            JSON                 │      │
│ workout_types    JSON                 │      │
│ preferred_schedule VARCHAR(20)        │      │
│ preferred_days   JSON                 │      │
│ bio              TEXT                 │      │
│ preferred_gym_id VARCHAR(36) FK       │──┐   │
│ created_at       DATETIME             │  │   │
│ updated_at       DATETIME             │  │   │
└───────────────────────────────────────┘  │   │
                                           │   │
                    ┌──────────────────────┘   │
                    │ N:1                      │
                    ▼                          │
┌───────────────────────────────────────┐      │
│                 GYMS                  │      │
├───────────────────────────────────────┤      │
│ id (PK)          VARCHAR(36)          │      │
│ name             VARCHAR(200)         │      │
│ address          VARCHAR(500)         │      │
│ city             VARCHAR(100)         │      │
│ latitude         FLOAT                │      │
│ longitude        FLOAT                │      │
│ is_active        BOOLEAN              │      │
│ created_at       DATETIME             │      │
│ updated_at       DATETIME             │      │
└───────────────────────────────────────┘      │
                                               │
                                               │
    ┌──────────────────────────────────────────┘
    │
    ▼
  References users.id with ON DELETE CASCADE
```

## Relationships

| From | To | Type | Description |
|------|-----|------|-------------|
| users | fitness_profiles | 1:1 | Each user has one fitness profile |
| fitness_profiles | gyms | N:1 | Many profiles can reference one gym |

## Indexes

- `users.email` - Unique index for login lookup
- `users.id` - Primary key index
- `fitness_profiles.user_id` - Unique index for profile lookup
- `gyms.name` - Index for gym search
- `gyms.city` - Index for location filtering
