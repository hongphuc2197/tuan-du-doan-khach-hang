import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score
from sklearn.impute import SimpleImputer
import warnings
import os
warnings.filterwarnings('ignore')

# Đọc dữ liệu với đường dẫn tuyệt đối
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, '..', 'marketing_campaign.csv')
df = pd.read_csv(csv_path, sep='\t')

# Xử lý missing values
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
imputer = SimpleImputer(strategy='mean')
df[numeric_cols] = imputer.fit_transform(df[numeric_cols])

# Chọn các biến đặc trưng
features = ['Year_Birth', 'Income', 'Kidhome', 'Teenhome', 'Recency',
            'MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts',
            'MntSweetProducts', 'MntGoldProds', 'NumDealsPurchases',
            'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases',
            'NumWebVisitsMonth']

X = df[features]
y = df['Response']

# Chia dữ liệu thành tập train và test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Chuẩn hóa dữ liệu
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Định nghĩa các mô hình
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'SVM': SVC(probability=True, random_state=42)
}

# Train và đánh giá từng mô hình
results = []
for name, model in models.items():
    print(f"\n=== Training {name} ===")
    
    # Train mô hình
    model.fit(X_train_scaled, y_train)
    
    # Dự đoán trên tập test
    y_pred = model.predict(X_test_scaled)
    
    # Tính các chỉ số đánh giá
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
    cv_mean = cv_scores.mean()
    cv_std = cv_scores.std()
    
    # Lưu kết quả
    results.append({
        'Model': name,
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1-score': f1,
        'CV Mean': cv_mean,
        'CV Std': cv_std
    })
    
    # In kết quả chi tiết
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-score: {f1:.4f}")
    print(f"Cross-validation: {cv_mean:.4f} (+/- {cv_std:.4f})")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

# Chuyển kết quả thành DataFrame
results_df = pd.DataFrame(results)
print("\n=== Tổng hợp kết quả ===")
print(results_df)

# Lưu kết quả vào file
results_df.to_csv('model_results.csv', index=False)

# Lưu mô hình tốt nhất
best_model = models[results_df.loc[results_df['F1-score'].idxmax(), 'Model']]
print(f"\nMô hình tốt nhất: {best_model.__class__.__name__}")

# Lưu scaler và mô hình tốt nhất với đường dẫn tuyệt đối
import joblib
script_dir = os.path.dirname(os.path.abspath(__file__))
scaler_path = os.path.join(script_dir, '..', 'scaler.pkl')
model_path = os.path.join(script_dir, '..', 'best_model.pkl')
joblib.dump(scaler, scaler_path)
joblib.dump(best_model, model_path) 