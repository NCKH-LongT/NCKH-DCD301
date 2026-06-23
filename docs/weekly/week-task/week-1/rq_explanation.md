# RQ-09: Phân biệt mạch tổ hợp và mạch tuần tự. Vì sao mạch tuần tự cần phần tử nhớ như latch hoặc flip-flop?

## Giải thích khái niệm

### Mạch tuần tự (Sequential Circuit)

Mạch tuần tự là loại mạch số mà đầu ra không chỉ phụ thuộc vào đầu vào hiện tại mà còn phụ thuộc vào trạng thái trước đó của mạch. Vì vậy, mạch tuần tự có khả năng ghi nhớ dữ liệu thông qua các phần tử nhớ như Flip-Flop hoặc thanh ghi.

### Mạch tổ hợp (Combinational Circuit)

Mạch tổ hợp là loại mạch số mà đầu ra chỉ phụ thuộc vào các đầu vào hiện tại, không phụ thuộc vào trạng thái trước đó hay xung đồng hồ. Mạch không có khả năng ghi nhớ dữ liệu và không chứa phần tử phản hồi.

### Latch

Latch là phần tử lưu trữ cơ bản hoạt động dựa trên mức tín hiệu (signal levels) thay vì sự chuyển đổi tín hiệu. Latch là thiết bị nhạy mức (level-sensitive), nghĩa là trạng thái của nó thay đổi khi tín hiệu điều khiển ở một mức xác định. Latch thường được sử dụng trong các mạch tuần tự bất đồng bộ.

### Flip-Flop

Flip-flop là mạch có khả năng duy trì trạng thái cho đến khi có tín hiệu đầu vào yêu cầu thay đổi trạng thái đó. Flip-flop là mạch tuần tự dùng để lưu trữ một trạng thái nhị phân duy nhất của dữ liệu hoặc thông tin. Flip-flop nhạy theo cạnh (edge-triggered), chỉ cập nhật tại cạnh lên/xuống của clock.

---

## Phân biệt mạch tổ hợp và mạch tuần tự

| Đặc điểm | Mạch tổ hợp | Mạch tuần tự |
|---|---|---|
| Phụ thuộc đầu ra | Chỉ phụ thuộc vào đầu vào hiện tại | Phụ thuộc vào đầu vào hiện tại và trạng thái trước đó |
| Bộ nhớ | Không có bộ nhớ | Có bộ nhớ |
| Phần tử nhớ | Không sử dụng | Sử dụng latch hoặc flip-flop |
| Clock | Không cần clock | Thường sử dụng clock |
| Phản hồi | Không có phản hồi | Có phản hồi |
| Ứng dụng | Bộ cộng, bộ giải mã, Multiplexer | Counter, Register, Memory, State Machine |

Mạch tuần tự cần phần tử nhớ như **latch** hoặc **flip-flop** vì chúng phải lưu trữ trạng thái trước đó của hệ thống, giúp:
- Ghi nhớ dữ liệu tạm thời
- Theo dõi trạng thái hiện tại của hệ thống
- Thực hiện các hoạt động theo trình tự thời gian

---

## RQ9.1: Output của mạch tổ hợp phụ thuộc vào những yếu tố nào?

Đầu ra của mạch tổ hợp **chỉ phụ thuộc vào các đầu vào hiện tại**. Mạch tổ hợp **không phụ thuộc vào**:
- Trạng thái trước đó
- Bộ nhớ
- Xung clock

---

## RQ9.2: Output của mạch tuần tự phụ thuộc vào input hiện tại và trạng thái trước đó như thế nào?

Trong mạch tuần tự, output tại thời điểm t không chỉ phụ thuộc vào input hiện tại, mà còn phụ thuộc vào trạng thái nội bộ (state) được lưu từ các thời điểm trước:

$$ \text{Output}(t) = f(\text{Input}(t), \text{State}(t-1)) $$
$$ \text{State}(t) = g(\text{Input}(t), \text{State}(t-1)) $$

Điểm khác biệt cốt lõi so với mạch tổ hợp là: mạch tuần tự có cơ chế ghi nhớ state, nên output có thể khác nhau với cùng một input nếu state trước đó khác nhau.

---

## RQ9.3: Latch và Flip-Flop đóng vai trò gì trong việc lưu trữ trạng thái của mạch tuần tự?

Latch và flip-flop là các phần tử nhớ cơ bản, giữ vai trò lưu trữ state cho mạch tuần tự:

- **Latch**: nhạy cảm theo mức (level-sensitive). Khi enable hoạt động, latch cập nhật output theo input. Khi enable tắt, latch giữ nguyên giá trị.
- **Flip-flop**: nhạy cảm theo cạnh (edge-triggered). Chỉ cập nhật tại cạnh lên/xuống của clock, giúp đồng bộ hóa và hạn chế bất định.

Ghép nhiều latch/flip-flop tạo thành thanh ghi (register) hoặc bộ đếm (counter) để lưu trạng thái nhiều bit.

---

## Ví dụ minh họa

### 1) SR Latch (NOR)

| S | R | Q (mới) | Ghi chú |
|---|---|---------|---------|
| 0 | 0 | Giữ     | Lưu trạng thái trước |
| 1 | 0 | 1       | Set |
| 0 | 1 | 0       | Reset |
| 1 | 1 | Không hợp lệ | Trạng thái cấm |

### 2) D Flip-Flop (cạnh lên)

Tại mỗi cạnh lên của clock, Q nhận giá trị D. Giữa các cạnh, Q giữ nguyên.

### 3) Counter / Register

- Bộ đếm nhị phân 2-bit đồng bộ: 00 → 01 → 10 → 11 → 00 → ...
- Thanh ghi 4-bit: tại cạnh lên, toàn bộ 4 bit input được chốt vào output.

---

## Nguồn tham khảo

- M. Morris Mano, M. D. Ciletti, "Digital Design", Pearson.
- S. Brown, Z. Vranesic, "Fundamentals of Digital Logic with VHDL/Verilog Design", McGraw-Hill.
- D. Harris, S. Harris, "Digital Design and Computer Architecture", Morgan Kaufmann.
- N. Nisan, S. Schocken, "The Elements of Computing Systems" (Nand2Tetris), MIT Press.
