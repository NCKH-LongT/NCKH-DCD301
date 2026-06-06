# Điều khiển khí hậu nhà kính

## Tổng quan

Hệ thống điều khiển khí hậu nhà kính bao gồm:
- Quạt thông gió
- Hệ thống sưởi
- Máy làm mát (cooling pad)
- Hệ thống che nắng tự động

## Ngưỡng điều khiển

### Quạt thông gió
| Nhiệt độ | Hành động |
|----------|-----------|
| < 25°C | Tắt |
| 25-30°C | Bật quạt tốc độ thấp |
| 30-35°C | Bật quạt tốc độ cao |
| > 35°C | Bật quạt + cooling pad |

### Hệ thống sưởi
| Nhiệt độ | Hành động |
|----------|-----------|
| > 18°C | Tắt sưởi |
| 15-18°C | Bật sưởi 50% công suất |
| 10-15°C | Bật sưởi 75% công suất |
| < 10°C | Bật sưởi 100% |

## Độ ẩm không khí

Độ ẩm lý tưởng: 60-80%

| Độ ẩm | Hành động |
|--------|-----------|
| < 50% | Bật hệ thống tưới phun sương |
| 50-60% | Tăng độ ẩm từ từ |
| 60-80% | Lý tưởng |
| 80-90% | Tăng thông gió |
| > 90% | Cảnh báo nguy hiểm |

## CO2 Control

| CO2 (ppm) | Mức độ | Hành động |
|-----------|--------|-----------|
| < 350 | Thấp | Bổ sung CO2 |
| 350-450 | Bình thường | Duy trì |
| 450-800 | Cao | Tăng thông gió |
| > 800 | Nguy hiểm | Thông gió khẩn cấp |

## Best Practices

1. **PID Controller**: Sử dụng PID để điều khiển mượt mà hơn
2. **Hysteresis**: Đặt ngưỡng hysteresis 2-3°C để tránh relay bật tắt liên tục
3. **Backup System**: Luôn có kế hoạch dự phòng khi thiết bị hỏng
4. **Monitoring**: Gửi cảnh báo qua Telegram/Email khi vượt ngưỡng