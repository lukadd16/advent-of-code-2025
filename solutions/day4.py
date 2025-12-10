# https://adventofcode.com/2025/day/4

# Rolls of paper are arranged in a grid
# Each cell in the grid can either be blank (.) or have a roll of paper (@)
# A roll of paper can only be accessed if there are fewer than four rolls of paper in the eight adjacent positions (N, NE, E, SE, S, SW, W, NW)
# PART 1: How many rolls of paper can be accessed?
# PART 2: Once a roll can be accessed it can be removed; how many rolls of paper in total can be removed?

EMPTY_CELL = "."
PAPER_ROLL = "@"


# Helper function that returns the values of adjacent cells
def get_adjacent_cells(grid: list[list[str]], row: int, col: int) -> list[str]:
    adjacent_cells = []
    # We want to check all 8 directions (NW, N, NE, W, E, SW, S, SE)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        # Handle out-of-bounds
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            adjacent_cells.append(grid[r][c])
    return adjacent_cells


def run() -> None:
    part_1 = 0
    part_2 = 0

    with open("input/day4.txt") as f:
        # Represent the grid as a 2D array
        grid: list[list[str]] = [
            list(row) for line in f.read().splitlines() if (row := line.strip())
        ]

    for row_idx, row in enumerate(grid):
        for col_idx, column in enumerate(row):
            # Skip over empty cells
            if column == EMPTY_CELL:
                continue
            # Check adjacent cells
            if get_adjacent_cells(grid, row_idx, col_idx).count(PAPER_ROLL) < 4:
                part_1 += 1

    first_iteration = True

    # Iterate over the entire grid, finding which rolls are accessible, removing them at the end of each iteration
    # Stop when there are zero accessible rolls remaining
    while True:
        to_remove: list[tuple[int, int]] = []

        for row_idx, row in enumerate(grid):
            for col_idx, column in enumerate(row):
                # Skip over empty cells
                if column != PAPER_ROLL:
                    continue
                # Check adjacent cells
                if get_adjacent_cells(grid, row_idx, col_idx).count(PAPER_ROLL) < 4:
                    to_remove.append((row_idx, col_idx))

        removed = len(to_remove)
        if removed == 0:
            break

        # Part 1 only cares about the original grid (result after the first iteration)
        if first_iteration:
            part_1 = removed
            first_iteration = False

        # Accumulate total removed across iterations
        part_2 += removed

        # Remove cells by marking them as empty
        for r, c in to_remove:
            grid[r][c] = EMPTY_CELL

    print("-- DAY 4 --")
    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")
