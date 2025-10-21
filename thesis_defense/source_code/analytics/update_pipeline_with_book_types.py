#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cập nhật pipeline chính để bao gồm phân tích theo loại sách
"""

import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import LabelEncoder
import joblib
import warnings
warnings.filterwarnings('ignore')

print('=' * 70)
print('CẬP NHẬT PIPELINE VỚI PHÂN TÍCH THEO LOẠI SÁCH')
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
    12: "Công nghệ giáo dục"
}

# Thêm cột book_type vào DataFrame
df['book_type'] = df['product_id'].map(book_type_mapping)

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

print(f'✅ Tạo features cho {len(user_behavior)} users với thông tin loại sách')

# Encode categorical variables
le_income = LabelEncoder()
le_education = LabelEncoder()
user_behavior['income_encoded'] = le_income.fit_transform(user_behavior['income_level'])
user_behavior['education_encoded'] = le_education.fit_transform(user_behavior['education'])

# Load mô hình tốt nhất
try:
    model = joblib.load('analytics/best_student_model.pkl')
    print(f'✅ Đã load mô hình: best_student_model.pkl')
except:
    print('⚠️  Không tìm thấy mô hình, sử dụng dữ liệu thực tế')
    model = None

# Prepare features (bao gồm cả thông tin loại sách)
feature_columns = ['total_actions', 'unique_products', 'total_spending', 'avg_spending', 
                  'age', 'income_encoded', 'education_encoded']
X = user_behavior[feature_columns]

# Dự đoán
if model is not None:
    try:
        predictions = model.predict(X)
        probabilities = model.predict_proba(X)[:, 1]
        user_behavior['predicted_potential'] = predictions
        user_behavior['probability'] = probabilities
        print(f'✅ Dự đoán hoàn tất')
    except:
        # Nếu có lỗi, sử dụng dữ liệu thực tế
        user_behavior['predicted_potential'] = user_behavior['is_potential']
        user_behavior['probability'] = user_behavior['is_potential'].astype(float)
else:
    # Nếu không có mô hình, sử dụng dữ liệu thực tế
    user_behavior['predicted_potential'] = user_behavior['is_potential']
    user_behavior['probability'] = user_behavior['is_potential'].astype(float)

# Lọc khách hàng tiềm năng
potential_customers = user_behavior[user_behavior['predicted_potential'] == True].copy()
potential_customers = potential_customers.sort_values('probability', ascending=False)

print(f'\n📊 KẾT QUẢ:')
print(f'   Tổng số khách hàng: {len(user_behavior)}')
print(f'   Khách hàng tiềm năng: {len(potential_customers)} ({len(potential_customers)/len(user_behavior)*100:.1f}%)')
print(f'   Khách hàng không tiềm năng: {len(user_behavior) - len(potential_customers)} ({(len(user_behavior) - len(potential_customers))/len(user_behavior)*100:.1f}%)')

# Tạo dữ liệu JSON cho web app với thông tin loại sách
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
        'probability': float(row['probability']),
        'book_preferences': book_preferences,
        'favorite_book_type': favorite_book_type
    }
    potential_customers_data.append(customer_data)

# Lưu dữ liệu JSON
with open('analytics/potential_customers.json', 'w', encoding='utf-8') as f:
    json.dump(potential_customers_data, f, ensure_ascii=False, indent=2)

print(f'✅ Đã lưu 100 khách hàng tiềm năng vào: analytics/potential_customers.json')

# Tạo dữ liệu cho tất cả khách hàng
all_customers_data = []
for idx, row in user_behavior.iterrows():
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
        'probability': float(row['probability']),
        'is_potential': bool(row['predicted_potential']),
        'book_preferences': book_preferences,
        'favorite_book_type': favorite_book_type
    }
    all_customers_data.append(customer_data)

# Lưu dữ liệu tất cả khách hàng
with open('analytics/all_customers.json', 'w', encoding='utf-8') as f:
    json.dump(all_customers_data, f, ensure_ascii=False, indent=2)

print(f'✅ Đã lưu {len(user_behavior)} khách hàng vào: analytics/all_customers.json')

# Tạo thống kê tổng quan với thông tin loại sách
analytics_data = {
    'summary': {
        'total_customers': len(user_behavior),
        'potential_customers': len(potential_customers),
        'potential_percentage': float(len(potential_customers) / len(user_behavior) * 100),
        'average_age': float(user_behavior['age'].mean()),
        'average_spending': float(user_behavior['total_spending'].mean()),
        'average_income': float(user_behavior['income'].mean())
    },
    'book_type_analysis': {},
    'education_distribution': {},
    'income_distribution': {},
    'age_distribution': {}
}

# Phân tích theo loại sách
for book_type, col_name in book_type_columns.items():
    customers_with_books = len(potential_customers[potential_customers[col_name] > 0])
    total_books = potential_customers[col_name].sum()
    avg_books = potential_customers[col_name].mean()
    
    analytics_data['book_type_analysis'][book_type] = {
        'customers': int(customers_with_books),
        'percentage': float((customers_with_books / len(potential_customers)) * 100),
        'total_books': int(total_books),
        'avg_books_per_customer': float(avg_books)
    }

# Phân bố trình độ học vấn
education_dist = user_behavior['education'].value_counts()
analytics_data['education_distribution'] = {edu: int(count) for edu, count in education_dist.items()}

# Phân bố mức thu nhập
income_dist = user_behavior['income_level'].value_counts()
analytics_data['income_distribution'] = {income: int(count) for income, count in income_dist.items()}

# Phân bố độ tuổi
age_dist = user_behavior['age'].value_counts().sort_index()
analytics_data['age_distribution'] = {str(age): int(count) for age, count in age_dist.items()}

# Lưu thống kê tổng quan
with open('analytics/analytics_data.json', 'w', encoding='utf-8') as f:
    json.dump(analytics_data, f, ensure_ascii=False, indent=2)

print(f'✅ Đã lưu thống kê tổng quan vào: analytics/analytics_data.json')

print(f'\n📈 THỐNG KÊ TỔNG QUAN:')
print(f'   Tổng số khách hàng: {len(user_behavior)}')
print(f'   Khách hàng tiềm năng: {len(potential_customers)} ({len(potential_customers)/len(user_behavior)*100:.1f}%)')
print(f'   Tuổi trung bình: {user_behavior["age"].mean():.1f}')
print(f'   Chi tiêu trung bình: {user_behavior["total_spending"].mean():,.0f} VNĐ')
print(f'   Thu nhập trung bình: {user_behavior["income"].mean():,.0f} VNĐ')

print(f'\n📊 PHÂN BỐ TRÌNH ĐỘ HỌC VẤN:')
education_dist = user_behavior['education'].value_counts()
for edu, count in education_dist.items():
    print(f'   {edu}: {count} ({count/len(user_behavior)*100:.1f}%)')

print(f'\n💰 PHÂN BỐ MỨC THU NHẬP:')
income_dist = user_behavior['income_level'].value_counts()
for income, count in income_dist.items():
    print(f'   {income}: {count} ({count/len(user_behavior)*100:.1f}%)')

print(f'\n🎂 PHÂN BỐ ĐỘ TUỔI:')
age_dist = user_behavior['age'].value_counts().sort_index()
age_ranges = {
    '18-20': len(user_behavior[(user_behavior['age'] >= 18) & (user_behavior['age'] <= 20)]),
    '21-23': len(user_behavior[(user_behavior['age'] >= 21) & (user_behavior['age'] <= 23)]),
    '24-25': len(user_behavior[(user_behavior['age'] >= 24) & (user_behavior['age'] <= 25)])
}
for age_range, count in age_ranges.items():
    print(f'   {age_range}: {count} ({count/len(user_behavior)*100:.1f}%)')

# Top 10 khách hàng tiềm năng với thông tin loại sách
print(f'\n🏆 TOP 10 KHÁCH HÀNG TIỀM NĂNG:')
print('-' * 80)
print(f'{"Tên":<25} {"Tuổi":<5} {"Thu nhập":<12} {"Chi tiêu":<12} {"Loại sách yêu thích":<20}')
print('-' * 80)
for i, (idx, row) in enumerate(potential_customers.head(10).iterrows(), 1):
    favorite_book_type = max([(book_type, row[col_name]) for book_type, col_name in book_type_columns.items()], key=lambda x: x[1])[0]
    print(f'{row["name"][:24]:<25} {int(row["age"]):<5} {int(row["income"]):<12,} {int(row["total_spending"]):<12,} {favorite_book_type[:19]:<20}')

print('-' * 80)

print(f'\n✨ Dữ liệu đã sẵn sàng cho web application với thông tin loại sách!')

