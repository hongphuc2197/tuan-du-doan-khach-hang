import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

print('🖼️ TẠO HÌNH ẢNH PNG')
print('=' * 30)

# Tạo hình 1: So sánh các mô hình
fig1, ax1 = plt.subplots(figsize=(12, 8))

models = ['Logistic Regression', 'Random Forest', 'Gradient Boosting', 'SVM']
accuracy = [66.4, 67.2, 66.4, 69.8]
f1_scores = [76.4, 73.6, 75.8, 78.8]

x = np.arange(len(models))
width = 0.35

bars1 = ax1.bar(x - width/2, accuracy, width, label='Accuracy (%)', color='skyblue', alpha=0.8)
bars2 = ax1.bar(x + width/2, f1_scores, width, label='F1-Score (%)', color='lightgreen', alpha=0.8)

ax1.set_xlabel('Models', fontsize=12, fontweight='bold')
ax1.set_ylabel('Performance (%)', fontsize=12, fontweight='bold')
ax1.set_title('So sánh hiệu suất các mô hình', fontsize=16, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(models, rotation=45, ha='right')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Thêm giá trị lên cột
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('model_comparison.png', dpi=300, bbox_inches='tight')
print('✅ Đã tạo: model_comparison.png')

# Tạo hình 2: SVM Performance
fig2, ax2 = plt.subplots(figsize=(10, 6))

metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
svm_values = [69.8, 69.1, 91.5, 78.8]
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']

bars = ax2.bar(metrics, svm_values, color=colors, alpha=0.8, edgecolor='black')

ax2.set_ylabel('Performance (%)', fontsize=12, fontweight='bold')
ax2.set_title('SVM Model Performance', fontsize=16, fontweight='bold')
ax2.set_ylim(0, 100)

# Thêm giá trị lên cột
for bar, value in zip(bars, svm_values):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
            f'{value:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=12)

plt.tight_layout()
plt.savefig('svm_performance.png', dpi=300, bbox_inches='tight')
print('✅ Đã tạo: svm_performance.png')

# Tạo hình 3: Dataset Overview
fig3, ax3 = plt.subplots(figsize=(12, 8))

# Dữ liệu dataset
categories = ['Total Records', 'Users', 'View Events', 'Purchase Events']
values = [1813, 576, 1274, 539]
colors = ['#FF9FF3', '#54A0FF', '#5F27CD', '#00D2D3']

bars = ax3.bar(categories, values, color=colors, alpha=0.8, edgecolor='black')

ax3.set_ylabel('Count', fontsize=12, fontweight='bold')
ax3.set_title('Dataset Overview', fontsize=16, fontweight='bold')

# Thêm giá trị lên cột
for bar, value in zip(bars, values):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height + 20,
            f'{value:,}', ha='center', va='bottom', fontweight='bold', fontsize=11)

plt.tight_layout()
plt.savefig('dataset_overview.png', dpi=300, bbox_inches='tight')
print('✅ Đã tạo: dataset_overview.png')

# Tạo hình 4: Feature Importance cho SVM
fig4, ax4 = plt.subplots(figsize=(12, 8))

# Vì SVM không có feature importance trực tiếp, ta dùng kết quả từ Random Forest
features = ['total_spending', 'avg_spending', 'age', 'unique_products', 'total_actions', 'education', 'income']
importance = [32.5, 29.4, 16.0, 6.9, 6.8, 5.0, 3.5]
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']

bars = ax4.barh(features, importance, color=colors, alpha=0.8, edgecolor='black')

ax4.set_xlabel('Importance (%)', fontsize=12, fontweight='bold')
ax4.set_title('Feature Importance (SVM sử dụng tất cả features)', fontsize=16, fontweight='bold')

# Thêm giá trị lên cột
for bar, value in zip(bars, importance):
    width = bar.get_width()
    ax4.text(width + 0.5, bar.get_y() + bar.get_height()/2,
            f'{value:.1f}%', ha='left', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
print('✅ Đã tạo: feature_importance.png')

print('\n🎉 Đã tạo xong 4 hình ảnh PNG:')
print('1. model_comparison.png - So sánh các mô hình')
print('2. svm_performance.png - Hiệu suất SVM')
print('3. dataset_overview.png - Tổng quan dataset')
print('4. feature_importance.png - Tầm quan trọng features')
