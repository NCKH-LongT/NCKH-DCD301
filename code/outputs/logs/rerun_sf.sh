#!/bin/sh
# Feature parity on M5: the four ML models are refitted with the 21 features shared with VN1
# (no events, SNAP days or static attributes). Statistical forecasts are copied from the standard cache.
set -e
export PYTHONIOENCODING=utf-8
cd "$(dirname "$0")/../../.."
# wait for the VN1 price ablation to finish (same CPU)
until grep -q "exit_" code/outputs/logs/rerun_nop_driver.log 2>/dev/null; do sleep 30; done
M=empirical,tsb,tsb_nb,ets,lgb_tweedie,lgb_conformal,hgb_quantile,lgb_quantile
for W in 0 26 52; do
  if [ "$W" = "0" ]; then OFF=""; TAG="sf"; else OFF="--offset $W"; TAG="w${W}_sf"; fi
  python -u code/run_pipeline.py --dataset M5 --models $M --grid tau --boot 200 $OFF --shared-features > code/outputs/logs/run_M5_$TAG.log 2>&1
  python -u code/equal_fill_ci.py --datasets M5 --models $M $OFF --fc-suffix sf > code/outputs/logs/equal_fill_ci_M5_$TAG.log 2>&1
  echo "DONE_$TAG"
done
echo SF_DONE
