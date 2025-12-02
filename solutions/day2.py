# https://adventofcode.com/2025/day/2

# Input is a list of comma-separated product ID ranges
# Product ID ranges are specified as: firstid-lastid
# Any ID that contains a sequence of digits that are repeated twice (55, 123123) is invalid
# PART 1: compute the sum of all of the invalid IDs
# PART 2: invalid IDs can contain sequences that are repeated at least twice (123123123, 11111), compute the sum of all of these IDs

def get_part1_invalid_id(product_id: int) -> int:
    str_id = str(product_id)

    # Ignore strings with an odd number of characters
    if len(str_id) % 2 != 0:
        return 0

    # Cut the string in half and check if the halves are equal
    first, second = str_id[:len(str_id)//2], str_id[len(str_id)//2:]
    if first == second:
        return int(str_id)
    
    return 0

def get_part2_invalid_id(product_id: int) -> int:
    str_id = str(product_id)
    n = len(str_id)

    # Try all pattern lengths that can repeat to fill the entire string
    for L in range(1, n // 2 + 1):
        if n % L != 0:
            continue
        pattern = str_id[:L]
        if pattern * (n // L) == str_id:
            return int(str_id)

    return 0

def run() -> None:
    part_1 = 0
    part_2 = 0

    # test_data = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
    # ranges = []
    # for raw in test_data.strip().split(","):
    #     if (r := raw.strip()):
    #         first_id, last_id = r.split("-")
    #         ranges.append((int(first_id), int(last_id)))

    with open("input/day2.txt") as f:
        ranges: list[tuple[int, int]] = []
        for raw in f.read().strip().split(","):
            if (r := raw.strip()):
                first_id, last_id = r.split("-")
                ranges.append((int(first_id), int(last_id)))

    # Iterate over all ID ranges
    for first_id, last_id in ranges:
        # Iterate over all product IDs in the range
        for product_id in range(first_id, last_id + 1):
            part_1 += get_part1_invalid_id(product_id)
            part_2 += get_part2_invalid_id(product_id)

    print("-- DAY 2 --")
    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")