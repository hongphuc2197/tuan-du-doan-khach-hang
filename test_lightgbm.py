#!/usr/bin/env python3
"""
Test LightGBM and other boosting methods to improve F1-score
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
from sklearn.ensemble import GradientBoostingClassifier
import warnings
warnings.filterwarnings('ignore')

print('=' * 70)
print('TESTING BOOSTING METHODS FOR F1 IMPROVEMENT')
print('=' * 70)

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

# Scale for SVM
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print('\n' + '=' * 70)
print('MODEL COMPARISON')
print('=' * 70)

results = {}

# 1. Baseline SVM
from sklearn.svm import SVC
print('\n1. SVM (Baseline):')
svm = SVC(probability=True, random_state=42)
svm.fit(X_train_scaled, y_train)
y_pred = svm.predict(X_test_scaled)
results['SVM'] = {
    'f1': f1_score(y_test, y_pred),
    'acc': accuracy_score(y_test, y_pred),
    'prec': precision_score(y_test, y_pred),
    'rec': recall_score(y_test, y_pred)
}
print(f'   F1: {results["SVM"]["f1"]:.4f}')

# 2. Gradient Boosting (Default)
print('\n2. Gradient Boosting (Default):')
gb_default = GradientBoostingClassifier(random_state=42)
gb_default.fit(X_train, y_train)
y_pred = gb_default.predict(X_test)
results['GB_Default'] = {
    'f1': f1_score(y_test, y_pred),
    'acc': accuracy_score(y_test, y_pred),
    'prec': precision_score(y_test, y_pred),
    'rec': recall_score(y_test, y_pred)
}
print(f'   F1: {results["GB_Default"]["f1"]:.4f}')

# 3. Gradient Boosting (Tuned)
print('\n3. Gradient Boosting (Tuned):')
print('   Running GridSearchCV...')
gb_params = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.05, 0.1, 0.2],
    'max_depth': [3, 5, 7],
    'min_samples_split': [2, 5],
    'subsample': [0.8, 1.0]
}

gb_grid = GridSearchCV(
    GradientBoostingClassifier(random_state=42),
    gb_params,
    cv=5,
    scoring='f1',
    n_jobs=-1,
    verbose=0
)
gb_grid.fit(X_train, y_train)

print(f'   Best params: {gb_grid.best_params_}')
print(f'   Best CV F1:  {gb_grid.best_score_:.4f}')

y_pred = gb_grid.best_estimator_.predict(X_test)
results['GB_Tuned'] = {
    'f1': f1_score(y_test, y_pred),
    'acc': accuracy_score(y_test, y_pred),
    'prec': precision_score(y_test, y_pred),
    'rec': recall_score(y_test, y_pred)
}
print(f'   Test F1: {results["GB_Tuned"]["f1"]:.4f}')

# 4. AdaBoost
from sklearn.ensemble import AdaBoostClassifier
print('\n4. AdaBoost:')
ada = AdaBoostClassifier(n_estimators=100, learning_rate=0.1, random_state=42)
ada.fit(X_train, y_train)
y_pred = ada.predict(X_test)
results['AdaBoost'] = {
    'f1': f1_score(y_test, y_pred),
    'acc': accuracy_score(y_test, y_pred),
    'prec': precision_score(y_test, y_pred),
    'rec': recall_score(y_test, y_pred)
}
print(f'   F1: {results["AdaBoost"]["f1"]:.4f}')

# 5. HistGradientBoosting (Fast GradientBoosting)
from sklearn.ensemble import HistGradientBoostingClassifier
print('\n5. HistGradientBoosting:')
hgb = HistGradientBoostingClassifier(
    max_iter=200,
    learning_rate=0.1,
    max_depth=7,
    random_state=42
)
hgb.fit(X_train, y_train)
y_pred = hgb.predict(X_test)
results['HistGB'] = {
    'f1': f1_score(y_test, y_pred),
    'acc': accuracy_score(y_test, y_pred),
    'prec': precision_score(y_test, y_pred),
    'rec': recall_score(y_test, y_pred)
}
print(f'   F1: {results["HistGB"]["f1"]:.4f}')

# 6. Stacking with best models
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression
print('\n6. Stacking (RF + GB + SVM):')
from sklearn.ensemble import RandomForestClassifier

stacking = StackingClassifier(
    estimators=[
        ('rf', RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)),
        ('gb', gb_grid.best_estimator_),
        ('svm', svm)
    ],
    final_estimator=LogisticRegression(max_iter=1000, random_state=42),
    cv=3
)

# Fit with scaled data for consistency
stacking.fit(X_train_scaled, y_train)
y_pred = stacking.predict(X_test_scaled)
results['Stacking'] = {
    'f1': f1_score(y_test, y_pred),
    'acc': accuracy_score(y_test, y_pred),
    'prec': precision_score(y_test, y_pred),
    'rec': recall_score(y_test, y_pred)
}
print(f'   F1: {results["Stacking"]["f1"]:.4f}')

# Summary
print('\n' + '=' * 70)
print('SUMMARY TABLE')
print('=' * 70)

baseline_f1 = results['SVM']['f1']

print(f'\n{"Model":<25s} {"F1":>8s} {"Acc":>8s} {"Prec":>8s} {"Rec":>8s} {"vs SVM":>10s}')
print('-' * 80)

for name, metrics in results.items():
    improvement = metrics['f1'] - baseline_f1
    pct = (improvement / baseline_f1) * 100
    print(f'{name:<25s} {metrics["f1"]:>8.4f} {metrics["acc"]:>8.4f} {metrics["prec"]:>8.4f} {metrics["rec"]:>8.4f} {improvement:>+5.4f} ({pct:>+5.2f}%)')

# Find best
best_name = max(results.keys(), key=lambda x: results[x]['f1'])
best_f1 = results[best_name]['f1']

print(f'\n🏆 BEST MODEL: {best_name}')
print(f'   F1-Score: {best_f1:.4f}')
print(f'   Accuracy: {results[best_name]["acc"]:.4f}')
print(f'   Precision: {results[best_name]["prec"]:.4f}')
print(f'   Recall: {results[best_name]["rec"]:.4f}')

if best_f1 > baseline_f1:
    improvement = best_f1 - baseline_f1
    pct_improvement = (improvement / baseline_f1) * 100
    print(f'   ✅ IMPROVEMENT vs SVM: +{improvement:.4f} ({pct_improvement:+.2f}%)')
else:
    print(f'   ℹ️  SVM remains best baseline')

# Save results
import joblib
import json
import os

os.makedirs('defense_results/boosting', exist_ok=True)

# Save best GB model
joblib.dump(gb_grid.best_estimator_, 'defense_results/boosting/best_gb_model.pkl')

# Save all results
boosting_results = {
    'baseline_f1': float(baseline_f1),
    'best_model': best_name,
    'best_f1': float(best_f1),
    'improvement': float(best_f1 - baseline_f1),
    'improvement_percent': float(((best_f1 - baseline_f1)/baseline_f1)*100),
    'all_results': {name: {k: float(v) for k, v in metrics.items()} 
                    for name, metrics in results.items()},
    'gb_best_params': gb_grid.best_params_
}

with open('defense_results/boosting/boosting_results.json', 'w') as f:
    json.dump(boosting_results, f, indent=2)

print('\n✅ Saved results to defense_results/boosting/')
print('   • best_gb_model.pkl')
print('   • boosting_results.json')

print('\n' + '=' * 70)
print('✨ BOOSTING TEST COMPLETED!')
print('=' * 70)

