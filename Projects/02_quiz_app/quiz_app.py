"""
Project — Quiz App
====================
A command-line quiz application with:
  - Multiple choice questions from JSON
  - Score tracking
  - Optional question timer
  - Randomized question order
  - Difficulty filtering
  - Detailed end-of-quiz review

Skills: OOP, JSON, dataclasses, datetime, random, CLI
"""

import json
import os
import sys
import random
import time
from dataclasses import dataclass
from typing import Optional


DEFAULT_QUESTIONS = os.path.join(os.path.dirname(__file__), "questions.json")


@dataclass
class Question:
    """Represents a single quiz question."""
    question:   str
    options:    list
    answer:     int         # 0-based index of correct option
    difficulty: str = "easy"
    category:   str = "General"

    @property
    def correct_option(self) -> str:
        return self.options[self.answer]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            question   = data["question"],
            options    = data["options"],
            answer     = int(data["answer"]),
            difficulty = data.get("difficulty", "easy"),
            category   = data.get("category", "General"),
        )


class QuizSession:
    """Manages a single quiz session."""

    def __init__(self, questions: list, time_limit: Optional[int] = None):
        self.questions    = questions
        self.time_limit   = time_limit   # seconds per question, or None
        self.answers      = []           # (question, user_answer_idx, is_correct)
        self.start_time   = None
        self.end_time     = None

    @property
    def score(self) -> int:
        return sum(1 for _, _, correct in self.answers if correct)

    @property
    def total(self) -> int:
        return len(self.questions)

    @property
    def percentage(self) -> float:
        return (self.score / self.total * 100) if self.total else 0.0

    @property
    def elapsed(self) -> float:
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0

    def run(self):
        """Run the quiz interactively."""
        self.start_time = time.perf_counter()

        for i, question in enumerate(self.questions, start=1):
            self._display_question(i, question)
            user_answer = self._get_answer(len(question.options))
            is_correct  = user_answer == question.answer

            self.answers.append((question, user_answer, is_correct))

            if is_correct:
                print("  ✅ Correct!\n")
            else:
                print(f"  ❌ Wrong! Correct answer: ({question.answer + 1}) {question.correct_option}\n")

        self.end_time = time.perf_counter()

    def _display_question(self, number: int, q: Question):
        """Print a question with its options."""
        diff_emoji = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}.get(q.difficulty, "⚪")
        print(f"\n  Q{number}/{self.total}  [{q.category}] {diff_emoji}")
        print(f"  {q.question}")
        print()
        for j, option in enumerate(q.options, start=1):
            print(f"    {j}. {option}")
        print()

    def _get_answer(self, max_option: int) -> int:
        """Get and validate user's answer. Returns 0-based index."""
        while True:
            raw = input(f"  Your answer (1-{max_option}): ").strip()
            try:
                idx = int(raw) - 1   # convert to 0-based
                if 0 <= idx < max_option:
                    return idx
                print(f"  ⚠️  Please enter a number between 1 and {max_option}.")
            except ValueError:
                print("  ⚠️  Invalid input. Enter a number.")

    def print_results(self):
        """Print the final quiz results and review."""
        print("\n" + "=" * 55)
        print("  QUIZ RESULTS")
        print("=" * 55)
        print(f"  Score:      {self.score} / {self.total}")
        print(f"  Percentage: {self.percentage:.1f}%")
        print(f"  Time taken: {self.elapsed:.1f}s")

        # Grade
        if self.percentage >= 90:
            grade, emoji = "A", "🏆"
        elif self.percentage >= 80:
            grade, emoji = "B", "⭐"
        elif self.percentage >= 70:
            grade, emoji = "C", "👍"
        elif self.percentage >= 60:
            grade, emoji = "D", "📚"
        else:
            grade, emoji = "F", "💪"

        print(f"  Grade:      {grade} {emoji}")

        # Detailed review
        print("\n  --- Review ---")
        for i, (q, user_idx, correct) in enumerate(self.answers, start=1):
            status = "✅" if correct else "❌"
            print(f"  {status} Q{i}: {q.question[:50]}...")
            if not correct:
                print(f"       You chose: ({user_idx + 1}) {q.options[user_idx]}")
                print(f"       Correct:    ({q.answer + 1}) {q.correct_option}")

        print("=" * 55)


class QuizApp:
    """Main quiz application."""

    def __init__(self, questions_file: str = DEFAULT_QUESTIONS):
        self.questions_file = questions_file
        self.all_questions  = self._load_questions()

    def _load_questions(self) -> list:
        """Load questions from JSON file."""
        if not os.path.exists(self.questions_file):
            print(f"⚠️  Questions file not found: {self.questions_file}")
            return []
        with open(self.questions_file, "r") as f:
            data = json.load(f)
        return [Question.from_dict(q) for q in data]

    def _select_questions(self, difficulty: str = None, count: int = None) -> list:
        """Filter and sample questions."""
        questions = self.all_questions
        if difficulty and difficulty != "all":
            questions = [q for q in questions if q.difficulty == difficulty]
        random.shuffle(questions)
        if count:
            questions = questions[:count]
        return questions

    def run(self):
        """Run the interactive quiz application."""
        print("=" * 50)
        print("     🧠  PYTHON QUIZ APP")
        print("=" * 50)
        print(f"  Total questions available: {len(self.all_questions)}")

        while True:
            print("\n  Options:")
            print("  1. Start quiz")
            print("  2. Quiz by difficulty")
            print("  3. View categories")
            print("  4. Quit")

            choice = input("\n  Choice (1-4): ").strip()

            if choice == "4":
                print("  Thanks for playing! 👋")
                break

            elif choice == "3":
                categories = {}
                for q in self.all_questions:
                    categories[q.category] = categories.get(q.category, 0) + 1
                print("\n  Categories:")
                for cat, count in sorted(categories.items()):
                    print(f"    {cat}: {count} questions")

            elif choice in ("1", "2"):
                difficulty = None
                if choice == "2":
                    print("  Difficulties: easy / medium / hard / all")
                    difficulty = input("  Select difficulty: ").strip().lower()

                try:
                    raw_count = input("  How many questions? [all]: ").strip()
                    count = int(raw_count) if raw_count else None
                except ValueError:
                    count = None

                questions = self._select_questions(difficulty, count)
                if not questions:
                    print("  ⚠️  No questions match your criteria.")
                    continue

                print(f"\n  Starting quiz with {len(questions)} questions...")
                print("  Press Enter to begin...")
                input()

                session = QuizSession(questions)
                session.run()
                session.print_results()

            else:
                print("  ⚠️  Invalid choice.")


if __name__ == "__main__":
    qfile = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_QUESTIONS
    app = QuizApp(qfile)
    app.run()
