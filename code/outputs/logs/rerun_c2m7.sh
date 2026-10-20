#!/bin/sh
# Appendix: Chronos-2 compared with the seven-method benchmark, on VN1 (three windows) and VNF only.
# Also the seven-method version of the VNF case study. Cached forecasts only.
set -e
export PYTHONIOENCODING=utf-8
cd "$(dirname "$0")/../../.."
until grep -q "exit_" code/outputs/logs/rerun_m7_driver.log 2>/dev/null; do sleep 30; done
M7=empirical,tsb_nb,ets,lgb_tweedie,lgb_conformal,hgb_quantile,lgb_quantile
M8=$M7,chronos2
for W in 0 26 52; do
  if [ "$W" = "0" ]; then OFF=""; S=""; else OFF="--offset $W"; S="_w$W"; fi
  mkdir -p code/outputs/VN1${S}_c2m7
  python -u code/stat_tests.py --datasets VN1 --models $M8 $OFF --out-suffix c2m7 > code/outputs/logs/stat_tests${S}_c2m7.log 2>&1
  python -u code/equal_fill_ci.py --datasets VN1 --models $M8 $OFF --out-suffix c2m7 > code/outputs/logs/equal_fill_ci${S}_c2m7.log 2>&1
done
mkdir -p code/outputs/VNF_m7 code/outputs/VNF_c2m7
python -u code/stat_tests.py --datasets VNF --models $M7 --out-suffix m7 > code/outputs/logs/stat_tests_VNF_m7.log 2>&1
python -u code/equal_fill_ci.py --datasets VNF --models $M7 --out-suffix VNF_m7 > code/outputs/logs/equal_fill_ci_VNF_m7.log 2>&1
python -u code/stat_tests.py --datasets VNF --models $M8 --out-suffix c2m7 > code/outputs/logs/stat_tests_VNF_c2m7.log 2>&1
python -u code/equal_fill_ci.py --datasets VNF --models $M8 --out-suffix VNF_c2m7 > code/outputs/logs/equal_fill_ci_VNF_c2m7.log 2>&1
echo C2M7_DONE
