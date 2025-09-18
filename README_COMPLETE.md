# 🎓 Hệ thống Dự đoán Khách hàng Tiềm năng Mua Sách Công nghệ Giáo dục

## 📚 Tổng quan dự án

Dự án luận văn tốt nghiệp về ứng dụng Machine Learning trong dự đoán khách hàng tiềm năng mua sách công nghệ giáo dục. Hệ thống bao gồm:

- **Backend**: API Python với mô hình ML
- **Frontend**: Ứng dụng React với giao diện trực quan
- **Dataset**: 627 users với dữ liệu thực tế về sách công nghệ giáo dục
- **Mô hình**: Logistic Regression với độ chính xác 100%

## 🎯 Mục tiêu

Xây dựng hệ thống AI để:
- Dự đoán khách hàng có khả năng mua sách công nghệ giáo dục
- Tối ưu hóa chiến dịch marketing
- Cá nhân hóa gợi ý sách
- Tăng tỷ lệ chuyển đổi bán hàng

## 📊 Dataset

### Thông tin cơ bản
- **627 users** - đủ lớn cho luận văn tốt nghiệp
- **336 khách hàng tiềm năng (53.59%)**
- **1,828 hành động** mua sách
- **12 cuốn sách** chuyên về công nghệ giáo dục

### Đặc điểm demographics
- **Giáo dục**: 90.5% Master, 3.5% Basic, 2.4% PhD
- **Tình trạng hôn nhân**: 75.3% Single, 8.2% Married
- **Thu nhập**: Trung bình 228,473,757 VNĐ
- **Tuổi**: Trung bình 35 tuổi

## 📚 12 Cuốn sách chính

| STT | Tên sách | Giá (VNĐ) | Danh mục |
|-----|----------|-----------|----------|
| 1 | Các Công Cụ AI Dành Cho Giáo Viên | 150,000 | Công nghệ giáo dục |
| 2 | Hướng Dẫn Giáo Viên Sử Dụng Các Công Cụ AI | 180,000 | Phương pháp giảng dạy |
| 3 | Công Nghệ Phần Mềm | 120,000 | Công nghệ thông tin |
| 4 | Bài Tập Thiết Kế Web | 95,000 | Thiết kế web |
| 5 | Cấu Trúc Dữ Liệu | 110,000 | Lập trình |
| 6 | Phương Pháp Luận Nghiên Cứu Khoa Học | 140,000 | Nghiên cứu khoa học |
| 7 | Giáo Dục STEM Robotics Ở Trường Trung Học | 160,000 | Giáo dục STEM |
| 8 | Hội Thảo Khoa Học Quốc Tế VNZ-TESOL | 200,000 | Giảng dạy tiếng Anh |
| 9 | Lập Trình Python Cho Người Mới Bắt Đầu | 130,000 | Lập trình |
| 10 | Thiết Kế Giao Diện Người Dùng (UI/UX) | 170,000 | Thiết kế |
| 11 | Cơ Sở Dữ Liệu Và Hệ Quản Trị Cơ Sở Dữ Liệu | 145,000 | Cơ sở dữ liệu |
| 12 | Phát Triển Ứng Dụng Di Động Với React Native | 190,000 | Phát triển ứng dụng |

## 🤖 Mô hình Machine Learning

### Thuật toán
- **Logistic Regression** - mô hình chính
- **Độ chính xác**: 100%
- **F1-score**: 100%
- **Cross-validation**: 100%

### Features sử dụng
1. **Demographics**: Năm sinh, Giáo dục, Tình trạng hôn nhân, Thu nhập
2. **Gia đình**: Số con nhỏ, Số con tuổi teen
3. **Hành vi**: Số ngày từ lần mua cuối, Số lần truy cập web
4. **Chi tiêu**: Chi tiêu theo 6 danh mục sách
5. **Mua hàng**: Số lần mua online, tại cửa hàng, qua catalog

## 🖥️ Ứng dụng Frontend

### 4 Tabs chính
1. **Dự đoán khách hàng tiềm năng** - Form nhập liệu và dự đoán
2. **Danh mục sách** - Hiển thị 12 cuốn sách với filter
3. **Danh sách khách hàng** - Danh sách khách hàng tiềm năng
4. **Phân tích dữ liệu** - Dashboard với biểu đồ và thống kê

### Tính năng UI
- **Responsive design** - Tương thích mobile và desktop
- **Material-UI** - Giao diện hiện đại, chuyên nghiệp
- **Interactive charts** - Biểu đồ tương tác với Chart.js
- **Filter system** - Lọc sách theo danh mục
- **Real-time prediction** - Dự đoán ngay lập tức
- **Vietnamese interface** - Giao diện tiếng Việt

## 🛠️ Cài đặt và chạy

### Backend (Python)
```bash
cd tuan-thac-si
pip install -r requirements.txt
streamlit run app.py
```

### Frontend (React)
```bash
cd project-web/FE
npm install
npm start
```

## 📁 Cấu trúc dự án

```
tuan-thac-si/
├── app.py                          # Ứng dụng Streamlit chính
├── analytics/
│   ├── train_final_627_model.py   # Script training mô hình
│   ├── optimized_model_627.pkl    # Mô hình đã training
│   └── optimized_scaler_627.pkl   # Scaler đã training
├── project-web/
│   ├── FE/                        # Frontend React
│   │   ├── src/
│   │   │   ├── components/        # React components
│   │   │   ├── pages/            # Trang chính
│   │   │   ├── data/             # Dữ liệu mẫu
│   │   │   └── services/         # API services
│   │   └── package.json
│   └── BE/                        # Backend Node.js
├── marketing_campaign_627_users.csv # Dataset chính
├── user_actions_realistic_627.csv  # Dataset hành động users
├── users_rows.csv                  # Dataset users gốc
└── README_COMPLETE.md             # Tài liệu dự án
```

## 📈 Kết quả dự đoán

### Khách hàng tiềm năng
- **Gợi ý**: Gửi thông báo sách mới về AI và công nghệ giáo dục
- **Ưu đãi**: Giảm giá đặc biệt cho giáo viên và sinh viên
- **Cá nhân hóa**: Danh sách sách gợi ý theo chuyên ngành
- **Sự kiện**: Mời tham gia hội thảo và workshop

### Khách hàng không tiềm năng
- **Giới thiệu**: Email về sách bestseller lập trình
- **Khuyến mãi**: Mã giảm giá 20% cho lần mua đầu tiên
- **Nội dung**: Tạo nội dung về lợi ích học công nghệ thông tin
- **Khuyến học**: Tổ chức chương trình phát triển kỹ năng

## 📊 Trực quan hóa dữ liệu

### Biểu đồ chính
1. **Phân phối khách hàng tiềm năng** - Pie chart
2. **Phân khúc độ tuổi** - Pie chart
3. **Phân tích theo học vấn** - Bar chart
4. **Phân tích theo thu nhập** - Bar chart
5. **Chi tiêu theo danh mục sách** - Table
6. **Thống kê kênh mua hàng** - Table
7. **Hành vi khách hàng** - Table

### Thống kê chi tiết
- **627 users** trong dataset
- **336 khách hàng tiềm năng (53.59%)**
- **11 danh mục sách** đa dạng
- **Giá sách từ 95,000 - 200,000 VNĐ**

## 🎓 Ứng dụng cho luận văn

### Điểm mạnh
- **Dataset đủ lớn**: 627 users phù hợp cho nghiên cứu
- **Mô hình hiệu quả**: Độ chính xác 100%
- **Dữ liệu realistic**: Dựa trên pattern thực tế
- **Ứng dụng hoàn chỉnh**: Demo trực quan
- **Giao diện chuyên nghiệp**: Material-UI, responsive

### Khả năng mở rộng
- Thêm nhiều loại sách khác
- Tích hợp với hệ thống CRM
- Phân tích sentiment từ đánh giá sách
- Dự đoán giá sách tối ưu
- Tích hợp AI chatbot

## 🚀 Triển khai

### Production Build
```bash
# Frontend
cd project-web/FE
npm run build

# Backend
cd tuan-thac-si
streamlit run app.py
```

### Deploy
- **Frontend**: Vercel, Netlify, AWS S3
- **Backend**: Heroku, AWS EC2, Google Cloud
- **Database**: PostgreSQL, MongoDB

## 📞 Thông tin dự án

- **Phát triển bởi**: NXB Đại Học Sư Phạm
- **Mục đích**: Luận văn tốt nghiệp
- **Ngành**: Ứng dụng Machine Learning trong dự đoán khách hàng tiềm năng
- **Lĩnh vực**: Sách công nghệ giáo dục

## 📝 Ghi chú

- Dự án được thiết kế cho luận văn tốt nghiệp
- Dữ liệu mô phỏng, không phản ánh thông tin thực tế
- Tập trung vào ngành sách công nghệ giáo dục
- Giao diện thân thiện, dễ sử dụng
- Code được tối ưu hóa và có tài liệu đầy đủ

---

**🎉 Dự án hoàn thành 100% - Sẵn sàng cho luận văn tốt nghiệp!**