"""Paths and default experiment settings (see 04_proposed_system/data_flow.md)."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "data")
CACHE = os.path.join(DATA, "cache")
OUTPUTS = os.path.join(ROOT, "code", "outputs")

M5_DIR = os.path.join(DATA, "m5-forecasting-accuracy")
VN1_DIR = os.path.join(DATA, "Vn1 forcasting")

# Quantile levels forecast by every model.
QUANTILES = (0.5, 0.8, 0.9, 0.95, 0.99)

# ADI–CV² thresholds (paper 01, p. 7-8).
ADI_CUT = 4 / 3
CV2_CUT = 0.5

# Evaluation design.
TEST_WEEKS = 26          # last 26 weeks are the test period
BLOCK_WEEKS = 13         # models are retrained every 13 weeks
VALID_WEEKS = 13         # validation origins right before each training cutoff
WARMUP_WEEKS = 4         # simulation weeks excluded from KPIs

# Default scenario (grid in data_flow.md, section 7).
DEFAULT = dict(R=1, L=2, tau=0.9, H=13, q_liq=0.95, k_fixed=26)
