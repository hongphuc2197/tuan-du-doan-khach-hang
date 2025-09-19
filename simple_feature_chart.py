import matplotlib.pyplot as plt
import numpy as np

print('📊 TẠO BIỂU ĐỒ FEATURE IMPORTANCE ĐƠN GIẢN')
print('=' * 50)

# Dữ liệu
features = ['Tổng hành động', 'Sản phẩm khác nhau', 'Tổng chi tiêu', 'Chi tiêu TB', 'Tuổi', 'Thu nhập', 'Học vấn']
rf_importance = [0.067877, 0.069348, 0.324712, 0.293655, 0.159855, 0.034851, 0.049702]
gb_importance = [0.000516, 0.020839, 0.502674, 0.309984, 0.126699, 0.012385, 0.026904]

# Tạo biểu đồ Random Forest
plt.figure(figsize=(12, 8))
bars = plt.barh(features, rf_importance, color='skyblue', alpha=0.7, edgecolor='black')
plt.title('Random Forest - Mức độ quan trọng đặc trưng', fontsize=14, fontweight='bold')
plt.xlabel('Mức độ quan trọng', fontsize=12)
plt.ylabel('Đặc trưng', fontsize=12)

# Thêm giá trị lên cột
for bar, value in zip(bars, rf_importance):
    plt.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2, 
             f'{value:.3f}', ha='left', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('rf_feature_importance.png', dpi=300, bbox_inches='tight')
plt.close()
print('✅ Đã tạo: rf_feature_importance.png')

# Tạo biểu đồ Gradient Boosting
plt.figure(figsize=(12, 8))
bars = plt.barh(features, gb_importance, color='lightgreen', alpha=0.7, edgecolor='black')
plt.title('Gradient Boosting - Mức độ quan trọng đặc trưng', fontsize=14, fontweight='bold')
plt.xlabel('Mức độ quan trọng', fontsize=12)
plt.ylabel('Đặc trưng', fontsize=12)

# Thêm giá trị lên cột
for bar, value in zip(bars, gb_importance):
    plt.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2, 
             f'{value:.3f}', ha='left', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('gb_feature_importance.png', dpi=300, bbox_inches='tight')
plt.close()
print('✅ Đã tạo: gb_feature_importance.png')

# Tạo biểu đồ so sánh
plt.figure(figsize=(15, 8))
x = np.arange(len(features))
width = 0.35

bars1 = plt.bar(x - width/2, rf_importance, width, label='Random Forest', color='skyblue', alpha=0.7)
bars2 = plt.bar(x + width/2, gb_importance, width, label='Gradient Boosting', color='lightgreen', alpha=0.7)

plt.xlabel('Đặc trưng', fontsize=12, fontweight='bold')
plt.ylabel('Mức độ quan trọng', fontsize=12, fontweight='bold')
plt.title('So sánh mức độ quan trọng đặc trưng', fontsize=14, fontweight='bold')
plt.xticks(x, features, rotation=45, ha='right')
plt.legend()

# Thêm giá trị lên cột
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                f'{height:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('feature_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print('✅ Đã tạo: feature_comparison.png')

# In kết quả
print('\n=== PHÂN TÍCH FEATURE IMPORTANCE ===')
print('\n🌲 RANDOM FOREST - Top Features:')
rf_df = list(zip(features, rf_importance))
rf_df.sort(key=lambda x: x[1], reverse=True)
for i, (feature, importance) in enumerate(rf_df, 1):
    print(f'{i}. {feature}: {importance:.3f}')

print('\n🚀 GRADIENT BOOSTING - Top Features:')
gb_df = list(zip(features, gb_importance))
gb_df.sort(key=lambda x: x[1], reverse=True)
for i, (feature, importance) in enumerate(gb_df, 1):
    print(f'{i}. {feature}: {importance:.3f}')

print('\n🎉 Hoàn thành tạo biểu đồ Feature Importance!')
