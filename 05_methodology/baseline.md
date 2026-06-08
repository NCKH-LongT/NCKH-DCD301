# Baseline Models

## 1. Overview

This document describes the baseline models used to evaluate the effectiveness of the proposed Firefly-Optimized CNN-LSTM framework for Remaining Useful Life (RUL) prediction of rolling bearings.

A baseline model serves as a reference for comparison, allowing the performance improvement achieved by the proposed model to be objectively measured.

The proposed Firefly-CNN-LSTM model will be compared with several widely used deep learning architectures and representative approaches reported in the literature.

---

# 2. Purpose of Baseline Comparison

The baseline comparison aims to answer the following research question:

**Does Firefly-based hyperparameter optimization improve the prediction performance of CNN-LSTM models for bearing Remaining Useful Life estimation?**

To answer this question, the proposed model will be evaluated against simpler and widely accepted benchmark models.

---

# 3. Baseline 1: CNN

## Description

Convolutional Neural Network (CNN) is a deep learning architecture capable of automatically extracting degradation-related features from vibration signals.

CNN has been widely used in bearing fault diagnosis and prognostics because of its strong feature extraction capability.

## Strengths

* Automatic feature extraction.
* Effective for vibration signal analysis.
* Relatively simple architecture.

## Limitations

* Cannot effectively model long-term temporal dependencies.
* Limited ability to learn degradation evolution over time.

## Purpose of Comparison

This baseline is used to evaluate the contribution of temporal learning provided by LSTM.

---

# 4. Baseline 2: LSTM

## Description

Long Short-Term Memory (LSTM) is a recurrent neural network designed for sequential and time-series learning.

LSTM can learn degradation trends from historical observations and capture long-term dependencies.

## Strengths

* Excellent temporal modeling capability.
* Effective for degradation trend learning.

## Limitations

* Does not perform automatic spatial feature extraction.
* Sensitive to input feature quality.

## Purpose of Comparison

This baseline evaluates the importance of CNN-based feature extraction.

---

# 5. Baseline 3: CNN-LSTM

## Description

CNN-LSTM combines convolutional feature extraction with temporal sequence learning.

CNN extracts degradation features from vibration signals, while LSTM models degradation evolution over time.

This architecture is one of the most widely adopted approaches for bearing RUL prediction.

## Strengths

* Simultaneous spatial and temporal learning.
* Strong predictive capability.
* Widely validated in previous studies.

## Limitations

* Hyperparameters are usually selected manually.
* Performance depends heavily on parameter tuning.

## Purpose of Comparison

CNN-LSTM serves as the primary baseline because it represents the foundation of the proposed model.

The proposed Firefly-CNN-LSTM model is an extension of CNN-LSTM with automated hyperparameter optimization.

---

# 6. Baseline 4: Metaheuristic-Optimized CNN-LSTM

## Description

Several recent studies have improved CNN-LSTM performance through metaheuristic optimization algorithms.

Examples include:

* Particle Swarm Optimization (PSO)
* Genetic Algorithm (GA)
* Sparrow Search Algorithm (SSA)
* Artificial Gorilla Troop Optimization (GTO)
* Whale Optimization Algorithm (WOA)

## Strengths

* Automated hyperparameter optimization.
* Improved convergence performance.

## Limitations

* Optimization effectiveness varies across problems.
* May converge prematurely to local optima.

## Purpose of Comparison

This baseline evaluates whether Firefly Algorithm can outperform or compete with other optimization strategies.

---

# 7. Proposed Model: Firefly-CNN-LSTM

## Description

The proposed model integrates Firefly Algorithm with CNN-LSTM to automatically search for optimal hyperparameter configurations.

The optimization process focuses on:

* Learning Rate
* Number of CNN Filters
* Kernel Size
* Number of LSTM Units
* Dropout Rate
* Batch Size

The optimized CNN-LSTM model is expected to achieve better predictive performance and more stable convergence.

---

# 8. Comparison Metrics

The proposed model and all baseline models will be evaluated using the same performance metrics:

| Metric                | Description                  |
| --------------------- | ---------------------------- |
| RMSE                  | Root Mean Square Error       |
| MAE                   | Mean Absolute Error          |
| R²                    | Coefficient of Determination |
| Training Time         | Computational Cost           |
| Convergence Stability | Optimization Stability       |

---

# 9. Expected Outcome

Based on findings from previous studies, the proposed Firefly-CNN-LSTM framework is expected to:

* Achieve lower RMSE than CNN, LSTM, and standard CNN-LSTM.
* Reduce prediction error measured by MAE.
* Improve goodness-of-fit measured by R².
* Provide better hyperparameter configurations automatically.
* Enhance convergence stability during training.

---

# 10. Summary

Four baseline categories are selected for experimental comparison:

| Category       | Model                            |
| -------------- | -------------------------------- |
| Baseline 1     | CNN                              |
| Baseline 2     | LSTM                             |
| Baseline 3     | CNN-LSTM                         |
| Baseline 4     | Metaheuristic-Optimized CNN-LSTM |
| Proposed Model | Firefly-CNN-LSTM                 |

These baselines provide a comprehensive benchmark for evaluating the effectiveness of the proposed Firefly-based hyperparameter optimization strategy for Remaining Useful Life prediction of rolling bearings.
