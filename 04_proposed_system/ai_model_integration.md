    # AI Model Integration

## 1. Overview of the Proposed AI Model

This study proposes a Firefly-Optimized CNN-LSTM framework for Remaining Useful Life (RUL) prediction of rolling bearings. The proposed model integrates a Convolutional Neural Network (CNN) and a Long Short-Term Memory (LSTM) network, while employing the Firefly Algorithm (FA) to automatically optimize critical hyperparameters.

The integration aims to address a key limitation identified in the literature: although CNN-LSTM architectures have demonstrated strong predictive performance for bearing prognostics, their effectiveness is highly dependent on manually selected hyperparameters. Manual tuning is often time-consuming, computationally expensive, and susceptible to suboptimal solutions.

The proposed framework combines:

* CNN for automatic feature extraction from vibration signals.
* LSTM for temporal degradation modeling.
* Firefly Algorithm for hyperparameter optimization.
* RUL estimation module for bearing life prediction.

The overall objective is to improve prediction accuracy, model robustness, and convergence performance while reducing the dependence on manual parameter selection.

---

# 2. Convolutional Neural Network (CNN) Module

## 2.1 Purpose of CNN

Rolling bearing vibration signals contain complex degradation patterns that are difficult to capture using traditional handcrafted features.

The CNN module is employed to automatically learn degradation-related features directly from raw or preprocessed vibration signals.

Unlike conventional feature engineering approaches, CNN can identify:

* Local degradation characteristics.
* Frequency-related fault signatures.
* Amplitude variations.
* Nonlinear degradation patterns.

## 2.2 CNN Function in the Proposed Framework

Within the proposed architecture, CNN serves as the first feature extraction stage.

Input:

* Bearing vibration signals.
* Time-domain signal segments generated through sliding-window preprocessing.

Output:

* High-level degradation feature representations.

These extracted features are subsequently provided to the LSTM module for temporal sequence learning.

## 2.3 Justification from Literature

Several studies reviewed in the literature demonstrated that CNN-based architectures significantly improve feature extraction capability for bearing prognostics.

Research such as:

* CNN-LSTM
* CNN-BiLSTM
* CNN-VAE-MBiLSTM
* SAL-CNN

reported superior performance compared with conventional machine learning approaches because CNN effectively captures local degradation information from vibration signals.

---

# 3. Long Short-Term Memory (LSTM) Module

## 3.1 Purpose of LSTM

Although CNN is effective at extracting degradation features, it lacks the ability to model long-term temporal dependencies.

Bearing degradation is inherently a sequential process where future health conditions depend on historical operating states.

LSTM is therefore employed to learn temporal degradation evolution patterns.

## 3.2 LSTM Function in the Proposed Framework

The LSTM module receives feature vectors extracted by CNN.

Its responsibilities include:

* Learning degradation progression trends.
* Capturing long-term temporal dependencies.
* Modeling health state evolution.
* Supporting future RUL estimation.

Input:

* CNN feature sequences.

Output:

* Temporal degradation representations.

These representations are used to estimate Remaining Useful Life.

## 3.3 Justification from Literature

Numerous studies identified in the literature review reported that hybrid CNN-LSTM architectures outperform standalone CNN models because they combine:

* Spatial feature learning.
* Temporal sequence learning.

This combination is particularly effective for bearing degradation modeling and RUL prediction.

---

# 4. CNN-LSTM Hybrid Architecture

## 4.1 Integration Strategy

The proposed model integrates CNN and LSTM in a sequential manner.

Workflow:

Bearing Vibration Signal

↓

CNN Feature Extraction

↓

Feature Sequence Generation

↓

LSTM Temporal Learning

↓

RUL Prediction Layer

The CNN module transforms raw signals into representative feature vectors, while the LSTM module learns degradation evolution from these feature sequences.

## 4.2 Advantages of CNN-LSTM

Compared with standalone models, CNN-LSTM offers:

* Better feature representation.
* Improved temporal dependency learning.
* Higher prediction accuracy.
* Greater robustness against noise.

These advantages explain why CNN-LSTM and its variants remain among the most frequently adopted architectures in recent bearing prognostics research.

---

# 5. Firefly Algorithm Optimization Module

## 5.1 Motivation

A major limitation identified in the reviewed literature is the dependence on manually selected hyperparameters.

Examples include:

* Learning rate.
* Number of CNN filters.
* Kernel size.
* Number of LSTM units.
* Dropout rate.
* Batch size.

Poor parameter selection may significantly reduce prediction performance.

## 5.2 Firefly Algorithm Overview

The Firefly Algorithm is a swarm intelligence optimization technique inspired by the flashing behavior of fireflies.

Each firefly represents a candidate hyperparameter configuration.

The brightness of a firefly corresponds to model performance, measured using prediction error metrics such as RMSE.

Brighter fireflies attract weaker ones, guiding the population toward better solutions.

## 5.3 Advantages of Firefly Algorithm

Compared with other metaheuristic approaches such as:

* Genetic Algorithm (GA)
* Particle Swarm Optimization (PSO)
* Sparrow Search Algorithm (SSA)
* Gorilla Troop Optimizer (GTO)

Firefly Algorithm offers:

* Effective global exploration.
* Strong local exploitation capability.
* Reduced risk of local optimum trapping.
* Competitive convergence speed.
* Simple implementation.

These characteristics make Firefly Algorithm suitable for optimizing deep learning hyperparameters.

---

# 6. Firefly-CNN-LSTM Integration

## 6.1 Optimization Targets

The Firefly Algorithm is used to optimize critical CNN-LSTM hyperparameters, including:

* Learning Rate
* Number of CNN Filters
* CNN Kernel Size
* Number of LSTM Units
* Dropout Rate
* Batch Size

## 6.2 Optimization Workflow

Initialization of Firefly Population

↓

Generate Hyperparameter Candidates

↓

Train CNN-LSTM Model

↓

Evaluate Prediction Error

↓

Update Firefly Positions

↓

Generate Improved Solutions

↓

Termination Criterion Reached

↓

Optimal Hyperparameter Set

↓

Final CNN-LSTM Training

↓

RUL Prediction

## 6.3 Expected Benefits

The integration of Firefly Algorithm is expected to:

* Improve prediction accuracy.
* Reduce RMSE and MAE.
* Improve model stability.
* Accelerate convergence.
* Reduce human intervention.

---

# 7. Relationship to Research Gap

The literature review identified that most existing RUL prediction studies focus on:

* CNN-LSTM architecture enhancement.
* Attention mechanisms.
* Uncertainty modeling.

However, limited research has investigated the direct integration of Firefly Algorithm with CNN-LSTM for rolling bearing RUL prediction.

Furthermore, many existing studies continue to rely on manually selected hyperparameters or alternative optimization techniques such as PSO, GA, SSA, and GTO.

Therefore, the proposed Firefly-Optimized CNN-LSTM framework directly addresses this research gap by introducing automated hyperparameter optimization into CNN-LSTM-based bearing prognostics.

---

# 8. Expected Research Contribution

The expected contributions of this study include:

1. Development of a Firefly-Optimized CNN-LSTM framework for bearing RUL prediction.

2. Automated optimization of CNN-LSTM hyperparameters using Firefly Algorithm.

3. Comprehensive evaluation on benchmark bearing datasets such as FEMTO-ST (PRONOSTIA) and IMS.

4. Comparison with conventional CNN-LSTM and other baseline approaches.

5. Improvement of prediction accuracy and model robustness for predictive maintenance applications.

---

# 9. Summary

This study integrates CNN, LSTM, and Firefly Algorithm into a unified prognostics framework for Remaining Useful Life prediction of rolling bearings.

CNN is responsible for degradation feature extraction, LSTM models temporal degradation behavior, and Firefly Algorithm automatically optimizes critical hyperparameters.

The proposed Firefly-Optimized CNN-LSTM model is expected to provide more accurate, stable, and efficient RUL prediction compared with conventional manually tuned CNN-LSTM approaches, thereby contributing to the advancement of intelligent predictive maintenance systems.
