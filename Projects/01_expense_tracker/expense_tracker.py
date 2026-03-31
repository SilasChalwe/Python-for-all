"""
Project — Expense Tracker
===========================
A full-featured command-line expense tracker with:
  - Add / delete expenses
  - Category management
  - Monthly summary with statistics
  - Persistent JSON storage
  - CSV export

Skills: OOP, dataclasses, JSON, CSV, datetime, statistics, CLI
"""

import json
import csv
import os
from datetime import datetime, date
from dataclasses import dataclass, field, asdict
from collections import defaultdict
from typing import Optional


CATEGORIES = ["food", "transport", "entertainment", "utilities", "health", "education", "other"]
DATA_FILE  = os.path.join(os.path.dirname(__file__), "expenses.json")


@dataclass
class Expense:
    """Represents a single expense entry."""
    id:          int
    description: str
    amount:      float
    category:    str
    date:        str   # ISO format: YYYY-MM-DD

    def __post_init__(self):
        self.amount = round(float(self.amount), 2)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def __str__(self) -> str:
        return (f"[{self.id:04d}] {self.date}  {self.description:<25} "
                f"${self.amount:>8.2f}  ({self.category})")


class ExpenseTracker:
    """Manages a collection of expenses with persistence."""

    def __init__(self, filepath: str = DATA_FILE):
        self.filepath = filepath
        self.expenses: list[Expense] = []
        self._next_id = 1
        self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    data = json.load(f)
                self.expenses = [Expense.from_dict(e) for e in data.get("expenses", [])]
                self._next_id = max((e.id for e in self.expenses), default=0) + 1
            except (json.JSONDecodeError, KeyError, TypeError):
                self.expenses = []

    def _save(self):
        with open(self.filepath, "w") as f:
            json.dump({"expenses": [e.to_dict() for e in self.expenses]}, f, indent=2)

    def add(self, description: str, amount: float, category: str,
            expense_date: str = None) -> Expense:
        """Add a new expense. Returns the created Expense."""
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        if category not in CATEGORIES:
            category = "other"
        expense_date = expense_date or date.today().isoformat()

        expense = Expense(
            id=self._next_id,
            description=description.strip(),
            amount=amount,
            category=category,
            date=expense_date,
        )
        self.expenses.append(expense)
        self._next_id += 1
        self._save()
        return expense

    def delete(self, expense_id: int) -> bool:
        """Delete an expense by ID. Returns True if found and deleted."""
        for i, e in enumerate(self.expenses):
            if e.id == expense_id:
                self.expenses.pop(i)
                self._save()
                return True
        return False

    def list_expenses(self, category: str = None, month: str = None) -> list:
        """Return filtered list of expenses."""
        result = self.expenses
        if category:
            result = [e for e in result if e.category == category]
        if month:
            result = [e for e in result if e.date.startswith(month)]
        return sorted(result, key=lambda e: e.date)

    def monthly_summary(self, month: str = None) -> dict:
        """Return a summary for the given month (YYYY-MM) or all time."""
        expenses = self.list_expenses(month=month)
        total    = sum(e.amount for e in expenses)

        by_category = defaultdict(float)
        for e in expenses:
            by_category[e.category] += e.amount

        return {
            "total":       round(total, 2),
            "count":       len(expenses),
            "by_category": dict(sorted(by_category.items(), key=lambda x: x[1], reverse=True)),
        }

    def export_csv(self, filepath: str):
        """Export all expenses to a CSV file."""
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "date", "description", "amount", "category"])
            writer.writeheader()
            for e in self.expenses:
                writer.writerow(e.to_dict())
        print(f"  Exported {len(self.expenses)} expenses to {filepath}")

    def print_list(self, expenses: list):
        """Print a formatted list of expenses."""
        if not expenses:
            print("  📭 No expenses found.")
            return
        total = sum(e.amount for e in expenses)
        print(f"\n  {'ID':<6} {'Date':<12} {'Description':<25} {'Amount':>9}  Category")
        print("  " + "-" * 65)
        for e in expenses:
            print(f"  {e}")
        print("  " + "-" * 65)
        print(f"  {'TOTAL':<43} ${total:>8.2f}")

    def print_summary(self, summary: dict, label: str = "All Time"):
        """Print a formatted summary."""
        print(f"\n  📊 EXPENSE SUMMARY — {label}")
        print("  " + "-" * 40)
        print(f"  Total spent:  ${summary['total']:>10.2f}")
        print(f"  Transactions: {summary['count']:>10}")
        print("\n  By category:")
        for cat, amount in summary["by_category"].items():
            pct  = amount / summary["total"] * 100 if summary["total"] else 0
            bar  = "█" * int(pct / 3)
            print(f"    {cat:<15} ${amount:>8.2f}  ({pct:4.1f}%) {bar}")

    def run(self):
        """Run the interactive CLI."""
        print("=" * 50)
        print("     💰  EXPENSE TRACKER")
        print("=" * 50)

        while True:
            print("\n  Commands: add | list | summary | delete | export | quit")
            cmd = input("  > ").strip().lower()

            if cmd == "quit":
                print("  Goodbye! 👋")
                break

            elif cmd == "add":
                try:
                    desc   = input("  Description: ").strip()
                    amount = float(input("  Amount ($):  "))
                    print(f"  Categories: {', '.join(CATEGORIES)}")
                    cat    = input("  Category:    ").strip().lower()
                    dt     = input("  Date [today]: ").strip() or date.today().isoformat()
                    e = self.add(desc, amount, cat, dt)
                    print(f"\n  ✅ Added: {e}")
                except ValueError as err:
                    print(f"  ⚠️  {err}")

            elif cmd == "list":
                cat   = input("  Filter by category (or blank for all): ").strip().lower() or None
                month = input("  Filter by month YYYY-MM (or blank):    ").strip() or None
                self.print_list(self.list_expenses(category=cat, month=month))

            elif cmd == "summary":
                month = input("  Month YYYY-MM (or blank for all time): ").strip() or None
                label = month or "All Time"
                self.print_summary(self.monthly_summary(month), label)

            elif cmd == "delete":
                self.print_list(self.list_expenses())
                try:
                    eid = int(input("  Enter ID to delete: "))
                    if self.delete(eid):
                        print(f"  🗑️  Deleted expense #{eid}")
                    else:
                        print(f"  ⚠️  ID {eid} not found.")
                except ValueError:
                    print("  ⚠️  Invalid ID.")

            elif cmd == "export":
                path = input("  Export filename [expenses.csv]: ").strip() or "expenses.csv"
                self.export_csv(path)

            else:
                print("  ⚠️  Unknown command.")


if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.run()
