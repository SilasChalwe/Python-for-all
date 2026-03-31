"""
Mini Project — Command-Line To-Do App
=======================================
A persistent to-do list application with:
  - Add / remove / complete tasks
  - List tasks (with optional filter)
  - Save/load from JSON file
  - Task priorities

Skills: OOP, file I/O, JSON, error handling, CLI
"""

import json
import os
from datetime import datetime


class Task:
    """Represents a single to-do task."""

    PRIORITIES = {"low": 1, "medium": 2, "high": 3}

    def __init__(self, title: str, priority: str = "medium", done: bool = False, created: str = None):
        self.title    = title.strip()
        self.priority = priority.lower() if priority.lower() in self.PRIORITIES else "medium"
        self.done     = done
        self.created  = created or datetime.now().strftime("%Y-%m-%d %H:%M")

    def complete(self):
        """Mark this task as done."""
        self.done = True

    def to_dict(self) -> dict:
        return {
            "title":    self.title,
            "priority": self.priority,
            "done":     self.done,
            "created":  self.created,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def __str__(self) -> str:
        status = "✅" if self.done else "⬜"
        prio   = f"[{self.priority.upper()}]"
        return f"{status} {prio:<8} {self.title}  ({self.created})"


class TodoApp:
    """Command-line To-Do application."""

    def __init__(self, filepath: str = "todos.json"):
        self.filepath = filepath
        self.tasks: list[Task] = []
        self._load()

    def _load(self):
        """Load tasks from JSON file if it exists."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    data = json.load(f)
                self.tasks = [Task.from_dict(t) for t in data]
            except (json.JSONDecodeError, KeyError):
                self.tasks = []

    def _save(self):
        """Persist all tasks to JSON file."""
        with open(self.filepath, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)

    def add(self, title: str, priority: str = "medium"):
        """Add a new task."""
        if not title.strip():
            print("  ⚠️  Task title cannot be empty.")
            return
        task = Task(title, priority)
        self.tasks.append(task)
        self._save()
        print(f"  ✅ Added: '{task.title}'")

    def remove(self, index: int):
        """Remove a task by 1-based index."""
        if 1 <= index <= len(self.tasks):
            removed = self.tasks.pop(index - 1)
            self._save()
            print(f"  🗑️  Removed: '{removed.title}'")
        else:
            print(f"  ⚠️  Invalid task number: {index}")

    def complete(self, index: int):
        """Mark a task as completed by 1-based index."""
        if 1 <= index <= len(self.tasks):
            self.tasks[index - 1].complete()
            self._save()
            print(f"  ✅ Completed: '{self.tasks[index - 1].title}'")
        else:
            print(f"  ⚠️  Invalid task number: {index}")

    def list_tasks(self, show_all: bool = True):
        """Display tasks, optionally filtered to pending only."""
        filtered = self.tasks if show_all else [t for t in self.tasks if not t.done]
        if not filtered:
            print("  📭 No tasks found.")
            return
        # Sort by priority (high first), then by creation time
        sorted_tasks = sorted(
            filtered,
            key=lambda t: (-Task.PRIORITIES.get(t.priority, 0), t.created)
        )
        print(f"\n  {'#':<3} Task")
        print("  " + "-" * 55)
        for i, task in enumerate(sorted_tasks, start=1):
            print(f"  {i:<3} {task}")
        pending = sum(1 for t in self.tasks if not t.done)
        print(f"\n  {pending}/{len(self.tasks)} tasks pending")

    def run(self):
        """Start the interactive CLI."""
        print("=" * 45)
        print("         📝  TO-DO APP")
        print("=" * 45)
        self.list_tasks()

        while True:
            print("\n  Commands: add | done | remove | list | pending | quit")
            cmd = input("  > ").strip().lower()

            if cmd == "quit":
                print("  Goodbye! 👋")
                break

            elif cmd == "add":
                title    = input("  Task title:   ").strip()
                priority = input("  Priority (low/medium/high) [medium]: ").strip() or "medium"
                self.add(title, priority)

            elif cmd in ("done", "complete"):
                self.list_tasks()
                try:
                    idx = int(input("  Task number to complete: "))
                    self.complete(idx)
                except ValueError:
                    print("  ⚠️  Please enter a valid number.")

            elif cmd == "remove":
                self.list_tasks()
                try:
                    idx = int(input("  Task number to remove: "))
                    self.remove(idx)
                except ValueError:
                    print("  ⚠️  Please enter a valid number.")

            elif cmd == "list":
                self.list_tasks(show_all=True)

            elif cmd == "pending":
                self.list_tasks(show_all=False)

            else:
                print("  ⚠️  Unknown command.")


if __name__ == "__main__":
    app = TodoApp()
    app.run()
