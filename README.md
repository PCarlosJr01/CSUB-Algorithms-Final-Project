P7 Wearable Heart-Rate Median Filter

Group B Algorithms

This project compares two algorithms for computing sliding window medians on heart-rate data:

- Quickselect per window
- Histogram + median pointer

Correctness Tests
-python run_checks.py my_solutions.py --only quickselect,hist --labels small
-python run_checks.py my_solutions.py --only quickselect,hist --labels medium
-python run_checks.py my_solutions.py --only quickselect,hist --labels large

Benchmark
python benchmark.py

Assistance:
ChatGPT was used to help develop part of the benchmark python file.
