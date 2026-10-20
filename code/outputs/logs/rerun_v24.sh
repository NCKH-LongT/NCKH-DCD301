#!/bin/sh
# v2.4 rerun: Tweedie on scaled target, τ grid {0.5..0.99}, dead-stock policies
set -e
export PYTHONIOENCODING=utf-8
cd "$(dirname "$0")/../../.."
python -u code/run_pipeline.py --dataset M5 --grid tau --boot 200 > code/outputs/logs/run_M5_v24.log 2>&1
python -u code/run_pipeline.py --dataset VN1 --grid full --boot 200 > code/outputs/logs/run_VN1_v24.log 2>&1
python -u code/liquidation_breakeven.py --dataset M5 > code/outputs/logs/breakeven_M5.log 2>&1
python -u code/liquidation_breakeven.py --dataset VN1 > code/outputs/logs/breakeven_VN1.log 2>&1
python -u code/stat_tests.py > code/outputs/logs/stat_tests.log 2>&1
python -u code/analyze_results.py > code/outputs/logs/analyze.log 2>&1
echo ALL_DONE
