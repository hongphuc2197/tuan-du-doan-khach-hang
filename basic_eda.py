import pandas as pd
import matplotlib.pyplot as plt

print('📊 TẠO BIỂU ĐỒ EDA CƠ BẢN')
print('=' * 40)

# Đọc dataset
df = pd.read_csv('user_actions_students_576.csv')
print(f'Dataset: {len(df)} records, {df["user_id"].nunique()} users')

# Tạo figure đơn giản
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# 1. Phân phối Event Types
axes[0, 0].pie(df['event_type'].value_counts().values, 
               labels=df['event_type'].value_counts().index,
               autopct='%1.1f%%')
axes[0, 0].set_title('Phân phối loại hành vi')

# 2. Phân phối Age
axes[0, 1].hist(df['age'], bins=8, alpha=0.7, edgecolor='black')
axes[0, 1].set_title('Phân phối độ tuổi')
axes[0, 1].set_xlabel('Tuổi')
axes[0, 1].set_ylabel('Số lượng')

# 3. Phân phối Income Level
income_counts = df['income_level'].value_counts()
axes[1, 0].bar(income_counts.index, income_counts.values)
axes[1, 0].set_title('Phân phối mức thu nhập')
axes[1, 0].set_xlabel('Mức thu nhập')
axes[1, 0].set_ylabel('Số lượng')

# 4. Phân phối Price
axes[1, 1].hist(df['price'], bins=20, alpha=0.7, edgecolor='black')
axes[1, 1].set_title('Phân phối giá sản phẩm')
axes[1, 1].set_xlabel('Giá ($)')
axes[1, 1].set_ylabel('Số lượng')

plt.suptitle('BIỂU ĐỒ KHÁM PHÁ DỮ LIỆU (EDA)', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('basic_eda.png', dpi=300, bbox_inches='tight')
print('✅ Đã lưu biểu đồ: basic_eda.png')

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

# Thống kê theo người dùng
user_stats = df.groupby('user_id').agg({
    'event_type': 'count',
    'price': 'sum'
})
user_stats.columns = ['total_actions', 'total_spending']

print(f'\n=== THỐNG KÊ THEO NGƯỜI DÙNG ===')
print(f'📊 Hành động trung bình/người: {user_stats["total_actions"].mean():.1f}')
print(f'💰 Chi tiêu trung bình/người: ${user_stats["total_spending"].mean():,.0f}')
print(f'📈 Hành động cao nhất: {user_stats["total_actions"].max()}')
print(f'💰 Chi tiêu cao nhất: ${user_stats["total_spending"].max():,.0f}')

print('\n🎉 Hoàn thành tạo biểu đồ EDA!')
