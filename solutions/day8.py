# https://adventofcode.com/2025/day/8

# Input contains the positions of junction boxes in 3D space
# Each position is given as x,y,z coordinates
# The goal is to connect pairs of junction boxes that are as close together as possible

# PART 1: Connect together the 1000 pairs of junction boxes which are closest together; what do you get if you multiply together the sizes (number of junction boxes) of the three largest circuits?
# PART 2: tbd

import math


def run() -> None:
    part_1 = 0
    part_2 = 0

    with open("input/day8.txt") as f:
        positions: list[tuple[int, int, int]] = [
            tuple(map(int, row.split(",")))
            for line in f.read().splitlines()
            if (row := line.strip())
        ]

    # Compute all unique unordered pairs and their squared distances
    pairs: list[tuple[int, tuple[tuple[int, int, int], tuple[int, int, int]]]] = []
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            a = positions[i]
            b = positions[j]
            dx = a[0] - b[0]
            dy = a[1] - b[1]
            dz = a[2] - b[2]
            d2 = dx * dx + dy * dy + dz * dz
            pairs.append((d2, (a, b)))

    # Sort pairs by squared distance
    pairs.sort(key=lambda x: x[0])

    top_n = 1000
    print(len(positions), top_n)
    print(f"Top {top_n} shortest connections (squared distance, distance, pair):")
    for d2, (a, b) in pairs[:top_n]:
        dist = math.sqrt(d2)
        print(f"{d2:10d}, {dist:8.3f}, {a} <-> {b}")

    # Create a set for every new circuit formed
    circuits: list[set[tuple[int, int, int]]] = []

    # Form the top_n shortest connections into circuits
    for _, (junc_a, junc_b) in pairs[:top_n]:
        # Find indices of circuits that contain either endpoint
        indices = [
            i
            for i, circuit in enumerate(circuits)
            if (junc_a in circuit) or (junc_b in circuit)
        ]
        if not indices:
            # Neither endpoint in any existing circuit --> form a new circuit
            print(junc_a, junc_b, "--> adding to new circuit")
            circuits.append({junc_a, junc_b})
        else:
            # Merge all found circuits into the first one and add endpoints
            print(junc_a, junc_b, f"--> merging into circuits at indices {indices}")
            first = indices[0]
            circuits[first].add(junc_a)
            circuits[first].add(junc_b)
            for idx in sorted(indices[1:], reverse=True):
                circuits[first].update(circuits[idx])
                del circuits[idx]

    # print(circuits)
    print(len(circuits))

    # Add each remaining junction box to a new circuit
    for pos in positions:
        if not any(pos in circuit for circuit in circuits):
            circuits.append({pos})

    print(len(circuits))

    sizes = sorted((len(c) for c in circuits), reverse=True)
    print(sizes)
    part_1 = 1
    for s in sizes[:3]:  # only the three largest circuits
        part_1 *= s

    print("-- DAY 8 --")
    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")
