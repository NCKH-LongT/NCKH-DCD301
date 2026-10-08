# Code

## Data (not in git)

Put the two datasets under `data/` at the repository root (the folder is git-ignored):

```text
data/
├── m5-forecasting-accuracy/            # Kaggle: M5 Forecasting - Accuracy
│   ├── calendar.csv
│   ├── sales_train_evaluation.csv
│   └── sell_prices.csv
└── vietnamsaleandinventory/            # Kaggle: tienanh2003/sales-and-inventory-snapshot-data
    └── InventoryAndSale_snapshot_data/
        ├── Sales_snapshot_data/
        ├── Inventory_snapshot_data/
        └── MasterData/
```

## Scripts

| Script | Output | Purpose |
|---|---|---|
| `profile_datasets.py` | `outputs/data_profile.md`, `data/cache/*.parquet` | Size, sparsity and ADI–CV² classes of both datasets at several aggregation levels; inventory vs sales check |

```bash
pip install -r code/requirements.txt
```

```bash
python code/profile_datasets.py
```
