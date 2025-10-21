#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thêm phân loại sách và phân tích khách hàng tiềm năng theo loại sách
"""

import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

print('=' * 70)
print('PHÂN TÍCH KHÁCH HÀNG TIỀM NĂNG THEO LOẠI SÁCH')
print('=' * 70)

# Đọc dữ liệu
df = pd.read_csv('user_actions_students_576.csv')
print(f'✅ Đọc dữ liệu: {len(df)} records, {df["user_id"].nunique()} users')

# Định nghĩa mapping từ product_id đến loại sách
book_type_mapping = {
    1: "Công nghệ giáo dục",
    2: "Phương pháp giảng dạy", 
    3: "Công nghệ thông tin",
    4: "Thiết kế web",
    5: "Lập trình",
    6: "Nghiên cứu khoa học",
    7: "Giáo dục STEM",
    8: "Giảng dạy tiếng Anh",
    9: "Thiết kế",
    10: "Cơ sở dữ liệu",
    11: "Phát triển ứng dụng",
    12: "Công nghệ giáo dục"  # Thêm một loại nữa
}

# Thêm cột book_type vào DataFrame
df['book_type'] = df['product_id'].map(book_type_mapping)

print(f'\n📚 CÁC LOẠI SÁCH TRONG HỆ THỐNG:')
for product_id, book_type in book_type_mapping.items():
    count = len(df[df['product_id'] == product_id])
    print(f'   Product {product_id}: {book_type} ({count} records)')

# Tạo features từ dữ liệu với thông tin loại sách
user_behavior = df.groupby('user_id').agg({
    'event_type': lambda x: 'purchase' in x.values,
    'product_id': 'nunique',
    'price': ['sum', 'mean'],
    'age': 'first',
    'income_level': 'first',
    'education': 'first',
    'name': 'first',
    'email': 'first',
    'income': 'first',
    'book_type': lambda x: list(x.unique())
}).reset_index()

user_behavior['total_actions'] = df.groupby('user_id')['event_type'].count().values

# Flatten column names
user_behavior.columns = ['user_id', 'is_potential', 'unique_products', 'total_spending', 
                         'avg_spending', 'age', 'income_level', 'education', 'name', 
                         'email', 'income', 'book_types', 'total_actions']

# Tạo cột cho từng loại sách (số lượng mua)
book_type_columns = {}
for book_type in set(book_type_mapping.values()):
    col_name = f'books_{book_type.lower().replace(" ", "_").replace("đ", "d")}'
    user_behavior[col_name] = 0
    book_type_columns[book_type] = col_name

# Đếm số lượng sách theo loại cho mỗi user
for idx, row in user_behavior.iterrows():
    user_id = row['user_id']
    user_books = df[df['user_id'] == user_id]
    
    for book_type, col_name in book_type_columns.items():
        count = len(user_books[user_books['book_type'] == book_type])
        user_behavior.loc[idx, col_name] = count

print(f'\n✅ Tạo features cho {len(user_behavior)} users với thông tin loại sách')

# Phân tích khách hàng tiền năng theo loại sách
potential_customers = user_behavior[user_behavior['is_potential'] == True].copy()

print(f'\n📊 PHÂN TÍCH KHÁCH HÀNG TIỀM NĂNG THEO LOẠI SÁCH:')
print(f'   Tổng số khách hàng tiềm năng: {len(potential_customers)}')

# Thống kê theo loại sách
book_type_stats = {}
for book_type, col_name in book_type_columns.items():
    customers_with_books = len(potential_customers[potential_customers[col_name] > 0])
    total_books = potential_customers[col_name].sum()
    avg_books = potential_customers[col_name].mean()
    
    book_type_stats[book_type] = {
        'customers': int(customers_with_books),
        'percentage': float((customers_with_books / len(potential_customers)) * 100),
        'total_books': int(total_books),
        'avg_books_per_customer': float(avg_books)
    }

# Sắp xếp theo số lượng khách hàng
sorted_book_types = sorted(book_type_stats.items(), key=lambda x: x[1]['customers'], reverse=True)

print(f'\n🏆 TOP LOẠI SÁCH ĐƯỢC KHÁCH HÀNG TIỀM NĂNG YÊU THÍCH:')
for i, (book_type, stats) in enumerate(sorted_book_types[:8], 1):
    print(f'   {i}. {book_type}')
    print(f'      👥 Khách hàng: {stats["customers"]} ({stats["percentage"]:.1f}%)')
    print(f'      📚 Tổng sách: {stats["total_books"]}')
    print(f'      📊 TB/khách hàng: {stats["avg_books_per_customer"]:.1f}')
    print()

# Tạo biểu đồ phân tích
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Phân Tích Khách Hàng Tiềm Năng Theo Loại Sách', fontsize=16, fontweight='bold')

# 1. Biểu đồ số lượng khách hàng theo loại sách
book_types = [item[0] for item in sorted_book_types]
customer_counts = [item[1]['customers'] for item in sorted_book_types]

axes[0, 0].barh(range(len(book_types)), customer_counts, alpha=0.7, color='skyblue')
axes[0, 0].set_yticks(range(len(book_types)))
axes[0, 0].set_yticklabels([bt[:15] + '...' if len(bt) > 15 else bt for bt in book_types])
axes[0, 0].set_xlabel('Số lượng khách hàng')
axes[0, 0].set_title('Số Khách Hàng Tiềm Năng Theo Loại Sách')
axes[0, 0].grid(True, alpha=0.3)

# 2. Biểu đồ phần trăm khách hàng
percentages = [item[1]['percentage'] for item in sorted_book_types]
axes[0, 1].barh(range(len(book_types)), percentages, alpha=0.7, color='lightcoral')
axes[0, 1].set_yticks(range(len(book_types)))
axes[0, 1].set_yticklabels([bt[:15] + '...' if len(bt) > 15 else bt for bt in book_types])
axes[0, 1].set_xlabel('Phần trăm (%)')
axes[0, 1].set_title('Phần Trăm Khách Hàng Tiềm Năng')
axes[0, 1].grid(True, alpha=0.3)

# 3. Biểu đồ tổng số sách bán được
total_books = [item[1]['total_books'] for item in sorted_book_types]
axes[1, 0].barh(range(len(book_types)), total_books, alpha=0.7, color='lightgreen')
axes[1, 0].set_yticks(range(len(book_types)))
axes[1, 0].set_yticklabels([bt[:15] + '...' if len(bt) > 15 else bt for bt in book_types])
axes[1, 0].set_xlabel('Tổng số sách')
axes[1, 0].set_title('Tổng Số Sách Bán Được Theo Loại')
axes[1, 0].grid(True, alpha=0.3)

# 4. Biểu đồ trung bình sách/khách hàng
avg_books = [item[1]['avg_books_per_customer'] for item in sorted_book_types]
axes[1, 1].barh(range(len(book_types)), avg_books, alpha=0.7, color='gold')
axes[1, 1].set_yticks(range(len(book_types)))
axes[1, 1].set_yticklabels([bt[:15] + '...' if len(bt) > 15 else bt for bt in book_types])
axes[1, 1].set_xlabel('Trung bình sách/khách hàng')
axes[1, 1].set_title('Trung Bình Số Sách Mỗi Khách Hàng')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('book_type_analysis.png', dpi=300, bbox_inches='tight')
print('✅ Đã lưu biểu đồ: book_type_analysis.png')

# Tạo dữ liệu JSON cho web app
potential_customers_data = []
for idx, row in potential_customers.head(100).iterrows():
    # Tính tổng số sách theo loại
    book_preferences = {}
    for book_type, col_name in book_type_columns.items():
        book_preferences[book_type] = int(row[col_name])
    
    # Tìm loại sách yêu thích nhất
    favorite_book_type = max(book_preferences.items(), key=lambda x: x[1])[0] if any(book_preferences.values()) else "Không xác định"
    
    customer_data = {
        'id': row['user_id'],
        'name': row['name'],
        'email': row['email'],
        'age': int(row['age']),
        'total_actions': int(row['total_actions']),
        'unique_products': int(row['unique_products']),
        'total_spending': int(row['total_spending']),
        'probability': 0.8,  # Default probability
        'book_preferences': book_preferences,
        'favorite_book_type': favorite_book_type
    }
    potential_customers_data.append(customer_data)

# Lưu dữ liệu JSON
with open('potential_customers_by_book_type.json', 'w', encoding='utf-8') as f:
    json.dump(potential_customers_data, f, ensure_ascii=False, indent=2)

print(f'✅ Đã lưu dữ liệu JSON: potential_customers_by_book_type.json')

# Tạo báo cáo chi tiết
report = {
    'summary': {
        'total_potential_customers': len(potential_customers),
        'total_book_types': len(book_type_mapping),
        'analysis_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    },
    'book_type_statistics': book_type_stats,
    'top_customers_by_book_type': {}
}

# Top khách hàng theo từng loại sách
for book_type, col_name in book_type_columns.items():
    top_customers = potential_customers.nlargest(5, col_name)
    report['top_customers_by_book_type'][book_type] = []
    
    for _, customer in top_customers.iterrows():
        if customer[col_name] > 0:  # Chỉ lấy khách hàng có mua loại sách này
            report['top_customers_by_book_type'][book_type].append({
                'name': str(customer['name']),
                'email': str(customer['email']),
                'books_count': int(customer[col_name]),
                'total_spending': int(customer['total_spending'])
            })

# Lưu báo cáo
with open('book_type_analysis_report.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f'✅ Đã lưu báo cáo: book_type_analysis_report.json')

print(f'\n🎯 INSIGHTS CHÍNH:')
print(f'   1. Loại sách phổ biến nhất: {sorted_book_types[0][0]} ({sorted_book_types[0][1]["percentage"]:.1f}% khách hàng)')
print(f'   2. Loại sách ít phổ biến nhất: {sorted_book_types[-1][0]} ({sorted_book_types[-1][1]["percentage"]:.1f}% khách hàng)')
print(f'   3. Trung bình {np.mean([stats["avg_books_per_customer"] for stats in book_type_stats.values()]):.1f} sách/khách hàng')

print(f'\n✨ HOÀN THÀNH PHÂN TÍCH THEO LOẠI SÁCH!')

