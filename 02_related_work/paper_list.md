# Paper List

## Research Topic

**Firefly-Optimized CNN-LSTM for Remaining Useful Life Prediction of Rolling Bearings**

---

# 2.1 Traditional Deep Learning for RUL Prediction

Các nghiên cứu trong nhóm này tập trung vào việc sử dụng CNN, LSTM, BiLSTM và các mô hình lai nhằm khai thác đặc trưng suy giảm của ổ lăn từ dữ liệu rung động để dự đoán tuổi thọ còn lại (RUL).

| No. | Paper Title                                                                                           |
| --- | ----------------------------------------------------------------------------------------------------- |
| 1   | Prediction of the Remaining Useful Life of Bearings Through CNN-Bi-LSTM-Based Domain Adaptation Model |
| 2   | Prediction of Remaining Useful Life of Rolling Bearings                                               |
| 3   | Remaining Useful Life Prediction of Rolling Bearings Based on CNN-LSTM                                |
| 4   | Research on Remaining Useful Life Prediction of Bearings Based on MBCNN-BiLSTM (2023)                 |
| 5   | Rolling Bearing Remaining Useful Life Prediction Based on CNN-VAE-MBiLSTM                             |
| 6   | SAL-CNN: Estimate the Remaining Useful Life of Bearings                                               |

---

# 2.2 Attention-Based and Advanced Deep Learning Models

Nhóm nghiên cứu này cải tiến các mô hình CNN-LSTM truyền thống bằng cơ chế Attention và các kỹ thuật học sâu tiên tiến nhằm nâng cao khả năng trích xuất đặc trưng suy giảm.

| No. | Paper Title                                                                                        |
| --- | -------------------------------------------------------------------------------------------------- |
| 7   | Remaining Useful Life Prediction of Rolling Bearings Based on CBAM-CNN-LSTM                        |
| 8   | Remaining Useful Life Prediction Method for Bearings Based on LSTM with Uncertainty Quantification |

---

# 2.3 Metaheuristic Optimization for Deep Learning-Based RUL Prediction

Các nghiên cứu này sử dụng các thuật toán tối ưu hóa metaheuristic để tự động lựa chọn siêu tham số và cải thiện hiệu năng của mô hình học sâu.

| No. | Paper Title                                                                                                                         |
| --- | ----------------------------------------------------------------------------------------------------------------------------------- |
| 9   | Bearing Remaining Useful Life Prediction with an Improved CNN-LSTM Network Using an Artificial Gorilla Troop Optimization Algorithm |
| 10  | Wind Power Generation Prediction Using LSTM Model Optimized by Sparrow Search Algorithm and Firefly Algorithm                       |

---

# 2.4 Firefly Algorithm and Deep Learning Optimization Literature

Nhóm nghiên cứu này cung cấp nền tảng lý thuyết và thực nghiệm cho việc ứng dụng Firefly Algorithm trong tối ưu hóa mô hình học máy và học sâu.

| No. | Paper Title                                                                                                                                                  |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 11  | An Improved Firefly Algorithm with Dynamic Self-Adaptive Adjustment                                                                                          |
| 12  | Firefly Neural Architecture Descent: A General Approach for Growing Neural Networks                                                                          |
| 13  | Investigating the Performance of LSTM Models Optimized by Firefly Algorithms on Diverse Time-Series Data                                                     |
| 14  | Optimizing Convolutional Neural Network Hyperparameters by Enhanced Swarm Intelligence Metaheuristics                                                        |
| 15  | Optimizing Transfer Learning and Fine-Tuning Hyperparameters in Image Classification Problems with Firefly Algorithm                                         |
| 16  | Parameter Tuning of the Firefly Algorithm by Three Tuning Methods: Standard Monte Carlo, Quasi-Monte Carlo and Latin Hypercube Sampling Methods              |
| 17  | Performance of a Novel Chaotic Firefly Algorithm with Enhanced Exploration for Tackling Global Optimization Problems: Application for Dropout Regularization |

---

# Research Categorization Summary

| Category                                         | Number of Papers |
| ------------------------------------------------ | ---------------- |
| CNN / LSTM / BiLSTM Based RUL Prediction         | 6                |
| Attention & Uncertainty-Aware Models             | 2                |
| Metaheuristic Optimization for Prediction Models | 2                |
| Firefly Algorithm & Optimization Literature      | 7                |
| **Total**                                        | **17**           |

---

# Selection Criteria

The selected papers were chosen based on the following criteria:

* Published in peer-reviewed journals or conference proceedings.
* Related to Remaining Useful Life (RUL) prediction, prognostics, or predictive maintenance.
* Utilized deep learning architectures such as CNN, LSTM, BiLSTM, CNN-LSTM, or hybrid networks.
* Investigated metaheuristic optimization algorithms, especially Firefly Algorithm.
* Provided insights relevant to hyperparameter optimization and bearing prognostics.

---

# Contribution to This Study

The reviewed literature provides three important foundations for this research:

1. CNN-LSTM and its variants are among the most effective architectures for bearing RUL prediction.
2. Recent studies show that optimization algorithms can significantly improve deep learning performance through automated hyperparameter tuning.
3. Although Firefly Algorithm has demonstrated promising optimization capability in many deep learning applications, its application to CNN-LSTM-based bearing RUL prediction remains limited.

Therefore, this study proposes a Firefly-Optimized CNN-LSTM model to automatically optimize critical hyperparameters and improve prediction accuracy for bearing Remaining Useful Life estimation.










# Paper List

## Research Topic

**Firefly-Optimized CNN-LSTM for Remaining Useful Life Prediction of Rolling Bearings**

---

# Introduction

This document presents the collection and categorization of research papers selected for the literature review phase of the study entitled **"Firefly-Optimized CNN-LSTM for Remaining Useful Life Prediction of Rolling Bearings."**

The selected literature was organized into four major categories:

1. Traditional Deep Learning Models for RUL Prediction.
2. Attention and Uncertainty-Aware RUL Prediction Models.
3. Metaheuristic Optimization for Deep Learning-Based Prediction.
4. Firefly Algorithm and Deep Learning Optimization Literature.

This categorization enables a systematic analysis of existing approaches and facilitates the identification of research gaps for the proposed Firefly-Optimized CNN-LSTM framework.

---

# 2.1 Traditional Deep Learning Models for RUL Prediction

This category focuses on deep learning architectures that directly estimate the Remaining Useful Life (RUL) of rolling bearings from degradation signals. These studies mainly employ CNN, LSTM, BiLSTM, and hybrid CNN-LSTM architectures to capture both spatial and temporal degradation characteristics.

| No. | Paper Title                                                                                           | Main Technique                     | Relevance |
| --- | ----------------------------------------------------------------------------------------------------- | ---------------------------------- | --------- |
| 1   | Prediction of the Remaining Useful Life of Bearings Through CNN-Bi-LSTM-Based Domain Adaptation Model | CNN-BiLSTM + Domain Adaptation     | High      |
| 2   | Prediction of Remaining Useful Life of Rolling Bearings                                               | Deep Learning-Based RUL Prediction | High      |
| 3   | Remaining Useful Life Prediction of Rolling Bearings Based on CNN-LSTM                                | CNN-LSTM                           | Very High |
| 4   | Research on Remaining Useful Life Prediction of Bearings Based on MBCNN-BiLSTM                        | Multi-Branch CNN + BiLSTM          | High      |
| 5   | Rolling Bearing Remaining Useful Life Prediction Based on CNN-VAE-MBiLSTM                             | CNN-VAE-MBiLSTM                    | High      |
| 6   | SAL-CNN: Estimate the Remaining Useful Life of Bearings                                               | Self-Attention Learning CNN        | Medium    |

### Category Contribution

These studies demonstrate that CNN-LSTM-based architectures have become one of the most effective approaches for bearing RUL prediction due to their capability to simultaneously extract degradation features and temporal dependencies.

---

# 2.2 Attention and Uncertainty-Aware RUL Prediction Models

Recent studies have enhanced traditional CNN-LSTM architectures by introducing attention mechanisms and uncertainty quantification methods. These approaches aim to improve feature extraction, interpretability, and prediction reliability.

| No. | Paper Title                                                                                        | Main Technique            | Relevance |
| --- | -------------------------------------------------------------------------------------------------- | ------------------------- | --------- |
| 7   | Remaining Useful Life Prediction of Rolling Bearings Based on CBAM-CNN-LSTM                        | CBAM Attention + CNN-LSTM | Very High |
| 8   | Remaining Useful Life Prediction Method for Bearings Based on LSTM with Uncertainty Quantification | LSTM + UQ                 | High      |

### Category Contribution

The literature confirms that attention mechanisms can significantly improve prediction performance by emphasizing critical degradation features. However, these methods often increase model complexity and computational cost.

---

# 2.3 Metaheuristic Optimization for Deep Learning-Based Prediction

This category investigates the application of metaheuristic optimization algorithms to automatically search for optimal hyperparameters in deep learning models.

| No. | Paper Title                                                                                                                         | Main Technique | Relevance |
| --- | ----------------------------------------------------------------------------------------------------------------------------------- | -------------- | --------- |
| 9   | Bearing Remaining Useful Life Prediction with an Improved CNN-LSTM Network Using an Artificial Gorilla Troop Optimization Algorithm | CNN-LSTM + GTO | Very High |
| 10  | Wind Power Generation Prediction Using LSTM Model Optimized by Sparrow Search Algorithm and Firefly Algorithm                       | SSA-FA-LSTM    | Medium    |

### Category Contribution

These studies provide evidence that automated hyperparameter optimization can significantly improve prediction accuracy compared with manually tuned deep learning models.

---

# 2.4 Firefly Algorithm and Deep Learning Optimization Literature

This category provides theoretical and experimental foundations for employing Firefly Algorithm in optimization problems involving machine learning and deep learning models.

| No. | Paper Title                                                                                                          | Main Technique                   | Relevance |
| --- | -------------------------------------------------------------------------------------------------------------------- | -------------------------------- | --------- |
| 11  | An Improved Firefly Algorithm with Dynamic Self-Adaptive Adjustment                                                  | Improved Firefly Algorithm       | High      |
| 12  | Firefly Neural Architecture Descent: A General Approach for Growing Neural Networks                                  | Neural Architecture Optimization | High      |
| 13  | Investigating the Performance of LSTM Models Optimized by Firefly Algorithms on Diverse Time-Series Data             | FA-LSTM                          | Very High |
| 14  | Optimizing Convolutional Neural Network Hyperparameters by Enhanced Swarm Intelligence Metaheuristics                | CNN Hyperparameter Optimization  | High      |
| 15  | Optimizing Transfer Learning and Fine-Tuning Hyperparameters in Image Classification Problems with Firefly Algorithm | Transfer Learning Optimization   | Medium    |
| 16  | Parameter Tuning of the Firefly Algorithm by Three Tuning Methods                                                    | Firefly Parameter Analysis       | Medium    |
| 17  | Performance of a Novel Chaotic Firefly Algorithm with Enhanced Exploration for Tackling Global Optimization Problems | Chaotic Firefly Optimization     | High      |

### Category Contribution

The reviewed studies indicate that Firefly Algorithm possesses strong global search capability, good convergence characteristics, and significant potential for hyperparameter optimization in deep learning applications.

---

# Research Categorization Summary

| Category                                         | Number of Papers |
| ------------------------------------------------ | ---------------- |
| Traditional CNN/LSTM-Based RUL Prediction        | 6                |
| Attention and Uncertainty-Aware Models           | 2                |
| Metaheuristic Optimization for Prediction Models | 2                |
| Firefly Algorithm and Optimization Literature    | 7                |
| **Total**                                        | **17**           |

---

# Paper Selection Criteria

The selected papers satisfy the following criteria:

* Published in peer-reviewed journals or conference proceedings.
* Related to Remaining Useful Life (RUL), Prognostics and Health Management (PHM), or Predictive Maintenance.
* Utilize CNN, LSTM, BiLSTM, CNN-LSTM, or hybrid deep learning architectures.
* Investigate hyperparameter optimization techniques for deep learning models.
* Include Firefly Algorithm or related swarm intelligence approaches.
* Provide methodological insights applicable to bearing degradation prediction.

---

# Contribution to the Proposed Research

The literature review reveals three major findings:

1. CNN-LSTM and its variants remain among the most effective architectures for bearing RUL prediction.
2. Metaheuristic optimization algorithms can substantially improve deep learning performance through automated hyperparameter tuning.
3. Although Firefly Algorithm has demonstrated promising optimization capability across multiple domains, its application to CNN-LSTM-based bearing RUL prediction remains limited.

Consequently, this study proposes a **Firefly-Optimized CNN-LSTM model** that automatically searches for optimal hyperparameters, including convolution filters, kernel sizes, LSTM units, and learning rates, with the objective of improving RUL prediction accuracy and model robustness.
