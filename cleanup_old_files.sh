#!/bin/bash

echo "=================================================="
echo "DỌN DẸP FILES CŨ VÀ TRUNG LẶP"
echo "=================================================="

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Đếm số file sẽ xóa
total_files=0

echo -e "\n${YELLOW}📋 DANH SÁCH FILES SẼ XÓA:${NC}\n"

# 1. Python scripts cũ
echo -e "${YELLOW}1. Python scripts cũ/test (36 files):${NC}"
python_files=(
    "basic_chart.py"
    "basic_eda.py"
    "bright_correlation.py"
    "bright_correlation_heatmap.py"
    "colorful_heatmap.py"
    "correlation_chart.py"
    "correlation_heatmap.py"
    "create_bright_correlation_heatmap.py"
    "create_charts.py"
    "create_heatmap.py"
    "create_images.py"
    "eda_statistics.py"
    "eda_visualization.py"
    "feature_chart.py"
    "feature_importance_chart.py"
    "feature_importance_final.py"
    "feature_importance_plot.py"
    "gradient_boosting.py"
    "heatmap.py"
    "heatmap_bright.py"
    "heatmap_final.py"
    "heatmap_simple.py"
    "heatmap_with_colors.py"
    "logistic_regression.py"
    "model_comparison.py"
    "quick_eda.py"
    "quick_model_comparison.py"
    "random_forest.py"
    "simple_bright_heatmap.py"
    "simple_correlation.py"
    "simple_eda.py"
    "simple_feature_chart.py"
    "simple_feature_importance.py"
    "simple_heatmap.py"
    "simple_images.py"
    "svm.py"
    "svm_analysis.py"
    "text_charts.py"
)

for file in "${python_files[@]}"; do
    if [ -f "$file" ]; then
        echo "   - $file"
        ((total_files++))
    fi
done

# 2. Model/scaler files cũ
echo -e "\n${YELLOW}2. Model/scaler files cũ (5 files):${NC}"
model_files=(
    "best_model.pkl"
    "optimized_model.pkl"
    "optimized_scaler.pkl"
    "scaler.pkl"
    "model_results.csv"
)

for file in "${model_files[@]}"; do
    if [ -f "$file" ]; then
        echo "   - $file"
        ((total_files++))
    fi
done

# 3. PNG files cũ
echo -e "\n${YELLOW}3. PNG/Image files cũ (8 files):${NC}"
png_files=(
    "bright_correlation_heatmap_coolwarm.png"
    "bright_correlation_heatmap_rdbu.png"
    "bright_correlation_heatmap_rdylbu.png"
    "bright_correlation_heatmap_spectral.png"
    "correlation_heatmap.png"
    "feature_comparison.png"
    "gb_feature_importance.png"
    "heatmap.png"
    "rf_feature_importance.png"
    "simple_eda.png"
    "svm_performance.png"
)

for file in "${png_files[@]}"; do
    if [ -f "$file" ]; then
        echo "   - $file"
        ((total_files++))
    fi
done

# 4. README files trung lặp
echo -e "\n${YELLOW}4. README files trung lặp (4 files):${NC}"
readme_files=(
    "README_COMPLETE.md"
    "README_FINAL.md"
    "README_STUDENT_FINAL.md"
    "SUMMARY_FINAL.md"
)

for file in "${readme_files[@]}"; do
    if [ -f "$file" ]; then
        echo "   - $file"
        ((total_files++))
    fi
done

# Xác nhận
echo -e "\n${RED}⚠️  Tổng cộng: $total_files files sẽ bị xóa${NC}"
echo -e "${YELLOW}Files được giữ lại:${NC}"
echo "   ✅ user_actions_students_576.csv"
echo "   ✅ real_training.py, app.py"
echo "   ✅ run_full_pipeline.sh"
echo "   ✅ README.md, QUICK_START.md, RUN_RESULTS.md, SUMMARY.md"
echo "   ✅ eda_plots.png, correlation_matrix.png, feature_importance.png, model_comparison.png"
echo "   ✅ requirements.txt"
echo "   ✅ Tất cả files trong analytics/, project-web/, venv/"

echo -e "\n${YELLOW}Bạn có chắc chắn muốn xóa? (yes/no)${NC}"
read -r response

if [[ "$response" == "yes" ]]; then
    echo -e "\n${GREEN}Đang xóa files...${NC}"
    
    deleted_count=0
    
    # Xóa Python files
    for file in "${python_files[@]}"; do
        if [ -f "$file" ]; then
            rm "$file"
            echo "   ✓ Đã xóa: $file"
            ((deleted_count++))
        fi
    done
    
    # Xóa model files
    for file in "${model_files[@]}"; do
        if [ -f "$file" ]; then
            rm "$file"
            echo "   ✓ Đã xóa: $file"
            ((deleted_count++))
        fi
    done
    
    # Xóa PNG files
    for file in "${png_files[@]}"; do
        if [ -f "$file" ]; then
            rm "$file"
            echo "   ✓ Đã xóa: $file"
            ((deleted_count++))
        fi
    done
    
    # Xóa README files
    for file in "${readme_files[@]}"; do
        if [ -f "$file" ]; then
            rm "$file"
            echo "   ✓ Đã xóa: $file"
            ((deleted_count++))
        fi
    done
    
    # Xóa file cleanup list
    if [ -f "files_to_cleanup.txt" ]; then
        rm "files_to_cleanup.txt"
        echo "   ✓ Đã xóa: files_to_cleanup.txt"
        ((deleted_count++))
    fi
    
    echo -e "\n${GREEN}✅ HOÀN TẤT!${NC}"
    echo -e "${GREEN}Đã xóa $deleted_count files${NC}"
    echo -e "\n${YELLOW}Thư mục đã được dọn dẹp!${NC}"
    
else
    echo -e "\n${YELLOW}❌ Hủy bỏ. Không có file nào bị xóa.${NC}"
fi

echo -e "\n=================================================="

