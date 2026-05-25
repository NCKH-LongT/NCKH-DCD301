# Topic Proposal

## 1. Selected Application Domain

Smart Agriculture / Nông nghiệp thông minh

## 2. Project Title

Smart Greenhouse Monitoring with BCD Arithmetic Error Detection and Agentic RAG

## 3. Vietnamese Title

Hệ Thống Nhà Kính Thông Minh AIoT: Ứng Dụng Phát Hiện Lỗi Số Học BCD và Agentic RAG

## 4. Problem Statement

Trong các hệ thống nông nghiệp thông minh, dữ liệu cảm biến như nhiệt độ, độ ẩm, độ ẩm đất và cường độ ánh sáng thường được dùng để đưa ra quyết định tưới tiêu hoặc điều chỉnh môi trường nhà kính. Tuy nhiên, dữ liệu cảm biến có thể bị lỗi do mất gói tin, sai mã BCD, nhiễu phần cứng hoặc xung đột giữa các cảm biến.

Nếu dữ liệu lỗi được đưa trực tiếp vào hệ thống AI hoặc RAG, hệ thống có thể đưa ra khuyến nghị sai, thiếu độ tin cậy hoặc gây ra hành động không an toàn.

## 5. Proposed Solution

Dự án đề xuất một hệ thống giám sát nhà kính thông minh kết hợp AIoT, kiểm tra lỗi số học BCD, đánh giá chất lượng dữ liệu và Agentic RAG.

Dữ liệu cảm biến sẽ được mã hóa và kiểm tra bằng cơ chế phát hiện lỗi BCD trước khi đi vào pipeline AI. Sau đó, hệ thống tính điểm chất lượng dữ liệu và dùng Agentic RAG để truy xuất kiến thức nông nghiệp phù hợp, từ đó đưa ra khuyến nghị an toàn và có thể giải thích.

## 6. Main Features

- Thu thập dữ liệu cảm biến nhà kính theo thời gian thực.
- Kiểm tra lỗi dữ liệu bằng BCD arithmetic error detection.
- Tính điểm chất lượng dữ liệu dựa trên validity, completeness và consistency.
- Truy xuất kiến thức nông nghiệp bằng RAG.
- Sử dụng Agentic RAG để quan sát, chẩn đoán, truy xuất, đánh giá và xác minh kết quả.
- Hiển thị dữ liệu và cảnh báo trên dashboard.
- Chặn hành động không an toàn khi dữ liệu không đáng tin cậy.

## 7. Expected Users

- Người quản lý nhà kính.
- Kỹ sư nông nghiệp.
- Sinh viên hoặc nhà nghiên cứu về AIoT và Smart Agriculture.
- Người vận hành hệ thống trồng trọt thông minh.

## 8. Expected Outcome

Hệ thống kỳ vọng giúp tăng độ tin cậy của khuyến nghị AI trong môi trường nhà kính thông minh. Việc kết hợp kiểm tra lỗi BCD và Agentic RAG giúp giảm sai lệch dữ liệu, hạn chế hallucination của AI và cải thiện khả năng safe-failure khi cảm biến gặp lỗi.

## 9. Suggested Technologies

- Backend: FastAPI
- Database: PostgreSQL / TimescaleDB
- Vector Database: Qdrant hoặc ChromaDB
- Embedding Model: multilingual-e5-large
- Frontend: ReactJS + TailwindCSS
- Dashboard: Recharts
- Logic Layer: Python bitwise operations
- AI/RAG: LLM + Agentic RAG pipeline

## 10. Keywords

Smart Agriculture, AIoT, Smart Greenhouse, Agentic RAG, BCD Error Detection, Data Quality, Sensor Fault Detection, Explainable AI, Safe-Failure AI.
