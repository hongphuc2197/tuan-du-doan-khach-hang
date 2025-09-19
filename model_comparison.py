import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_dataset():
    """Phân tích dataset để hiểu features"""
    df = pd.read_csv('user_actions_students_576.csv')
    
    print('=== PHÂN TÍCH DATASET CHO MÔ HÌNH DỰ ĐOÁN ===')
    print(f'Dataset: {len(df)} records, {df["user_id"].nunique()} users')
    print()
    
    print('=== FEATURES CÓ THỂ SỬ DỤNG ===')
    print('1. DEMOGRAPHIC:')
    print(f'- Age: {df["age"].min()}-{df["age"].max()} tuổi')
    print(f'- Income: {df["income_level"].value_counts().to_dict()}')
    print()
    
    print('2. BEHAVIORAL:')
    print(f'- Event types: {df["event_type"].value_counts().to_dict()}')
    print(f'- Price range: ${df["price"].min()}-${df["price"].max()}')
    print()
    
    # Tạo target variable: khách hàng tiềm năng (có mua hàng)
    user_behavior = df.groupby('user_id').agg({
        'event_type': lambda x: 'purchase' in x.values,  # Có mua hàng không
        'product_id': 'nunique',  # Số sản phẩm khác nhau
        'price': ['sum', 'mean'],  # Tổng và trung bình chi tiêu
        'age': 'first',
        'income_level': 'first',
        'education': 'first'
    })
    
    # Thêm cột total_actions riêng
    user_behavior['total_actions'] = df.groupby('user_id')['event_type'].count()
    
    user_behavior.columns = ['is_potential', 'unique_products', 'total_spending', 'avg_spending', 'age', 'income_level', 'education', 'total_actions']
    
    print('=== TARGET VARIABLE (KHÁCH HÀNG TIỀM NĂNG) ===')
    potential_count = user_behavior['is_potential'].sum()
    print(f'- Khách hàng tiềm năng (có mua): {potential_count}/{len(user_behavior)} ({potential_count/len(user_behavior)*100:.1f}%)')
    print(f'- Khách hàng chỉ xem: {len(user_behavior) - potential_count}/{len(user_behavior)} ({(len(user_behavior) - potential_count)/len(user_behavior)*100:.1f}%)')
    
    return user_behavior

def prepare_data(user_behavior):
    """Chuẩn bị dữ liệu cho training"""
    print('\n=== CHUẨN BỊ DỮ LIỆU ===')
    
    # Chọn features
    feature_columns = ['total_actions', 'unique_products', 'total_spending', 'avg_spending', 'age']
    
    # Encode categorical variables
    le_income = LabelEncoder()
    le_education = LabelEncoder()
    
    user_behavior['income_encoded'] = le_income.fit_transform(user_behavior['income_level'])
    user_behavior['education_encoded'] = le_education.fit_transform(user_behavior['education'])
    
    feature_columns.extend(['income_encoded', 'education_encoded'])
    
    X = user_behavior[feature_columns]
    y = user_behavior['is_potential']
    
    print(f'Features: {feature_columns}')
    print(f'Target distribution: {y.value_counts().to_dict()}')
    
    return X, y, feature_columns

def train_and_compare_models(X, y):
    """So sánh các mô hình"""
    print('\n=== SO SÁNH CÁC MÔ HÌNH ===')
    
    # Chia dữ liệu
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Chuẩn hóa dữ liệu
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Định nghĩa các mô hình
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100),
        'Gradient Boosting': GradientBoostingClassifier(random_state=42, n_estimators=100),
        'SVM': SVC(random_state=42, probability=True)
    }
    
    results = {}
    
    for name, model in models.items():
        print(f'\n--- {name} ---')
        
        # Training
        if name == 'SVM':
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            y_proba = model.predict_proba(X_test_scaled)[:, 1]
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_proba = model.predict_proba(X_test)[:, 1]
        
        # Cross-validation
        if name == 'SVM':
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='accuracy')
        else:
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'y_pred': y_pred,
            'y_proba': y_proba
        }
        
        print(f'Accuracy: {accuracy:.4f}')
        print(f'Precision: {precision:.4f}')
        print(f'Recall: {recall:.4f}')
        print(f'F1-score: {f1:.4f}')
        print(f'CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})')
        
        # Classification Report
        print('\nClassification Report:')
        print(classification_report(y_test, y_pred))
    
    return results, X_test, y_test

def main():
    """Hàm chính"""
    print("🚀 BẮT ĐẦU SO SÁNH MÔ HÌNH DỰ ĐOÁN KHÁCH HÀNG TIỀM NĂNG")
    print("=" * 60)
    
    # 1. Phân tích dataset
    user_behavior = analyze_dataset()
    
    # 2. Chuẩn bị dữ liệu
    X, y, feature_columns = prepare_data(user_behavior)
    
    # 3. So sánh mô hình
    results, X_test, y_test = train_and_compare_models(X, y)
    
    # 4. Kết quả cuối cùng
    print('\n=== KẾT QUẢ SO SÁNH CHI TIẾT ===')
    print(f'{"Model":<20} {"Accuracy":<10} {"Precision":<10} {"Recall":<10} {"F1-score":<10} {"CV Score":<12} {"Stability":<10}')
    print('-' * 95)
    
    best_model = None
    best_score = 0
    
    for name, result in results.items():
        print(f'{name:<20} {result["accuracy"]:<10.4f} {result["precision"]:<10.4f} {result["recall"]:<10.4f} {result["f1_score"]:<10.4f} {result["cv_mean"]:<12.4f} {result["cv_std"]:<10.4f}')
        if result['cv_mean'] > best_score:
            best_score = result['cv_mean']
            best_model = name
    
    print(f'\n🏆 MÔ HÌNH TỐT NHẤT: {best_model}')
    print(f'📊 CV Score: {best_score:.4f}')
    
    # Thêm phân tích chi tiết
    print(f'\n=== PHÂN TÍCH THEO METRIC ===')
    
    # Tìm mô hình tốt nhất cho từng metric
    metrics = ['accuracy', 'precision', 'recall', 'f1_score']
    for metric in metrics:
        best_for_metric = max(results.items(), key=lambda x: x[1][metric])
        print(f'🥇 {metric.upper()}: {best_for_metric[0]} ({best_for_metric[1][metric]:.4f})')
    
    print(f'\n🥇 STABILITY (CV std): {min(results.items(), key=lambda x: x[1]["cv_std"])[0]} ({min(results.items(), key=lambda x: x[1]["cv_std"])[1]["cv_std"]:.4f})')
    
    return results, best_model

if __name__ == "__main__":
    results, best_model = main()
