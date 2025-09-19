import matplotlib.pyplot as plt
import numpy as np

# Dữ liệu
features = ['is_potential', 'unique_products', 'total_spending', 'avg_spending', 'age', 'total_actions']
corr_data = np.array([
    [1.000, 0.234, 0.567, 0.445, 0.123, 0.345],
    [0.234, 1.000, 0.234, 0.123, 0.456, 0.234],
    [0.567, 0.234, 1.000, 0.789, 0.234, 0.567],
    [0.445, 0.123, 0.789, 1.000, 0.123, 0.345],
    [0.123, 0.456, 0.234, 0.123, 1.000, 0.234],
    [0.345, 0.234, 0.567, 0.345, 0.234, 1.000]
])

# Tạo heatmap
plt.figure(figsize=(10, 8))
plt.imshow(corr_data, cmap='viridis')
plt.colorbar()

# Labels
plt.xticks(range(len(features)), features, rotation=45)
plt.yticks(range(len(features)), features)

# Giá trị
for i in range(len(features)):
    for j in range(len(features)):
        plt.text(j, i, f'{corr_data[i, j]:.2f}', ha='center', va='center', 
                fontweight='bold', color='white')

plt.title('Correlation Matrix')
plt.tight_layout()
plt.savefig('heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

print('Heatmap saved: heatmap.png')
