import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

# Đọc dữ liệu
df = pd.read_csv('marketing_campaign.csv', sep='\t')

# Hiển thị thông tin cơ bản về dữ liệu
print("=== Thông tin cơ bản về dữ liệu ===")
print(f"Số dòng: {df.shape[0]}")
print(f"Số cột: {df.shape[1]}")
print("\nThông tin các cột:")
print(df.info())
print("\nThống kê mô tả:")
print(df.describe())

# Kiểm tra missing values
print("\n=== Kiểm tra missing values ===")
missing_values = df.isnull().sum()
print(missing_values[missing_values > 0])

# Xử lý missing values
# Thay thế missing values bằng giá trị trung bình cho các cột số
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
imputer = SimpleImputer(strategy='mean')
df[numeric_cols] = imputer.fit_transform(df[numeric_cols])

# Phân tích biến mục tiêu
print("\n=== Phân tích biến mục tiêu (Response) ===")
print(df['Response'].value_counts(normalize=True))

# Visualize phân phối của một số biến quan trọng
plt.figure(figsize=(15, 10))

# Phân phối thu nhập
plt.subplot(2, 2, 1)
sns.histplot(data=df, x='Income', bins=30)
plt.title('Phân phối thu nhập')

# Phân phối tuổi
plt.subplot(2, 2, 2)
df['Age'] = 2024 - df['Year_Birth']  # Tính tuổi
sns.histplot(data=df, x='Age', bins=30)
plt.title('Phân phối tuổi')

# Tương quan giữa Response và Education
plt.subplot(2, 2, 3)
sns.countplot(data=df, x='Education', hue='Response')
plt.title('Tương quan giữa Education và Response')
plt.xticks(rotation=45)

# Tương quan giữa Response và Marital_Status
plt.subplot(2, 2, 4)
sns.countplot(data=df, x='Marital_Status', hue='Response')
plt.title('Tương quan giữa Marital_Status và Response')
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('eda_plots.png')
plt.close()

# Phân tích tương quan giữa các biến số
correlation_matrix = df[numeric_cols].corr()

plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Ma trận tương quan')
plt.tight_layout()
plt.savefig('correlation_matrix.png')
plt.close()

# Tiền xử lý dữ liệu cho mô hình
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

# Xây dựng mô hình Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)

# Đánh giá mô hình
y_pred = rf_model.predict(X_test_scaled)
print("\n=== Đánh giá mô hình ===")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Hiển thị feature importance
feature_importance = pd.DataFrame({
    'Feature': features,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(data=feature_importance, x='Importance', y='Feature')
plt.title('Feature Importance')
plt.tight_layout()
plt.savefig('feature_importance.png')
plt.close()

print("\n=== Feature Importance ===")
print(feature_importance) 