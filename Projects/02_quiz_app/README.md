# 🧠 Quiz App

A feature-rich command-line quiz application.

## Features
- Multiple choice questions loaded from JSON
- Score tracking and percentage display
- Optional timer per question
- Randomized question order
- Difficulty levels
- End-of-quiz detailed review

## Usage
```bash
python quiz_app.py
# or specify a custom question file:
python quiz_app.py questions.json
```

## Question Format (questions.json)
```json
[
  {
    "question": "What is 2 + 2?",
    "options": ["3", "4", "5", "6"],
    "answer": 1,
    "difficulty": "easy",
    "category": "math"
  }
]
```
The `answer` field is the 0-based index of the correct option.
