Project P7 - Wearable Heart-Rate Median Filter (sliding-window median)
STARTER FOLDER
============================================================

problem.py       Loads a data file into a Python dict (inst), checks an answer (validate) and lists the technique keys.
                 READ ITS DOCSTRING FIRST: it defines the instance fields and the exact format every technique must return.
my_solutions.py  Template. Fill in your two techniques; keep the TECHNIQUES dictionary at the bottom.
run_checks.py    Test harness. It runs your functions on the files listed in ../data/manifest.json, validates every answer
                 and compares it with the reference value.

Quick start (Python 3.10+, standard library only):
    python run_checks.py my_solutions.py --only bf,quickselect --labels small

Technique keys for this project:
    bf          Brute force (recompute every window from scratch)  [exact]
    quickselect Decrease-and-conquer (quickselect per window)  [exact]
    heaps       Transform-and-conquer (two heaps with lazy deletion)  [exact]
    hist        Space-time trade-off (histogram of values + median pointer)  [exact]

The harness is for CORRECTNESS. For the timing / operation-count experiments in your report, write your own benchmark script
(time.perf_counter, repeated runs, growing n) - the project brief and the master document explain the protocol.
