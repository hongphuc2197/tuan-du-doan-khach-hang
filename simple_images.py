import matplotlib.pyplot as plt
import numpy as np

print('Creating PNG images...')

# Tạo hình 1: Model Comparison
plt.figure(figsize=(10, 6))
models = ['Logistic\nRegression', 'Random\nForest', 'Gradient\nBoosting', 'SVM']
accuracy = [66.4, 67.2, 66.4, 69.8]

bars = plt.bar(models, accuracy, color=['lightblue', 'lightgreen', 'orange', 'red'], alpha=0.7)
plt.title('Model Accuracy Comparison', fontsize=14, fontweight='bold')
plt.ylabel('Accuracy (%)', fontsize=12)
plt.ylim(0, 80)

for bar, value in zip(bars, accuracy):
    plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
             f'{value}%', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('model_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print('✅ Created: model_comparison.png')

# Tạo hình 2: SVM Performance
plt.figure(figsize=(8, 6))
metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
values = [69.8, 69.1, 91.5, 78.8]
colors = ['red', 'blue', 'green', 'purple']

bars = plt.bar(metrics, values, color=colors, alpha=0.7)
plt.title('SVM Model Performance', fontsize=14, fontweight='bold')
plt.ylabel('Performance (%)', fontsize=12)
plt.ylim(0, 100)

for bar, value in zip(bars, values):
    plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
             f'{value}%', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('svm_performance.png', dpi=300, bbox_inches='tight')
plt.close()
print('✅ Created: svm_performance.png')

print('Done!')
