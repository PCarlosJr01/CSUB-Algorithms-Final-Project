"""
P7 - Wearable Heart-Rate Median Filter (sliding-window median)
Instance loader, solution validator and technique registry used by run_checks.py.

Instance (dict returned by load_instance):
    n        number of readings
    t        t[k]  seconds since the start of recording (0, 1, 2, ...)
    hr       hr[k] heart rate in beats per minute (integers, 30-220)
    w        window length (ODD integer, given by the dataset's parameters in manifest.json)

Required output:
    the TRAILING-window median:  out[i] = median(hr[i], hr[i+1], ..., hr[i+w-1])   for i = 0 .. n-w
    (so the list has n - w + 1 entries; because w is odd, the median is the middle element after sorting,
     the element of rank (w-1)/2 counting from 0 - always one of the readings, never an average).

Solution format (what every technique returns):
    a list of n - w + 1 integers.
"""
import csv
from bisect import bisect_left, insort

SENSE = "none"
TECHNIQUES = {
    "bf":          {"name": "Brute force (recompute every window from scratch)", "exact": True},
    "quickselect": {"name": "Decrease-and-conquer (quickselect per window)", "exact": True},
    "heaps":       {"name": "Transform-and-conquer (two heaps with lazy deletion)", "exact": True},
    "hist":        {"name": "Space-time trade-off (histogram of values + median pointer)", "exact": True},
}


def load_instance(path, params=None):
    params = params or {}
    t, hr = [], []
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            t.append(int(r["t_sec"]))
            hr.append(int(r["hr_bpm"]))
    w = int(params.get("w", 31))
    if w % 2 == 0 or w < 1 or w > len(hr):
        raise ValueError("window length must be odd and not longer than the recording")
    return {"n": len(hr), "t": t, "hr": hr, "w": w}


def oracle(inst):
    """Independent reference: keep the window as a sorted list (bisect). Used only to check answers."""
    hr, w = inst["hr"], inst["w"]
    win = sorted(hr[:w])
    mid = w // 2
    out = [win[mid]]
    for i in range(w, len(hr)):
        del win[bisect_left(win, hr[i - w])]
        insort(win, hr[i])
        out.append(win[mid])
    return out


def validate(inst, sol, params=None):
    exp = inst.get("_expected")
    if exp is None:
        exp = inst["_expected"] = oracle(inst)
    try:
        got = [int(v) for v in sol]
    except (TypeError, ValueError):
        return False, None, "solution must be a list of integers"
    if len(got) != len(exp):
        return False, None, f"expected {len(exp)} medians, got {len(got)}"
    for i, (a, b) in enumerate(zip(got, exp)):
        if a != b:
            return False, None, f"first difference at window {i}: got {a}, expected {b}"
    return True, None, ""
