"""
Mini Project — Student Grade Manager
======================================
A grade management system with:
  - Add students and their scores
  - Calculate average, highest, lowest scores
  - Assign letter grades
  - Generate class report
  - Save/load from JSON

Skills: OOP, statistics, file I/O, JSON, error handling
"""

import json
import os
import statistics


# Letter grade thresholds
GRADE_SCALE = [
    (90, "A"),
    (80, "B"),
    (70, "C"),
    (60, "D"),
    (0,  "F"),
]


def get_letter_grade(score: float) -> str:
    """Return the letter grade for a numeric score."""
    for threshold, letter in GRADE_SCALE:
        if score >= threshold:
            return letter
    return "F"


class Student:
    """Represents a student with a name and list of scores."""

    def __init__(self, name: str, scores: list = None):
        self.name   = name.strip().title()
        self.scores = scores or []

    def add_score(self, score: float):
        """Add a single score (0-100)."""
        if not 0 <= score <= 100:
            raise ValueError(f"Score must be between 0 and 100, got {score}")
        self.scores.append(round(float(score), 2))

    @property
    def average(self) -> float:
        """Calculate the average score."""
        if not self.scores:
            return 0.0
        return round(statistics.mean(self.scores), 2)

    @property
    def grade(self) -> str:
        """Return the letter grade based on the average score."""
        return get_letter_grade(self.average)

    @property
    def highest(self) -> float:
        return max(self.scores) if self.scores else 0.0

    @property
    def lowest(self) -> float:
        return min(self.scores) if self.scores else 0.0

    def to_dict(self) -> dict:
        return {"name": self.name, "scores": self.scores}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["name"], data["scores"])

    def __str__(self) -> str:
        return (
            f"{self.name:<20} Avg: {self.average:5.1f}  "
            f"Grade: {self.grade}  "
            f"Scores: {self.scores}"
        )


class GradeManager:
    """Manages a class of students and their grades."""

    def __init__(self, class_name: str, filepath: str = "grades.json"):
        self.class_name = class_name
        self.filepath   = filepath
        self.students: dict[str, Student] = {}
        self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    data = json.load(f)
                for entry in data.get("students", []):
                    s = Student.from_dict(entry)
                    self.students[s.name.lower()] = s
            except (json.JSONDecodeError, KeyError):
                pass

    def _save(self):
        with open(self.filepath, "w") as f:
            json.dump({
                "class": self.class_name,
                "students": [s.to_dict() for s in self.students.values()]
            }, f, indent=2)

    def add_student(self, name: str) -> Student:
        """Add a new student. Returns the Student object."""
        key = name.strip().lower()
        if key in self.students:
            print(f"  Student '{name}' already exists.")
            return self.students[key]
        student = Student(name)
        self.students[key] = student
        self._save()
        print(f"  ✅ Added student: {student.name}")
        return student

    def add_score(self, name: str, score: float):
        """Add a score for a student."""
        key = name.strip().lower()
        if key not in self.students:
            print(f"  ⚠️  Student '{name}' not found. Adding them first.")
            self.add_student(name)
        try:
            self.students[key].add_score(score)
            self._save()
            print(f"  ✅ Added score {score} for {self.students[key].name}")
        except ValueError as e:
            print(f"  ⚠️  {e}")

    def get_student(self, name: str):
        return self.students.get(name.strip().lower())

    def class_average(self) -> float:
        """Return the average score across ALL students."""
        all_scores = [s.average for s in self.students.values() if s.scores]
        return round(statistics.mean(all_scores), 2) if all_scores else 0.0

    def top_students(self, n: int = 3) -> list:
        """Return the top N students by average."""
        return sorted(self.students.values(), key=lambda s: s.average, reverse=True)[:n]

    def grade_distribution(self) -> dict:
        """Return count of each letter grade in the class."""
        dist = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
        for s in self.students.values():
            if s.scores:
                dist[s.grade] = dist.get(s.grade, 0) + 1
        return dist

    def print_report(self):
        """Print a formatted class report."""
        print("\n" + "=" * 60)
        print(f"  CLASS REPORT: {self.class_name}")
        print("=" * 60)

        if not self.students:
            print("  No students registered.")
            return

        # Student listing
        print(f"\n  {'STUDENT':<20} {'AVG':>6}  {'GRADE':<6}  SCORES")
        print("  " + "-" * 55)
        for s in sorted(self.students.values(), key=lambda x: x.average, reverse=True):
            scores_str = ", ".join(str(sc) for sc in s.scores) if s.scores else "No scores"
            print(f"  {s.name:<20} {s.average:>6.1f}  {s.grade:<6}  {scores_str}")

        # Class statistics
        print("\n  " + "-" * 55)
        print(f"  Class average: {self.class_average()}")

        top = self.top_students(1)
        if top:
            print(f"  Top student:   {top[0].name} ({top[0].average})")

        print(f"\n  Grade distribution: {self.grade_distribution()}")
        print("=" * 60)

    def run(self):
        """Interactive CLI for the grade manager."""
        print("=" * 45)
        print("     📊  STUDENT GRADE MANAGER")
        print("=" * 45)
        print(f"  Class: {self.class_name}")

        while True:
            print("\n  Commands: add | score | report | top | quit")
            cmd = input("  > ").strip().lower()

            if cmd == "quit":
                print("  Goodbye! 👋")
                break

            elif cmd == "add":
                name = input("  Student name: ").strip()
                self.add_student(name)

            elif cmd == "score":
                name = input("  Student name: ").strip()
                try:
                    score = float(input("  Score (0-100): "))
                    self.add_score(name, score)
                except ValueError:
                    print("  ⚠️  Invalid score.")

            elif cmd == "report":
                self.print_report()

            elif cmd == "top":
                try:
                    n = int(input("  How many top students? [3]: ") or "3")
                    tops = self.top_students(n)
                    print(f"\n  Top {n} students:")
                    for i, s in enumerate(tops, 1):
                        print(f"    {i}. {s.name}: {s.average} ({s.grade})")
                except ValueError:
                    print("  ⚠️  Invalid number.")

            else:
                print("  ⚠️  Unknown command.")


if __name__ == "__main__":
    manager = GradeManager("Python 101")
    manager.run()
