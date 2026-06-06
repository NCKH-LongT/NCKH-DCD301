# Literature Review Matrix

## Research Topic

**Firefly-Optimized CNN-LSTM for Remaining Useful Life Prediction of Rolling Bearings**

---

# Literature Review Matrix

| No. | Paper Title                                                                                                                                                  | Category                           | AI Method / Model                         | Main Contribution                                                                       | Limitation                                                          | Relevance to Proposed Work                                                                                         |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------- | ----------------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| 1   | Prediction of the Remaining Useful Life of Bearings Through CNN-Bi-LSTM-Based Domain Adaptation Model                                                        | Traditional Deep Learning RUL      | CNN-BiLSTM + Domain Adaptation            | Improves generalization across different operating conditions by reducing domain shift. | Increased model complexity and computational cost.                  | Demonstrates the effectiveness of CNN-LSTM variants for extracting degradation features and temporal dependencies. |
| 2   | Prediction of Remaining Useful Life of Rolling Bearings                                                                                                      | Traditional Deep Learning RUL      | Deep Learning-Based RUL Framework         | Establishes a baseline deep learning approach for bearing prognostics.                  | Limited ability to capture complex degradation patterns.            | Serves as a baseline reference for evaluating advanced architectures.                                              |
| 3   | Remaining Useful Life Prediction of Rolling Bearings Based on CNN-LSTM                                                                                       | Traditional Deep Learning RUL      | CNN-LSTM                                  | Combines CNN feature extraction with LSTM temporal modeling for RUL estimation.         | Hyperparameters selected manually.                                  | Forms the core architecture of the proposed Firefly-CNN-LSTM model.                                                |
| 4   | Research on Remaining Useful Life Prediction of Bearings Based on MBCNN-BiLSTM                                                                               | Traditional Deep Learning RUL      | MBCNN-BiLSTM                              | Enhances multi-scale feature extraction and sequence learning.                          | More parameters increase training complexity.                       | Shows benefits of hybrid CNN-LSTM architectures.                                                                   |
| 5   | Rolling Bearing Remaining Useful Life Prediction Based on CNN-VAE-MBiLSTM                                                                                    | Traditional Deep Learning RUL      | CNN-VAE-MBiLSTM                           | Integrates feature compression and bidirectional temporal learning.                     | Computationally expensive and difficult to tune.                    | Highlights the importance of feature representation learning.                                                      |
| 6   | SAL-CNN: Estimate the Remaining Useful Life of Bearings                                                                                                      | Traditional Deep Learning RUL      | Self-Attention Learning CNN               | Improves degradation feature extraction through attention-guided learning.              | Limited temporal modeling capability compared to LSTM-based models. | Provides insight into attention-enhanced feature extraction.                                                       |
| 7   | Remaining Useful Life Prediction of Rolling Bearings Based on CBAM-CNN-LSTM                                                                                  | Attention-Based Models             | CBAM-CNN-LSTM                             | Uses channel and spatial attention to improve degradation representation.               | Higher training cost and architectural complexity.                  | Demonstrates how attention mechanisms can improve CNN-LSTM performance.                                            |
| 8   | Remaining Useful Life Prediction Method for Bearings Based on LSTM with Uncertainty Quantification                                                           | Uncertainty-Aware RUL              | LSTM + Uncertainty Quantification         | Provides confidence intervals and reliability estimates for RUL predictions.            | Does not optimize network hyperparameters.                          | Highlights reliability and interpretability aspects of RUL prediction.                                             |
| 9   | Bearing Remaining Useful Life Prediction with an Improved CNN-LSTM Network Using an Artificial Gorilla Troop Optimization Algorithm                          | Metaheuristic Optimization for RUL | GTO-CNN-LSTM                              | Uses Gorilla Troop Optimization to tune CNN-LSTM hyperparameters automatically.         | Optimization performance depends on algorithm settings.             | Directly related to automated hyperparameter optimization for CNN-LSTM.                                            |
| 10  | Wind Power Generation Prediction Using LSTM Model Optimized by Sparrow Search Algorithm and Firefly Algorithm                                                | Metaheuristic Optimization         | SSA-FA-LSTM                               | Demonstrates the effectiveness of Firefly-based optimization in time-series prediction. | Application domain is not prognostics.                              | Provides evidence that Firefly Algorithm improves LSTM performance.                                                |
| 11  | An Improved Firefly Algorithm with Dynamic Self-Adaptive Adjustment                                                                                          | Firefly Literature                 | Improved Firefly Algorithm                | Enhances exploration and exploitation balance through adaptive parameter control.       | Not evaluated on deep learning optimization tasks.                  | Potential optimization strategy for CNN-LSTM hyperparameter tuning.                                                |
| 12  | Firefly Neural Architecture Descent: A General Approach for Growing Neural Networks                                                                          | Firefly Literature                 | Firefly-Based Neural Architecture Search  | Applies Firefly principles to neural architecture optimization.                         | Focuses on architecture growth rather than prognostics.             | Supports automatic architecture optimization concepts.                                                             |
| 13  | Investigating the Performance of LSTM Models Optimized by Firefly Algorithms on Diverse Time-Series Data                                                     | Firefly Literature                 | FA-LSTM                                   | Demonstrates improved forecasting accuracy after Firefly optimization.                  | Not evaluated on bearing degradation datasets.                      | Strong evidence supporting Firefly optimization for LSTM models.                                                   |
| 14  | Optimizing Convolutional Neural Network Hyperparameters by Enhanced Swarm Intelligence Metaheuristics                                                        | Firefly Literature                 | Swarm-Optimized CNN                       | Compares swarm intelligence approaches for CNN tuning.                                  | Does not evaluate CNN-LSTM architectures.                           | Supports metaheuristic-based hyperparameter optimization.                                                          |
| 15  | Optimizing Transfer Learning and Fine-Tuning Hyperparameters in Image Classification Problems with Firefly Algorithm                                         | Firefly Literature                 | Firefly-Based Hyperparameter Optimization | Shows Firefly Algorithm can effectively optimize neural network configurations.         | Focused on image classification tasks.                              | Confirms Firefly's capability in deep learning optimization.                                                       |
| 16  | Parameter Tuning of the Firefly Algorithm by Three Tuning Methods: Standard Monte Carlo, Quasi-Monte Carlo and Latin Hypercube Sampling Methods              | Firefly Literature                 | Firefly Parameter Analysis                | Investigates parameter sensitivity and tuning strategies for Firefly Algorithm.         | Does not involve deep learning applications.                        | Useful for selecting Firefly parameters in the proposed model.                                                     |
| 17  | Performance of a Novel Chaotic Firefly Algorithm with Enhanced Exploration for Tackling Global Optimization Problems: Application for Dropout Regularization | Firefly Literature                 | Chaotic Firefly Algorithm                 | Improves global search capability and avoids local optima.                              | Not tested in prognostics applications.                             | Suggests possible future enhancement of Firefly-CNN-LSTM optimization.                                             |

---

# Research Trend Analysis

The reviewed literature can be grouped into four major research directions.

| Research Direction                            | Number of Papers | Percentage |
| --------------------------------------------- | ---------------- | ---------- |
| Traditional CNN/LSTM-Based RUL Prediction     | 6                | 35.3%      |
| Attention & Uncertainty-Based Models          | 2                | 11.8%      |
| Metaheuristic Optimization for RUL Prediction | 2                | 11.8%      |
| Firefly Algorithm & Optimization Literature   | 7                | 41.1%      |
| **Total**                                     | **17**           | **100%**   |

---

# Research Gap Identification

Based on the reviewed studies, several research gaps remain open.

## Gap 1: Manual Hyperparameter Selection

Most CNN-LSTM-based RUL prediction studies still rely on manually selected hyperparameters, including learning rate, number of filters, kernel size, batch size, hidden units, and dropout rate. Manual tuning is time-consuming and may not guarantee optimal performance.

## Gap 2: Limited Application of Firefly Algorithm in Bearing RUL Prediction

Although Firefly Algorithm has demonstrated strong optimization capability in neural networks, time-series forecasting, transfer learning, and architecture search, its application to bearing Remaining Useful Life prediction remains limited.

## Gap 3: Lack of Firefly-Optimized CNN-LSTM Frameworks

Few studies have investigated the integration of Firefly Algorithm with CNN-LSTM architectures for RUL prediction using benchmark bearing datasets such as FEMTO-ST (PRONOSTIA) and IMS.

## Gap 4: Need for More Stable and Automated Prognostic Models

Existing approaches primarily focus on improving network architecture. Comparatively less attention has been paid to developing automated hyperparameter optimization frameworks that improve prediction accuracy, convergence speed, and model robustness simultaneously.

---

# Contribution of the Proposed Study

To address the identified gaps, this research proposes a **Firefly-Optimized CNN-LSTM** framework for Remaining Useful Life prediction of rolling bearings.

The proposed study aims to:

1. Automatically optimize critical CNN-LSTM hyperparameters using Firefly Algorithm.
2. Reduce dependence on manual hyperparameter tuning.
3. Improve prediction accuracy and convergence stability.
4. Evaluate performance on benchmark bearing degradation datasets such as FEMTO-ST and IMS.
5. Compare the proposed model against conventional CNN-LSTM and optimization-based baseline methods.
6. Provide a practical and efficient prognostic framework for predictive maintenance applications.

---

# Summary

The literature review demonstrates that CNN-LSTM architectures are among the most effective approaches for bearing Remaining Useful Life prediction. Recent studies also indicate that metaheuristic optimization algorithms can significantly enhance deep learning performance through automated hyperparameter tuning. However, the combination of Firefly Algorithm and CNN-LSTM for bearing RUL prediction remains insufficiently explored. Therefore, the proposed Firefly-Optimized CNN-LSTM model represents a promising research direction with both theoretical significance and practical value in predictive maintenance and Prognostics and Health Management (PHM).
