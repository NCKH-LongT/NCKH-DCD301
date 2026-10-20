"""One-command runner of the N-HiTS baseline for a second team member: check, run, verify, commit and push.

For each test window it
  1. checks the branch, the neuralforecast version and the raw data files (size in bytes);
  2. runs a short smoke test once (code/run_neural.py --quick) and checks that the data fingerprint matches the
     development machine exactly;
  3. runs the full forecast (code/run_neural.py), with a log;
  4. checks the log (fingerprint, no missing forecasts, file written);
  5. copies the forecast and the log to code/outputs/neural/ (tracked by git) and records the run time and machine;
  6. commits only code/outputs/neural/, pulls with rebase and pushes to the branch's remote.
Windows already present in code/outputs/neural/ are skipped, so the script can simply be restarted after an
interruption. It never edits code or data and never commits anything outside code/outputs/neural/.

Run with the interpreter that has neuralforecast 3.3.0, from the repository root:
    D:/venvs/nf/Scripts/python.exe code/member_run_neural.py                 # M5, windows 0, 26, 52
    D:/venvs/nf/Scripts/python.exe code/member_run_neural.py --check-only    # checks + smoke test only
    D:/venvs/nf/Scripts/python.exe code/member_run_neural.py --no-push       # run and commit, push by hand later
"""
import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANCH = "FA26_BDT301_SE1926_G01"
NF_VERSION = "3.3.0"
OUT = os.path.join(ROOT, "code", "outputs", "neural")
FILES = {
    "M5": {os.path.join("data", "m5-forecasting-accuracy", f): s for f, s in
           [("calendar.csv", 103469), ("sales_train_evaluation.csv", 121736518), ("sell_prices.csv", 203395785)]},
    "VN1": {os.path.join("data", "Vn1 forcasting", f): s for f, s in
            [("Phase 0 - Sales.csv", 10804654), ("Phase 0 - Price.csv", 7588298), ("Phase 1 - Sales.csv", 1018396),
             ("Phase 1 - Price.csv", 962283), ("Phase 2 - Sales.csv", 1012437)]},
}
FINGERPRINT = {
    ("M5", 0): "30490 series x 277 weeks, evaluated 30381, total sales of evaluated series 66793704",
    ("M5", 26): "30490 series x 251 weeks, evaluated 29917, total sales of evaluated series 59390858",
    ("M5", 52): "30490 series x 225 weeks, evaluated 28824, total sales of evaluated series 52145075",
    ("VN1", 0): "15053 series x 196 weeks, evaluated 13844, total sales of evaluated series 39234029",
    ("VN1", 26): "15053 series x 170 weeks, evaluated 11442, total sales of evaluated series 31620787",
    ("VN1", 52): "15053 series x 144 weeks, evaluated 9383, total sales of evaluated series 24659310",
}


def stop(msg):
    print(f"\nSTOP: {msg}\n", flush=True)
    sys.exit(1)


def git(*args, check=True):
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if check and r.returncode != 0:
        stop(f"git {' '.join(args)} failed:\n{r.stdout}{r.stderr}")
    return r.stdout.strip()


def run_logged(args, log_path):
    """Run code/run_neural.py with the current interpreter; stream to a log file; return (exit code, seconds, text)."""
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    t0 = time.time()
    with open(log_path, "w", encoding="utf-8") as fh:
        proc = subprocess.Popen([sys.executable, "-u", os.path.join("code", "run_neural.py"), *args], cwd=ROOT,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                                errors="replace", env=env)
        for line in proc.stdout:
            fh.write(line)
            if re.search(r"fingerprint|trained on|predicted|done in|written|Error|error", line):
                print("    " + line.rstrip(), flush=True)
        proc.wait()
    with open(log_path, encoding="utf-8") as fh:
        return proc.returncode, time.time() - t0, fh.read()


def check_fingerprint(text, dataset, offset):
    m = re.search(rf"fingerprint {dataset} w{offset}: (.*)", text)
    got = m.group(1).strip() if m else "(no fingerprint line)"
    if got != FINGERPRINT[dataset, offset]:
        stop(f"data fingerprint does not match the development machine.\n  expected: {FINGERPRINT[dataset, offset]}\n"
             f"  got:      {got}\nCheck the raw data files (section 3.2 of 07_paper_draft/handoff_neural_baseline.md).")


def machine():
    info = dict(platform=platform.platform(), processor=platform.processor(), cpu_count=os.cpu_count(),
                python=platform.python_version())
    try:
        import psutil
        info["ram_gb"] = round(psutil.virtual_memory().total / 2 ** 30, 1)
    except Exception:
        pass
    try:
        import torch
        info["torch"] = torch.__version__
    except Exception:
        pass
    return info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="M5", choices=["M5", "VN1"])
    ap.add_argument("--offsets", default="0,26,52")
    ap.add_argument("--h", type=int, default=3)
    ap.add_argument("--no-push", action="store_true", help="commit locally but do not push")
    ap.add_argument("--check-only", action="store_true", help="only the checks and the smoke test (no full run, no commit)")
    a = ap.parse_args()
    offsets = [int(x) for x in a.offsets.split(",")]
    os.makedirs(os.path.join(OUT, "logs"), exist_ok=True)

    # ---- 1. checks
    print("1. Checks", flush=True)
    br = git("rev-parse", "--abbrev-ref", "HEAD")
    if br != BRANCH:
        stop(f"current branch is {br}; run: git checkout {BRANCH} && git pull")
    try:
        import neuralforecast
    except ImportError:
        stop(f"neuralforecast is not installed in {sys.executable}; install neuralforecast=={NF_VERSION}")
    if neuralforecast.__version__ != NF_VERSION:
        stop(f"neuralforecast {neuralforecast.__version__} found, {NF_VERSION} required")
    for f, size in FILES[a.dataset].items():
        p = os.path.join(ROOT, f)
        if not os.path.exists(p):
            stop(f"missing data file {f}")
        if os.path.getsize(p) != size:
            stop(f"{f} has {os.path.getsize(p)} bytes, expected {size} (wrong file or version)")
    print(f"   branch {br}, neuralforecast {neuralforecast.__version__}, {a.dataset} data files OK", flush=True)

    todo = [o for o in offsets if not os.path.exists(os.path.join(OUT, f"{a.dataset}_w{o}_nhits_h{a.h}.npz"))]
    if not todo:
        print("All requested windows are already in code/outputs/neural/. Nothing to do.")
        return

    # ---- 2. smoke test (once)
    print("2. Smoke test", flush=True)
    log = os.path.join(OUT, "logs", f"{a.dataset}_quick.log")
    rc, sec, text = run_logged(["--dataset", a.dataset, "--offset", str(todo[0]), "--h", str(a.h), "--quick"], log)
    if rc != 0:
        stop(f"smoke test failed (see {log})")
    check_fingerprint(text, a.dataset, todo[0])
    if "missing forecasts: 0.00%" not in text:
        stop(f"smoke test produced missing forecasts (see {log})")
    print(f"   smoke test OK in {sec:.0f}s", flush=True)
    if a.check_only:
        print("Check-only mode: everything is ready for the full run.", flush=True)
        return

    # ---- 3-6. full runs, one window at a time
    info_path = os.path.join(OUT, f"{a.dataset}_run_info.json")
    info = json.load(open(info_path, encoding="utf-8")) if os.path.exists(info_path) else {"machine": machine(), "runs": {}}
    for o in todo:
        print(f"3. Full run {a.dataset} window offset {o} (started {time.strftime('%H:%M')})", flush=True)
        log = os.path.join(OUT, "logs", f"{a.dataset}_w{o}_nhits_h{a.h}.log")
        rc, sec, text = run_logged(["--dataset", a.dataset, "--offset", str(o), "--h", str(a.h)], log)
        if rc != 0:
            stop(f"run failed with exit code {rc} (see {log}); send this log to Anh Duy")
        check_fingerprint(text, a.dataset, o)
        if "missing forecasts: 0.00%" not in text or "written" not in text:
            stop(f"run finished without a complete forecast file (see {log})")
        src = os.path.join(ROOT, "data", "cache", "forecasts", a.dataset + (f"_w{o}" if o else ""), f"nhits_h{a.h}.npz")
        dst = os.path.join(OUT, f"{a.dataset}_w{o}_nhits_h{a.h}.npz")
        shutil.copyfile(src, dst)
        info["runs"][f"w{o}"] = dict(seconds=round(sec), finished=time.strftime("%Y-%m-%d %H:%M"))
        with open(info_path, "w", encoding="utf-8") as fh:
            json.dump(info, fh, indent=2)
        print(f"4. Window offset {o} done in {sec / 60:.1f} min; committing", flush=True)
        git("add", "--", os.path.relpath(OUT, ROOT))
        if git("diff", "--cached", "--name-only"):
            git("commit", "-m", f"experiment: N-HiTS forecasts, {a.dataset} window offset {o}, h = {a.h}", "--",
                os.path.relpath(OUT, ROOT))
        if not a.no_push:
            git("pull", "--rebase", "--autostash")
            r = subprocess.run(["git", "push"], cwd=ROOT, capture_output=True, text=True)
            if r.returncode != 0:
                print("   push failed (no permission or network). The commit is saved locally; send the files in "
                      "code/outputs/neural/ to Anh Duy instead.\n" + r.stderr, flush=True)
            else:
                print("   pushed", flush=True)
    print("\nFinished. Results are in code/outputs/neural/.", flush=True)


if __name__ == "__main__":
    main()
