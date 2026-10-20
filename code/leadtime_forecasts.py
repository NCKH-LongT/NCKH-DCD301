"""Forecasts for the lead-time check (L = 1 and 4 weeks, horizons h = 2 and 5) in the second and third windows.

The main window already has these horizons (run_pipeline.py --grid full). This script fills the earlier windows so
that leadtime_equal_fill.py can evaluate every window. Same models, same protocol as run_pipeline.py; existing
cache files are skipped, so the script can be restarted.

Usage:
    python code/leadtime_forecasts.py --datasets VN1,M5 --offsets 26,52
"""
import argparse
import os
import sys
import time
import warnings

warnings.filterwarnings("ignore")
import numpy as np  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f2d import classify, config, data, models  # noqa: E402
from f2d.features import Builder  # noqa: E402

METHODS = ["empirical", "tsb_nb", "ets", "lgb_tweedie", "lgb_conformal", "lgb_quantile"]
ML = {"lgb_tweedie", "lgb_conformal", "lgb_quantile"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--datasets", default="VN1,M5")
    ap.add_argument("--offsets", default="26,52")
    ap.add_argument("--horizons", default="2,5")
    a = ap.parse_args()
    qs = list(config.QUANTILES)
    for name in a.datasets.split(","):
        base = data.load(name)
        for off in [int(x) for x in a.offsets.split(",")]:
            p = data.truncate(base, base["Y"].shape[1] - off) if off else base
            Y = p["Y"]
            T = Y.shape[1]
            test0 = T - config.TEST_WEEKS
            origins = list(range(test0, T))
            sel = p["start"] <= test0 - config.VALID_WEEKS
            cls, _, _ = classify.classify(Y, p["start"], test0)
            sel &= cls != "none"
            b = Builder(p)
            out = os.path.join(config.CACHE, "forecasts", name + (f"_w{off}" if off else ""))
            os.makedirs(out, exist_ok=True)
            for h in [int(x) for x in a.horizons.split(",")]:
                for m in METHODS:
                    path = os.path.join(out, f"{m}_h{h}.npz")
                    if os.path.exists(path):
                        continue
                    t0 = time.time()
                    print(f"{name} w{off} h{h}: {m} ...", flush=True)
                    fn = models.MODELS[m]
                    Q = fn(b, origins, h, qs, sel, log=lambda *x, **k: None) if m in ML else fn(b, origins, h, qs, sel)
                    np.savez_compressed(path, Q=Q.astype(np.float32))
                    print(f"    done in {time.time() - t0:.0f}s", flush=True)
    print("ALL_DONE", flush=True)


if __name__ == "__main__":
    main()
