# Frontend - Hệ thống Dự đoán Khách hàng Mua Sách Công nghệ Giáo dục

## 📚 Tổng quan

Ứng dụng web React được xây dựng để dự đoán khách hàng tiềm năng mua sách công nghệ giáo dục, bao gồm 12 cuốn sách chuyên về AI, lập trình, STEM và công nghệ giáo dục.

## 🎯 Tính năng chính

### 1. **Dự đoán khách hàng tiềm năng**
- Form nhập liệu thông tin khách hàng
- Dự đoán real-time với độ tin cậy cao
- Gợi ý marketing phù hợp cho từng loại khách hàng

### 2. **Danh mục sách**
- Hiển thị 12 cuốn sách công nghệ giáo dục
- Lọc theo danh mục (11 danh mục)
- Thông tin chi tiết: giá, tác giả, mô tả, ISBN

### 3. **Phân tích dữ liệu**
- Biểu đồ phân phối khách hàng
- Thống kê theo độ tuổi, học vấn, thu nhập
- Phân tích chi tiêu theo danh mục sách
- Thống kê kênh mua hàng và hành vi khách hàng

### 4. **Danh sách khách hàng**
- Hiển thị danh sách khách hàng tiềm năng
- Thông tin chi tiết về từng khách hàng

## 📚 Danh mục sách

### 12 Cuốn sách chính:
1. **Các Công Cụ AI Dành Cho Giáo Viên** - 150,000 VNĐ
2. **Hướng Dẫn Giáo Viên Sử Dụng Các Công Cụ AI** - 180,000 VNĐ
3. **Công Nghệ Phần Mềm** - 120,000 VNĐ
4. **Bài Tập Thiết Kế Web** - 95,000 VNĐ
5. **Cấu Trúc Dữ Liệu** - 110,000 VNĐ
6. **Phương Pháp Luận Nghiên Cứu Khoa Học** - 140,000 VNĐ
7. **Giáo Dục STEM Robotics Ở Trường Trung Học** - 160,000 VNĐ
8. **Hội Thảo Khoa Học Quốc Tế VNZ-TESOL** - 200,000 VNĐ
9. **Lập Trình Python Cho Người Mới Bắt Đầu** - 130,000 VNĐ
10. **Thiết Kế Giao Diện Người Dùng (UI/UX)** - 170,000 VNĐ
11. **Cơ Sở Dữ Liệu Và Hệ Quản Trị Cơ Sở Dữ Liệu** - 145,000 VNĐ
12. **Phát Triển Ứng Dụng Di Động Với React Native** - 190,000 VNĐ

### 11 Danh mục sách:
- Công nghệ giáo dục
- Phương pháp giảng dạy
- Công nghệ thông tin
- Thiết kế web
- Lập trình
- Nghiên cứu khoa học
- Giáo dục STEM
- Giảng dạy tiếng Anh
- Thiết kế
- Cơ sở dữ liệu
- Phát triển ứng dụng

## 🛠️ Công nghệ sử dụng

- **React 18** - Framework chính
- **Material-UI (MUI)** - UI components
- **Chart.js** - Biểu đồ và trực quan hóa
- **Axios** - HTTP client
- **React Router** - Điều hướng

## 📦 Cài đặt và chạy

### Yêu cầu hệ thống
- Node.js 16+
- npm hoặc yarn

### Cài đặt
```bash
cd project-web/FE
npm install
```

### Chạy ứng dụng
```bash
npm start
```

Ứng dụng sẽ chạy tại `http://localhost:3000`

## 📁 Cấu trúc dự án

```
FE/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── AnalyticsDashboard.js    # Dashboard phân tích
│   │   ├── BookList.js              # Danh mục sách
│   │   ├── CustomerList.js          # Danh sách khách hàng
│   │   ├── Navbar.js                # Navigation bar
│   │   └── PredictionForm.js        # Form dự đoán
│   ├── pages/
│   │   └── HomePage.js              # Trang chủ
│   ├── services/
│   │   └── customerService.js       # API services
│   ├── App.js                       # App component chính
│   └── index.js                     # Entry point
├── package.json
└── README.md
```

## 🎨 Giao diện

### Trang chủ có 4 tab:
1. **Dự đoán khách hàng tiềm năng** - Form nhập liệu và dự đoán
2. **Danh mục sách** - Hiển thị 12 cuốn sách với filter
3. **Danh sách khách hàng** - Danh sách khách hàng tiềm năng
4. **Phân tích dữ liệu** - Dashboard với biểu đồ và thống kê

### Tính năng UI:
- **Responsive design** - Tương thích mobile và desktop
- **Material Design** - Giao diện hiện đại, thân thiện
- **Interactive charts** - Biểu đồ tương tác với Chart.js
- **Filter system** - Lọc sách theo danh mục
- **Real-time prediction** - Dự đoán ngay lập tức

## 🔗 Kết nối Backend

Ứng dụng kết nối với backend API tại `http://localhost:3001` để:
- Dự đoán khách hàng tiềm năng
- Lấy dữ liệu phân tích
- Quản lý danh sách khách hàng

## 📊 Dữ liệu hiển thị

### Thống kê chính:
- **627 users** trong dataset
- **336 khách hàng tiềm năng (53.59%)**
- **11 danh mục sách** đa dạng
- **Giá sách từ 95,000 - 200,000 VNĐ**

### Biểu đồ:
- Phân phối khách hàng tiềm năng
- Phân khúc độ tuổi
- Phân tích theo học vấn và thu nhập
- Chi tiêu theo danh mục sách
- Thống kê kênh mua hàng

## 🚀 Triển khai

### Build production
```bash
npm run build
```

### Deploy
Có thể deploy lên các platform như:
- Vercel
- Netlify
- AWS S3 + CloudFront
- Heroku

## 📝 Ghi chú

- Ứng dụng được thiết kế cho luận văn tốt nghiệp
- Dữ liệu mô phỏng, không phản ánh thông tin thực tế
- Tập trung vào ngành sách công nghệ giáo dục
- Giao diện thân thiện, dễ sử dụng

---

**Phát triển bởi**: NXB Đại Học Sư Phạm  
**Mục đích**: Luận văn tốt nghiệp về ứng dụng Machine Learning trong dự đoán khách hàng tiềm năng mua sách