# https://adventofcode.com/2025/day/1

# There is a safe with a dial, numbered 0-99 (inclusive)
# Rotations are given in the format: L# or R#
# E.g., L8 = move dial 8 positions to the left

# The dial starts at 50

# PART 1: the password is the number of times the dial is left pointing at 0 after any rotation in the sequence.
# PART 2: count the number of times any click causes the dial to point at 0, regardless of whether it happens during a rotation or at the end of one.

from dataclasses import dataclass

STARTING_POSITION = 50
MIN_POSITION = 0
MAX_POSITION = 99
TOTAL_POSITIONS = MAX_POSITION - MIN_POSITION + 1

@dataclass
class Dial:
    position: int

    def turn(self, direction: str, amount: int) -> int:
        assert direction in ("L", "R")

        hits_on_zero = 0  # number of times the dial hits 0 during this turn
        
        # This sequence prevents double counting if the turn ends on a zero
        for step in range(1, amount + 1):
            if direction == "L":
                pos = (self.position - step) % TOTAL_POSITIONS
            else:
                pos = (self.position + step) % TOTAL_POSITIONS
            if pos == 0:
                hits_on_zero += 1

        if direction == "L":
            self.position = (self.position - amount) % TOTAL_POSITIONS
        else:
            self.position = (self.position + amount) % TOTAL_POSITIONS

        return hits_on_zero

def run() -> None:
    part_1 = 0
    part_2 = 0

    dial = Dial(position=STARTING_POSITION)

    with open("input/day1.txt") as f:
        rotations = [r for raw in f.read().splitlines() if (r := raw.strip())]

    for rotation in rotations:
        direction = rotation[0]
        amount = int(rotation[1:])
        part_2 += dial.turn(direction, amount)
        if dial.position == 0:
            part_1 += 1

    print("-- DAY 1 --")
    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")