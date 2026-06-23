# Domain Scope — Smart Greenhouse Control System

## Tên đề tài

**Smart Greenhouse Control System** (Hệ thống điều khiển nhà kính thông minh)

## Lý do chọn domain

1. **Bám sát yêu cầu Nông nghiệp thông minh** của môn học — phù hợp với định hướng AIoT.
2. **Thích hợp để thiết kế FSM (Máy trạng thái tuần tự)** — điều khiển các trạng thái: tưới tiêu, làm mát, sưởi ấm, chiếu sáng.
3. **Môi trường nhà kính khắc nghiệt** dễ phát sinh lỗi cảm biến (nhiệt độ cao, độ ẩm lớn, bụi) — tạo điều kiện khai thác module Data Quality (SDQM).
4. **Tính thực tiễn cao** — nhà kính là ứng dụng phổ biến trong nông nghiệp công nghệ cao tại Việt Nam.

## Research Theme

**Theme 9:** Mạch tuần tự cơ bản (Sequential Circuits)

## Công nghệ dự kiến

| Thành phần | Công nghệ |
|---|---|
| IoT Simulation | Python Script |
| Backend API | FastAPI |
| Database | PostgreSQL / TimescaleDB |
| RAG Pipeline | LangChain + ChromaDB |
| Embedding | sentence-transformers (local) |
| LLM | Google Gemini |
| Agent Workflow | LangGraph |
