#!/usr/bin/env python3
"""
Advanced ML Pipeline - Simplified for quick run
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, StackingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
import joblib
import json
import warnings
warnings.filterwarnings('ignore')

print('=' * 70)
print('ADVANCED ML PIPELINE - QUICK RUN')
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
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f'\nTrain: {len(X_train)}, Test: {len(X_test)}')

# 1. HYPERPARAMETER TUNING
print('\n' + '=' * 70)
print('1. HYPERPARAMETER TUNING')
print('=' * 70)

# SVM Tuning (quick)
print('\nTuning SVM...')
svm_params = {
    'C': [1, 10],
    'gamma': ['scale', 0.001],
    'kernel': ['rbf']
}
svm_grid = GridSearchCV(SVC(probability=True, random_state=42), svm_params, 
                        cv=3, scoring='f1', n_jobs=-1, verbose=0)
svm_grid.fit(X_train_scaled, y_train)
print(f'✓ Best params: {svm_grid.best_params_}')
print(f'✓ Best CV F1: {svm_grid.best_score_:.4f}')

# Random Forest Tuning (quick)
print('\nTuning Random Forest...')
rf_params = {
    'n_estimators': [100, 200],
    'max_depth': [10, None]
}
rf_grid = GridSearchCV(RandomForestClassifier(random_state=42), rf_params,
                       cv=3, scoring='f1', n_jobs=-1, verbose=0)
rf_grid.fit(X_train, y_train)
print(f'✓ Best params: {rf_grid.best_params_}')
print(f'✓ Best CV F1: {rf_grid.best_score_:.4f}')

# Gradient Boosting Tuning
print('\nTuning Gradient Boosting...')
gb_params = {
    'n_estimators': [100],
    'learning_rate': [0.1],
    'max_depth': [5]
}
gb_grid = GridSearchCV(GradientBoostingClassifier(random_state=42), gb_params,
                       cv=3, scoring='f1', n_jobs=-1, verbose=0)
gb_grid.fit(X_train, y_train)
print(f'✓ Best params: {gb_grid.best_params_}')
print(f'✓ Best CV F1: {gb_grid.best_score_:.4f}')

# 2. ENSEMBLE - STACKING
print('\n' + '=' * 70)
print('2. STACKING ENSEMBLE')
print('=' * 70)

print('\nBuilding stacking classifier...')
stacking = StackingClassifier(
    estimators=[
        ('svm', svm_grid.best_estimator_),
        ('rf', rf_grid.best_estimator_),
        ('gb', gb_grid.best_estimator_)
    ],
    final_estimator=LogisticRegression(max_iter=1000, random_state=42),
    cv=3
)
stacking.fit(X_train_scaled, y_train)
print('✓ Stacking ensemble trained')

# 3. EVALUATION
print('\n' + '=' * 70)
print('3. MODEL EVALUATION')
print('=' * 70)

models = {
    'SVM (Baseline)': SVC(probability=True, random_state=42),
    'SVM (Tuned)': svm_grid.best_estimator_,
    'RF (Tuned)': rf_grid.best_estimator_,
    'GB (Tuned)': gb_grid.best_estimator_,
    'Stacking Ensemble': stacking
}

# Train baseline SVM for comparison
models['SVM (Baseline)'].fit(X_train_scaled, y_train)

results = {}
print('\n{:<25s} {:>8s} {:>8s} {:>8s} {:>8s}'.format('Model', 'F1', 'Acc', 'Prec', 'Recall'))
print('-' * 70)

for name, model in models.items():
    # Predict
    if 'SVM' in name or 'Stacking' in name:
        y_pred = model.predict(X_test_scaled)
        y_proba = model.predict_proba(X_test_scaled)[:, 1]
    else:
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]
    
    # Metrics
    f1 = f1_score(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    
    # Cross-validation
    if 'SVM' in name or 'Stacking' in name:
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='f1')
    else:
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
    
    results[name] = {
        'f1_score': float(f1),
        'accuracy': float(acc),
        'precision': float(prec),
        'recall': float(rec),
        'cv_mean': float(cv_scores.mean()),
        'cv_std': float(cv_scores.std())
    }
    
    print(f'{name:<25s} {f1:>7.4f} {acc:>7.4f} {prec:>7.4f} {rec:>7.4f}')

# Find best
best_name = max(results.keys(), key=lambda x: results[x]['f1_score'])
print('\n' + '=' * 70)
print(f'🏆 BEST MODEL: {best_name}')
print(f'   F1-Score:  {results[best_name]["f1_score"]:.4f}')
print(f'   Accuracy:  {results[best_name]["accuracy"]:.4f}')
print(f'   Precision: {results[best_name]["precision"]:.4f}')
print(f'   Recall:    {results[best_name]["recall"]:.4f}')
print(f'   CV F1:     {results[best_name]["cv_mean"]:.4f} (±{results[best_name]["cv_std"]:.4f})')

# Save
print('\n' + '=' * 70)
print('4. SAVING RESULTS')
print('=' * 70)

import os
os.makedirs('defense_results/advanced', exist_ok=True)

joblib.dump(models[best_name], 'defense_results/advanced/best_advanced_model.pkl')
joblib.dump(scaler, 'defense_results/advanced/scaler.pkl')

# Save comparison
comparison = {
    'baseline': {
        'model': 'SVM (Default)',
        'f1_score': results['SVM (Baseline)']['f1_score'],
        'accuracy': results['SVM (Baseline)']['accuracy']
    },
    'advanced': {
        'model': best_name,
        'f1_score': results[best_name]['f1_score'],
        'accuracy': results[best_name]['accuracy']
    },
    'improvement': {
        'f1_delta': results[best_name]['f1_score'] - results['SVM (Baseline)']['f1_score'],
        'f1_percent': ((results[best_name]['f1_score'] - results['SVM (Baseline)']['f1_score']) / 
                       results['SVM (Baseline)']['f1_score'] * 100)
    },
    'all_results': results
}

with open('defense_results/advanced/advanced_results.json', 'w') as f:
    json.dump(comparison, f, indent=2)

print('✓ Saved: best_advanced_model.pkl')
print('✓ Saved: scaler.pkl')
print('✓ Saved: advanced_results.json')

# Summary
print('\n' + '=' * 70)
print('SUMMARY')
print('=' * 70)
print(f'\nBaseline SVM:  F1 = {results["SVM (Baseline)"]["f1_score"]:.4f}')
print(f'Advanced Best: F1 = {results[best_name]["f1_score"]:.4f}')
print(f'Improvement:   +{comparison["improvement"]["f1_delta"]:.4f} ({comparison["improvement"]["f1_percent"]:.2f}%)')
print('\n✅ ADVANCED ML PIPELINE COMPLETED!')

