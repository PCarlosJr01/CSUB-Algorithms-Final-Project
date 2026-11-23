Project P7 - Wearable Heart-Rate Median Filter (sliding-window median)
DATA FOLDER
============================================================

These datasets are SYNTHETIC: produced by generate_data.py from a fixed random seed so that every student gets identical files,
with distributions modelled on the real-world situation described in the project brief.

FORMAT
hr_nNNNNN.csv : t_sec, hr_bpm (1 reading per second). The window length w is NOT in the file: it comes from the
'params' of each manifest entry (the same file is used with w = 31, 301 and 1001).

REFERENCE VALUES
There is exactly one correct output list per (file, w) entry; the checker recomputes it independently.

MORE DATA
    python generate_data.py --help      (any size, any seed; the same seed always gives the same file)

FILES (from manifest.json)
    file                               label       size  suitable techniques                reference
    hr_n00060.csv                      small         60  bf,quickselect,heaps,hist          exact_output  (w=5)
    hr_n05000.csv                      medium      5000  bf,quickselect,heaps,hist          exact_output  (w=31)
    hr_n86400.csv                      large      86400  bf,quickselect,heaps,hist          exact_output  (w=31)
    hr_n86400.csv                      large      86400  quickselect,heaps,hist             exact_output  (w=301)
    hr_n86400.csv                      large      86400  quickselect,heaps,hist             exact_output  (w=1001)

Labels: small = hand-checkable / every technique; medium = exponential techniques still feasible; large = only the efficient techniques; stress = slow even for them (use for the top of your scaling curve).
A technique listed as 'suitable' for a file is expected to finish in under about a minute in CPython; a technique NOT listed is expected to be too slow (that is part of what you will measure).
