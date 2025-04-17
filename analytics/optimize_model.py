import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score
from sklearn.impute import SimpleImputer
import joblib
import warnings
warnings.filterwarnings('ignore')

# Đọc dữ liệu
df = pd.read_csv('marketing_campaign.csv', sep='\t')

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

# Định nghĩa các tham số cần tối ưu
param_grid = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 4, 5],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Tạo mô hình cơ sở
gb_model = GradientBoostingClassifier(random_state=42)

# Tìm kiếm tham số tối ưu
print("Bắt đầu tìm kiếm tham số tối ưu...")
grid_search = GridSearchCV(
    estimator=gb_model,
    param_grid=param_grid,
    cv=5,
    scoring='f1',
    n_jobs=-1,
    verbose=1
)

# Train mô hình với tham số tối ưu
grid_search.fit(X_train_scaled, y_train)

# In kết quả tối ưu
print("\n=== Kết quả tối ưu ===")
print("Tham số tốt nhất:", grid_search.best_params_)
print("F1-score tốt nhất:", grid_search.best_score_)

# Đánh giá mô hình tối ưu trên tập test
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test_scaled)

print("\n=== Đánh giá mô hình tối ưu trên tập test ===")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1-score:", f1_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Lưu mô hình tối ưu và scaler
joblib.dump(scaler, 'optimized_scaler.pkl')
joblib.dump(best_model, 'optimized_model.pkl')

print("\nMô hình tối ưu đã được lưu vào file 'optimized_model.pkl'") 