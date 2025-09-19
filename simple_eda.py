import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Thiết lập để hiển thị tiếng Việt
plt.rcParams['font.family'] = ['DejaVu Sans']

print('📊 TẠO BIỂU ĐỒ EDA ĐƠN GIẢN')
print('=' * 40)

# Đọc dataset
df = pd.read_csv('user_actions_students_576.csv')
print(f'Dataset: {len(df)} records, {df["user_id"].nunique()} users')

# Tạo figure
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# 1. Phân phối Event Types
axes[0, 0].pie(df['event_type'].value_counts().values, 
               labels=df['event_type'].value_counts().index,
               autopct='%1.1f%%',
               colors=['#FF6B6B', '#4ECDC4'])
axes[0, 0].set_title('Phân phối loại hành vi', fontsize=14, fontweight='bold')

# 2. Phân phối Age
axes[0, 1].hist(df['age'], bins=8, color='#45B7D1', alpha=0.7, edgecolor='black')
axes[0, 1].set_title('Phân phối độ tuổi', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Tuổi')
axes[0, 1].set_ylabel('Số lượng')

# 3. Phân phối Income Level
income_counts = df['income_level'].value_counts()
bars = axes[0, 2].bar(income_counts.index, income_counts.values, 
                      color=['#FFA07A', '#98D8C8'])
axes[0, 2].set_title('Phân phối mức thu nhập', fontsize=14, fontweight='bold')
axes[0, 2].set_xlabel('Mức thu nhập')
axes[0, 2].set_ylabel('Số lượng')

# 4. Phân phối Price
axes[1, 0].hist(df['price'], bins=20, color='#FFB347', alpha=0.7, edgecolor='black')
axes[1, 0].set_title('Phân phối giá sản phẩm', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Giá ($)')
axes[1, 0].set_ylabel('Số lượng')

# 5. Scatter: Age vs Price
axes[1, 1].scatter(df['age'], df['price'], alpha=0.6, color='#FF69B4')
axes[1, 1].set_title('Tuổi vs Giá sản phẩm', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Tuổi')
axes[1, 1].set_ylabel('Giá ($)')

# 6. Box plot: Price by Event Type
df.boxplot(column='price', by='event_type', ax=axes[1, 2])
axes[1, 2].set_title('Giá sản phẩm theo loại hành vi', fontsize=14, fontweight='bold')
axes[1, 2].set_xlabel('Loại hành vi')
axes[1, 2].set_ylabel('Giá ($)')

plt.suptitle('BIỂU ĐỒ KHÁM PHÁ DỮ LIỆU (EDA)', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('simple_eda.png', dpi=300, bbox_inches='tight')
print('✅ Đã lưu biểu đồ: simple_eda.png')

# Tạo biểu đồ thống kê
fig2, axes2 = plt.subplots(1, 2, figsize=(15, 6))

# User behavior analysis
user_behavior = df.groupby('user_id').agg({
    'event_type': lambda x: 'purchase' in x.values,
    'product_id': 'nunique',
    'price': 'sum'
})
user_behavior['total_actions'] = df.groupby('user_id')['event_type'].count()
user_behavior.columns = ['is_potential', 'unique_products', 'total_spending', 'total_actions']

# 1. Distribution of total actions per user
axes2[0].hist(user_behavior['total_actions'], bins=15, color='#FF6B6B', alpha=0.7, edgecolor='black')
axes2[0].set_title('Phân phối tổng hành động/người dùng', fontweight='bold')
axes2[0].set_xlabel('Tổng số hành động')
axes2[0].set_ylabel('Số người dùng')

# 2. Distribution of spending per user
axes2[1].hist(user_behavior['total_spending'], bins=15, color='#4ECDC4', alpha=0.7, edgecolor='black')
axes2[1].set_title('Phân phối tổng chi tiêu/người dùng', fontweight='bold')
axes2[1].set_xlabel('Tổng chi tiêu ($)')
axes2[1].set_ylabel('Số người dùng')

plt.suptitle('PHÂN TÍCH HÀNH VI NGƯỜI DÙNG', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('user_behavior.png', dpi=300, bbox_inches='tight')
print('✅ Đã lưu biểu đồ hành vi: user_behavior.png')

# In thống kê
print('\n=== THỐNG KÊ TỔNG QUAN ===')
print(f'📊 Tổng số records: {len(df):,}')
print(f'👥 Số người dùng: {df["user_id"].nunique():,}')
print(f'🛍️ Tổng lượt xem: {(df["event_type"] == "view").sum():,}')
print(f'💳 Tổng lượt mua: {(df["event_type"] == "purchase").sum():,}')
print(f'💰 Giá trung bình: ${df["price"].mean():,.0f}')
print(f'📈 Giá cao nhất: ${df["price"].max():,.0f}')
print(f'📉 Giá thấp nhất: ${df["price"].min():,.0f}')
print(f'👶 Tuổi trung bình: {df["age"].mean():.1f}')
print(f'🎓 Học vấn phổ biến: {df["education"].mode()[0]}')
print(f'💵 Thu nhập phổ biến: {df["income_level"].mode()[0]}')

print('\n🎉 Hoàn thành tạo biểu đồ EDA!')
