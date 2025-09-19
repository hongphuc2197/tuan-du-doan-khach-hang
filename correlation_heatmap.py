import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Thiết lập font và style
plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial', 'sans-serif']
plt.style.use('default')

print('🔥 TẠO HEATMAP MA TRẬN TƯƠNG QUAN')
print('=' * 50)

# Đọc dataset
df = pd.read_csv('user_actions_students_576.csv')
print(f'✅ Dataset: {len(df)} records, {df["user_id"].nunique()} users')

# Tạo features từ dữ liệu
user_behavior = df.groupby('user_id').agg({
    'event_type': lambda x: 'purchase' in x.values,
    'product_id': 'nunique',
    'price': ['sum', 'mean'],
    'age': 'first',
    'income_level': 'first',
    'education': 'first'
})

user_behavior['total_actions'] = df.groupby('user_id')['event_type'].count()
user_behavior.columns = ['is_potential', 'unique_products', 'total_spending', 'avg_spending', 'age', 'income_level', 'education', 'total_actions']

# Encode categorical variables
from sklearn.preprocessing import LabelEncoder
le_income = LabelEncoder()
le_education = LabelEncoder()
user_behavior['income_encoded'] = le_income.fit_transform(user_behavior['income_level'])
user_behavior['education_encoded'] = le_education.fit_transform(user_behavior['education'])

# Chuẩn bị dữ liệu cho correlation
numeric_features = ['total_actions', 'unique_products', 'total_spending', 'avg_spending', 'age', 'income_encoded', 'education_encoded', 'is_potential']
correlation_data = user_behavior[numeric_features]

print(f'✅ Features for correlation: {numeric_features}')

# Tính ma trận tương quan
correlation_matrix = correlation_data.corr()
print(f'✅ Correlation matrix shape: {correlation_matrix.shape}')

# Tạo heatmap với seaborn
plt.figure(figsize=(12, 10))

# Tạo mask để ẩn phần trên của ma trận (vì đối xứng)
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))

# Vẽ heatmap
sns.heatmap(correlation_matrix, 
            mask=mask,
            annot=True, 
            cmap='RdBu_r', 
            center=0,
            square=True, 
            fmt='.3f',
            cbar_kws={'shrink': 0.8},
            linewidths=0.5,
            annot_kws={'fontsize': 10, 'fontweight': 'bold'})

plt.title('Ma trận tương quan giữa các đặc trưng', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print('✅ Đã lưu: correlation_heatmap.png')

# Tạo heatmap với tên features tiếng Việt
feature_names_vi = ['Tổng hành động', 'Sản phẩm khác nhau', 'Tổng chi tiêu', 'Chi tiêu TB', 'Tuổi', 'Thu nhập', 'Học vấn', 'Có tiềm năng']
correlation_matrix_vi = correlation_matrix.copy()
correlation_matrix_vi.index = feature_names_vi
correlation_matrix_vi.columns = feature_names_vi

plt.figure(figsize=(12, 10))

# Tạo mask
mask = np.triu(np.ones_like(correlation_matrix_vi, dtype=bool))

# Vẽ heatmap với tên tiếng Việt
sns.heatmap(correlation_matrix_vi, 
            mask=mask,
            annot=True, 
            cmap='RdBu_r', 
            center=0,
            square=True, 
            fmt='.3f',
            cbar_kws={'shrink': 0.8},
            linewidths=0.5,
            annot_kws={'fontsize': 9, 'fontweight': 'bold'})

plt.title('Ma trận tương quan giữa các đặc trưng (Tiếng Việt)', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('correlation_heatmap_vi.png', dpi=300, bbox_inches='tight')
plt.close()
print('✅ Đã lưu: correlation_heatmap_vi.png')

# Tạo heatmap chỉ hiển thị correlations với target
target_correlations = correlation_matrix['is_potential'].drop('is_potential').sort_values(key=abs, ascending=False)

plt.figure(figsize=(10, 8))
colors = ['red' if x > 0 else 'blue' for x in target_correlations.values]
bars = plt.barh(range(len(target_correlations)), target_correlations.values, color=colors, alpha=0.7)

plt.yticks(range(len(target_correlations)), [feature_names_vi[i] for i in range(len(target_correlations))])
plt.xlabel('Hệ số tương quan với "Có tiềm năng"', fontsize=12, fontweight='bold')
plt.title('Tương quan giữa các đặc trưng và khách hàng tiềm năng', fontsize=14, fontweight='bold')
plt.axvline(x=0, color='black', linestyle='-', alpha=0.3)

# Thêm giá trị lên cột
for bar, value in zip(bars, target_correlations.values):
    plt.text(bar.get_width() + (0.01 if value > 0 else -0.01), bar.get_y() + bar.get_height()/2, 
             f'{value:.3f}', ha='left' if value > 0 else 'right', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('target_correlation.png', dpi=300, bbox_inches='tight')
plt.close()
print('✅ Đã lưu: target_correlation.png')

# In kết quả phân tích
print('\n=== PHÂN TÍCH MA TRẬN TƯƠNG QUAN ===')

print('\n🎯 TƯƠNG QUAN VỚI TARGET (Có tiềm năng):')
for i, (feature, corr) in enumerate(target_correlations.items(), 1):
    feature_name = feature_names_vi[numeric_features.index(feature)]
    direction = 'Tích cực' if corr > 0 else 'Tiêu cực'
    strength = 'Mạnh' if abs(corr) > 0.5 else 'Trung bình' if abs(corr) > 0.3 else 'Yếu'
    print(f'{i}. {feature_name}: {corr:.3f} ({direction}, {strength})')

print('\n🔥 TƯƠNG QUAN MẠNH GIỮA CÁC FEATURES:')
strong_correlations = []
for i in range(len(correlation_matrix.columns)):
    for j in range(i+1, len(correlation_matrix.columns)):
        corr_value = correlation_matrix.iloc[i, j]
        if abs(corr_value) > 0.5 and correlation_matrix.columns[i] != 'is_potential' and correlation_matrix.columns[j] != 'is_potential':
            strong_correlations.append((correlation_matrix.columns[i], correlation_matrix.columns[j], corr_value))

strong_correlations.sort(key=lambda x: abs(x[2]), reverse=True)
for i, (feat1, feat2, corr) in enumerate(strong_correlations[:5], 1):
    feat1_name = feature_names_vi[numeric_features.index(feat1)]
    feat2_name = feature_names_vi[numeric_features.index(feat2)]
    print(f'{i}. {feat1_name} ↔ {feat2_name}: {corr:.3f}')

print('\n📊 THỐNG KÊ TƯƠNG QUAN:')
print(f'Có {len(strong_correlations)} cặp features có tương quan mạnh (>0.5)')
print(f'Feature có tương quan mạnh nhất với target: {feature_names_vi[numeric_features.index(target_correlations.index[0])]} ({target_correlations.iloc[0]:.3f})')

print('\n🎉 Hoàn thành tạo heatmap ma trận tương quan!')
print('\n📁 Các file đã tạo:')
print('1. correlation_heatmap.png - Ma trận tương quan đầy đủ')
print('2. correlation_heatmap_vi.png - Ma trận tương quan (Tiếng Việt)')
print('3. target_correlation.png - Tương quan với target')
