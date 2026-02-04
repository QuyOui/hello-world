#!/usr/bin/env python3
"""
Quy's Workout Logger - GitHub Integration
Syncs workout data to GitHub repository
"""

import subprocess
import json
import os
from datetime import datetime
from pathlib import Path

class WorkoutLogger:
    def __init__(self, repo_name="workout-log"):
        self.repo_name = repo_name
        self.repo_path = Path(repo_name)
        self.log_file = self.repo_path / "workouts.json"

    def init_repo(self):
        """Initialize GitHub repo if it doesn't exist"""
        if not self.repo_path.exists():
            print(f"Creating repo directory: {self.repo_name}")
            self.repo_path.mkdir()
            os.chdir(self.repo_name)
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "config", "user.email", "workout@log.local"], check=True)
            subprocess.run(["git", "config", "user.name", "Workout Logger"], check=True)
            os.chdir("..")
        else:
            os.chdir(self.repo_name)
            subprocess.run(["git", "pull"], check=True)
            os.chdir("..")

    def load_workouts(self):
        """Load existing workouts from file"""
        if self.log_file.exists():
            with open(self.log_file) as f:
                return json.load(f)
        return {"workouts": []}

    def save_workouts(self, data):
        """Save workouts to file"""
        with open(self.log_file, 'w') as f:
            json.dump(data, f, indent=2)

    def add_workout(self, date, day, exercise, weight, sets_reps, notes=""):
        """Add a new workout entry"""
        data = self.load_workouts()

        workout = {
            "date": date,
            "day": day,
            "exercise": exercise,
            "weight": weight,
            "sets_reps": sets_reps,
            "notes": notes
        }

        data["workouts"].append(workout)
        self.save_workouts(data)

        # Commit to git
        os.chdir(self.repo_name)
        subprocess.run(["git", "add", "workouts.json"], check=True)
        subprocess.run(["git", "commit", "-m", f"Add workout: {exercise} on {date}"], check=True)
        os.chdir("..")

        print(f"✓ Added: {exercise} ({sets_reps}) on {date}")

    def view_workouts(self, limit=10):
        """View recent workouts"""
        data = self.load_workouts()
        workouts = data["workouts"][-limit:]

        print(f"\n{'Date':<12} {'Day':<10} {'Exercise':<25} {'Weight':<10} {'Sets/Reps':<15}")
        print("-" * 72)
        for w in workouts:
            print(f"{w['date']:<12} {w['day']:<10} {w['exercise']:<25} {w['weight']:<10} {w['sets_reps']:<15}")

    def get_current_weights(self):
        """Get latest weight for each exercise"""
        data = self.load_workouts()
        weights = {}

        for w in data["workouts"]:
            weights[w["exercise"]] = w["weight"]

        return weights


# Historical workout data
HISTORICAL_WORKOUTS = [
    {"date": "1/23/26", "day": "Upper A", "exercise": "Bench Press", "weight": "130", "sets_reps": "8,8,5,3", "notes": ""},
    {"date": "1/23/26", "day": "Upper A", "exercise": "Barbell Rows", "weight": "70", "sets_reps": "8,8,8,8", "notes": ""},
    {"date": "1/23/26", "day": "Upper A", "exercise": "Overhead Press", "weight": "65", "sets_reps": "8,8,5", "notes": ""},
    {"date": "1/23/26", "day": "Upper A", "exercise": "Chin-ups", "weight": "BW", "sets_reps": "4,4,4", "notes": "Shoulders fine"},
    {"date": "1/23/26", "day": "Upper A", "exercise": "Dumbbell Curls", "weight": "25", "sets_reps": "12,5,5", "notes": "Pre-fatigued"},
    {"date": "1/27/26", "day": "Upper B", "exercise": "Bench Press", "weight": "135", "sets_reps": "8,8,5,5", "notes": ""},
    {"date": "1/27/26", "day": "Upper B", "exercise": "Overhead Press", "weight": "65", "sets_reps": "9,8,6", "notes": ""},
    {"date": "1/27/26", "day": "Upper B", "exercise": "Underhand Barbell Rows", "weight": "65", "sets_reps": "10,10,12", "notes": ""},
    {"date": "1/27/26", "day": "Upper B", "exercise": "Overhead Tricep Ext", "weight": "35", "sets_reps": "12,12,8", "notes": ""},
    {"date": "1/27/26", "day": "Upper B", "exercise": "Hammer Curls", "weight": "25", "sets_reps": "12,10,8", "notes": ""},
    {"date": "1/29/26", "day": "Lower B", "exercise": "Romanian Deadlifts", "weight": "85", "sets_reps": "12,12,12,12", "notes": "Ready to increase"},
    {"date": "1/29/26", "day": "Lower B", "exercise": "Goblet Squats", "weight": "35", "sets_reps": "10,12,10", "notes": ""},
    {"date": "1/29/26", "day": "Lower B", "exercise": "Leg Curls", "weight": "55", "sets_reps": "12,12,12", "notes": ""},
    {"date": "1/29/26", "day": "Lower B", "exercise": "Leg Extensions", "weight": "60", "sets_reps": "15,15,15", "notes": "Ready to increase"},
    {"date": "1/29/26", "day": "Lower B", "exercise": "Standing Calf Raises", "weight": "125", "sets_reps": "20,20,20", "notes": ""},
    {"date": "1/31/26", "day": "Upper A", "exercise": "Bench Press", "weight": "130", "sets_reps": "8,8,8,8", "notes": ""},
    {"date": "1/31/26", "day": "Upper A", "exercise": "Barbell Rows", "weight": "70", "sets_reps": "12,12,9,9", "notes": ""},
    {"date": "1/31/26", "day": "Upper A", "exercise": "Overhead Press", "weight": "65", "sets_reps": "12,8,5", "notes": ""},
    {"date": "1/31/26", "day": "Upper A", "exercise": "Tricep Extension", "weight": "35", "sets_reps": "7,8,8", "notes": ""},
    {"date": "1/31/26", "day": "Upper A", "exercise": "Chin-ups", "weight": "BW", "sets_reps": "3,2,2,2", "notes": "Fatigued"},
    {"date": "1/31/26", "day": "Upper A", "exercise": "Dumbbell Curls", "weight": "25", "sets_reps": "8,8,8", "notes": ""},
]

if __name__ == "__main__":
    logger = WorkoutLogger()

    # Initialize repo
    print("Initializing workout logger...")
    logger.init_repo()

    # Load existing or create new
    data = logger.load_workouts()

    # If empty, populate with historical data
    if not data["workouts"]:
        print(f"Populating with {len(HISTORICAL_WORKOUTS)} historical workouts...")
        data["workouts"] = HISTORICAL_WORKOUTS
        logger.save_workouts(data)

        # Commit initial data
        os.chdir("workout-log")
        subprocess.run(["git", "add", "workouts.json"], check=True)
        subprocess.run(["git", "commit", "-m", "Initial workout history"], check=True)
        os.chdir("..")

    # Display current state
    logger.view_workouts(15)

    print("\n✓ Workout logger ready!")
    print("\nUsage:")
    print("  logger.add_workout('2/1/26', 'Lower A', 'Back Squats', '115', '8,8,8,8')")
    print("  logger.view_workouts()")
    print("  logger.get_current_weights()")
