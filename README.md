# Customer Prediction System

Hệ thống dự đoán khách hàng tiềm năng sử dụng Machine Learning và Web Application.

## Cấu trúc dự án

```
project-root/
├── analytics/                    # Thư mục chứa logic xử lý Python
│   ├── analyze.py               # Phân tích dữ liệu và tạo biểu đồ
│   ├── predict_all.py           # Dự đoán khách hàng tiềm năng
│   ├── train_models.py          # Huấn luyện các mô hình ML
│   ├── optimize_model.py        # Tối ưu hóa mô hình
│   └── predict.py               # API dự đoán
├── project-web/
│   ├── BE/                      # Backend Express.js
│   │   ├── server.js
│   │   └── package.json
│   └── FE/                      # Frontend React.js
│       ├── src/
│       └── package.json
└── README.md
```

## Yêu cầu hệ thống

- Python 3.8+
- Node.js 14+
- npm hoặc yarn

## Cài đặt

### 1. Cài đặt môi trường Python

```bash
# Tạo và kích hoạt môi trường ảo
python -m venv venv
source venv/bin/activate  # Trên Windows: venv\Scripts\activate

# Cài đặt các thư viện Python
pip install -r requirements.txt
```

### 2. Cài đặt Backend

```bash
cd project-web/BE
npm install
```

### 3. Cài đặt Frontend

```bash
cd project-web/FE
npm install
```

## Chạy ứng dụng

### 1. Khởi động Backend

```bash
cd project-web/BE
npm start
```

Backend sẽ chạy tại: http://localhost:5000

### 2. Khởi động Frontend

```bash
cd project-web/FE
npm start
```

Frontend sẽ chạy tại: http://localhost:3000

## Dữ liệu

Dự án sử dụng dataset `marketing_campaign.csv` với 2242 mẫu dữ liệu. Các file dữ liệu và model đã được bỏ qua trong git để giảm kích thước repository. Để có được dữ liệu:

1. Tải file `marketing_campaign.csv` từ nguồn dữ liệu
2. Đặt file vào thư mục gốc của dự án
3. Chạy các script Python để tạo model và phân tích dữ liệu

## API Endpoints

### Backend API

- `GET /`: Trang chủ API
- `GET /api/test`: Kiểm tra API
- `GET /api/customers`: Lấy danh sách khách hàng
- `POST /api/predict`: Dự đoán khách hàng tiềm năng
- `GET /api/analytics`: Lấy kết quả phân tích
- `GET /api/potential-customers`: Lấy danh sách khách hàng tiềm năng
- `GET /api/health`: Kiểm tra trạng thái hệ thống

## Phân tích dữ liệu

Dự án bao gồm các phân tích sau:

1. Phân tích thống kê cơ bản
2. Phân tích tương quan giữa các biến
3. Phân tích phân khúc khách hàng
4. Phân tích chi tiêu và hành vi mua hàng
5. Dự đoán khách hàng tiềm năng

## Công nghệ sử dụng

### Backend
- Python
  - pandas, numpy
  - scikit-learn
  - joblib
- Node.js
  - Express.js
  - PythonShell

### Frontend
- React.js
- Material-UI
- Axios

## Đóng góp

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push lên branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## Giấy phép

MIT License - xem file [LICENSE](LICENSE) để biết thêm chi tiết. 