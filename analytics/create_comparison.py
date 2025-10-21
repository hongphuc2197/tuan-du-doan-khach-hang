#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tạo biểu đồ so sánh giữa phiên bản cũ (bị cắt) và phiên bản mới (hoàn chỉnh)
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
import numpy as np

def create_comparison():
    """Tạo biểu đồ so sánh hai phiên bản"""
    print("=== TẠO BIỂU ĐỒ SO SÁNH PHIÊN BẢN CŨ VÀ MỚI ===")
    
    # Tạo figure với 2 subplot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    # Tiêu đề chính
    fig.suptitle('So sánh: Phiên bản cũ (bị cắt) vs Phiên bản mới (hoàn chỉnh)', 
                 fontsize=16, fontweight='bold', y=0.95)
    
    # Subplot 1: Phiên bản cũ (bị cắt)
    ax1.set_title('❌ Phiên bản cũ - Bị cắt', fontsize=14, fontweight='bold', color='red')
    ax1.set_facecolor('#ffe6e6')
    
    # Vẽ một hình chữ nhật để mô tả phiên bản cũ bị cắt
    old_rect = Rectangle((0.1, 0.1), 0.8, 0.8, 
                        facecolor='#ffcccc', edgecolor='red', linewidth=3,
                        transform=ax1.transAxes)
    ax1.add_patch(old_rect)
    
    # Vẽ các đường cắt
    ax1.axvline(x=0.7, color='red', linestyle='--', linewidth=3, alpha=0.7)
    ax1.axhline(y=0.6, color='red', linestyle='--', linewidth=3, alpha=0.7)
    
    # Thêm text mô tả
    ax1.text(0.5, 0.8, 'Bảng dữ liệu bị cắt', ha='center', va='center', 
             fontsize=12, fontweight='bold', color='red', transform=ax1.transAxes)
    ax1.text(0.5, 0.6, 'Biểu đồ không hiển thị đầy đủ', ha='center', va='center', 
             fontsize=12, fontweight='bold', color='red', transform=ax1.transAxes)
    ax1.text(0.5, 0.4, 'Thống kê bị mất', ha='center', va='center', 
             fontsize=12, fontweight='bold', color='red', transform=ax1.transAxes)
    ax1.text(0.5, 0.2, 'Layout không tối ưu', ha='center', va='center', 
             fontsize=12, fontweight='bold', color='red', transform=ax1.transAxes)
    
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.axis('off')
    
    # Subplot 2: Phiên bản mới (hoàn chỉnh)
    ax2.set_title('✅ Phiên bản mới - Hoàn chỉnh', fontsize=14, fontweight='bold', color='green')
    ax2.set_facecolor('#e6ffe6')
    
    # Vẽ layout hoàn chỉnh
    # Header
    header_rect = Rectangle((0.05, 0.85), 0.9, 0.1, 
                           facecolor='#2c3e50', edgecolor='none', transform=ax2.transAxes)
    ax2.add_patch(header_rect)
    
    # Bảng dữ liệu
    table_rect = Rectangle((0.05, 0.5), 0.9, 0.3, 
                          facecolor='#ecf0f1', edgecolor='#bdc3c7', linewidth=1,
                          transform=ax2.transAxes)
    ax2.add_patch(table_rect)
    
    # Thống kê
    stats_rect = Rectangle((0.05, 0.35), 0.9, 0.1, 
                          facecolor='#e8f5e8', edgecolor='#27ae60', linewidth=2,
                          transform=ax2.transAxes)
    ax2.add_patch(stats_rect)
    
    # Biểu đồ 1 (phân phối xác suất)
    chart1_rect = Rectangle((0.7, 0.6), 0.25, 0.15, 
                           facecolor='#3498db', edgecolor='#2980b9', linewidth=1,
                           transform=ax2.transAxes)
    ax2.add_patch(chart1_rect)
    
    # Biểu đồ 2 (pie chart)
    chart2_rect = Rectangle((0.7, 0.4), 0.25, 0.15, 
                           facecolor='#e74c3c', edgecolor='#c0392b', linewidth=1,
                           transform=ax2.transAxes)
    ax2.add_patch(chart2_rect)
    
    # Biểu đồ 3 (so sánh chi tiêu)
    chart3_rect = Rectangle((0.7, 0.2), 0.25, 0.15, 
                           facecolor='#f39c12', edgecolor='#e67e22', linewidth=1,
                           transform=ax2.transAxes)
    ax2.add_patch(chart3_rect)
    
    # Thêm text mô tả
    ax2.text(0.5, 0.9, 'Hình 5.X - Giao Diện Hoàn Chỉnh', ha='center', va='center', 
             fontsize=12, fontweight='bold', color='white', transform=ax2.transAxes)
    ax2.text(0.5, 0.65, 'Bảng dữ liệu đầy đủ', ha='center', va='center', 
             fontsize=10, fontweight='bold', color='#2c3e50', transform=ax2.transAxes)
    ax2.text(0.5, 0.4, 'Thống kê tổng quan', ha='center', va='center', 
             fontsize=10, fontweight='bold', color='#2c3e50', transform=ax2.transAxes)
    ax2.text(0.825, 0.675, 'Phân phối\nxác suất', ha='center', va='center', 
             fontsize=9, fontweight='bold', color='white', transform=ax2.transAxes)
    ax2.text(0.825, 0.475, 'Phân bố\ntiềm năng', ha='center', va='center', 
             fontsize=9, fontweight='bold', color='white', transform=ax2.transAxes)
    ax2.text(0.825, 0.275, 'So sánh\nchi tiêu', ha='center', va='center', 
             fontsize=9, fontweight='bold', color='white', transform=ax2.transAxes)
    
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis('off')
    
    # Thêm ghi chú
    fig.text(0.5, 0.02, '✨ Phiên bản mới có kích thước lớn hơn (24x16), layout tối ưu, và hiển thị đầy đủ tất cả thông tin', 
             ha='center', va='bottom', fontsize=12, fontweight='bold', 
             bbox=dict(boxstyle="round,pad=0.5", facecolor='#e8f5e8', edgecolor='#27ae60'))
    
    plt.tight_layout()
    plt.savefig('Hinh_5_X_Comparison_Old_vs_New.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✅ Đã tạo biểu đồ so sánh: Hinh_5_X_Comparison_Old_vs_New.png")
    
    return fig

def main():
    """Hàm chính"""
    print("🎯 TẠO BIỂU ĐỒ SO SÁNH PHIÊN BẢN CŨ VÀ MỚI")
    print("=" * 60)
    
    try:
        # Tạo biểu đồ so sánh
        fig = create_comparison()
        
        print("\n🎉 HOÀN THÀNH TẠO BIỂU ĐỒ SO SÁNH!")
        print("=" * 60)
        print("📁 File đã được tạo:")
        print("   • Hinh_5_X_Comparison_Old_vs_New.png")
        print("\n✨ Biểu đồ so sánh cho thấy sự khác biệt giữa:")
        print("   • Phiên bản cũ: Bị cắt, thiếu thông tin, layout không tối ưu")
        print("   • Phiên bản mới: Hoàn chỉnh, đầy đủ thông tin, layout chuyên nghiệp")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
