# Evaluation Metrics

## 1. Introduction

The primary objective of this study is to evaluate the effectiveness of the proposed Firefly-Optimized CNN-LSTM framework for Remaining Useful Life (RUL) prediction of rolling bearings.

Since RUL prediction is a regression problem, appropriate evaluation metrics are required to accurately measure prediction errors and assess the overall performance of the proposed model. Furthermore, because the main contribution of this research lies in the integration of the Firefly Algorithm for hyperparameter optimization, additional metrics are necessary to evaluate optimization effectiveness and computational efficiency.

To provide a comprehensive assessment, the evaluation framework is divided into three categories:

1. Prediction Performance Metrics
2. Optimization Performance Metrics
3. Computational Performance Metrics

This multi-dimensional evaluation strategy enables objective comparison between baseline models and the proposed Firefly-Optimized CNN-LSTM framework.

---

# 2. Prediction Performance Metrics

Prediction performance metrics are used to evaluate how accurately the model estimates the Remaining Useful Life of rolling bearings.

## 2.1 Mean Absolute Error (MAE)

Mean Absolute Error measures the average absolute difference between predicted and actual RUL values.

### Purpose

MAE provides a direct and interpretable measure of prediction accuracy.

### Interpretation

* Lower MAE indicates better prediction performance.
* MAE represents the average prediction error in the same unit as the target variable.

### Advantages

* Easy to understand and interpret.
* Less sensitive to extreme outliers.

---

## 2.2 Mean Squared Error (MSE)

Mean Squared Error measures the average squared difference between predicted and actual values.

### Purpose

MSE penalizes larger prediction errors more heavily than smaller errors.

### Interpretation

* Lower MSE indicates better performance.
* Large prediction errors have a greater impact on the metric.

### Advantages

* Commonly used during model training and optimization.
* Useful for detecting significant prediction deviations.

---

## 2.3 Root Mean Squared Error (RMSE)

Root Mean Squared Error is the square root of MSE and is one of the most widely used evaluation metrics in prognostics and health management research.

### Purpose

RMSE measures the overall magnitude of prediction errors.

### Interpretation

* Lower RMSE indicates higher prediction accuracy.
* RMSE strongly penalizes large prediction errors.

### Importance in This Study

RMSE is selected as the primary evaluation metric and optimization objective.

The Firefly Algorithm uses RMSE as the fitness function during hyperparameter optimization. Therefore, minimizing RMSE directly corresponds to improving model performance.

---

## 2.4 Coefficient of Determination (R² Score)

The coefficient of determination evaluates how well the predicted values explain the variability of the actual RUL values.

### Purpose

R² measures the goodness-of-fit of the prediction model.

### Interpretation

* R² = 1 indicates perfect prediction.
* R² = 0 indicates no explanatory capability.
* Higher R² values indicate better predictive performance.

### Advantages

* Provides an overall measure of model effectiveness.
* Widely used for benchmarking regression models.

---

## 2.5 Improvement Rate

Improvement Rate quantifies the performance gain achieved by the proposed Firefly-Optimized CNN-LSTM model compared with baseline approaches.

### Purpose

To directly measure the contribution of Firefly-based hyperparameter optimization.

### Interpretation

* Higher Improvement Rate indicates greater effectiveness of the optimization process.
* Positive values indicate performance improvement over baseline models.

### Application in This Study

Improvement Rate will be calculated based on the reduction in RMSE achieved by the proposed model relative to the conventional CNN-LSTM model.

### Importance

Because the central contribution of this research is the integration of the Firefly Algorithm, Improvement Rate serves as a key indicator for validating the effectiveness of the proposed optimization strategy.

---

# 3. Optimization Performance Metrics

In addition to prediction accuracy, the optimization capability of the Firefly Algorithm must also be evaluated.

## 3.1 Best Fitness Value

Best Fitness Value represents the minimum RMSE achieved during the optimization process.

### Purpose

Measures the quality of the best solution discovered by the Firefly Algorithm.

### Interpretation

* Lower fitness value indicates a better hyperparameter configuration.
* Demonstrates optimization effectiveness.

---

## 3.2 Convergence Rate

Convergence Rate measures how quickly the Firefly Algorithm reaches a stable solution.

### Purpose

Evaluates optimization efficiency.

### Interpretation

* Faster convergence indicates more efficient optimization.
* Helps compare Firefly with alternative optimization methods.

---

## 3.3 Optimization Stability

Optimization Stability evaluates the consistency of optimization results across different executions.

### Purpose

Measures robustness of the optimization process.

### Interpretation

* Smaller performance variation indicates higher stability.
* Large fluctuations may indicate sensitivity to initialization.

---

## 3.4 Statistical Stability Analysis

Metaheuristic optimization algorithms are inherently stochastic and may generate different results across independent runs.

### Purpose

To assess repeatability and robustness of the proposed Firefly-based optimization framework.

### Method

The proposed model will be executed multiple independent runs using different random initializations.

The following statistics will be reported:

* Mean RMSE
* Standard Deviation of RMSE
* Best RMSE
* Worst RMSE

### Interpretation

* Lower standard deviation indicates greater stability.
* Consistent performance across runs demonstrates robustness.

### Importance

This analysis helps verify that performance improvements are attributable to the optimization mechanism rather than random chance.

---

# 4. Computational Performance Metrics

Computational metrics evaluate the practical feasibility of deploying the proposed framework.

## 4.1 Training Time

Training Time represents the total duration required to train the CNN-LSTM model.

### Purpose

Measures computational cost.

### Importance

Although optimization may improve prediction accuracy, excessive training time can reduce practical applicability.

---

## 4.2 Optimization Time

Optimization Time measures the duration required for the Firefly Algorithm to identify optimal hyperparameter configurations.

### Purpose

Evaluates the computational overhead introduced by the optimization process.

### Interpretation

* Shorter optimization time is preferable.
* Must be balanced against prediction performance improvements.

---

## 4.3 Inference Time

Inference Time measures the time required to generate a single RUL prediction after model training.

### Purpose

Evaluates suitability for real-time predictive maintenance applications.

### Importance

Low inference latency is desirable in industrial monitoring environments.

---

# 5. Comparative Evaluation Strategy

To demonstrate the effectiveness of the proposed framework, the Firefly-Optimized CNN-LSTM model will be compared against several baseline models.

## Baseline Models

1. CNN
2. LSTM
3. CNN-LSTM
4. Firefly-Optimized CNN-LSTM

## Comparison Criteria

The comparison will focus on:

* MAE
* RMSE
* R² Score
* Improvement Rate
* Training Time
* Optimization Time
* Optimization Stability

This comparative analysis enables objective assessment of both predictive performance and optimization effectiveness.

---

# 6. Benchmarking Strategy

Several experiments will be conducted to validate the proposed framework.

## Experiment 1: Individual Deep Learning Models

Models:

* CNN
* LSTM

### Objective

To establish baseline performance for feature extraction and temporal learning individually.

---

## Experiment 2: Hybrid Deep Learning Model

Model:

* CNN-LSTM

### Objective

To evaluate the effectiveness of combining convolutional feature extraction with temporal sequence learning.

---

## Experiment 3: Proposed Firefly-Optimized CNN-LSTM

Model:

* Firefly-CNN-LSTM

### Objective

To evaluate the effectiveness of Firefly-based hyperparameter optimization.

---

## Evaluation Goals

The benchmarking experiments aim to determine:

1. Whether CNN-LSTM outperforms standalone CNN and LSTM models.
2. Whether Firefly optimization improves CNN-LSTM performance.
3. The magnitude of performance improvement achieved through automatic hyperparameter tuning.
4. The stability and robustness of the proposed optimization framework.

These objectives directly address the research questions and validate the proposed research hypothesis.

---

# 7. Expected Evaluation Outcomes

Based on findings reported in existing literature, the proposed Firefly-CNN-LSTM framework is expected to achieve:

* Lower MAE than baseline models.
* Lower RMSE than conventional CNN-LSTM.
* Higher R² values.
* Improved hyperparameter configurations.
* Better optimization stability.
* More robust prediction performance across multiple runs.

The Firefly Algorithm is expected to improve model accuracy by automatically discovering superior hyperparameter combinations that may be difficult to identify through manual tuning.

---

# 8. Evaluation Summary

This study adopts a comprehensive evaluation framework consisting of prediction performance metrics, optimization performance metrics, and computational performance metrics.

Prediction accuracy will be evaluated using MAE, MSE, RMSE, R² Score, and Improvement Rate. Optimization effectiveness will be assessed through Best Fitness Value, Convergence Rate, Optimization Stability, and Statistical Stability Analysis. Computational feasibility will be measured using Training Time, Optimization Time, and Inference Time.

Together, these metrics provide a rigorous, objective, and comprehensive assessment of the proposed Firefly-Optimized CNN-LSTM framework for Remaining Useful Life prediction of rolling bearings.
