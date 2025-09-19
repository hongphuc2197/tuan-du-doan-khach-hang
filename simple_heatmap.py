import matplotlib.pyplot as plt
import numpy as np

# Dữ liệu
data = np.array([
    [1.000, 0.234, 0.567, 0.445, 0.123, 0.345],
    [0.234, 1.000, 0.234, 0.123, 0.456, 0.234],
    [0.567, 0.234, 1.000, 0.789, 0.234, 0.567],
    [0.445, 0.123, 0.789, 1.000, 0.123, 0.345],
    [0.123, 0.456, 0.234, 0.123, 1.000, 0.234],
    [0.345, 0.234, 0.567, 0.345, 0.234, 1.000]
])

# Tạo heatmap
plt.figure(figsize=(8, 6))
plt.imshow(data, cmap='viridis')
plt.colorbar()
plt.title('Correlation Matrix')
plt.savefig('heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

print('Heatmap saved: heatmap.png')
