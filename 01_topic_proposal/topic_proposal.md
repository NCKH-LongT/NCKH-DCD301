BÁO CÁO ĐỀ XUẤT DỰ ÁN (PROJECT PROPOSAL)
1. Tên Domain & Tóm tắt dự án (Overview)
Tên Domain: Hệ thống Quản lý và Kiểm soát Ra Vào Phòng Lab Thiết bị Thông minh (Lab Access Control System).

Tóm tắt (Elevator Pitch): Hệ thống tích hợp giữa Website quản lý và Thiết bị Phần cứng (IoT) đặt tại cửa nhằm tự động hóa quy trình cấp quyền và kiểm soát ra vào phòng Lab. Dự án phục vụ cho Ban quản lý và thành viên phòng Lab, mang lại giá trị cốt lõi là bảo mật tối đa bằng cơ chế Token thời hạn/OTP một lần, đồng thời tối ưu hóa tài nguyên phần cứng thông qua việc áp dụng lý thuyết Máy trạng thái (FSM).

2. Bối cảnh & Vấn đề hiện tại (Problem Statement)
Thực trạng: Hiện nay, việc quản lý ra vào các phòng Lab, phòng nghiên cứu tại các trường học hoặc tổ chức phần lớn vẫn phụ thuộc vào việc điểm danh thủ công, ký sổ, giữ chìa khóa cơ truyền thống, hoặc sử dụng các hệ thống quét thẻ offline cũ kỹ thiếu đồng bộ với cơ sở dữ liệu trực tuyến.

Nỗi đau (Pain points):

Quản lý thời hạn kém: Không thể giới hạn thời gian vào phòng Lab của từng thành viên theo lịch đăng ký trước (ví dụ: chỉ cho vào từ 8h - 11h).

Bất tiện cho khách tạm thời: Khi có chuyên gia hoặc sinh viên mượn phòng ngắn hạn, ban quản lý phải có mặt trực tiếp để mở cửa hoặc bàn giao chìa khóa, tốn thời gian và dễ thất lạc.

Thiếu dữ liệu thời gian thực (Real-time): Không có dữ liệu chính xác ai đang ở trong phòng Lab tại thời điểm thực tế, gây khó khăn khi xảy ra sự cố mất mát thiết bị.

3. Giải pháp đề xuất (Proposed Solution)
Giải pháp: Xây dựng hệ thống IoT kết hợp Web Dashboard trực tuyến. Thiết bị điều khiển cửa (ESP32 + RC522 + Keypad) sẽ liên lạc thời gian thực với Web API để xác thực quyền truy cập qua hai phương thức song song: Thẻ từ chứa Token định thời hoặc Mã OTP dùng một lần.

Điểm khác biệt & Giá trị nổi bật (USPs):

Xác thực kép linh hoạt: Kết hợp thẻ vật lý bảo mật cho thành viên cố định và mã số OTP sinh tự động trên Web cho khách ngắn hạn.

Ứng dụng lý thuyết tối ưu phần cứng: Dự án tích hợp và so sánh trực quan hai thuật toán điều khiển Mealy FSM (Ưu tiên phản hồi nhanh) và Moore FSM (Ưu tiên an toàn bảo mật, chống nhiễu mạng) ngay trên bo mạch nhúng, tạo ra điểm nhấn kỹ thuật mạnh mẽ cho một đồ án công nghệ.

4. Đối tượng người dùng (Actors)
Admin / Manager (Ban quản lý Lab): Cấp phát thẻ, duyệt yêu cầu mượn phòng, cấu hình thời gian token cho thẻ, xem báo cáo lịch sử ra vào trực tuyến, quản lý danh mục thiết bị.

Member (Thành viên/Sinh viên cố định): Đăng ký lịch sử dụng Lab trên website, theo dõi thời hạn hoạt động của thẻ từ cá nhân.

Guest (Khách/Thành viên tạm thời): Đăng nhập web để yêu cầu cấp mã OTP vào phòng Lab một lần (hiệu lực trong 5 phút)
