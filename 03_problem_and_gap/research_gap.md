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