"""
generate_data.py - make a wearable heart-rate recording of any length for Project P7.

    python generate_data.py --n 86400 --seed 3 --out hr_24h.csv        # one full day at 1 reading per second

Columns: t_sec, hr_bpm  (integers, clipped to 30-220 bpm).

Signal model (what a smart-watch optical sensor sees):
  * resting baseline around 62 bpm with a slow day/night swing (+/- 9 bpm) and a slow random drift;
  * exercise episodes (about every 3-4 hours, 15-40 minutes) where the rate ramps to 110-165 bpm and recovers;
  * small beat-to-beat noise (+/- 2 bpm);
  * MOTION ARTEFACTS: short bursts (3-12 s) in which the sensor reports garbage values anywhere in 35-210 bpm.
    These are the outliers a median filter exists to remove (a mean filter would smear them into the signal).
--artifact-rate sets the chance per second that a burst starts (default 0.0015, i.e. about 130 bursts a day);
--burst-min / --burst-max set the burst length (default 3-12 s). A window of w readings can only remove bursts shorter than (w+1)/2.
The same seed always gives the same file.
"""
import argparse
import csv
import math
import random


def generate(n, seed, artifact_rate=0.0015, burst=(3, 12)):
    rng = random.Random(seed)
    hr = []
    drift = 0.0
    ex_start = rng.randint(0, max(1, min(n, 3 * 3600)))
    ex_len = rng.randint(900, 2400)
    ex_peak = rng.randint(110, 165)
    burst_left = 0
    for t in range(n):
        circadian = 62 + 9 * math.sin(2 * math.pi * (t / 86400.0) - 1.2)
        drift = 0.999 * drift + rng.gauss(0, 0.25)
        base = circadian + drift
        if ex_start <= t < ex_start + ex_len:                 # exercise: ramp up, plateau, ramp down
            x = (t - ex_start) / ex_len
            base += (ex_peak - 62) * math.sin(math.pi * min(1.0, x * 1.15)) ** 0.7
        elif t == ex_start + ex_len:                          # schedule the next episode
            ex_start = t + rng.randint(3 * 3600, 4 * 3600)
            ex_len = rng.randint(900, 2400)
            ex_peak = rng.randint(110, 165)
        v = base + rng.gauss(0, 1.3)
        if burst_left == 0 and rng.random() < artifact_rate:
            burst_left = rng.randint(*burst)
        if burst_left > 0:
            burst_left -= 1
            v = rng.uniform(35, 210)
        hr.append(int(max(30, min(220, round(v)))))
    return hr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True, help="number of readings (seconds)")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--artifact-rate", type=float, default=0.0015)
    ap.add_argument("--burst-min", type=int, default=3, help="shortest artefact burst in seconds")
    ap.add_argument("--burst-max", type=int, default=12, help="longest artefact burst in seconds")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    hr = generate(a.n, a.seed, a.artifact_rate, (a.burst_min, a.burst_max))
    with open(a.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["t_sec", "hr_bpm"])
        w.writerows(enumerate(hr))
    print("wrote", a.out)


if __name__ == "__main__":
    main()
