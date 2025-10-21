#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tạo các biểu đồ cho Chương 5 - Đánh giá mô hình
- Hình 5.2: ROC Curve so sánh 4 mô hình
- Hình 5.3: Confusion Matrix của mô hình tốt nhất
- Hình 5.4: Feature Importance analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, 
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
import warnings
warnings.filterwarnings('ignore')

# Thiết lập style cho matplotlib
plt.style.use('default')
sns.set_palette("husl")

def load_and_prepare_data():
    """Tải và chuẩn bị dữ liệu"""
    print("=== TẢI VÀ CHUẨN BỊ DỮ LIỆU ===")
    
    # Tạo dữ liệu mẫu để demo
    print("Tạo dữ liệu mẫu để demo...")
    np.random.seed(42)
    n_samples = 1000
    
    # Tạo dữ liệu mẫu
    data = {
        'Year_Birth': np.random.randint(1970, 2000, n_samples),
        'Income': np.random.normal(50000, 20000, n_samples).astype(int),
        'Kidhome': np.random.randint(0, 3, n_samples),
        'Teenhome': np.random.randint(0, 3, n_samples),
        'Recency': np.random.randint(0, 100, n_samples),
        'MntWines': np.random.exponential(200, n_samples).astype(int),
        'MntFruits': np.random.exponential(50, n_samples).astype(int),
        'MntMeatProducts': np.random.exponential(150, n_samples).astype(int),
        'MntFishProducts': np.random.exponential(30, n_samples).astype(int),
        'MntSweetProducts': np.random.exponential(40, n_samples).astype(int),
        'MntGoldProds': np.random.exponential(100, n_samples).astype(int),
        'NumDealsPurchases': np.random.poisson(2, n_samples),
        'NumWebPurchases': np.random.poisson(4, n_samples),
        'NumCatalogPurchases': np.random.poisson(2, n_samples),
        'NumStorePurchases': np.random.poisson(5, n_samples),
        'NumWebVisitsMonth': np.random.poisson(6, n_samples),
        'Education': np.random.choice(['Basic', 'Graduation', 'Master', 'PhD'], n_samples),
        'Marital_Status': np.random.choice(['Single', 'Married', 'Divorced', 'Together'], n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Tạo target variable dựa trên các features
    # Khách hàng tiềm năng có xu hướng có thu nhập cao, chi tiêu nhiều, và mua hàng thường xuyên
    potential_score = (
        df['Income'] / 1000 +  # Thu nhập cao
        df['MntWines'] / 100 +  # Chi tiêu rượu vang
        df['MntMeatProducts'] / 100 +  # Chi tiêu thịt
        df['NumStorePurchases'] +  # Mua hàng tại cửa hàng
        df['NumWebPurchases']  # Mua hàng online
    )
    
    # Tạo Response dựa trên potential_score
    threshold = potential_score.quantile(0.7)  # Top 30% là khách hàng tiềm năng
    df['Response'] = (potential_score > threshold).astype(int)
    
    print(f"Dataset có {len(df)} dòng và {len(df.columns)} cột")
    print(f"Số khách hàng tiềm năng: {(df['Response'] == 1).sum()}")
    print(f"Tỷ lệ khách hàng tiềm năng: {(df['Response'] == 1).mean()*100:.2f}%")
    
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
    
    results = {}
    
    for name, model in models.items():
        print(f"Training {name}...")
        
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
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        
        # Lưu kết quả
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'roc_auc': roc_auc,
            'y_test': y_test,
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba
        }
        
        print(f"  Accuracy: {accuracy:.4f}")
        print(f"  F1-score: {f1:.4f}")
        print(f"  ROC AUC: {roc_auc:.4f}")
    
    return results

def create_figure_5_2_roc_curves(results):
    """Tạo Hình 5.2 - ROC Curve so sánh 4 mô hình"""
    print("\n=== TẠO HÌNH 5.2 - ROC CURVES ===")
    
    plt.figure(figsize=(12, 8))
    
    # Màu sắc cho từng mô hình
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    for i, (name, metrics) in enumerate(results.items()):
        fpr, tpr, _ = roc_curve(metrics['y_test'], metrics['y_pred_proba'])
        plt.plot(fpr, tpr, 
                color=colors[i], 
                linewidth=2.5,
                label=f'{name} (AUC = {metrics["roc_auc"]:.3f})')
    
    # Đường chéo (random classifier)
    plt.plot([0, 1], [0, 1], 'k--', linewidth=1.5, alpha=0.7, label='Random Classifier')
    
    # Thiết lập biểu đồ
    plt.xlabel('False Positive Rate (1 - Specificity)', fontsize=12, fontweight='bold')
    plt.ylabel('True Positive Rate (Sensitivity)', fontsize=12, fontweight='bold')
    plt.title('Hình 5.2 - ROC Curves So Sánh 4 Mô Hình Dự Đoán Khách Hàng Tiềm Năng', 
              fontsize=14, fontweight='bold', pad=20)
    
    # Thiết lập legend
    plt.legend(loc='lower right', fontsize=11, frameon=True, fancybox=True, shadow=True)
    
    # Thiết lập grid
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Thiết lập axis
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    
    # Thêm text box với thông tin
    textstr = f'Dataset: {len(results[list(results.keys())[0]]["y_test"])} samples\nTest Size: 20%'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    plt.text(0.02, 0.98, textstr, transform=plt.gca().transAxes, fontsize=10,
             verticalalignment='top', bbox=props)
    
    plt.tight_layout()
    plt.savefig('Hinh_5_2_ROC_Curves.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print("✅ Đã lưu Hình 5.2: Hinh_5_2_ROC_Curves.png")
    
    return plt.gcf()

def create_figure_5_3_confusion_matrix(results):
    """Tạo Hình 5.3 - Confusion Matrix của mô hình tốt nhất"""
    print("\n=== TẠO HÌNH 5.3 - CONFUSION MATRIX ===")
    
    # Tìm mô hình tốt nhất dựa trên F1-score
    best_model_name = max(results.keys(), key=lambda x: results[x]['f1_score'])
    best_metrics = results[best_model_name]
    
    print(f"Mô hình tốt nhất: {best_model_name}")
    print(f"F1-score: {best_metrics['f1_score']:.4f}")
    print(f"Accuracy: {best_metrics['accuracy']:.4f}")
    
    # Tạo confusion matrix
    cm = confusion_matrix(best_metrics['y_test'], best_metrics['y_pred'])
    
    # Tạo biểu đồ
    plt.figure(figsize=(10, 8))
    
    # Tạo heatmap
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Không tiềm năng', 'Tiềm năng'],
                yticklabels=['Không tiềm năng', 'Tiềm năng'],
                cbar_kws={'label': 'Số lượng mẫu'})
    
    # Thiết lập tiêu đề và labels
    plt.title(f'Hình 5.3 - Confusion Matrix của Mô Hình {best_model_name}\n'
              f'(F1-score: {best_metrics["f1_score"]:.3f}, Accuracy: {best_metrics["accuracy"]:.3f})', 
              fontsize=14, fontweight='bold', pad=20)
    
    plt.xlabel('Dự đoán', fontsize=12, fontweight='bold')
    plt.ylabel('Thực tế', fontsize=12, fontweight='bold')
    
    # Thêm thông tin chi tiết
    tn, fp, fn, tp = cm.ravel()
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    
    # Text box với thông tin chi tiết
    textstr = f'True Negative: {tn}\nFalse Positive: {fp}\nFalse Negative: {fn}\nTrue Positive: {tp}\n\n' \
              f'Precision: {precision:.3f}\nRecall: {recall:.3f}\nSpecificity: {specificity:.3f}'
    
    props = dict(boxstyle='round', facecolor='lightblue', alpha=0.8)
    plt.text(0.02, 0.98, textstr, transform=plt.gca().transAxes, fontsize=10,
             verticalalignment='top', bbox=props)
    
    plt.tight_layout()
    plt.savefig('Hinh_5_3_Confusion_Matrix.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✅ Đã lưu Hình 5.3: Hinh_5_3_Confusion_Matrix.png")
    
    return plt.gcf(), best_model_name

def create_figure_5_4_feature_importance(results, feature_columns, best_model_name):
    """Tạo Hình 5.4 - Feature Importance analysis"""
    print("\n=== TẠO HÌNH 5.4 - FEATURE IMPORTANCE ===")
    
    best_model = results[best_model_name]['model']
    
    # Lấy feature importance
    if hasattr(best_model, 'feature_importances_'):
        importances = best_model.feature_importances_
    elif hasattr(best_model, 'coef_'):
        # Đối với Logistic Regression, sử dụng absolute value của coefficients
        importances = np.abs(best_model.coef_[0])
    else:
        print("⚠️ Mô hình không hỗ trợ feature importance trực tiếp")
        return None
    
    # Tạo DataFrame với feature names và importance
    feature_importance_df = pd.DataFrame({
        'feature': feature_columns,
        'importance': importances
    }).sort_values('importance', ascending=True)
    
    # Tạo biểu đồ
    plt.figure(figsize=(12, 10))
    
    # Tạo horizontal bar plot
    bars = plt.barh(range(len(feature_importance_df)), 
                    feature_importance_df['importance'],
                    color=plt.cm.viridis(np.linspace(0, 1, len(feature_importance_df))))
    
    # Thiết lập labels
    plt.yticks(range(len(feature_importance_df)), 
               feature_importance_df['feature'], fontsize=10)
    
    # Thiết lập tiêu đề và labels
    plt.title(f'Hình 5.4 - Feature Importance của Mô Hình {best_model_name}\n'
              f'(Tầm quan trọng của các đặc trưng trong dự đoán)', 
              fontsize=14, fontweight='bold', pad=20)
    
    plt.xlabel('Tầm quan trọng (Importance)', fontsize=12, fontweight='bold')
    plt.ylabel('Đặc trưng (Features)', fontsize=12, fontweight='bold')
    
    # Thêm giá trị importance trên mỗi bar
    for i, (idx, row) in enumerate(feature_importance_df.iterrows()):
        plt.text(row['importance'] + 0.001, i, f'{row["importance"]:.3f}', 
                va='center', fontsize=9)
    
    # Thiết lập grid
    plt.grid(True, alpha=0.3, axis='x')
    
    # Thêm thông tin tổng quan
    total_importance = feature_importance_df['importance'].sum()
    top_5_importance = feature_importance_df.tail(5)['importance'].sum()
    
    textstr = f'Tổng importance: {total_importance:.3f}\n' \
              f'Top 5 features: {top_5_importance:.3f} ({top_5_importance/total_importance*100:.1f}%)'
    
    props = dict(boxstyle='round', facecolor='lightgreen', alpha=0.8)
    plt.text(0.02, 0.98, textstr, transform=plt.gca().transAxes, fontsize=10,
             verticalalignment='top', bbox=props)
    
    plt.tight_layout()
    plt.savefig('Hinh_5_4_Feature_Importance.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✅ Đã lưu Hình 5.4: Hinh_5_4_Feature_Importance.png")
    
    # In top 10 features quan trọng nhất
    print(f"\n📊 TOP 10 FEATURES QUAN TRỌNG NHẤT:")
    print("-" * 50)
    top_features = feature_importance_df.tail(10)
    for i, (idx, row) in enumerate(top_features.iterrows(), 1):
        print(f"{i:2d}. {row['feature']:25s} : {row['importance']:.4f}")
    
    return plt.gcf(), feature_importance_df

def create_summary_table(results):
    """Tạo bảng tóm tắt kết quả"""
    print("\n=== BẢNG TÓM TẮT KẾT QUẢ ===")
    
    summary_data = []
    for name, metrics in results.items():
        summary_data.append({
            'Mô hình': name,
            'Accuracy': f"{metrics['accuracy']:.4f}",
            'Precision': f"{metrics['precision']:.4f}",
            'Recall': f"{metrics['recall']:.4f}",
            'F1-score': f"{metrics['f1_score']:.4f}",
            'ROC AUC': f"{metrics['roc_auc']:.4f}"
        })
    
    summary_df = pd.DataFrame(summary_data)
    print(summary_df.to_string(index=False))
    
    # Lưu bảng tóm tắt
    summary_df.to_csv('Chapter5_Model_Summary.csv', index=False, encoding='utf-8')
    print("\n✅ Đã lưu bảng tóm tắt: Chapter5_Model_Summary.csv")
    
    return summary_df

def main():
    """Hàm chính"""
    print("🎯 TẠO CÁC BIỂU ĐỒ CHO CHƯƠNG 5 - ĐÁNH GIÁ MÔ HÌNH")
    print("=" * 60)
    
    try:
        # 1. Tải và chuẩn bị dữ liệu
        df = load_and_prepare_data()
        
        # 2. Chuẩn bị features
        X, y, feature_columns = prepare_features(df)
        
        # 3. Training các mô hình
        results = train_models(X, y)
        
        # 4. Tạo Hình 5.2 - ROC Curves
        create_figure_5_2_roc_curves(results)
        
        # 5. Tạo Hình 5.3 - Confusion Matrix
        fig_cm, best_model_name = create_figure_5_3_confusion_matrix(results)
        
        # 6. Tạo Hình 5.4 - Feature Importance
        fig_fi, feature_importance_df = create_figure_5_4_feature_importance(
            results, feature_columns, best_model_name)
        
        # 7. Tạo bảng tóm tắt
        summary_df = create_summary_table(results)
        
        print("\n🎉 HOÀN THÀNH TẠO CÁC BIỂU ĐỒ CHƯƠNG 5!")
        print("=" * 60)
        print("📁 Các file đã được tạo:")
        print("   • Hinh_5_2_ROC_Curves.png")
        print("   • Hinh_5_3_Confusion_Matrix.png") 
        print("   • Hinh_5_4_Feature_Importance.png")
        print("   • Chapter5_Model_Summary.csv")
        print("\n✨ Tất cả biểu đồ đã sẵn sàng để sử dụng trong báo cáo!")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
