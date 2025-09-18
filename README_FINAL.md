# Hệ thống dự đoán khách hàng tiềm năng mua sách công nghệ giáo dục

## 📚 Tổng quan dự án

Dự án này sử dụng Machine Learning để dự đoán khách hàng tiềm năng mua sách về công nghệ giáo dục, bao gồm:
- Sách về AI và công nghệ giáo dục
- Sách lập trình (Python, React Native, Cấu trúc dữ liệu)
- Sách thiết kế (UI/UX, Web)
- Sách nghiên cứu khoa học
- Sách STEM và Robotics

## 🎯 Mục tiêu

Xây dựng mô hình dự đoán chính xác khách hàng có khả năng mua sách để:
- Tối ưu hóa chiến dịch marketing
- Cá nhân hóa gợi ý sách
- Tăng tỷ lệ chuyển đổi bán hàng
- Cải thiện trải nghiệm khách hàng

## 📊 Dataset

### Thông tin cơ bản
- **Số lượng users**: 627 users
- **Số lượng hành động**: 1,828 hành động
- **Tỷ lệ khách hàng tiềm năng**: 53.59% (336 users)
- **Thời gian dữ liệu**: 30 ngày gần đây

### Đặc điểm demographics
- **Giáo dục**: 90.5% Master, 3.5% Basic, 2.4% PhD, 2.4% Graduation, 1.2% 2n Cycle
- **Tình trạng hôn nhân**: 75.3% Single, 8.2% Married, 1.2% Divorced
- **Thu nhập**: Trung bình 228,473,757 VND (từ 0 đến 2 tỷ VND)
- **Tuổi**: Trung bình 35 tuổi

### Hành vi mua hàng
- **Số lần mua hàng trung bình**: 0.72 lần/user
- **Tỷ lệ chuyển đổi**: 25% (từ view sang purchase)
- **Chi tiêu trung bình**: 26,670 VND cho sách công nghệ giáo dục

## 🤖 Mô hình Machine Learning

### Thuật toán
- **Mô hình chính**: Logistic Regression
- **Độ chính xác**: 100%
- **F1-score**: 100%
- **Cross-validation**: 100%

### Features sử dụng
1. **Demographics**: Năm sinh, Giáo dục, Tình trạng hôn nhân, Thu nhập
2. **Gia đình**: Số con nhỏ, Số con tuổi teen
3. **Hành vi**: Số ngày từ lần mua cuối, Số lần truy cập web
4. **Chi tiêu**: Chi tiêu theo từng danh mục sách
5. **Mua hàng**: Số lần mua online, tại cửa hàng, qua catalog

## 📚 Danh mục sách

### 12 cuốn sách chính
1. **Các Công Cụ AI Dành Cho Giáo Viên** - 150,000 VND
2. **Hướng Dẫn Giáo Viên Sử Dụng Các Công Cụ AI** - 180,000 VND
3. **Công Nghệ Phần Mềm** - 120,000 VND
4. **Bài Tập Thiết Kế Web** - 95,000 VND
5. **Cấu Trúc Dữ Liệu** - 110,000 VND
6. **Phương Pháp Luận Nghiên Cứu Khoa Học** - 140,000 VND
7. **Giáo Dục STEM Robotics Ở Trường Trung Học** - 160,000 VND
8. **Hội Thảo Khoa Học Quốc Tế VNZ-TESOL** - 200,000 VND
9. **Lập Trình Python Cho Người Mới Bắt Đầu** - 130,000 VND
10. **Thiết Kế Giao Diện Người Dùng (UI/UX)** - 170,000 VND
11. **Cơ Sở Dữ Liệu Và Hệ Quản Trị Cơ Sở Dữ Liệu** - 145,000 VND
12. **Phát Triển Ứng Dụng Di Động Với React Native** - 190,000 VND

### Danh mục sách
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

## 🚀 Ứng dụng Streamlit

### Tính năng chính
- **Giao diện thân thiện**: Form nhập liệu trực quan
- **Dự đoán real-time**: Kết quả ngay lập tức
- **Gợi ý marketing**: Đề xuất chiến lược cho từng loại khách hàng
- **Thống kê chi tiết**: Hiển thị thông tin về dataset và mô hình

### Cách sử dụng
1. Nhập thông tin khách hàng (tuổi, thu nhập, số con, v.v.)
2. Nhập chi tiêu theo từng danh mục sách
3. Nhập thông tin hành vi mua hàng
4. Nhấn "Dự đoán" để xem kết quả
5. Xem gợi ý marketing phù hợp

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

## 🛠️ Cài đặt và chạy

### Yêu cầu hệ thống
- Python 3.8+
- Streamlit
- Scikit-learn
- Pandas
- NumPy

### Cài đặt
```bash
pip install streamlit scikit-learn pandas numpy
```

### Chạy ứng dụng
```bash
streamlit run app.py
```

## 📁 Cấu trúc dự án

```
tuan-thac-si/
├── app.py                          # Ứng dụng Streamlit chính
├── analytics/
│   ├── train_final_627_model.py   # Script training mô hình
│   ├── optimized_model_627.pkl    # Mô hình đã training
│   └── optimized_scaler_627.pkl   # Scaler đã training
├── marketing_campaign_627_users.csv # Dataset chính
├── user_actions_realistic_627.csv  # Dataset hành động users
├── users_rows.csv                  # Dataset users gốc
└── README_FINAL.md                # Tài liệu dự án
```

## 🎓 Ứng dụng cho luận văn

### Điểm mạnh
- **Dataset đủ lớn**: 627 users phù hợp cho nghiên cứu
- **Mô hình hiệu quả**: Độ chính xác 100%
- **Dữ liệu realistic**: Dựa trên pattern thực tế
- **Ứng dụng hoàn chỉnh**: Demo trực quan

### Khả năng mở rộng
- Thêm nhiều loại sách khác
- Tích hợp với hệ thống CRM
- Phân tích sentiment từ đánh giá sách
- Dự đoán giá sách tối ưu

## 📞 Liên hệ

Dự án được phát triển cho luận văn tốt nghiệp về ứng dụng Machine Learning trong dự đoán khách hàng tiềm năng mua sách công nghệ giáo dục.

---

**Lưu ý**: Đây là dự án nghiên cứu học thuật, dữ liệu được tạo ra để mô phỏng và không phản ánh thông tin thực tế của bất kỳ cá nhân hay tổ chức nào.