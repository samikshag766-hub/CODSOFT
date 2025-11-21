"""Simple password generator CLI and function.

This module provides generate_password(length, complexity) which returns a
securely-generated password using the `secrets` module. It also provides a
small interactive CLI when run as a script.

Complexity options:
 - "low": lowercase letters only
 - "medium": lowercase + uppercase + digits
 - "strong": medium + punctuation
 - "custom": caller provides charset or interactive prompts are used

"""
from __future__ import annotations

import secrets
import string
from typing import Optional


def generate_password(length: int, complexity: Optional[str] = "strong", charset: Optional[str] = None) -> str:
    """Generate a secure password.

    Args:
        length: Desired password length (must be >= 1).
        complexity: One of 'low', 'medium', 'strong', or 'custom'. Ignored if charset is provided.
        charset: Optional explicit string of characters to draw from. If provided, this is used regardless
                 of complexity.

    Returns:
        The generated password string.

    Raises:
        ValueError: if length < 1 or no characters are available.
    """
    if length < 1:
        raise ValueError("length must be >= 1")

    if charset:
        pool = charset
    else:
        comp = (complexity or "strong").lower()
        if comp == "low":
            pool = string.ascii_lowercase
        elif comp == "medium":
            pool = string.ascii_lowercase + string.ascii_uppercase + string.digits
        elif comp == "strong":
            pool = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
        elif comp == "custom":
            # Fallback to strong if custom but no charset given
            pool = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
        else:
            # Unknown complexity value
            raise ValueError(f"unknown complexity: {complexity}")

    if not pool:
        raise ValueError("character set is empty; cannot generate password")

    # Use secrets.choice for cryptographic randomness
    return ''.join(secrets.choice(pool) for _ in range(length))


def _prompt_yes_no(prompt: str, default: bool = True) -> bool:
    suffix = "[Y/n]" if default else "[y/N]"
    while True:
        resp = input(f"{prompt} {suffix} ").strip().lower()
        if not resp:
            return default
        if resp in ("y", "yes"):
            return True
        if resp in ("n", "no"):
            return False
        print("Please answer y/yes or n/no.")


def main() -> None:
    """Run an interactive prompt for generating a password and print it."""
    print("Password generator — choose length and complexity")

    # Length input
    while True:
        val = input("Enter desired password length (1-25): ").strip()
        try:
            length = int(val)
            if 1 <= length <= 25:
                break
            print("Please enter a number between 1 and 25.")
        except ValueError:
            print("Please enter a valid integer.")

    # Complexity selection
    print("Choose complexity:")
    print("  1) low    — lowercase letters only")
    print("  2) medium — lowercase + uppercase + digits")
    print("  3) strong — medium + symbols (recommended)")
    print("  4) custom — choose which character sets to include")

    while True:
        choice = input("Enter choice [1-4] (default 3): ").strip() or "3"
        if choice in ("1", "2", "3", "4"):
            break
        print("Please enter 1, 2, 3, or 4.")

    if choice == "1":
        complexity = "low"
        pw = generate_password(length, complexity=complexity)
    elif choice == "2":
        complexity = "medium"
        pw = generate_password(length, complexity=complexity)
    elif choice == "3":
        complexity = "strong"
        pw = generate_password(length, complexity=complexity)
    else:
        # custom
        include_lower = _prompt_yes_no("Include lowercase letters?", default=True)
        include_upper = _prompt_yes_no("Include uppercase letters?", default=True)
        include_digits = _prompt_yes_no("Include digits?", default=True)
        include_symbols = _prompt_yes_no("Include symbols/punctuation?", default=False)

        pool = ""
        if include_lower:
            pool += string.ascii_lowercase
        if include_upper:
            pool += string.ascii_uppercase
        if include_digits:
            pool += string.digits
        if include_symbols:
            pool += string.punctuation

        if not pool:
            print("No character sets selected — defaulting to 'strong'.")
            pool = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation

        pw = generate_password(length, charset=pool)

    print("\nGenerated password:\n")
    print(pw)


if __name__ == "__main__":
    main()
