import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Thiết lập font và style
plt.rcParams['font.family'] = ['DejaVu Sans']
plt.style.use('default')

print('📊 TẠO BIỂU ĐỒ FEATURE IMPORTANCE')
print('=' * 50)

# Dữ liệu từ kết quả training (lấy từ kết quả đã chạy)
features = ['total_actions', 'unique_products', 'total_spending', 'avg_spending', 'age', 'income_encoded', 'education_encoded']

# Feature importance từ Random Forest
rf_importance = [0.067877, 0.069348, 0.324712, 0.293655, 0.159855, 0.034851, 0.049702]

# Feature importance từ Gradient Boosting
gb_importance = [0.000516, 0.020839, 0.502674, 0.309984, 0.126699, 0.012385, 0.026904]

# Feature coefficients từ Logistic Regression (absolute values)
lr_coefficients = [0.238890, 0.275727, 0.000006, 0.000014, 0.067497, 0.080019, 0.215671]

# Tạo figure với 2 subplot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

# 1. Random Forest Feature Importance
colors_rf = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
bars1 = ax1.barh(features, rf_importance, color=colors_rf)
ax1.set_title('Random Forest - Feature Importance', fontsize=16, fontweight='bold', pad=20)
ax1.set_xlabel('Importance Score', fontsize=12)
ax1.set_ylabel('Features', fontsize=12)

# Thêm giá trị lên cột
for i, (bar, value) in enumerate(zip(bars1, rf_importance)):
    ax1.text(value + 0.005, bar.get_y() + bar.get_height()/2, 
             f'{value:.3f}', va='center', ha='left', fontweight='bold')

# 2. Gradient Boosting Feature Importance
colors_gb = ['#FF9FF3', '#54A0FF', '#5F27CD', '#00D2D3', '#FF9F43', '#EE5A24', '#C44569']
bars2 = ax2.barh(features, gb_importance, color=colors_gb)
ax2.set_title('Gradient Boosting - Feature Importance', fontsize=16, fontweight='bold', pad=20)
ax2.set_xlabel('Importance Score', fontsize=12)
ax2.set_ylabel('Features', fontsize=12)

# Thêm giá trị lên cột
for i, (bar, value) in enumerate(zip(bars2, gb_importance)):
    ax2.text(value + 0.005, bar.get_y() + bar.get_height()/2, 
             f'{value:.3f}', va='center', ha='left', fontweight='bold')

plt.tight_layout()
plt.savefig('feature_importance_comparison.png', dpi=300, bbox_inches='tight')
print('✅ Đã lưu biểu đồ so sánh: feature_importance_comparison.png')

# Tạo biểu đồ tổng hợp
fig2, ax = plt.subplots(1, 1, figsize=(15, 10))

# Tạo DataFrame để dễ vẽ
df_importance = pd.DataFrame({
    'Random Forest': rf_importance,
    'Gradient Boosting': gb_importance,
    'Logistic Regression': lr_coefficients
}, index=features)

# Vẽ biểu đồ grouped bar
x = np.arange(len(features))
width = 0.25

bars1 = ax.bar(x - width, df_importance['Random Forest'], width, label='Random Forest', color='#FF6B6B', alpha=0.8)
bars2 = ax.bar(x, df_importance['Gradient Boosting'], width, label='Gradient Boosting', color='#4ECDC4', alpha=0.8)
bars3 = ax.bar(x + width, df_importance['Logistic Regression'], width, label='Logistic Regression', color='#45B7D1', alpha=0.8)

ax.set_xlabel('Features', fontsize=12, fontweight='bold')
ax.set_ylabel('Importance Score', fontsize=12, fontweight='bold')
ax.set_title('So sánh Feature Importance giữa các mô hình', fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(features, rotation=45, ha='right')
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)

# Thêm giá trị lên cột
def add_value_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                f'{height:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

add_value_labels(bars1)
add_value_labels(bars2)
add_value_labels(bars3)

plt.tight_layout()
plt.savefig('feature_importance_all_models.png', dpi=300, bbox_inches='tight')
print('✅ Đã lưu biểu đồ tổng hợp: feature_importance_all_models.png')

# Tạo biểu đồ top features
fig3, ax = plt.subplots(1, 1, figsize=(12, 8))

# Tính điểm trung bình của tất cả mô hình
avg_importance = (np.array(rf_importance) + np.array(gb_importance) + np.array(lr_coefficients)) / 3

# Sắp xếp theo thứ tự giảm dần
sorted_indices = np.argsort(avg_importance)[::-1]
sorted_features = [features[i] for i in sorted_indices]
sorted_importance = [avg_importance[i] for i in sorted_indices]

# Vẽ biểu đồ
colors = plt.cm.viridis(np.linspace(0, 1, len(features)))
bars = ax.barh(sorted_features, sorted_importance, color=colors)

ax.set_title('Top Features - Trung bình từ tất cả mô hình', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Average Importance Score', fontsize=12, fontweight='bold')
ax.set_ylabel('Features', fontsize=12, fontweight='bold')

# Thêm giá trị lên cột
for i, (bar, value) in enumerate(zip(bars, sorted_importance)):
    ax.text(value + 0.01, bar.get_y() + bar.get_height()/2, 
            f'{value:.3f}', va='center', ha='left', fontweight='bold')

# Thêm grid
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('top_features_average.png', dpi=300, bbox_inches='tight')
print('✅ Đã lưu biểu đồ top features: top_features_average.png')

# In kết quả phân tích
print('\n=== PHÂN TÍCH FEATURE IMPORTANCE ===')
print('\n🏆 TOP 3 FEATURES QUAN TRỌNG NHẤT:')
for i, (feature, importance) in enumerate(zip(sorted_features[:3], sorted_importance[:3]), 1):
    print(f'{i}. {feature}: {importance:.3f}')

print('\n📊 PHÂN TÍCH CHI TIẾT:')
for i, feature in enumerate(features):
    rf_val = rf_importance[i]
    gb_val = gb_importance[i]
    lr_val = lr_coefficients[i]
    avg_val = avg_importance[i]
    print(f'{feature}:')
    print(f'  - Random Forest: {rf_val:.3f}')
    print(f'  - Gradient Boosting: {gb_val:.3f}')
    print(f'  - Logistic Regression: {lr_val:.3f}')
    print(f'  - Trung bình: {avg_val:.3f}')
    print()

plt.show()
print('\n🎉 Hoàn thành tạo biểu đồ Feature Importance!')
