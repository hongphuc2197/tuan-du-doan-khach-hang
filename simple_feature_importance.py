import pandas as pd
import matplotlib.pyplot as plt

print('📊 TẠO BIỂU ĐỒ FEATURE IMPORTANCE ĐƠN GIẢN')
print('=' * 50)

# Dữ liệu từ kết quả training
features = ['total_actions', 'unique_products', 'total_spending', 'avg_spending', 'age', 'income_encoded', 'education_encoded']

# Random Forest Feature Importance
rf_importance = [0.067877, 0.069348, 0.324712, 0.293655, 0.159855, 0.034851, 0.049702]

# Gradient Boosting Feature Importance  
gb_importance = [0.000516, 0.020839, 0.502674, 0.309984, 0.126699, 0.012385, 0.026904]

# Tạo biểu đồ đơn giản
fig, ax = plt.subplots(figsize=(12, 8))

# Vẽ biểu đồ Random Forest
x = range(len(features))
bars = ax.bar(x, rf_importance, color='skyblue', alpha=0.7, edgecolor='black')

ax.set_title('Random Forest - Feature Importance', fontsize=16, fontweight='bold')
ax.set_xlabel('Features', fontsize=12)
ax.set_ylabel('Importance Score', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(features, rotation=45, ha='right')

# Thêm giá trị lên cột
for bar, value in zip(bars, rf_importance):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
            f'{value:.3f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('rf_feature_importance.png', dpi=300, bbox_inches='tight')
print('✅ Đã lưu biểu đồ RF: rf_feature_importance.png')

# Tạo biểu đồ Gradient Boosting
fig2, ax2 = plt.subplots(figsize=(12, 8))

bars2 = ax2.bar(x, gb_importance, color='lightgreen', alpha=0.7, edgecolor='black')

ax2.set_title('Gradient Boosting - Feature Importance', fontsize=16, fontweight='bold')
ax2.set_xlabel('Features', fontsize=12)
ax2.set_ylabel('Importance Score', fontsize=12)
ax2.set_xticks(x)
ax2.set_xticklabels(features, rotation=45, ha='right')

# Thêm giá trị lên cột
for bar, value in zip(bars2, gb_importance):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
            f'{value:.3f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('gb_feature_importance.png', dpi=300, bbox_inches='tight')
print('✅ Đã lưu biểu đồ GB: gb_feature_importance.png')

# In kết quả phân tích
print('\n=== PHÂN TÍCH FEATURE IMPORTANCE ===')

print('\n🌲 RANDOM FOREST - Top Features:')
rf_df = pd.DataFrame({'feature': features, 'importance': rf_importance})
rf_df = rf_df.sort_values('importance', ascending=False)
for i, (_, row) in enumerate(rf_df.iterrows(), 1):
    print(f'{i}. {row["feature"]}: {row["importance"]:.3f}')

print('\n🚀 GRADIENT BOOSTING - Top Features:')
gb_df = pd.DataFrame({'feature': features, 'importance': gb_importance})
gb_df = gb_df.sort_values('importance', ascending=False)
for i, (_, row) in enumerate(gb_df.iterrows(), 1):
    print(f'{i}. {row["feature"]}: {row["importance"]:.3f}')

print('\n🎉 Hoàn thành tạo biểu đồ Feature Importance!')
