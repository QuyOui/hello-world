#!/usr/bin/env python3
"""
Interactive Workout Logger
"""

from workout_logger import WorkoutLogger

logger = WorkoutLogger()

# Initialize repo
logger.init_repo()

print("\n=== Workout Logger Ready ===\n")
print("I'm ready to log your workouts!")
print("Just provide the date, day, exercise, weight, and sets/reps.\n")

while True:
    try:
        print("\n--- Add New Workout ---")
        date = input("Date (e.g., 2/1/26): ").strip()
        day = input("Day (Upper A/B or Lower A/B): ").strip()
        exercise = input("Exercise: ").strip()
        weight = input("Weight: ").strip()
        sets_reps = input("Sets/Reps (e.g., 8,8,8,8): ").strip()
        notes = input("Notes (optional): ").strip()

        if date and day and exercise and weight and sets_reps:
            logger.add_workout(date, day, exercise, weight, sets_reps, notes)
            print("✓ Workout logged and committed!")
        else:
            print("Please fill in all required fields.")

    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        break
    except Exception as e:
        print(f"Error: {e}")
