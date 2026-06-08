# Optimized Research & Code Guide  
# Change-Point-Guided Validation of TTF Stage Boundaries for Three-Stage Bearing Health Classification

## 0. Mục tiêu tối ưu của file này

File này chỉnh lại hướng nghiên cứu để bài có **contribution mạnh hơn**, tránh bị xem là “chỉ đổi ngưỡng thủ công”, đồng thời đưa thêm một số bài tương tự để định vị gap.

Ý tưởng ban đầu:

```text
Healthy   : [0, 0.60)
Degrading : [0.60, 0.90)
Fault     : [0.90, 1.00]
```

Vấn đề nghiên cứu:

> Trong các bài toán bearing run-to-failure, việc chia Healthy / Degrading / Fault thường dựa trên ngưỡng TTF hoặc kinh nghiệm. Nếu không kiểm chứng ngưỡng, nhãn stage có thể gây bias cho mô hình classification.

Hướng tối ưu:

> Không chỉ chứng minh 60/90 là hợp lý, mà đề xuất một **framework kiểm chứng và lựa chọn stage boundary dựa trên dữ liệu** bằng vibration–temperature health indicators, change-point detection, separability analysis và downstream classification robustness.

---

# 1. Tên bài báo đề xuất

## Tên khuyến nghị

```text
Change-Point-Guided Validation of Time-to-Failure Stage Boundaries for Three-Stage Bearing Health Classification
```

## Tên ngắn hơn

```text
Data-Driven Validation of Stage Boundaries for Bearing Health Classification
```

## Tên nhấn mạnh vibration–temperature

```text
Vibration–Temperature Health Indicator Based Validation of Stage Boundaries in Run-to-Failure Bearing Classification
```

## Tên nếu muốn nối với bài Mamba sau này

```text
From Fixed TTF Labels to Data-Driven Stage Boundaries in Bearing Degradation Classification
```

---

# 2. Định vị contribution để không bị trùng

## 2.1. Không nên claim

Không nên viết:

```text
We propose the first method for bearing degradation stage division.
```

Vì đã có nhiều bài về:

- Health indicator construction.
- Degradation stage division.
- Change-point detection.
- RUL prediction.
- Stage-based bearing prognosis.

## 2.2. Nên claim

Nên viết:

```text
Although previous studies have investigated health indicator construction and degradation stage division, the effect of fixed TTF-based stage boundaries on three-stage bearing classification remains insufficiently examined, especially when vibration and temperature signals are jointly considered. This study proposes a practical validation framework that combines health indicator trajectory analysis, change-point detection, threshold sensitivity analysis, and downstream classification robustness to assess whether selected Healthy–Degrading–Fault boundaries are data-supported.
```

## 2.3. Contribution mạnh hơn

### Contribution 1 — Boundary validation framework

Đề xuất một framework để kiểm chứng ngưỡng Healthy–Degrading–Fault trong run-to-failure bearing classification, thay vì chọn ngưỡng TTF theo cảm tính.

### Contribution 2 — Multi-modal health indicator

Xây dựng health indicator từ cả:

```text
two-axis vibration features
+
two-channel temperature trend descriptors
```

Điểm này giúp khác với nhiều bài vibration-only.

### Contribution 3 — Change-point + classification robustness

Không chỉ dùng change-point detection để tìm điểm chuyển, mà còn kiểm tra các ngưỡng candidate bằng downstream classification:

```text
candidate thresholds
→ stage labels
→ train classifier
→ compare Macro-F1 / F1 Degrading / Healthy–Degrading confusion
```

### Contribution 4 — Threshold sensitivity analysis

Đánh giá độ nhạy của mô hình classification khi thay đổi ngưỡng:

```text
50/85, 55/90, 60/90, 65/90, 70/95
```

Nếu 60/90 nằm trong vùng ổn định, có thể nói ngưỡng này được hỗ trợ bởi dữ liệu. Nếu không, bài vẫn có contribution vì chỉ ra fixed threshold có thể chưa tối ưu.

### Contribution 5 — Bridge to sequence-aware models

Kết quả boundary validation có thể dùng làm nền cho bài sau:

```text
CNN-Mamba + Temperature Fusion for Bearing Health Stage Classification
```

---

# 3. Bài tương tự và khoảng trống nghiên cứu

## 3.1. Nhóm bài về degradation stage / RUL

| Nhóm | Bài tương tự | Họ làm gì | Khoảng trống để mình khai thác |
|---|---|---|---|
| Stage-based RUL | Stage-Based Remaining Useful Life Prediction for Bearings, Machines 2025 | Dùng feature extraction và GNN cho bearing degradation stage/RUL | Tập trung RUL, chưa tập trung kiểm chứng ngưỡng TTF cho bài toán 3-class classification |
| Multi-stage RUL | Rolling bearing degradation stage division and RUL prediction, Reliability Engineering & System Safety 2025 | Có health state classification và degradation starting point | Mục tiêu chính là RUL, không phải threshold sensitivity cho Healthy/Degrading/Fault labels |
| Adaptive RUL | Adaptive prediction approach for rolling bearing RUL, Reliability Engineering & System Safety 2022 | Xem degradation trend có nhiều stage và bất định | Tập trung stochastic process/RUL, chưa kiểm chứng ngưỡng TTF cố định |
| Change-point RUL | Change Point Detection Integrated Remaining Useful Life Estimation, arXiv 2024 | Dùng change points để hỗ trợ labeling cho LSTM RUL | Tập trung RUL, không phải stage-boundary validation cho classification |
| Slope-based CPD | Bearing RUL prediction with slope-based change-point detection, 2025 | Xây HI và tìm fault change point cho RUL | Tập trung xác định điểm fault/RUL, chưa phân tích nhiều threshold Healthy–Degrading–Fault |
| Stage division + GMM | Health Indicator and Stage Division using improved GMM and confidence value | Xây HI và chia stage bằng GMM | Khác ở phương pháp: bài mình dùng CPD + sensitivity + classification robustness |
| Adaptive degradation recognition | Outlier cleaning based adaptive recognition for degradation stage, 2022 | Nhận diện degradation stage, dùng kỹ thuật làm sạch ngoại lệ | Có liên quan stage recognition, nhưng bài mình tập trung kiểm chứng ngưỡng TTF và multi-modal vibration–temperature |

## 3.2. Gap statement tối ưu

Có thể viết trong bài:

```text
Existing bearing prognostics studies have extensively investigated health indicator construction, degradation point detection, and stage-based RUL prediction. However, in three-stage bearing health classification, the stage labels are often derived from fixed lifetime or TTF thresholds, and the sensitivity of these thresholds is rarely examined. Moreover, most threshold validation procedures rely primarily on vibration indicators, while temperature trends, which can reflect frictional and thermal degradation effects, are less frequently used to support stage boundary validation. This motivates a data-driven framework for validating TTF-based Healthy–Degrading–Fault boundaries using vibration–temperature health indicators, change-point detection, and downstream classification robustness.
```

## 3.3. Novelty positioning

Bài của mình không cạnh tranh trực tiếp với các bài RUL phức tạp. Bài của mình có vai trò:

```text
Before training a complex classifier or RUL model, first validate whether the stage labels are data-supported.
```

Đây là điểm thực tế và dễ thuyết phục ở hội thảo.

---

# 4. Research Questions

## RQ1

Các vibration–temperature health indicators có thể phản ánh các vùng chuyển tiếp trong vòng đời vòng bi không?

## RQ2

Các thuật toán change-point detection có phát hiện được transition regions gần với các ngưỡng TTF 0.60 và 0.90 không?

## RQ3

Khi thay đổi ngưỡng stage, hiệu năng classification thay đổi như thế nào?

## RQ4

Ngưỡng 60/90 có tạo ra sự cân bằng tốt giữa Macro-F1, F1 Degrading và Healthy–Degrading confusion không?

## RQ5

Temperature trend có đóng góp gì trong việc hỗ trợ boundary validation so với vibration-only health indicators?

---

# 5. Hypotheses

## H1

Health indicators được xây từ vibration + temperature sẽ thể hiện các thay đổi rõ hơn so với vibration-only indicators.

## H2

Change-point detection sẽ phát hiện các transition regions gần vùng 0.60 và 0.90 TTF hoặc chỉ ra vùng thay thế phù hợp hơn.

## H3

Ngưỡng 60/90 sẽ nằm trong nhóm threshold settings có classification robustness tốt nếu nó phản ánh đúng thay đổi dữ liệu.

## H4

F1 Degrading và Healthy–Degrading confusion nhạy cảm hơn Accuracy khi đánh giá stage-boundary quality.

## H5

Temperature trend features giúp boundary validation ổn định hơn ở giai đoạn Degrading/Fault transition.

---

# 6. Pipeline nghiên cứu tối ưu

```text
Raw vibration + temperature
        ↓
File/window metadata with normalized TTF
        ↓
Feature extraction
        ↓
Vibration-only HI
        ↓
Vibration–temperature HI
        ↓
Change-point detection
        ↓
Candidate threshold generation
        ↓
Stage labeling under each threshold set
        ↓
Feature separability analysis
        ↓
Classification robustness analysis
        ↓
Boundary recommendation / validation
```

Điểm mới nằm ở việc kết hợp 4 bằng chứng:

```text
1. Health indicator trajectory
2. Change-point detection
3. Feature/stage separability
4. Downstream classification robustness
```

---

# 7. Candidate thresholds

Bộ threshold chính:

| Setting | Healthy | Degrading | Fault | Vai trò |
|---|---|---|---|---|
| T1 | [0, 0.50) | [0.50, 0.85) | [0.85, 1.00] | fault sớm hơn |
| T2 | [0, 0.55) | [0.55, 0.90) | [0.90, 1.00] | healthy ngắn hơn |
| T3 | [0, 0.60) | [0.60, 0.90) | [0.90, 1.00] | baseline hiện tại |
| T4 | [0, 0.65) | [0.65, 0.90) | [0.90, 1.00] | degrading muộn hơn |
| T5 | [0, 0.70) | [0.70, 0.95) | [0.95, 1.00] | fault rất muộn |

Nếu change-point detection tìm ra điểm khác, thêm một setting data-driven:

| Setting | Healthy | Degrading | Fault | Vai trò |
|---|---|---|---|---|
| TD | [0, cp1) | [cp1, cp2) | [cp2, 1.00] | data-driven boundary |

Ví dụ:

```text
cp1 = 0.62
cp2 = 0.88
```

Thì:

```text
TD: [0,0.62), [0.62,0.88), [0.88,1.00]
```

---

# 8. Feature extraction

## 8.1. Vibration features

Dùng cả hai trục vibration:

```text
vib_x
vib_y
```

Feature đề xuất:

| Feature | Ý nghĩa |
|---|---|
| mean | giá trị trung bình |
| std | độ dao động |
| RMS | năng lượng rung |
| peak | biên độ cực đại |
| kurtosis | xung bất thường |
| skewness | độ lệch phân phối |
| crest factor | mức xung đỉnh |
| spectral energy | năng lượng miền tần số |
| spectral centroid | trọng tâm phổ |
| low-band energy | năng lượng tần số thấp |
| mid-band energy | năng lượng tần số trung |
| high-band energy | năng lượng tần số cao |

## 8.2. Temperature features

Dùng hai kênh nhiệt:

```text
bearing temperature
ambient temperature
```

Feature đề xuất:

| Feature | Ý nghĩa |
|---|---|
| temp_mean | nhiệt độ trung bình |
| temp_std | độ dao động |
| temp_min | min |
| temp_max | max |
| temp_delta | cuối - đầu |
| temp_slope | xu hướng tăng/giảm |
| temp_rolling_mean | xu hướng cục bộ |
| temp_rolling_std | độ bất ổn cục bộ |

## 8.3. Feature groups để ablation

Cần tạo 3 nhóm feature:

```text
G1: vibration-only
G2: temperature-only
G3: vibration + temperature
```

Bảng ablation:

| Feature group | Purpose |
|---|---|
| Vibration-only | So với literature phổ biến |
| Temperature-only | Xem nhiệt độ có tự phản ánh degradation không |
| Vibration + Temperature | Proposed multi-modal boundary validation |

---

# 9. Health Indicator Construction

## 9.1. PCA-based HI

```text
features → StandardScaler → PCA(n_components=1) → HI
```

Nếu correlation giữa HI và TTF âm:

```text
HI = -HI
```

Sau đó scale:

```text
HI ∈ [0,1]
```

## 9.2. Weighted mean HI

Chọn các feature nhạy suy giảm:

```text
RMS, kurtosis, spectral_energy, crest_factor, temp_slope, temp_delta
```

Chuẩn hóa min-max rồi lấy trung bình.

## 9.3. Proposed HI variants

Nên báo cáo ít nhất 2 HI:

| HI | Feature group | Method |
|---|---|---|
| HI-V | vibration-only | PCA |
| HI-T | temperature-only | PCA hoặc weighted mean |
| HI-VT | vibration + temperature | PCA hoặc weighted mean |

Nếu HI-VT cho change points ổn định hơn, đó là contribution tốt.

---

# 10. Change-point detection

Dùng 3 phương pháp:

| Method | Lý do |
|---|---|
| Binary Segmentation | dễ kiểm soát số điểm chuyển |
| PELT | phổ biến, tìm nhiều change points |
| Window-based CPD | dễ trực quan hóa |
| Optional: CUSUM | dễ giải thích nếu viết ngắn |

Kết quả cần lưu:

```text
change_point_results.csv
```

Format:

```csv
hi_variant,method,cp1,cp2,distance_to_60_90
HI-V,binary,0.58,0.91,0.03
HI-VT,binary,0.61,0.89,0.02
...
```

Cách tính khoảng cách tới 60/90:

```text
distance_to_60_90 = |cp1 - 0.60| + |cp2 - 0.90|
```

Nếu dùng data-driven threshold:

```text
cp1 = median(cp1 của các method)
cp2 = median(cp2 của các method)
```

---

# 11. Separability analysis

Đây là phần làm contribution mạnh hơn so với chỉ dùng classifier.

Với mỗi threshold setting, tính:

| Metric | Ý nghĩa |
|---|---|
| Silhouette score | class separation |
| Davies-Bouldin index | càng thấp càng tốt |
| Calinski-Harabasz score | càng cao càng tốt |

Input:

```text
feature vectors + stage labels
```

Nếu T3 hoặc TD có separability tốt, có thêm bằng chứng cho boundary.

Output:

```text
separability_results.csv
```

---

# 12. Classification robustness analysis

Với mỗi threshold setting:

```text
T1, T2, T3, T4, T5, TD
```

Train các classifier:

```text
SVM
Random Forest
Logistic Regression
Optional: XGBoost
```

Metrics:

| Metric | Lý do |
|---|---|
| Accuracy | tổng quan |
| Macro-F1 | class imbalance |
| F1 Healthy | false alarm |
| F1 Degrading | quan trọng nhất |
| F1 Fault | fault detection |
| Healthy → Degrading confusion | false degradation |
| Degrading → Healthy confusion | missed degradation |
| Balanced Accuracy | hữu ích nếu lệch class |

Metric quan trọng nhất:

```text
F1 Degrading
Healthy–Degrading confusion
Macro-F1
```

Không nên chỉ dùng Accuracy.

---

# 13. Boundary recommendation score

Để bài có tính “framework”, nên đề xuất một điểm tổng hợp:

```text
Boundary Score = 
0.30 × normalized_change_point_consistency
+ 0.25 × normalized_separability
+ 0.25 × Macro-F1
+ 0.20 × F1_Degrading
```

Trong đó:

```text
change_point_consistency = 1 - distance_to_detected_cps
```

Hoặc đơn giản hơn:

```text
Boundary Score = 
0.4 × Macro-F1 
+ 0.4 × F1_Degrading 
- 0.2 × Normalized_H-D_Confusion
```

Bản an toàn cho hội thảo:

```text
Boundary Score = 0.4 × Macro-F1 + 0.4 × F1_Degrading + 0.2 × F1_Fault
```

Sau đó xếp hạng threshold:

| Threshold | Boundary Score | Rank |
|---|---:|---:|
| T3 |  |  |
| TD |  |  |
| T2 |  |  |

Điểm này giúp bài có một artifact rõ: **recommendation framework**.

---

# 14. Code update: cấu trúc thư mục tối ưu

```text
bearing_stage_boundary/
│
├── configs/
│   └── config.yaml
│
├── data/
│   ├── raw/
│   ├── metadata/
│   └── processed/
│
├── src/
│   ├── 01_prepare_metadata.py
│   ├── 02_extract_features.py
│   ├── 03_build_health_index.py
│   ├── 04_change_point_detection.py
│   ├── 05_generate_stage_labels.py
│   ├── 06_separability_analysis.py
│   ├── 07_train_classifiers.py
│   ├── 08_boundary_score.py
│   ├── 09_plot_results.py
│   └── utils.py
│
├── results/
│   ├── tables/
│   ├── figures/
│   └── logs/
│
├── paper/
│   ├── related_work_matrix.md
│   ├── method_notes.md
│   └── result_tables.md
│
└── README.md
```

---

# 15. Config tối ưu

```yaml
data:
  raw_dir: "data/raw"
  processed_dir: "data/processed"
  metadata_path: "data/metadata/files.csv"

signal:
  sampling_rate: 25600
  window_sec: 1.0
  overlap: 0.5

health_index:
  variants:
    - name: "HI_V"
      feature_group: "vibration"
      method: "pca"
    - name: "HI_T"
      feature_group: "temperature"
      method: "pca"
    - name: "HI_VT"
      feature_group: "vibration_temperature"
      method: "pca"

change_point:
  n_bkps: 2
  model: "rbf"
  methods:
    - "binary"
    - "pelt"
    - "window"

thresholds:
  fixed:
    T1: [0.50, 0.85]
    T2: [0.55, 0.90]
    T3: [0.60, 0.90]
    T4: [0.65, 0.90]
    T5: [0.70, 0.95]
  include_data_driven: true

classification:
  test_size: 0.2
  random_state: 42
  models:
    - "svm"
    - "random_forest"
    - "logistic_regression"

boundary_score:
  macro_f1_weight: 0.4
  f1_degrading_weight: 0.4
  f1_fault_weight: 0.2
```

---

# 16. Code bổ sung: separability analysis

Tạo file:

```text
src/06_separability_analysis.py
```

```python
from pathlib import Path
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score
)


def select_feature_columns(df):
    ignore = {
        "file_id", "file_name", "file_path",
        "file_index", "ttf_percent",
        "stage", "stage_id"
    }

    return [
        c for c in df.columns
        if c not in ignore and pd.api.types.is_numeric_dtype(df[c])
    ]


def compute_separability(df):
    feature_cols = select_feature_columns(df)

    X = df[feature_cols].replace([np.inf, -np.inf], np.nan).fillna(0.0)
    y = df["stage_id"].values

    X = StandardScaler().fit_transform(X)

    # Need at least 2 labels for these metrics
    if len(set(y)) < 2:
        return {
            "silhouette": np.nan,
            "davies_bouldin": np.nan,
            "calinski_harabasz": np.nan
        }

    return {
        "silhouette": silhouette_score(X, y),
        "davies_bouldin": davies_bouldin_score(X, y),
        "calinski_harabasz": calinski_harabasz_score(X, y)
    }


def main():
    labeled_dir = Path("data/processed/labeled_thresholds")
    output_dir = Path("results/tables")
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = []

    for csv_path in sorted(labeled_dir.glob("features_*.csv")):
        threshold_name = csv_path.stem.replace("features_", "")
        df = pd.read_csv(csv_path)

        result = compute_separability(df)
        result["threshold_setting"] = threshold_name
        rows.append(result)

        print(threshold_name, result)

    out = pd.DataFrame(rows)
    out.to_csv(output_dir / "separability_results.csv", index=False)


if __name__ == "__main__":
    main()
```

---

# 17. Code bổ sung: boundary score

Tạo file:

```text
src/08_boundary_score.py
```

```python
from pathlib import Path
import pandas as pd
import numpy as np


def minmax(series, higher_is_better=True):
    s = series.astype(float)
    if s.max() == s.min():
        return pd.Series([1.0] * len(s), index=s.index)

    norm = (s - s.min()) / (s.max() - s.min())

    if not higher_is_better:
        norm = 1.0 - norm

    return norm


def main():
    table_dir = Path("results/tables")

    cls = pd.read_csv(table_dir / "classification_results.csv")

    # Average across classifiers for each threshold
    cls_summary = cls.groupby("threshold_setting").agg({
        "accuracy": "mean",
        "macro_f1": "mean",
        "f1_healthy": "mean",
        "f1_degrading": "mean",
        "f1_fault": "mean"
    }).reset_index()

    # Optional: add separability if available
    sep_path = table_dir / "separability_results.csv"
    if sep_path.exists():
        sep = pd.read_csv(sep_path)
        merged = cls_summary.merge(sep, on="threshold_setting", how="left")
    else:
        merged = cls_summary

    # Base score for conference paper
    merged["boundary_score"] = (
        0.4 * merged["macro_f1"]
        + 0.4 * merged["f1_degrading"]
        + 0.2 * merged["f1_fault"]
    )

    # Optional separability-aware score
    if "silhouette" in merged.columns:
        merged["silhouette_norm"] = minmax(merged["silhouette"], higher_is_better=True)
        merged["db_norm"] = minmax(merged["davies_bouldin"], higher_is_better=False)

        merged["boundary_score_with_sep"] = (
            0.30 * merged["macro_f1"]
            + 0.30 * merged["f1_degrading"]
            + 0.20 * merged["f1_fault"]
            + 0.10 * merged["silhouette_norm"]
            + 0.10 * merged["db_norm"]
        )

    merged = merged.sort_values("boundary_score", ascending=False)
    merged["rank"] = range(1, len(merged) + 1)

    output_path = table_dir / "boundary_score_results.csv"
    merged.to_csv(output_path, index=False)

    print(merged)
    print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()
```

---

# 18. Update thứ tự chạy pipeline

```bash
python src/01_prepare_metadata.py
python src/02_extract_features.py
python src/03_build_health_index.py
python src/04_change_point_detection.py
python src/05_generate_stage_labels.py
python src/06_separability_analysis.py
python src/07_train_classifiers.py
python src/08_boundary_score.py
python src/09_plot_results.py
```

---

# 19. Figure cần có để bài mạnh hơn

## Figure 1 — Research framework

```text
Feature extraction → HI construction → CPD → Candidate labels → Separability + Classification → Boundary recommendation
```

## Figure 2 — Health Indicator trajectory

Vẽ 3 đường:

```text
HI-V
HI-T
HI-VT
```

Kèm vertical lines:

```text
0.60
0.90
detected cp1
detected cp2
```

## Figure 3 — Change-point comparison

Bar/table plot:

```text
method vs cp1/cp2
```

## Figure 4 — Threshold sensitivity

Vẽ:

```text
Macro-F1
F1 Degrading
Boundary Score
```

theo:

```text
T1, T2, T3, T4, T5, TD
```

## Figure 5 — Confusion matrix comparison

So sánh:

```text
T3 vs TD
```

hoặc:

```text
T3 vs worst threshold
```

---

# 20. Bảng cần có trong paper

## Table 1 — Related work positioning

| Study group | Main focus | Limitation relative to this study |
|---|---|---|
| Health indicator construction | Build degradation index | Often not evaluate fixed TTF label sensitivity |
| Change-point RUL | Detect degradation point for RUL | Focus on RUL rather than 3-class classification labels |
| Stage-based RUL | Divide life into stages for RUL | Does not directly validate Healthy/Degrading/Fault thresholds |
| GMM/stage division | Cluster degradation stages | Often vibration-only or no downstream classification robustness |
| This study | Validate TTF boundaries using vibration–temperature HI + CPD + classification | Focused and practical for stage-label reliability |

## Table 2 — Candidate threshold settings

| Setting | Healthy | Degrading | Fault |
|---|---|---|---|
| T1 | [0, 0.50) | [0.50, 0.85) | [0.85, 1.00] |
| T2 | [0, 0.55) | [0.55, 0.90) | [0.90, 1.00] |
| T3 | [0, 0.60) | [0.60, 0.90) | [0.90, 1.00] |
| T4 | [0, 0.65) | [0.65, 0.90) | [0.90, 1.00] |
| T5 | [0, 0.70) | [0.70, 0.95) | [0.95, 1.00] |
| TD | [0, cp1) | [cp1, cp2) | [cp2, 1.00] |

## Table 3 — Change-point results

| HI variant | Method | cp1 | cp2 | Distance to 60/90 |
|---|---|---:|---:|---:|
| HI-V | Binary |  |  |  |
| HI-T | Binary |  |  |  |
| HI-VT | Binary |  |  |  |
| HI-VT | PELT |  |  |  |

## Table 4 — Separability results

| Threshold | Silhouette | Davies-Bouldin | Calinski-Harabasz |
|---|---:|---:|---:|
| T1 |  |  |  |
| T2 |  |  |  |
| T3 |  |  |  |
| TD |  |  |  |

## Table 5 — Classification robustness

| Threshold | Accuracy | Macro-F1 | F1 Healthy | F1 Degrading | F1 Fault | Boundary Score |
|---|---:|---:|---:|---:|---:|---:|
| T1 |  |  |  |  |  |  |
| T2 |  |  |  |  |  |  |
| T3 |  |  |  |  |  |  |
| TD |  |  |  |  |  |  |

---

# 21. Cách viết kết quả theo từng trường hợp

## Trường hợp 1 — 60/90 được ủng hộ

Nếu change-point gần 0.60 và 0.90, và T3 có score tốt:

```text
The detected transition regions are broadly consistent with the 60/90 TTF thresholds. In addition, the 60/90 setting achieves competitive or superior Macro-F1 and Degrading F1 among candidate boundaries. These findings suggest that the selected thresholds are not purely arbitrary but are supported by both signal-level transitions and downstream classification robustness.
```

## Trường hợp 2 — Data-driven threshold tốt hơn 60/90

Nếu TD tốt hơn:

```text
Although the 60/90 setting provides an interpretable baseline, the data-driven boundary derived from change-point detection achieves better class separability and classification robustness. This indicates that fixed TTF thresholds may introduce label noise and should be validated before training downstream health classification models.
```

## Trường hợp 3 — Kết quả không rõ ràng

Nếu các threshold tương đương nhau:

```text
The candidate threshold settings produce comparable classification performance, suggesting that the dataset contains gradual rather than abrupt transitions. In this case, the boundary should be interpreted as a transition region rather than a sharp point. This supports the need for transition-focused evaluation and soft-label or sequence-aware classification in future work.
```

---

# 22. Abstract tối ưu

```text
Stage labeling is a critical yet often under-examined step in run-to-failure bearing health classification. Fixed time-to-failure thresholds are commonly used to define Healthy, Degrading, and Fault stages, but such boundaries may be arbitrary and can affect downstream classification results. This paper proposes a data-driven validation framework for assessing TTF-based stage boundaries using vibration–temperature health indicators. Time-domain, frequency-domain, and temperature trend descriptors are extracted to construct vibration-only, temperature-only, and multi-modal health indicators. Multiple change-point detection methods are then applied to identify potential transition regions. To evaluate whether candidate boundaries are useful for classification, we compare several TTF threshold settings using feature separability metrics and downstream machine learning classifiers. The framework provides a practical way to determine whether fixed stage boundaries, such as the 60/90 TTF split, are supported by signal-level transitions and classification robustness. The study contributes a transparent stage-boundary validation procedure that can improve the reliability of subsequent bearing health classification and sequence-aware degradation modeling.
```

---

# 23. Introduction skeleton

## Paragraph 1 — Problem

```text
Rolling bearing health monitoring is a key task in condition-based maintenance. In run-to-failure settings, the machine state evolves gradually from normal operation to degradation and eventually fault. Therefore, three-stage health classification, such as Healthy, Degrading, and Fault, provides a practical abstraction for maintenance decision-making.
```

## Paragraph 2 — Labeling problem

```text
A major challenge is that many run-to-failure datasets do not provide explicit stage labels. Researchers often define stages using fixed lifetime or TTF thresholds. However, if these thresholds are selected without data-driven validation, the resulting labels may introduce noise and bias into downstream classifiers.
```

## Paragraph 3 — Prior work

```text
Prior studies have investigated health indicator construction, change-point detection, and stage-based RUL prediction. These studies show that degradation processes are multi-stage and that transition points can be estimated from condition-monitoring signals. However, fewer studies examine how fixed TTF thresholds affect three-stage classification robustness, especially when both vibration and temperature information are available.
```

## Paragraph 4 — This study

```text
This paper proposes a data-driven framework for validating TTF-based stage boundaries in bearing health classification. The framework constructs vibration-only, temperature-only, and vibration–temperature health indicators, applies change-point detection to identify transition regions, and compares candidate threshold settings using separability metrics and downstream classification performance.
```

---

# 24. Related Work section outline

## 2.1. Bearing health indicators

Nội dung:

- HI là trung tâm của PHM/RUL.
- Feature vibration như RMS, kurtosis, spectral energy phổ biến.
- Gần đây có nhiều HI tự học hoặc multi-feature fusion.

## 2.2. Change-point and degradation point detection

Nội dung:

- Change-point dùng để xác định điểm bắt đầu suy giảm.
- Nhiều bài dùng CPD để hỗ trợ RUL.
- Gap: ít bài dùng CPD để validate stage labels cho classification.

## 2.3. Stage-based bearing prognosis

Nội dung:

- Một số bài chia degradation thành nhiều stage để dự đoán RUL.
- Có GMM, deep learning, graph model, stochastic process.
- Gap: stage division thường phục vụ RUL; ít đánh giá threshold sensitivity cho 3-class classification.

## 2.4. Position of this study

Nội dung:

```text
This work is positioned before model training: it examines whether the stage labels themselves are data-supported.
```

---

# 25. Discussion points để bài không bị yếu

## 25.1. Không chứng minh threshold là tuyệt đối

Viết rõ:

```text
The proposed framework does not claim that a single universal threshold exists for all bearings or datasets.
```

## 25.2. Boundary là transition region

Do degradation gradual, nên nói:

```text
Healthy–Degrading and Degrading–Fault boundaries should be interpreted as transition regions rather than exact physical points.
```

## 25.3. Single-run limitation

Nếu dataset chỉ một run:

```text
The main limitation is the use of a single run-to-failure trajectory. Therefore, the results should be interpreted as dataset-specific boundary validation rather than universal threshold discovery.
```

## 25.4. Vì sao vẫn có giá trị

```text
Even under a single-run setting, the framework is useful because it exposes the sensitivity of classification results to label construction and provides a transparent procedure for selecting or justifying stage boundaries.
```

---

# 26. References gợi ý để đọc và trích dẫn

> Lưu ý: cần kiểm tra lại BibTeX/DOI chính xác trước khi đưa vào bản nộp.

## Directly related

1. **Stage-Based Remaining Useful Life Prediction for Bearings**  
   Machines, 2025.  
   Liên quan: stage-based RUL, feature extraction, bearing degradation stage.

2. **Rolling bearing degradation stage division and remaining useful life prediction using RESFA and Bi-LSTM**  
   Reliability Engineering & System Safety, 2025.  
   Liên quan: health state classification, degradation starting point, stage division, RUL.

3. **An adaptive prediction approach for rolling bearing remaining useful life based on stochastic process model**  
   Reliability Engineering & System Safety, 2022.  
   Liên quan: degradation trend divided into multiple stages.

4. **A Change Point Detection Integrated Remaining Useful Life Estimation Model**  
   arXiv, 2024.  
   Liên quan: detected change points inform degradation data labeling for LSTM-based RUL.

5. **A Novel Bearing Remaining Useful Life Prediction Methodology with Slope-Based Change Point Detection and WOA-Attention-BiLSTM Model**  
   2025.  
   Liên quan: health indicator construction, slope-based change point detection, RUL.

6. **An Integrated Approach for Bearing Health Indicator and Stage Division Using Improved Gaussian Mixture Model and Confidence Value**  
   Liên quan: health indicator and stage division using improved GMM.

7. **An Outlier Cleaning Based Adaptive Recognition Method for the Degradation Stage of Rolling Bearings**  
   2022.  
   Liên quan: degradation stage recognition, adaptive recognition.

## Background references

8. **Prognostics and Health Management: A Review of Vibration Based Bearing and Gear Health Indicators**  
   IEEE Access, 2017.  
   Liên quan: review về vibration-based HI.

9. **Applications of machine learning to machine fault diagnosis: A review and roadmap**  
   Mechanical Systems and Signal Processing, 2020.  
   Liên quan: fault diagnosis roadmap.

10. **Deep learning and its applications to machine health monitoring**  
   Mechanical Systems and Signal Processing, 2019.  
   Liên quan: deep learning for machine health monitoring.

---

# 27. Final recommended conference paper framing

## Core message

```text
Stage labels are not just preprocessing; they directly affect the validity of bearing health classification. Therefore, before training complex models, stage boundaries should be validated using signal-level evidence and downstream classification behavior.
```

## Final contribution sentence

```text
This study contributes a practical stage-boundary validation framework that combines vibration–temperature health indicators, change-point detection, separability analysis, and classification robustness to assess whether fixed TTF-based Healthy–Degrading–Fault labels are data-supported.
```

## Best conference scope

Phù hợp với:

```text
AIoT
Industrial AI
Predictive Maintenance
Applied Machine Learning
Condition Monitoring
PHM
Smart Manufacturing
```

---

# 28. Checklist cập nhật code

Cần cập nhật file code theo checklist:

```text
[ ] Thêm HI variants: HI-V, HI-T, HI-VT
[ ] Thêm change-point result cho từng HI variant
[ ] Thêm data-driven threshold TD từ median cp1/cp2
[ ] Thêm separability_analysis.py
[ ] Thêm boundary_score.py
[ ] Thêm plot HI-V/HI-T/HI-VT
[ ] Thêm plot boundary score theo threshold
[ ] Thêm related_work_matrix.md
[ ] Thêm result_tables.md
```

---

# 29. Output cuối cùng cần có

```text
results/tables/features.csv
results/tables/health_index_variants.csv
results/tables/change_point_results.csv
results/tables/separability_results.csv
results/tables/classification_results.csv
results/tables/boundary_score_results.csv

results/figures/hi_trajectory_variants.png
results/figures/change_point_comparison.png
results/figures/threshold_sensitivity.png
results/figures/boundary_score_ranking.png
results/figures/confusion_matrix_T3_vs_TD.png
```

---

# 30. Kết luận

Hướng tối ưu không phải là “chứng minh 60/90 luôn đúng”, mà là:

```text
Đề xuất framework kiểm chứng stage boundary.
```

Nếu 60/90 tốt:

```text
60/90 được hỗ trợ bởi dữ liệu.
```

Nếu data-driven threshold tốt hơn:

```text
Bài vẫn có contribution vì chỉ ra fixed threshold cần được validate.
```

Nếu các threshold gần tương đương:

```text
Bài vẫn có contribution vì chứng minh boundary là transition region, không phải điểm cắt cứng.
```

Như vậy, bài hội thảo sẽ có contribution rõ hơn, ít rủi ro hơn và dễ nối sang bài tiếp theo về CNN-Mamba + temperature fusion.
