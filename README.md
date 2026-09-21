# Chương Trình Thống Kê Sinh Viên Lớp Học & Vẽ Biểu Đồ Trực Quan

Chương trình được phát triển bằng ngôn ngữ **Python** trên môi trường ảo Anaconda **`kiemtra`**, sử dụng thư viện **Matplotlib** để kết xuất biểu đồ và **Flask** để phục vụ máy chủ web tại cổng **`5175`**.

---

## 1. Khởi chạy máy chủ Web (Cổng 5175)

### Cách 1: Sử dụng lệnh trực tiếp với Python của môi trường `kiemtra` (Khuyên dùng)
```powershell
& "C:\Users\Lenovo\anaconda3\envs\kiemtra\python.exe" "C:\Users\Lenovo\.gemini\antigravity-ide\scratch\kiemtra_sinhvien\main.py" --port 5175
```

### Cách 2: Kích hoạt Conda trước khi chạy
```powershell
conda activate kiemtra
cd "C:\Users\Lenovo\.gemini\antigravity-ide\scratch\kiemtra_sinhvien"
python main.py --port 5175
```

Sau đó mở trình duyệt web và truy cập:
👉 **[http://localhost:5175](http://localhost:5175)**

---

## 2. Khởi chạy ở chế độ dòng lệnh Console (CLI)
Nếu muốn nhập dữ liệu và xuất biểu đồ trực tiếp từ cửa sổ dòng lệnh:
```powershell
& "C:\Users\Lenovo\anaconda3\envs\kiemtra\python.exe" "C:\Users\Lenovo\.gemini\antigravity-ide\scratch\kiemtra_sinhvien\main.py" --cli
```

---

## 3. Các tính năng nổi bật
- **4 Chế độ nhập liệu thông minh cho một lớp học**:
  1. **Nam / Nữ**: Nhập số sinh viên Nam và Nữ trong lớp.
  2. **Học lực**: Nhập số lượng sinh viên theo từng mức (Xuất sắc, Giỏi, Khá, Trung bình, Yếu/Kém).
  3. **Tổ / Nhóm**: Nhập sĩ số theo từng tổ học tập (hỗ trợ thêm/xóa tổ linh hoạt).
  4. **Phổ điểm**: Nhập danh sách điểm thi/kiểm tra để tự động tính điểm trung bình, min, max và vẽ phổ điểm lớp.
- **Tùy chọn hiển thị**: Chuyển đổi mượt mà giữa **Biểu đồ Cột (Bar Chart)** và **Biểu đồ Tròn (Donut/Pie Chart)**.
- **Tùy chỉnh tên lớp học**: Tự do đặt tên lớp (ví dụ: `CNTT K21A`, `Lớp 12A1`).
- **Thẻ chỉ số (KPIs)** & Bảng thống kê chi tiết theo thời gian thực.
- **Tải ảnh biểu đồ PNG độ phân giải cao (300 DPI)**: Tự động lưu tệp `bieu_do_sinh_vien.png` và cho phép tải về với 1 cú click.
