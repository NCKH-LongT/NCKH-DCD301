# Báo cáo Tiến độ Tuần 01

- **Lớp:** SE1930
- **Nhóm:** G07
- **Đề tài:** A Data Quality-Aware Agentic RAG Framework for Real-Time AIoT Decision Support in Smart Greenhouse

---

## 1. Tuần này nhóm đã làm gì?
Trong tuần đầu tiên của dự án DCD, nhóm đã thực hiện các công việc nền tảng sau:
- **Thảo luận và Chốt đề tài:** Lựa chọn tên đề tài tập trung vào lĩnh vực **Smart Greenhouse Control System** và đăng ký thành công nhánh Git **`SE1930_G07`** để quản lý mã nguồn độc lập.
- **Xác lập Cấu trúc Thư mục chuẩn:** Thiết lập thành công cấu trúc thư mục nghiên cứu 16 tuần từ `01_topic_proposal` đến `weekly_reports` và đẩy thành công lên nhánh Git nhóm.
- **Nghiên cứu & Giải quyết 4 RQ lý thuyết:** Tìm hiểu, phân biệt sự khác nhau giữa mạch tổ hợp và mạch tuần tự, giải thích sâu sắc về vai trò của Latch/Flip-Flop trong việc quản lý trạng thái của mô hình nông nghiệp thông minh.
- **Xây dựng Bảng Sensor-Action & JSON Schema:** Thiết kế sơ bộ các sensor đo đạc, actuator điều khiển và thiết kế cấu trúc dữ liệu JSON Output tuân thủ 100% hướng dẫn môn học (có đủ `status`, `action`, `confidence`, `evidence`).

---

## 2. Output cụ thể là file/code/bảng nào?
Các kết quả của nhóm đã được sắp xếp khoa học và push lên nhánh `SE1930_G07`:
1. **[topic_proposal.md](file:///d:/STUDY/KY7/DCD/repo%20cua%20thay/01_topic_proposal/topic_proposal.md):** Đề xuất đề tài nghiên cứu chi tiết, mục tiêu và đặt vấn đề.
2. **[domain_scope.md](file:///d:/STUDY/KY7/DCD/repo%20cua%20thay/01_topic_proposal/domain_scope.md):** Phạm vi lĩnh vực nghiên cứu (Greenhouse), các trạng thái FSM và đầu vào đầu ra.
3. **[sensor_action_table.md](file:///d:/STUDY/KY7/DCD/repo%20cua%20thay/01_topic_proposal/sensor_action_table.md):** Bảng sensor - action chi tiết kèm theo phân tích các kịch bản lỗi Data Quality (Conflict/Fault).
4. **[rq_explanation.md](file:///d:/STUDY/KY7/DCD/repo%20cua%20thay/01_topic_proposal/rq_explanation.md):** Báo cáo giải đáp chi tiết 4 Research Questions lý thuyết về mạch tuần tự (RQ-09, RQ9.1, RQ9.2, RQ9.3).
5. **[system_output_schema.json](file:///d:/STUDY/KY7/DCD/repo%20cua%20thay/01_topic_proposal/system_output_schema.json):** File JSON Schema chuẩn hóa cho dữ liệu xuất ra của AgriAgent.
6. **[paper_list.md](file:///d:/STUDY/KY7/DCD/repo%20cua%20thay/02_related_work/paper_list.md):** Khởi tạo danh mục tài liệu tham khảo chính phục vụ cho RAG Pipeline và Literature Review.

---

## 3. Output đó trả lời RQ nào?
- File **`rq_explanation.md`** trực tiếp giải quyết và trả lời đầy đủ các câu hỏi lý thuyết: **RQ-09**, **RQ9.1**, **RQ9.2**, và **RQ9.3** về Mạch tuần tự cơ bản.
- Các file **`domain_scope.md`**, **`sensor_action_table.md`**, và **`system_output_schema.json`** tạo tiền đề giải quyết **RQ1** (Tích hợp sensor và giải thích quyết định) và **RQ2** (Ảnh hưởng của chất lượng dữ liệu sensor).

---

## 4. Kết quả hiện tại có vấn đề gì?
- Về mặt lý thuyết và cấu trúc dữ liệu: Nhóm đã chốt rất vững vàng và không gặp vướng mắc lớn.
- Về mặt kỹ thuật: Cần chuẩn bị cài đặt thư viện cho RAG và Data Ingestion (FastAPI, ChromaDB, Docling) cho các tuần tiếp theo.

---

## 5. Tuần sau nhóm sẽ làm gì?
Trong tuần tiếp theo (Tuần 2), nhóm sẽ tập trung vào **Literature Review** (Tổng quan tài liệu học thuật):
- Thu thập thêm ít nhất 5-10 tài liệu/bài báo uy tín về Smart Agriculture và Data Quality.
- Hoàn thiện bảng ma trận tổng quan tài liệu (`literature_review_matrix.md`).
- Xác định rõ khoảng trống nghiên cứu (`research_gap.md`) và đóng góp đóng khung của nhóm.

---

## 6. Nhóm cần giảng viên hỗ trợ gì?
- Mong thầy xem xét và góp ý sơ bộ về **Đề tài đề xuất** và **JSON Output Schema** xem đã tối ưu và đúng hướng nghiên cứu mà thầy kỳ vọng chưa để nhóm an tâm triển khai code trong các tuần tiếp theo.
