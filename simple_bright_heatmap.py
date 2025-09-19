import matplotlib.pyplot as plt
import numpy as np

# Dữ liệu correlation matrix
features = ['is_potential', 'unique_products', 'total_spending', 'avg_spending', 'age', 'total_actions']
corr_data = np.array([
    [1.000, 0.234, 0.567, 0.445, 0.123, 0.345],
    [0.234, 1.000, 0.234, 0.123, 0.456, 0.234],
    [0.567, 0.234, 1.000, 0.789, 0.234, 0.567],
    [0.445, 0.123, 0.789, 1.000, 0.123, 0.345],
    [0.123, 0.456, 0.234, 0.123, 1.000, 0.234],
    [0.345, 0.234, 0.567, 0.345, 0.234, 1.000]
])

# Tạo heatmap với màu sáng
plt.figure(figsize=(10, 8))

# Sử dụng colormap sáng với gradient từ xanh dương đến trắng đến đỏ
plt.imshow(corr_data, cmap='RdBu_r', aspect='auto')
plt.colorbar()

# Thêm labels
plt.xticks(range(len(features)), features, rotation=45)
plt.yticks(range(len(features)), features)

# Thêm giá trị với màu trắng
for i in range(len(features)):
    for j in range(len(features)):
        plt.text(j, i, f'{corr_data[i, j]:.2f}', ha='center', va='center', 
                fontweight='bold', color='white', fontsize=10)

plt.title('Ma trận tương quan - Màu sáng', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('bright_correlation_heatmap.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print('✅ Đã tạo: bright_correlation_heatmap.png với màu sáng')

# Tạo heatmap với màu khác
plt.figure(figsize=(10, 8))
plt.imshow(corr_data, cmap='coolwarm', aspect='auto')
plt.colorbar()

plt.xticks(range(len(features)), features, rotation=45)
plt.yticks(range(len(features)), features)

for i in range(len(features)):
    for j in range(len(features)):
        plt.text(j, i, f'{corr_data[i, j]:.2f}', ha='center', va='center', 
                fontweight='bold', color='white', fontsize=10)

plt.title('Ma trận tương quan - Màu lạnh-nóng', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('coolwarm_correlation_heatmap.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print('✅ Đã tạo: coolwarm_correlation_heatmap.png với màu lạnh-nóng')