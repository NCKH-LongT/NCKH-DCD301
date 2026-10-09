#!/bin/sh
# Second test window: the 26 weeks before the main test period (panel truncated by 26 weeks)
set -e
export PYTHONIOENCODING=utf-8
cd "$(dirname "$0")/../../.."
python -u code/run_pipeline.py --dataset M5 --grid tau --boot 200 --offset 26 > code/outputs/logs/run_M5_w26.log 2>&1
python -u code/run_pipeline.py --dataset VN1 --grid tau --boot 200 --offset 26 > code/outputs/logs/run_VN1_w26.log 2>&1
python -u code/stat_tests.py --offset 26 > code/outputs/logs/stat_tests_w26.log 2>&1
python -u code/analyze_results.py --tag w26 > code/outputs/logs/analyze_w26.log 2>&1
echo W26_DONE
