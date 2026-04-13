from sqlmodel import select
from app.database import get_cli_session
from app.models.workout import Workout

def seed_workouts():
    with get_cli_session() as session:
        # Check if data already exists
        existing = session.exec(select(Workout)).first()
        if existing:
            print("Workouts already seeded")
            return

        workouts = [
            Workout(
                name="Push Ups",
                description="Upper body strength exercise",
                duration=10,
                difficulty="Easy",
                muscle_group="Chest"
            ),
            Workout(
                name="Squats",
                description="Lower body strength exercise",
                duration=15,
                difficulty="Medium",
                muscle_group="Legs"
            ),
            Workout(
                name="Plank",
                description="Core stability exercise",
                duration=5,
                difficulty="Medium",
                muscle_group="Core"
            ),
            Workout(
                name="Jump Rope",
                description="Cardio endurance exercise",
                duration=20,
                difficulty="Hard",
                muscle_group="Full Body"
            ),
        ]

        session.add_all(workouts)
        session.commit()

        print("Workouts seeded successfully")