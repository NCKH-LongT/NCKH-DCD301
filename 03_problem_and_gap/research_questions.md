# Giải thích RQ cho Smart Greenhouse và Research Theme Mạch Multiplexer

- RQ1: Làm thế nào dữ liệu cảm biến IoT thời gian thực có thể tích hợp với kiến thức chuyên môn nông nghiệp để hỗ trợ ra quyết định có thể giải thích được trong nông nghiệp thông minh?
  - Giải thích: Với domain Smart Greenhouse, nghiên cứu này sẽ thiết kế cách tích hợp dữ liệu real-time từ các sensor nhiệt độ, độ ẩm, độ ẩm đất và ánh sáng với tài liệu kỹ thuật nông nghiệp. Hệ thống sẽ dùng pipeline RAG để truy xuất kiến thức phù hợp và tạo output khuyến nghị có lời giải thích và bằng chứng.

- RQ2: Chất lượng dữ liệu cảm biến ảnh hưởng như thế nào đến độ tin cậy của khuyến nghị AIoT trong nông nghiệp?
  - Giải thích: RQ này tập trung vào đánh giá dữ liệu cảm biến về missing data, nhiễu, lỗi sensor và dữ liệu mâu thuẫn. Nhóm sẽ xây module đánh giá chất lượng dữ liệu, tính điểm tin cậy và phân tích mức độ lỗi ảnh hưởng đến kết quả khuyến nghị bật quạt, tưới nước, bật đèn, hoặc cảnh báo.

- RQ3: Liệu khung Agentic RAG có cải thiện tính liên quan ngữ cảnh và khả năng giải thích của hệ hỗ trợ quyết định nông nghiệp so với phương pháp rule-based hoặc LLM-only không?
  - Giải thích: Nghiên cứu sẽ xây dựng hệ thống Agentic RAG và các baseline so sánh. Mục tiêu là kiểm tra xem Agentic RAG có mang lại đề xuất chính xác hơn, phù hợp ngữ cảnh hơn và giải thích tốt hơn so với rule-based hay chỉ dùng LLM.

- RQ4: Khung đề xuất hoạt động hiệu quả như thế nào trong các kịch bản bình thường, thiếu dữ liệu, lỗi cảm biến và sensor mâu thuẫn?
  - Giải thích: Nhóm sẽ tạo các kịch bản thử nghiệm cho môi trường Smart Greenhouse, chạy hệ thống trong các tình huống khác nhau và đo các chỉ số như accuracy, confidence, latency, explanation score và các trường hợp thất bại.

- RQ-07: Multiplexer (MUX) là gì? Làm thế nào để sử dụng MUX nhằm chọn một trong nhiều tín hiệu đầu vào và đưa ra một ngõ ra duy nhất?
  - Giải thích: Multiplexer là một mạch tổ hợp cho phép chọn một trong nhiều tín hiệu đầu vào theo các đường chọn và cung cấp một ngõ ra duy nhất. Trong Smart Greenhouse, MUX dùng để chọn dữ liệu từ các sensor khác nhau rồi gửi qua một chân ADC duy nhất của ESP32.

- RQ7.1: Multiplexer có các thành phần chính nào, bao gồm data inputs, select lines và output?
  - Giải thích: Các thành phần chính của MUX gồm nhiều data inputs (các tín hiệu vào), select lines (các đường chọn) và một output duy nhất. Select lines xác định tín hiệu nào được chuyển qua output.

- RQ7.2: Với MUX 4-to-1, các đường chọn S1 và S0 quyết định ngõ vào được chọn như thế nào?
  - Giải thích: Với MUX 4-to-1, hai đường chọn S1 và S0 mã hóa bốn ngõ vào. Ví dụ: 00 chọn input 0, 01 chọn input 1, 10 chọn input 2, 11 chọn input 3.

- RQ7.3: Multiplexer có thể được ứng dụng như thế nào trong việc chọn dữ liệu trong hệ thống số?
  - Giải thích: MUX có thể dùng trong hệ thống số để chọn dữ liệu từ nhiều nguồn đầu vào và truyền một tín hiệu thích hợp đến bộ xử lý hoặc module tiếp theo. Trong hệ thống Smart Greenhouse, MUX có thể chọn dữ liệu sensor nhiệt độ, độ ẩm, độ ẩm đất hoặc ánh sáng để ESP32 đọc tuần tự.
