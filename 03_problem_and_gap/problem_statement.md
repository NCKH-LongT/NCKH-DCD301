# Problem Statement

## 1. Vấn đề thực tế

Các nhà bán lẻ phải đối mặt cùng lúc với hai rủi ro ngược chiều:

- **Hết hàng (stockout):** mất doanh thu và khách hàng.
- **Tồn kho dư thừa (overstock):** tốn chi phí lưu kho, đọng vốn, hàng phải giảm giá hoặc xử lý.

Khó khăn này tăng lên vì hai đặc điểm của nhu cầu bán lẻ:

1. Nhu cầu biến động mạnh theo mùa vụ, giá bán, sự kiện và chương trình SNAP.
2. Phần lớn sản phẩm có **nhu cầu rời rạc (intermittent demand)**: nhiều ngày liên tiếp không bán được, rồi bất ngờ bán được vài đơn vị. Trong bộ dữ liệu M5, 73% chuỗi thuộc nhóm intermittent và 17% thuộc nhóm lumpy (bài 01).

Với mỗi sản phẩm tại mỗi cửa hàng (SKU–store), người quản lý cần quyết định: **nhập thêm bao nhiêu**, **giữ nguyên**, hay **thanh lý/giảm giá** phần tồn dư.

## 2. Vì sao vấn đề này quan trọng

- Dự báo điểm chỉ cho một con số, trong khi quyết định lượng tồn kho an toàn cần biết **độ bất định** của nhu cầu. Vì vậy cần dự báo xác suất (phân vị).
- Phần lớn nghiên cứu trên M5 tối ưu **độ chính xác dự báo** (WRMSSE, WSPL) và dừng ở đó (bài 02, 03). Sai số thấp hơn chưa chắc dẫn tới chi phí tồn kho thấp hơn.
- Các chuỗi rời rạc chiếm phần lớn M5 nhưng thường bị loại hoặc chọn lọc bỏ khỏi các nghiên cứu gắn với tồn kho (bài 11, 21, 22), trong khi đây là nhóm dễ gây tồn kho chết nhất.
- Quyết định xử lý hàng tồn dư (thanh lý/giảm giá) hầu như chưa được xét cùng quyết định nhập hàng.

## 3. Phát biểu bài toán

> Xây dựng và đánh giá một pipeline **từ dự báo nhu cầu xác suất đến khuyến nghị nhập hàng và thanh lý** trên bộ dữ liệu M5, đo hiệu quả bằng **KPI tồn kho** (fill rate, tỷ lệ hết hàng, tồn dư, chi phí) trong mô phỏng nhiều kỳ có lead time, và phân tích kết quả theo từng nhóm nhu cầu ADI–CV².

## 4. Phạm vi và giả định

- Dữ liệu: M5 (Walmart). Giai đoạn thử nghiệm dùng 3 cửa hàng đại diện (CA_1, TX_1, WI_1), mở rộng nếu tài nguyên cho phép.
- M5 **không có dữ liệu tồn kho thực**: tồn kho ban đầu, lead time, chu kỳ đặt hàng và chi phí thiếu/thừa hàng (c_u, c_o) là **tham số giả định**, kèm phân tích độ nhạy.
- Doanh số quan sát được không hoàn toàn bằng nhu cầu thực (khi hết hàng, doanh số bằng 0 dù nhu cầu khác 0).
- Quyết định thanh lý chỉ được so sánh giữa các chính sách trong mô phỏng, không mô hình hóa phản ứng của nhu cầu khi giảm giá.