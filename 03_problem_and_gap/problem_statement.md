# Problem Statement

## Research Topic

Firefly-Optimized CNN-LSTM for Remaining Useful Life Prediction of Rolling Bearings

---

# 1. Background

Rolling bearings are critical components in rotating machinery and are widely used in industrial equipment such as turbines, motors, pumps, compressors, and manufacturing systems. The degradation or failure of bearings can significantly reduce system reliability, increase maintenance costs, and lead to unexpected downtime.

To address this issue, Prognostics and Health Management (PHM) has emerged as an important research area that focuses on monitoring equipment health and predicting failures before they occur. One of the most important PHM tasks is Remaining Useful Life (RUL) prediction, which estimates the amount of operational time remaining before a component reaches failure.

Accurate RUL prediction enables condition-based maintenance, reduces maintenance costs, improves operational safety, and minimizes unexpected production interruptions.

---

# 2. Practical Problem

Traditional maintenance strategies are generally categorized into:

- Corrective Maintenance (repair after failure).
- Preventive Maintenance (maintenance at fixed intervals).

These approaches suffer from several limitations.

Corrective maintenance often results in unexpected failures and expensive downtime, while preventive maintenance may replace components that are still in usable condition, leading to unnecessary maintenance costs.

Therefore, industries increasingly require predictive maintenance solutions capable of estimating equipment degradation and predicting remaining useful life in advance.

---

# 3. Existing Research Approaches

Recent studies have demonstrated the effectiveness of deep learning techniques for bearing RUL prediction.

Convolutional Neural Networks (CNNs) are commonly used to automatically extract degradation features from vibration signals.

Long Short-Term Memory (LSTM) networks are effective in modeling temporal degradation patterns and long-term dependencies.

To leverage the strengths of both architectures, many researchers have proposed hybrid CNN-LSTM models for RUL prediction.

Several advanced approaches have further incorporated:

- Bidirectional LSTM (BiLSTM)
- Attention Mechanisms
- Variational Autoencoders (VAE)
- Domain Adaptation Techniques
- Uncertainty Quantification

These approaches have achieved improved prediction accuracy compared with conventional methods.

---

# 4. Limitations of Existing Studies

Despite significant progress, several limitations remain.

First, most existing studies focus primarily on designing more complex neural network architectures while relying on manually selected hyperparameters.

Second, CNN-LSTM performance is highly sensitive to hyperparameter settings such as:

- Number of convolution filters
- Kernel size
- Number of LSTM units
- Learning rate
- Batch size
- Dropout rate

In many studies, these hyperparameters are determined through trial-and-error experiments, which can be time-consuming and may not produce optimal results.

Third, suboptimal hyperparameter configurations may lead to:

- Reduced prediction accuracy
- Slower convergence
- Overfitting
- Poor model generalization

Consequently, there is a need for an automated and intelligent hyperparameter optimization strategy for CNN-LSTM-based RUL prediction models.

---

# 5. Research Motivation

Metaheuristic optimization algorithms have recently demonstrated strong capabilities in solving complex optimization problems.

Algorithms such as:

- Particle Swarm Optimization (PSO)
- Genetic Algorithm (GA)
- Whale Optimization Algorithm (WOA)
- Sparrow Search Algorithm (SSA)
- Gorilla Troop Optimization (GTO)

have been successfully applied to optimize deep learning models.

Among these approaches, Firefly Algorithm (FA) has shown promising performance due to its balance between global exploration and local exploitation, enabling efficient search for optimal solutions.

The success of Firefly Algorithm in neural network optimization motivates its application to CNN-LSTM-based bearing RUL prediction.

---

# 6. Research Problem

This study investigates the following research problem:

How can Firefly Algorithm be integrated with a CNN-LSTM architecture to automatically optimize critical hyperparameters and improve the accuracy and robustness of Remaining Useful Life prediction for rolling bearings?

---

# 7. Expected Contribution

The proposed study aims to:

- Develop a Firefly-Optimized CNN-LSTM framework for bearing RUL prediction.
- Automate hyperparameter optimization using Firefly Algorithm.
- Improve prediction accuracy compared with conventional CNN-LSTM models.
- Reduce prediction error and improve model convergence.
- Provide a practical predictive maintenance solution for bearing health management applications.

---