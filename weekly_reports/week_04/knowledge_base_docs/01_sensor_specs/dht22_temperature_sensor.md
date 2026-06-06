# Cảm biến nhiệt độ DHT22

## Thông số kỹ thuật

| Thông số | Giá trị |
|----------|---------|
| Điện áp | 3.3V - 5V |
| Phạm vi đo nhiệt độ | -40°C to 80°C |
| Độ chính xác | ±0.5°C |
| Phạm vi đo độ ẩm | 0-100% RH |
| Độ chính xác độ ẩm | ±2% RH |

## Ngưỡng cảnh báo cho nhà kính

| Thông số | Bình thường | Cảnh báo | Nguy hiểm |
|----------|------------|----------|-----------|
| Nhiệt độ ban ngày | 22-28°C | 28-32°C | >32°C |
| Nhiệt độ ban đêm | 16-20°C | 14-16°C | <14°C |
| Độ ẩm | 60-80% | 80-90% | >90% |

## Cách sử dụng với Arduino/Raspberry Pi

```python
import Adafruit_DHT

sensor = Adafruit_DHT.DHT22
pin = 4

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
```

## Lưu ý khi lắp đặt

1. Đặt cảm biến tránh ánh nắng trực tiếp
2. Độ cao tối ưu: 1.2-1.5m từ mặt đất
3. Khoảng cách đến nguồn nhiệt: tối thiểu 50cm
4. Vệ sinh cảm biến định kỳ 3 tháng/lần