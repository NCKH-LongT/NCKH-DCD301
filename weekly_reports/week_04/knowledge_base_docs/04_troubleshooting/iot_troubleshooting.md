# Xử lý sự cố hệ thống IoT nhà kính

## Vấn đề cảm biến

### Cảm biến không đọc được dữ liệu

| Nguyên nhân | Kiểm tra | Xử lý |
|-------------|----------|--------|
| Cáp bị đứt | Kiểm tra đầu nối | Thay cáp mới |
| Địa chỉ I2C sai | Quét I2C bus | Đặt đúng địa chỉ |
| Cảm biến hỏng | Test với module khác | Thay cảm biến mới |
| Nguồn yếu | Đo điện áp | Cấp nguồn ổn định |

### Đọc sai giá trị

1. **Nhiệt độ cao bất thường**
   - Kiểm tra: Cảm biến có bị ánh nắng trực tiếp?
   - Kiểm tra: Có nguồn nhiệt gần không?
   - Xử lý: Di chuyển cảm biến, thêm che chắn

2. **Độ ẩm đất sai**
   - Nguyên nhân: Cảm biến bị khô
   - Xử lý: Tưới nước quanh cảm biến, đợi ổn định

3. **Giá trị nhảy không ổn định**
   - Kiểm tra: Nhiễu điện từ
   - Kiểm tra: Cáp quá dài
   - Xử lý: Thêm bộ lọc, rút ngắn cáp

## Vấn đề kết nối

### ESP32/Arduino mất kết nối WiFi

1. Kiểm tra RSSI WiFi (nên > -70 dBm)
2. Reset module WiFi
3. Kiểm tra router có bị đầy kết nối không
4. Thử reboot thiết bị

### MQTT broker không nhận message

| Kiểm tra | Cách xử lý |
|----------|-----------|
| Broker đang chạy? | Kiểm tra service |
| Port đúng? | Mặc định 1883, SSL 8883 |
| Authentication? | Kiểm tra username/password |
| Topic đúng? | Verify topic format |

### Database không lưu được

1. Kiểm tra kết nối PostgreSQL
2. Verify schema có đúng không
3. Kiểm tra disk space
4. Xem log lỗi chi tiết

## Cảnh báo (Alert) không gửi được

1. **Telegram bot**
   - Kiểm tra bot token còn valid
   - Verify chat ID
   - Test gửi thủ công

2. **Email**
   - Kiểm tra SMTP settings
   - Verify email recipient
   - Check spam folder

## Best Practices

1. **Monitoring**: Luôn monitor hệ thống 24/7
2. **Alerting**: Đặt ngưỡng hợp lý, không quá nhạy
3. **Backup**: Backup cấu hình định kỳ
4. **Logging**: Ghi log đầy đủ để debug
5. **Update firmware**: Cập nhật định kỳ để fix bugs