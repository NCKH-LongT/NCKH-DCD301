# Research Questions

## Research Topic

**Firefly-Optimized CNN-LSTM for Remaining Useful Life Prediction of Rolling Bearings**

---

# Main Research Question

How can Firefly Algorithm be integrated with a CNN-LSTM architecture to improve the accuracy, robustness, and efficiency of Remaining Useful Life prediction for rolling bearings?

---

# Sub Research Questions

## RQ1

How effectively can a CNN-LSTM architecture model bearing degradation patterns and predict Remaining Useful Life using vibration-based condition monitoring data?

### Motivation

CNN-LSTM has been widely adopted for RUL prediction because CNN can extract degradation features while LSTM can capture temporal dependencies. However, its performance depends heavily on network configuration and dataset characteristics.

---

## RQ2

Can Firefly Algorithm automatically identify optimal hyperparameter configurations for CNN-LSTM models more effectively than conventional manual tuning approaches?

### Motivation

Most existing studies rely on trial-and-error or empirical parameter selection. Automated optimization may reduce human effort and improve model performance.

---

## RQ3

To what extent does Firefly-based hyperparameter optimization improve prediction performance compared with a conventional CNN-LSTM model?

### Motivation

This question evaluates whether integrating Firefly Algorithm actually produces measurable benefits in predictive accuracy and model convergence.

### Evaluation Metrics

* RMSE (Root Mean Squared Error)
* MAE (Mean Absolute Error)
* R² Score
* Training Convergence Performance

---

## RQ4

Which CNN-LSTM hyperparameters have the greatest impact on Remaining Useful Life prediction performance?

### Motivation

Understanding the influence of individual hyperparameters provides practical insights for future PHM and predictive maintenance applications.

### Candidate Hyperparameters

* Learning Rate
* Number of CNN Filters
* Kernel Size
* Number of LSTM Units
* Batch Size
* Dropout Rate

---

## RQ5

How robust and generalizable is the proposed Firefly-Optimized CNN-LSTM framework when evaluated on benchmark bearing degradation datasets?

### Motivation

A practical predictive maintenance model should maintain stable performance across different operating conditions and degradation patterns.

### Benchmark Datasets

* FEMTO-ST (PRONOSTIA)
* IMS Bearing Dataset

---

# Research Objectives

Based on the proposed research questions, this study aims to achieve the following objectives.

## RO1

Develop a CNN-LSTM-based framework for Remaining Useful Life prediction of rolling bearings.

## RO2

Design a Firefly Algorithm optimization mechanism for automatic CNN-LSTM hyperparameter tuning.

## RO3

Evaluate the effectiveness of Firefly-based optimization in improving prediction accuracy and reducing prediction error.

## RO4

Analyze the influence of critical hyperparameters on model performance.

## RO5

Validate the proposed framework using benchmark bearing degradation datasets and compare results against baseline CNN-LSTM models.

---

# Expected Research Contributions

The proposed study is expected to contribute in three aspects.

### Theoretical Contribution

Provide a systematic investigation of Firefly-based hyperparameter optimization for deep learning-based prognostics.

### Methodological Contribution

Develop a Firefly-Optimized CNN-LSTM framework for automated Remaining Useful Life prediction.

### Practical Contribution

Support predictive maintenance applications by providing a more accurate and robust bearing health monitoring solution.

---

# Relationship Between Research Gap and Research Questions

| Identified Research Gap                      | Research Question |
| -------------------------------------------- | ----------------- |
| CNN-LSTM remains a strong RUL architecture   | RQ1               |
| Hyperparameters are often manually selected  | RQ2               |
| Limited evaluation of optimization benefits  | RQ3               |
| Lack of understanding of parameter influence | RQ4               |
| Limited validation across benchmark datasets | RQ5               |

---

# Summary

The proposed research questions investigate the feasibility and effectiveness of integrating Firefly Algorithm with CNN-LSTM for rolling bearing Remaining Useful Life prediction. The questions are designed to address the major gaps identified in the literature and provide a structured foundation for the proposed methodology and experimental evaluation.
