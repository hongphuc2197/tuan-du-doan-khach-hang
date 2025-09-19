#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

print('📊 TẠO BIỂU ĐỒ FEATURE IMPORTANCE')
print('=' * 50)

try:
    import matplotlib.pyplot as plt
    import numpy as np
    print('✅ Matplotlib imported successfully')
except ImportError as e:
    print(f'❌ Error importing matplotlib: {e}')
    print('Please install matplotlib: pip install matplotlib')
    sys.exit(1)

# Dữ liệu Feature Importance
features = ['Total Actions', 'Unique Products', 'Total Spending', 'Avg Spending', 'Age', 'Income', 'Education']
rf_importance = [0.067877, 0.069348, 0.324712, 0.293655, 0.159855, 0.034851, 0.049702]
gb_importance = [0.000516, 0.020839, 0.502674, 0.309984, 0.126699, 0.012385, 0.026904]

print(f'Features: {len(features)}')
print(f'RF Importance: {len(rf_importance)}')
print(f'GB Importance: {len(gb_importance)}')

try:
    # Tạo biểu đồ Random Forest
    plt.figure(figsize=(12, 8))
    bars = plt.barh(features, rf_importance, color='skyblue', alpha=0.7, edgecolor='black')
    plt.title('Random Forest - Feature Importance', fontsize=14, fontweight='bold')
    plt.xlabel('Importance Score', fontsize=12)
    plt.ylabel('Features', fontsize=12)
    
    # Thêm giá trị lên cột
    for bar, value in zip(bars, rf_importance):
        plt.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2, 
                 f'{value:.3f}', ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('rf_feature_importance.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('✅ Created: rf_feature_importance.png')
    
    # Tạo biểu đồ Gradient Boosting
    plt.figure(figsize=(12, 8))
    bars = plt.barh(features, gb_importance, color='lightgreen', alpha=0.7, edgecolor='black')
    plt.title('Gradient Boosting - Feature Importance', fontsize=14, fontweight='bold')
    plt.xlabel('Importance Score', fontsize=12)
    plt.ylabel('Features', fontsize=12)
    
    # Thêm giá trị lên cột
    for bar, value in zip(bars, gb_importance):
        plt.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2, 
                 f'{value:.3f}', ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('gb_feature_importance.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('✅ Created: gb_feature_importance.png')
    
    # Tạo biểu đồ so sánh
    plt.figure(figsize=(15, 8))
    x = np.arange(len(features))
    width = 0.35
    
    bars1 = plt.bar(x - width/2, rf_importance, width, label='Random Forest', color='skyblue', alpha=0.7)
    bars2 = plt.bar(x + width/2, gb_importance, width, label='Gradient Boosting', color='lightgreen', alpha=0.7)
    
    plt.xlabel('Features', fontsize=12, fontweight='bold')
    plt.ylabel('Importance Score', fontsize=12, fontweight='bold')
    plt.title('Feature Importance Comparison', fontsize=14, fontweight='bold')
    plt.xticks(x, features, rotation=45, ha='right')
    plt.legend()
    
    # Thêm giá trị lên cột
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                    f'{height:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('feature_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('✅ Created: feature_comparison.png')
    
    # Kiểm tra file đã tạo
    files_created = []
    for filename in ['rf_feature_importance.png', 'gb_feature_importance.png', 'feature_comparison.png']:
        if os.path.exists(filename):
            files_created.append(filename)
            print(f'✅ File exists: {filename}')
        else:
            print(f'❌ File not found: {filename}')
    
    print(f'\n🎉 Successfully created {len(files_created)} charts!')
    
except Exception as e:
    print(f'❌ Error creating charts: {e}')
    import traceback
    traceback.print_exc()

# In kết quả phân tích
print('\n=== FEATURE IMPORTANCE ANALYSIS ===')
print('\n🌲 RANDOM FOREST - Top Features:')
rf_sorted = sorted(zip(features, rf_importance), key=lambda x: x[1], reverse=True)
for i, (feature, importance) in enumerate(rf_sorted, 1):
    print(f'{i}. {feature}: {importance:.3f}')

print('\n🚀 GRADIENT BOOSTING - Top Features:')
gb_sorted = sorted(zip(features, gb_importance), key=lambda x: x[1], reverse=True)
for i, (feature, importance) in enumerate(gb_sorted, 1):
    print(f'{i}. {feature}: {importance:.3f}')

print('\n📊 Top 3 Most Important Features:')
avg_importance = [(rf_importance[i] + gb_importance[i]) / 2 for i in range(len(features))]
avg_sorted = sorted(zip(features, avg_importance), key=lambda x: x[1], reverse=True)
for i, (feature, importance) in enumerate(avg_sorted[:3], 1):
    print(f'{i}. {feature}: {importance:.3f}')

print('\n✅ Analysis complete!')
