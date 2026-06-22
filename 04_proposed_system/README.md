# 04_proposed_system

Folder này chứa **hệ thống đề xuất** (Tuần 3 + 5).

## Cấu trúc

```
04_proposed_system/
├── src/
│   ├── agent/
│   │   └── agent_workflow.py          ✅ LangGraph agent
│   ├── data_quality/
│   │   ├── checker.py                 ✅ Data quality checker
│   │   ├── missing_data.py            ✅
│   │   ├── outlier.py                 ✅
│   │   ├── sensor_drift.py            ✅
│   │   ├── sensor_stuck.py            ✅
│   │   └── timestamp_delay.py         ✅
│   └── rag/
│       └── rag_client.py              ✅ RAG client
├── ai_model_integration.md            ❌ Chưa có
├── data_flow.md                       🔶 Có trong product_overview.md (Mermaid)
├── system_architecture.md             🔶 Có trong product_overview.md (Mermaid)
├── system_overview.md                 🔶 Có trong product_overview.md
└── diagrams/                          🔶 Cần export Mermaid → PNG/DrawIO
```

## Trạng thái hiện tại

| File yêu cầu | Trạng thái |
|---|---|
| `src/agent/agent_workflow.py` | ✅ Có |
| `src/data_quality/*.py` (6 files) | ✅ Có đủ |
| `src/rag/rag_client.py` | ✅ Có |
| `system_architecture.md` | 🔶 Nội dung nằm trong `docs/project/product_overview.md` (Mermaid) |
| `data_flow.md` | 🔶 Nội dung nằm trong `docs/project/product_overview.md` (sequence diagram) |
| `ai_model_integration.md` | ❌ Chưa có |
| `diagrams/` | 🔶 Trống (cần export từ Mermaid) |

## Hành động cần làm

1. Tách nội dung từ `docs/project/product_overview.md` ra thành:
   - `system_architecture.md` (Mermaid diagram + giải thích)
   - `data_flow.md` (sequence diagram)
   - `system_overview.md` (tổng quan)
2. Export Mermaid diagram sang file PNG và lưu vào `diagrams/`
3. Viết `ai_model_integration.md` mô tả cách LLM, embedding, vector DB tích hợp
