import matplotlib.pyplot as plt
import numpy as np

# Dữ liệu
features = ['Total Actions', 'Unique Products', 'Total Spending', 'Avg Spending', 'Age', 'Income', 'Education']
rf_importance = [0.067877, 0.069348, 0.324712, 0.293655, 0.159855, 0.034851, 0.049702]

# Tạo biểu đồ
plt.figure(figsize=(10, 6))
bars = plt.barh(features, rf_importance, color='blue', alpha=0.7)
plt.title('Random Forest - Feature Importance')
plt.xlabel('Importance Score')

# Thêm giá trị
for bar, value in zip(bars, rf_importance):
    plt.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2, 
             f'{value:.3f}', ha='left', va='center')

plt.tight_layout()
plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
plt.close()

print('Chart saved: feature_importance.png')
