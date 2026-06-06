# RAG Evaluation Report - Week 4

**Người thực hiện:** Quý Đam  
**Ngày:** 2026-06-04  
**Mode:** Mock data (chờ Huy ingest tài liệu thật)

---

## 1. Phương pháp đánh giá

### 1.1. Metrics

| Metric | Công thức | Ý nghĩa |
|:---|---:|---|
| **Recall@k** | \|relevant ∩ retrieved\| / \|relevant\| | Tỷ lệ tài liệu liên quan được tìm thấy |
| **Precision@k** | \|relevant ∩ retrieved\| / k | Độ chính xác trong top-k |
| **MRR** | 1 / rank_of_first_relevant | Thứ hạng trung bình của kết quả đúng đầu tiên |
| **Relevance Score** | similarity(query, chunk) | Độ tương tự giữa query và chunk |
| **Latency** | response_time (ms) | Thời gian phản hồi |

### 1.2. Test queries

10 câu hỏi mẫu được chia thành 4 nhóm:
- **normal** (3): hỏi về điều kiện bình thường
- **warning** (4): hỏi về điều kiện sắp nguy hiểm
- **critical** (2): hỏi về điều kiện nguy hiểm
- **fault** (1): hỏi về lỗi sensor

---

## 2. Kết quả

### 2.1. Tổng hợp

| Metric | Kết quả | Đánh giá |
|:---|---:|:---:|
| Pass rate | **10/10 (100%)** | 🟢 Xuất sắc |
| Avg Recall@3 | **0.95** | 🟢 Rất tốt |
| Avg Precision@3 | **0.4667** | 🟡 Trung bình (kỳ vọng với mock data) |
| Avg MRR | **1.0** | 🟢 Luôn có kết quả đúng ở vị trí #1 |
| Avg Relevance Score | **0.5072** | 🟡 Có thể cải thiện với embedding thật |
| Avg Latency | **0.05ms** | 🟢 Cực nhanh (mock, không có network) |

### 2.2. Theo nhóm kịch bản

| Category | Count | Avg Recall | Avg MRR | Pass Rate |
|:---|:---:|:---:|:---:|:---:|
| normal | 3 | 0.8333 | 1.0 | 3/3 |
| warning | 4 | 1.0 | 1.0 | 4/4 |
| critical | 2 | 1.0 | 1.0 | 2/2 |
| fault | 1 | 1.0 | 1.0 | 1/1 |

---

## 3. Phân tích

### 3.1. Điểm mạnh
- ✅ **MRR = 1.0**: Chứng tỏ với mock data, chunk liên quan nhất luôn được xếp hạng #1
- ✅ **Pass rate 100%**: Tất cả queries đều trả về đúng chủ đề kỳ vọng
- ✅ **Latency rất thấp**: 0.05ms (do dùng keyword matching, không cần GPU)
- ✅ **Phát hiện đúng chủ đề**: Cả 4 category (normal/warning/critical/fault) đều cho recall cao

### 3.2. Điểm cần cải thiện
- ⚠️ **Precision@3 chỉ 0.4667**: Do mock data chỉ có 8 chunks, keyword overlap dễ xảy ra
- ⚠️ **Relevance score trung bình 0.5072**: Sẽ cải thiện khi dùng sentence-transformers thật
- ⚠️ **Chỉ dùng keyword matching**: Chưa có embedding thực sự, cần Huy ingest tài liệu

### 3.3. Khi chuyển sang vector DB thật
Khi Huy hoàn thành `rag_ingest.py` với tài liệu thật:
1. **Sentence-transformers** sẽ tạo embedding chất lượng hơn → relevance score tăng
2. **Vector search** (cosine similarity) sẽ thay thế keyword matching
3. **Precision@k** sẽ cải thiện nhờ corpora lớn hơn
4. **Latency** sẽ tăng lên ~50-200ms (chấp nhận được)

---

## 4. Kết luận

Hệ thống RAG Query API đã sẵn sàng với mock data:
- ✅ Code hoàn chỉnh, chạy được
- ✅ API endpoints hoạt động
- ✅ Evaluation metrics đo được
- ✅ Integration test với sensor API passed

**Cần chờ Huy** để:
- [ ] Ingest tài liệu thật → vector DB
- [ ] Chạy lại evaluation với dữ liệu thật
- [ ] So sánh metrics giữa mock vs real
