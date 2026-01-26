"""
Workout Service
Business logic for workout plan generation and session management
"""

from typing import List, Dict, Optional
from datetime import date, timedelta
from sqlalchemy.orm import Session

from app.models import User, WorkoutPlan, WorkoutSession, FitnessProfile, PlanStatus


# Workout templates based on goal and level
WORKOUT_TEMPLATES = {
    "build_muscle": {
        "beginner": {
            "name": "Beginner Muscle Building",
            "plan_type": "3-day full body",
            "days": [
                {
                    "day": "monday",
                    "focus": "Full Body A",
                    "exercises": [
                        {"name": "Squats", "sets": 3, "reps": "10-12"},
                        {"name": "Bench Press", "sets": 3, "reps": "10-12"},
                        {"name": "Bent Over Rows", "sets": 3, "reps": "10-12"},
                        {"name": "Shoulder Press", "sets": 3, "reps": "10-12"},
                        {"name": "Bicep Curls", "sets": 2, "reps": "12-15"},
                    ]
                },
                {
                    "day": "wednesday",
                    "focus": "Full Body B",
                    "exercises": [
                        {"name": "Deadlifts", "sets": 3, "reps": "8-10"},
                        {"name": "Incline Dumbbell Press", "sets": 3, "reps": "10-12"},
                        {"name": "Lat Pulldowns", "sets": 3, "reps": "10-12"},
                        {"name": "Lunges", "sets": 3, "reps": "10 each"},
                        {"name": "Tricep Dips", "sets": 2, "reps": "12-15"},
                    ]
                },
                {
                    "day": "friday",
                    "focus": "Full Body C",
                    "exercises": [
                        {"name": "Leg Press", "sets": 3, "reps": "12-15"},
                        {"name": "Dumbbell Flyes", "sets": 3, "reps": "12-15"},
                        {"name": "Cable Rows", "sets": 3, "reps": "10-12"},
                        {"name": "Lateral Raises", "sets": 3, "reps": "12-15"},
                        {"name": "Plank", "sets": 3, "reps": "30-60 sec"},
                    ]
                }
            ]
        },
        "intermediate": {
            "name": "Intermediate Push-Pull-Legs",
            "plan_type": "push-pull-legs",
            "days": [
                {
                    "day": "monday",
                    "focus": "Push",
                    "exercises": [
                        {"name": "Bench Press", "sets": 4, "reps": "6-8"},
                        {"name": "Overhead Press", "sets": 4, "reps": "8-10"},
                        {"name": "Incline Dumbbell Press", "sets": 3, "reps": "10-12"},
                        {"name": "Tricep Pushdowns", "sets": 3, "reps": "12-15"},
                        {"name": "Lateral Raises", "sets": 3, "reps": "15"},
                    ]
                },
                {
                    "day": "tuesday",
                    "focus": "Pull",
                    "exercises": [
                        {"name": "Deadlifts", "sets": 4, "reps": "5"},
                        {"name": "Pull-ups", "sets": 4, "reps": "8-10"},
                        {"name": "Barbell Rows", "sets": 4, "reps": "8-10"},
                        {"name": "Face Pulls", "sets": 3, "reps": "15"},
                        {"name": "Barbell Curls", "sets": 3, "reps": "10-12"},
                    ]
                },
                {
                    "day": "thursday",
                    "focus": "Legs",
                    "exercises": [
                        {"name": "Squats", "sets": 4, "reps": "6-8"},
                        {"name": "Romanian Deadlifts", "sets": 4, "reps": "10-12"},
                        {"name": "Leg Press", "sets": 3, "reps": "12-15"},
                        {"name": "Leg Curls", "sets": 3, "reps": "12-15"},
                        {"name": "Calf Raises", "sets": 4, "reps": "15-20"},
                    ]
                }
            ]
        },
        "advanced": {
            "name": "Advanced 5-Day Split",
            "plan_type": "5-day body part split",
            "days": [
                {"day": "monday", "focus": "Chest", "exercises": [
                    {"name": "Bench Press", "sets": 5, "reps": "5"},
                    {"name": "Incline Press", "sets": 4, "reps": "8"},
                    {"name": "Cable Flyes", "sets": 4, "reps": "12"},
                ]},
                {"day": "tuesday", "focus": "Back", "exercises": [
                    {"name": "Deadlifts", "sets": 5, "reps": "3"},
                    {"name": "Weighted Pull-ups", "sets": 4, "reps": "6"},
                    {"name": "T-Bar Rows", "sets": 4, "reps": "8"},
                ]},
                {"day": "wednesday", "focus": "Shoulders", "exercises": [
                    {"name": "Military Press", "sets": 4, "reps": "6"},
                    {"name": "Arnold Press", "sets": 4, "reps": "10"},
                    {"name": "Rear Delt Flyes", "sets": 4, "reps": "15"},
                ]},
                {"day": "friday", "focus": "Legs", "exercises": [
                    {"name": "Squats", "sets": 5, "reps": "5"},
                    {"name": "Front Squats", "sets": 4, "reps": "8"},
                    {"name": "Leg Press", "sets": 4, "reps": "12"},
                ]},
                {"day": "saturday", "focus": "Arms", "exercises": [
                    {"name": "Barbell Curls", "sets": 4, "reps": "8"},
                    {"name": "Skull Crushers", "sets": 4, "reps": "10"},
                    {"name": "Hammer Curls", "sets": 3, "reps": "12"},
                ]}
            ]
        }
    },
    "lose_weight": {
        "beginner": {
            "name": "Beginner Fat Loss",
            "plan_type": "3-day circuit",
            "days": [
                {
                    "day": "monday",
                    "focus": "Circuit A",
                    "exercises": [
                        {"name": "Jumping Jacks", "sets": 3, "reps": "30 sec"},
                        {"name": "Bodyweight Squats", "sets": 3, "reps": "15"},
                        {"name": "Push-ups", "sets": 3, "reps": "10-12"},
                        {"name": "Mountain Climbers", "sets": 3, "reps": "30 sec"},
                        {"name": "Plank", "sets": 3, "reps": "30 sec"},
                    ]
                },
                {
                    "day": "wednesday",
                    "focus": "Circuit B",
                    "exercises": [
                        {"name": "Burpees", "sets": 3, "reps": "8-10"},
                        {"name": "Lunges", "sets": 3, "reps": "12 each"},
                        {"name": "Dumbbell Rows", "sets": 3, "reps": "12"},
                        {"name": "High Knees", "sets": 3, "reps": "30 sec"},
                        {"name": "Bicycle Crunches", "sets": 3, "reps": "20"},
                    ]
                },
                {
                    "day": "friday",
                    "focus": "Circuit C",
                    "exercises": [
                        {"name": "Box Jumps", "sets": 3, "reps": "10"},
                        {"name": "Kettlebell Swings", "sets": 3, "reps": "15"},
                        {"name": "Dips", "sets": 3, "reps": "8-10"},
                        {"name": "Jump Rope", "sets": 3, "reps": "60 sec"},
                        {"name": "Russian Twists", "sets": 3, "reps": "20"},
                    ]
                }
            ]
        },
        "intermediate": {
            "name": "Intermediate HIIT Program",
            "plan_type": "4-day HIIT",
            "days": [
                {"day": "monday", "focus": "HIIT Cardio", "exercises": [
                    {"name": "Sprint Intervals", "sets": 8, "reps": "30 sec on / 30 sec off"},
                    {"name": "Burpee Box Jumps", "sets": 4, "reps": "10"},
                    {"name": "Battle Ropes", "sets": 4, "reps": "30 sec"},
                ]},
                {"day": "tuesday", "focus": "Strength Circuit", "exercises": [
                    {"name": "Goblet Squats", "sets": 4, "reps": "12"},
                    {"name": "Push Press", "sets": 4, "reps": "10"},
                    {"name": "Renegade Rows", "sets": 3, "reps": "8 each"},
                ]},
                {"day": "thursday", "focus": "HIIT Cardio", "exercises": [
                    {"name": "Rowing Intervals", "sets": 6, "reps": "500m"},
                    {"name": "Sled Pushes", "sets": 4, "reps": "40m"},
                ]},
                {"day": "friday", "focus": "Strength Circuit", "exercises": [
                    {"name": "Deadlifts", "sets": 4, "reps": "8"},
                    {"name": "Dumbbell Thrusters", "sets": 4, "reps": "12"},
                    {"name": "Pull-ups", "sets": 3, "reps": "Max"},
                ]}
            ]
        },
        "advanced": {
            "name": "Advanced Metabolic Conditioning",
            "plan_type": "5-day metabolic",
            "days": [
                {"day": "monday", "focus": "AMRAP", "exercises": [
                    {"name": "Thrusters", "sets": 1, "reps": "21-15-9"},
                    {"name": "Pull-ups", "sets": 1, "reps": "21-15-9"},
                ]},
                {"day": "tuesday", "focus": "EMOM", "exercises": [
                    {"name": "Power Cleans", "sets": 10, "reps": "5"},
                    {"name": "Box Jumps", "sets": 10, "reps": "10"},
                ]},
                {"day": "thursday", "focus": "Chipper", "exercises": [
                    {"name": "Wall Balls", "sets": 1, "reps": "50"},
                    {"name": "Kettlebell Swings", "sets": 1, "reps": "40"},
                    {"name": "Burpees", "sets": 1, "reps": "30"},
                ]},
                {"day": "friday", "focus": "Intervals", "exercises": [
                    {"name": "Assault Bike", "sets": 8, "reps": "1 min on / 1 min off"},
                ]},
                {"day": "saturday", "focus": "Long WOD", "exercises": [
                    {"name": "Run", "sets": 1, "reps": "1 mile"},
                    {"name": "100 Air Squats", "sets": 1, "reps": "100"},
                    {"name": "Run", "sets": 1, "reps": "1 mile"},
                ]}
            ]
        }
    }
}


class WorkoutService:
    """Service for workout plan generation and session management."""

    def generate_plan(self, db: Session, user: User, weeks: int = 4) -> WorkoutPlan:
        """
        Generate a workout plan based on user's fitness profile.
        """
        profile = user.fitness_profile
        if not profile:
            raise ValueError("User must have a fitness profile")
        
        # Determine goal and level
        primary_goal = profile.goals[0] if profile.goals else "build_muscle"
        level = profile.fitness_level or "beginner"
        
        # Get template
        goal_templates = WORKOUT_TEMPLATES.get(primary_goal, WORKOUT_TEMPLATES["build_muscle"])
        template = goal_templates.get(level, goal_templates["beginner"])
        
        # Create plan
        plan = WorkoutPlan(
            user_id=user.id,
            name=template["name"],
            description=f"Auto-generated {template['plan_type']} plan for {primary_goal}",
            plan_data={"days": template["days"]},
            plan_type=template["plan_type"],
            target_goal=primary_goal,
            start_date=date.today(),
            end_date=date.today() + timedelta(weeks=weeks),
            status=PlanStatus.ACTIVE.value,
        )
        
        db.add(plan)
        db.commit()
        db.refresh(plan)
        
        return plan

    def get_user_plans(self, db: Session, user_id: str, status_filter: str = None) -> List[WorkoutPlan]:
        """Get all workout plans for a user."""
        query = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id)
        if status_filter:
            query = query.filter(WorkoutPlan.status == status_filter)
        return query.order_by(WorkoutPlan.created_at.desc()).all()

    def log_session(
        self,
        db: Session,
        user_id: str,
        session_date: date,
        duration_minutes: int = None,
        plan_id: str = None,
        notes: str = None,
        calories_burned: int = None,
        exercises_completed: int = None,
        energy_level: int = None,
        mood_after: int = None,
    ) -> WorkoutSession:
        """Log a workout session."""
        session = WorkoutSession(
            user_id=user_id,
            plan_id=plan_id,
            date=session_date,
            duration_minutes=duration_minutes,
            notes=notes,
            calories_burned=calories_burned,
            exercises_completed=exercises_completed,
            energy_level=energy_level,
            mood_after=mood_after,
        )
        
        db.add(session)
        db.commit()
        db.refresh(session)
        
        return session

    def get_user_sessions(
        self,
        db: Session,
        user_id: str,
        limit: int = 50,
        plan_id: str = None,
    ) -> List[WorkoutSession]:
        """Get workout sessions for a user."""
        query = db.query(WorkoutSession).filter(WorkoutSession.user_id == user_id)
        if plan_id:
            query = query.filter(WorkoutSession.plan_id == plan_id)
        return query.order_by(WorkoutSession.date.desc()).limit(limit).all()
