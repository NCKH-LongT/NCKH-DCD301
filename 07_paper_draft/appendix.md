# Appendix

> Draft v0.2, English. Tables A1–A5 are generated from `code/outputs/` by `code/paper_appendix_tables.py`; every number can be re-derived from the cited CSV files. Tag conventions: `paper_outline.md`.

## A1. Inventory KPIs at the default scenario (τ = 0.9, no liquidation), main window

Fill rate, CSL, stockout rate (stockout weeks / weeks with demand) and inventory (weeks of demand); 95% bootstrap CIs over series (200 resamples). Source: `code/outputs/<D>/kpi.csv`.

**M5**

| Method | Fill rate [CI] | CSL | Stockout rate | Inventory [CI] |
|---|---|---|---|---|
| EMP | 0.935 [0.933, 0.937] | 0.906 | 0.117 | 1.78 [1.73, 1.82] |
| TSB-P | 0.891 [0.889, 0.893] | 0.873 | 0.158 | 1.00 [0.98, 1.02] |
| TSB-NB | 0.950 [0.949, 0.952] | 0.929 | 0.088 | 1.65 [1.62, 1.67] |
| ETS | 0.960 [0.959, 0.961] | 0.946 | 0.067 | 1.87 [1.84, 1.90] |
| LGB-T | 0.950 [0.948, 0.951] | 0.931 | 0.086 | 1.58 [1.55, 1.61] |
| LGB-C | 0.967 [0.966, 0.969] | 0.954 | 0.057 | 2.08 [2.06, 2.11] |
| HGB-Q | 0.951 [0.950, 0.952] | 0.937 | 0.079 | 1.53 [1.50, 1.55] |
| LGB-Q | 0.956 [0.954, 0.957] | 0.942 | 0.072 | 1.58 [1.55, 1.61] |

**VN1**

| Method | Fill rate [CI] | CSL | Stockout rate | Inventory [CI] |
|---|---|---|---|---|
| EMP | 0.888 [0.877, 0.898] | 0.943 | 0.137 | 2.80 [2.59, 3.00] |
| TSB-P | 0.823 [0.813, 0.832] | 0.910 | 0.216 | 1.31 [1.18, 1.45] |
| TSB-NB | 0.911 [0.902, 0.920] | 0.948 | 0.125 | 2.40 [2.22, 2.60] |
| ETS | 0.917 [0.908, 0.925] | 0.958 | 0.100 | 2.74 [2.53, 2.97] |
| LGB-T | 0.924 [0.917, 0.931] | 0.961 | 0.094 | 2.57 [2.37, 2.76] |
| LGB-C | 0.935 [0.925, 0.943] | 0.964 | 0.086 | 2.87 [2.67, 3.09] |
| HGB-Q | 0.945 [0.940, 0.951] | 0.972 | 0.068 | 3.47 [3.17, 3.79] |
| LGB-Q | 0.948 [0.943, 0.953] | 0.973 | 0.066 | 3.41 [3.13, 3.70] |

## A2. LightGBM-Tweedie trained on unscaled vs. scaled target

Source: `06_experiment_results/tables/tweedie_fix_before_after.csv` ([R §1.1]).

| dataset   | model         |   horizon | version                 |   SQL |   RMSSE |   cov_0.9 |
|:----------|:--------------|----------:|:------------------------|------:|--------:|----------:|
| M5        | lgb_tweedie   |         3 | before (raw D_h target) | 0.226 |   0.567 |     0.860 |
| M5        | lgb_tweedie   |        13 | before (raw D_h target) | 0.215 |   0.460 |     0.828 |
| M5        | lgb_conformal |         3 | before (raw D_h target) | 0.229 |   0.574 |     0.899 |
| M5        | lgb_conformal |        13 | before (raw D_h target) | 0.231 |   0.461 |     0.909 |
| M5        | lgb_tweedie   |         3 | after (D_h / s target)  | 0.229 |   0.565 |     0.858 |
| M5        | lgb_tweedie   |        13 | after (D_h / s target)  | 0.223 |   0.456 |     0.837 |
| M5        | lgb_conformal |         3 | after (D_h / s target)  | 0.232 |   0.572 |     0.901 |
| M5        | lgb_conformal |        13 | after (D_h / s target)  | 0.241 |   0.458 |     0.910 |
| VN1       | lgb_tweedie   |         3 | before (raw D_h target) | 0.496 |   0.819 |     0.922 |
| VN1       | lgb_tweedie   |        13 | before (raw D_h target) | 0.664 |   1.131 |     0.910 |
| VN1       | lgb_conformal |         3 | before (raw D_h target) | 0.436 |   0.800 |     0.907 |
| VN1       | lgb_conformal |        13 | before (raw D_h target) | 0.590 |   1.074 |     0.921 |
| VN1       | lgb_tweedie   |         3 | after (D_h / s target)  | 0.439 |   0.651 |     0.913 |
| VN1       | lgb_tweedie   |        13 | after (D_h / s target)  | 0.575 |   0.896 |     0.908 |
| VN1       | lgb_conformal |         3 | after (D_h / s target)  | 0.405 |   0.633 |     0.906 |
| VN1       | lgb_conformal |        13 | after (D_h / s target)  | 0.507 |   0.825 |     0.915 |

## A3. Scaled pinball loss by quantile (h = 3), intermittent series

Mean and median over series of the per-series scaled pinball loss, and share of series where LGB-Q has a strictly lower loss than TSB-NB. Source: `code/outputs/per_quantile_loss.csv`.

| Data | Window | q | Mean LGB-Q | Mean TSB-NB | Median LGB-Q | Median TSB-NB | LGB-Q lower (%) |
|---|---|---|---|---|---|---|---|
| VN1 | Main | 0.5 | 0.417 | 0.438 | 0.125 | 0.140 | 29.4 |
| VN1 | Main | 0.8 | 0.495 | 0.532 | 0.165 | 0.162 | 32.5 |
| VN1 | Main | 0.9 | 0.441 | 0.492 | 0.142 | 0.122 | 29.7 |
| VN1 | Main | 0.95 | 0.364 | 0.431 | 0.119 | 0.081 | 28.0 |
| VN1 | Main | 0.99 | 0.206 | 0.321 | 0.064 | 0.025 | 24.1 |
| VN1 | Second | 0.5 | 0.884 | 1.099 | 0.161 | 0.171 | 31.0 |
| VN1 | Second | 0.8 | 1.058 | 1.429 | 0.192 | 0.187 | 34.1 |
| VN1 | Second | 0.9 | 0.978 | 1.434 | 0.147 | 0.134 | 33.1 |
| VN1 | Second | 0.95 | 0.876 | 1.379 | 0.112 | 0.089 | 33.7 |
| VN1 | Second | 0.99 | 0.678 | 1.241 | 0.052 | 0.027 | 29.4 |
| VN1 | Third | 0.5 | 4.343 | 5.437 | 0.191 | 0.196 | 32.4 |
| VN1 | Third | 0.8 | 4.351 | 7.433 | 0.209 | 0.197 | 34.9 |
| VN1 | Third | 0.9 | 3.990 | 7.643 | 0.161 | 0.142 | 34.3 |
| VN1 | Third | 0.95 | 3.613 | 7.485 | 0.117 | 0.093 | 34.1 |
| VN1 | Third | 0.99 | 3.068 | 6.899 | 0.055 | 0.028 | 30.0 |
| M5 | Main | 0.5 | 0.473 | 0.521 | 0.309 | 0.322 | 59.5 |
| M5 | Main | 0.8 | 0.401 | 0.489 | 0.239 | 0.254 | 61.1 |
| M5 | Main | 0.9 | 0.296 | 0.393 | 0.156 | 0.170 | 59.1 |
| M5 | Main | 0.95 | 0.209 | 0.310 | 0.095 | 0.103 | 57.1 |
| M5 | Main | 0.99 | 0.096 | 0.194 | 0.027 | 0.026 | 48.7 |
| M5 | Second | 0.5 | 0.482 | 0.546 | 0.306 | 0.318 | 56.9 |
| M5 | Second | 0.8 | 0.414 | 0.522 | 0.238 | 0.246 | 55.2 |
| M5 | Second | 0.9 | 0.307 | 0.428 | 0.156 | 0.161 | 54.6 |
| M5 | Second | 0.95 | 0.220 | 0.344 | 0.095 | 0.098 | 53.9 |
| M5 | Second | 0.99 | 0.103 | 0.221 | 0.027 | 0.025 | 45.7 |
| M5 | Third | 0.5 | 0.491 | 0.547 | 0.296 | 0.307 | 55.6 |
| M5 | Third | 0.8 | 0.441 | 0.535 | 0.236 | 0.244 | 55.7 |
| M5 | Third | 0.9 | 0.339 | 0.447 | 0.156 | 0.164 | 56.2 |
| M5 | Third | 0.95 | 0.250 | 0.369 | 0.096 | 0.101 | 55.4 |
| M5 | Third | 0.99 | 0.127 | 0.255 | 0.028 | 0.026 | 46.3 |
| VNF | Main | 0.5 | 0.183 | 0.179 | 0.017 | 0.000 | 14.3 |
| VNF | Main | 0.8 | 0.266 | 0.261 | 0.075 | 0.027 | 30.5 |
| VNF | Main | 0.9 | 0.334 | 0.269 | 0.120 | 0.047 | 27.9 |
| VNF | Main | 0.95 | 0.277 | 0.254 | 0.094 | 0.048 | 21.0 |
| VNF | Main | 0.99 | 0.192 | 0.216 | 0.053 | 0.018 | 8.5 |

## A4. Inventory (weeks of demand) needed to reach a fill rate, by window and demand class

Point estimates, linear interpolation along the τ curve (τ ∈ [0.5, 0.99]); "—" = target not reached. Source: `code/outputs/equal_fill_ci*.csv` (identical to `comparison*.md`).

**M5, Main window, all** (n = 30,381)

| Method | 0.90 | 0.92 | 0.94 | 0.96 | 0.98 | Frontier rank |
|---|---|---|---|---|---|---|
| EMP | 1.41 | 1.62 | 1.88 | 2.31 | 3.14 | 7.20 |
| TSB-P | 1.08 | 1.32 | — | — | — | 6.70 |
| TSB-NB | 1.09 | 1.24 | 1.51 | 1.92 | 2.91 | 5.00 |
| ETS | 1.20 | 1.32 | 1.52 | 1.87 | 2.67 | 5.40 |
| LGB-T | 1.07 | 1.19 | 1.45 | 1.83 | — | 4.10 |
| LGB-C | 1.14 | 1.26 | 1.44 | 1.91 | 2.82 | 4.60 |
| HGB-Q | 1.03 | 1.15 | 1.39 | 1.74 | 2.60 | 2.00 |
| LGB-Q | 1.02 | 1.12 | 1.38 | 1.69 | 2.49 | 1.00 |

**VN1, Main window, all** (n = 13,844)

| Method | 0.90 | 0.92 | 0.94 | 0.96 | 0.98 | Frontier rank |
|---|---|---|---|---|---|---|
| EMP | 3.16 | 3.73 | 4.67 | — | — | 6.70 |
| TSB-P | — | — | — | — | — | 7.30 |
| TSB-NB | 2.21 | 2.67 | 3.50 | 4.79 | — | 4.80 |
| ETS | 2.38 | 2.83 | 3.54 | — | — | 6.10 |
| LGB-T | 2.05 | 2.48 | 3.19 | — | — | 3.30 |
| LGB-C | 2.10 | 2.55 | 3.22 | 4.72 | 8.94 | 3.00 |
| HGB-Q | 2.17 | 2.68 | 3.31 | 4.36 | 7.61 | 3.40 |
| LGB-Q | 2.07 | 2.54 | 3.17 | 4.13 | 7.24 | 1.40 |

**VN1, Main window, smooth** (n = 2,596)

| Method | 0.90 | 0.92 | 0.94 | 0.96 | 0.98 | Frontier rank |
|---|---|---|---|---|---|---|
| EMP | 1.70 | 2.02 | 2.43 | 3.12 | — | 6.80 |
| TSB-P | — | — | — | — | — | 7.60 |
| TSB-NB | 1.19 | 1.36 | 1.67 | 2.32 | — | 2.40 |
| ETS | 1.28 | 1.42 | 1.74 | 2.34 | — | 4.00 |
| LGB-T | 1.28 | 1.44 | 1.73 | 2.29 | — | 3.40 |
| LGB-C | 1.31 | 1.42 | 1.76 | 2.22 | 3.75 | 3.00 |
| HGB-Q | 1.34 | 1.51 | 1.93 | 2.41 | 3.82 | 5.40 |
| LGB-Q | 1.28 | 1.44 | 1.85 | 2.34 | 3.50 | 3.40 |

**VN1, Main window, erratic** (n = 1,901)

| Method | 0.90 | 0.92 | 0.94 | 0.96 | 0.98 | Frontier rank |
|---|---|---|---|---|---|---|
| EMP | 5.07 | 6.04 | 7.39 | — | — | 6.10 |
| TSB-P | — | — | — | — | — | 6.90 |
| TSB-NB | 4.22 | 5.45 | 6.79 | — | — | 5.30 |
| ETS | 4.39 | 5.19 | — | — | — | 5.90 |
| LGB-T | 3.59 | 4.52 | — | — | — | 4.30 |
| LGB-C | 3.81 | 4.71 | 6.74 | 9.08 | — | 3.70 |
| HGB-Q | 3.88 | 4.62 | 5.67 | 7.49 | 12.33 | 2.60 |
| LGB-Q | 3.60 | 4.28 | 5.35 | 7.18 | 11.86 | 1.20 |

**VN1, Main window, intermittent** (n = 6,539)

| Method | 0.90 | 0.92 | 0.94 | 0.96 | 0.98 | Frontier rank |
|---|---|---|---|---|---|---|
| EMP | 4.47 | 5.19 | — | — | — | 6.70 |
| TSB-P | — | — | — | — | — | 7.10 |
| TSB-NB | 2.12 | 2.64 | 3.68 | — | — | 3.20 |
| ETS | 2.59 | 3.13 | 4.01 | — | — | 5.20 |
| LGB-T | 2.51 | 2.96 | 3.72 | — | — | 4.40 |
| LGB-C | 3.36 | 3.73 | 4.10 | 6.56 | 16.41 | 4.80 |
| HGB-Q | 2.59 | 3.07 | 3.70 | 5.10 | 10.26 | 3.20 |
| LGB-Q | 2.47 | 2.90 | 3.64 | 4.88 | 8.96 | 1.40 |

**VN1, Main window, lumpy** (n = 2,808)

| Method | 0.90 | 0.92 | 0.94 | 0.96 | 0.98 | Frontier rank |
|---|---|---|---|---|---|---|
| EMP | 12.80 | — | — | — | — | 5.90 |
| TSB-P | — | — | — | — | — | 6.30 |
| TSB-NB | 8.99 | 10.76 | — | — | — | 5.20 |
| ETS | — | — | — | — | — | 6.30 |
| LGB-T | — | — | — | — | — | 6.30 |
| LGB-C | 6.11 | 8.11 | 10.11 | 20.64 | 32.40 | 2.80 |
| HGB-Q | 6.27 | 7.49 | 9.29 | 12.97 | 22.85 | 2.20 |
| LGB-Q | 6.06 | 7.11 | 8.69 | 11.85 | 21.24 | 1.00 |

**M5, Second window, all** (n = 29,917)

| Method | 0.90 | 0.92 | 0.94 | 0.96 | 0.98 | Frontier rank |
|---|---|---|---|---|---|---|
| EMP | 1.57 | 1.81 | 2.11 | 2.58 | 3.48 | 7.20 |
| TSB-P | 1.15 | 1.39 | — | — | — | 6.50 |
| TSB-NB | 1.18 | 1.31 | 1.60 | 1.99 | 2.95 | 4.00 |
| ETS | 1.29 | 1.43 | 1.60 | 1.99 | 2.79 | 5.20 |
| LGB-T | 1.19 | 1.31 | 1.59 | 1.98 | — | 4.50 |
| LGB-C | 1.26 | 1.38 | 1.61 | 2.07 | 3.01 | 5.60 |
| HGB-Q | 1.13 | 1.25 | 1.51 | 1.85 | 2.72 | 1.80 |
| LGB-Q | 1.13 | 1.24 | 1.49 | 1.80 | 2.59 | 1.20 |

**VN1, Second window, all** (n = 11,442)

| Method | 0.90 | 0.92 | 0.94 | 0.96 | 0.98 | Frontier rank |
|---|---|---|---|---|---|---|
| EMP | 2.10 | 2.46 | 3.03 | 4.05 | — | 6.90 |
| TSB-P | — | — | — | — | — | 7.70 |
| TSB-NB | 1.10 | 1.22 | 1.63 | 2.27 | 4.10 | 1.80 |
| ETS | 1.28 | 1.49 | 1.78 | 2.40 | — | 5.90 |
| LGB-T | 1.21 | 1.37 | 1.65 | 2.13 | — | 3.50 |
| LGB-C | 1.19 | 1.30 | 1.71 | 2.23 | 3.67 | 2.00 |
| HGB-Q | 1.21 | 1.38 | 1.77 | 2.37 | 4.19 | 4.40 |
| LGB-Q | 1.20 | 1.38 | 1.79 | 2.33 | 3.87 | 3.80 |

**VN1, Second window, smooth** (n = 2,265)

| Method | 0.90 | 0.92 | 0.94 | 0.96 | 0.98 | Frontier rank |
|---|---|---|---|---|---|---|
| EMP | 1.33 | 1.47 | 1.82 | 2.29 | 3.31 | 7.20 |
| TSB-P | 0.67 | — | — | — | — | 6.60 |
| TSB-NB | 0.75 | 0.86 | 1.02 | 1.34 | 2.17 | 2.00 |
| ETS | 0.80 | 0.94 | 1.08 | 1.39 | 2.14 | 2.60 |
| LGB-T | 0.81 | 0.94 | 1.10 | 1.44 | 2.13 | 3.60 |
| LGB-C | 0.86 | 0.97 | 1.08 | 1.43 | 2.07 | 4.00 |
| HGB-Q | 0.82 | 0.93 | 1.16 | 1.49 | 2.45 | 4.80 |
| LGB-Q | 0.83 | 0.95 | 1.18 | 1.48 | 2.15 | 5.20 |

**VN1, Second window, erratic** (n = 1,629)

| Method | 0.90 | 0.92 | 0.94 | 0.96 | 0.98 | Frontier rank |
|---|---|---|---|---|---|---|
| EMP | 3.03 | 3.47 | 4.51 | 5.91 | — | 6.90 |
| TSB-P | — | — | — | — | — | 7.70 |
| TSB-NB | 1.59 | 2.02 | 2.51 | 3.64 | 6.79 | 2.80 |
| ETS | 1.95 | 2.26 | 2.82 | 3.88 | — | 5.70 |
| LGB-T | 1.66 | 1.86 | 2.30 | 3.00 | — | 2.50 |
| LGB-C | 1.58 | 1.90 | 2.53 | 3.63 | 6.73 | 2.20 |
| HGB-Q | 1.67 | 2.11 | 2.70 | 4.17 | 6.72 | 4.20 |
| LGB-Q | 1.67 | 2.14 | 2.74 | 3.97 | 6.22 | 4.00 |

**VN1, Second window, intermittent** (n = 5,258)

| Method | 0.90 | 0.92 | 0.94 | 0.96 | 0.98 | Frontier rank |
|---|---|---|---|---|---|---|
| EMP | 3.68 | 4.20 | 4.80 | — | — | 6.60 |
| TSB-P | — | — | — | — | — | 7.20 |
| TSB-NB | 1.68 | 2.16 | 3.11 | — | — | 4.40 |
| ETS | 1.76 | 2.18 | 2.87 | — | — | 5.20 |
| LGB-T | 1.74 | 2.00 | 2.51 | — | — | 3.60 |
| LGB-C | 2.26 | 2.70 | 3.14 | 4.68 | 14.14 | 4.80 |
| HGB-Q | 1.70 | 2.01 | 2.54 | 3.80 | 7.52 | 2.20 |
| LGB-Q | 1.70 | 2.02 | 2.53 | 3.46 | 6.98 | 2.00 |

**VN1, Second window, lumpy** (n = 2,290)

| Method | 0.90 | 0.92 | 0.94 | 0.96 | 0.98 | Frontier rank |
|---|---|---|---|---|---|---|
| EMP | 5.14 | 6.07 | 7.85 | 10.02 | — | 6.90 |
| TSB-P | — | — | — | — | — | 7.70 |
| TSB-NB | 1.75 | 2.29 | 2.87 | 4.15 | 8.24 | 2.40 |
| ETS | 2.52 | 2.94 | 3.87 | 5.57 | — | 6.10 |
| LGB-T | 2.23 | 2.48 | 2.97 | 3.81 | — | 3.30 |
| LGB-C | 2.27 | 2.89 | 3.51 | 4.13 | 7.63 | 4.40 |
| HGB-Q | 2.23 | 2.60 | 3.15 | 4.08 | 6.88 | 3.20 |
| LGB-Q | 2.16 | 2.46 | 3.08 | 3.89 | 6.33 | 2.00 |

**M5, Third window, all** (n = 28,824)

| Method | 0.90 | 0.92 | 0.94 | 0.96 | 0.98 | Frontier rank |
|---|---|---|---|---|---|---|
| EMP | 1.75 | 1.98 | 2.34 | 2.87 | 3.98 | 7.20 |
| TSB-P | 1.36 | 1.64 | — | — | — | 7.10 |
| TSB-NB | 1.33 | 1.53 | 1.82 | 2.29 | 3.44 | 4.40 |
| ETS | 1.47 | 1.62 | 1.84 | 2.23 | 3.15 | 4.80 |
| LGB-T | 1.35 | 1.49 | 1.79 | 2.24 | — | 4.30 |
| LGB-C | 1.40 | 1.52 | 1.87 | 2.31 | 3.43 | 5.20 |
| HGB-Q | 1.32 | 1.45 | 1.74 | 2.13 | 3.15 | 2.00 |
| LGB-Q | 1.31 | 1.44 | 1.74 | 2.12 | 3.07 | 1.00 |

**VN1, Third window, all** (n = 9,383)

| Method | 0.90 | 0.92 | 0.94 | 0.96 | 0.98 | Frontier rank |
|---|---|---|---|---|---|---|
| EMP | 3.71 | 4.42 | — | — | — | 6.25 |
| TSB-P | — | — | — | — | — | 6.88 |
| TSB-NB | 2.44 | 3.27 | — | — | — | 5.50 |
| ETS | 2.62 | — | — | — | — | 6.38 |
| LGB-T | 2.17 | 3.03 | — | — | — | 5.00 |
| LGB-C | 2.10 | 2.63 | 3.69 | 13.22 | — | 2.25 |
| HGB-Q | 2.15 | 2.64 | 3.35 | 5.09 | — | 2.50 |
| LGB-Q | 2.12 | 2.62 | 3.31 | 4.83 | — | 1.25 |

**VN1, Third window, smooth** (n = 2,094)

| Method | 0.90 | 0.92 | 0.94 | 0.96 | 0.98 | Frontier rank |
|---|---|---|---|---|---|---|
| EMP | 1.87 | 2.18 | 2.70 | — | — | 6.90 |
| TSB-P | — | — | — | — | — | 7.50 |
| TSB-NB | 0.97 | 1.21 | 1.55 | 2.21 | — | 2.60 |
| ETS | 1.11 | 1.29 | 1.63 | 2.25 | — | 4.20 |
| LGB-T | 1.12 | 1.29 | 1.64 | 2.38 | — | 4.60 |
| LGB-C | 1.06 | 1.22 | 1.55 | 2.11 | 4.02 | 1.80 |
| HGB-Q | 1.16 | 1.32 | 1.71 | 2.21 | 3.58 | 4.80 |
| LGB-Q | 1.16 | 1.32 | 1.69 | 2.16 | 3.36 | 3.60 |

**VN1, Third window, erratic** (n = 1,202)

| Method | 0.90 | 0.92 | 0.94 | 0.96 | 0.98 | Frontier rank |
|---|---|---|---|---|---|---|
| EMP | 6.39 | 7.59 | 8.79 | — | — | 5.00 |
| TSB-P | — | — | — | — | — | 6.75 |
| TSB-NB | 5.53 | 6.54 | — | — | — | 5.38 |
| ETS | 5.18 | — | — | — | — | 5.88 |
| LGB-T | — | — | — | — | — | 6.75 |
| LGB-C | 4.66 | 5.59 | 9.06 | 12.56 | — | 3.00 |
| HGB-Q | 4.61 | 5.61 | 7.55 | 10.52 | — | 2.25 |
| LGB-Q | 4.54 | 5.53 | 7.05 | 10.06 | — | 1.00 |

**VN1, Third window, intermittent** (n = 4,278)

| Method | 0.90 | 0.92 | 0.94 | 0.96 | 0.98 | Frontier rank |
|---|---|---|---|---|---|---|
| EMP | — | — | — | — | — | — |
| TSB-P | — | — | — | — | — | — |
| TSB-NB | — | — | — | — | — | — |
| ETS | — | — | — | — | — | — |
| LGB-T | — | — | — | — | — | — |
| LGB-C | — | — | — | — | — | — |
| HGB-Q | — | — | — | — | — | — |
| LGB-Q | — | — | — | — | — | — |

**VN1, Third window, lumpy** (n = 1,809)

| Method | 0.90 | 0.92 | 0.94 | 0.96 | 0.98 | Frontier rank |
|---|---|---|---|---|---|---|
| EMP | — | — | — | — | — | 6.00 |
| TSB-P | — | — | — | — | — | 6.00 |
| TSB-NB | — | — | — | — | — | 6.00 |
| ETS | — | — | — | — | — | 6.00 |
| LGB-T | — | — | — | — | — | 6.00 |
| LGB-C | 8.42 | 38.46 | 73.10 | 107.73 | — | 3.00 |
| HGB-Q | 6.75 | 8.17 | 11.58 | — | — | 1.67 |
| LGB-Q | 6.75 | 8.05 | 11.53 | — | — | 1.33 |

## A5. Value-weighted inventory at fill rate 0.94 with bootstrap CIs

As Table 5, with units weighted by the weekly selling price. Δ = I_method / I_LGB-Q − 1 (%). Source: `code/outputs/equal_fill_ci*.csv`.

| Dataset | Window | LGB-Q inventory | Frontier rank | P(best) | HGB-Q | LGB-T | LGB-C | TSB-NB | ETS |
|---|---|---|---|---|---|---|---|---|---|
| M5 | Main | 1.42 [1.38, 1.46] | 1.00 | 1.00 | +1.2 [+0.9, +1.6] | +4.8 [+4.1, +5.4] | +6.6 [+5.3, +7.8] | +7.7 [+6.9, +8.5] | +9.7 [+8.9, +10.5] |
| M5 | Second | 1.60 [1.55, 1.67] | 1.00 | 1.00 | +1.2 [+1.0, +1.4] | +5.3 [+4.7, +6.1] | +6.7 [+5.4, +8.0] | +5.7 [+5.0, +6.4] | +7.2 [+6.4, +8.0] |
| M5 | Third | 1.76 [1.72, 1.80] | 1.00 | 1.00 | +0.3 [-0.0, +0.5] | +4.4 [+3.7, +5.2] | +9.2 [+7.5, +11.2] | +4.4 [+3.5, +5.3] | +6.6 [+5.7, +7.6] |
| VN1 | Main | 4.07 [3.42, 5.03] | 1.80 | 0.98 | +5.0 [+2.4, +9.6] | -1.4 [-18.0, +13.0] | +7.2 [-0.0, +19.1] | +15.3 [-1.2, +27.7] | +17.1 [+0.3, +30.1] |
| VN1 | Second | 2.58 [2.10, 3.52] | 4.80 | 0.00 | -1.7 [-3.1, +0.5] | -12.5 [-26.2, -6.1] | -9.7 [-18.4, -6.5] | -13.0 [-23.0, -7.2] | -2.6 [-16.1, +3.7] |
| VN1 | Third | 4.44 [3.61, 5.31] | 1.50 | 0.59 | +0.4 [-4.1, +3.4] | — | +1.8 [-7.6, +79.9] | — | — |

## A6. Preparation of the Vietnamese footwear data (VNF)

Implementation: `code/f2d/data.py`, function `load_vnf`; source tables from `code/profile_datasets.py` ([DP]).

1. Use the monthly sales files of the Vietnam Datathon 2023 snapshot data (831,966 rows, 227 sites, 30,367 SKUs) and keep the retail channel ("Bán lẻ") [DP].
2. Drop rows with negative quantity (returns; 26,432 rows over all channels) [DP].
3. Map each SKU to its style (mold code) and colour from the product master; a series is a style–colour summed over all stores.
4. Fix week codes at the year boundary: drop 202153 (1–2 January 2022), merge 202352 (1 January 2023) into 202252, and drop the incomplete last week 202331 (31 July 2023). The result is a gap-free weekly grid of 82 ISO weeks starting 2022-01-03.
5. Weekly price = net revenue / units, carried forward; per-series unit cost and price = medians of the weekly cost and price per unit.
6. Series start at their first sale; demand classes and the evaluation rule as for M5 and VN1 (Section 3.2).

Data caveats are listed in Section 3.2 and Section 6.4.
