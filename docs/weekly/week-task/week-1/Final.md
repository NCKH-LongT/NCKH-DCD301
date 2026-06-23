# Final — Phỏng vấn Q&A Nhóm 7 (Week 1)

## Câu hỏi 1: Đề tài nhóm em cụ thể là gì? Tại sao lại chọn miền ứng dụng này?

**Trả lời:**
"Thưa thầy, nhóm em chọn đề tài **Smart Greenhouse Control System** (Nhà kính thông minh). Lý do chọn là vì miền này bám sát yêu cầu Nông nghiệp thông minh của môn học, rất thích hợp để thiết kế máy trạng thái FSM (Mạch tuần tự) để điều khiển tưới tiêu/làm mát, đồng thời môi trường nhà kính khắc nghiệt dễ sinh ra các lỗi cảm biến để nhóm em khai thác module Data Quality (SDQM)."

---

## Câu hỏi 2: Nhóm em làm về Mạch tuần tự cơ bản (Theme 9). Hãy giải thích sự khác biệt giữa mạch tuần tự và mạch tổ hợp? Tại sao lại cần phần tử nhớ như Flip-Flop?

**Trả lời:**
"Thưa thầy, đầu ra của **mạch tổ hợp** chỉ phụ thuộc vào đầu vào hiện tại. Còn **mạch tuần tự** phụ thuộc vào cả đầu vào hiện tại và trạng thái trước đó (lịch sử). Chúng em bắt buộc phải có **Flip-Flop** (nhạy theo cạnh clock) hoặc **Latch** (nhạy theo mức) để làm phần tử nhớ 1-bit lưu trữ trạng thái hiện hành, phản hồi ngược lại đầu vào để hệ thống chuyển trạng thái tiếp theo một cách đồng bộ và an toàn."

**Hỏi thêm (Mealy vs Moore):** "Mealy có đầu ra phụ thuộc cả trạng thái và đầu vào hiện tại. Moore có đầu ra chỉ phụ thuộc vào trạng thái hiện tại. Trong thiết kế nhà kính, tụi em sẽ kết hợp cả hai để tối ưu hóa điều khiển."

---

## Câu hỏi 3: Các sensor và action cụ thể của nhà kính nhóm em sẽ giả lập là gì?

**Trả lời:**
"Chúng em sử dụng **4 loại cảm biến đầu vào**: Nhiệt độ, Độ ẩm không khí, Độ ẩm đất, và Cường độ ánh sáng, cùng một Xung Clock/Timer để đồng bộ FSM. Các hành động điều khiển đầu ra gồm có: **Bật quạt** thông gió (khi quá nóng), **Bật đèn sưởi** (khi quá lạnh), **Bật máy bơm** (khi đất khô), và **Kéo rèm che** (khi nắng gắt)."

---

## Câu hỏi 4: Đầu ra JSON của hệ thống trông như thế nào? Có đúng yêu cầu bắt buộc của thầy không?

**Trả lời:**
"Thưa thầy, cấu trúc đầu ra JSON của tụi em hoàn toàn tuân thủ yêu cầu bắt buộc của thầy. Trong phần control_recommendations, tụi em thiết kế chuẩn hóa chứa đủ 4 thuộc tính:
- **status** (mức độ an toàn: SAFE/WARNING/CRITICAL)
- **action** (hành động cụ thể của actuator)
- **confidence** (độ tin cậy được tính từ chất lượng cảm biến và RAG)
- **evidence** (bằng chứng trích dẫn trực tiếp từ tài liệu nông nghiệp của ChromaDB)."

---

## Câu hỏi 5: Các em định xử lý lỗi chất lượng dữ liệu (Data Quality) như thế nào?

**Trả lời:**
"Chúng em sẽ xây dựng module **SDQM** để đối chiếu chéo các cảm biến (Sensor Fusion). Ví dụ, nếu cảm biến độ ẩm đất báo 0% (cực khô) nhưng cảm biến nhiệt độ báo 20°C và độ ẩm không khí là 95% (trời mưa ẩm), hệ thống sẽ phát hiện ngay sự mâu thuẫn (Data Conflict), giảm điểm tin cậy confidence xuống và không kích hoạt bơm bừa bãi để bảo vệ hệ thống."
