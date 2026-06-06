# System Overview

## Research Topic

**Firefly-Optimized CNN-LSTM for Remaining Useful Life Prediction of Rolling Bearings**

---

# 1. Introduction

Rolling bearings are critical components widely used in rotating machinery such as motors, turbines, pumps, manufacturing equipment, and industrial automation systems. Bearing failures are among the most common causes of unexpected machine downtime and can result in significant maintenance costs, production interruptions, and safety risks.

To address these challenges, modern Prognostics and Health Management (PHM) systems aim to estimate the Remaining Useful Life (RUL) of equipment before failure occurs. Accurate RUL prediction enables maintenance activities to be scheduled proactively, thereby reducing operational costs and improving system reliability.

Recent advances in deep learning have demonstrated that hybrid architectures such as CNN-LSTM can effectively model bearing degradation processes from vibration signals. However, the performance of CNN-LSTM models heavily depends on the selection of hyperparameters, which are commonly determined through manual trial-and-error procedures.

To overcome this limitation, this research proposes a Firefly-Optimized CNN-LSTM framework that integrates the Firefly Algorithm with a CNN-LSTM architecture to automatically optimize critical hyperparameters and improve RUL prediction performance.

---

# 2. System Objective

The primary objective of the proposed system is to develop an intelligent prediction framework capable of estimating the Remaining Useful Life of rolling bearings based on vibration monitoring data.

Specifically, the system aims to:

* Automatically extract degradation features from raw vibration signals.
* Capture temporal degradation trends over time.
* Optimize CNN-LSTM hyperparameters using Firefly Algorithm.
* Generate accurate Remaining Useful Life predictions.
* Reduce prediction error compared with conventional CNN-LSTM models.
* Improve the robustness and generalization capability of predictive maintenance systems.

---

# 3. Proposed System Overview

The proposed framework consists of five major stages:

1. Data Acquisition
2. Data Preprocessing
3. Deep Feature Learning
4. Firefly-Based Hyperparameter Optimization
5. Remaining Useful Life Prediction and Evaluation

The overall workflow transforms raw bearing condition monitoring data into an estimated Remaining Useful Life value through a combination of deep learning and metaheuristic optimization techniques.

---

# 4. System Components

## 4.1 Data Acquisition Module

This module collects run-to-failure bearing datasets used for model training and evaluation.

### Input Datasets

The study focuses on benchmark bearing degradation datasets commonly used in PHM research:

* FEMTO-ST (PRONOSTIA) Dataset
* IMS Bearing Dataset

These datasets contain vibration measurements recorded from bearings operating under accelerated degradation conditions until failure occurs.

### Input Data

The collected data may include:

* Horizontal vibration signals
* Vertical vibration signals
* Bearing operating conditions
* Degradation trajectories
* Failure labels
* Remaining Useful Life targets

The acquired signals serve as the foundation for subsequent feature extraction and prediction tasks.

---

## 4.2 Data Preprocessing Module

Raw vibration signals typically contain noise, irrelevant fluctuations, and inconsistent scales.

Therefore, preprocessing is required before model training.

Typical preprocessing procedures include:

* Signal normalization
* Data cleaning
* Window segmentation
* Feature sequence generation
* Label generation for RUL prediction

The objective of this stage is to transform raw sensor measurements into structured inputs suitable for deep learning models.

---

## 4.3 CNN Feature Extraction Module

Convolutional Neural Networks (CNNs) are employed to automatically extract degradation-related features from vibration data.

CNN layers perform:

* Local feature extraction
* Pattern recognition
* Fault-related characteristic learning

Compared with traditional handcrafted feature engineering methods, CNNs can automatically learn informative degradation representations directly from data.

The output of this module is a high-level feature representation describing the bearing health condition.

---

## 4.4 LSTM Temporal Modeling Module

Bearing degradation is a time-dependent process.

To capture temporal relationships among degradation states, Long Short-Term Memory (LSTM) networks are employed after CNN feature extraction.

The LSTM module is responsible for:

* Learning degradation trends
* Modeling long-term temporal dependencies
* Capturing bearing health evolution over time
* Predicting future degradation behavior

By combining CNN and LSTM, the framework simultaneously exploits spatial feature extraction and temporal sequence learning capabilities.

---

## 4.5 Firefly Optimization Module

This module represents the core contribution of the proposed research.

Instead of relying on manually selected hyperparameters, Firefly Algorithm is utilized to automatically search for optimal CNN-LSTM configurations.

### Candidate Hyperparameters

The optimization process may include:

* Learning rate
* Number of CNN filters
* Kernel size
* Number of LSTM units
* Dropout rate
* Batch size
* Training epochs

Each Firefly individual represents a candidate hyperparameter configuration.

The optimization objective is to minimize prediction error on validation data.

Through iterative exploration and exploitation, Firefly Algorithm identifies parameter combinations that improve model performance.

---

## 4.6 RUL Prediction Module

Using the optimized CNN-LSTM architecture, the framework predicts the Remaining Useful Life of rolling bearings.

### Output

The system outputs:

* Predicted RUL value
* Predicted degradation trajectory
* Model performance indicators

These outputs can support predictive maintenance decision-making and maintenance scheduling.

---

## 4.7 Performance Evaluation Module

The final stage evaluates the effectiveness of the proposed Firefly-Optimized CNN-LSTM framework.

### Evaluation Metrics

Performance is assessed using:

* RMSE (Root Mean Squared Error)
* MAE (Mean Absolute Error)
* R² Score

### Baseline Models

The proposed model will be compared with:

* CNN
* LSTM
* CNN-LSTM
* Other reported benchmark methods from the literature

The purpose of this comparison is to quantify the benefits introduced by Firefly-based hyperparameter optimization.

---

# 5. Overall Workflow

The complete workflow of the proposed framework can be summarized as follows:

Benchmark Bearing Dataset
→ Data Preprocessing
→ CNN Feature Extraction
→ LSTM Temporal Modeling
→ Firefly Hyperparameter Optimization
→ Optimized CNN-LSTM Model
→ Remaining Useful Life Prediction
→ Performance Evaluation

This workflow establishes an end-to-end predictive maintenance framework capable of transforming raw vibration signals into accurate Remaining Useful Life estimates.

---

# 6. Expected Benefits

The proposed Firefly-Optimized CNN-LSTM framework is expected to provide several advantages:

* Improved prediction accuracy.
* Reduced prediction error.
* Automated hyperparameter optimization.
* Better convergence behavior.
* Reduced dependence on manual tuning.
* Enhanced robustness and generalization capability.
* Increased applicability in industrial predictive maintenance systems.

---

# 7. Summary

This study proposes a Firefly-Optimized CNN-LSTM framework for Remaining Useful Life prediction of rolling bearings. The framework combines CNN-based feature extraction, LSTM-based temporal modeling, and Firefly-based hyperparameter optimization to improve prediction performance. By integrating deep learning and swarm intelligence techniques, the proposed system aims to provide a more accurate, efficient, and robust solution for bearing prognostics and predictive maintenance applications.
