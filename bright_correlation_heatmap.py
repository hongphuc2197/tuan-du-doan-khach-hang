import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print('🌈 TẠO CORRELATION HEATMAP VỚI MÀU SẮC SÁNG')
print('=' * 50)

# Đọc dữ liệu
df = pd.read_csv('user_actions_students_576.csv')

# Tạo features
user_behavior = df.groupby('user_id').agg({
    'event_type': lambda x: 'purchase' in x.values,
    'product_id': 'nunique',
    'price': ['sum', 'mean'],
    'age': 'first'
})

user_behavior['total_actions'] = df.groupby('user_id')['event_type'].count()
user_behavior.columns = ['is_potential', 'unique_products', 'total_spending', 'avg_spending', 'age', 'total_actions']

# Tính correlation
corr_matrix = user_behavior.corr()

print(f'✅ Dữ liệu đã chuẩn bị: {corr_matrix.shape}')
print(f'✅ Range correlation: {corr_matrix.min().min():.3f} đến {corr_matrix.max().max():.3f}')

# Tạo heatmap với màu sáng như hình mẫu
plt.figure(figsize=(10, 8))

# Sử dụng colormap sáng với gradient từ xanh dương đến trắng đến đỏ
sns.heatmap(corr_matrix, 
            annot=True, 
            cmap='RdBu_r',  # Màu đỏ-xanh dương (đảo ngược để đỏ ở trên)
            center=0,
            square=True, 
            fmt='.3f',
            cbar_kws={'shrink': 0.8},
            linewidths=1,
            linecolor='white',
            annot_kws={'fontsize': 12, 'fontweight': 'bold', 'color': 'white'})

plt.title('Ma trận tương quan - Màu sáng', fontsize=16, fontweight='bold', color='darkblue')
plt.tight_layout()
plt.savefig('bright_correlation_heatmap.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print('✅ Đã lưu: bright_correlation_heatmap.png')

# Tạo heatmap với màu sáng khác
plt.figure(figsize=(10, 8))

sns.heatmap(corr_matrix, 
            annot=True, 
            cmap='coolwarm',  # Màu lạnh-nóng
            center=0,
            square=True, 
            fmt='.3f',
            cbar_kws={'shrink': 0.8},
            linewidths=1,
            linecolor='white',
            annot_kws={'fontsize': 12, 'fontweight': 'bold', 'color': 'white'})

plt.title('Ma trận tương quan - Màu lạnh-nóng', fontsize=16, fontweight='bold', color='darkgreen')
plt.tight_layout()
plt.savefig('coolwarm_correlation_heatmap.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print('✅ Đã lưu: coolwarm_correlation_heatmap.png')

# Tạo heatmap với màu sáng nhất
plt.figure(figsize=(10, 8))

sns.heatmap(corr_matrix, 
            annot=True, 
            cmap='RdYlBu_r',  # Màu đỏ-vàng-xanh dương (đảo ngược)
            center=0,
            square=True, 
            fmt='.3f',
            cbar_kws={'shrink': 0.8},
            linewidths=1,
            linecolor='white',
            annot_kws={'fontsize': 12, 'fontweight': 'bold', 'color': 'white'})

plt.title('Ma trận tương quan - Màu sáng nhất', fontsize=16, fontweight='bold', color='darkred')
plt.tight_layout()
plt.savefig('brightest_correlation_heatmap.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print('✅ Đã lưu: brightest_correlation_heatmap.png')

print('\n🎉 Đã tạo xong 3 heatmap với màu sắc sáng khác nhau!')
print('\n📁 Các file đã tạo:')
print('1. bright_correlation_heatmap.png - Màu đỏ-xanh dương sáng')
print('2. coolwarm_correlation_heatmap.png - Màu lạnh-nóng')
print('3. brightest_correlation_heatmap.png - Màu sáng nhất')

print('\n💡 Gợi ý:')
print('- Màu sáng nhất: brightest_correlation_heatmap.png')
print('- Màu dễ nhìn: bright_correlation_heatmap.png')
print('- Màu chuyên nghiệp: coolwarm_correlation_heatmap.png')
