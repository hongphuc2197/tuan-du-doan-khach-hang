#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

print('🌈 TẠO HEATMAP VỚI MÀU SẮC SÁNG')
print('=' * 50)

try:
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    print('✅ Libraries imported successfully')
except ImportError as e:
    print(f'❌ Error importing libraries: {e}')
    print('Please install required packages: pip install pandas numpy matplotlib')
    sys.exit(1)

# Dữ liệu mẫu correlation matrix
features = ['is_potential', 'unique_products', 'total_spending', 'avg_spending', 'age', 'total_actions']
corr_data = np.array([
    [1.000, 0.234, 0.567, 0.445, 0.123, 0.345],
    [0.234, 1.000, 0.234, 0.123, 0.456, 0.234],
    [0.567, 0.234, 1.000, 0.789, 0.234, 0.567],
    [0.445, 0.123, 0.789, 1.000, 0.123, 0.345],
    [0.123, 0.456, 0.234, 0.123, 1.000, 0.234],
    [0.345, 0.234, 0.567, 0.345, 0.234, 1.000]
])

print(f'✅ Data prepared: {corr_data.shape}')

try:
    # Tạo heatmap với màu sáng
    plt.figure(figsize=(10, 8))
    plt.imshow(corr_data, cmap='viridis', aspect='auto')
    plt.colorbar()
    
    # Thêm labels
    plt.xticks(range(len(features)), features, rotation=45)
    plt.yticks(range(len(features)), features)
    
    # Thêm giá trị
    for i in range(len(features)):
        for j in range(len(features)):
            plt.text(j, i, f'{corr_data[i, j]:.2f}', ha='center', va='center', 
                    fontweight='bold', color='white', fontsize=10)
    
    plt.title('Correlation Matrix - Bright Colors', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('bright_heatmap.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print('✅ Created: bright_heatmap.png')
    
    # Tạo heatmap với màu khác
    plt.figure(figsize=(10, 8))
    plt.imshow(corr_data, cmap='plasma', aspect='auto')
    plt.colorbar()
    
    plt.xticks(range(len(features)), features, rotation=45)
    plt.yticks(range(len(features)), features)
    
    for i in range(len(features)):
        for j in range(len(features)):
            plt.text(j, i, f'{corr_data[i, j]:.2f}', ha='center', va='center', 
                    fontweight='bold', color='white', fontsize=10)
    
    plt.title('Correlation Matrix - Hot Colors', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('hot_heatmap.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print('✅ Created: hot_heatmap.png')
    
    # Kiểm tra file đã tạo
    files_created = []
    for filename in ['bright_heatmap.png', 'hot_heatmap.png']:
        if os.path.exists(filename):
            files_created.append(filename)
            print(f'✅ File exists: {filename}')
        else:
            print(f'❌ File not found: {filename}')
    
    print(f'\n🎉 Successfully created {len(files_created)} heatmaps!')
    
except Exception as e:
    print(f'❌ Error creating heatmaps: {e}')
    import traceback
    traceback.print_exc()

print('\n📊 Correlation Matrix:')
print('Features:', features)
print('Data shape:', corr_data.shape)
print('Max correlation:', corr_data.max())
print('Min correlation:', corr_data.min())

print('\n✅ Heatmap creation complete!')
