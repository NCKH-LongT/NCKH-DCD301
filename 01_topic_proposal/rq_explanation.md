# RQ-09: Phân biệt mạch tổ hợp và mạch tuần tự. Vì sao mạch tuần tự cần phần tử nhớ như latch hoặc flip-flop?

## Phân biệt mạch tổ hợp và mạch tuần tự

| Đặc điểm | Mạch tổ hợp (Combinational Circuit) | Mạch tuần tự (Sequential Circuit) |
|---|---|---|
| **Định nghĩa** | Đầu ra chỉ phụ thuộc vào các giá trị đầu vào ở thời điểm hiện tại. | Đầu ra phụ thuộc vào cả đầu vào hiện tại và trạng thái trước đó (lịch sử hoạt động) của mạch. |
| **Bộ nhớ / Khả năng lưu trữ** | Không có bộ nhớ. | Có bộ nhớ để ghi nhớ trạng thái hiện tại. |
| **Phần tử phản hồi (Feedback)** | Không có đường phản hồi tín hiệu từ đầu ra về đầu vào. | Có đường phản hồi tín hiệu từ đầu ra của phần tử nhớ quay lại đầu vào của mạch tổ hợp. |
| **Xung nhịp (Clock)** | Không sử dụng xung clock (bất đồng bộ hoàn toàn). | Thường sử dụng xung clock để đồng bộ hóa hoạt động (hoặc hoạt động bất đồng bộ có điều kiện). |
| **Phần tử nhớ tích hợp** | Không sử dụng. | Sử dụng Latch hoặc Flip-Flop để lưu trạng thái. |
| **Ứng dụng thực tế** | Bộ cộng (Adder), bộ chọn kênh (Multiplexer), bộ giải mã (Decoder). | Bộ đếm (Counter), thanh ghi (Register), bộ nhớ (RAM/ROM), Máy trạng thái (FSM). |

### Vì sao mạch tuần tự cần phần tử nhớ như Latch hoặc Flip-Flop?
Mạch tuần tự cần phần tử nhớ vì hoạt động của nó mang tính chất **trình tự thời gian**. Nếu không có phần tử nhớ để lưu lại "trạng thái hiện tại" (State) của hệ thống, mạch sẽ bị mất đi khái niệm về lịch sử/quá khứ và lập tức hoạt động giống như một mạch tổ hợp bình thường (chỉ phản ứng tức thời với đầu vào tại đúng thời điểm đó). 

---

## RQ9.1: Output của mạch tổ hợp phụ thuộc vào những yếu tố nào?

Đầu ra của mạch tổ hợp chỉ phụ thuộc duy nhất vào:
- **Các giá trị đầu vào vật lý hiện tại (Current Inputs)** đang được cấp trực tiếp cho các cổng logic của mạch.

Mạch tổ hợp hoàn toàn **không phụ thuộc** vào:
- Trạng thái hoạt động trước đó của hệ thống (vì không có phần tử lưu trữ).
- Xung clock đồng bộ thời gian (hoạt động tức thời sau khi tín hiệu truyền qua các cổng logic bị trễ - propagation delay).

---

## RQ9.2: Output của mạch tuần tự phụ thuộc vào input hiện tại và trạng thái trước đó như thế nào?

Trong mạch tuần tự, mối quan hệ giữa Đầu ra (Output), Đầu vào (Input) và Trạng thái (State) được phân thành 2 mô hình toán học / kiến trúc máy trạng thái (FSM) kinh điển:

1. **Mô hình Mealy (Mealy Machine):**
   - Đầu ra ở thời điểm hiện tại $Y(t)$ phụ thuộc vào cả **Đầu vào hiện tại $X(t)$** và **Trạng thái hiện tại $S(t)$** (trạng thái được lưu từ chu kỳ trước).
   - Công thức: $Y(t) = f(X(t), S(t))$
   - *Đặc điểm:* Đầu ra có thể thay đổi ngay lập tức khi đầu vào thay đổi, bất kể có xung clock hay không.

2. **Mô hình Moore (Moore Machine):**
   - Đầu ra ở thời điểm hiện tại $Y(t)$ chỉ phụ thuộc duy nhất vào **Trạng thái hiện tại $S(t)$** của mạch.
   - Công thức: $Y(t) = g(S(t))$
   - *Đặc điểm:* Đầu ra cực kỳ ổn định vì nó chỉ thay đổi đồng bộ theo xung nhịp clock (khi trạng thái của Flip-Flop chuyển tiếp).

### Ý nghĩa thực tế (Ví dụ Nhà kính)
Khi độ ẩm giảm xuống thấp (Input hiện tại), hệ thống không chỉ bật máy bơm ngay lập tức (mạch tổ hợp). Nó sẽ đối chiếu với trạng thái hiện tại (Ví dụ: trạng thái `WATERING` đã được kích hoạt cách đây 2 phút). Nhờ bộ nhớ lưu giữ trạng thái trước đó, hệ thống biết rằng máy bơm đang chạy và sẽ tiếp tục giữ nguyên trạng thái tưới mà không kích hoạt lại từ đầu, tránh làm hỏng thiết bị.

---

## RQ9.3: Latch và Flip-Flop đóng vai trò gì trong việc lưu trữ trạng thái của mạch tuần tự?

Latch và Flip-Flop là các **phần tử nhớ cơ bản nhất (1-bit memory elements)** trong kỹ thuật số. Chúng đóng vai trò cốt lõi trong mạch tuần tự thông qua cơ chế sau:

1. **Lưu trữ trạng thái vật lý (State Storage):**
   - Mỗi Latch hoặc Flip-Flop có khả năng lưu giữ 1 bit thông tin nhị phân (`0` hoặc `1`). Bằng cách kết hợp nhiều Flip-Flops (tạo thành thanh ghi trạng thái - State Register), ta có thể biểu diễn nhiều trạng thái phức tạp khác nhau của hệ thống FSM.

2. **Tạo đường phản hồi (Feedback Loop):**
   - Chúng nhận tín hiệu "Trạng thái tiếp theo" (Next State) từ đầu ra của mạch logic tổ hợp, giữ lại giá trị đó, và phản hồi ngược lại đầu vào của mạch logic tổ hợp ở chu kỳ tiếp theo dưới dạng "Trạng thái hiện tại" (Present State).

3. **Cơ chế hoạt động và Phân biệt Vai trò:**
   - **Latch (Chốt):** Nhạy theo **mức tín hiệu (Level-sensitive)**. Latch thay đổi trạng thái bất cứ khi nào tín hiệu cho phép (Enable) ở mức tích cực. Latch hoạt động không đồng bộ, dễ gây ra hiện tượng chạy đua tín hiệu (race conditions) nếu không thiết kế cẩn thận.
   - **Flip-Flop (Dép lê):** Nhạy theo **cạnh xung nhịp (Edge-triggered)** (chỉ thay đổi khi có cạnh lên hoặc cạnh xuống của xung Clock). Flip-Flop là nền tảng của **Mạch tuần tự đồng bộ (Synchronous Sequential Circuits)**, đảm bảo toàn bộ hệ thống chuyển trạng thái cực kỳ ổn định và đồng đều theo nhịp clock.
