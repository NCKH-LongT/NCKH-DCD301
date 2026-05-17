# Đề xuất Đề tài Nghiên cứu (Research Topic Proposal)

- **Tên lớp:** SE1930
- **Nhóm:** G07
- **Tên Đề tài Đề xuất:** *A Data Quality-Aware Agentic RAG Framework for Real-Time AIoT Decision Support in Smart Greenhouse*
- **Research Theme:** Research Theme 9 - Mạch tuần tự cơ bản

---

## 1. Đặt vấn đề & Mục tiêu Nghiên cứu (Introduction & Motivation)

Trong canh tác nông nghiệp công nghệ cao, đặc biệt là mô hình **Nhà kính thông minh (Smart Greenhouse)**, việc ra quyết định điều khiển (tưới tiêu, thông gió, sưởi ấm) dựa trên dữ liệu cảm biến IoT thời gian thực đóng vai trò sống còn. 

Tuy nhiên, hệ thống điều khiển thực tế đối mặt với 2 thách thức lớn:
1. **Lỗi chất lượng dữ liệu cảm biến (Data Quality Issues):** Các cảm biến hoạt động trong môi trường khắc nghiệt (nhiệt độ cao, bụi bẩn, nước) dễ bị hỏng, báo sai số, mất kết nối hoặc trả về dữ liệu mâu thuẫn (ví dụ cảm biến độ ẩm đất báo 0% nhưng nhiệt độ mát mẻ và độ ẩm không khí rất cao).
2. **Hạn chế của điều khiển tức thời (Combinational Logic):** Nếu hệ thống chỉ bật/tắt thiết bị dựa trên ngưỡng tức thời (ví dụ: Độ ẩm < 40% bật bơm, >= 40% tắt bơm), rơ-le điều khiển sẽ bị dao động liên tục (chattering) gây cháy hỏng thiết bị.

**Mục tiêu nghiên cứu:**
Xây dựng một hệ thống **AgriAgent** tích hợp mô hình **Mạch tuần tự (FSM)** có khả năng lưu trữ trạng thái lịch sử kết hợp với **Agentic RAG** (được cung cấp tri thức nông nghiệp chuẩn từ tài liệu quốc gia) và **SDQM (Sensor Data Quality Module)** để đưa ra các quyết định điều khiển tối ưu, tự động phát hiện/xử lý lỗi cảm biến, và giải thích được lý do ra quyết định.

---

## 2. Phạm vi Lĩnh vực Nghiên cứu (Domain & Scope)
Nhóm lựa chọn lĩnh vực **Smart Greenhouse Control System** (Hệ thống điều khiển nhà kính thông minh) tập trung vào các khía cạnh:
- **Đầu vào (Telemetry Input):** Nhiệt độ, độ ẩm không khí, độ ẩm đất, cường độ ánh sáng.
- **Trạng thái hệ thống (Sequential States):** `IDLE`, `COOLING`, `HEATING`, `WATERING`.
- **Hành động điều khiển (Actuator Control):** Máy bơm nước tưới nhỏ giọt, quạt thông gió, đèn sưởi ấm, rèm che nắng.
- **Data Quality:** Khử nhiễu, xử lý dữ liệu khuyết thiếu, phát hiện mâu thuẫn cảm biến bằng phương pháp đối chiếu chéo (Sensor Fusion).

*Chi tiết xem tại:* [domain_scope.md](file:///d:/STUDY/KY7/DCD/repo%20cua%20thay/01_topic_proposal/domain_scope.md)

---

## 3. Câu hỏi Nghiên cứu (Research Questions)
Nhóm tập trung giải quyết các câu hỏi nghiên cứu nền tảng về mạch số tuần tự và tính ứng dụng thực tiễn của nó trong mô hình AIoT:

1. **RQ-09:** Phân biệt mạch tổ hợp và mạch tuần tự. Vì sao mạch tuần tự cần phần tử nhớ như latch hoặc flip-flop?
2. **RQ9.1:** Output của mạch tổ hợp phụ thuộc vào những yếu tố nào?
3. **RQ9.2:** Output của mạch tuần tự phụ thuộc vào input hiện tại và trạng thái trước đó như thế nào?
4. **RQ9.3:** Latch và Flip-Flop đóng vai trò gì trong việc lưu trữ trạng thái của mạch tuần tự?

*Chi tiết lời giải đáp xem tại:* [rq_explanation.md](file:///d:/STUDY/KY7/DCD/repo%20cua%20thay/01_topic_proposal/rq_explanation.md)

---

## 4. Mô hình Đầu ra của Hệ thống (JSON Output Design)
Hệ thống cung cấp kết quả đầu ra chuẩn hóa dưới dạng JSON, bảo đảm tuân thủ 100% yêu cầu về mặt dữ liệu của giảng viên bao gồm 4 thuộc tính bắt buộc: `status`, `action`, `confidence`, và `evidence`.

*Chi tiết thiết kế cấu trúc Schema xem tại:* [system_output_schema.json](file:///d:/STUDY/KY7/DCD/repo%20cua%20thay/01_topic_proposal/system_output_schema.json)
