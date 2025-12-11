# https://adventofcode.com/2025/day/9

# Input contains a list of x,y coordinates that represent "red tiles" on a grid
# PART 1: Picking any two red tiles as the opposite corners of a rectangle, what is the largest area of any rectangle you can make?
# PART 2: Using two red tiles as opposite corners, what is the largest area of any rectangle you can make using only red and green tiles?

def run() -> None:
    part_1 = 0
    part_2 = 0

    with open("input/day9.txt") as f:
        red_tiles: list[tuple[int, int]] = [
            tuple(map(int, line.strip().split(","))) for line in f.readlines()
        ]

    # PART 1: compute the largest rectangle area from any two red tiles used as opposite corners
    n = len(red_tiles)
    for i in range(n):
        x1, y1 = red_tiles[i]
        for j in range(i + 1, n):
            x2, y2 = red_tiles[j]
            w = abs(x1 - x2) + 1
            h = abs(y1 - y2) + 1
            if w == 1 or h == 1:
                continue
            area = w * h
            if area > part_1:
                part_1 = area

    # PART 2 (thanks again copilot 🙏): build polygon interior from the ordered red tile loop (edges are axis-aligned),
    # then test rectangles whose opposite corners are red: rectangle is valid if for every
    # horizontal slab between vertex y-values the rectangle's x-span is fully within the
    # polygon's x-intervals for that slab.
    # Build vertical edges (x, y_low, y_high)
    vertical_edges: list[tuple[int, int, int]] = []
    for i in range(n):
        x_a, y_a = red_tiles[i]
        x_b, y_b = red_tiles[(i + 1) % n]
        if x_a == x_b:
            y_low, y_high = (y_a, y_b) if y_a < y_b else (y_b, y_a)
            vertical_edges.append((x_a, y_low, y_high))

    # unique sorted vertex y-values
    y_vals = sorted({y for _, y in red_tiles})
    slabs: list[list[tuple[int, int]]] = []
    y_samples: list[float] = []

    # For each slab between consecutive vertex y-values pick a sample y and compute interior x-intervals
    for k in range(len(y_vals) - 1):
        y_lo = y_vals[k]
        y_hi = y_vals[k + 1]
        y_sample = (y_lo + y_hi) / 2.0
        y_samples.append(y_sample)
        xs: list[int] = []
        for x, yl, yh in vertical_edges:
            # include vertical edge if it crosses the sample line
            if yl < y_sample < yh:
                xs.append(x)
        xs.sort()
        intervals: list[tuple[int, int]] = []
        # pair intersections to interior intervals
        for idx in range(0, len(xs), 2):
            if idx + 1 < len(xs):
                intervals.append((xs[idx], xs[idx + 1]))
        slabs.append(intervals)

    def covers(intervals: list[tuple[int, int]], x_min: int, x_max: int) -> bool:
        # check if any interval fully contains [x_min, x_max]
        for a, b in intervals:
            if a <= x_min and b >= x_max:
                return True
        return False

    # Test all red-red opposite-corner rectangles and require rectangle's x-span to be covered
    # in every slab whose sample y lies strictly between the rectangle's y bounds.
    for i in range(n):
        x1, y1 = red_tiles[i]
        for j in range(i + 1, n):
            x2, y2 = red_tiles[j]
            if x1 == x2 or y1 == y2:
                continue
            x_min, x_max = (x1, x2) if x1 < x2 else (x2, x1)
            y_min, y_max = (y1, y2) if y1 < y2 else (y2, y1)

            ok = True
            # for each slab sample check if it lies inside the rectangle's vertical open interval
            for sample_y, intervals in zip(y_samples, slabs):
                if y_min < sample_y < y_max:
                    if not covers(intervals, x_min, x_max):
                        ok = False
                        break
            if ok:
                w = x_max - x_min + 1
                h = y_max - y_min + 1
                area = w * h
                if area > part_2:
                    part_2 = area

    print("-- DAY 9 --")
    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")
