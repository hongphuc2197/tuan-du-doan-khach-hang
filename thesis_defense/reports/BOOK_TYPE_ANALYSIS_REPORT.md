# 📚 BÁO CÁO PHÂN TÍCH KHÁCH HÀNG TIỀM NĂNG THEO LOẠI SÁCH

## 🎯 Tổng Quan

Hệ thống đã được cập nhật để phân tích khách hàng tiềm năng theo **12 loại sách** dựa trên danh sách từ hình ảnh bạn cung cấp.

## 📊 Các Loại Sách Được Phân Tích

| Product ID | Loại Sách | Số Records |
|------------|-----------|------------|
| 1 | Công nghệ giáo dục | 156 |
| 2 | Phương pháp giảng dạy | 154 |
| 3 | Công nghệ thông tin | 139 |
| 4 | Thiết kế web | 165 |
| 5 | Lập trình | 152 |
| 6 | Nghiên cứu khoa học | 141 |
| 7 | Giáo dục STEM | 166 |
| 8 | Giảng dạy tiếng Anh | 138 |
| 9 | Thiết kế | 134 |
| 10 | Cơ sở dữ liệu | 159 |
| 11 | Phát triển ứng dụng | 156 |
| 12 | Công nghệ giáo dục | 153 |

## 🏆 Top Loại Sách Được Khách Hàng Tiềm Năng Yêu Thích

### 1. Công nghệ giáo dục (43.7%)
- 👥 **Khách hàng**: 155/355 (43.7%)
- 📚 **Tổng sách**: 205
- 📊 **TB/khách hàng**: 0.6

### 2. Thiết kế web (28.5%)
- 👥 **Khách hàng**: 101/355 (28.5%)
- 📚 **Tổng sách**: 121
- 📊 **TB/khách hàng**: 0.3

### 3. Giáo dục STEM (27.0%)
- 👥 **Khách hàng**: 96/355 (27.0%)
- 📚 **Tổng sách**: 112
- 📊 **TB/khách hàng**: 0.3

### 4. Phát triển ứng dụng (27.0%)
- 👥 **Khách hàng**: 96/355 (27.0%)
- 📚 **Tổng sách**: 111
- 📊 **TB/khách hàng**: 0.3

### 5. Lập trình (27.0%)
- 👥 **Khách hàng**: 96/355 (27.0%)
- 📚 **Tổng sách**: 111
- 📊 **TB/khách hàng**: 0.3

## 📈 Thống Kê Tổng Quan

- **Tổng số khách hàng**: 576
- **Khách hàng tiềm năng**: 576 (100%)
- **Tuổi trung bình**: 21.5
- **Chi tiêu trung bình**: 469,618 VNĐ
- **Thu nhập trung bình**: 2,958,774 VNĐ

## 🎯 Top 10 Khách Hàng Tiềm Năng

| Tên | Tuổi | Thu Nhập | Chi Tiêu | Loại Sách Yêu Thích |
|-----|------|----------|----------|---------------------|
| Tô Huy | 21 | 3,305,594 | 321,726 | Công nghệ thông tin |
| Nguyễn Quang | 25 | 3,285,820 | 418,941 | Lập trình |
| Hồ Thảo | 22 | 2,445,492 | 241,531 | Nghiên cứu khoa học |
| Bùi Hương | 23 | 3,089,069 | 191,810 | Công nghệ giáo dục |
| Tô Linh | 25 | 4,977,810 | 755,945 | Phát triển ứng dụng |
| Võ Long | 20 | 1,351,873 | 149,193 | Thiết kế |
| Đinh Nga | 19 | 1,245,392 | 266,628 | Giảng dạy tiếng Anh |
| Đặng Hùng | 20 | 1,956,825 | 490,158 | Giáo dục STEM |
| Đào Hoa | 18 | 1,166,797 | 242,804 | Công nghệ giáo dục |
| Tô Hạnh | 20 | 2,045,371 | 721,821 | Lập trình |

## 💡 Insights Chính

### 🔥 Loại Sách Hot Nhất
**Công nghệ giáo dục** - 43.7% khách hàng tiềm năng quan tâm

### 📊 Phân Bố Theo Độ Tuổi
- **18-20**: 213 khách hàng (37.0%)
- **21-23**: 213 khách hàng (37.0%)
- **24-25**: 150 khách hàng (26.0%)

### 📚 Phân Bố Trình Độ Học Vấn
- **Basic**: 398 khách hàng (69.1%)
- **Graduation**: 173 khách hàng (30.0%)
- **Master**: 5 khách hàng (0.9%)

### 💰 Phân Bố Mức Thu Nhập
- **Medium**: 429 khách hàng (74.5%)
- **Low**: 147 khách hàng (25.5%)

## 🛠️ Các File Đã Tạo

### 📁 Analytics Files
- `analytics/potential_customers.json` - Top 100 khách hàng tiềm năng
- `analytics/all_customers.json` - Tất cả 576 khách hàng
- `analytics/analytics_data.json` - Thống kê tổng quan với phân tích loại sách
- `analytics/book_type_analysis.png` - Biểu đồ phân tích theo loại sách

### 📁 Backend Files
- `project-web/BE/potential_customers.json`
- `project-web/BE/all_customers.json`
- `project-web/BE/analytics_data.json`
- `project-web/BE/book_type_analysis.png`

### 📁 Frontend Components
- `project-web/FE/src/components/BookTypeAnalysis.js`
- `project-web/FE/src/components/BookTypeAnalysis.css`

## 🚀 Cách Sử Dụng

### 1. Khởi động Backend
```bash
cd project-web/BE && npm start
```

### 2. Khởi động Frontend
```bash
cd project-web/FE && npm start
```

### 3. Truy cập Component Mới
Thêm `BookTypeAnalysis` component vào ứng dụng để hiển thị phân tích theo loại sách.

## 📊 API Endpoints

- `GET /api/analytics` - Lấy thống kê tổng quan với phân tích loại sách
- `GET /api/potential-customers` - Lấy khách hàng tiềm năng với thông tin loại sách
- `GET /api/all-customers` - Lấy tất cả khách hàng với thông tin loại sách

## ✨ Tính Năng Mới

1. **Phân tích theo loại sách**: Mỗi khách hàng được phân tích theo sở thích sách
2. **Loại sách yêu thích**: Xác định loại sách mà khách hàng quan tâm nhất
3. **Biểu đồ trực quan**: Hiển thị phân tích theo loại sách
4. **Thống kê chi tiết**: Số lượng khách hàng, phần trăm, tổng sách bán được
5. **Component React**: Giao diện đẹp để hiển thị phân tích

## 🎯 Kết Luận

Hệ thống đã được nâng cấp thành công để phân tích khách hàng tiềm năng theo **12 loại sách** khác nhau. Điều này giúp:

- **Hiểu rõ sở thích** của từng khách hàng
- **Tối ưu hóa marketing** theo loại sách
- **Cá nhân hóa trải nghiệm** người dùng
- **Tăng hiệu quả bán hàng** thông qua phân tích chi tiết

🎊 **Hệ thống đã sẵn sàng để sử dụng!**
