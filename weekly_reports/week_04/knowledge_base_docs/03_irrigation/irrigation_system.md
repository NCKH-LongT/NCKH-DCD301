# Hệ thống tưới tiêu tự động

## Giới thiệu

Hệ thống tưới tiêu tự động cho nhà kính bao gồm:
- Cảm biến độ ẩm đất
- Van điện từ
- Bơm nước
- Điều khiển tưới nhỏ giọt/phun mưa

## Ngưỡng độ ẩm đất

| Loại cây | Độ ẩm tối ưu | Tưới khi |
|----------|-------------|----------|
| Rau ăn lá | 60-70% | < 60% |
| Cây cà chua | 65-75% | < 65% |
| Ớt | 55-65% | < 55% |
| Dưa leo | 70-80% | < 70% |

## Chế độ tưới

### Tưới nhỏ giọt (Drip)
- Lưu lượng: 1-4 L/giờ/cây
- Thời gian: 15-30 phút/lần
- Tần suất: 2-4 lần/ngày (tùy điều kiện thời tiết)

### Tưới phun mưa
- Lưu lượng: 5-15 L/phút
- Thời gian: 10-20 phút/lần
- Tần suất: 1-2 lần/ngày

## Cảm biến độ ẩm đất Capacitive

| Thông số | Giá trị |
|----------|---------|
| Điện áp | 3.3V - 5V |
| Output | Analog (0-3.3V) |
| Phạm vi đo | 0-100% |
| Độ phân giải | 0.1% |

## Lập trình điều khiển

```python
# Ví dụ điều khiển tưới
def should_water(soil_moisture, target_moisture=60):
    return soil_moisture < target_moisture

def water_cycle(duration_minutes=15):
    print(f"Tưới trong {duration_minutes} phút")
    # Mở van, bật bơm
    time.sleep(duration_minutes * 60)
    # Đóng van, tắt bơm
```

## Lưu ý quan trọng

1. **Chất lượng nước**: Kiểm tra pH và EC định kỳ
2. **Thời gian tưới**: Tưới vào sáng sớm hoặc chiều tối
3. **Tránh tưới lá**: Tưới gốc để phòng bệnh nấm
4. **Drainage**: Đảm bảo thoát nước tốt, tránh úng