# 💰 Expense Tracker

A command-line expense tracking application.

## Features
- Add expenses with category, amount, description, and date
- List all expenses with optional category filtering
- Monthly summary with totals per category
- Delete expenses
- Persistent storage using JSON
- Export to CSV

## Usage
```bash
python expense_tracker.py
```

## Commands
```
add      → Add a new expense
list     → List all expenses (or by category)
summary  → Monthly summary
delete   → Delete an expense by ID
export   → Export to CSV
quit     → Exit
```

## Example
```
> add
  Description: Coffee
  Amount: 3.50
  Category (food/transport/entertainment/utilities/other): food
  Date [today]: 

✅ Added: Coffee — $3.50 (food) on 2024-01-15
```
