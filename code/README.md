# Code

## Data (not in git)

Put the datasets under `data/` at the repository root (the folder is git-ignored):

```text
data/
├── m5-forecasting-accuracy/            # Kaggle: M5 Forecasting - Accuracy
│   ├── calendar.csv
│   ├── sales_train_evaluation.csv
│   └── sell_prices.csv
├── Vn1 forcasting/                     # VN1 Forecasting – Accuracy Challenge (Vandeput, 2024)
│   ├── Phase 0 - Sales.csv, Phase 0 - Price.csv
│   ├── Phase 1 - Sales.csv, Phase 1 - Price.csv
│   └── Phase 2 - Sales.csv
└── vietnamsaleandinventory/            # Kaggle: tienanh2003/sales-and-inventory-snapshot-data  (appendix only)
    └── InventoryAndSale_snapshot_data/
        ├── Sales_snapshot_data/
        ├── Inventory_snapshot_data/
        └── MasterData/
```

## Scripts

| Script | Output | Purpose |
|---|---|---|
| `profile_datasets.py` | `outputs/data_profile.md`, `data/cache/*.parquet` | Size, sparsity and ADI–CV² classes of M5, VN1 and the Vietnam footwear dataset (appendix); inventory vs sales check |
| `liquidation_breakeven.py` | `outputs/<DATASET>/{breakeven,series_inventory}.csv` | RQ3: break-even salvage ratio of liquidation (upper/lower bound) over a holding-rate × margin grid; series-level weeks of supply |
| `analyze_results.py` | `outputs/comparison.md`, `outputs/fig_tradeoff_<D>.png` | Cross-dataset tables, inventory–fill-rate trade-off, ranking consistency |
| `run_pipeline.py` | `outputs/<DATASET>/{classes,forecast_metrics,kpi}.csv`, `summary.md` | Full benchmark: panel → ADI–CV² → forecasts → Decision Engine → lost-sales simulation → KPIs |

## Package `f2d/`

| Module | Pipeline step (`04_proposed_system/data_flow.md`) |
|---|---|
| `config.py` | Paths, quantiles, ADI–CV² cut-offs, split sizes, default scenario |
| `data.py` | 1–3. Weekly panel for M5 (277 full Walmart weeks) and VN1 (196 weeks, Phase 0+1+2) |
| `classify.py` | 4. ADI–CV² classes on the training period |
| `features.py` | 5. Lags, rolling stats, calendar/events, price, static attributes, scale |
| `models.py` | 6. Quantiles of D_{L+R} and D_H. Statistical: `empirical`, `ets` (ETS(A,N,N), normal), `tsb` (Poisson), `tsb_nb` (negative binomial). ML: `lgb_tweedie` (+ normal safety stock), `lgb_conformal` (+ split conformal by demand class), `hgb_quantile` (scikit-learn), `lgb_quantile` (main). No deep learning |
| `policy.py` | 7–8. Order-up-to + liquidation rules, multi-period lost-sales simulator, stock-out risk |
| `evaluate.py` | 9. SQL, RMSSE, coverage; fill rate, CSL, inventory and excess in weeks of demand, liquidation share, bootstrap CIs |

Design: last 26 weeks are the test period (2 blocks of 13 weeks); every model is refitted at each block cutoff
using only targets observed before it and forecasts every week from the newest data; the first 4 simulated
weeks are warm-up. Forecasts are cached in `data/cache/forecasts/<DATASET>/` — delete a file to recompute it.

```bash
pip install -r code/requirements.txt
```

```bash
python code/profile_datasets.py
```

```bash
python -u code/run_pipeline.py --dataset VN1 --boot 200
```

```bash
python -u code/run_pipeline.py --dataset M5 --boot 200
```

Quick check on one M5 store (a few minutes): `--stores CA_1 --tag smoke`. Scenario grid for RQ4: `--grid full`.
