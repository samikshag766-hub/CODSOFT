"""Simple CLI calculator with basic arithmetic operations.

Provides functions for add, subtract, multiply, divide and an interactive
prompt when run as a script.
"""

from __future__ import annotations

from typing import Callable


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return a / b


_OPS: dict[str, tuple[str, Callable[[float, float], float]]] = {
    "+": ("Add", add),
    "-": ("Subtract", subtract),
    "*": ("Multiply", multiply),
    "/": ("Divide", divide),
}


def _get_number(prompt: str) -> float:
    while True:
        try:
            raw = input(prompt)
            value = float(raw)
            return value
        except ValueError:
            print("Invalid number. Please enter a valid numeric value.")


def _choose_operation() -> str:
    print("Choose an operation:")
    for sym, (name, _) in _OPS.items():
        print(f"  {sym}  {name}")

    while True:
        choice = input("Operation: ").strip()
        if choice in _OPS:
            return choice
        print("Invalid operation choice. Pick one of: " + ", ".join(_OPS.keys()))


def interactive_calculator() -> None:
    print("Simple Calculator — basic arithmetic operations")
    a = _get_number("Enter the first number: ")
    b = _get_number("Enter the second number: ")
    op = _choose_operation()

    name, func = _OPS[op]
    try:
        result = func(a, b)
    except Exception as exc:  # keep message user-friendly
        print(f"Error performing {name}: {exc}")
    else:
        # Show integer-like floats without unnecessary decimals
        if result.is_integer():
            print(f"Result: {int(result)}")
        else:
            print(f"Result: {result}")


if __name__ == "__main__":
    interactive_calculator()
