import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import warnings
warnings.filterwarnings('ignore')

def train_student_model():
    """
    Training mô hình với dataset sinh viên 627 users
    """
    print("=== TRAINING MÔ HÌNH VỚI DATASET SINH VIÊN ===")
    
    # Đọc dữ liệu
    print("Đang đọc dữ liệu...")
    df = pd.read_csv('../marketing_campaign_students_627.csv', sep='\t')
    
    print(f"Dataset có {len(df)} users và {len(df.columns)} features")
    print(f"Số khách hàng tiềm năng: {(df['Response'] == 1).sum()}/{len(df)} ({(df['Response'] == 1).mean()*100:.1f}%)")
    
    # Thống kê độ tuổi
    ages = 2024 - df['Year_Birth']
    print(f"\nThống kê độ tuổi sinh viên:")
    print(f"Tuổi trung bình: {ages.mean():.1f}")
    print(f"Tuổi tối thiểu: {ages.min()}")
    print(f"Tuổi tối đa: {ages.max()}")
    
    # Phân khúc độ tuổi
    age_18_20 = ((ages >= 18) & (ages <= 20)).sum()
    age_21_23 = ((ages >= 21) & (ages <= 23)).sum()
    age_24_25 = ((ages >= 24) & (ages <= 25)).sum()
    
    print(f"18-20 tuổi: {age_18_20} ({age_18_20/len(df)*100:.1f}%)")
    print(f"21-23 tuổi: {age_21_23} ({age_21_23/len(df)*100:.1f}%)")
    print(f"24-25 tuổi: {age_24_25} ({age_24_25/len(df)*100:.1f}%)")
    
    # Chuẩn bị dữ liệu
    print("\nChuẩn bị dữ liệu...")
    
    # Chọn features
    feature_columns = [
        'Year_Birth', 'Income', 'Kidhome', 'Teenhome', 'Recency',
        'MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 
        'MntSweetProducts', 'MntGoldProds', 'NumDealsPurchases',
        'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases', 
        'NumWebVisitsMonth'
    ]
    
    # Encode categorical variables
    df_encoded = df.copy()
    df_encoded['Education'] = df_encoded['Education'].map({
        'Basic': 0, 'Graduation': 1, 'Master': 2, 'PhD': 3, '2n Cycle': 4
    })
    df_encoded['Marital_Status'] = df_encoded['Marital_Status'].map({
        'Single': 0, 'Married': 1, 'Divorced': 2, 'Together': 3, 'Widow': 4
    })
    
    feature_columns.extend(['Education', 'Marital_Status'])
    
    X = df_encoded[feature_columns]
    y = df_encoded['Response']
    
    print(f"Số features: {X.shape[1]}")
    print(f"Features: {feature_columns}")
    
    # Chia dữ liệu
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print(f"\nDữ liệu training: {X_train.shape[0]} samples")
    print(f"Dữ liệu test: {X_test.shape[0]} samples")
    
    # Chuẩn hóa dữ liệu
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Training các mô hình
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100),
        'Gradient Boosting': GradientBoostingClassifier(random_state=42),
        'SVM': SVC(random_state=42, probability=True)
    }
    
    results = {}
    
    print("\n=== TRAINING CÁC MÔ HÌNH ===")
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        
        # Training
        if name == 'SVM':
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            y_pred_proba = model.predict_proba(X_test_scaled)
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)
        
        # Đánh giá
        accuracy = accuracy_score(y_test, y_pred)
        cv_scores = cross_val_score(model, X_train if name != 'SVM' else X_train_scaled, y_train, cv=5)
        
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }
        
        print(f"Accuracy: {accuracy:.4f}")
        print(f"CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    # Chọn mô hình tốt nhất
    best_model_name = max(results.keys(), key=lambda x: results[x]['cv_mean'])
    best_model = results[best_model_name]['model']
    
    print(f"\n=== MÔ HÌNH TỐT NHẤT: {best_model_name} ===")
    print(f"Accuracy: {results[best_model_name]['accuracy']:.4f}")
    print(f"CV Score: {results[best_model_name]['cv_mean']:.4f} (+/- {results[best_model_name]['cv_std'] * 2:.4f})")
    
    # Lưu mô hình và scaler
    scaler_filename = 'student_scaler_627.pkl'
    model_filename = 'student_model_627.pkl'
    
    joblib.dump(scaler, scaler_filename)
    joblib.dump(best_model, model_filename)
    
    print(f"\nĐã lưu scaler vào: {scaler_filename}")
    print(f"Đã lưu mô hình vào: {model_filename}")
    
    # Tạo báo cáo chi tiết
    print(f"\n=== BÁO CÁO CHI TIẾT ===")
    print(f"Dataset: {len(df)} sinh viên")
    print(f"Độ tuổi: {ages.min()}-{ages.max()} (trung bình: {ages.mean():.1f})")
    print(f"Khách hàng tiềm năng: {(df['Response'] == 1).sum()} ({(df['Response'] == 1).mean()*100:.1f}%)")
    print(f"Mô hình tốt nhất: {best_model_name}")
    print(f"Độ chính xác: {results[best_model_name]['accuracy']:.4f}")
    
    # Lưu kết quả
    results_df = pd.DataFrame({
        'Model': list(results.keys()),
        'Accuracy': [results[name]['accuracy'] for name in results.keys()],
        'CV_Mean': [results[name]['cv_mean'] for name in results.keys()],
        'CV_Std': [results[name]['cv_std'] for name in results.keys()]
    })
    
    results_df.to_csv('student_model_results_627.csv', index=False)
    print(f"\nĐã lưu kết quả vào: student_model_results_627.csv")
    
    return best_model, scaler, results

if __name__ == "__main__":
    model, scaler, results = train_student_model()
    print("\nTraining mô hình sinh viên hoàn tất!")