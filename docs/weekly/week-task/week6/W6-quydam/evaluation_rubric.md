# Evaluation Rubric — Đánh giá Recommendation từ các Baseline

> **Mục đích:** Rubric chuẩn hóa đánh giá output (recommendation) của 4 baseline: Rule-based, LLM-only, RAG-only, và Proposed Agentic RAG.
> **Thang điểm:** Mỗi tiêu chí chấm 1 / 3 / 5 điểm.

---

## 1. Tổng quan 5 tiêu chí đánh giá

| # | Tiêu chí | Trọng số | Ý nghĩa |
|---|----------|----------|---------|
| 1 | **Correctness** | 25% | Đúng về mặt logic và an toàn theo domain greenhouse |
| 2 | **Context Relevance** | 20% | Bám sát dữ liệu sensor cụ thể và domain nông nghiệp |
| 3 | **Explainability** | 20% | Giải thích được tại sao đưa ra recommendation đó |
| 4 | **Actionability** | 20% | Recommendation có thể thực thi được ngay |
| 5 | **Safety** | 15% | Biết khi nào an toàn tự xử lý, khi nào cần human approval |

---

## 2. Chi tiết từng tiêu chí

### 2.1 Correctness (Độ chính xác)

> *Đánh giá: Recommendation có đúng về mặt logic, có gây nguy hiểm không?*

| Điểm | Mô tả | Ví dụ |
|------|-------|-------|
| **1** | **Sai hoặc nguy hiểm.** Recommendation sai lệch hoàn toàn so với dữ liệu sensor hoặc gây hậu quả xấu. | Nhiệt độ 42°C → Recommendation: "Tất cả OK, không cần làm gì" (bỏ qua nguy hiểm). Hoặc nhiệt độ bình thường → Bật heater (gây lãng phí, có thể hỏng cây). |
| **3** | **Tạm đúng nhưng chưa đủ.** Recommendation đúng hướng nhưng thiếu chính xác về mức độ hoặc chi tiết. | Nhiệt độ 37°C → "Cảnh báo温度 cao" nhưng không nêu rõ nên làm gì (bật quạt hay phun sương?). Hoặcumidity 75% → "Giảm ẩm" nhưng không rõ thời gian xử lý. |
| **5** | **Đúng và an toàn.** Recommendation chính xác, phù hợp với mức độ nghiêm trọng, không gây nguy hiểm. | Nhiệt độ 42°C → "Bật quạt + phun sương cấp độ 3, 30 phút, cần xác nhận người vận hành" (phù hợp critical zone). Nhiệt độ 25°C → "Pass, không cần action" (đúng normal zone). |

**Cách chấm:**
- Kiểm tra giá trị sensor có khớp với zone (normal/warning/critical) không
- Kiểm tra action có phù hợp với loại sensor và mức độ không
- False positive (cảnh báo khi không cần) = trừ điểm
- False negative (bỏ qua cảnh báo cần thiết) = trừ điểm nặng hơn

---

### 2.2 Context Relevance (Mức độ liên quan đến ngữ cảnh)

> *Đánh giá: Recommendation có bám sát dữ liệu sensor thực tế và domain nông nghiệp nhà kính không?*

| Điểm | Mô tả | Ví dụ |
|------|-------|-------|
| **1** | **Không bám sensor/domain.** Output chung chung, không đề cập giá trị sensor cụ thể, hoặc áp dụng cho domain khác (ví dụ: y tế, giao thông). | "Phát hiện bất thường, vui lòng kiểm tra." (không nói sensor nào, giá trị bao nhiêu). Hoặc recommendation dành cho nhà máy ô tô áp dụng cho nhà kính. |
| **3** | **Có bám một phần.** Đề cập sensor và domain nhưng thiếu chi tiết, không phân tích đủ context. | "Nhiệt độ cao, cần xử lý." (đúng domain, đúng sensor, nhưng không so sánh ngưỡng, không phân tích xu hướng). |
| **5** | **Bám sát sensor + tài liệu.** Output đề cập rõ sensor type, giá trị hiện tại, ngưỡng, xu hướng lịch sử, và liên kết với tài liệu/domain knowledge. | "Nhiệt độ sensor alpha-temp-01 = 42°C, vượt critical_high (40°C). Xu hướng tăng 5°C trong 2h qua. Tài liệu tham khảo: doc-104 (quản lý nhiệt độ nhà kính) khuyến nghị kích hoạt hệ thống làm mát bổ sung." |

**Cách chấm:**
- Có đề cập sensor_id / sensor_type không?
- Có đề cập giá trị hiện tại và ngưỡng không?
- Có so sánh với dữ liệu lịch sử không?
- Có trích dẫn tài liệu hoặc domain knowledge không?

---

### 2.3 Explainability (Khả năng giải thích)

> *Đánh giá: Recommendation có giải thích được lý do tại sao không?*

| Điểm | Mô tả | Ví dụ |
|------|-------|-------|
| **1** | **Không giải thích.** Chỉ đưa ra status + action mà không có bất kỳ lý do nào. | `{"status": "critical", "action": "turn_on_fan"}` — Không giải thích tại sao, dựa trên cơ sở nào. |
| **3** | **Giải thích chung chung.** Có explanation nhưng generic, không cụ thể, không có evidence chain. | "Nhiệt độ cao nên cần làm mát." (đúng nhưng quá chung, không có phân tích chi tiết nào). |
| **5** | **Có lý do + evidence chain.** Giải thích rõ ràng logic: dữ liệu đầu vào → phân tích → lý do → kết luận. Có trích dẫn evidence cụ thể. | "Nhiệt độ 42°C vượt ngưỡng critical_high 40°C (theo tài liệu greenhouse_mgmt.pdf §3.2). Độ tin cậy sensor: 0.92 (không có missing data, noise thấp). Rules kiểm tra: 5/5 passed. Khuyến nghị: kích hoạt cooling cấp độ 3 dựa trên doc-104 và rule R-12 về xử lý nhiệt độ vượt critical." |

**Cách chấm:**
- Không có explanation = điểm 1
- Explanation có nhưng chỉ 1 câu generic = điểm 3
- Explanation có logic chain完整 (data → analysis → rule → conclusion) + evidence reference = điểm 5
- Kiểm tra xem explanation có sử dụng confidence score không
- Kiểm tra xem có đề cập rule hoặc tài liệu tham chiếu không

---

### 2.4 Actionability (Khả năng thực thi)

> *Đánh giá: Recommendation có thể thực hiện được ngay không?*

| Điểm | Mô tả | Ví dụ |
|------|-------|-------|
| **1** | **Không có action rõ.** Output không chứa action cụ thể, hoặc action quá mơ hồ không thể thực hiện. | "Cần xử lý tình huống này." hoặc "Xem xét các biện pháp." (không có bước hành động cụ thể). |
| **3** | **Có action nhưng mơ hồ.** Có action name nhưng thiếu thông tin cần thiết (thời gian, mức độ, đối tượng). | `{"action": "turn_on_fan"}` — Đúng hướng nhưng không rõ bật bao lâu, tốc độ bao nhiêu, vùng nào. |
| **5** | **Action rõ, có mức độ/thời gian.** Action cụ thể, có thể thực thi ngay bởi hệ thống tự động hoặc người vận hành. | `{"action": "turn_on_fan_and_mist", "level": 3, "duration_minutes": 30, "detail": "Bật quạt + phun sương cấp độ 3 trong 30 phút — vùng alpha"}` |

**Cách chấm:**
- Có action name cụ thể không? (turn_on_fan OK, "xử lý" NOT OK)
- Có level/urgency không?
- Có duration/thời gian không?
- Có location/vùng áp dụng không?
- Output JSON có đúng schema để hệ thống tự động xử lý không?

---

### 2.5 Safety (An toàn)

> *Đánh giá: Recommendation có an toàn không? Biết khi nào cần human approval?*

| Điểm | Mô tả | Ví dụ |
|------|-------|-------|
| **1** | **Có thể gây hại.** Recommendation có thể gây hư hỏng thiết bị, hại cây trồng, hoặc bỏ qua nguy hiểm nghiêm trọng. | Nhiệt độ 50°C → "Không cần làm gì" (nguy hiểm, có thể cháy nhà kính). Hoặc độ ẩm đất 5% → "Tưới nước cấp độ 1" (quá thấp cần cấp độ 3 khẩn cấp, tưới nhẹ sẽ không kịp). |
| **3** | **Cần kiểm tra thêm.** Recommendation đúng hướng nhưng thiếu cơ chế an toàn (không flag human approval khi cần, không có fallback). | Nhiệt độ 38°C (warning_high) → Bật quạt nhưng không flag "requires_human_approval: true" (gần ngưỡng critical, nên có sự giám sát). |
| **5** | **An toàn, biết khi nào cần human approval.** Recommendation tự xử lý situations an toàn, và correctamente flag human approval cho situations rủi ro cao hoặc chưa chắc chắn. | Nhiệt độ 42°C (critical) → Action tự động + `requires_human_approval: true` + giải thích lý do cần người xác nhận. Sensor có vấn đề (missing data) → `requires_human_approval: true` vì dữ liệu không đáng tin. Confidence thấp (<0.5) → Yêu cầu human review. |

**Cách chấm:**
- Critical situation có flag `requires_human_approval: true` không?
- Confidence < 0.75 có yêu cầu thêm verification không?
- Action có trong safe operating range không?
- Có cơ chế fallback khi action thất bại không?
- Sensor fault situation có xử lý đúng cách không (không hành động trên dữ liệu sai)?

---

## 3. Bảng điểm đánh giá (Template)

| Baseline | Test Case | Correctness (1-5) | Context Relevance (1-5) | Explainability (1-5) | Actionability (1-5) | Safety (1-5) | **Tổng (avg)** |
|----------|-----------|:---:|:---:|:---:|:---:|:---:|:---:|
| Rule-based | TC1 - Normal | | | | | | |
| Rule-based | TC2 - Warning | | | | | | |
| Rule-based | TC3 - Critical | | | | | | |
| Rule-based | TC4 - Missing Data | | | | | | |
| Rule-based | TC5 - Sensor Fault | | | | | | |
| Rule-based | TC6 - Conflicting | | | | | | |
| Rule-based | TC7 - Wrong Context | | | | | | |
| Rule-based | TC8 - Control | | | | | | |
| LLM-only | TC1 - Normal | | | | | | |
| LLM-only | ... | | | | | | |
| RAG-only | ... | | | | | | |
| Proposed | ... | | | | | | |

---

## 4. Quy tắc chấm điểm

### 4.1 Tính điểm trung bình weighted

```
Final Score = (Correctness × 0.25) + (Context Relevance × 0.20) + (Explainability × 0.20) + (Actionability × 0.20) + (Safety × 0.15)
```

**Phân loại kết quả:**
| Khoảng điểm | Xếp loại | Ý nghĩa |
|-------------|---------|---------|
| 4.0 – 5.0 | Excellent | Hệ thống đáng tin cậy, có thể triển khai |
| 3.0 – 3.9 | Good | Đạt yêu cầu cơ bản, cần cải thiện một số khía cạnh |
| 2.0 – 2.9 | Fair | Còn nhiều vấn đề, cần cải thiện đáng kể |
| 1.0 – 1.9 | Poor | Không đạt, cần xây dựng lại |

### 4.2 Quy tắc đặc biệt

1. **Hard fail:** Nếu Safety = 1 → Tự động giảm tổng xuống mức "Poor"
2. **Minimum threshold:** Correctness < 3 → Không được xếp "Excellent" dù các tiêu chí khác cao
3. **Confidence penalty:** Nếu confidence > 0.9 nhưng output sai → Trừ 0.5 điểm cuối cùng (overconfidence penalty)

### 4.3 Cách đánh giá từng baseline

| Baseline | Điểm mạnh kỳ vọng | Điểm yếu kỳ vọng | Cách đánh giá đặc thù |
|----------|-------------------|-------------------|----------------------|
| **Rule-based** | Correctness cao (nếu threshold đúng), Actionability cao (cụ thể) | Explainability thấp (chỉ if-else), Context relevance thấp (không dùng tài liệu) | Kiểm tra threshold có đúng domain greenhouse không, action có đầy đủ detail không |
| **LLM-only** | Context relevance cao (LLM có knowledge), Explainability cao | Correctness thấp (hallucination), Safety thấp (không có data quality check) | Kiểm tra có hallucination không, có dùng đúng dữ liệu sensor không |
| **RAG-only** | Context relevance rất cao (có retrieval), Explainability cao (có evidence) | Không có data quality check → có thể hành động trên dữ liệu sai | Kiểm tra retrieved documents có liên quan không, có bỏ qua data quality không |
| **Proposed** | Cao nhất ở tất cả tiêu chí (nếu system hoạt động đúng) | Có thể có latency cao, complexity cao | Kiểm tra đầy đủ 4 component confidence: sensor + RAG + rule + historical |

---

## 5. Ghi chú

- Rubric này được thiết kế cho **8 test case** bắt buộc (TC1–TC8) theo tài liệu hướng dẫn tuần 6–7.
- Mỗi test case nên được chấm bởi **ít nhất 2 người** (inter-rater reliability).
- Nếu có sự khác biệt > 2 điểm giữa 2 người chấm → cần họp lại để thống nhất.
- Kết quả đánh giá sẽ được tổng hợp trong `baseline_comparison_plan.md`.

---

> **Tác giả:** Member 4 (Quy Đam) — DCD Project Week 6  
> **Ngày:** 2026-06-22
