import matplotlib.pyplot as plt
import numpy as np

# Dữ liệu
features = ['Total Actions', 'Unique Products', 'Total Spending', 'Avg Spending', 'Age', 'Income', 'Education']
rf_importance = [0.067877, 0.069348, 0.324712, 0.293655, 0.159855, 0.034851, 0.049702]

# Tạo biểu đồ đơn giản
plt.figure(figsize=(10, 6))
bars = plt.bar(features, rf_importance, color='blue', alpha=0.7)
plt.title('Random Forest - Feature Importance')
plt.xlabel('Features')
plt.ylabel('Importance')
plt.xticks(rotation=45)

# Thêm giá trị lên cột
for bar, value in zip(bars, rf_importance):
    plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.005,
             f'{value:.3f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
plt.close()

print('Chart created: feature_importance.png')
