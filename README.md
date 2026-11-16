# Tiny Calculator

A minimal command-line calculator that evaluates expressions with the four basic
arithmetic operators: `+`, `-`, `*` and `/`. It is written in plain Python with no
dependencies, so it runs anywhere Python 3 is installed.

## Usage

Run it with a single expression, or start it with no arguments for an interactive prompt:

```
$ python3 calculator.py "2 + 3 * 4"
14

$ python3 calculator.py
Tiny calculator. Operators: + - * /  (type 'quit' to exit)
> 10 - 4 - 3
3
> quit
```

## Behaviour

- Numbers may be written as whole numbers (`7`) or decimals (`2.5`).
- Multiplication and division are evaluated before addition and subtraction, and
  operators of equal precedence are evaluated from left to right.
- Division returns the exact fractional result, so `7 / 2` evaluates to `3.5`.
- Dividing by zero, an unbalanced expression, or an unknown character is reported
  as an error; in one-shot mode the process exits with a non-zero status.
- Whole results are printed without a decimal point (`6`, not `6.0`).
