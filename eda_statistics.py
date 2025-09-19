import pandas as pd
import numpy as np

print('📊 PHÂN TÍCH DỮ LIỆU (EDA) - THỐNG KÊ')
print('=' * 50)

# Đọc dataset
df = pd.read_csv('user_actions_students_576.csv')
print(f'✅ Dataset: {len(df)} records, {df["user_id"].nunique()} users')

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

print('\n=== PHÂN PHỐI EVENT TYPES ===')
event_counts = df['event_type'].value_counts()
for event, count in event_counts.items():
    percentage = (count / len(df)) * 100
    print(f'{event}: {count:,} ({percentage:.1f}%)')

print('\n=== PHÂN PHỐI TUỔI ===')
age_stats = df['age'].describe()
print(f'Tuổi nhỏ nhất: {age_stats["min"]:.0f}')
print(f'Tuổi trung bình: {age_stats["mean"]:.1f}')
print(f'Tuổi trung vị: {age_stats["50%"]:.0f}')
print(f'Tuổi lớn nhất: {age_stats["max"]:.0f}')

print('\n=== PHÂN PHỐI THU NHẬP ===')
income_counts = df['income_level'].value_counts()
for income, count in income_counts.items():
    percentage = (count / len(df)) * 100
    print(f'{income}: {count:,} ({percentage:.1f}%)')

print('\n=== PHÂN PHỐI HỌC VẤN ===')
edu_counts = df['education'].value_counts()
for edu, count in edu_counts.items():
    percentage = (count / len(df)) * 100
    print(f'{edu}: {count:,} ({percentage:.1f}%)')

print('\n=== PHÂN PHỐI GIÁ SẢN PHẨM ===')
price_stats = df['price'].describe()
print(f'Giá thấp nhất: ${price_stats["min"]:,.0f}')
print(f'Giá trung bình: ${price_stats["mean"]:,.0f}')
print(f'Giá trung vị: ${price_stats["50%"]:,.0f}')
print(f'Giá cao nhất: ${price_stats["max"]:,.0f}')

# Thống kê theo người dùng
print('\n=== THỐNG KÊ THEO NGƯỜI DÙNG ===')
user_stats = df.groupby('user_id').agg({
    'event_type': 'count',
    'price': 'sum',
    'product_id': 'nunique'
})
user_stats.columns = ['total_actions', 'total_spending', 'unique_products']

print(f'📊 Hành động trung bình/người: {user_stats["total_actions"].mean():.1f}')
print(f'💰 Chi tiêu trung bình/người: ${user_stats["total_spending"].mean():,.0f}')
print(f'🛍️ Sản phẩm trung bình/người: {user_stats["unique_products"].mean():.1f}')
print(f'📈 Hành động cao nhất: {user_stats["total_actions"].max()}')
print(f'💰 Chi tiêu cao nhất: ${user_stats["total_spending"].max():,.0f}')

# Phân tích khách hàng tiềm năng
print('\n=== PHÂN TÍCH KHÁCH HÀNG TIỀM NĂNG ===')
user_behavior = df.groupby('user_id').agg({
    'event_type': lambda x: 'purchase' in x.values,
    'event_type': 'count',
    'price': 'sum'
})
user_behavior.columns = ['is_potential', 'total_actions', 'total_spending']

potential_count = user_behavior['is_potential'].sum()
total_users = len(user_behavior)
print(f'👥 Tổng số người dùng: {total_users}')
print(f'🎯 Khách hàng tiềm năng: {potential_count} ({potential_count/total_users*100:.1f}%)')
print(f'👀 Chỉ xem không mua: {total_users - potential_count} ({(total_users - potential_count)/total_users*100:.1f}%)')

# So sánh chi tiêu
potential_spending = user_behavior[user_behavior['is_potential'] == True]['total_spending'].mean()
non_potential_spending = user_behavior[user_behavior['is_potential'] == False]['total_spending'].mean()
print(f'💰 Chi tiêu trung bình - Có mua: ${potential_spending:,.0f}')
print(f'💰 Chi tiêu trung bình - Chỉ xem: ${non_potential_spending:,.0f}')

print('\n🎉 Hoàn thành phân tích EDA!')
