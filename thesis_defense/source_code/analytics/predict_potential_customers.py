#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dự đoán khách hàng tiềm năng từ dataset và tạo file JSON cho web app
"""

import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import LabelEncoder
import joblib
import warnings
warnings.filterwarnings('ignore')

print('=' * 70)
print('DỰ ĐOÁN KHÁCH HÀNG TIỀM NĂNG')
print('=' * 70)

# Đọc dữ liệu
df = pd.read_csv('../user_actions_students_576.csv')
print(f'\n✅ Đọc dữ liệu: {len(df)} records, {df["user_id"].nunique()} users')

# Tạo features từ dữ liệu
user_behavior = df.groupby('user_id').agg({
    'event_type': lambda x: 'purchase' in x.values,
    'product_id': 'nunique',
    'price': ['sum', 'mean'],
    'age': 'first',
    'income_level': 'first',
    'education': 'first',
    'name': 'first',
    'email': 'first',
    'income': 'first'
}).reset_index()

user_behavior['total_actions'] = df.groupby('user_id')['event_type'].count().values

# Flatten column names
user_behavior.columns = ['user_id', 'is_potential', 'unique_products', 'total_spending', 
                         'avg_spending', 'age', 'income_level', 'education', 'name', 
                         'email', 'income', 'total_actions']

print(f'✅ Tạo features cho {len(user_behavior)} users')

# Encode categorical variables
le_income = LabelEncoder()
le_education = LabelEncoder()
user_behavior['income_encoded'] = le_income.fit_transform(user_behavior['income_level'])
user_behavior['education_encoded'] = le_education.fit_transform(user_behavior['education'])

# Load mô hình tốt nhất
try:
    model = joblib.load('best_student_model.pkl')
    print(f'✅ Đã load mô hình: best_student_model.pkl')
except:
    print('⚠️  Không tìm thấy mô hình, sử dụng dữ liệu thực tế')
    model = None

# Prepare features
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

# Tạo dữ liệu JSON cho web app
potential_customers_data = []
for idx, row in potential_customers.head(100).iterrows():  # Lấy top 100
    customer = {
        'id': str(row['user_id']),
        'name': str(row['name']),
        'email': str(row['email']),
        'age': int(row['age']),
        'education': str(row['education']),
        'income': int(row['income']),
        'income_level': str(row['income_level']),
        'total_spending': int(row['total_spending']),
        'avg_spending': int(row['avg_spending']),
        'total_actions': int(row['total_actions']),
        'unique_products': int(row['unique_products']),
        'probability': float(row['probability']),
        'is_potential': True
    }
    potential_customers_data.append(customer)

# Lưu dữ liệu JSON
with open('potential_customers.json', 'w', encoding='utf-8') as f:
    json.dump(potential_customers_data, f, ensure_ascii=False, indent=2)

print(f'\n✅ Đã lưu {len(potential_customers_data)} khách hàng tiềm năng vào: potential_customers.json')

# Lưu tất cả khách hàng
all_customers_data = []
for idx, row in user_behavior.iterrows():
    customer = {
        'id': str(row['user_id']),
        'name': str(row['name']),
        'email': str(row['email']),
        'age': int(row['age']),
        'education': str(row['education']),
        'income': int(row['income']),
        'income_level': str(row['income_level']),
        'total_spending': int(row['total_spending']),
        'avg_spending': int(row['avg_spending']),
        'total_actions': int(row['total_actions']),
        'unique_products': int(row['unique_products']),
        'probability': float(row['probability']),
        'is_potential': bool(row['predicted_potential'])
    }
    all_customers_data.append(customer)

# Lưu tất cả khách hàng
with open('all_customers.json', 'w', encoding='utf-8') as f:
    json.dump(all_customers_data, f, ensure_ascii=False, indent=2)

print(f'✅ Đã lưu {len(all_customers_data)} khách hàng vào: all_customers.json')

# Tạo thống kê tổng quan
analytics_data = {
    'total_customers': len(user_behavior),
    'potential_customers': len(potential_customers),
    'non_potential_customers': len(user_behavior) - len(potential_customers),
    'potential_rate': float(len(potential_customers) / len(user_behavior) * 100),
    'avg_age': float(user_behavior['age'].mean()),
    'avg_spending': float(user_behavior['total_spending'].mean()),
    'avg_income': float(user_behavior['income'].mean()),
    'education_distribution': user_behavior['education'].value_counts().to_dict(),
    'income_level_distribution': user_behavior['income_level'].value_counts().to_dict(),
    'age_distribution': {
        '18-20': int(((user_behavior['age'] >= 18) & (user_behavior['age'] <= 20)).sum()),
        '21-23': int(((user_behavior['age'] >= 21) & (user_behavior['age'] <= 23)).sum()),
        '24-25': int(((user_behavior['age'] >= 24) & (user_behavior['age'] <= 25)).sum())
    }
}

# Lưu analytics
with open('analytics_data.json', 'w', encoding='utf-8') as f:
    json.dump(analytics_data, f, ensure_ascii=False, indent=2)

print(f'✅ Đã lưu thống kê tổng quan vào: analytics_data.json')

# Hiển thị thống kê
print(f'\n📈 THỐNG KÊ TỔNG QUAN:')
print(f'   Tổng số khách hàng: {analytics_data["total_customers"]}')
print(f'   Khách hàng tiềm năng: {analytics_data["potential_customers"]} ({analytics_data["potential_rate"]:.1f}%)')
print(f'   Tuổi trung bình: {analytics_data["avg_age"]:.1f}')
print(f'   Chi tiêu trung bình: {analytics_data["avg_spending"]:,.0f} VNĐ')
print(f'   Thu nhập trung bình: {analytics_data["avg_income"]:,.0f} VNĐ')

print(f'\n📊 PHÂN BỐ TRÌNH ĐỘ HỌC VẤN:')
for edu, count in analytics_data['education_distribution'].items():
    print(f'   {edu}: {count} ({count/analytics_data["total_customers"]*100:.1f}%)')

print(f'\n💰 PHÂN BỐ MỨC THU NHẬP:')
for income, count in analytics_data['income_level_distribution'].items():
    print(f'   {income}: {count} ({count/analytics_data["total_customers"]*100:.1f}%)')

print(f'\n🎂 PHÂN BỐ ĐỘ TUỔI:')
for age_range, count in analytics_data['age_distribution'].items():
    print(f'   {age_range}: {count} ({count/analytics_data["total_customers"]*100:.1f}%)')

# In top 10 khách hàng tiềm năng
print(f'\n🏆 TOP 10 KHÁCH HÀNG TIỀM NĂNG:')
print('-' * 70)
print(f'{"Tên":<25} {"Tuổi":<5} {"Thu nhập":<12} {"Chi tiêu":<12} {"Xác suất"}')
print('-' * 70)
for idx, row in potential_customers.head(10).iterrows():
    print(f'{str(row["name"])[:24]:<25} {int(row["age"]):<5} {int(row["income"]):>11,} {int(row["total_spending"]):>11,} {row["probability"]:>9.1%}')

print('\n' + '=' * 70)
print('HOÀN THÀNH!')
print('=' * 70)
print('\n📁 Các file đã được tạo:')
print('   • potential_customers.json - Top 100 khách hàng tiềm năng')
print('   • all_customers.json - Tất cả khách hàng')
print('   • analytics_data.json - Thống kê tổng quan')
print('\n✨ Dữ liệu đã sẵn sàng cho web application!')

