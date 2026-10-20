#!/bin/sh
# Price ablation on VN1: the four ML models are refitted without the price features (three test windows).
# Statistical forecasts are copied from the standard cache (they use no features).
set -e
export PYTHONIOENCODING=utf-8
cd "$(dirname "$0")/../../.."
M=empirical,tsb,tsb_nb,ets,lgb_tweedie,lgb_conformal,hgb_quantile,lgb_quantile
for W in 26 0 52; do
  if [ "$W" = "0" ]; then OFF=""; TAG="nop"; else OFF="--offset $W"; TAG="w${W}_nop"; fi
  python -u code/run_pipeline.py --dataset VN1 --models $M --grid tau --boot 200 $OFF --no-price > code/outputs/logs/run_VN1_$TAG.log 2>&1
  python -u code/equal_fill_ci.py --datasets VN1 --models $M $OFF --fc-suffix nop > code/outputs/logs/equal_fill_ci_VN1_$TAG.log 2>&1
  python -u code/analyze_results.py --datasets VN1 --tag $TAG > code/outputs/logs/analyze_VN1_$TAG.log 2>&1
  echo "DONE_$TAG"
done
echo NOP_DONE
