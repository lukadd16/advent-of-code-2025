# https://adventofcode.com/2025/day/7

# Input contains a diagram of a "tachyon manifold"
# The beam enters at the location marked "S"
# Beams move downward, passing freely through empty space "."
# If the beam encounters a splitter "^" it stops and a new beam continues from the immediate left and right of the splitter

# PART 1: How many times will the beam be split?
# PART 2: In total, how many different timelines would a single tachyon particle end up on?

import functools


BEAM_ENTER = "S"
EMPTY_SPACE = "."
SPLITTER = "^"


def run() -> None:
    part_1 = 0
    part_2 = 0

    with open("input/day7.txt") as f:
        grid: list[list[str]] = [
            list(row) for line in f.read().splitlines() if (row := line.strip())
        ]

    width, height = len(grid[0]), len(grid)

    # -- PART 1 --
    start_y = grid[0].index(BEAM_ENTER)
    prev_beam_indices: set[int] = {  # We only care about tracking unique beam positions
        start_y
    }
    for row in grid[::2]:  # Iterate over every other row
        cur_beam_indices: set[int] = set()
        for y in prev_beam_indices:
            if row[y] == SPLITTER:
                part_1 += 1
                for ny in (y - 1, y + 1):
                    if 0 <= ny < width:
                        cur_beam_indices.add(ny)
            else:
                cur_beam_indices.add(y)

        prev_beam_indices = cur_beam_indices

    # -- PART 2 -- (used hints from reddit)
    @functools.cache
    def count_routes(node: tuple[int, int]) -> int:
        x, y = node
        if x >= height:
            return 1
        if grid[x][y] == SPLITTER:
            # Split beam
            left, right = (x, y - 1), (x, y + 1)
            left_count = right_count = 0
            # Prevent out-of-bounds
            if left[1] >= 0:
                left_count = count_routes(left)
            if right[1] < width:
                right_count = count_routes(right)
            return left_count + right_count
        else:
            return count_routes((x + 1, y))

    part_2 = count_routes((0, start_y))

    print("-- DAY 7 --")
    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")
