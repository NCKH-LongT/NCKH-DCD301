# Week 6 - Baseline Comparison for Agentic RAG System

## 📋 Task Summary

**Objective:** Build 4 baselines to compare against the Proposed Agentic RAG system.

| Baseline | Description | Status |
|----------|-------------|--------|
| Rule-based | If-else threshold logic per sensor | ✅ Complete |
| LLM-only | LLM without RAG support | ✅ Complete |
| RAG-only | RAG without data quality checks | ✅ Complete |
| Proposed Agentic RAG | Full system (data quality + RAG + agent) | ✅ Complete |

---

## 👥 Member Contributions

### Member 1 (Nam) - Rule-based Baseline ✅
- **File:** `code/baselines/baseline_rule_based.py`
- **Description:** Implements if-else threshold logic for 4 sensor types (temperature, humidity, soil_moisture, light)
- **Features:**
  - Configurable thresholds per sensor type
  - JSON output with status, confidence, and recommendations
  - CSV data processing support
  - Human approval flag for critical situations

### Member 2 (Huy) - LLM-only Baseline ✅
- **File:** `code/baselines/baseline_llm_only.md`
- **Description:** LLM prompt template and test results without RAG support
- **Test Cases:**
  1. 4-bit Counter
  2. JK Flip-flop State Machine
  3. Frequency Divider
  4. Bidirectional Shift Register
- **Key Findings:**
  - ✅ Good at understanding natural language requirements
  - ❌ Prone to hallucination in logic equations
  - ❌ No timing verification
  - ❌ Inconsistent between outputs

### Member 3 (Bảo) - RAG-only + Proposed System ✅
- **Files:**
  - `code/baselines/baseline_rag_only.py` - RAG query without data quality
  - `code/baselines/baseline_proposed.py` - Full Proposed Agentic RAG
- **Description:**
  - RAG-only: Retrieves documents but ignores data quality metrics
  - Proposed: Integrates data quality scoring, RAG relevance, rule consistency, and historical stability

### Member 4 (Quy Đam) - Evaluation Rubric + Comparison Plan ⏳
- **Status:** Pending
- **Files to create:**
  - `docs/evaluation_rubric.md`
  - `docs/baseline_comparison_plan.md`

---

## 📊 Progress Status

| Task | Assignee | Status |
|------|----------|--------|
| Rule-based Baseline | Nam | ✅ |
| LLM-only Baseline | Huy | ✅ |
| RAG-only Baseline | Bảo | ✅ |
| Proposed System | Bảo | ✅ |
| Evaluation Rubric | Quy Đam | ⏳ |
| Comparison Plan | Quy Đam | ⏳ |

**Overall Progress:** 4/6 tasks complete (67%)

---

## 📁 File Structure

```
weekly_reports/week_06/
├── week_06.md                          # This file
├── task_assignment_week6.md            # Task assignment with progress
└── code/baselines/
    ├── README.md                       # Baselines overview
    ├── baseline_rule_based.py          # Member 1 - Rule-based
    ├── baseline_llm_only.md            # Member 2 - LLM-only
    ├── baseline_rag_only.py            # Member 3 - RAG-only
    └── baseline_proposed.py            # Member 3 - Proposed
```

---

## 🔗 Related Files

- Task Assignment: `task_assignment_week6.md`
- Week 5 Data Quality: `weekly_reports/week_05/src/data_quality/`
- Week 4 Sample Data: `weekly_reports/week_04/sample_data/`

---

*Last updated: 2026-06-21*
