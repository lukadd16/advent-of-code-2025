# https://adventofcode.com/2025/day/5

# Input contains a list of fresh ingredient ID ranges, a blank line, and a list of available ingredient IDs.
# Fresh ID ranges are inclusive and can overlap. An ingredient ID is fresh if it is in any range.

# PART 1: How many of the available ingredient IDs are fresh?
# PART 2: How many fresh ingredient IDs are there?

def run() -> None:
    part_1 = 0
    part_2 = 0

    with open("input/day5.txt") as f:
        fresh_ranges = []
        available_ids = []
        processing_fresh = True

        for line in f:
            line = line.strip()
            if line == "":
                processing_fresh = False
                continue

            if processing_fresh:
                start, end = map(int, line.split("-"))
                fresh_ranges.append((start, end))
            else:
                available_ids.append(int(line))

        part_1 = sum(
            1
            for id_ in available_ids
            if any(start <= id_ <= end for start, end in fresh_ranges)
        )

        # Merge overlapping/adjacent ranges
        merged: list[tuple[int, int]] = []
        for start, end in sorted(fresh_ranges):
            if not merged or start > merged[-1][1] + 1:
                # The start of the current range comes after the end of the last merged range
                # so add the entire range
                merged.append((start, end))
            else:
                # The start of the current range overlaps with or is adjacent to the end of the last merged range
                # so extend the last merged range
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))

        part_2 = sum(end - start + 1 for start, end in merged)

    print("-- DAY 5 --")
    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")
