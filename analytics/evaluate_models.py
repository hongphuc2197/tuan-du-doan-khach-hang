#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script đánh giá mô hình dự đoán khách hàng tiềm năng
Dựa trên dataset thực tế từ website Kyanon Digital
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def load_and_prepare_data():
    """Tải và chuẩn bị dữ liệu"""
    print("=== TẢI VÀ CHUẨN BỊ DỮ LIỆU ===")
    
    # Tải dataset
    df = pd.read_csv('../marketing_campaign_students_627.csv', sep='\t')
    print(f"Dataset có {len(df)} dòng và {len(df.columns)} cột")
    
    # Hiển thị thông tin cơ bản
    print(f"\nThông tin dataset:")
    print(f"- Số khách hàng tiềm năng: {(df['Response'] == 1).sum()}")
    print(f"- Tỷ lệ khách hàng tiềm năng: {(df['Response'] == 1).mean()*100:.2f}%")
    print(f"- Độ tuổi trung bình: {2024 - df['Year_Birth'].mean():.1f}")
    print(f"- Thu nhập trung bình: {df['Income'].mean():,.0f} VNĐ")
    
    return df

def prepare_features(df):
    """Chuẩn bị features cho training"""
    print("\n=== CHUẨN BỊ FEATURES ===")
    
    # Chọn features quan trọng
    feature_columns = [
        'Year_Birth', 'Income', 'Kidhome', 'Teenhome', 'Recency',
        'MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 
        'MntSweetProducts', 'MntGoldProds', 'NumDealsPurchases',
        'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases', 
        'NumWebVisitsMonth'
    ]
    
    # Xử lý categorical variables
    le_education = LabelEncoder()
    le_marital = LabelEncoder()
    
    df['Education_encoded'] = le_education.fit_transform(df['Education'])
    df['Marital_Status_encoded'] = le_marital.fit_transform(df['Marital_Status'])
    
    feature_columns.extend(['Education_encoded', 'Marital_Status_encoded'])
    
    X = df[feature_columns]
    y = df['Response']
    
    print(f"Số features: {len(feature_columns)}")
    print(f"Features: {feature_columns}")
    
    return X, y, feature_columns

def train_models(X, y):
    """Training các mô hình"""
    print("\n=== TRAINING CÁC MÔ HÌNH ===")
    
    # Chia dữ liệu
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Chuẩn hóa dữ liệu
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Định nghĩa các mô hình
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
        'SVM': SVC(random_state=42, probability=True)
    }
    
    # Cross-validation setup
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    results = {}
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        
        # Training
        if name == 'SVM':
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        # Tính toán metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        # Cross-validation
        if name == 'SVM':
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=cv, scoring='accuracy')
        else:
            cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='accuracy')
        
        cv_mean = cv_scores.mean()
        cv_std = cv_scores.std()
        
        # Lưu kết quả
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'cv_mean': cv_mean,
            'cv_std': cv_std,
            'y_test': y_test,
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba
        }
        
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1-score: {f1:.4f}")
        print(f"CV Mean: {cv_mean:.4f} (+/- {cv_std:.4f})")
    
    return results, scaler

def create_evaluation_table(results):
    """Tạo bảng đánh giá chi tiết"""
    print("\n=== BẢNG ĐÁNH GIÁ MÔ HÌNH ===")
    
    # Tạo DataFrame
    eval_data = []
    for name, metrics in results.items():
        eval_data.append({
            'Mô hình': name,
            'Accuracy': f"{metrics['accuracy']:.4f}",
            'Precision': f"{metrics['precision']:.4f}",
            'Recall': f"{metrics['recall']:.4f}",
            'F1-score': f"{metrics['f1_score']:.4f}",
            'CV Mean': f"{metrics['cv_mean']:.4f}",
            'CV Std': f"{metrics['cv_std']:.4f}"
        })
    
    eval_df = pd.DataFrame(eval_data)
    print(eval_df.to_string(index=False))
    
    return eval_df

def find_best_model(results):
    """Tìm mô hình tốt nhất"""
    print("\n=== MÔ HÌNH TỐT NHẤT ===")
    
    # Sắp xếp theo F1-score (cân bằng precision và recall)
    sorted_models = sorted(results.items(), key=lambda x: x[1]['f1_score'], reverse=True)
    
    best_name, best_metrics = sorted_models[0]
    
    print(f"Mô hình tốt nhất: {best_name}")
    print(f"Accuracy: {best_metrics['accuracy']:.4f}")
    print(f"Precision: {best_metrics['precision']:.4f}")
    print(f"Recall: {best_metrics['recall']:.4f}")
    print(f"F1-score: {best_metrics['f1_score']:.4f}")
    print(f"CV Mean: {best_metrics['cv_mean']:.4f} (+/- {best_metrics['cv_std']:.4f})")
    
    return best_name, best_metrics

def create_visualizations(results):
    """Tạo các biểu đồ đánh giá"""
    print("\n=== TẠO BIỂU ĐỒ ĐÁNH GIÁ ===")
    
    # Chuẩn bị dữ liệu cho biểu đồ
    model_names = list(results.keys())
    accuracies = [results[name]['accuracy'] for name in model_names]
    precisions = [results[name]['precision'] for name in model_names]
    recalls = [results[name]['recall'] for name in model_names]
    f1_scores = [results[name]['f1_score'] for name in model_names]
    
    # Tạo figure với subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Đánh giá các mô hình dự đoán khách hàng tiềm năng', fontsize=16)
    
    # Accuracy comparison
    axes[0, 0].bar(model_names, accuracies, color='skyblue', alpha=0.7)
    axes[0, 0].set_title('So sánh Accuracy')
    axes[0, 0].set_ylabel('Accuracy')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # Precision vs Recall
    x = np.arange(len(model_names))
    width = 0.35
    axes[0, 1].bar(x - width/2, precisions, width, label='Precision', alpha=0.7)
    axes[0, 1].bar(x + width/2, recalls, width, label='Recall', alpha=0.7)
    axes[0, 1].set_title('Precision vs Recall')
    axes[0, 1].set_ylabel('Score')
    axes[0, 1].set_xticks(x)
    axes[0, 1].set_xticklabels(model_names, rotation=45)
    axes[0, 1].legend()
    
    # F1-score comparison
    axes[1, 0].bar(model_names, f1_scores, color='lightgreen', alpha=0.7)
    axes[1, 0].set_title('So sánh F1-score')
    axes[1, 0].set_ylabel('F1-score')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # CV Mean comparison
    cv_means = [results[name]['cv_mean'] for name in model_names]
    cv_stds = [results[name]['cv_std'] for name in model_names]
    axes[1, 1].bar(model_names, cv_means, yerr=cv_stds, color='orange', alpha=0.7, capsize=5)
    axes[1, 1].set_title('Cross-Validation Mean ± Std')
    axes[1, 1].set_ylabel('CV Mean')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('model_evaluation_comparison.png', dpi=300, bbox_inches='tight')
    print("Đã lưu biểu đồ: model_evaluation_comparison.png")
    
    return fig

def create_confusion_matrices(results):
    """Tạo confusion matrix cho tất cả mô hình"""
    print("\n=== CONFUSION MATRICES ===")
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Confusion Matrices - Các mô hình dự đoán', fontsize=16)
    
    for idx, (name, metrics) in enumerate(results.items()):
        row = idx // 2
        col = idx % 2
        
        cm = confusion_matrix(metrics['y_test'], metrics['y_pred'])
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[row, col])
        axes[row, col].set_title(f'{name}\nAccuracy: {metrics["accuracy"]:.3f}')
        axes[row, col].set_xlabel('Predicted')
        axes[row, col].set_ylabel('Actual')
    
    plt.tight_layout()
    plt.savefig('confusion_matrices.png', dpi=300, bbox_inches='tight')
    print("Đã lưu confusion matrices: confusion_matrices.png")

def save_results(results, eval_df, best_name, best_metrics):
    """Lưu kết quả đánh giá"""
    print("\n=== LƯU KẾT QUẢ ===")
    
    # Lưu bảng đánh giá
    eval_df.to_csv('model_evaluation_results.csv', index=False)
    print("Đã lưu bảng đánh giá: model_evaluation_results.csv")
    
    # Lưu mô hình tốt nhất
    best_model = results[best_name]['model']
    joblib.dump(best_model, f'best_model_{best_name.lower().replace(" ", "_")}.pkl')
    print(f"Đã lưu mô hình tốt nhất: best_model_{best_name.lower().replace(' ', '_')}.pkl")
    
    # Lưu báo cáo chi tiết
    with open('model_evaluation_report.txt', 'w', encoding='utf-8') as f:
        f.write("BÁO CÁO ĐÁNH GIÁ MÔ HÌNH DỰ ĐOÁN KHÁCH HÀNG TIỀM NĂNG\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Ngày tạo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("BẢNG ĐÁNH GIÁ CHI TIẾT:\n")
        f.write("-" * 40 + "\n")
        f.write(eval_df.to_string(index=False))
        f.write("\n\n")
        
        f.write(f"MÔ HÌNH TỐT NHẤT: {best_name}\n")
        f.write("-" * 40 + "\n")
        f.write(f"Accuracy: {best_metrics['accuracy']:.4f}\n")
        f.write(f"Precision: {best_metrics['precision']:.4f}\n")
        f.write(f"Recall: {best_metrics['recall']:.4f}\n")
        f.write(f"F1-score: {best_metrics['f1_score']:.4f}\n")
        f.write(f"CV Mean: {best_metrics['cv_mean']:.4f} (+/- {best_metrics['cv_std']:.4f})\n")
    
    print("Đã lưu báo cáo chi tiết: model_evaluation_report.txt")

def main():
    """Hàm chính"""
    print("=== ĐÁNH GIÁ MÔ HÌNH DỰ ĐOÁN KHÁCH HÀNG TIỀM NĂNG ===")
    print("Dựa trên dataset thực tế từ website Kyanon Digital\n")
    
    try:
        # 1. Tải và chuẩn bị dữ liệu
        df = load_and_prepare_data()
        
        # 2. Chuẩn bị features
        X, y, feature_columns = prepare_features(df)
        
        # 3. Training các mô hình
        results, scaler = train_models(X, y)
        
        # 4. Tạo bảng đánh giá
        eval_df = create_evaluation_table(results)
        
        # 5. Tìm mô hình tốt nhất
        best_name, best_metrics = find_best_model(results)
        
        # 6. Tạo biểu đồ
        create_visualizations(results)
        create_confusion_matrices(results)
        
        # 7. Lưu kết quả
        save_results(results, eval_df, best_name, best_metrics)
        
        print("\n=== HOÀN THÀNH ĐÁNH GIÁ MÔ HÌNH ===")
        print("Tất cả kết quả đã được lưu trong thư mục analytics/")
        
    except Exception as e:
        print(f"Lỗi: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()