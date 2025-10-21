# Kết Quả Chạy Lại Source Code

## Tổng Quan
Đã chạy lại toàn bộ source code với dữ liệu từ file `user_actions_students_576.csv`

## Dữ Liệu
- **File dữ liệu**: `user_actions_students_576.csv`
- **Tổng số records**: 1,813 records
- **Số lượng users**: 1,813 users duy nhất
- **Khách hàng tiềm năng**: 539 users (29.7%)

## Thống Kê Dữ Liệu

### Độ Tuổi
- Tuổi trung bình: 21.6
- Phân bố:
  - 18-20 tuổi: 650 (35.9%)
  - 21-23 tuổi: 676 (37.3%)
  - 24-25 tuổi: 487 (26.9%)

### Trình Độ Học Vấn
- Basic: 1,230 (67.8%)
- Graduation: 561 (30.9%)
- Master: 22 (1.2%)

### Thu Nhập
- Thu nhập trung bình: 2,913,673 VNĐ
- Mức thu nhập:
  - Medium: 1,332 (73.5%)
  - Low: 481 (26.5%)

### Chi Tiêu
- Chi tiêu trung bình: 149,200 VNĐ

## Kết Quả Training Model

### Các Mô Hình Đã Training
1. **Logistic Regression**
   - Accuracy: 0.7025 (70.2%)
   - Precision: 0.0000 (0.0%)
   - Recall: 0.0000 (0.0%)
   - F1-score: 0.0000 (0.0%)

2. **Random Forest** ⭐ (Tốt nhất)
   - Accuracy: 0.6309 (63.1%)
   - Precision: 0.3452 (34.5%)
   - Recall: 0.2685 (26.9%)
   - F1-score: 0.3021 (30.2%)

3. **Gradient Boosting**
   - Accuracy: 0.6804 (68.0%)
   - Precision: 0.3000 (30.0%)
   - Recall: 0.0556 (5.6%)
   - F1-score: 0.0938 (9.4%)

4. **SVM**
   - Accuracy: 0.6970 (69.7%)
   - Precision: 0.0000 (0.0%)
   - Recall: 0.0000 (0.0%)
   - F1-score: 0.0000 (0.0%)

### Mô Hình Tốt Nhất
- **Random Forest** với F1-score cao nhất: 0.3021

### Feature Importance (Random Forest)
1. avg_spending: 43.3%
2. total_spending: 42.5%
3. age: 10.3%
4. education_encoded: 2.3%
5. income_encoded: 1.6%

## Files Đã Tạo

### 1. Analytics Files (trong thư mục `analytics/`)
- ✅ `analyze_student_data.py` - Script phân tích dữ liệu
- ✅ `predict_potential_customers.py` - Script dự đoán khách hàng tiềm năng
- ✅ `best_student_model.pkl` - Mô hình ML tốt nhất (Random Forest)
- ✅ `model_evaluation_results.csv` - Kết quả đánh giá các mô hình
- ✅ `model_evaluation_report.txt` - Báo cáo chi tiết

### 2. Data Files (JSON)
- ✅ `potential_customers.json` - Top 100 khách hàng tiềm năng
- ✅ `all_customers.json` - Tất cả 1,813 khách hàng
- ✅ `analytics_data.json` - Thống kê tổng quan

### 3. Visualization Files (PNG)
- ✅ `eda_plots.png` - Biểu đồ phân tích khám phá dữ liệu
- ✅ `correlation_matrix.png` - Ma trận tương quan
- ✅ `model_comparison.png` - So sánh hiệu suất các mô hình
- ✅ `feature_importance.png` - Tầm quan trọng của features
- ✅ `confusion_matrix.png` - Ma trận nhầm lẫn

### 4. Backend Files
- ✅ Đã copy tất cả JSON files vào `project-web/BE/`
- ✅ Đã copy tất cả PNG files vào `project-web/BE/`
- ✅ Đã copy model file vào `project-web/BE/`
- ✅ Đã cập nhật `server.js` để sử dụng JSON files

## Cải Tiến Backend

### Thay đổi chính:
1. **Tăng tốc API**: Sử dụng JSON files thay vì gọi Python scripts mỗi lần request
2. **Fallback mechanism**: Vẫn giữ khả năng gọi Python scripts nếu JSON không tồn tại
3. **Static file serving**: Serve các biểu đồ PNG qua endpoint `/images/`

### Các Endpoints API:
- `GET /api/customers` - Lấy tất cả khách hàng (từ all_customers.json)
- `GET /api/potential-customers` - Lấy khách hàng tiềm năng (từ potential_customers.json)
- `GET /api/analytics` - Lấy thống kê tổng quan (từ analytics_data.json)
- `POST /api/predict` - Dự đoán một khách hàng mới
- `GET /api/health` - Kiểm tra trạng thái server
- `GET /images/<filename>.png` - Lấy các biểu đồ

## Top 10 Khách Hàng Tiềm Năng

| Tên | Tuổi | Thu nhập | Chi tiêu | Xác suất |
|-----|------|----------|----------|----------|
| Phạm Thị Nhật | 19 | 4,734,203 | 192,765 | 99.0% |
| Lê Hồng Nhật | 19 | 2,140,991 | 192,315 | 98.0% |
| Trần Hải Linh | 19 | 2,458,622 | 183,973 | 97.0% |
| Trần Kiều Hoa | 23 | 1,081,540 | 239,765 | 97.0% |
| Trần Thu Hoa | 22 | 1,828,399 | 238,006 | 97.0% |
| Nguyễn Tuấn An | 19 | 2,873,041 | 183,855 | 97.0% |
| Lê Tuấn Huy | 25 | 2,722,322 | 160,033 | 96.0% |
| Nguyễn Hưng An | 25 | 4,924,282 | 184,119 | 96.0% |
| Nguyễn Anh Ly | 22 | 1,010,514 | 164,203 | 95.0% |
| Trần Văn My | 21 | 1,464,803 | 107,288 | 95.0% |

## Cách Chạy Ứng Dụng

### 1. Backend
```bash
cd project-web/BE
npm install
npm start
# Server chạy tại: http://localhost:5001
```

### 2. Frontend
```bash
cd project-web/FE
npm install
npm start
# Frontend chạy tại: http://localhost:3000
```

### 3. Chạy lại training (nếu cần)
```bash
# Activate virtual environment
source venv/bin/activate

# Chạy training
python real_training.py

# Chạy phân tích và tạo biểu đồ
cd analytics
python analyze_student_data.py

# Tạo dữ liệu JSON cho web app
python predict_potential_customers.py
```

## Ghi Chú

### Vấn Đề Với Model Performance
- Các mô hình có độ chính xác không cao (F1-score tốt nhất chỉ 30.2%)
- Nguyên nhân:
  1. Dữ liệu có thể không cân bằng (29.7% positive class)
  2. Features hiện tại chưa đủ mạnh để phân biệt khách hàng tiềm năng
  3. Mỗi user chỉ có 1 action duy nhất trong dataset

### Đề Xuất Cải Thiện
1. **Thu thập thêm dữ liệu**: Cần nhiều actions hơn cho mỗi user
2. **Feature engineering**: Tạo thêm features từ:
   - Thời gian trong ngày
   - Ngày trong tuần
   - Lịch sử xem sản phẩm
   - Interaction với các categories khác nhau
3. **Class balancing**: Áp dụng SMOTE hoặc class weights
4. **Hyperparameter tuning**: Tối ưu parameters của Random Forest

## Kết Luận

✅ **Hoàn thành chạy lại toàn bộ source code với dữ liệu mới**

Tất cả các thành phần đã được cập nhật:
- ✅ Training models
- ✅ Tạo visualizations
- ✅ Dự đoán khách hàng tiềm năng
- ✅ Cập nhật backend API
- ✅ Sẵn sàng cho frontend

Web application có thể chạy ngay với dữ liệu đã được xử lý sẵn!

