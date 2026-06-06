# RAG Query Test Results - Week 4

**Người thực hiện:** Quý Đam  
**Ngày:** 2026-06-04  
**Mode:** Mock (chưa có vector DB thật từ Huy)

---

## 📊 Tổng quan

| Metric | Giá trị |
|:---|---:|
| Số lượng test queries | 10 |
| Pass rate | **10/10 (100%)** |
| Avg Recall@3 | 0.95 |
| Avg Precision@3 | 0.4667 |
| Avg MRR | 1.0 |
| Avg Relevance Score | 0.5072 |
| Avg Latency | 0.05ms |

---

## 📋 Kết quả chi tiết

### ✅ Normal scenarios (3/3 passed)

| Query | Recall | MRR | Kết quả |
|:---|:---:|:---:|:---:|
| What is the optimal temperature for tomato plants? | 1.00 | 1.00 | ✅ |
| When should I water my plants soil moisture dry | 0.50 | 1.00 | ✅ |
| greenhouse ventilation fan cooling system | 1.00 | 1.00 | ✅ |

### ✅ Warning scenarios (4/4 passed)

| Query | Recall | MRR | Kết quả |
|:---|:---:|:---:|:---:|
| temperature too high in greenhouse what to do | 1.00 | 1.00 | ✅ |
| humidity high fungal disease prevention greenhouse | 1.00 | 1.00 | ✅ |
| light intensity too high shade cloth needed | 1.00 | 1.00 | ✅ |
| low humidity below 30 percent water stress | 1.00 | 1.00 | ✅ |

### ✅ Critical scenarios (2/2 passed)

| Query | Recall | MRR | Kết quả |
|:---|:---:|:---:|:---:|
| extreme heat above 38 degrees greenhouse emergency | 1.00 | 1.00 | ✅ |
| soil moisture above 70 percent waterlogging root rot | 1.00 | 1.00 | ✅ |

### ✅ Fault scenarios (1/1 passed)

| Query | Recall | MRR | Kết quả |
|:---|:---:|:---:|:---:|
| sensor stuck at same value not changing fault | 1.00 | 1.00 | ✅ |

---

## 🔍 Integration Test Results

| Test case | Kết quả |
|:---|---:|
| Sensor data format validation | ✅ PASS |
| RAG query - high temperature | ✅ PASS |
| RAG query - low soil moisture | ✅ PASS |
| RAG query - humidity disease | ✅ PASS |
| Sensor → RAG flow (temp=34.2°C) | ✅ PASS |
| Empty query handling | ✅ PASS |
| Normal sensor scenario | ✅ PASS |

**Tổng: 7/7 passed**

---

## 📌 Ví dụ output RAG query

```
📝 Query: 'temperature too high in greenhouse what to do'
   Found: 3 chunks (0.05ms)

  [1] greenhouse_guidelines.pdf
      Chunk: mock_001
      Score: 1.0000
      Text: Optimal temperature for tomato plants in a greenhouse is between 18-28°C...

  [2] ventilation_guide.pdf
      Chunk: mock_005
      Score: 0.7000
      Text: When greenhouse temperature exceeds 32°C, ventilation fans should be...

  [3] greenhouse_guidelines.pdf
      Chunk: mock_002
      Score: 0.5000
      Text: Relative humidity should be maintained between 40-70%...
```

---

## ⚠️ Ghi chú

- Hiện tại đang chạy với **mock data** (8 chunks về nhà kính)
- Cần **Huy ingest tài liệu thật** vào vector DB để chạy với dữ liệu thực
- Khi có vector DB thật, chỉ cần chạy lại với flag `--mock=false`
