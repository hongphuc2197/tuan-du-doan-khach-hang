#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tạo correlation heatmap với màu sắc sáng như hình mẫu
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_bright_correlation_heatmap():
    """Tạo correlation heatmap với màu sắc sáng"""
    
    print('🌈 TẠO CORRELATION HEATMAP VỚI MÀU SẮC SÁNG')
    print('=' * 60)
    
    try:
        # Đọc dữ liệu
        if os.path.exists('user_actions_students_576.csv'):
            df = pd.read_csv('user_actions_students_576.csv')
            print(f'✅ Đã đọc dữ liệu: {len(df)} records')
            
            # Tạo features từ dữ liệu thực
            user_behavior = df.groupby('user_id').agg({
                'event_type': lambda x: 'purchase' in x.values,
                'product_id': 'nunique',
                'price': ['sum', 'mean'],
                'age': 'first'
            })
            
            user_behavior['total_actions'] = df.groupby('user_id')['event_type'].count()
            user_behavior.columns = ['is_potential', 'unique_products', 'total_spending', 'avg_spending', 'age', 'total_actions']
            
            # Tính correlation
            corr_matrix = user_behavior.corr()
            
        else:
            print('⚠️  Không tìm thấy file dữ liệu, sử dụng dữ liệu mẫu')
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
            corr_matrix = pd.DataFrame(corr_data, index=features, columns=features)
        
        print(f'📊 Ma trận correlation: {corr_matrix.shape}')
        print(f'📈 Range: {corr_matrix.min().min():.3f} đến {corr_matrix.max().max():.3f}')
        
        # 1. Tạo heatmap với màu RdBu_r (giống hình mẫu nhất)
        plt.style.use('default')
        plt.figure(figsize=(12, 10))
        
        # Sử dụng seaborn để tạo heatmap đẹp
        sns.heatmap(corr_matrix, 
                    annot=True,           # Hiển thị giá trị số
                    cmap='RdBu_r',        # Màu đỏ-xanh dương (đảo ngược)
                    center=0,             # Trung tâm tại 0
                    square=True,          # Ô vuông
                    fmt='.3f',            # Format số thập phân
                    cbar_kws={'shrink': 0.8, 'aspect': 20},
                    linewidths=0.5,       # Đường viền mỏng
                    linecolor='white',    # Đường viền trắng
                    annot_kws={'fontsize': 11, 'fontweight': 'bold'})
        
        plt.title('Ma trận tương quan - Màu sáng (RdBu_r)', 
                 fontsize=18, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig('bright_correlation_heatmap_rdbu.png', 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print('✅ Đã tạo: bright_correlation_heatmap_rdbu.png')
        
        # 2. Tạo heatmap với màu coolwarm
        plt.figure(figsize=(12, 10))
        
        sns.heatmap(corr_matrix, 
                    annot=True,
                    cmap='coolwarm',      # Màu lạnh-nóng
                    center=0,
                    square=True,
                    fmt='.3f',
                    cbar_kws={'shrink': 0.8, 'aspect': 20},
                    linewidths=0.5,
                    linecolor='white',
                    annot_kws={'fontsize': 11, 'fontweight': 'bold'})
        
        plt.title('Ma trận tương quan - Màu lạnh-nóng (coolwarm)', 
                 fontsize=18, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig('bright_correlation_heatmap_coolwarm.png', 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print('✅ Đã tạo: bright_correlation_heatmap_coolwarm.png')
        
        # 3. Tạo heatmap với màu RdYlBu_r (màu sáng nhất)
        plt.figure(figsize=(12, 10))
        
        sns.heatmap(corr_matrix, 
                    annot=True,
                    cmap='RdYlBu_r',      # Màu đỏ-vàng-xanh dương
                    center=0,
                    square=True,
                    fmt='.3f',
                    cbar_kws={'shrink': 0.8, 'aspect': 20},
                    linewidths=0.5,
                    linecolor='white',
                    annot_kws={'fontsize': 11, 'fontweight': 'bold'})
        
        plt.title('Ma trận tương quan - Màu sáng nhất (RdYlBu_r)', 
                 fontsize=18, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig('bright_correlation_heatmap_rdylbu.png', 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print('✅ Đã tạo: bright_correlation_heatmap_rdylbu.png')
        
        # 4. Tạo heatmap với màu Spectral_r
        plt.figure(figsize=(12, 10))
        
        sns.heatmap(corr_matrix, 
                    annot=True,
                    cmap='Spectral_r',    # Màu quang phổ
                    center=0,
                    square=True,
                    fmt='.3f',
                    cbar_kws={'shrink': 0.8, 'aspect': 20},
                    linewidths=0.5,
                    linecolor='white',
                    annot_kws={'fontsize': 11, 'fontweight': 'bold'})
        
        plt.title('Ma trận tương quan - Màu quang phổ (Spectral_r)', 
                 fontsize=18, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig('bright_correlation_heatmap_spectral.png', 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print('✅ Đã tạo: bright_correlation_heatmap_spectral.png')
        
        print('\n🎉 ĐÃ TẠO XONG 4 HEATMAP VỚI MÀU SẮC SÁNG!')
        print('\n📁 Các file đã tạo:')
        print('1. bright_correlation_heatmap_rdbu.png - Màu đỏ-xanh dương (giống hình mẫu nhất)')
        print('2. bright_correlation_heatmap_coolwarm.png - Màu lạnh-nóng')
        print('3. bright_correlation_heatmap_rdylbu.png - Màu đỏ-vàng-xanh dương (sáng nhất)')
        print('4. bright_correlation_heatmap_spectral.png - Màu quang phổ')
        
        print('\n💡 KHUYẾN NGHỊ:')
        print('🥇 Giống hình mẫu nhất: bright_correlation_heatmap_rdbu.png')
        print('🥈 Màu sáng nhất: bright_correlation_heatmap_rdylbu.png')
        print('🥉 Dễ nhìn nhất: bright_correlation_heatmap_coolwarm.png')
        
        # Hiển thị thông tin correlation
        print('\n📊 CHI TIẾT CORRELATION:')
        print(corr_matrix.round(3))
        
        return True
        
    except Exception as e:
        print(f'❌ Lỗi: {e}')
        print('\n💡 HƯỚNG DẪN KHẮC PHỤC:')
        print('1. Cài đặt thư viện: pip install pandas matplotlib seaborn')
        print('2. Đảm bảo file user_actions_students_576.csv tồn tại')
        print('3. Chạy lại script này')
        return False

if __name__ == "__main__":
    create_bright_correlation_heatmap()
