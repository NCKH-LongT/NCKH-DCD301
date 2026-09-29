# Problem Statement

> Số trang `(tr. N)` và số bài theo `02_related_work/paper_list.md`. Chi tiết nguồn xem `02_related_work/paper_summaries/`.

## 1. Vấn đề thực tế

Các nhà bán lẻ phải đối mặt cùng lúc với hai rủi ro ngược chiều:

- **Hết hàng (stockout):** mất doanh thu và khách hàng.
- **Tồn kho dư thừa (overstock):** tốn chi phí lưu kho, đọng vốn, hàng phải giảm giá hoặc xử lý. Ví dụ thực tế: bài 25 ghi nhận mức tồn cuối kỳ của nhiều phụ tùng vượt xa mức safety stock trong thời gian dài (tr. 7).

Khó khăn này tăng lên vì hai đặc điểm của nhu cầu bán lẻ:

1. Nhu cầu biến động theo giá bán, sự kiện và chương trình SNAP. Trong M5, SNAP áp dụng khoảng 10 ngày mỗi tháng, tức khoảng 33% số ngày (bài 01, tr. 6).
2. Phần lớn sản phẩm có **nhu cầu rời rạc (intermittent demand)**: nhiều ngày liên tiếp không bán được, rồi bất ngờ bán được vài đơn vị. Trong M5, **73% chuỗi thuộc nhóm intermittent và 17% thuộc nhóm lumpy** (bài 01, tr. 8); khoảng **60,1% quan sát bằng 0** (bài 11, tr. 16).

Với mỗi sản phẩm tại mỗi cửa hàng (SKU–store), người quản lý cần quyết định: **nhập thêm bao nhiêu**, **giữ nguyên**, hay **thanh lý/giảm giá** phần tồn dư.

## 2. Vì sao vấn đề này quan trọng

- **Cần dự báo xác suất, không chỉ dự báo điểm.** Dự báo điểm chỉ cho một con số, trong khi quyết định tồn kho an toàn cần biết độ bất định. Chính nhóm tổ chức M5 nêu rằng các phân vị cao (0,925–0,995) thường được dùng để xác định safety stock (bài 03, tr. 2).
- **Độ chính xác dự báo chưa phải là mục tiêu cuối cùng.**
  - M5 đánh giá bằng WRMSSE và WSPL (bài 01, tr. 3), và **không tập trung vào một bài toán ra quyết định cụ thể** (bài 03, tr. 2–3).
  - Trong tồn kho, độ chính xác cao hơn không nhất thiết cho quyết định tốt hơn (bài 11, abstract).
  - Dự báo đúng các kỳ bằng 0 làm giảm tồn kho nhưng tăng rủi ro thiếu hàng (bài 24, tr. 21).
- **Chuỗi rời rạc chiếm đa số nhưng thường bị bỏ qua trong các nghiên cứu gắn với tồn kho.**
  - Bài 22 chỉ dùng 8.000 chuỗi bán nhiều và tự nêu đây là "điểm yếu chính" (tr. 4, 18).
  - Bài 21 chỉ dùng một tập con thực phẩm biến động mạnh (tr. 8).
  - Với chuỗi rời rạc, phương pháp Croston không cập nhật sau các kỳ bằng 0 nên phản ứng chậm khi sản phẩm lỗi thời (bài 16, abstract), đúng là tình huống dễ sinh tồn kho chết.
- **Quyết định xử lý hàng tồn dư chưa được xét cùng quyết định nhập hàng.** Khi tìm các từ khóa liquidation, markdown, clearance, salvage trong toàn văn bài 11, 21–25, các từ này chỉ xuất hiện ở phần tài liệu tham khảo, không bài nào có quyết định thanh lý (xem `literature_review_matrix.md`).

## 3. Phát biểu bài toán

> Xây dựng và đánh giá một pipeline **từ dự báo nhu cầu xác suất đến khuyến nghị nhập hàng và thanh lý** trên bộ dữ liệu M5, đo hiệu quả bằng **KPI tồn kho** (fill rate, tỷ lệ hết hàng, tồn dư, chi phí) trong mô phỏng nhiều kỳ có lead time, **giữ lại toàn bộ các nhóm nhu cầu** và phân tích kết quả theo từng nhóm ADI–CV².

## 4. Phạm vi và giả định

- Dữ liệu: M5 (Walmart). Giai đoạn thử nghiệm dùng 3 cửa hàng đại diện (CA_1, TX_1, WI_1), mở rộng nếu tài nguyên cho phép.
- M5 **không có dữ liệu tồn kho thực**. Tồn kho ban đầu, lead time, chu kỳ đặt hàng và chi phí thiếu/thừa hàng (c_u, c_o) là **tham số giả định**, kèm phân tích độ nhạy.
- Doanh số quan sát được không hoàn toàn bằng nhu cầu thực: khi hết hàng, doanh số bằng 0 dù nhu cầu khác 0 (nhận định của nhóm; M5 chỉ có dữ liệu doanh số, giá và lịch, bài 01, tr. 5).
- Quyết định thanh lý chỉ được so sánh giữa các chính sách trong mô phỏng, **không mô hình hóa phản ứng của nhu cầu khi giảm giá**.
- Kết luận về chi phí phụ thuộc vào các giả định mô phỏng ở trên.
