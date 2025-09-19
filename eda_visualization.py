import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

# Thiết lập style cho biểu đồ
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

print('📊 TẠO BIỂU ĐỒ KHÁM PHÁ DỮ LIỆU (EDA)')
print('=' * 50)

# Đọc dataset
df = pd.read_csv('user_actions_students_576.csv')
print(f'✅ Dataset: {len(df)} records, {df["user_id"].nunique()} users')

# Tạo figure với nhiều subplot
fig = plt.figure(figsize=(20, 16))

# 1. Phân phối Event Types
plt.subplot(3, 4, 1)
event_counts = df['event_type'].value_counts()
colors = ['#FF6B6B', '#4ECDC4']
plt.pie(event_counts.values, labels=event_counts.index, autopct='%1.1f%%', colors=colors)
plt.title('Phân phối loại hành vi', fontsize=14, fontweight='bold')

# 2. Phân phối Age
plt.subplot(3, 4, 2)
plt.hist(df['age'], bins=8, color='#45B7D1', alpha=0.7, edgecolor='black')
plt.title('Phân phối độ tuổi', fontsize=14, fontweight='bold')
plt.xlabel('Tuổi')
plt.ylabel('Số lượng')

# 3. Phân phối Income Level
plt.subplot(3, 4, 3)
income_counts = df['income_level'].value_counts()
bars = plt.bar(income_counts.index, income_counts.values, color=['#FFA07A', '#98D8C8'])
plt.title('Phân phối mức thu nhập', fontsize=14, fontweight='bold')
plt.xlabel('Mức thu nhập')
plt.ylabel('Số lượng')
# Thêm số liệu lên cột
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}', ha='center', va='bottom')

# 4. Phân phối Education
plt.subplot(3, 4, 4)
edu_counts = df['education'].value_counts()
bars = plt.bar(edu_counts.index, edu_counts.values, color=['#DDA0DD', '#F0E68C', '#87CEEB'])
plt.title('Phân phối trình độ học vấn', fontsize=14, fontweight='bold')
plt.xlabel('Trình độ học vấn')
plt.ylabel('Số lượng')
plt.xticks(rotation=45)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}', ha='center', va='bottom')

# 5. Phân phối Price
plt.subplot(3, 4, 5)
plt.hist(df['price'], bins=20, color='#FFB347', alpha=0.7, edgecolor='black')
plt.title('Phân phối giá sản phẩm', fontsize=14, fontweight='bold')
plt.xlabel('Giá ($)')
plt.ylabel('Số lượng')

# 6. Scatter plot: Age vs Price
plt.subplot(3, 4, 6)
plt.scatter(df['age'], df['price'], alpha=0.6, color='#FF69B4')
plt.title('Tuổi vs Giá sản phẩm', fontsize=14, fontweight='bold')
plt.xlabel('Tuổi')
plt.ylabel('Giá ($)')

# 7. Box plot: Price by Event Type
plt.subplot(3, 4, 7)
df.boxplot(column='price', by='event_type', ax=plt.gca())
plt.title('Giá sản phẩm theo loại hành vi', fontsize=14, fontweight='bold')
plt.xlabel('Loại hành vi')
plt.ylabel('Giá ($)')
plt.suptitle('')  # Xóa title mặc định

# 8. Heatmap correlation
plt.subplot(3, 4, 8)
# Tạo dữ liệu số cho correlation
numeric_data = df[['age', 'price']].copy()
le_income = LabelEncoder()
le_education = LabelEncoder()
numeric_data['income_encoded'] = le_income.fit_transform(df['income_level'])
numeric_data['education_encoded'] = le_education.fit_transform(df['education'])
numeric_data['event_encoded'] = (df['event_type'] == 'purchase').astype(int)

correlation_matrix = numeric_data.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
            square=True, fmt='.2f', cbar_kws={'shrink': 0.8})
plt.title('Ma trận tương quan', fontsize=14, fontweight='bold')

# 9. User behavior analysis
plt.subplot(3, 4, 9)
user_behavior = df.groupby('user_id').agg({
    'event_type': 'count',
    'product_id': 'nunique',
    'price': 'sum'
})
user_behavior.columns = ['total_actions', 'unique_products', 'total_spending']

plt.scatter(user_behavior['total_actions'], user_behavior['total_spending'], 
           alpha=0.6, color='#32CD32')
plt.title('Tổng hành động vs Tổng chi tiêu', fontsize=14, fontweight='bold')
plt.xlabel('Tổng số hành động')
plt.ylabel('Tổng chi tiêu ($)')

# 10. Event type by age group
plt.subplot(3, 4, 10)
df['age_group'] = pd.cut(df['age'], bins=[17, 20, 23, 26], labels=['18-20', '21-23', '24-25'])
event_age = pd.crosstab(df['age_group'], df['event_type'])
event_age.plot(kind='bar', stacked=True, ax=plt.gca())
plt.title('Loại hành vi theo nhóm tuổi', fontsize=14, fontweight='bold')
plt.xlabel('Nhóm tuổi')
plt.ylabel('Số lượng')
plt.legend(title='Loại hành vi')
plt.xticks(rotation=45)

# 11. Price distribution by income
plt.subplot(3, 4, 11)
sns.boxplot(data=df, x='income_level', y='price', ax=plt.gca())
plt.title('Giá sản phẩm theo thu nhập', fontsize=14, fontweight='bold')
plt.xlabel('Mức thu nhập')
plt.ylabel('Giá ($)')

# 12. Summary statistics
plt.subplot(3, 4, 12)
plt.axis('off')
summary_text = f"""
THỐNG KÊ TỔNG QUAN:

📊 Tổng số records: {len(df):,}
👥 Số người dùng: {df['user_id'].nunique():,}
🛍️ Tổng lượt xem: {(df['event_type'] == 'view').sum():,}
💳 Tổng lượt mua: {(df['event_type'] == 'purchase').sum():,}
💰 Giá trung bình: ${df['price'].mean():,.0f}
📈 Giá cao nhất: ${df['price'].max():,.0f}
📉 Giá thấp nhất: ${df['price'].min():,.0f}
👶 Tuổi trung bình: {df['age'].mean():.1f}
🎓 Học vấn phổ biến: {df['education'].mode()[0]}
💵 Thu nhập phổ biến: {df['income_level'].mode()[0]}
"""

plt.text(0.1, 0.9, summary_text, transform=plt.gca().transAxes, 
         fontsize=10, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))

plt.tight_layout()
plt.savefig('eda_visualization.png', dpi=300, bbox_inches='tight')
print('✅ Đã lưu biểu đồ EDA: eda_visualization.png')

# Tạo thêm biểu đồ chi tiết về user behavior
fig2, axes = plt.subplots(2, 2, figsize=(15, 12))

# User behavior distribution
user_stats = df.groupby('user_id').agg({
    'event_type': lambda x: 'purchase' in x.values,
    'event_type': 'count',
    'product_id': 'nunique',
    'price': ['sum', 'mean']
})
user_stats.columns = ['is_potential', 'total_actions', 'unique_products', 'total_spending', 'avg_spending']

# 1. Distribution of total actions per user
axes[0, 0].hist(user_stats['total_actions'], bins=15, color='#FF6B6B', alpha=0.7, edgecolor='black')
axes[0, 0].set_title('Phân phối tổng hành động/người dùng', fontweight='bold')
axes[0, 0].set_xlabel('Tổng số hành động')
axes[0, 0].set_ylabel('Số người dùng')

# 2. Distribution of spending per user
axes[0, 1].hist(user_stats['total_spending'], bins=15, color='#4ECDC4', alpha=0.7, edgecolor='black')
axes[0, 1].set_title('Phân phối tổng chi tiêu/người dùng', fontweight='bold')
axes[0, 1].set_xlabel('Tổng chi tiêu ($)')
axes[0, 1].set_ylabel('Số người dùng')

# 3. Scatter: Actions vs Spending
axes[1, 0].scatter(user_stats['total_actions'], user_stats['total_spending'], 
                   c=user_stats['is_potential'], cmap='RdYlBu', alpha=0.7)
axes[1, 0].set_title('Hành động vs Chi tiêu (màu = có mua)', fontweight='bold')
axes[1, 0].set_xlabel('Tổng số hành động')
axes[1, 0].set_ylabel('Tổng chi tiêu ($)')

# 4. Potential customers by age
potential_by_age = df.groupby(['age', 'event_type']).size().unstack(fill_value=0)
potential_by_age['purchase_rate'] = potential_by_age['purchase'] / (potential_by_age['view'] + potential_by_age['purchase'])
axes[1, 1].bar(potential_by_age.index, potential_by_age['purchase_rate'], color='#98D8C8')
axes[1, 1].set_title('Tỷ lệ mua hàng theo tuổi', fontweight='bold')
axes[1, 1].set_xlabel('Tuổi')
axes[1, 1].set_ylabel('Tỷ lệ mua hàng')
axes[1, 1].set_ylim(0, 1)

plt.tight_layout()
plt.savefig('user_behavior_analysis.png', dpi=300, bbox_inches='tight')
print('✅ Đã lưu phân tích hành vi người dùng: user_behavior_analysis.png')

plt.show()
print('\n🎉 Hoàn thành tạo biểu đồ EDA!')
