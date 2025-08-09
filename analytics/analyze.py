# analytics/analyze.py

import os
import sys
import json
import io
import warnings
warnings.filterwarnings('ignore')

# Dùng backend không GUI trước khi import pyplot
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
import pandas as pd
from pathlib import Path

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    accuracy_score,
    confusion_matrix as sk_confusion_matrix,
    roc_curve as sk_roc_curve,
    auc as sk_auc,
)
from sklearn.impute import SimpleImputer

# --- helper: log sang STDERR (để Node không bị lẫn vào JSON) ---
def log(*args):
    print(*args, file=sys.stderr)

def main():
    # ====== Load data với đường dẫn tuyệt đối
    script_dir = Path(__file__).resolve().parent
    csv_path = (script_dir / '..' / 'marketing_campaign.csv').resolve()

    if not csv_path.exists():
        print(json.dumps({
            "status": "error",
            "message": f"CSV not found at {str(csv_path)}"
        }, ensure_ascii=False))
        return

    df = pd.read_csv(csv_path, sep='\t')

    # ====== LOG thông tin cơ bản (SANG STDERR)
    log("=== Thông tin cơ bản về dữ liệu ===")
    log(f"Số dòng: {df.shape[0]}")
    log(f"Số cột: {df.shape[1]}")

    buf = io.StringIO()
    df.info(buf=buf)
    log(buf.getvalue())

    log("\nThống kê mô tả:")
    log(str(df.describe(include='all')))

    # ====== Missing values (log sang stderr)
    log("\n=== Kiểm tra missing values ===")
    mv = df.isnull().sum()
    missing_values_total = int(mv.sum())
    log(str(mv[mv > 0]))

    # ====== Xử lý missing values cho cột số
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    if numeric_cols:
        imputer = SimpleImputer(strategy='mean')
        df[numeric_cols] = imputer.fit_transform(df[numeric_cols])

    # ====== Phân tích biến mục tiêu
    log("\n=== Phân tích biến mục tiêu (Response) ===")
    target_col = 'Response'
    if target_col not in df.columns:
        print(json.dumps({
            "status": "error",
            "message": f"Missing target column '{target_col}' in CSV."
        }, ensure_ascii=False))
        return

    vc_norm = df[target_col].value_counts(normalize=True, dropna=False)
    positive_ratio = float(vc_norm.get(1, 0.0))
    negative_ratio = float(vc_norm.get(0, 0.0))
    log(str(vc_norm))

    # ====== Vẽ biểu đồ EDA (lưu file, không show)
    try:
        if 'Year_Birth' in df.columns:
            df['Age'] = 2024 - df['Year_Birth']

        plt.figure(figsize=(15, 10))

        if 'Income' in df.columns:
            plt.subplot(2, 2, 1)
            sns.histplot(data=df, x='Income', bins=30)
            plt.title('Phân phối thu nhập')

        if 'Age' in df.columns:
            plt.subplot(2, 2, 2)
            sns.histplot(data=df, x='Age', bins=30)
            plt.title('Phân phối tuổi')

        if 'Education' in df.columns and target_col in df.columns:
            plt.subplot(2, 2, 3)
            sns.countplot(data=df, x='Education', hue=target_col)
            plt.title('Tương quan giữa Education và Response')
            plt.xticks(rotation=45)

        if 'Marital_Status' in df.columns and target_col in df.columns:
            plt.subplot(2, 2, 4)
            sns.countplot(data=df, x='Marital_Status', hue=target_col)
            plt.title('Tương quan giữa Marital_Status và Response')
            plt.xticks(rotation=45)

        plt.tight_layout()
        plt.savefig(str(script_dir / 'eda_plots.png'))
        plt.close()

        if numeric_cols:
            corr = df[numeric_cols].corr()
            plt.figure(figsize=(12, 10))
            sns.heatmap(corr, annot=False, cmap='coolwarm', fmt='.2f')
            plt.title('Ma trận tương quan')
            plt.tight_layout()
            plt.savefig(str(script_dir / 'correlation_matrix.png'))
            plt.close()
    except Exception as viz_err:
        log(f"[warn] Visualization error: {viz_err}")

    # ====== Tiền xử lý cho mô hình
    features = [
        'Year_Birth', 'Income', 'Kidhome', 'Teenhome', 'Recency',
        'MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts',
        'MntSweetProducts', 'MntGoldProds', 'NumDealsPurchases',
        'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases',
        'NumWebVisitsMonth'
    ]
    features = [f for f in features if f in df.columns]
    if not features:
        print(json.dumps({
            "status": "error",
            "message": "No valid features found in CSV."
        }, ensure_ascii=False))
        return

    X = df[features].copy()
    y = df[target_col].copy()

    # Chia train/test
    strat = y if y.nunique() > 1 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=strat
    )

    # Chuẩn hoá
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train RF
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train_scaled, y_train)

    # Đánh giá
    y_pred = rf_model.predict(X_test_scaled)
    acc = float(accuracy_score(y_test, y_pred))
    report_str = classification_report(y_test, y_pred)
    log("\n=== Đánh giá mô hình ===")
    log(f"Accuracy: {acc}")
    log("Classification Report:")
    log(report_str)

    # Confusion matrix (tn, fp, fn, tp)
    tn = fp = fn = tp = 0
    try:
        cm = sk_confusion_matrix(y_test, y_pred, labels=[0, 1])
        if cm.shape == (2, 2):
            tn, fp, fn, tp = int(cm[0, 0]), int(cm[0, 1]), int(cm[1, 0]), int(cm[1, 1])
    except Exception as _:
        pass

    # ROC & AUC (nếu có predict_proba/decision_function và có cả 2 lớp)
    roc = {"fpr": [], "tpr": []}
    auc_val = None
    try:
        if getattr(rf_model, "predict_proba", None) and y_test.nunique() == 2:
            y_score = rf_model.predict_proba(X_test_scaled)[:, 1]
        elif getattr(rf_model, "decision_function", None) and y_test.nunique() == 2:
            y_score = rf_model.decision_function(X_test_scaled)
        else:
            y_score = None

        if y_score is not None:
            fpr, tpr, _ = sk_roc_curve(y_test, y_score, pos_label=1)
            # Giảm mẫu nếu dài quá để FE vẽ mượt
            if len(fpr) > 300:
                step = max(1, len(fpr) // 300)
                fpr = fpr[::step]
                tpr = tpr[::step]
            roc = {"fpr": [float(x) for x in fpr], "tpr": [float(x) for x in tpr]}
            auc_val = float(sk_auc(fpr, tpr))
    except Exception as e:
        log(f"[warn] ROC/AUC error: {e}")

    # Feature importance
    fi_df = pd.DataFrame({
        'Feature': features,
        'Importance': rf_model.feature_importances_
    }).sort_values('Importance', ascending=False)

    # Lưu hình FI
    try:
        plt.figure(figsize=(10, 6))
        sns.barplot(data=fi_df, x='Importance', y='Feature')
        plt.title('Feature Importance')
        plt.tight_layout()
        plt.savefig(str(script_dir / 'feature_importance.png'))
        plt.close()
    except Exception as fi_err:
        log(f"[warn] Feature importance plot error: {fi_err}")

    log("\n=== Feature Importance ===")
    log(str(fi_df))

    # Tính số lượng KH tiềm năng / không tiềm năng theo ratio
    total_customers = int(len(df))
    potential_customers = int(round(total_customers * positive_ratio))
    non_potential_customers = int(round(total_customers * negative_ratio))

    # Chuẩn dữ liệu cho FE (vẫn giữ cả khóa cũ để tương thích)
    feature_importance_for_fe = [
        {"name": r["Feature"], "importance": float(r["Importance"])}
        for r in fi_df.to_dict('records')
    ]

    result = {
        "status": "success",
        "data": {
            # Giữ các khóa cũ
            "total_customers": total_customers,
            "total_features": int(len(features)),
            "accuracy": float(round(acc, 6)),
            "missing_values": int(missing_values_total),
            "response_distribution": {
                "positive": positive_ratio,
                "negative": negative_ratio
            },
            "feature_importance": fi_df.to_dict('records'),

            # Bổ sung schema FE đang dùng
            "potentialCustomers": potential_customers,
            "nonPotentialCustomers": non_potential_customers,
            "featureImportance": feature_importance_for_fe,
            "confusionMatrix": {
                "tp": tp, "fp": fp, "tn": tn, "fn": fn
            },
            "rocCurve": roc,
            "auc": auc_val,

            # Thêm đường dẫn hình nếu muốn render
            "plots": {
                "eda": "eda_plots.png",
                "correlation": "correlation_matrix.png",
                "feature_importance": "feature_importance.png"
            }
        }
    }

    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "message": str(e)
        }, ensure_ascii=False))
        import traceback
        traceback.print_exc(file=sys.stderr)
