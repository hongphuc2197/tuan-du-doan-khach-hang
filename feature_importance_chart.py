import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Thiết lập font để hiển thị tiếng Việt
plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial', 'sans-serif']

print('📊 TẠO BIỂU ĐỒ FEATURE IMPORTANCE')
print('=' * 50)

# Dữ liệu từ kết quả training
features = ['total_actions', 'unique_products', 'total_spending', 'avg_spending', 'age', 'income_encoded', 'education_encoded']
feature_names = ['Tổng hành động', 'Sản phẩm khác nhau', 'Tổng chi tiêu', 'Chi tiêu TB', 'Tuổi', 'Thu nhập', 'Học vấn']

# Random Forest Feature Importance
rf_importance = [0.067877, 0.069348, 0.324712, 0.293655, 0.159855, 0.034851, 0.049702]

# Gradient Boosting Feature Importance  
gb_importance = [0.000516, 0.020839, 0.502674, 0.309984, 0.126699, 0.012385, 0.026904]

# Tạo figure với 2 subplot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

# 1. Random Forest Feature Importance
colors_rf = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
bars1 = ax1.barh(feature_names, rf_importance, color=colors_rf, alpha=0.8, edgecolor='black')

ax1.set_title('Random Forest - Mức độ quan trọng đặc trưng', fontsize=16, fontweight='bold', pad=20)
ax1.set_xlabel('Mức độ quan trọng', fontsize=12, fontweight='bold')
ax1.set_ylabel('Đặc trưng', fontsize=12, fontweight='bold')

# Thêm giá trị lên cột
for i, (bar, value) in enumerate(zip(bars1, rf_importance)):
    ax1.text(value + 0.005, bar.get_y() + bar.get_height()/2, 
             f'{value:.3f}', va='center', ha='left', fontweight='bold', fontsize=10)

# Thêm grid
ax1.grid(True, alpha=0.3, axis='x')

# 2. Gradient Boosting Feature Importance
colors_gb = ['#FF9FF3', '#54A0FF', '#5F27CD', '#00D2D3', '#FF9F43', '#EE5A24', '#C44569']
bars2 = ax2.barh(feature_names, gb_importance, color=colors_gb, alpha=0.8, edgecolor='black')

ax2.set_title('Gradient Boosting - Mức độ quan trọng đặc trưng', fontsize=16, fontweight='bold', pad=20)
ax2.set_xlabel('Mức độ quan trọng', fontsize=12, fontweight='bold')
ax2.set_ylabel('Đặc trưng', fontsize=12, fontweight='bold')

# Thêm giá trị lên cột
for i, (bar, value) in enumerate(zip(bars2, gb_importance)):
    ax2.text(value + 0.005, bar.get_y() + bar.get_height()/2, 
             f'{value:.3f}', va='center', ha='left', fontweight='bold', fontsize=10)

# Thêm grid
ax2.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('feature_importance_comparison.png', dpi=300, bbox_inches='tight')
print('✅ Đã lưu: feature_importance_comparison.png')

# Tạo biểu đồ tổng hợp
fig2, ax = plt.subplots(1, 1, figsize=(15, 10))

# Tạo DataFrame để dễ vẽ
df_importance = pd.DataFrame({
    'Random Forest': rf_importance,
    'Gradient Boosting': gb_importance
}, index=feature_names)

# Vẽ biểu đồ grouped bar
x = np.arange(len(feature_names))
width = 0.35

bars1 = ax.bar(x - width/2, df_importance['Random Forest'], width, 
               label='Random Forest', color='#FF6B6B', alpha=0.8, edgecolor='black')
bars2 = ax.bar(x + width/2, df_importance['Gradient Boosting'], width, 
               label='Gradient Boosting', color='#4ECDC4', alpha=0.8, edgecolor='black')

ax.set_xlabel('Đặc trưng', fontsize=12, fontweight='bold')
ax.set_ylabel('Mức độ quan trọng', fontsize=12, fontweight='bold')
ax.set_title('So sánh mức độ quan trọng đặc trưng giữa các mô hình', fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(feature_names, rotation=45, ha='right')
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)

# Thêm giá trị lên cột
def add_value_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                f'{height:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

add_value_labels(bars1)
add_value_labels(bars2)

plt.tight_layout()
plt.savefig('feature_importance_all_models.png', dpi=300, bbox_inches='tight')
print('✅ Đã lưu: feature_importance_all_models.png')

# Tạo biểu đồ top features
fig3, ax = plt.subplots(1, 1, figsize=(12, 8))

# Tính điểm trung bình của 2 mô hình
avg_importance = (np.array(rf_importance) + np.array(gb_importance)) / 2

# Sắp xếp theo thứ tự giảm dần
sorted_indices = np.argsort(avg_importance)[::-1]
sorted_features = [feature_names[i] for i in sorted_indices]
sorted_importance = [avg_importance[i] for i in sorted_indices]

# Vẽ biểu đồ
colors = plt.cm.viridis(np.linspace(0, 1, len(feature_names)))
bars = ax.barh(sorted_features, sorted_importance, color=colors, alpha=0.8, edgecolor='black')

ax.set_title('Top đặc trưng quan trọng nhất (Trung bình từ 2 mô hình)', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Mức độ quan trọng trung bình', fontsize=12, fontweight='bold')
ax.set_ylabel('Đặc trưng', fontsize=12, fontweight='bold')

# Thêm giá trị lên cột
for i, (bar, value) in enumerate(zip(bars, sorted_importance)):
    ax.text(value + 0.01, bar.get_y() + bar.get_height()/2, 
            f'{value:.3f}', va='center', ha='left', fontweight='bold')

# Thêm grid
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('top_features_average.png', dpi=300, bbox_inches='tight')
print('✅ Đã lưu: top_features_average.png')

# In kết quả phân tích
print('\n=== PHÂN TÍCH FEATURE IMPORTANCE ===')
print('\n🏆 TOP 3 ĐẶC TRƯNG QUAN TRỌNG NHẤT:')
for i, (feature, importance) in enumerate(zip(sorted_features[:3], sorted_importance[:3]), 1):
    print(f'{i}. {feature}: {importance:.3f}')

print('\n📊 PHÂN TÍCH CHI TIẾT:')
for i, feature in enumerate(feature_names):
    rf_val = rf_importance[i]
    gb_val = gb_importance[i]
    avg_val = avg_importance[i]
    print(f'{feature}:')
    print(f'  - Random Forest: {rf_val:.3f}')
    print(f'  - Gradient Boosting: {gb_val:.3f}')
    print(f'  - Trung bình: {avg_val:.3f}')
    print()

# Tạo biểu đồ pie chart cho top features
fig4, ax = plt.subplots(1, 1, figsize=(10, 8))

# Lấy top 5 features
top5_features = sorted_features[:5]
top5_importance = sorted_importance[:5]

# Tạo pie chart
colors_pie = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
wedges, texts, autotexts = ax.pie(top5_importance, labels=top5_features, autopct='%1.1f%%', 
                                  colors=colors_pie, startangle=90, textprops={'fontsize': 10})

ax.set_title('Phân bố mức độ quan trọng của Top 5 đặc trưng', fontsize=16, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('top5_features_pie.png', dpi=300, bbox_inches='tight')
print('✅ Đã lưu: top5_features_pie.png')

print('\n🎉 Hoàn thành tạo tất cả biểu đồ Feature Importance!')
print('\n📁 Các file đã tạo:')
print('1. feature_importance_comparison.png - So sánh 2 mô hình')
print('2. feature_importance_all_models.png - Biểu đồ tổng hợp')
print('3. top_features_average.png - Top features quan trọng nhất')
print('4. top5_features_pie.png - Pie chart top 5 features')
