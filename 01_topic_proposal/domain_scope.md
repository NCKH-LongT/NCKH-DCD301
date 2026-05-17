# 1. Tên Domain
**Smart Greenhouse Control System** (Hệ thống điều khiển nhà kính thông minh).

# 2. Lý do chọn Domain
Domain này được lựa chọn dựa trên 3 tiêu chí cốt lõi của dự án:
- **Tuân thủ Guideline "Smart Agriculture":** Đây là lĩnh vực nông nghiệp thông minh điển hình, bám sát yêu cầu của môn học.
- **Tính ứng dụng của Mạch tuần tự (FSM):** Hoạt động của nhà kính (tưới tiêu, sưởi ấm) không diễn ra tức thời mà cần có bộ nhớ trạng thái và độ trễ thời gian (Timers), là minh chứng sống động cho Mạch tuần tự.
- **Tiềm năng khai thác Data Quality:** Rất dễ xảy ra lỗi cảm biến trong môi trường nông nghiệp (bụi bẩn, độ ẩm cao làm hỏng mạch), tạo ra nhiều test case hấp dẫn (nhiễu, mâu thuẫn dữ liệu).

# 3. Phân tích Mạch tuần tự trong Nhà kính (Liên hệ RQ9)
Hệ thống điều khiển nhà kính không thể chỉ dùng **mạch tổ hợp (Combinational Logic)**. 
*Ví dụ:* Nếu cấu hình "Độ ẩm < 40% thì bật bơm, >= 40% thì tắt", máy bơm sẽ bị bật/tắt liên tục từng giây khi độ ẩm dao động quanh mức 40% (hiện tượng chattering), dẫn đến cháy bơm.

Do đó, hệ thống bắt buộc phải dùng **mạch tuần tự (Sequential Circuit)** có khả năng lưu trữ trạng thái (State):
- **Trạng thái (States):** `IDLE` (Bình thường), `HEATING` (Sưởi ấm), `COOLING` (Làm mát), `WATERING` (Tưới tiêu).
- **Phần tử nhớ (Memory/Flip-Flops):** Khi hệ thống chuyển sang state `WATERING`, một bộ đếm (Timer) cấu tạo từ Flip-flops sẽ được kích hoạt. Bơm sẽ tiếp tục chạy trong đủ 10 phút (Output phụ thuộc vào State hiện hành) bất chấp việc cảm biến có thể báo độ ẩm đã vượt 40% ngay phút thứ 2.

# 4. Input & Output Hệ thống
**Input (Dữ liệu vào từ Sensor):**
```json
{
  "temperature": 35.5,
  "humidity": 60.0,
  "soil_moisture": 30.5,
  "light_lux": 15000
}
```

**Output (Dữ liệu xuất từ Agentic RAG):**
- `current_state`: Trạng thái hệ thống (VD: IDLE).
- `next_state`: Trạng thái cần chuyển tiếp (VD: WATERING).
- `confidence`: Độ tin cậy của cảm biến.
- `explanation`: Giải thích lý do ra quyết định dựa trên FSM và tài liệu nông nghiệp.
