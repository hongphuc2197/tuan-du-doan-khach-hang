import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print('🔥 TẠO HEATMAP MA TRẬN TƯƠNG QUAN')
print('=' * 50)

# Đọc dataset
df = pd.read_csv('user_actions_students_576.csv')
print(f'Dataset: {len(df)} records, {df["user_id"].nunique()} users')

# Tạo features
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

# Encode categorical
from sklearn.preprocessing import LabelEncoder
le_income = LabelEncoder()
le_education = LabelEncoder()
user_behavior['income_encoded'] = le_income.fit_transform(user_behavior['income_level'])
user_behavior['education_encoded'] = le_education.fit_transform(user_behavior['education'])

# Correlation matrix
features = ['total_actions', 'unique_products', 'total_spending', 'avg_spending', 'age', 'income_encoded', 'education_encoded', 'is_potential']
corr_matrix = user_behavior[features].corr()

# Tạo heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='RdBu_r', center=0, square=True, fmt='.3f')
plt.title('Correlation Matrix Heatmap')
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

print('✅ Created: correlation_heatmap.png')

# In correlation với target
target_corr = corr_matrix['is_potential'].drop('is_potential').sort_values(key=abs, reverse=True)
print('\n=== TƯƠNG QUAN VỚI TARGET ===')
for feature, corr in target_corr.items():
    print(f'{feature}: {corr:.3f}')

print('Done!')
