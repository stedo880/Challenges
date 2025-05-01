# Advent of Code 2022 - Day 21
# https://adventofcode.com/2022/day/21

import re
import sys


# Function to parse the input text and create a dictionary of monkeys
def parse_input(input_text):
    monkeys = {}
    for line in input_text.strip().split("\n"):
        name, job = line.split(": ")
        if re.match(r"^\d+$", job):
            # If the job is a number, store it as an integer
            monkeys[name] = int(job)
        else:
            # Otherwise, store the operation as a string
            monkeys[name] = job
    return monkeys


# Recursively evaluate the monkey's job
def evaluate_monkey(monkeys, name):
    # If the monkey's job is a number, return it
    if isinstance(monkeys[name], int):
        return monkeys[name]

    # if the monkey's name is "humn", return symbolic "humn"
    if name == "humn":
        return "humn"

    # Split the job into parts
    parts = monkeys[name].split()
    left = evaluate_monkey(monkeys, parts[0])
    operator = parts[1]
    right = evaluate_monkey(monkeys, parts[2])

    # Perform the operation based on the operator
    if operator == "+":
        return left + right
    elif operator == "-":
        return left - right
    elif operator == "*":
        return left * right
    elif operator == "/":
        return left // right  # Use integer division for consistency with the problem statement
    else:
        raise ValueError(f"Unknown operator: {operator}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python AOC-2022-21.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    try:
        with open(input_file, 'r') as file:
            input_text = file.read()
        monkeys = parse_input(input_text)
        print(monkeys)

        # Evaluate the root monkey's job
        root_value = evaluate_monkey(monkeys, "root")
        print(f"Root monkey yells: {root_value}")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
