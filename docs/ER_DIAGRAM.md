# GymBuddy - Complete ER Diagram (v2)

This diagram outlines the complete database schema architecture encompassing Phase 1 through Phase 6 features including ML collaborative filtering matches, chat messaging, gym locations, and AI generated workout plans.

## Entity Relationship Diagram

```mermaid
erDiagram
    %% Users and Authentication
    users {
        string id PK
        string email UK
        string hashed_password
        string full_name
        string avatar_url
        boolean is_active
        boolean is_verified
        boolean is_superuser
        datetime created_at
        datetime updated_at
    }

    %% Fitness Profile Data
    fitness_profiles {
        string id PK
        string user_id FK "UK"
        string fitness_level
        json goals
        json workout_types
        string preferred_schedule
        json preferred_days
        text bio
        string preferred_gym_id FK
        datetime created_at
        datetime updated_at
    }

    match_preferences {
        string id PK
        string profile_id FK "UK"
        int max_distance_km
        json preferred_genders
        int min_age
        int max_age
        boolean require_same_gym
    }

    %% Locations
    gyms {
        string id PK
        string name
        string address
        string city
        float latitude
        float longitude
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    %% Features (Matches, Messages, Workouts)
    matches {
        string id PK
        string user1_id FK
        string user2_id FK
        string status "pending|accepted|rejected|active"
        int match_score "0-100 ML Correlation"
        datetime matched_at
        datetime updated_at
    }

    messages {
        string id PK
        string match_id FK
        string sender_id FK
        text content
        boolean is_read
        datetime created_at
    }

    workout_plans {
        string id PK
        string user_id FK
        string name
        string description
        json plan_data
        string plan_type
        string target_goal
        string status
        date start_date
        date end_date
        datetime created_at
        datetime updated_at
    }

    workout_sessions {
        string id PK
        string user_id FK
        string plan_id FK "Optional"
        date session_date
        int duration_minutes
        int calories_burned
        int exercises_completed
        int energy_level
        int mood_after
        text notes
        datetime created_at
    }

    %% Relationships Mapping
    users ||--o| fitness_profiles : "has"
    fitness_profiles ||--o| match_preferences : "configures"
    gyms ||--o{ fitness_profiles : "preferred by"

    users ||--o{ matches : "initiates/receives"
    matches ||--o{ messages : "contains"
    users ||--o{ messages : "sends"

    users ||--o{ workout_plans : "owns"
    users ||--o{ workout_sessions : "logs"
    workout_plans ||--o{ workout_sessions : "tracks"
```

## Description of Mappings

1. **Authentication Core:** `users` is the primary table. Upon registration, users get an entry. Secondary onboarding triggers the creation of `fitness_profiles` and `match_preferences` which act in a `1:1` relationship linking `user_id`.
2. **Geographical Features:** Physical `gyms` have a `1:N` relationship with User Profiles. Many users can set the same gym as their `preferred_gym_id`.
3. **Connections:** The ML matching engine calculates similarity and instantiates a `matches` table connecting `user1_id` and `user2_id`.
4. **Real-time Chat:** If a match achieves `active` status, WebSockets allow real-time creation of `messages` scoped to exactly one `match_id`.
5. **Workout Tracking:** The AI generates `workout_plans` which persist for 4-weeks. `workout_sessions` acts as an event log table tracking daily checks correlating to the overarching plan via `plan_id`.

## Indexes (Optimized for Query Performance)
- `users.email` - Unique index for JWT Auth login parsing.
- `fitness_profiles.user_id` - Fast indexed joins.
- `gyms.city`, `gyms.name` - Used in `/gyms` query parameters.
- `matches.user1_id`, `matches.user2_id` - Finding active chats.
- `messages.match_id` - Aggressive ordering and WebSocket bulk fetch.
