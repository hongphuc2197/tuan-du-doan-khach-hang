#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tạo dữ liệu khách hàng tiềm năng cho API frontend
Format: user_id, age, total_actions, unique_products, total_spending, potential, probability
"""

import pandas as pd
import numpy as np
import json
import warnings
warnings.filterwarnings('ignore')

def generate_potential_customers_data():
    """Tạo dữ liệu khách hàng tiềm năng"""
    print("=== TẠO DỮ LIỆU KHÁCH HÀNG TIỀM NĂNG CHO API ===")
    
    # Tạo dữ liệu mẫu dựa trên dataset sinh viên thực tế
    np.random.seed(42)
    n_potential = 100  # Tăng số lượng để có nhiều dữ liệu hơn
    
    potential_customers = []
    for i in range(n_potential):
        # Tạo dữ liệu thực tế hơn cho sinh viên
        total_actions = np.random.randint(5, 50)  # Tổng số hành động
        unique_products = np.random.randint(2, min(total_actions, 20))  # Sản phẩm duy nhất
        total_spending = np.random.randint(500000, 5000000)  # Tổng chi tiêu
        age = np.random.randint(18, 25)
        
        # Tính probability dựa trên các yếu tố
        base_prob = 0.6
        age_factor = (25 - age) / 7 * 0.1  # Tuổi càng trẻ càng có tiềm năng
        action_factor = min(total_actions / 50, 1) * 0.2  # Hành động nhiều = tiềm năng cao
        spending_factor = min(total_spending / 5000000, 1) * 0.1  # Chi tiêu nhiều = tiềm năng cao
        
        probability = min(base_prob + age_factor + action_factor + spending_factor + np.random.normal(0, 0.05), 0.99)
        probability = max(probability, 0.1)  # Đảm bảo trong khoảng [0.1, 0.99]
        
        customer = {
            'user_id': f'user_{i+1:03d}',
            'age': int(age),
            'total_actions': int(total_actions),
            'unique_products': int(unique_products),
            'total_spending': int(total_spending),
            'potential': 'High' if probability > 0.8 else 'Medium' if probability > 0.6 else 'Low',
            'probability': round(probability, 3)
        }
        potential_customers.append(customer)
    
    # Sắp xếp theo probability giảm dần
    potential_customers.sort(key=lambda x: x['probability'], reverse=True)
    
    # Thêm thông tin bổ sung
    result = {
        'success': True,
        'total_customers': len(potential_customers),
        'high_potential': len([c for c in potential_customers if c['potential'] == 'High']),
        'medium_potential': len([c for c in potential_customers if c['potential'] == 'Medium']),
        'low_potential': len([c for c in potential_customers if c['potential'] == 'Low']),
        'average_probability': round(np.mean([c['probability'] for c in potential_customers]), 3),
        'average_actions': round(np.mean([c['total_actions'] for c in potential_customers]), 1),
        'average_spending': int(np.mean([c['total_spending'] for c in potential_customers])),
        'customers': potential_customers
    }
    
    print(f"✅ Đã tạo {len(potential_customers)} khách hàng tiềm năng")
    print(f"📊 Thống kê:")
    print(f"   • High potential: {result['high_potential']}")
    print(f"   • Medium potential: {result['medium_potential']}")
    print(f"   • Low potential: {result['low_potential']}")
    print(f"   • Average probability: {result['average_probability']}")
    print(f"   • Average actions: {result['average_actions']}")
    print(f"   • Average spending: {result['average_spending']:,} VNĐ")
    
    return result

def main():
    """Hàm chính"""
    try:
        # Tạo dữ liệu khách hàng tiềm năng
        data = generate_potential_customers_data()
        
        # In ra JSON để API có thể đọc
        print(json.dumps(data, ensure_ascii=False, indent=2))
        
    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'customers': []
        }
        print(json.dumps(error_result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
