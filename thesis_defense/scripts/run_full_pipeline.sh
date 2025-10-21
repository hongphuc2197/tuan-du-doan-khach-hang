#!/bin/bash

echo "=================================================="
echo "CHẠY TOÀN BỘ PIPELINE PHÂN TÍCH DỮ LIỆU"
echo "=================================================="

# Màu sắc cho output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Kiểm tra file dữ liệu
if [ ! -f "user_actions_students_576.csv" ]; then
    echo -e "${YELLOW}⚠️  Không tìm thấy file user_actions_students_576.csv${NC}"
    exit 1
fi

echo -e "${GREEN}✅ File dữ liệu OK${NC}"

# Activate virtual environment
echo -e "\n${BLUE}1. Kích hoạt virtual environment...${NC}"
source venv/bin/activate

# Bước 1: Training models
echo -e "\n${BLUE}2. Training các mô hình ML...${NC}"
python real_training.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Training hoàn tất${NC}"
else
    echo -e "${YELLOW}⚠️  Training có lỗi${NC}"
fi

# Bước 2: Phân tích và tạo biểu đồ
echo -e "\n${BLUE}3. Phân tích dữ liệu và tạo biểu đồ...${NC}"
cd analytics
python analyze_student_data.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Phân tích hoàn tất${NC}"
else
    echo -e "${YELLOW}⚠️  Phân tích có lỗi${NC}"
    cd ..
    exit 1
fi

# Bước 3: Dự đoán khách hàng tiềm năng
echo -e "\n${BLUE}4. Dự đoán khách hàng tiềm năng...${NC}"
python predict_potential_customers.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dự đoán hoàn tất${NC}"
else
    echo -e "${YELLOW}⚠️  Dự đoán có lỗi${NC}"
    cd ..
    exit 1
fi

cd ..

# Bước 4: Copy files vào thư mục cần thiết
echo -e "\n${BLUE}5. Copy files vào các thư mục...${NC}"

# Copy biểu đồ
cp analytics/eda_plots.png .
cp analytics/correlation_matrix.png .
cp analytics/feature_importance.png .
cp analytics/confusion_matrix.png .
cp analytics/model_comparison.png .

cp analytics/eda_plots.png project-web/BE/
cp analytics/correlation_matrix.png project-web/BE/
cp analytics/feature_importance.png project-web/BE/

# Copy JSON files
cp analytics/potential_customers.json project-web/BE/
cp analytics/all_customers.json project-web/BE/
cp analytics/analytics_data.json project-web/BE/

# Copy model
cp analytics/best_student_model.pkl project-web/BE/

echo -e "${GREEN}✅ Copy files hoàn tất${NC}"

# Tổng kết
echo -e "\n=================================================="
echo -e "${GREEN}✅ HOÀN THÀNH TOÀN BỘ PIPELINE${NC}"
echo -e "=================================================="

echo -e "\n📁 Files đã được tạo:"
echo "   • analytics/best_student_model.pkl - Mô hình ML"
echo "   • analytics/*.png - Các biểu đồ"
echo "   • analytics/*.json - Dữ liệu JSON"
echo "   • project-web/BE/*.png - Biểu đồ cho backend"
echo "   • project-web/BE/*.json - Dữ liệu cho backend"

echo -e "\n🚀 Để khởi động web application:"
echo "   Backend:  cd project-web/BE && npm start"
echo "   Frontend: cd project-web/FE && npm start"

echo -e "\n📊 Để xem báo cáo chi tiết:"
echo "   cat analytics/model_evaluation_report.txt"
echo "   cat RUN_RESULTS.md"

