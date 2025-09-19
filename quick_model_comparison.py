import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score

print("🚀 SO SÁNH MÔ HÌNH DỰ ĐOÁN KHÁCH HÀNG TIỀM NĂNG")
print("=" * 60)

# Đọc và chuẩn bị dữ liệu
df = pd.read_csv('user_actions_students_576.csv')

# Tạo features
user_behavior = df.groupby('user_id').agg({
    'event_type': lambda x: 'purchase' in x.values,
    'product_id': 'nunique',
    'price': ['sum', 'mean'],
    'age': 'first',
    'income_level': 'first',
    'education': 'first'
})

user_behavior['total_actions'] = df.groupby('user_id')['event_type'].count()
user_behavior.columns = ['is_potential', 'unique_products', 'total_spending', 'avg_spending', 'age', 'income_level', 'education', 'total_actions']

# Chuẩn bị features
le_income = LabelEncoder()
le_education = LabelEncoder()
user_behavior['income_encoded'] = le_income.fit_transform(user_behavior['income_level'])
user_behavior['education_encoded'] = le_education.fit_transform(user_behavior['education'])

feature_columns = ['total_actions', 'unique_products', 'total_spending', 'avg_spending', 'age', 'income_encoded', 'education_encoded']
X = user_behavior[feature_columns]
y = user_behavior['is_potential']

print(f"Dataset: {len(X)} users, {y.sum()} potential customers ({y.mean()*100:.1f}%)")
print()

# Chia dữ liệu
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Chuẩn hóa
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Định nghĩa mô hình
models = {
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
    'Random Forest': RandomForestClassifier(random_state=42, n_estimators=50),
    'Gradient Boosting': GradientBoostingClassifier(random_state=42, n_estimators=50),
    'SVM': SVC(random_state=42, probability=True)
}

print("=== SO SÁNH CÁC MÔ HÌNH ===")
print(f'{"Model":<20} {"Accuracy":<10} {"Precision":<10} {"Recall":<10} {"F1-score":<10} {"CV Score":<12}')
print('-' * 80)

results = {}
for name, model in models.items():
    # Training
    if name == 'SVM':
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='accuracy')
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
    
    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cv_mean = cv_scores.mean()
    
    results[name] = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'cv_mean': cv_mean
    }
    
    print(f'{name:<20} {accuracy:<10.4f} {precision:<10.4f} {recall:<10.4f} {f1:<10.4f} {cv_mean:<12.4f}')

print("\n=== CHI TIẾT CHO TỪNG MÔ HÌNH ===")
for name, result in results.items():
    print(f"\n--- {name} ---")
    print(f"Accuracy: {result['accuracy']:.4f}")
    print(f"Precision: {result['precision']:.4f}")
    print(f"Recall: {result['recall']:.4f}")
    print(f"F1-score: {result['f1_score']:.4f}")
    print(f"CV Score: {result['cv_mean']:.4f}")

print(f"\n=== KẾT LUẬN ===")
best_accuracy = max(results.items(), key=lambda x: x[1]['accuracy'])
best_f1 = max(results.items(), key=lambda x: x[1]['f1_score'])
best_cv = max(results.items(), key=lambda x: x[1]['cv_mean'])

print(f"🥇 Accuracy cao nhất: {best_accuracy[0]} ({best_accuracy[1]['accuracy']:.4f})")
print(f"🥇 F1-score cao nhất: {best_f1[0]} ({best_f1[1]['f1_score']:.4f})")
print(f"🥇 CV Score cao nhất: {best_cv[0]} ({best_cv[1]['cv_mean']:.4f})")

