# https://adventofcode.com/2025/day/3

# Each row represents a battery bank
# Within each bank, we must turn on exactly two batteries
# The joltage that the bank produces is equal to the number formed by the digits on the batteries you've turned on
# E.g., if we turn on batteries 2 and 4 in the bank 54321, the joltage is 42

# PART 1: find the maximum joltage possible from each bank; what is the total output joltage?
# PART 2: by turning on exactly twelve batteries within each bank, what is the new total output joltage?

def max_subsequence(s: str, k: int) -> int:
    """Return the integer value of the largest subsequence of length k (order preserved)."""
    if k >= len(s):
        return int(s)
    stack: list[str] = []
    to_remove = len(s) - k
    for ch in s:
        while stack and to_remove > 0 and stack[-1] < ch:
            stack.pop()
            to_remove -= 1
        stack.append(ch)
    return int("".join(stack[:k]))

def run() -> None:
    part_1 = 0
    part_2 = 0

    with open("input/day3.txt") as f:
        banks = [bank for line in f.read().splitlines() if (bank := line.strip())]

    for bank in banks:
        part_1 += max_subsequence(bank, 2)
        part_2 += max_subsequence(bank, 12)


    print("-- DAY 3 --")
    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")
