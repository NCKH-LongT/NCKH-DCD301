# 📊 Báo Cáo Tiến Độ Tuần 2

> **Tuần:** 2 / 8  
> **Thời gian:** [Ngày bắt đầu] - [Ngày kết thúc]  
> **Trạng thái:** ✅ **ĐÃ HOÀN THÀNH**

---

## 1. Tuần này nhóm đã làm gì?

Tuần 2 tập trung vào **Literature Review và Gap Analysis** theo yêu cầu của đề tài. Các công việc đã thực hiện:

- Đọc và phân tích 3-5 bài báo liên quan đến các chủ đề:
  - IoT/AIoT trong Smart Agriculture
  - RAG/LLM cho Decision Support
  - Sensor Data Quality và Anomaly Detection
  - Smart Greenhouse domain
- Phân loại bài báo theo nhóm và tạo Literature Review Matrix
- Xác định Research Gap - khoảng trống nghiên cứu mà đề tài sẽ giải quyết
- Chốt Contribution của đề tài so với các công trình hiện có

---

## 2. Output cụ thể là file/code/bảng nào?

| File | Nội dung | Trạng thái |
|------|----------|------------|
| `drafts/literature_review_matrix.md` | Bảng tổng hợp các bài báo đã đọc | ✅ Hoàn thành |
| `drafts/research_gap.md` | Phân tích khoảng trống nghiên cứu | ✅ Hoàn thành |
| `drafts/related_work_summary.md` | Tóm tắt các nhóm bài liên quan | ✅ Hoàn thành |
| `drafts/contribution.md` | Các contribution dự kiến của đề tài | ✅ Hoàn thành |

---

## 3. Output đó trả lời RQ nào?

Tuần 2 chuẩn bị nền tảng cho **tất cả 4 Research Questions**:

| RQ | Mối liên hệ với output tuần 2 |
|----|------------------------------|
| **RQ1** | Hiểu cách các công trình hiện tại tích hợp IoT + AI, từ đó thiết kế giải pháp RAG phù hợp |
| **RQ2** | Nghiên cứu các phương pháp đánh giá data quality trong bài báo liên quan |
| **RQ3** | So sánh các baseline (rule-based, LLM-only) từ literature để thiết kế evaluation |
| **RQ4** | Xác định các scenario test phổ biến trong nghiên cứu AIoT |

---

## 4. Kết quả hiện tại có vấn đề gì?

### ✅ Điểm tốt:
- Đã xác định rõ Research Gap: Thiếu framework tích hợp **Data Quality-Aware** vào **Agentic RAG** cho Smart Agriculture
- Đã chốt được 3 baseline cần so sánh: Rule-based, LLM-only, RAG-only
- Đã xác định domain cụ thể: **Smart Greenhouse**

### ⚠️ Vấn đề cần lưu ý:
- Cần đảm bảo các bài báo chọn đọc có chất lượng (venue tốt, gần đây)
- Cần liên kết rõ ràng hơn giữa Gap và Contribution cụ thể

---

## 5. Tuần sau nhóm sẽ làm gì?

**Tuần 3: Thiết kế kiến trúc và dữ liệu**

| Task | Output | Người phụ trách |
|------|--------|-----------------|
| Vẽ sơ đồ kiến trúc hệ thống | `architecture.png` | TV1 |
| Vẽ luồng dữ liệu | `data_flow.png` | TV2 |
| Thiết kế database schema | `database_schema.md` | TV2 |
| Thiết kế API spec | `api_spec.md` | TV3 |
| Thiết kế output JSON schema | `api_spec.md` (phần output) | TV3 |
| Thiết kế kế hoạch test case | `testcase_plan.md` | TV4 |

---

## 6. Nhóm cần giảng viên hỗ trợ gì?

- [ ] Review và góp ý về Research Gap đã xác định
- [ ] Xác nhận các baseline chọn so sánh có phù hợp không
- [ ] Góp ý về công nghệ nên dùng cho tuần 3 (FastAPI vs Node.js, PostgreSQL vs MongoDB, v.v.)

---

## 📋 Checklist Tuần 2 (Theo Guidelines)

- [x] Mỗi sinh viên đã đọc ít nhất 3 bài
- [x] Có matrix tổng hợp
- [x] Có gap rõ
- [x] Có contribution rõ
- [x] Biết bài của mình khác gì bài cũ

---

## 📝 Ghi chú bổ sung

- Domain đã chốt: **Smart Greenhouse**
- Sensor: Nhiệt độ, Độ ẩm không khí, Độ ẩm đất, Ánh sáng
- Action: Bật quạt, Tưới nước, Bật đèn, Cảnh báo
- Trạng thái FSM: Idle → Heating → Cooling → Watering