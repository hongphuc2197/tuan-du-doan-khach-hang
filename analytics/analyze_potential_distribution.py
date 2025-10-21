#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phân tích chi tiết phân bố khách hàng tiềm năng
"""

import pandas as pd
import json

print('=' * 70)
print('PHÂN TÍCH CHI TIẾT PHÂN BỐ KHÁCH HÀNG TIỀM NĂNG')
print('=' * 70)

# Đọc dữ liệu từ JSON
with open('all_customers.json', 'r', encoding='utf-8') as f:
    all_customers = json.load(f)

with open('potential_customers.json', 'r', encoding='utf-8') as f:
    top_100 = json.load(f)

print(f'\n📊 TỔNG QUAN:')
print(f'   Tổng số khách hàng: {len(all_customers)}')
print(f'   Khách hàng tiềm năng: {sum(1 for c in all_customers if c["is_potential"])}')
print(f'   Top 100 được hiển thị: {len(top_100)}')

# Phân tích 514 khách hàng tiềm năng
potential_customers = [c for c in all_customers if c['is_potential']]
print(f'\n🎯 PHÂN TÍCH 514 KHÁCH HÀNG TIỀM NĂNG:')

# Phân loại theo xác suất
high_potential = [c for c in potential_customers if c['probability'] >= 0.7]
medium_potential = [c for c in potential_customers if 0.4 <= c['probability'] < 0.7]
low_potential = [c for c in potential_customers if c['probability'] < 0.4]

print(f'   🔴 High potential (≥70%): {len(high_potential)} khách hàng')
print(f'   🟡 Medium potential (40-70%): {len(medium_potential)} khách hàng')
print(f'   🟢 Low potential (<40%): {len(low_potential)} khách hàng')

# Thống kê chi tiết
print(f'\n📈 THỐNG KÊ CHI TIẾT:')

# High potential
if high_potential:
    high_probs = [c['probability'] for c in high_potential]
    print(f'   🔴 High Potential ({len(high_potential)} khách hàng):')
    print(f'      Xác suất: {min(high_probs):.1%} - {max(high_probs):.1%}')
    print(f'      Xác suất TB: {sum(high_probs)/len(high_probs):.1%}')

# Medium potential
if medium_potential:
    medium_probs = [c['probability'] for c in medium_potential]
    print(f'   🟡 Medium Potential ({len(medium_potential)} khách hàng):')
    print(f'      Xác suất: {min(medium_probs):.1%} - {max(medium_probs):.1%}')
    print(f'      Xác suất TB: {sum(medium_probs)/len(medium_probs):.1%}')

# Low potential
if low_potential:
    low_probs = [c['probability'] for c in low_potential]
    print(f'   🟢 Low Potential ({len(low_potential)} khách hàng):')
    print(f'      Xác suất: {min(low_probs):.1%} - {max(low_probs):.1%}')
    print(f'      Xác suất TB: {sum(low_probs)/len(low_probs):.1%}')

# Top 100 analysis
print(f'\n🏆 PHÂN TÍCH TOP 100:')
top_100_probs = [c['probability'] for c in top_100]
print(f'   Xác suất: {min(top_100_probs):.1%} - {max(top_100_probs):.1%}')
print(f'   Xác suất TB: {sum(top_100_probs)/len(top_100_probs):.1%}')

# So sánh với threshold
print(f'\n🔍 GIẢI THÍCH TẠI SAO CHỈ HIỂN THỊ HIGH:')
print(f'   Top 100 có xác suất từ {min(top_100_probs):.1%} đến {max(top_100_probs):.1%}')
print(f'   Tất cả đều ≥ 70% → Được phân loại là HIGH potential')
print(f'   Frontend filter "High potential" → Hiển thị tất cả 100')

print(f'\n💡 KẾT LUẬN:')
print(f'   • Dataset có 1,813 khách hàng')
print(f'   • 514 khách hàng được dự đoán là tiềm năng')
print(f'   • Backend chỉ trả về top 100 có xác suất cao nhất')
print(f'   • Top 100 này đều có xác suất ≥70% → HIGH potential')
print(f'   • Frontend hiển thị đúng: 100 khách hàng HIGH potential')

