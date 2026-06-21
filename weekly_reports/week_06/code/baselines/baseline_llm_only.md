# Baseline LLM-only (No RAG)

## Mục đích
Đánh giá khả năng của LLM khi được cung cấp trực tiếp mô tả bài toán mạch tuần tự cơ bản mà không có hỗ trợ từ RAG (Retrieval-Augmented Generation). LLM sẽ dựa trên kiến thức được training để thiết kế mạch, xác định trạng thái tiếp theo, và đưa ra giải pháp.

---

## 1. Prompt Template

```
Bạn là một kỹ sư thiết kế mạch điện tử chuyên về các mạch tuần tự cơ bản (Sequential Circuit).
Nhiệm vụ của bạn là phân tích các yêu cầu thiết kế mạch và đưa ra giải pháp.

**Yêu cầu thiết kế:**
- Loại mạch: {circuit_type}
- Số bit/input: {input_bits}
- Số output: {output_bits}
- Các biểu thức logic/trạng thái: {requirements}
- Điều kiện reset: {reset_condition}
- Clock: {clock_frequency}

**Phân tích và thiết kế:**
1. Xác định số trạng thái (state) cần thiết
2. Vẽ bảng chuyển trạng thái (State Transition Table)
3. Xác định phương trình Boolean cho input của flip-flop (D, JK, v.v.)
4. Đề xuất cách cài đặt (logic gates hoặc VHDL/Verilog)
5. Mức độ tự tin về thiết kế (cao/vừa/thấp)

**Format JSON phản hồi:**
{
  "circuit_type": "counter|state_machine|frequency_divider|...",
  "num_states": "số trạng thái",
  "state_table": [
    {
      "current_state": "S0",
      "input": "input_values",
      "next_state": "S1",
      "output": "output_values"
    }
  ],
  "equations": {
    "D_flipflop_inputs": "equations",
    "output_logic": "equations"
  },
  "implementation": "Verilog/VHDL code hoặc mô tả thiết kế",
  "confidence": 0.5-1.0,
  "explanation": "giải thích chi tiết"
}
```

---

## 2. Sample Sensor Data

### Test Case 1: Mạch đếm 4-bit (4-bit Counter)
```json
{
  "circuit_type": "counter",
  "num_bits": 4,
  "reset": true,
  "requirements": "Mạch đếm từ 0 đến 15, sau đó reset về 0. Có điều khiển enable",
  "clock_frequency": "1 kHz"
}
```

**LLM Output:**
```json
{
  "circuit_type": "counter",
  "num_states": 16,
  "state_table": [
    {
      "current_state": "0000",
      "input": "enable=1",
      "next_state": "0001",
      "output": "0000"
    },
    {
      "current_state": "0001",
      "input": "enable=1",
      "next_state": "0010",
      "output": "0001"
    },
    {
      "current_state": "1111",
      "input": "enable=1",
      "next_state": "0000",
      "output": "1111"
    },
    {
      "current_state": "any",
      "input": "enable=0",
      "next_state": "no_change",
      "output": "current_output"
    }
  ],
  "equations": {
    "D_flipflop_inputs": "D[i] = Q[i] XOR (enable AND carry_in[i])",
    "carry": "carry[i+1] = Q[i] AND carry[i]"
  },
  "implementation": "module counter_4bit(input clk, reset, enable, output [3:0] count); always@(posedge clk) if(reset) count <= 0; else if(enable) count <= count + 1; endmodule",
  "confidence": 0.92,
  "explanation": "Đây là một mạch đếm lên tiêu chuẩn sử dụng 4 flip-flop D. Mỗi clock, nếu enable=1, giá trị counter tăng 1. Khi đạt 15 (1111), lần tiếp theo reset về 0. Sơ đồ logic sử dụng XOR gates để thực hiện phép cộng. Nếu enable=0, counter giữ nguyên giá trị."
}
```

---

### Test Case 2: Mạch Flip-flop JK với điều kiện
```json
{
  "circuit_type": "state_machine",
  "num_states": 3,
  "inputs": "A, B",
  "reset": true,
  "requirements": "Mạch có 3 trạng thái: S0 (chờ), S1 (sẵn sàng), S2 (hoạt động). S0->S1 khi A=1, S1->S2 khi B=1, S2->S0 khi A=0 và B=0",
  "output_behavior": "Output=1 chỉ khi ở trạng thái S2"
}
```

**LLM Output:**
```json
{
  "circuit_type": "state_machine",
  "num_states": 3,
  "state_table": [
    {
      "current_state": "S0",
      "input": "A=0, B=0",
      "next_state": "S0",
      "output": 0
    },
    {
      "current_state": "S0",
      "input": "A=1, B=0",
      "next_state": "S1",
      "output": 0
    },
    {
      "current_state": "S1",
      "input": "A=1, B=0",
      "next_state": "S1",
      "output": 0
    },
    {
      "current_state": "S1",
      "input": "A=1, B=1",
      "next_state": "S2",
      "output": 0
    },
    {
      "current_state": "S2",
      "input": "A=0, B=0",
      "next_state": "S0",
      "output": 1
    },
    {
      "current_state": "S2",
      "input": "any_other",
      "next_state": "S2",
      "output": 1
    }
  ],
  "equations": {
    "state_encoding": "S0=00, S1=01, S2=10",
    "J_K_inputs": "J1 = A, K1 = A*B', J0 = A*Q1', K0 = (A'B')*Q1"
  },
  "implementation": "Sử dụng 2 flip-flop JK để lưu trữ 3 trạng thái. Logic tổ hợp để tính J, K inputs dựa trên hiện tại state và inputs A, B.",
  "confidence": 0.85,
  "explanation": "Mạch có 3 trạng thái (S0, S1, S2) được mã hóa bằng 2 flip-flop JK. Các điều kiện chuyển trạng thái được thực hiện bằng logic gates. Output chỉ hoạt động (=1) ở trạng thái S2."
}
```

---

### Test Case 3: Bộ chia tần số (Frequency Divider)
```json
{
  "circuit_type": "frequency_divider",
  "input_frequency": "8 kHz",
  "output_frequency": "1 kHz",
  "division_ratio": 8,
  "requirements": "Chia tần số input thành 1/8"
}
```

**LLM Output:**
```json
{
  "circuit_type": "frequency_divider",
  "num_states": 8,
  "state_table": [
    {
      "current_state": "count=0",
      "input": "clock_pulse",
      "next_state": "count=1",
      "output": 0
    },
    {
      "current_state": "count=7",
      "input": "clock_pulse",
      "next_state": "count=0",
      "output": 1
    }
  ],
  "equations": {
    "implementation": "Sử dụng bộ đếm 3-bit (divide by 8), output lấy từ bit MSB hoặc từ bộ so sánh (count==7)"
  },
  "implementation": "module freq_divider_8(input clk, output clk_div8); reg [2:0] counter; always@(posedge clk) counter <= (counter == 3'd7) ? 3'd0 : counter + 1; assign clk_div8 = (counter == 3'd7); endmodule",
  "confidence": 0.95,
  "explanation": "Bộ chia tần số ×8 được thực hiện bằng bộ đếm 3-bit. Output được set HIGH khi bộ đếm đạt 7 (lần thứ 8), tạo ra một xung. Tần số output = tần số input / 8. Đây là giải pháp chuẩn cho mạch chia tần."
}
```

---

### Test Case 4: Mạch Shift Register (khó - LLM có thể lặng lẽ sai)
```json
{
  "circuit_type": "shift_register",
  "width": 8,
  "mode": "bidirectional",
  "requirements": "Mạch shift 8-bit có thể shift trái, phải, hoặc giữ nguyên. Có tín hiệu serial input từ cả 2 phía. Output đầu ra từ hai đầu."
}
```

**LLM Output (có thể sai):**
```json
{
  "circuit_type": "shift_register",
  "num_states": "256 (mọi kết hợp 8-bit)",
  "equations": {
    "shift_left": "Q[i] = Q[i-1] (với Q[0] = serial_input_left)",
    "shift_right": "Q[i] = Q[i+1] (với Q[7] = serial_input_right)"
  },
  "implementation": "module shift_reg_8bit(input clk, [1:0] mode, serial_in_left, serial_in_right, output [7:0] data); always@(posedge clk) begin case(mode) 2'b00: data <= data; // hold 2'b01: data <= {data[6:0], serial_in_left}; // shift left 2'b10: data <= {serial_in_right, data[7:1]}; // shift right endcase end endmodule",
  "confidence": 0.72,
  "explanation": "Shift register bidirectional được thực hiện bằng 8 flip-flop D trong chuỗi nối tiếp. Mode được điều khiển bằng 2 bit: 00=hold, 01=shift left, 10=shift right. Serial input được đưa vào từ cả hai phía. Đây là triển khai chuẩn của shift register."
}
```

**Lưu ý:** LLM có thể sai về chi tiết triển khai (ví dụ: độ ưu tiên của mode control, cách nối shift chain) nhưng cấu trúc tổng thể là đúng.

---

## 3. Đánh giá Ưu/Nhược điểm

### ✅ Ưu điểm

| Ưu điểm | Chi tiết |
|---------|---------|
| **Hiểu yêu cầu ngôn ngữ tự nhiên** | LLM có thể hiểu mô tả "shift register bidirectional" và đưa ra thiết kế |
| **Giải thích lôgic** | Có thể giải thích tại sao chọn 2 flip-flop cho 3 trạng thái, v.v. |
| **Nhanh sinh output** | Có thể tạo ra Verilog/VHDL code nhanh chóng |
| **Cách tiếp cận linh hoạt** | Có thể xử lý các biến thể của bài toán cơ bản |

### ❌ Nhược điểm - NGHIÊM TRỌNG

| Nhược điểm | Chi tiết | Ảnh hưởng |
|-----------|---------|----------|
| **Hallucination về logic** | LLM có thể "bịa ra" các phương trình Boolean sai | Mạch thiết kế không hoạt động |
| **Lỗi trong state encoding** | Có thể chỉ định encoding không hiệu quả hoặc không tối ưu | Tốn thêm gates, logic phức tạp |
| **Không verify timing** | Không kiểm tra setup/hold time, race condition | Mạch hoạt động không ổn định (metastability) |
| **Mã code Verilog/VHDL có lỗi** | Syntax sai, logic lỗi, vòng lặp không kết thúc | Code không compile được |
| **Không biết tối ưu hóa** | Có thể dùng quá nhiều gates, flip-flops, hoặc logic phức tạp | Thiết kế không hiệu quả, tốn diện tích/điện năng |
| **Sai về trạng thái đặc biệt** | Quên reset, quên đối xử với trạng thái không dùng | Mạch bị stuck ở trạng thái lạ |
| **Inconsistent giữa các output** | Phương trình logic không match với code Verilog/VHDL | Confusion, không biết phiên bản nào đúng |
| **Không validate logic sơ đồ** | Không kiểm tra kỹ thuật tính đúng đắn của state table | Có thể có lỗi logic tinh tế khó phát hiện |

---

## 4. Kết luận

### Khi nào dùng LLM-only cho thiết kế mạch?
✅ **Thích hợp khi:**
- Cần nhanh giải quyết bài toán đơn giản (counter, frequency divider)
- Cần hiểu rõ logic cao cấp trước khi chi tiết hóa
- Dùng làm điểm xuất phát, sau đó verify kỹ

❌ **KHÔNG thích hợp khi:**
- Thiết kế mạch phức tạp, critical (có lỗi dẫn đến hư hỏng)
- Cần đảm bảo tính đúng đắn 100%
- Thiết kế cần tối ưu hóa (diện tích, điện năng, tốc độ)
- Cần tính toán timing (setup/hold time, metastability)

### So sánh với các baseline khác
- **vs Rule-based:** LLM linh hoạt hơn nhưng không chính xác; Rule-based có quy tắc cứng nhưng đơn giản
- **vs RAG-only:** LLM-only nhanh nhưng rủi ro lỗi cao; RAG-only có tài liệu hỗ trợ, chính xác hơn
- **vs Proposed (RAG + Agent):** LLM-only không verify logic, dễ sai; Proposed có validation, an toàn hơn

---

## 5. Ghi chú kỹ thuật

### Model được test
- **Model gợi ý:** GPT-4o, Claude-3.5, Gemini-Pro
- **Temperature:** 0.2-0.3 (giảm để tăng consistency)
- **Max tokens:** 1500-2000 (mạch có thể có code dài)

### Thử nghiệm tiếp theo cần làm
1. Test với các mạch phức tạp hơn (bộ nhân, mạch mã hóa)
2. Có tha hóa prompt để yêu cầu LLM verify lại state table
3. So sánh output Verilog với simulation (ModelSim, Vivado)
4. Test với prompt bao gồm hạn chế (ví dụ: "chỉ dùng flip-flop D" hoặc "tối ưu hóa số gates")
5. Đo độ tin tưởng của LLM (confidence score) vs tỷ lệ lỗi thực tế

