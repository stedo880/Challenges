import re
import sys


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
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
