"""
my_solutions.py - starter file for Project P7: Wearable Heart-Rate Median Filter (sliding-window median)

Implement the TWO techniques assigned to you (the keys are listed in TECHNIQUES below). Delete or ignore the others.
Every function receives the loaded instance (a dict; its fields are described at the top of problem.py)
and must return: a list of n - w + 1 integers (trailing-window medians).

Test your work from this folder:
    python run_checks.py my_solutions.py --only <key>[,<key>]      e.g.  --only bf,quickselect
Rules: write the algorithms under study yourself (see the project brief for which library helpers are allowed).
"""
import random

def partiition(values, low, high, pivot_index):
    pivot_value = values[pivot_index]

    values[pivot_index], values[high] = values[high], values[pivot_index]

    store_index = low

    for i in range(low, high):
        if values[i] < pivot_value:
            values[i], values[store_index] = values[store_index], values[i]
            store_index += 1

    values[store_index], values[high] = values[high], values[store_index]
    return store_index

def quickselect(values, target, rng):
    low = 0
    high = len(values) - 1

    while True:
        if low == high:
            return values[low]

        pivot_index = rng.randint(low, high)
        pivot_index = partiition(values, low, high, pivot_index)

        if pivot_index == target:
            return values[pivot_index]
        elif target < pivot_index:
            high = pivot_index - 1
        else:
            low = pivot_index + 1

def solve_bf(inst):
    """Brute force (recompute every window from scratch).

    Return: a list of n - w + 1 integers (trailing-window medians).
    """
    raise NotImplementedError("write the bf technique here")


def solve_quickselect(inst):
    """Decrease-and-conquer (quickselect per window).

    Return: a list of n - w + 1 integers (trailing-window medians).
    """

    hr = inst["hr"]
    w = inst["w"]

    output = []
    target = w//2

    rng = random.Random(1)
    for start in range(len(hr) - w + 1):
        window = hr[start:start + w]
        median = quickselect(window, target, rng)
        output.append(median)
    return output

    raise NotImplementedError("write the quickselect technique here")


def solve_heaps(inst):
    """Transform-and-conquer (two heaps with lazy deletion).
    Return: a list of n - w + 1 integers (trailing-window medians).
    """

    raise NotImplementedError("write the heaps technique here")


def solve_hist(inst):
    """Space-time trade-off (histogram of values + median pointer).

    Return: a list of n - w + 1 integers (trailing-window medians).
    """

    hr = inst["hr"]
    w = inst["w"]

    MIN_HR = 30
    MAX_HR = 220
    RANGE_SIZE = MAX_HR - MIN_HR + 1

    counts = [0] * RANGE_SIZE
    output = []

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
    output.append(median_index + MIN_HR)

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

        while below + counts[median_index] <= target:
            below += counts[median_index]
            median_index += 1

        output.append(median_index + MIN_HR)
    return output    

    raise NotImplementedError("write the hist technique here")


TECHNIQUES = {
    "bf": solve_bf,
    "quickselect": solve_quickselect,
    "heaps": solve_heaps,
    "hist": solve_hist,
}
