"""
Reads WorkoutBase.csv and inserts rows into the workout table.
Called once at app startup if the table is empty.
"""
import csv
import os
import logging
from sqlmodel import Session, select
from app.models.workout import Workout

logger = logging.getLogger(__name__)

# Look for CSV relative to the project root (one level above app/)
_HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(_HERE, "..", "..", "WorkoutBase.csv")


def seed_workouts(db: Session):
    existing = db.exec(select(Workout)).first()
    if existing:
        logger.info("Workouts already seeded — skipping.")
        return

    csv_path = os.path.abspath(CSV_PATH)
    if not os.path.exists(csv_path):
        logger.warning(f"WorkoutBase.csv not found at {csv_path}. Skipping seed.")
        return

    count = 0
    try:
        with open(csv_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Strip BOM / whitespace from all keys and values
                row = {k.strip(): v.strip() for k, v in row.items()}
                workout = Workout(
                    name=row["name"],
                    description=row["description"],
                    duration=int(row["duration"]),
                    difficulty=row["difficulty"],
                    muscle_group=row["muscle_group"],
                )
                db.add(workout)
                count += 1
        db.commit()
        logger.info(f"Seeded {count} workouts from WorkoutBase.csv")
    except Exception as e:
        logger.error(f"Seeder failed: {e}")
        db.rollback()
        raise
