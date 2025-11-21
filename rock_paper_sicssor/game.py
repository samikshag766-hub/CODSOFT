
"""Simple Rock-Paper-Scissors console game.

Features:
- Prompt user for rock/paper/scissors (accepts full words or r/p/s)
- Random computer choice
- Determine winner and show reason
- Track scores across rounds
- Ask to play again
- Non-interactive --test mode to run automated rounds for verification
"""
import random
import sys

CHOICES = ["rock", "paper", "scissors"]

def normalize_choice(s: str):
    if not s:
        return None
    s = s.strip().lower()
    if s in ("r", "rock"):
        return "rock"
    if s in ("p", "paper"):
        return "paper"
    if s in ("s", "scissors", "scissor"):
        return "scissors"
    return None

def get_computer_choice():
    return random.choice(CHOICES)

def determine_winner(user: str, comp: str):
    """Return (winner, reason) where winner is 'user'|'computer'|'tie'."""
    if user == comp:
        return "tie", f"Both chose {user}."

    wins = {
        ("rock", "scissors"): "Rock crushes Scissors",
        ("scissors", "paper"): "Scissors cut Paper",
        ("paper", "rock"): "Paper covers Rock",
    }

    if (user, comp) in wins:
        return "user", wins[(user, comp)]
    else:
        # find reason from reversed pair
        reason = wins.get((comp, user), f"{comp.capitalize()} beats {user}")
        return "computer", reason

def prompt_user_choice():
    prompt = "Choose [r]ock, [p]aper or [s]cissors: "
    while True:
        try:
            raw = input(prompt)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting game.")
            return None
        choice = normalize_choice(raw)
        if choice:
            return choice
        print("Invalid choice. Type 'rock', 'paper', or 'scissors' (or r/p/s).\n")

def yes_no_prompt(prompt: str, default_yes=True):
    suffix = "[Y/n]" if default_yes else "[y/N]"
    while True:
        try:
            resp = input(f"{prompt} {suffix}: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print()
            return False
        if resp == "" and default_yes:
            return True
        if resp == "" and not default_yes:
            return False
        if resp in ("y", "yes"):
            return True
        if resp in ("n", "no"):
            return False
        print("Please answer yes or no (y/n).")

def play_round():
    user = prompt_user_choice()
    if user is None:
        return None, None, None
    comp = get_computer_choice()
    winner, reason = determine_winner(user, comp)
    return user, comp, (winner, reason)

def run_interactive():
    print("Welcome to Rock - Paper - Scissors!\n")
    print("Instructions: Type 'rock', 'paper', or 'scissors' (or r/p/s). Press Ctrl+C to quit.\n")

    user_score = 0
    comp_score = 0
    rounds = 0

    while True:
        rounds += 1
        print(f"--- Round {rounds} ---")
        user, comp, result = play_round()
        if user is None:
            break

        winner, reason = result
        print(f"You chose: {user}")
        print(f"Computer chose: {comp}")
        if winner == "user":
            user_score += 1
            print(f"You win! {reason}.")
        elif winner == "computer":
            comp_score += 1
            print(f"You lose. {reason}.")
        else:
            print("It's a tie.")

        print(f"Score -> You: {user_score} | Computer: {comp_score}\n")

        if not yes_no_prompt("Play another round?", default_yes=True):
            break

    print("\nFinal Score")
    print(f"You: {user_score} | Computer: {comp_score} | Rounds: {rounds}")
    print("Thanks for playing!")

def run_test_mode(rounds=5):
    """Non-interactive test: run a few random rounds to verify logic."""
    print("Running automated test mode...\n")
    user_score = 0
    comp_score = 0
    for i in range(1, rounds + 1):
        # simulate random user choices to exercise the logic
        user = random.choice(CHOICES)
        comp = get_computer_choice()
        winner, reason = determine_winner(user, comp)
        print(f"Round {i}: You={user} Computer={comp} -> {winner.upper()} ({reason})")
        if winner == "user":
            user_score += 1
        elif winner == "computer":
            comp_score += 1

    print(f"\nAutomated test finished. Score -> You: {user_score} | Computer: {comp_score} | Rounds: {rounds}")


def main(argv=None):
    argv = argv or sys.argv[1:]
    if "--test" in argv or "--auto" in argv:
        run_test_mode()
        return
    run_interactive()


if __name__ == "__main__":
    main()
