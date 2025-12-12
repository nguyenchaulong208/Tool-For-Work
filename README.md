# Project Tool Công Việc

## Giới thiệu
Dự án này tập hợp các công cụ hỗ trợ xử lý dữ liệu nội bộ, đặc biệt liên quan đến quản lý và hạch toán chi phí lương. Các chức năng được thiết kế để tự động hóa quy trình, giảm sai sót và tiết kiệm thời gian.

## Các chức năng chính

### 1. Gộp file Excel
*(Tạm thời bỏ trống – sẽ cập nhật sau)*

---

### 2. Phân chia hạch toán chi phí lương
- **Nguồn dữ liệu**:
  - File Excel danh sách nhân viên (chứa thông tin: mã nhân viên, tên, phòng ban, chức vụ).
  - File Excel lương nhân viên từng tháng.
- **Quy trình xử lý**:
  1. Đọc dữ liệu từ file danh sách nhân viên.
  2. Đọc dữ liệu từ file lương nhân viên theo tháng.
  3. Match dữ liệu lương với danh sách nhân viên dựa trên mã nhân viên.
  4. Phân chia chi phí lương theo phòng ban.
- **Đầu ra**:
  - File Excel tổng hợp chi phí lương theo phòng ban.
  - Báo cáo chi phí lương từng tháng.

---

### 3. Kiểm tra sai sót file Excel tính lương
- **Mục tiêu**:
  - Phát hiện các lỗi thường gặp trong file lương (ví dụ: nhân viên thiếu thông tin, dữ liệu trùng lặp, sai mã nhân viên).
  - Đưa ra cảnh báo hoặc báo cáo lỗi để người dùng chỉnh sửa.
- **Đầu ra**:
  - File báo cáo lỗi hoặc log chi tiết.
  - Danh sách nhân viên có dữ liệu bất thường.

---

## Yêu cầu hệ thống
- Python 3.9+
- Các thư viện:
  - `pandas`
  - `openpyxl`
  - `xlrd`
