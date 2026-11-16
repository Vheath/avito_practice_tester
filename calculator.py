#!/usr/bin/env python3
"""Tiny command-line calculator supporting +, -, *, /."""

import re
import sys

OPERATIONS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a // b,
}

TOKEN_RE = re.compile(r"\s*(\d+(?:\.\d+)?|[-+*/])")


def tokenize(expression):
    """Split an expression into numbers and operator tokens."""
    tokens = []
    position = 0
    expression = expression.strip()
    while position < len(expression):
        match = TOKEN_RE.match(expression, position)
        if not match:
            unexpected = expression[position:].lstrip()
            if not unexpected:
                break
            raise ValueError(f"unexpected character {unexpected[0]!r}")
        tokens.append(match.group(1))
        position = match.end()
    return tokens


def to_number(token):
    return float(token) if "." in token else int(token)


def apply(operator, left, right):
    if operator == "/" and right == 0:
        raise ValueError("division by zero")
    return OPERATIONS[operator](left, right)


def evaluate(tokens):
    """Evaluate tokens, applying * and / before + and -."""
    if not tokens:
        raise ValueError("empty expression")
    if tokens[0] in OPERATIONS:
        raise ValueError("expression must start with a number")

    values = [to_number(tokens[0])]
    operators = []
    index = 1
    while index < len(tokens):
        operator = tokens[index]
        if operator not in OPERATIONS:
            raise ValueError(f"unexpected token {operator!r}")
        if index + 1 >= len(tokens):
            raise ValueError(f"missing operand after {operator!r}")
        operators.append(operator)
        values.append(to_number(tokens[index + 1]))
        index += 2

    for operator in ("*", "/"):
        index = 0
        while index < len(operators):
            if operators[index] == operator:
                values[index:index + 2] = [apply(operator, values[index], values[index + 1])]
                del operators[index]
            else:
                index += 1

    result = values[0]
    for operator, value in zip(operators, values[1:]):
        result = apply(operator, result, value)
    return result


def calculate(expression):
    return evaluate(tokenize(expression))


def format_result(value):
    if isinstance(value, float):
        value = round(value, 10)
        if value.is_integer():
            return str(int(value))
    return str(value)


def main(argv):
    if len(argv) > 1:
        try:
            print(format_result(calculate(" ".join(argv[1:]))))
            return 0
        except ValueError as error:
            print(f"error: {error}", file=sys.stderr)
            return 1

    print("Tiny calculator. Operators: + - * /  (type 'quit' to exit)")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if line.lower() in ("quit", "exit"):
            return 0
        if not line:
            continue
        try:
            print(format_result(calculate(line)))
        except ValueError as error:
            print(f"error: {error}")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
