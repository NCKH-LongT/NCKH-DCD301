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

```bash
pip install -r code/requirements.txt
```

```bash
python code/profile_datasets.py
```
