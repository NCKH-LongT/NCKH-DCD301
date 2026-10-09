#!/bin/sh
# Chronos-2 (zero-shot foundation model) added as a 9th method. Outputs go to code/outputs/<D>[_wN]_c2 so the
# 8-method results stay unchanged; the forecast cache is shared (only chronos2 is computed).
# VN1 first (not in the Chronos-2 training corpora), then M5 (M5 is in autogluon/chronos_datasets and
# GiftEvalPretrain, so M5 results are not a clean zero-shot test).
set -e
export PYTHONIOENCODING=utf-8
cd "$(dirname "$0")/../../.."
export HF_HOME="$(pwd)/data/models/hf_home"
# wait for the third-window run to finish (shares the CPU)
while ! grep -q "^exit_" code/outputs/logs/rerun_w52.log 2>/dev/null; do sleep 60; done
M9=empirical,tsb,tsb_nb,ets,lgb_tweedie,lgb_conformal,hgb_quantile,lgb_quantile,chronos2
python -u code/run_pipeline.py --dataset VN1 --grid tau --boot 200 --models $M9 --out-suffix c2 > code/outputs/logs/run_VN1_c2.log 2>&1
python -u code/run_pipeline.py --dataset VN1 --grid tau --boot 200 --models $M9 --out-suffix c2 --offset 26 > code/outputs/logs/run_VN1_w26_c2.log 2>&1
python -u code/run_pipeline.py --dataset VN1 --grid tau --boot 200 --models $M9 --out-suffix c2 --offset 52 > code/outputs/logs/run_VN1_w52_c2.log 2>&1
python -u code/run_pipeline.py --dataset M5 --grid tau --boot 200 --models $M9 --out-suffix c2 > code/outputs/logs/run_M5_c2.log 2>&1
echo C2_DONE
