import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

# Tạo heatmap
plt.figure(figsize=(8, 6))
plt.imshow(corr_matrix, cmap='RdBu_r', aspect='auto')
plt.colorbar()

# Thêm labels
features = ['is_potential', 'unique_products', 'total_spending', 'avg_spending', 'age', 'total_actions']
plt.xticks(range(len(features)), features, rotation=45)
plt.yticks(range(len(features)), features)

# Thêm giá trị
for i in range(len(features)):
    for j in range(len(features)):
        plt.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}', ha='center', va='center', fontweight='bold')

plt.title('Correlation Matrix Heatmap')
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

print('Correlation heatmap saved: correlation_heatmap.png')
