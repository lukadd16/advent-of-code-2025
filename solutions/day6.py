# https://adventofcode.com/2025/day/6

# Input contains a list of problems
# Each problem has a group of numbers that need to be either added (+) or multiplied (*) together
# The numbers for each problem are arranged vertically, with the operation at the bottom
# Problems are separated by a full column of spaces

# PART 1: What is the grand total found by adding together all of the answers to the individual problems?
# PART 2: Reading the problems right-to-left, with the most significant digit at the top
#         and the least significant at the bottom, what is the grand total now?


def compute_answer(numbers: list[int], operation: str) -> int:
    assert operation in ("+", "*"), f"Unexpected operation '{operation}'"

    if operation == "+":
        answer = sum(numbers)
    else:
        answer = 1
        for num in numbers:
            answer *= num

    return answer


def run() -> None:
    part_1 = 0
    part_2 = 0

    with open("input/day6.txt") as f:
        # Preserve internal spacing
        lines = [line.rstrip("\n") for line in f.read().splitlines() if line.strip()]

    # -- PART 1 --
    part_one_rows = [line.split() for line in lines]
    problems: list[list[str]] = []
    max_cols = len(part_one_rows[0])  # Assume all rows are the same length
    for col_idx in range(max_cols):
        problem: list[str] = []
        for row_idx in range(len(part_one_rows)):
            problem.append(part_one_rows[row_idx][col_idx])
        problems.append(problem)

    for problem in problems:
        numbers = list(map(int, problem[:-1]))
        operation = problem[-1]
        part_1 += compute_answer(numbers, operation)

    # -- PART 2 -- (contains code from copilot)
    columns: list[list[str]] = []
    current_col = [[] for _ in lines]
    for col in range(len(lines[0])):
        vertical_slice = [row[col] for row in lines]

        # Check if this column is a "separator column" (all spaces)
        if all(ch == " " for ch in vertical_slice):
            # If we have collected a real column, store it
            if any("".join(row).strip() for row in zip(*current_col)):
                columns.append(["".join(row) for row in current_col])
            # Start a new column
            current_col = [[] for _ in lines]
        else:
            # Add this character to the current column
            for i, ch in enumerate(vertical_slice):
                current_col[i].append(ch)

    # Append final column if not empty
    if any("".join(row).strip() for row in zip(*current_col)):
        columns.append(["".join(row) for row in current_col])

    for column in columns:
        # Strip whitespace from the operator string
        column[-1] = column[-1].strip()

    # Extract the "real" numbers
    for column in columns:
        max_len = max(len(num) for num in column[:-1])
        numbers_str = column[:-1]
        operation = column[-1]
        # Treat every character within each number as a separate "column"
        digits: list[list[str]] = []
        for i in range(max_len):
            if i >= len(digits):
                digits.append([])
            for num in numbers_str:
                # Collect the ith digit from each number
                if i < len(num) and num[i].isdigit():
                    digits[i].append(num[i])

        # Combine the digits into numbers and compute the totals
        numbers = [int("".join(c)) for c in digits]
        part_2 += compute_answer(numbers, operation)

    print("-- DAY 6 --")
    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")
