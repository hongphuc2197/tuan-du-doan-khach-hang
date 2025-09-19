import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

print('🚀 TRAINING THỰC TẾ TRÊN DATASET CỦA BẠN')
print('=' * 50)

# Đọc dataset thực tế
df = pd.read_csv('user_actions_students_576.csv')
print(f'Dataset thực tế: {len(df)} records, {df["user_id"].nunique()} users')

# Tạo features từ dữ liệu thực tế
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

print(f'Training set: {len(X_train)} users')
print(f'Test set: {len(X_test)} users')
print()

# Models
models = {
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
    'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100),
    'Gradient Boosting': GradientBoostingClassifier(random_state=42, n_estimators=100),
    'SVM': SVC(random_state=42, probability=True)
}

print('=== KẾT QUẢ THỰC TẾ ===')
print(f'{"Model":<20} {"Accuracy":<10} {"Precision":<10} {"Recall":<10} {"F1-score":<10}')
print('-' * 60)

results = {}
for name, model in models.items():
    print(f'\n--- Training {name} ---')
    
    # Training
    if name == 'SVM':
        # Chuẩn hóa cho SVM
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
    
    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    results[name] = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'y_pred': y_pred
    }
    
    print(f'{name:<20} {accuracy:<10.4f} {precision:<10.4f} {recall:<10.4f} {f1:<10.4f}')

print('\n=== CHI TIẾT KẾT QUẢ ===')
for name, result in results.items():
    print(f'\n{name}:')
    print(f'  Accuracy: {result["accuracy"]:.4f} ({result["accuracy"]*100:.1f}%)')
    print(f'  Precision: {result["precision"]:.4f} ({result["precision"]*100:.1f}%)')
    print(f'  Recall: {result["recall"]:.4f} ({result["recall"]*100:.1f}%)')
    print(f'  F1-score: {result["f1_score"]:.4f} ({result["f1_score"]*100:.1f}%)')

# Tìm mô hình tốt nhất
best_accuracy = max(results.items(), key=lambda x: x[1]['accuracy'])
best_f1 = max(results.items(), key=lambda x: x[1]['f1_score'])

print(f'\n🏆 MÔ HÌNH TỐT NHẤT:')
print(f'🥇 Accuracy cao nhất: {best_accuracy[0]} ({best_accuracy[1]["accuracy"]*100:.1f}%)')
print(f'🥇 F1-score cao nhất: {best_f1[0]} ({best_f1[1]["f1_score"]*100:.1f}%)')

print('\n✅ Đây là kết quả THỰC TẾ từ dataset của bạn!')
