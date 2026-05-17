# Bảng Sensor - Action (Nhà kính thông minh)

Bảng dưới đây mô tả các đầu vào (Sensor/Input), ý nghĩa của chúng, và các hành động (Action) tương ứng mà hệ thống điều khiển nhà kính (FSM) sẽ thực hiện.

| Sensor/Input | Ý nghĩa (Đo lường) | Tín hiệu bất thường | Hành động (Action / Next State) |
|---|---|---|---|
| **Nhiệt độ (Temperature)** | Đo độ C môi trường | Quá nóng / Quá lạnh | Chuyển sang State `COOLING` (Bật quạt/phun sương) hoặc `HEATING` (Bật đèn sưởi). |
| **Độ ẩm không khí (Humidity)** | Đo % hơi nước trong không khí | Quá khô / Quá ẩm | Kết hợp với nhiệt độ để điều chỉnh máy phun sương hoặc tăng cường thông gió. |
| **Độ ẩm đất (Soil Moisture)** | Đo % nước trong đất | Đất khô hạn (< ngưỡng) | Chuyển sang State `WATERING` (Bật máy bơm tưới nhỏ giọt). |
| **Ánh sáng (Light)** | Đo cường độ sáng (Lux) | Thiếu nắng / Nắng gắt | Bật hệ thống đèn quang hợp nhân tạo hoặc Kéo rèm che nắng. |
| **Bộ đếm (Timer Clock)** | Xung nhịp thời gian mạch tuần tự | (Hỗ trợ chống nhiễu) | Không cho phép đổi trạng thái liên tục. Giữ nguyên State hiện tại cho đến khi Timer đếm xong chu kỳ an toàn. |

## Mối liên hệ với Data Quality Module
Hệ thống sẽ đối chiếu chéo các sensor (Sensor Fusion) để phát hiện lỗi trước khi ra quyết định:
- **Conflict Data (Mâu thuẫn):** Cảm biến độ ẩm đất báo 0% (khô nứt nẻ) nhưng cảm biến nhiệt độ báo 20°C và độ ẩm không khí 95% (đang mưa lạnh). -> *Agent nghi ngờ lỗi cảm biến đất.*
- **Fault/Missing:** Cảm biến ánh sáng luôn trả về 0 Lux vào giữa trưa (lỗi đứt cáp). -> *Bỏ qua dữ liệu ánh sáng, giữ nguyên rèm che.*
