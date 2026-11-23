import os
import json
import time

import problem
import my_solutions


HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.abspath(os.path.join(HERE, "..", "data"))
MANIFEST_FILE = os.path.join(DATA_FOLDER, "manifest.json")

RUNS = 5



def median_time(times):
    times = sorted(times)
    return times[len(times) // 2]


def test_algorithm(function, inst):
    times = []

    for run in range(RUNS):
        start = time.perf_counter()

        function(inst)

        end = time.perf_counter()

        times.append(end - start)

    return median_time(times)


def average_pointer_movement(inst):
    hr = inst["hr"]
    w = inst["w"]

    MIN_HR = 30
    MAX_HR = 220
    RANGE_SIZE = MAX_HR - MIN_HR + 1

    counts = [0] * RANGE_SIZE
    target = w // 2

    for i in range(w):
        counts[hr[i] - MIN_HR] += 1

    total = 0
    median_index = 0

    for i in range(RANGE_SIZE):
        if total + counts[i] > target:
            median_index = i
            break
        total += counts[i]

    below = total
    pointer_moves = 0
    steps = 0

    for i in range(w, len(hr)):
        old_index = hr[i - w] - MIN_HR
        new_index = hr[i] - MIN_HR

        if old_index < median_index:
            below -= 1
        counts[old_index] -= 1
        if new_index < median_index:
            below += 1
        counts[new_index] += 1

        while below > target:
            median_index -= 1
            below -= counts[median_index]
            pointer_moves += 1

        while below + counts[median_index] <= target:
            below += counts[median_index]
            median_index += 1
            pointer_moves += 1

        steps += 1

    if steps == 0:
        return 0

    return pointer_moves / steps

def main():
    with open(MANIFEST_FILE, "r", encoding="utf-8") as file:
        manifest = json.load(file)

    print("P7 Benchmark")
    print("Median of", RUNS, "runs")
    print()

    print(
        f"{'n':>8} {'w':>6} "
        f"{'Quickselect':>15} "
        f"{'Histogram':>15} "
        f"{'Avg Ptr Move':>15}"
    )

    print("-" * 75)

    for dataset in manifest["datasets"]:

        if dataset["label"] != "large":
            continue

        filename = os.path.join(DATA_FOLDER, dataset["file"])
        params = dataset["params"]

        inst = problem.load_instance(filename, params)

        n = inst["n"]
        w = inst["w"]

        quick_time = test_algorithm(
            my_solutions.solve_quickselect,
            inst
        )

        hist_time = test_algorithm(
            my_solutions.solve_hist,
            inst
        )

        avg_movement = average_pointer_movement(inst)
        print(
            f"{n:>8} {w:>6} "
            f"{quick_time:>15.6f} "
            f"{hist_time:>15.6f} "
            f"{avg_movement:>15.6f}"
        )


if __name__ == "__main__":
    main()