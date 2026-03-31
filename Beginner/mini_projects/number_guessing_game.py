"""
Mini Project — Number Guessing Game
=====================================
A fun game where the computer picks a random number and the player guesses it.

Skills used: random module, loops, conditionals, input/output, functions
"""

import random


def play_game(min_val=1, max_val=100, max_attempts=7):
    """
    Run one round of the number guessing game.
    Returns True if the player won, False otherwise.
    """
    secret = random.randint(min_val, max_val)
    attempts = 0

    print(f"\n🎲 I'm thinking of a number between {min_val} and {max_val}.")
    print(f"   You have {max_attempts} attempts. Good luck!\n")

    while attempts < max_attempts:
        attempts_left = max_attempts - attempts
        print(f"  Attempts remaining: {attempts_left}")

        raw = input("  Your guess: ").strip()

        # Validate input
        try:
            guess = int(raw)
        except ValueError:
            print("  ⚠️  Please enter a whole number.\n")
            continue

        # Check bounds
        if guess < min_val or guess > max_val:
            print(f"  ⚠️  Please guess between {min_val} and {max_val}.\n")
            continue

        attempts += 1

        if guess == secret:
            print(f"\n  🎉 Correct! You guessed it in {attempts} attempt(s)!")
            if attempts == 1:
                print("  🏆 First try! Incredible!")
            elif attempts <= 3:
                print("  ⭐ Excellent guessing!")
            return True
        elif guess < secret:
            print("  📈 Too low! Try higher.\n")
        else:
            print("  📉 Too high! Try lower.\n")

    print(f"\n  😔 Out of attempts! The number was {secret}.")
    return False


def main():
    """Main loop — allows multiple rounds."""
    print("=" * 40)
    print("   🎮  NUMBER GUESSING GAME")
    print("=" * 40)

    wins = 0
    rounds = 0

    while True:
        won = play_game()
        rounds += 1
        if won:
            wins += 1

        print(f"\n  Score: {wins} win(s) out of {rounds} round(s)")

        again = input("\n  Play again? (y/n): ").strip().lower()
        if again != "y":
            print("\n  Thanks for playing! Goodbye 👋")
            break


if __name__ == "__main__":
    main()
