#!/usr/bin/env python3
import pandas as pd
import numpy as np
import json
import sys
import os

# Thêm đường dẫn để import model
sys.path.append('/Users/trantuan/tuan-du-doan-khach-hang')

def main():
    try:
        # Load dữ liệu sinh viên
        df = pd.read_csv('/Users/trantuan/tuan-du-doan-khach-hang/user_actions_students_576.csv')
        
        # Tạo features đơn giản
        user_summary = df.groupby('user_id').agg({
            'price': ['sum', 'mean', 'count'],
            'year_birth': 'first',
            'income': 'first',
            'kidhome': 'first',
            'teenhome': 'first',
            'education': 'first',
            'income_level': 'first'
        }).reset_index()
        
        # Flatten column names
        user_summary.columns = ['user_id', 'total_spent', 'avg_purchase_value', 'purchase_count', 
                               'year_birth', 'income', 'kidhome', 'teenhome', 'education', 'income_level']
        
        # Tính toán các features cần thiết
        user_summary['age'] = 2024 - user_summary['year_birth']
        user_summary['recency'] = np.random.randint(1, 15, len(user_summary))  # Random recency
        user_summary['frequency'] = user_summary['purchase_count']
        user_summary['monetary'] = user_summary['total_spent']
        user_summary['purchase_rate'] = user_summary['purchase_count'] / 20  # Giả sử 20 actions trung bình
        
        # Tạo xác suất giả (để test nhanh)
        user_summary['probability'] = np.random.uniform(0.1, 0.99, len(user_summary))
        
        # Sắp xếp theo xác suất giảm dần
        user_summary = user_summary.sort_values('probability', ascending=False)
        
        # Chỉ lấy top 50 để load nhanh hơn
        top_customers = user_summary.head(50)
        
        # Chuyển đổi sang format JSON
        result = []
        for _, row in top_customers.iterrows():
            result.append({
                "ID": str(row['user_id']),
                "probability": float(row['probability']),
                "totalSpent": int(row['total_spent']),
                "avgPurchaseValue": int(row['avg_purchase_value']),
                "purchaseCount": int(row['purchase_count']),
                "age": int(row['age']),
                "education": str(row['education']),
                "income_level": str(row['income_level']),
                "recency": int(row['recency']),
                "frequency": int(row['frequency']),
                "monetary": int(row['monetary']),
                "purchase_rate": float(row['purchase_rate'])
            })
        
        # In kết quả JSON
        print(json.dumps(result))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
