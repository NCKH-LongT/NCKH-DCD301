#!/bin/sh
# Seven-method benchmark (TSB-P dropped): all ranks, tests and frontier tables recomputed from the cached forecasts.
set -e
export PYTHONIOENCODING=utf-8
cd "$(dirname "$0")/../../.."
M=empirical,tsb_nb,ets,lgb_tweedie,lgb_conformal,hgb_quantile,lgb_quantile
for W in 0 26 52; do
  if [ "$W" = "0" ]; then OFF=""; TAG=""; SFX="_m7"; else OFF="--offset $W"; TAG="--tag w$W"; SFX="_w${W}_m7"; fi
  mkdir -p code/outputs/M5$SFX code/outputs/VN1$SFX
  python -u code/stat_tests.py --models $M $OFF --out-suffix m7 > code/outputs/logs/stat_tests$SFX.log 2>&1
  python -u code/equal_fill_ci.py --models $M $OFF --out-suffix m7 > code/outputs/logs/equal_fill_ci$SFX.log 2>&1
  python -u code/analyze_results.py $TAG --exclude tsb --out-suffix m7 > code/outputs/logs/analyze$SFX.log 2>&1
  echo "DONE$SFX"
done
python -u code/robust_accuracy.py --models $M --out-suffix m7 > code/outputs/logs/robust_accuracy_m7.log 2>&1
python -u code/frontier_sensitivity.py --exclude tsb --out-suffix m7 > code/outputs/logs/frontier_sensitivity_m7.log 2>&1
echo M7_DONE
