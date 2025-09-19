import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

print('🚀 TRAINING LOGISTIC REGRESSION TRÊN DATASET CỦA BẠN')
print('=' * 60)

# Bước 1: Đọc dataset
print('Bước 1: Đọc dataset...')
df = pd.read_csv('user_actions_students_576.csv')
print(f'✅ Dataset: {len(df)} records, {df["user_id"].nunique()} users')

# Bước 2: Tạo features
print('\nBước 2: Tạo features...')
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

print(f'✅ Features tạo xong: {len(user_behavior)} users')
print(f'✅ Khách hàng tiềm năng: {user_behavior["is_potential"].sum()}/{len(user_behavior)} ({user_behavior["is_potential"].mean()*100:.1f}%)')

# Bước 3: Encode categorical variables
print('\nBước 3: Encode categorical variables...')
le_income = LabelEncoder()
le_education = LabelEncoder()
user_behavior['income_encoded'] = le_income.fit_transform(user_behavior['income_level'])
user_behavior['education_encoded'] = le_education.fit_transform(user_behavior['education'])

print(f'✅ Income levels: {list(le_income.classes_)}')
print(f'✅ Education levels: {list(le_education.classes_)}')

# Bước 4: Chuẩn bị X và y
print('\nBước 4: Chuẩn bị dữ liệu...')
feature_columns = ['total_actions', 'unique_products', 'total_spending', 'avg_spending', 'age', 'income_encoded', 'education_encoded']
X = user_behavior[feature_columns]
y = user_behavior['is_potential']

print(f'✅ Features: {feature_columns}')
print(f'✅ Target distribution: {y.value_counts().to_dict()}')

# Bước 5: Train-test split
print('\nBước 5: Chia dữ liệu train/test...')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f'✅ Training set: {len(X_train)} users')
print(f'✅ Test set: {len(X_test)} users')

# Bước 6: Training Logistic Regression
print('\nBước 6: Training Logistic Regression...')
model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X_train, y_train)
print('✅ Training hoàn thành!')

# Bước 7: Dự đoán và đánh giá
print('\nBước 7: Dự đoán và đánh giá...')
y_pred = model.predict(X_test)

# Metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f'\n=== KẾT QUẢ LOGISTIC REGRESSION ===')
print(f'Accuracy: {accuracy:.4f} ({accuracy*100:.1f}%)')
print(f'Precision: {precision:.4f} ({precision*100:.1f}%)')
print(f'Recall: {recall:.4f} ({recall*100:.1f}%)')
print(f'F1-score: {f1:.4f} ({f1*100:.1f}%)')

print(f'\n=== CLASSIFICATION REPORT ===')
print(classification_report(y_test, y_pred))

# Feature importance
print(f'\n=== FEATURE IMPORTANCE ===')
feature_importance = pd.DataFrame({
    'feature': feature_columns,
    'coefficient': model.coef_[0]
}).sort_values('coefficient', key=abs, ascending=False)

print(feature_importance)

print(f'\n✅ Hoàn thành training Logistic Regression!')
