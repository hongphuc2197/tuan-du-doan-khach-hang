#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phân tích chi tiết mô hình dự đoán khách hàng tiềm năng
Dựa trên dataset thực tế từ website Kyanon Digital
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def analyze_dataset():
    """Phân tích chi tiết dataset"""
    print("=== PHÂN TÍCH CHI TIẾT DATASET ===")
    
    # Tải dataset
    df = pd.read_csv('../marketing_campaign_students_627.csv', sep='\t')
    
    print(f"📊 THÔNG TIN TỔNG QUAN:")
    print(f"- Tổng số khách hàng: {len(df)}")
    print(f"- Số features: {len(df.columns)}")
    print(f"- Số khách hàng tiềm năng: {(df['Response'] == 1).sum()}")
    print(f"- Tỷ lệ khách hàng tiềm năng: {(df['Response'] == 1).mean()*100:.2f}%")
    
    # Phân tích độ tuổi
    df['Age'] = 2024 - df['Year_Birth']
    print(f"\n👥 PHÂN TÍCH ĐỘ TUỔI:")
    print(f"- Tuổi trung bình: {df['Age'].mean():.1f}")
    print(f"- Tuổi tối thiểu: {df['Age'].min()}")
    print(f"- Tuổi tối đa: {df['Age'].max()}")
    print(f"- Độ lệch chuẩn: {df['Age'].std():.1f}")
    
    # Phân tích thu nhập
    print(f"\n💰 PHÂN TÍCH THU NHẬP:")
    print(f"- Thu nhập trung bình: {df['Income'].mean():,.0f} VNĐ")
    print(f"- Thu nhập tối thiểu: {df['Income'].min():,.0f} VNĐ")
    print(f"- Thu nhập tối đa: {df['Income'].max():,.0f} VNĐ")
    print(f"- Độ lệch chuẩn: {df['Income'].std():,.0f} VNĐ")
    
    # Phân tích trình độ học vấn
    print(f"\n🎓 PHÂN TÍCH TRÌNH ĐỘ HỌC VẤN:")
    education_counts = df['Education'].value_counts()
    for edu, count in education_counts.items():
        percentage = (count / len(df)) * 100
        print(f"- {edu}: {count} ({percentage:.1f}%)")
    
    # Phân tích tình trạng hôn nhân
    print(f"\n💑 PHÂN TÍCH TÌNH TRẠNG HÔN NHÂN:")
    marital_counts = df['Marital_Status'].value_counts()
    for status, count in marital_counts.items():
        percentage = (count / len(df)) * 100
        print(f"- {status}: {count} ({percentage:.1f}%)")
    
    # Phân tích chi tiêu
    spending_cols = ['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
    print(f"\n💸 PHÂN TÍCH CHI TIÊU THEO DANH MỤC:")
    for col in spending_cols:
        avg_spending = df[col].mean()
        print(f"- {col}: {avg_spending:,.0f} VNĐ")
    
    return df

def create_realistic_evaluation():
    """Tạo đánh giá thực tế hơn với noise và validation"""
    print("\n=== ĐÁNH GIÁ MÔ HÌNH THỰC TẾ ===")
    
    # Tải dataset
    df = pd.read_csv('../marketing_campaign_students_627.csv', sep='\t')
    
    # Chuẩn bị features
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
    
    # Thêm noise để mô phỏng dữ liệu thực tế
    np.random.seed(42)
    noise_factor = 0.01  # 1% noise
    X_noisy = X.copy()
    for col in X_noisy.columns:
        if X_noisy[col].dtype in ['int64', 'float64']:
            noise = np.random.normal(0, X_noisy[col].std() * noise_factor, len(X_noisy))
            X_noisy[col] = X_noisy[col] + noise
    
    # Chia dữ liệu với stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X_noisy, y, test_size=0.3, random_state=42, stratify=y
    )
    
    # Chuẩn hóa dữ liệu
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Định nghĩa các mô hình với hyperparameters thực tế
    models = {
        'Logistic Regression': LogisticRegression(
            random_state=42, 
            max_iter=1000,
            C=1.0,
            penalty='l2'
        ),
        'Random Forest': RandomForestClassifier(
            n_estimators=100, 
            random_state=42,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2
        ),
        'Gradient Boosting': GradientBoostingClassifier(
            n_estimators=100, 
            random_state=42,
            learning_rate=0.1,
            max_depth=6,
            min_samples_split=5
        ),
        'SVM': SVC(
            random_state=42, 
            probability=True,
            C=1.0,
            kernel='rbf',
            gamma='scale'
        )
    }
    
    # Cross-validation setup
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    results = {}
    
    print("🔄 Training các mô hình với dữ liệu có noise...")
    
    for name, model in models.items():
        print(f"\n📈 Training {name}...")
        
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
        
        # ROC AUC
        try:
            roc_auc = roc_auc_score(y_test, y_pred_proba)
        except:
            roc_auc = 0.0
        
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
            'roc_auc': roc_auc,
            'cv_mean': cv_mean,
            'cv_std': cv_std,
            'y_test': y_test,
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba
        }
        
        print(f"✅ Accuracy: {accuracy:.4f}")
        print(f"✅ Precision: {precision:.4f}")
        print(f"✅ Recall: {recall:.4f}")
        print(f"✅ F1-score: {f1:.4f}")
        print(f"✅ ROC AUC: {roc_auc:.4f}")
        print(f"✅ CV Mean: {cv_mean:.4f} (+/- {cv_std:.4f})")
    
    return results

def create_detailed_comparison_table(results):
    """Tạo bảng so sánh chi tiết"""
    print("\n📊 BẢNG SO SÁNH CHI TIẾT CÁC MÔ HÌNH")
    print("=" * 80)
    
    # Tạo DataFrame
    comparison_data = []
    for name, metrics in results.items():
        comparison_data.append({
            'Mô hình': name,
            'Accuracy': f"{metrics['accuracy']:.4f}",
            'Precision': f"{metrics['precision']:.4f}",
            'Recall': f"{metrics['recall']:.4f}",
            'F1-score': f"{metrics['f1_score']:.4f}",
            'ROC AUC': f"{metrics['roc_auc']:.4f}",
            'CV Mean': f"{metrics['cv_mean']:.4f}",
            'CV Std': f"{metrics['cv_std']:.4f}"
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    print(comparison_df.to_string(index=False))
    
    return comparison_df

def rank_models(results):
    """Xếp hạng các mô hình"""
    print("\n🏆 XẾP HẠNG CÁC MÔ HÌNH")
    print("=" * 50)
    
    # Tính điểm tổng hợp (weighted score)
    rankings = []
    for name, metrics in results.items():
        # Trọng số: F1-score (40%), Accuracy (30%), ROC AUC (20%), CV Mean (10%)
        composite_score = (
            metrics['f1_score'] * 0.4 +
            metrics['accuracy'] * 0.3 +
            metrics['roc_auc'] * 0.2 +
            metrics['cv_mean'] * 0.1
        )
        
        rankings.append({
            'Model': name,
            'Composite Score': composite_score,
            'F1-score': metrics['f1_score'],
            'Accuracy': metrics['accuracy'],
            'ROC AUC': metrics['roc_auc']
        })
    
    # Sắp xếp theo composite score
    rankings.sort(key=lambda x: x['Composite Score'], reverse=True)
    
    for i, rank in enumerate(rankings, 1):
        print(f"{i}. {rank['Model']}")
        print(f"   Composite Score: {rank['Composite Score']:.4f}")
        print(f"   F1-score: {rank['F1-score']:.4f}")
        print(f"   Accuracy: {rank['Accuracy']:.4f}")
        print(f"   ROC AUC: {rank['ROC AUC']:.4f}")
        print()
    
    return rankings

def create_roc_curves(results):
    """Tạo ROC curves"""
    print("\n📈 Tạo ROC Curves...")
    
    plt.figure(figsize=(10, 8))
    
    for name, metrics in results.items():
        fpr, tpr, _ = roc_curve(metrics['y_test'], metrics['y_pred_proba'])
        plt.plot(fpr, tpr, label=f'{name} (AUC = {metrics["roc_auc"]:.3f})')
    
    plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curves - So sánh các mô hình')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('roc_curves_comparison.png', dpi=300, bbox_inches='tight')
    print("✅ Đã lưu ROC curves: roc_curves_comparison.png")

def save_detailed_report(results, comparison_df, rankings):
    """Lưu báo cáo chi tiết"""
    print("\n💾 Lưu báo cáo chi tiết...")
    
    with open('detailed_model_analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write("BÁO CÁO PHÂN TÍCH CHI TIẾT MÔ HÌNH DỰ ĐOÁN KHÁCH HÀNG TIỀM NĂNG\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Ngày tạo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Dựa trên dataset thực tế từ website Kyanon Digital\n\n")
        
        f.write("1. BẢNG SO SÁNH CHI TIẾT:\n")
        f.write("-" * 50 + "\n")
        f.write(comparison_df.to_string(index=False))
        f.write("\n\n")
        
        f.write("2. XẾP HẠNG MÔ HÌNH:\n")
        f.write("-" * 50 + "\n")
        for i, rank in enumerate(rankings, 1):
            f.write(f"{i}. {rank['Model']}\n")
            f.write(f"   Composite Score: {rank['Composite Score']:.4f}\n")
            f.write(f"   F1-score: {rank['F1-score']:.4f}\n")
            f.write(f"   Accuracy: {rank['Accuracy']:.4f}\n")
            f.write(f"   ROC AUC: {rank['ROC AUC']:.4f}\n\n")
        
        f.write("3. KHUYẾN NGHỊ:\n")
        f.write("-" * 50 + "\n")
        best_model = rankings[0]
        f.write(f"Mô hình tốt nhất: {best_model['Model']}\n")
        f.write(f"Lý do: Composite Score cao nhất ({best_model['Composite Score']:.4f})\n")
        f.write(f"Phù hợp cho: Dự đoán khách hàng tiềm năng trong thực tế\n")
    
    print("✅ Đã lưu báo cáo chi tiết: detailed_model_analysis_report.txt")

def main():
    """Hàm chính"""
    print("🔍 PHÂN TÍCH CHI TIẾT MÔ HÌNH DỰ ĐOÁN KHÁCH HÀNG TIỀM NĂNG")
    print("Dựa trên dataset thực tế từ website Kyanon Digital\n")
    
    try:
        # 1. Phân tích dataset
        df = analyze_dataset()
        
        # 2. Đánh giá mô hình thực tế
        results = create_realistic_evaluation()
        
        # 3. Tạo bảng so sánh chi tiết
        comparison_df = create_detailed_comparison_table(results)
        
        # 4. Xếp hạng mô hình
        rankings = rank_models(results)
        
        # 5. Tạo ROC curves
        create_roc_curves(results)
        
        # 6. Lưu báo cáo chi tiết
        save_detailed_report(results, comparison_df, rankings)
        
        print("\n🎉 HOÀN THÀNH PHÂN TÍCH CHI TIẾT!")
        print("Tất cả kết quả đã được lưu trong thư mục analytics/")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()