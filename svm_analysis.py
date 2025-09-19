import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt

print('🎯 PHÂN TÍCH CHI TIẾT MÔ HÌNH SVM')
print('=' * 50)

# Đọc dataset
df = pd.read_csv('user_actions_students_576.csv')
print(f'Dataset: {len(df)} records, {df["user_id"].nunique()} users')

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

# Chuẩn hóa dữ liệu cho SVM
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Training SVM
model = SVC(random_state=42, probability=True)
model.fit(X_train_scaled, y_train)

# Dự đoán
y_pred = model.predict(X_test_scaled)
y_proba = model.predict_proba(X_test_scaled)

# Metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f'\n=== KẾT QUẢ SVM ===')
print(f'Accuracy: {accuracy:.4f} ({accuracy*100:.1f}%)')
print(f'Precision: {precision:.4f} ({precision*100:.1f}%)')
print(f'Recall: {recall:.4f} ({recall*100:.1f}%)')
print(f'F1-score: {f1:.4f} ({f1*100:.1f}%)')

print(f'\n=== CLASSIFICATION REPORT ===')
print(classification_report(y_test, y_pred))

print(f'\n=== CONFUSION MATRIX ===')
cm = confusion_matrix(y_test, y_pred)
print('Confusion Matrix:')
print(f'True Negatives:  {cm[0,0]}')
print(f'False Positives: {cm[0,1]}')
print(f'False Negatives: {cm[1,0]}')
print(f'True Positives:  {cm[1,1]}')

print(f'\n=== SVM PARAMETERS ===')
print(f'Kernel: {model.kernel}')
print(f'C: {model.C}')
print(f'Gamma: {model.gamma}')
print(f'Number of support vectors: {model.n_support_}')
print(f'Total support vectors: {model.n_support_.sum()}')

# Phân tích chi tiết
print(f'\n=== PHÂN TÍCH CHI TIẾT SVM ===')
print(f'✅ SVM tìm được {cm[1,1]} khách hàng tiềm năng đúng trong {cm[1,1] + cm[1,0]} khách hàng thực sự có tiềm năng')
print(f'✅ SVM dự đoán đúng {cm[0,0]} khách hàng không tiềm năng trong {cm[0,0] + cm[0,1]} khách hàng thực sự không tiềm năng')
print(f'✅ Tổng cộng SVM dự đoán đúng {cm[0,0] + cm[1,1]} trong {len(y_test)} khách hàng test')

# Business impact
print(f'\n=== TÁC ĐỘNG KINH DOANH ===')
print(f'🎯 Khách hàng được dự đoán có tiềm năng: {cm[0,1] + cm[1,1]} người')
print(f'💰 Trong đó, {cm[1,1]} người thực sự có tiềm năng (hiệu quả: {cm[1,1]/(cm[0,1] + cm[1,1])*100:.1f}%)')
print(f'💸 Chi phí marketing cho {cm[0,1]} người không có tiềm năng (lãng phí: {cm[0,1]/(cm[0,1] + cm[1,1])*100:.1f}%)')
print(f'🚫 Bỏ sót {cm[1,0]} khách hàng tiềm năng (missed opportunity: {cm[1,0]/(cm[1,0] + cm[1,1])*100:.1f}%)')

print(f'\n✅ SVM là mô hình tốt nhất với F1-score {f1*100:.1f}%!')
