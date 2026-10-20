#!/bin/sh
# M5 full scenario grid (L in {1,2,4}, H in {8,13,26}, q_L, k) for the main window, as already run for VN1.
# Re-uses the cached forecasts at h = 3 and 13; LightGBM models are fitted for the extra horizons (2, 5, 8, 26).
set -e
export PYTHONIOENCODING=utf-8
cd "$(dirname "$0")/../../.."
python -u code/run_pipeline.py --dataset M5 --grid full --boot 200 > code/outputs/logs/run_M5_grid.log 2>&1
python -u code/analyze_results.py > code/outputs/logs/analyze.log 2>&1
echo M5_GRID_DONE
