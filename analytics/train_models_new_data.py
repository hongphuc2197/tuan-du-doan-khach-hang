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
warnings.filterwarnings('ignore')

# Đọc dữ liệu mới
df = pd.read_csv('../marketing_campaign_converted.csv', sep='\t')

print(f"Dữ liệu có {len(df)} dòng và {len(df.columns)} cột")
print("Các cột trong dữ liệu:")
for i, col in enumerate(df.columns):
    print(f"{i+1}. {col}")

# Hiển thị thống kê cơ bản
print("\n=== THỐNG KÊ DỮ LIỆU ===")
print(f"Số lượng khách hàng: {len(df)}")
print(f"Số khách hàng có Response = 1: {df['Response'].sum()}")
print(f"Tỷ lệ khách hàng tiềm năng: {df['Response'].mean():.2%}")

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

print(f"\nSố lượng features: {len(features)}")
print(f"Features: {features}")

# Chia dữ liệu thành tập train và test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"\nKích thước tập train: {X_train.shape}")
print(f"Kích thước tập test: {X_test.shape}")

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
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
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
    print(classification_report(y_test, y_pred, zero_division=0))

# Chuyển kết quả thành DataFrame
results_df = pd.DataFrame(results)
print("\n=== Tổng hợp kết quả ===")
print(results_df)

# Lưu kết quả vào file
results_df.to_csv('model_results_new_data.csv', index=False)

# Lưu mô hình tốt nhất
best_model = models[results_df.loc[results_df['F1-score'].idxmax(), 'Model']]
print(f"\nMô hình tốt nhất: {best_model.__class__.__name__}")

# Lưu scaler và mô hình tốt nhất
import joblib
joblib.dump(scaler, 'optimized_scaler_new.pkl')
joblib.dump(best_model, 'optimized_model_new.pkl')

print("\nĐã lưu mô hình và scaler mới!")
print("Files được lưu:")
print("- optimized_scaler_new.pkl")
print("- optimized_model_new.pkl")
print("- model_results_new_data.csv")