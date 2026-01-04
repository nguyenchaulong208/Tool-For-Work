# 📘 **Excel Combine Tool – User Guide (Hướng dẫn sử dụng)**

## 1. Giới thiệu

**Excel Combine Tool** là công cụ giúp bạn:

- Gộp dữ liệu từ nhiều file Excel khác nhau  
- Chọn sheet, chỉnh sửa dữ liệu trước khi gộp  
- Ghi dữ liệu vào một file form có sẵn (giữ nguyên định dạng)  
- Xuất file Excel mới  
- Theo dõi tiến trình qua vùng log realtime  

Ứng dụng chạy trên nền web (Streamlit), dễ sử dụng, không cần cài đặt phức tạp.

---

## 2. Cách chạy chương trình

Bạn có 2 cách chạy:

### **Cách 1: Chạy ẩn CMD (khuyên dùng)**
Nhấp đôi vào file:

```
run_hidden.vbs
```

✔ Không hiện cửa sổ CMD  
✔ Chỉ mở giao diện web  

### **Cách 2: Chạy trực tiếp**
Nhấp đôi vào:

```
run_app.bat
```

---

## 3. Giao diện chính

Khi mở ứng dụng, bạn sẽ thấy:

- **Tiêu đề ứng dụng**
- **Vùng log** (hiển thị tiến trình)
- **Khu vực upload file**
- **Khu vực thiết lập gộp dữ liệu**
- **Khu vực xuất file**

---

## 4. Các bước sử dụng

---

## **Bước 1 – Upload file Excel**

Nhấn vào:

```
📂 Chọn file Excel
```

Bạn có thể chọn **nhiều file** cùng lúc.

---

## **Bước 2 – Chọn sheet cần gộp**

Với mỗi file:

1. Mở phần **Thiết lập cho: <tên file>**
2. Chọn sheet bạn muốn gộp
3. Xem trước dữ liệu của sheet
4. Chỉnh sửa dữ liệu nếu cần (xóa cột, sửa giá trị…)
5. Chọn dòng bắt đầu gộp

---

## **Bước 3 – Thiết lập file form**

Ở phần **Gộp và xuất file**, bạn sẽ:

1. Nhập tên file xuất (ví dụ: `ket_qua.xlsx`)
2. Chọn file Excel dùng làm form
3. Chọn sheet trong form
4. Xem trước form để xác định:
   - Dòng bắt đầu vùng dữ liệu
   - Dòng kết thúc vùng dữ liệu
5. Chọn cột bắt đầu ghi dữ liệu

---

## **Bước 4 – Gộp dữ liệu**

Nhấn nút:

```
Gộp file
```

Ứng dụng sẽ:

- Gộp dữ liệu từ các file bạn đã chọn  
- Hiển thị bảng kết quả  
- Ghi dữ liệu vào form Excel  
- Tạo file xuất  

---

## **Bước 5 – Tải file kết quả**

Sau khi xử lý xong, bạn sẽ thấy nút:

```
📥 Tải file kết quả
```

Nhấn để tải file Excel đã gộp.

---

## 5. Vùng Log – Theo dõi tiến trình

Vùng log hiển thị:

- Tiến trình xử lý  
- Các bước đang chạy  
- Cảnh báo  
- Lỗi (nếu có)  

Bạn không cần cuộn — log mới nhất luôn hiển thị.

---

## 6. Lỗi thường gặp & cách xử lý

### ❗ Không thấy file xuất
- Kiểm tra xem bạn đã chọn file form chưa  
- Kiểm tra dòng bắt đầu/kết thúc có hợp lệ không  

### ❗ Lỗi pywin32
- Đảm bảo bạn chạy bằng Windows  
- Đảm bảo máy có cài Microsoft Excel  

### ❗ Không gộp được dữ liệu
- Kiểm tra sheet có tồn tại không  
- Kiểm tra cột bạn chọn có đúng tên không  

---

## 7. Yêu cầu hệ thống

- Windows 10/11  
- Microsoft Excel đã cài đặt  
- Python + Streamlit (đã được tự động cài qua setup)  

---

## 8. Hỗ trợ

Nếu bạn gặp lỗi hoặc cần nâng cấp tính năng, hãy liên hệ người quản lý dự án hoặc người phát triển.

