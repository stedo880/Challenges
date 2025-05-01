# Advent of Code 2022 - Day 21
# https://adventofcode.com/2022/day/21

import re
import sys

# Define a class hierarchy for symbolic expressions

class Expr:
    # Base class: either a constant, a variable, or a binary operation.
    pass

class Constant(Expr):
    def __init__(self, value: int):
        self.value = value
    def __repr__(self):
        return str(self.value)

class Variable(Expr):
    def __init__(self, name: str):
        self.name = name
    def __repr__(self):
        return self.name

class Operation(Expr):
    def __init__(self, left: Expr, op: str, right: Expr):
        self.left = left
        self.op = op    # one of "+", "-", "*", "/"
        self.right = right
    def __repr__(self):
        return f"({self.left} {self.op} {self.right})"

def compute(a: int, op: str, b: int) -> int:
    if   op == "+": return a + b
    elif op == "-": return a - b
    elif op == "*": return a * b
    elif op == "/": return a // b
    else: raise ValueError(f"Unknown operator {op!r}")

def contains_humn(expr: Expr) -> bool:
    if isinstance(expr, Variable):
        return True
    if isinstance(expr, Constant):
        return False
    # Operation
    return contains_humn(expr.left) or contains_humn(expr.right)

def eval_constant(expr: Expr) -> int:
    if isinstance(expr, Constant):
        return expr.value
    if isinstance(expr, Variable):
        raise ValueError("Cannot eval_constant on a Variable")
    return compute(eval_constant(expr.left),
                   expr.op,
                   eval_constant(expr.right))

def solve_equation(left: Expr, right: Expr) -> int:
    # base cases
    if isinstance(left, Variable):
        return eval_constant(right)
    if isinstance(right, Variable):
        return eval_constant(left)

    # pick symbolic side
    if contains_humn(left):
        sym, other = left, right
    else:
        sym, other = right, left

    const_val = eval_constant(other)
    L, op, R = sym.left, sym.op, sym.right

    if contains_humn(L):
        # (L op R) = const => L = inv(const, R)
        r = eval_constant(R)
        if op == "+": new_target = const_val - r
        elif op == "-": new_target = const_val + r
        elif op == "*": new_target = const_val // r
        elif op == "/": new_target = const_val * r
        next_sym = L
    else:
        # (L op R) = const => R = inv_left(const, L)
        l = eval_constant(L)
        if op == "+": new_target = const_val - l
        elif op == "-": new_target = l - const_val
        elif op == "*": new_target = const_val // l
        elif op == "/": new_target = l // const_val
        next_sym = R

    return solve_equation(next_sym, Constant(new_target))


# Function to parse the input text and create a dictionary of monkeys
def parse_input(input_text: str) -> dict[str, int|str]:
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
def evaluate_monkey(monkeys: dict[str, int|str], name: str) -> Expr:
    job = monkeys[name]
    
    # if the monkey's name is "humn", return variable "humn"
    if name == "humn":
        return Variable("humn")
    
    # If the monkey's job is a number, return it
    if isinstance(job, int):
        return Constant(job)

    # Split the job into parts
    left_name, operator, right_name = job.split()

    L = evaluate_monkey(monkeys, left_name)
    R = evaluate_monkey(monkeys, right_name)

    # If both sides are constand, resolve the operation
    if isinstance(L, Constant) and isinstance(R, Constant):
        return Constant(compute(L.value, operator, R.value))
    
    return Operation(L, operator, R)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python AOC-2022-21-part2.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    try:
        with open(input_file, 'r') as file:
            input_text = file.read()
        monkeys = parse_input(input_text)
        
        # Get children of root monkey
        root_job = monkeys["root"]
        root_left_child, root_operator, root_right_child = root_job.split()

        # Evaluate the left and right expressions
        left_expr = evaluate_monkey(monkeys, root_left_child)
        right_expr = evaluate_monkey(monkeys, root_right_child)

        print(f"Left expression: {left_expr}")
        print(f"Right expression: {right_expr}")    

        answer = solve_equation(left_expr, right_expr)
        
        print("humn =", answer)
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
