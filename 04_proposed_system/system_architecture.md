# System Architecture

## Research Topic

**Firefly-Optimized CNN-LSTM for Remaining Useful Life Prediction of Rolling Bearings**

---

# 1. Architecture Overview

The proposed system is an end-to-end predictive maintenance framework designed to estimate the Remaining Useful Life (RUL) of rolling bearings using vibration monitoring data.

The framework integrates three key technologies:

* Convolutional Neural Network (CNN)
* Long Short-Term Memory (LSTM)
* Firefly Algorithm (FA)

CNN is responsible for automatic feature extraction from vibration signals, LSTM captures temporal degradation patterns, and Firefly Algorithm automatically optimizes the hyperparameters of the CNN-LSTM model.

The overall objective is to improve prediction accuracy, reduce prediction error, and eliminate the limitations of manual hyperparameter tuning.

---

# 2. Overall System Architecture

```text
+------------------------------------------------+
|         FEMTO-ST / IMS Bearing Dataset          |
+------------------------+-----------------------+
                         |
                         v
+------------------------------------------------+
|             Data Preprocessing Module          |
|------------------------------------------------|
| - Data Cleaning                                |
| - Normalization                                |
| - Sliding Window Segmentation                  |
| - RUL Label Generation                         |
+------------------------+-----------------------+
                         |
                         v
+------------------------------------------------+
|          CNN Feature Extraction Module         |
|------------------------------------------------|
| - Local Pattern Learning                       |
| - Automatic Feature Extraction                 |
| - Health Indicator Representation              |
+------------------------+-----------------------+
                         |
                         v
+------------------------------------------------+
|          LSTM Temporal Modeling Module         |
|------------------------------------------------|
| - Sequential Learning                          |
| - Long-Term Dependency Modeling                |
| - Degradation Trend Learning                   |
+------------------------+-----------------------+
                         |
                         v
+------------------------------------------------+
|           RUL Prediction Output Layer          |
+------------------------+-----------------------+
                         |
                         v
+------------------------------------------------+
|          Performance Evaluation Module         |
|------------------------------------------------|
| RMSE | MAE | R²                                |
+------------------------------------------------+

                         ^
                         |
+------------------------------------------------+
|       Firefly Hyperparameter Optimization      |
|------------------------------------------------|
| - Learning Rate                                |
| - Number of CNN Filters                        |
| - Kernel Size                                  |
| - LSTM Units                                   |
| - Dropout Rate                                 |
| - Batch Size                                   |
+------------------------------------------------+
```

---

# 3. Main System Components

## 3.1 Dataset Layer

The first layer of the architecture consists of benchmark bearing degradation datasets used for model training and evaluation.

### Candidate Datasets

* FEMTO-ST (PRONOSTIA)
* IMS Bearing Dataset

These datasets provide run-to-failure vibration signals collected under controlled operating conditions.

### Purpose

* Provide degradation trajectories.
* Generate Remaining Useful Life labels.
* Support model training and validation.

---

## 3.2 Data Preprocessing Module

Raw vibration signals cannot be directly used for deep learning because they contain noise and inconsistent scales.

### Functions

* Signal normalization.
* Noise reduction.
* Data segmentation using sliding windows.
* Construction of time-series sequences.
* Generation of RUL target labels.

### Output

Structured input sequences suitable for CNN-LSTM training.

---

## 3.3 CNN Feature Extraction Module

This module performs automatic feature extraction from vibration signals.

### Purpose

Traditional feature engineering requires expert knowledge and handcrafted indicators.

CNN automatically learns degradation-related representations directly from raw sensor data.

### Functions

* Detect local degradation patterns.
* Learn fault-related characteristics.
* Generate high-level feature representations.

### Output

Feature vectors representing bearing health conditions.

---

## 3.4 LSTM Temporal Modeling Module

Bearing degradation evolves gradually over time.

Therefore, temporal information must be incorporated into the prediction process.

### Functions

* Capture sequential degradation behavior.
* Learn long-term temporal dependencies.
* Model health evolution trends.

### Output

Temporal degradation representations used for RUL prediction.

---

## 3.5 Firefly Optimization Module

The Firefly Optimization Module is the core innovation of this study.

Instead of manually selecting model hyperparameters, Firefly Algorithm automatically searches for the optimal configuration.

### Optimization Variables

The Firefly Algorithm may optimize:

| Hyperparameter | Description                   |
| -------------- | ----------------------------- |
| Learning Rate  | Training step size            |
| CNN Filters    | Number of convolution kernels |
| Kernel Size    | CNN receptive field           |
| LSTM Units     | Number of memory cells        |
| Dropout Rate   | Regularization parameter      |
| Batch Size     | Training batch size           |

### Optimization Objective

Minimize prediction error on validation data.

### Expected Benefits

* Faster convergence.
* Reduced manual tuning effort.
* Improved model stability.
* Enhanced prediction accuracy.

---

## 3.6 RUL Prediction Module

After optimization, the CNN-LSTM model generates Remaining Useful Life estimates.

### Input

Temporal degradation features from the LSTM layer.

### Output

Predicted Remaining Useful Life value.

The predicted value represents the estimated time remaining before bearing failure.

---

## 3.7 Evaluation Module

The final module evaluates the effectiveness of the proposed framework.

### Evaluation Metrics

| Metric | Purpose                            |
| ------ | ---------------------------------- |
| RMSE   | Measure prediction error magnitude |
| MAE    | Measure average absolute error     |
| R²     | Measure goodness of fit            |

### Baseline Models

The proposed Firefly-CNN-LSTM model will be compared against:

* CNN
* LSTM
* CNN-LSTM
* Existing benchmark methods reported in literature

---

# 4. Data Flow Description

The proposed framework follows the workflow below:

1. Bearing vibration signals are collected from benchmark datasets.
2. Raw signals are preprocessed and segmented into sequences.
3. CNN extracts degradation-related features.
4. LSTM learns temporal degradation patterns.
5. Firefly Algorithm searches for optimal hyperparameters.
6. The optimized CNN-LSTM model predicts Remaining Useful Life.
7. Prediction performance is evaluated using RMSE, MAE, and R².

This workflow forms a complete end-to-end predictive maintenance framework.

---

# 5. Relationship with Research Gap

The literature review identified that most existing CNN-LSTM-based RUL prediction studies rely on manually selected hyperparameters.

Although many studies have demonstrated the effectiveness of metaheuristic optimization algorithms, the application of Firefly Algorithm to optimize CNN-LSTM models for rolling bearing RUL prediction remains limited.

To address this gap, the proposed architecture integrates Firefly Algorithm directly into the model optimization process, enabling automated hyperparameter tuning and potentially improving prediction performance.

---

# 6. Expected Contribution

The proposed architecture is expected to contribute in three aspects:

1. Develop an end-to-end framework for bearing RUL prediction.
2. Integrate Firefly Algorithm with CNN-LSTM for automated hyperparameter optimization.
3. Improve prediction accuracy and robustness compared with conventional CNN-LSTM approaches.

---

# 7. Summary

The proposed system architecture combines benchmark bearing datasets, deep learning-based feature extraction, temporal sequence modeling, and Firefly-based hyperparameter optimization within a unified framework. By integrating CNN, LSTM, and Firefly Algorithm, the system aims to provide a more accurate and efficient solution for Remaining Useful Life prediction of rolling bearings in predictive maintenance applications.
