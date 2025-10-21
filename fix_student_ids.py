#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sửa ID và user_id có pattern student_ thành UUID format đồng bộ
"""

import pandas as pd
import uuid
import random

print('=' * 70)
print('SỬA ID VÀ USER_ID THÀNH FORMAT ĐỒNG BỘ')
print('=' * 70)

# Đọc dữ liệu
df = pd.read_csv('user_actions_students_576.csv')
print(f'✅ Đọc dữ liệu: {len(df)} records')

# Tìm các records có ID pattern student_
student_records = df[df['id'].str.contains('student_', na=False)]
unique_student_users = student_records['user_id'].unique()

print(f'\n📊 PHÂN TÍCH:')
print(f'   Tổng records: {len(df)}')
print(f'   Records có ID student_: {len(student_records)}')
print(f'   Unique users có ID student_: {len(unique_student_users)}')

# Tạo mapping từ user_id cũ sang UUID mới
user_id_mapping = {}
for old_user_id in unique_student_users:
    new_user_id = str(uuid.uuid4())
    user_id_mapping[old_user_id] = new_user_id

print(f'\n🔄 ĐANG SỬA ID...')

# Sửa user_id
replaced_users = 0
for old_user_id, new_user_id in user_id_mapping.items():
    mask = df['user_id'] == old_user_id
    count = mask.sum()
    df.loc[mask, 'user_id'] = new_user_id
    replaced_users += count
    print(f'   ✓ {old_user_id} → {new_user_id} ({count} records)')

# Sửa id (tạo UUID mới cho mỗi record)
print(f'\n🔄 ĐANG SỬA ID RECORDS...')
student_mask = df['id'].str.contains('student_', na=False)
student_count = student_mask.sum()

# Tạo UUID mới cho các records có ID student_
new_ids = [str(uuid.uuid4()) for _ in range(student_count)]
df.loc[student_mask, 'id'] = new_ids

print(f'✅ Đã sửa {student_count} ID records')

print(f'\n✅ HOÀN TẤT!')
print(f'   Đã sửa {replaced_users} records')
print(f'   Cho {len(unique_student_users)} users')

# Lưu file mới
output_file = 'user_actions_students_576_sync_ids.csv'
df.to_csv(output_file, index=False)
print(f'\n💾 Đã lưu file mới: {output_file}')

# Kiểm tra kết quả
print(f'\n📋 KIỂM TRA KẾT QUẢ:')
print(f'   Tổng records: {len(df)}')
print(f'   Records còn ID student_: {len(df[df["id"].str.contains("student_", na=False)])}')
print(f'   Unique users: {df["user_id"].nunique()}')

# Hiển thị ví dụ
print(f'\n🎯 VÍ DỤ ID MỚI:')
sample_records = df[df['user_id'].isin(list(user_id_mapping.values())[:3])]
for idx, row in sample_records.head(3).iterrows():
    print(f'   ID: {row["id"]}')
    print(f'   User ID: {row["user_id"]}')
    print(f'   Name: {row["name"]}')
    print()

print(f'\n✨ Tất cả ID đã được sửa thành format đồng bộ!')

