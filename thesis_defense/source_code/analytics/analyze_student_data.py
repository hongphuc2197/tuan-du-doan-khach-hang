#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phân tích dữ liệu sinh viên từ user_actions_students_576.csv
và tạo các biểu đồ trực quan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, roc_curve, auc, classification_report
import joblib
import warnings
warnings.filterwarnings('ignore')

# Thiết lập style
plt.style.use('default')
sns.set_palette("husl")

print('=' * 70)
print('PHÂN TÍCH DỮ LIỆU SINH VIÊN')
print('=' * 70)

# Đọc dữ liệu
df = pd.read_csv('../user_actions_students_576.csv')
print(f'\nĐọc dữ liệu: {len(df)} records, {df["user_id"].nunique()} users')

# Tạo features từ dữ liệu
user_behavior = df.groupby('user_id').agg({
    'event_type': lambda x: 'purchase' in x.values,  # Target: có mua hàng không
    'product_id': 'nunique',  # Số sản phẩm khác nhau
    'price': ['sum', 'mean'],  # Tổng và trung bình chi tiêu
    'age': 'first',
    'income_level': 'first',
    'education': 'first'
})

user_behavior['total_actions'] = df.groupby('user_id')['event_type'].count()
user_behavior.columns = ['is_potential', 'unique_products', 'total_spending', 'avg_spending', 'age', 'income_level', 'education', 'total_actions']

print(f'Khách hàng tiềm năng: {user_behavior["is_potential"].sum()}/{len(user_behavior)} ({user_behavior["is_potential"].mean()*100:.1f}%)')

# 1. PHÂN TÍCH THỐNG KÊ CƠ BẢN
print('\n' + '=' * 70)
print('1. THỐNG KÊ CƠ BẢN')
print('=' * 70)
print(user_behavior[['age', 'total_spending', 'avg_spending', 'total_actions', 'unique_products']].describe().round(2))

# 2. PHÂN TÍCH THEO ĐỘ TUỔI
print('\n' + '=' * 70)
print('2. PHÂN TÍCH THEO ĐỘ TUỔI')
print('=' * 70)
age_stats = user_behavior.groupby('age').agg({
    'is_potential': ['count', 'sum', 'mean']
}).round(3)
print(age_stats)

# 3. PHÂN TÍCH THEO TRÌNH ĐỘ HỌC VẤN
print('\n' + '=' * 70)
print('3. PHÂN TÍCH THEO TRÌNH ĐỘ HỌC VẤN')
print('=' * 70)
education_stats = user_behavior.groupby('education').agg({
    'is_potential': ['count', 'sum', 'mean'],
    'total_spending': 'mean',
    'avg_spending': 'mean'
}).round(2)
print(education_stats)

# 4. PHÂN TÍCH THEO MỨC THU NHẬP
print('\n' + '=' * 70)
print('4. PHÂN TÍCH THEO MỨC THU NHẬP')
print('=' * 70)
income_stats = user_behavior.groupby('income_level').agg({
    'is_potential': ['count', 'sum', 'mean'],
    'total_spending': 'mean',
    'avg_spending': 'mean'
}).round(2)
print(income_stats)

# Encode categorical variables
le_income = LabelEncoder()
le_education = LabelEncoder()
user_behavior['income_encoded'] = le_income.fit_transform(user_behavior['income_level'])
user_behavior['education_encoded'] = le_education.fit_transform(user_behavior['education'])

# Features
feature_columns = ['total_actions', 'unique_products', 'total_spending', 'avg_spending', 'age', 'income_encoded', 'education_encoded']
X = user_behavior[feature_columns]
y = user_behavior['is_potential']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f'\nTraining set: {len(X_train)} users')
print(f'Test set: {len(X_test)} users')

# 5. TRAINING VÀ ĐÁNH GIÁ MÔ HÌNH
print('\n' + '=' * 70)
print('5. TRAINING VÀ ĐÁNH GIÁ CÁC MÔ HÌNH')
print('=' * 70)

models = {
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
    'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100),
    'Gradient Boosting': GradientBoostingClassifier(random_state=42, n_estimators=100),
    'SVM': SVC(random_state=42, probability=True)
}

results = {}
y_preds = {}
y_probas = {}

for name, model in models.items():
    print(f'\nTraining {name}...')
    
    # Training
    if name == 'SVM':
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        y_proba = model.predict_proba(X_test_scaled)[:, 1]
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]
    
    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    results[name] = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'model': model
    }
    
    y_preds[name] = y_pred
    y_probas[name] = y_proba
    
    print(f'Accuracy: {accuracy:.4f}')
    print(f'Precision: {precision:.4f}')
    print(f'Recall: {recall:.4f}')
    print(f'F1-score: {f1:.4f}')

# Tìm mô hình tốt nhất
best_model_name = max(results.keys(), key=lambda x: results[x]['f1_score'])
print(f'\n🏆 MÔ HÌNH TỐT NHẤT: {best_model_name}')
print(f'   F1-score: {results[best_model_name]["f1_score"]:.4f}')
print(f'   Accuracy: {results[best_model_name]["accuracy"]:.4f}')

# Lưu mô hình tốt nhất
best_model = results[best_model_name]['model']
joblib.dump(best_model, 'best_student_model.pkl')
print(f'\n✅ Đã lưu mô hình tốt nhất: best_student_model.pkl')

# 6. TẠO CÁC BIỂU ĐỒ
print('\n' + '=' * 70)
print('6. TẠO CÁC BIỂU ĐỒ TRỰC QUAN')
print('=' * 70)

# 6.1. Biểu đồ phân phối độ tuổi
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Phân Tích Dữ Liệu Sinh Viên - Khách Hàng Tiềm Năng', fontsize=16, fontweight='bold')

# Age distribution
axes[0, 0].hist([user_behavior[user_behavior['is_potential'] == True]['age'],
                 user_behavior[user_behavior['is_potential'] == False]['age']],
                bins=20, label=['Tiềm năng', 'Không tiềm năng'], alpha=0.7)
axes[0, 0].set_xlabel('Tuổi')
axes[0, 0].set_ylabel('Số lượng')
axes[0, 0].set_title('Phân phối theo độ tuổi')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Spending distribution
axes[0, 1].hist([user_behavior[user_behavior['is_potential'] == True]['total_spending'],
                 user_behavior[user_behavior['is_potential'] == False]['total_spending']],
                bins=20, label=['Tiềm năng', 'Không tiềm năng'], alpha=0.7)
axes[0, 1].set_xlabel('Tổng chi tiêu')
axes[0, 1].set_ylabel('Số lượng')
axes[0, 1].set_title('Phân phối theo chi tiêu')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Education vs Potential
education_pivot = user_behavior.groupby(['education', 'is_potential']).size().unstack(fill_value=0)
education_pivot.plot(kind='bar', ax=axes[1, 0], alpha=0.7)
axes[1, 0].set_xlabel('Trình độ học vấn')
axes[1, 0].set_ylabel('Số lượng')
axes[1, 0].set_title('Phân phối theo trình độ học vấn')
axes[1, 0].legend(['Không tiềm năng', 'Tiềm năng'])
axes[1, 0].tick_params(axis='x', rotation=45)
axes[1, 0].grid(True, alpha=0.3)

# Income level vs Potential
income_pivot = user_behavior.groupby(['income_level', 'is_potential']).size().unstack(fill_value=0)
income_pivot.plot(kind='bar', ax=axes[1, 1], alpha=0.7)
axes[1, 1].set_xlabel('Mức thu nhập')
axes[1, 1].set_ylabel('Số lượng')
axes[1, 1].set_title('Phân phối theo thu nhập')
axes[1, 1].legend(['Không tiềm năng', 'Tiềm năng'])
axes[1, 1].tick_params(axis='x', rotation=45)
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('eda_plots.png', dpi=300, bbox_inches='tight')
print('✅ Đã lưu: eda_plots.png')

# 6.2. Correlation matrix
plt.figure(figsize=(10, 8))
corr_data = user_behavior[['is_potential', 'age', 'total_spending', 'avg_spending', 'total_actions', 'unique_products']].astype(float)
correlation = corr_data.corr()
sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Ma Trận Tương Quan Giữa Các Biến', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
print('✅ Đã lưu: correlation_matrix.png')

# 6.3. Model comparison
plt.figure(figsize=(12, 6))

# Plot model performance
metrics_df = pd.DataFrame(results).T
metrics_df = metrics_df[['accuracy', 'precision', 'recall', 'f1_score']]

x = np.arange(len(metrics_df.index))
width = 0.2

plt.bar(x - 1.5*width, metrics_df['accuracy'], width, label='Accuracy', alpha=0.8)
plt.bar(x - 0.5*width, metrics_df['precision'], width, label='Precision', alpha=0.8)
plt.bar(x + 0.5*width, metrics_df['recall'], width, label='Recall', alpha=0.8)
plt.bar(x + 1.5*width, metrics_df['f1_score'], width, label='F1-score', alpha=0.8)

plt.xlabel('Mô hình', fontsize=12, fontweight='bold')
plt.ylabel('Score', fontsize=12, fontweight='bold')
plt.title('So Sánh Hiệu Suất Các Mô Hình ML', fontsize=14, fontweight='bold')
plt.xticks(x, metrics_df.index, rotation=45, ha='right')
plt.legend()
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('model_comparison.png', dpi=300, bbox_inches='tight')
print('✅ Đã lưu: model_comparison.png')

# 6.4. Feature importance (cho Random Forest)
if 'Random Forest' in results:
    plt.figure(figsize=(10, 6))
    rf_model = results['Random Forest']['model']
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    plt.barh(range(len(feature_importance)), feature_importance['importance'], alpha=0.7)
    plt.yticks(range(len(feature_importance)), feature_importance['feature'])
    plt.xlabel('Importance', fontsize=12, fontweight='bold')
    plt.ylabel('Feature', fontsize=12, fontweight='bold')
    plt.title('Feature Importance - Random Forest', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
    print('✅ Đã lưu: feature_importance.png')
    
    print('\n📊 Feature Importance:')
    print(feature_importance.to_string(index=False))

# 6.5. Confusion Matrix cho mô hình tốt nhất
plt.figure(figsize=(8, 6))
cm = confusion_matrix(y_test, y_preds[best_model_name])
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Không tiềm năng', 'Tiềm năng'],
            yticklabels=['Không tiềm năng', 'Tiềm năng'])
plt.title(f'Confusion Matrix - {best_model_name}', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Dự đoán', fontsize=12, fontweight='bold')
plt.ylabel('Thực tế', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
print('✅ Đã lưu: confusion_matrix.png')

# 7. LƯU KẾT QUẢ
print('\n' + '=' * 70)
print('7. LƯU KẾT QUẢ')
print('=' * 70)

# Lưu kết quả mô hình
results_df = pd.DataFrame(results).T
results_df.to_csv('model_evaluation_results.csv')
print('✅ Đã lưu: model_evaluation_results.csv')

# Lưu báo cáo chi tiết
with open('model_evaluation_report.txt', 'w', encoding='utf-8') as f:
    f.write('=' * 70 + '\n')
    f.write('BÁO CÁO PHÂN TÍCH DỮ LIỆU SINH VIÊN\n')
    f.write('=' * 70 + '\n\n')
    
    f.write(f'Dataset: {len(df)} records, {df["user_id"].nunique()} users\n')
    f.write(f'Khách hàng tiềm năng: {user_behavior["is_potential"].sum()}/{len(user_behavior)} ({user_behavior["is_potential"].mean()*100:.1f}%)\n\n')
    
    f.write('THỐNG KÊ CƠ BẢN:\n')
    f.write(str(user_behavior[['age', 'total_spending', 'avg_spending', 'total_actions', 'unique_products']].describe().round(2)) + '\n\n')
    
    f.write('KẾT QUẢ MÔ HÌNH:\n')
    f.write(results_df.to_string() + '\n\n')
    
    f.write(f'MÔ HÌNH TỐT NHẤT: {best_model_name}\n')
    f.write(f'F1-score: {results[best_model_name]["f1_score"]:.4f}\n')
    f.write(f'Accuracy: {results[best_model_name]["accuracy"]:.4f}\n')
    
print('✅ Đã lưu: model_evaluation_report.txt')

print('\n' + '=' * 70)
print('HOÀN THÀNH PHÂN TÍCH!')
print('=' * 70)
print('\n📁 Các file đã được tạo:')
print('   • eda_plots.png - Phân tích dữ liệu khám phá')
print('   • correlation_matrix.png - Ma trận tương quan')
print('   • model_comparison.png - So sánh các mô hình')
print('   • feature_importance.png - Tầm quan trọng của features')
print('   • confusion_matrix.png - Ma trận nhầm lẫn')
print('   • model_evaluation_results.csv - Kết quả đánh giá')
print('   • model_evaluation_report.txt - Báo cáo chi tiết')
print('   • best_student_model.pkl - Mô hình tốt nhất')
print(f'\n🏆 Mô hình tốt nhất: {best_model_name} (F1-score: {results[best_model_name]["f1_score"]:.4f})')

