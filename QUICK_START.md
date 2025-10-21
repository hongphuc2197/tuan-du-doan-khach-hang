# Hướng Dẫn Nhanh - Dự Án Dự Đoán Khách Hàng Tiềm Năng

## 📋 Tóm Tắt Dự Án

Hệ thống dự đoán khách hàng tiềm năng sử dụng Machine Learning với dữ liệu từ 1,813 sinh viên.

### Kết Quả Chính:
- ✅ **Mô hình tốt nhất**: Random Forest (F1-score: 30.2%)
- ✅ **Khách hàng tiềm năng**: 514 users (28.4%)
- ✅ **Dữ liệu đã xử lý**: JSON files sẵn sàng cho web app

## 🚀 Khởi Động Nhanh

### Cách 1: Sử dụng dữ liệu đã có (Nhanh)

Backend và Frontend có thể chạy ngay với dữ liệu đã được xử lý sẵn:

```bash
# Terminal 1 - Backend
cd project-web/BE
npm start
# Backend: http://localhost:5001

# Terminal 2 - Frontend  
cd project-web/FE
npm start
# Frontend: http://localhost:3000
```

### Cách 2: Chạy lại toàn bộ pipeline (Đầy đủ)

```bash
# Chạy script tự động
./run_full_pipeline.sh
```

Hoặc chạy từng bước:

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Training models
python real_training.py

# 3. Phân tích và tạo biểu đồ
cd analytics
python analyze_student_data.py

# 4. Dự đoán khách hàng tiềm năng
python predict_potential_customers.py
cd ..

# 5. Khởi động web app
# Terminal 1 - Backend
cd project-web/BE && npm start

# Terminal 2 - Frontend
cd project-web/FE && npm start
```

## 📊 Kết Quả Training

| Mô hình | Accuracy | Precision | Recall | F1-score |
|---------|----------|-----------|--------|----------|
| Logistic Regression | 70.2% | 0.0% | 0.0% | 0.0% |
| **Random Forest** ⭐ | **63.1%** | **34.5%** | **26.9%** | **30.2%** |
| Gradient Boosting | 68.0% | 30.0% | 5.6% | 9.4% |
| SVM | 69.7% | 0.0% | 0.0% | 0.0% |

## 📁 Files Quan Trọng

### Dữ Liệu
- `user_actions_students_576.csv` - Dữ liệu gốc
- `analytics/all_customers.json` - Tất cả khách hàng (1,813)
- `analytics/potential_customers.json` - Top 100 khách hàng tiềm năng
- `analytics/analytics_data.json` - Thống kê tổng quan

### Mô Hình
- `analytics/best_student_model.pkl` - Random Forest model

### Biểu Đồ
- `analytics/eda_plots.png` - Phân tích khám phá dữ liệu
- `analytics/correlation_matrix.png` - Ma trận tương quan
- `analytics/feature_importance.png` - Tầm quan trọng features
- `analytics/confusion_matrix.png` - Ma trận nhầm lẫn
- `analytics/model_comparison.png` - So sánh các mô hình

### Scripts
- `real_training.py` - Training models
- `analytics/analyze_student_data.py` - Phân tích và biểu đồ
- `analytics/predict_potential_customers.py` - Dự đoán
- `run_full_pipeline.sh` - Script tự động chạy toàn bộ

## 🌐 API Endpoints

Backend API (http://localhost:5001):

- `GET /api/customers` - Lấy tất cả khách hàng
- `GET /api/potential-customers` - Lấy khách hàng tiềm năng
- `GET /api/analytics` - Lấy thống kê
- `POST /api/predict` - Dự đoán khách hàng mới
- `GET /api/health` - Kiểm tra server
- `GET /images/<filename>.png` - Lấy biểu đồ

## 📈 Thống Kê Dữ Liệu

### Tổng Quan
- Tổng số khách hàng: 1,813
- Khách hàng tiềm năng: 514 (28.4%)
- Tuổi trung bình: 21.6
- Chi tiêu trung bình: 149,200 VNĐ

### Phân Bố Độ Tuổi
- 18-20: 650 (35.9%)
- 21-23: 676 (37.3%)
- 24-25: 487 (26.9%)

### Trình Độ
- Basic: 1,230 (67.8%)
- Graduation: 561 (30.9%)
- Master: 22 (1.2%)

### Mức Thu Nhập
- Medium: 1,332 (73.5%)
- Low: 481 (26.5%)

## 🎯 Top 10 Khách Hàng Tiềm Năng

1. Phạm Thị Nhật - 99.0% (Chi tiêu: 192,765 VNĐ)
2. Lê Hồng Nhật - 98.0% (Chi tiêu: 192,315 VNĐ)
3. Trần Hải Linh - 97.0% (Chi tiêu: 183,973 VNĐ)
4. Trần Kiều Hoa - 97.0% (Chi tiêu: 239,765 VNĐ)
5. Trần Thu Hoa - 97.0% (Chi tiêu: 238,006 VNĐ)
6. Nguyễn Tuấn An - 97.0% (Chi tiêu: 183,855 VNĐ)
7. Lê Tuấn Huy - 96.0% (Chi tiêu: 160,033 VNĐ)
8. Nguyễn Hưng An - 96.0% (Chi tiêu: 184,119 VNĐ)
9. Nguyễn Anh Ly - 95.0% (Chi tiêu: 164,203 VNĐ)
10. Trần Văn My - 95.0% (Chi tiêu: 107,288 VNĐ)

## 🔧 Troubleshooting

### Lỗi "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Lỗi "Port already in use"
```bash
# Thay đổi port trong server.js hoặc kill process:
lsof -ti:5001 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

### Backend không khởi động
```bash
cd project-web/BE
npm install
npm start
```

### Frontend không khởi động
```bash
cd project-web/FE
npm install
npm start
```

## 📚 Tài Liệu Chi Tiết

- `RUN_RESULTS.md` - Kết quả chi tiết
- `README.md` - Hướng dẫn tổng quan
- `analytics/model_evaluation_report.txt` - Báo cáo đánh giá

## 💡 Tips

1. **Performance**: Backend hiện sử dụng JSON files nên API rất nhanh
2. **Update dữ liệu**: Chạy `./run_full_pipeline.sh` để cập nhật
3. **Debug**: Check console logs trong browser và terminal
4. **Images**: Biểu đồ có thể xem qua API `/images/<filename>.png`

## ✅ Checklist

- [x] Training models hoàn tất
- [x] Phân tích dữ liệu hoàn tất  
- [x] Tạo biểu đồ hoàn tất
- [x] Dự đoán khách hàng hoàn tất
- [x] Backend cập nhật xong
- [x] JSON files sẵn sàng
- [x] Sẵn sàng chạy web app

## 🎉 Bắt Đầu

```bash
# Khởi động Backend
cd project-web/BE && npm start

# Khởi động Frontend (terminal khác)
cd project-web/FE && npm start

# Truy cập: http://localhost:3000
```

---

**Lưu ý**: Nếu cần chạy lại toàn bộ pipeline từ đầu, sử dụng script:
```bash
./run_full_pipeline.sh
```

