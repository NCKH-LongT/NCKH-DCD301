# Sensor & Action Table — Smart Greenhouse

## Cảm biến đầu vào (Input Sensors)

| Sensor | Đơn vị | Khoảng đo | Mô tả |
|--------|--------|-----------|-------|
| Nhiệt độ (Temperature) | °C | 0–50 | Đo nhiệt độ không khí trong nhà kính |
| Độ ẩm không khí (Humidity) | % | 0–100 | Đo độ ẩm không khí |
| Độ ẩm đất (Soil Moisture) | % | 0–100 | Đo độ ẩm của đất trồng |
| Cường độ ánh sáng (Light) | lux | 0–100000 | Đo cường độ ánh sáng môi trường |
| Xung Clock / Timer | - | - | Đồng bộ FSM, tạo nhịp cho mạch tuần tự |

## Hành động điều khiển đầu ra (Output Actions / Actuators)

| Actuator | Hành động | Điều kiện kích hoạt |
|----------|-----------|---------------------|
| Quạt thông gió (Fan) | Bật / Tắt | Nhiệt độ > ngưỡng trên (vd: 35°C) |
| Đèn sưởi (Heater) | Bật / Tắt | Nhiệt độ < ngưỡng dưới (vd: 15°C) |
| Máy bơm (Pump) | Bật / Tắt | Độ ẩm đất < ngưỡng khô (vd: 30%) |
| Rèm che (Curtain) | Kéo / Mở | Cường độ ánh sáng > ngưỡng (vd: 50000 lux) |

## Ma trận Sensor → Action

| Sensor \ Action | Quạt | Đèn sưởi | Bơm | Rèm che |
|-----------------|------|----------|-----|---------|
| Nhiệt độ | ✅ | ✅ | ❌ | ❌ |
| Độ ẩm không khí | ✅ | ❌ | ❌ | ❌ |
| Độ ẩm đất | ❌ | ❌ | ✅ | ❌ |
| Ánh sáng | ❌ | ❌ | ❌ | ✅ |

## Trạng thái FSM (Finite State Machine)

| State | Mô tả | Hành động |
|-------|-------|-----------|
| IDLE | Bình thường, không action | Theo dõi sensor |
| COOLING | Đang làm mát | Bật quạt |
| HEATING | Đang sưởi ấm | Bật đèn sưởi |
| WATERING | Đang tưới | Bật máy bơm |
| SHADING | Đang che nắng | Kéo rèm |
