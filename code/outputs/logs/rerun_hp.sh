#!/bin/sh
# Hyper-parameter sensitivity of LGB-Q vs LGB-T (h = 3, main window): VN1 first (fast), then M5.
set -e
export PYTHONIOENCODING=utf-8
cd "$(dirname "$0")/../../.."
python -u code/hparam_sensitivity.py --datasets VN1 > code/outputs/logs/hparam_VN1.log 2>&1
cp code/outputs/hparam_sensitivity.md code/outputs/hparam_sensitivity_VN1_only.md
python -u code/hparam_sensitivity.py --datasets VN1,M5 > code/outputs/logs/hparam_all.log 2>&1
echo HP_DONE
