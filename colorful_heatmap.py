import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print('🌈 TẠO HEATMAP VỚI MÀU SẮC SÁNG')
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

# Tạo heatmap với màu sáng
plt.figure(figsize=(10, 8))

# Sử dụng colormap sáng hơn
sns.heatmap(corr_matrix, 
            annot=True, 
            cmap='viridis',  # Màu xanh lá sáng
            center=0,
            square=True, 
            fmt='.3f',
            cbar_kws={'shrink': 0.8},
            linewidths=1,
            linecolor='white',
            annot_kws={'fontsize': 12, 'fontweight': 'bold', 'color': 'white'})

plt.title('Ma trận tương quan - Màu sáng', fontsize=16, fontweight='bold', color='darkblue')
plt.tight_layout()
plt.savefig('bright_heatmap.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print('✅ Đã lưu: bright_heatmap.png')

# Tạo heatmap với màu nóng
plt.figure(figsize=(10, 8))

sns.heatmap(corr_matrix, 
            annot=True, 
            cmap='plasma',  # Màu tím-hồng-cam
            center=0,
            square=True, 
            fmt='.3f',
            cbar_kws={'shrink': 0.8},
            linewidths=1,
            linecolor='white',
            annot_kws={'fontsize': 12, 'fontweight': 'bold', 'color': 'white'})

plt.title('Ma trận tương quan - Màu nóng', fontsize=16, fontweight='bold', color='darkred')
plt.tight_layout()
plt.savefig('hot_heatmap.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print('✅ Đã lưu: hot_heatmap.png')

# Tạo heatmap với màu rainbow
plt.figure(figsize=(10, 8))

sns.heatmap(corr_matrix, 
            annot=True, 
            cmap='rainbow',  # Màu cầu vồng
            center=0,
            square=True, 
            fmt='.3f',
            cbar_kws={'shrink': 0.8},
            linewidths=1,
            linecolor='white',
            annot_kws={'fontsize': 12, 'fontweight': 'bold', 'color': 'black'})

plt.title('Ma trận tương quan - Màu cầu vồng', fontsize=16, fontweight='bold', color='darkgreen')
plt.tight_layout()
plt.savefig('rainbow_heatmap.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print('✅ Đã lưu: rainbow_heatmap.png')

# Tạo heatmap với màu xanh dương sáng
plt.figure(figsize=(10, 8))

sns.heatmap(corr_matrix, 
            annot=True, 
            cmap='Blues',  # Màu xanh dương sáng
            center=0,
            square=True, 
            fmt='.3f',
            cbar_kws={'shrink': 0.8},
            linewidths=1,
            linecolor='white',
            annot_kws={'fontsize': 12, 'fontweight': 'bold', 'color': 'white'})

plt.title('Ma trận tương quan - Màu xanh dương', fontsize=16, fontweight='bold', color='darkblue')
plt.tight_layout()
plt.savefig('blue_heatmap.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print('✅ Đã lưu: blue_heatmap.png')

# Tạo heatmap với màu xanh lá sáng
plt.figure(figsize=(10, 8))

sns.heatmap(corr_matrix, 
            annot=True, 
            cmap='Greens',  # Màu xanh lá sáng
            center=0,
            square=True, 
            fmt='.3f',
            cbar_kws={'shrink': 0.8},
            linewidths=1,
            linecolor='white',
            annot_kws={'fontsize': 12, 'fontweight': 'bold', 'color': 'white'})

plt.title('Ma trận tương quan - Màu xanh lá', fontsize=16, fontweight='bold', color='darkgreen')
plt.tight_layout()
plt.savefig('green_heatmap.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print('✅ Đã lưu: green_heatmap.png')

# Tạo heatmap với màu cam sáng
plt.figure(figsize=(10, 8))

sns.heatmap(corr_matrix, 
            annot=True, 
            cmap='Oranges',  # Màu cam sáng
            center=0,
            square=True, 
            fmt='.3f',
            cbar_kws={'shrink': 0.8},
            linewidths=1,
            linecolor='white',
            annot_kws={'fontsize': 12, 'fontweight': 'bold', 'color': 'white'})

plt.title('Ma trận tương quan - Màu cam', fontsize=16, fontweight='bold', color='darkorange')
plt.tight_layout()
plt.savefig('orange_heatmap.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print('✅ Đã lưu: orange_heatmap.png')

print('\n🎉 Đã tạo xong 6 heatmap với màu sắc khác nhau!')
print('\n📁 Các file đã tạo:')
print('1. bright_heatmap.png - Màu xanh lá sáng (viridis)')
print('2. hot_heatmap.png - Màu nóng (plasma)')
print('3. rainbow_heatmap.png - Màu cầu vồng')
print('4. blue_heatmap.png - Màu xanh dương')
print('5. green_heatmap.png - Màu xanh lá')
print('6. orange_heatmap.png - Màu cam')

print('\n💡 Gợi ý:')
print('- Màu sáng nhất: rainbow_heatmap.png')
print('- Màu dễ nhìn nhất: bright_heatmap.png (viridis)')
print('- Màu chuyên nghiệp: blue_heatmap.png')
