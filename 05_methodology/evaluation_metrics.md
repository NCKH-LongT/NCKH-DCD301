# Evaluation Metrics

## 1. Evaluation Objective

The evaluation must prove whether the proposed reliability-aware AIoT system improves smart greenhouse decision support compared with simpler baselines.

The system is evaluated from seven perspectives:

| Evaluation Type | Suitable Metrics |
|---|---|
| Classification / detection | Accuracy, Precision, Recall, F1-score |
| Prediction / scoring | MAE, RMSE, MAPE |
| Retrieval / recommendation | Top-k Accuracy, Precision@k, Recall@k, NDCG |
| RAG / LLM quality | Relevance, Faithfulness, Correctness, Expert Rating |
| System performance | Response Time, Throughput, Latency |
| User evaluation | Survey, SUS, User Satisfaction |
| Process comparison | Time Saving, Error Reduction |

## 2. Detection Metrics

Detection metrics are used for BCD validation, overflow detection, missing data detection, sensor fault detection, and unsafe-control blocking.

### 2.1 Confusion Matrix

| Term | Meaning in This Project |
|---|---|
| True Positive (TP) | System correctly detects an error case |
| True Negative (TN) | System correctly accepts a valid case |
| False Positive (FP) | System marks valid data as faulty |
| False Negative (FN) | System misses a real error case |

### 2.2 Accuracy

Accuracy measures the overall percentage of correct predictions.

```text
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```

Use for:

- Overall BCD validation result.
- Overall scenario status classification.
- Correct `Normal`, `Warning`, `Critical`, and `Blocked` labels.

### 2.3 Precision

Precision measures how many detected error cases are truly errors.

```text
Precision = TP / (TP + FP)
```

Use for:

- Invalid BCD detection.
- Overflow detection.
- Sensor fault detection.
- Safety blocking.

High precision means the system does not over-block valid greenhouse data.

### 2.4 Recall

Recall measures how many real error cases are detected.

```text
Recall = TP / (TP + FN)
```

Use for:

- Invalid BCD detection.
- Missing data detection.
- Critical unsafe data detection.

High recall is important because missing an invalid BCD or overflow case can lead to unsafe actuator actions.

### 2.5 F1-Score

F1-score balances precision and recall.

```text
F1-score = 2 * Precision * Recall / (Precision + Recall)
```

Use for:

- Data quality detection summary.
- Sensor fault detection summary.
- Safe-failure classification.

## 3. Prediction and Scoring Metrics

The system generates numerical scores such as data quality score, confidence score, and relevance score. If ground truth or expert-assigned target scores are available, prediction metrics can be used.

### 3.1 Mean Absolute Error

```text
MAE = average(|predicted_score - expected_score|)
```

Use for:

- Data quality score difference.
- Confidence score difference.
- Expert score alignment.

### 3.2 Root Mean Squared Error

```text
RMSE = sqrt(average((predicted_score - expected_score)^2))
```

Use when large scoring errors should be penalized more strongly.

### 3.3 Mean Absolute Percentage Error

```text
MAPE = average(|actual - predicted| / actual) * 100%
```

Use only when the expected value is not zero.

In this project, MAPE is optional and should be used mainly for numerical sensor estimation or latency prediction, not for labels.

## 4. RAG Retrieval Metrics

RAG retrieval metrics evaluate whether the system retrieves useful greenhouse knowledge before generating a recommendation.

### 4.1 Top-k Accuracy

Top-k Accuracy checks whether at least one relevant document appears in the top `k` retrieved results.

Use for:

- Checking whether the correct guideline appears in top 3 or top 5 retrieved chunks.

Example:

```text
Top-3 Accuracy = number of cases with a relevant chunk in top 3 / total cases
```

### 4.2 Precision@k

Precision@k measures how many of the top `k` retrieved chunks are relevant.

```text
Precision@k = relevant chunks in top k / k
```

Use for:

- Measuring retrieval noise.
- Comparing RAG-only and proposed system retrieval quality.

### 4.3 Recall@k

Recall@k measures how many relevant chunks are retrieved among all relevant chunks.

```text
Recall@k = relevant retrieved chunks in top k / total relevant chunks
```

Use for:

- Checking whether the system can retrieve enough supporting evidence.

### 4.4 NDCG

Normalized Discounted Cumulative Gain evaluates whether highly relevant documents are ranked near the top.

Use for:

- Ranking quality of retrieved greenhouse guideline passages.
- Comparing retrieval performance across query designs.

## 5. LLM and Agentic RAG Quality Metrics

Because the final output includes explanations and recommendations, some evaluation must be done using a rubric or expert rating.

### 5.1 Correctness

Correctness measures whether the final action matches the expected greenhouse decision.

Scoring rubric:

| Score | Meaning |
|---:|---|
| 1 | Wrong or unsafe recommendation |
| 2 | Partially wrong and missing key condition |
| 3 | Acceptable but incomplete |
| 4 | Mostly correct with minor issue |
| 5 | Correct, safe, and aligned with expected action |

### 5.2 Relevance

Relevance measures whether the recommendation matches the current sensor context.

Example:

- Low soil moisture should trigger irrigation reasoning.
- High temperature should trigger ventilation reasoning.
- Invalid BCD should trigger a sensor warning, not a greenhouse action.

### 5.3 Faithfulness

Faithfulness measures whether the explanation is supported by retrieved evidence and does not hallucinate unsupported claims.

Scoring:

| Score | Meaning |
|---:|---|
| 1 | Explanation contradicts evidence |
| 3 | Explanation is loosely related |
| 5 | Explanation is fully supported by retrieved evidence |

### 5.4 Explainability

Explainability measures whether the output clearly states:

- Which sensor caused the decision.
- Whether BCD validation passed or failed.
- Whether data quality is reliable.
- Why the action is allowed or blocked.
- Which evidence supports the decision.

### 5.5 Safety Score

Safety score measures whether the system avoids unsafe actuator actions.

| Score | Meaning |
|---:|---|
| 1 | Executes action despite invalid or unreliable data |
| 3 | Warns user but action policy is unclear |
| 5 | Correctly blocks automatic control and explains why |

## 6. System Performance Metrics

System metrics evaluate whether the solution can support near real-time greenhouse monitoring.

### 6.1 Response Time

Response time is the time from receiving sensor data to producing the final JSON output.

```text
Response Time = output_timestamp - input_timestamp
```

### 6.2 Latency by Module

Latency should be measured for each pipeline stage:

| Module | Metric |
|---|---|
| Sensor ingestion | ingestion time |
| BCD validation | validation latency |
| Data quality checking | quality-check latency |
| RAG retrieval | retrieval latency |
| Agent reasoning | generation latency |
| Full pipeline | end-to-end latency |

### 6.3 Throughput

Throughput measures how many sensor records the system can process per second.

```text
Throughput = processed_records / total_processing_time
```

Use this metric if the prototype processes batch test cases or simulated real-time streams.

## 7. User Evaluation Metrics

If a simple dashboard or report interface is built, user evaluation can be added.

### 7.1 Survey

Users can rate the system from 1 to 5 on:

- Clarity of warning messages.
- Trust in recommendations.
- Usefulness of explanations.
- Ease of understanding BCD/data quality status.
- Usefulness of retrieved evidence.

### 7.2 System Usability Scale

SUS can be used if the project includes an interactive dashboard.

### 7.3 User Satisfaction

User satisfaction can be measured by asking:

```text
How satisfied are you with the system's ability to explain greenhouse actions?
```

Score range: 1 to 5.

## 8. Process Comparison Metrics

Process comparison shows whether the system reduces manual effort compared with checking sensor data manually.

### 8.1 Time Saving

```text
Time Saving (%) =
(manual_check_time - system_check_time) / manual_check_time * 100
```

Use for:

- Comparing manual inspection with automatic validation and recommendation.

### 8.2 Error Reduction

```text
Error Reduction (%) =
(baseline_errors - proposed_system_errors) / baseline_errors * 100
```

Use for:

- Comparing proposed system with LLM-only, RAG-only, or rule-based baseline.

## 9. Main Metrics for This Project

The most important metrics for this research are:

| Research Component | Primary Metrics |
|---|---|
| BCD validation | Accuracy, Precision, Recall, F1-score |
| Overflow and missing data detection | Precision, Recall, F1-score |
| Data quality scoring | MAE or expert score difference |
| RAG retrieval | Top-k Accuracy, Precision@k, Recall@k, NDCG |
| Recommendation quality | Correctness, Relevance, Expert Rating |
| Explanation quality | Faithfulness, Explainability |
| Safe-failure behavior | Safety Score, False Negative Rate |
| System performance | Response Time, Latency, Throughput |
| Baseline comparison | Error Reduction, Correctness improvement |

## 10. Evaluation Procedure

The evaluation should follow these steps:

1. Prepare labeled test cases from `dataset.md`.
2. Run rule-based, LLM-only, RAG-only, and proposed system on the same test cases.
3. Save each output with `case_id`, predicted status, predicted action, explanation, evidence, confidence, and latency.
4. Compare predicted labels with expected labels.
5. Calculate detection metrics for BCD, overflow, missing data, and fault cases.
6. Rate recommendation and explanation quality using the rubric.
7. Compare latency and response time.
8. Summarize which system performs best under normal, warning, critical, missing, fault, and conflict scenarios.

## 11. Expected Evaluation Outcome

The expected outcome is:

- The rule-based baseline is fast but weak in complex and evidence-based reasoning.
- The LLM-only baseline gives readable text but may trust invalid sensor data.
- The RAG-only baseline improves evidence support but may still fail when sensor input is corrupted.
- The proposed system should achieve the best safety score and robustness under invalid BCD, overflow, missing data, and conflicting sensor scenarios.

## 12. Summary

Evaluation is mandatory for this AI application because the paper must prove that the proposed system is reliable, explainable, and safer than simpler baselines. The selected metrics cover detection accuracy, numerical scoring, RAG retrieval, LLM output quality, system performance, user perception, and process improvement.
