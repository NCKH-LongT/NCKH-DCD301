#!/bin/sh
# Third test window: the 26 weeks ending 52 weeks before the end of the panel (panel truncated by 52 weeks)
set -e
export PYTHONIOENCODING=utf-8
cd "$(dirname "$0")/../../.."
python -u code/run_pipeline.py --dataset VN1 --grid tau --boot 200 --offset 52 > code/outputs/logs/run_VN1_w52.log 2>&1
python -u code/run_pipeline.py --dataset M5 --grid tau --boot 200 --offset 52 > code/outputs/logs/run_M5_w52.log 2>&1
python -u code/stat_tests.py --offset 52 > code/outputs/logs/stat_tests_w52.log 2>&1
python -u code/analyze_results.py --tag w52 > code/outputs/logs/analyze_w52.log 2>&1
echo W52_DONE
