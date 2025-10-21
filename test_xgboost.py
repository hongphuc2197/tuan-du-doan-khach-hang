#!/usr/bin/env python3
"""
Test XGBoost to improve F1-score
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score, classification_report
import warnings
warnings.filterwarnings('ignore')

print('=' * 70)
print('TESTING XGBOOST FOR F1 IMPROVEMENT')
print('=' * 70)

# Check if xgboost is available
try:
    import xgboost as xgb
    print('✓ XGBoost available')
except ImportError:
    print('❌ XGBoost not installed. Installing...')
    import subprocess
    subprocess.check_call(['pip3', 'install', 'xgboost'])
    import xgboost as xgb
    print('✓ XGBoost installed')

# Load data
df = pd.read_csv('user_actions_students_576.csv')
print(f'\n✓ Data: {len(df)} records, {df["user_id"].nunique()} users')

# Feature engineering
user_behavior = df.groupby('user_id').agg({
    'event_type': lambda x: 'purchase' in x.values,
    'product_id': 'nunique',
    'price': ['sum', 'mean'],
    'age': 'first',
    'income_level': 'first',
    'education': 'first'
}).reset_index()

user_behavior['total_actions'] = df.groupby('user_id')['event_type'].count().values
user_behavior.columns = ['user_id', 'is_potential', 'unique_products', 'total_spending', 
                         'avg_spending', 'age', 'income_level', 'education', 'total_actions']

# Encode
le_income = LabelEncoder()
le_education = LabelEncoder()
user_behavior['income_encoded'] = le_income.fit_transform(user_behavior['income_level'])
user_behavior['education_encoded'] = le_education.fit_transform(user_behavior['education'])

# Features
feature_columns = ['total_actions', 'unique_products', 'total_spending', 
                   'avg_spending', 'age', 'income_encoded', 'education_encoded']
X = user_behavior[feature_columns].fillna(0)
y = user_behavior['is_potential']

print(f'✓ Features: {len(feature_columns)} columns')
print(f'✓ Potential: {y.sum()}/{len(y)} ({y.mean()*100:.1f}%)')

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f'\nTrain: {len(X_train)}, Test: {len(X_test)}')

# Compare models
print('\n' + '=' * 70)
print('BASELINE vs XGBOOST COMPARISON')
print('=' * 70)

# 1. Baseline SVM (for comparison)
from sklearn.svm import SVC
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

svm = SVC(probability=True, random_state=42)
svm.fit(X_train_scaled, y_train)
y_pred_svm = svm.predict(X_test_scaled)

print('\n1. BASELINE SVM (Default):')
print(f'   F1:        {f1_score(y_test, y_pred_svm):.4f}')
print(f'   Accuracy:  {accuracy_score(y_test, y_pred_svm):.4f}')
print(f'   Precision: {precision_score(y_test, y_pred_svm):.4f}')
print(f'   Recall:    {recall_score(y_test, y_pred_svm):.4f}')

# 2. XGBoost Default
print('\n2. XGBoost (Default):')
xgb_default = xgb.XGBClassifier(random_state=42, eval_metric='logloss')
xgb_default.fit(X_train, y_train)
y_pred_xgb_default = xgb_default.predict(X_test)

f1_xgb_default = f1_score(y_test, y_pred_xgb_default)
print(f'   F1:        {f1_xgb_default:.4f}')
print(f'   Accuracy:  {accuracy_score(y_test, y_pred_xgb_default):.4f}')
print(f'   Precision: {precision_score(y_test, y_pred_xgb_default):.4f}')
print(f'   Recall:    {recall_score(y_test, y_pred_xgb_default):.4f}')

# 3. XGBoost with scale_pos_weight (handle imbalance)
print('\n3. XGBoost (Balanced):')
scale_pos_weight = (len(y_train) - y_train.sum()) / y_train.sum()
print(f'   scale_pos_weight: {scale_pos_weight:.2f}')

xgb_balanced = xgb.XGBClassifier(
    scale_pos_weight=scale_pos_weight,
    random_state=42,
    eval_metric='logloss'
)
xgb_balanced.fit(X_train, y_train)
y_pred_xgb_balanced = xgb_balanced.predict(X_test)

f1_xgb_balanced = f1_score(y_test, y_pred_xgb_balanced)
print(f'   F1:        {f1_xgb_balanced:.4f}')
print(f'   Accuracy:  {accuracy_score(y_test, y_pred_xgb_balanced):.4f}')
print(f'   Precision: {precision_score(y_test, y_pred_xgb_balanced):.4f}')
print(f'   Recall:    {recall_score(y_test, y_pred_xgb_balanced):.4f}')

# 4. XGBoost with hyperparameter tuning
print('\n4. XGBoost (Tuned):')
print('   Running GridSearchCV (this may take a few minutes)...')

param_grid = {
    'max_depth': [3, 5, 7],
    'learning_rate': [0.05, 0.1, 0.2],
    'n_estimators': [100, 200, 300],
    'min_child_weight': [1, 3, 5],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0]
}

xgb_grid = GridSearchCV(
    xgb.XGBClassifier(random_state=42, eval_metric='logloss'),
    param_grid,
    cv=5,
    scoring='f1',
    n_jobs=-1,
    verbose=0
)
xgb_grid.fit(X_train, y_train)

print(f'   Best params: {xgb_grid.best_params_}')
print(f'   Best CV F1:  {xgb_grid.best_score_:.4f}')

y_pred_xgb_tuned = xgb_grid.best_estimator_.predict(X_test)
f1_xgb_tuned = f1_score(y_test, y_pred_xgb_tuned)

print(f'   Test F1:       {f1_xgb_tuned:.4f}')
print(f'   Accuracy:      {accuracy_score(y_test, y_pred_xgb_tuned):.4f}')
print(f'   Precision:     {precision_score(y_test, y_pred_xgb_tuned):.4f}')
print(f'   Recall:        {recall_score(y_test, y_pred_xgb_tuned):.4f}')

# Summary
print('\n' + '=' * 70)
print('SUMMARY')
print('=' * 70)

results = {
    'SVM (Baseline)': f1_score(y_test, y_pred_svm),
    'XGBoost (Default)': f1_xgb_default,
    'XGBoost (Balanced)': f1_xgb_balanced,
    'XGBoost (Tuned)': f1_xgb_tuned
}

print(f'\n{"Model":<25s} {"F1-Score":>10s} {"vs Baseline":>12s}')
print('-' * 70)

baseline_f1 = results['SVM (Baseline)']
for name, f1 in results.items():
    improvement = f1 - baseline_f1
    pct = (improvement / baseline_f1) * 100
    print(f'{name:<25s} {f1:>10.4f} {improvement:>+6.4f} ({pct:>+5.2f}%)')

# Find best
best_model = max(results.items(), key=lambda x: x[1])
print(f'\n🏆 BEST MODEL: {best_model[0]}')
print(f'   F1-Score: {best_model[1]:.4f}')

if best_model[1] > baseline_f1:
    print(f'   ✅ IMPROVEMENT: +{(best_model[1] - baseline_f1):.4f} ({((best_model[1] - baseline_f1)/baseline_f1)*100:.2f}%)')
else:
    print(f'   ⚠️  No improvement over baseline')

# Feature importance from best XGBoost
print('\n' + '=' * 70)
print('FEATURE IMPORTANCE (XGBoost)')
print('=' * 70)

if f1_xgb_tuned == max(f1_xgb_default, f1_xgb_balanced, f1_xgb_tuned):
    best_xgb = xgb_grid.best_estimator_
else:
    best_xgb = xgb_balanced if f1_xgb_balanced > f1_xgb_default else xgb_default

importance_df = pd.DataFrame({
    'feature': feature_columns,
    'importance': best_xgb.feature_importances_
}).sort_values('importance', ascending=False)

print(importance_df.to_string(index=False))

# Save best model
import joblib
import os
os.makedirs('defense_results/xgboost', exist_ok=True)

joblib.dump(xgb_grid.best_estimator_, 'defense_results/xgboost/best_xgboost_model.pkl')

# Save results
import json
xgb_results = {
    'baseline_svm_f1': float(baseline_f1),
    'xgboost_default_f1': float(f1_xgb_default),
    'xgboost_balanced_f1': float(f1_xgb_balanced),
    'xgboost_tuned_f1': float(f1_xgb_tuned),
    'best_model': best_model[0],
    'best_f1': float(best_model[1]),
    'improvement': float(best_model[1] - baseline_f1),
    'improvement_percent': float(((best_model[1] - baseline_f1)/baseline_f1)*100),
    'best_params': xgb_grid.best_params_,
    'feature_importance': importance_df.to_dict('records')
}

with open('defense_results/xgboost/xgboost_results.json', 'w') as f:
    json.dump(xgb_results, f, indent=2)

print('\n✅ Saved results to defense_results/xgboost/')
print('   • best_xgboost_model.pkl')
print('   • xgboost_results.json')

print('\n' + '=' * 70)
print('✨ XGBOOST TEST COMPLETED!')
print('=' * 70)

