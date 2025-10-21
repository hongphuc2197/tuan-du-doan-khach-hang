    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nâng cấp mô hình ML cho đồ án thạc sĩ
- Thêm Deep Learning
- Ensemble Methods
- Hyperparameter Tuning
- Advanced Feature Engineering
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import VotingClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import joblib
import warnings
warnings.filterwarnings('ignore')

print('=' * 70)
print('NÂNG CẤP MÔ HÌNH ML CHO ĐỒ ÁN THẠC SĨ')
print('=' * 70)

# Đọc dữ liệu
df = pd.read_csv('../user_actions_students_576.csv')
print(f'✅ Đọc dữ liệu: {len(df)} records, {df["user_id"].nunique()} users')

# Định nghĩa mapping từ product_id đến loại sách
book_type_mapping = {
    1: "Công nghệ giáo dục", 2: "Phương pháp giảng dạy", 3: "Công nghệ thông tin",
    4: "Thiết kế web", 5: "Lập trình", 6: "Nghiên cứu khoa học",
    7: "Giáo dục STEM", 8: "Giảng dạy tiếng Anh", 9: "Thiết kế",
    10: "Cơ sở dữ liệu", 11: "Phát triển ứng dụng", 12: "Công nghệ giáo dục"
}

df['book_type'] = df['product_id'].map(book_type_mapping)

# Advanced Feature Engineering
def create_advanced_features(df):
    """Tạo features nâng cao"""
    user_behavior = df.groupby('user_id').agg({
        'event_type': lambda x: 'purchase' in x.values,
        'product_id': 'nunique',
        'price': ['sum', 'mean', 'std', 'min', 'max'],
        'age': 'first',
        'income_level': 'first',
        'education': 'first',
        'name': 'first',
        'email': 'first',
        'income': 'first',
        'book_type': lambda x: list(x.unique())
    }).reset_index()
    
    user_behavior['total_actions'] = df.groupby('user_id')['event_type'].count().values
    
    # Flatten column names
    user_behavior.columns = ['user_id', 'is_potential', 'unique_products', 'total_spending', 
                             'avg_spending', 'spending_std', 'min_spending', 'max_spending',
                             'age', 'income_level', 'education', 'name', 'email', 'income', 
                             'book_types', 'total_actions']
    
    # Advanced features
    user_behavior['spending_ratio'] = user_behavior['total_spending'] / user_behavior['income']
    user_behavior['actions_per_spending'] = user_behavior['total_actions'] / user_behavior['total_spending']
    user_behavior['price_sensitivity'] = user_behavior['spending_std'] / user_behavior['avg_spending']
    user_behavior['age_income_ratio'] = user_behavior['age'] / (user_behavior['income'] / 1000000)
    
    # Book type features
    for book_type in set(book_type_mapping.values()):
        col_name = f'books_{book_type.lower().replace(" ", "_").replace("đ", "d")}'
        user_behavior[col_name] = 0
    
    for idx, row in user_behavior.iterrows():
        user_id = row['user_id']
        user_books = df[df['user_id'] == user_id]
        
        for book_type in set(book_type_mapping.values()):
            col_name = f'books_{book_type.lower().replace(" ", "_").replace("đ", "d")}'
            count = len(user_books[user_books['book_type'] == book_type])
            user_behavior.loc[idx, col_name] = count
    
    return user_behavior

user_behavior = create_advanced_features(df)
print(f'✅ Tạo advanced features cho {len(user_behavior)} users')

# Encode categorical variables
le_income = LabelEncoder()
le_education = LabelEncoder()
user_behavior['income_encoded'] = le_income.fit_transform(user_behavior['income_level'])
user_behavior['education_encoded'] = le_education.fit_transform(user_behavior['education'])

# Prepare features
feature_columns = [
    'total_actions', 'unique_products', 'total_spending', 'avg_spending',
    'spending_std', 'min_spending', 'max_spending', 'age',
    'income_encoded', 'education_encoded', 'spending_ratio',
    'actions_per_spending', 'price_sensitivity', 'age_income_ratio'
]

# Add book type features
book_type_cols = [col for col in user_behavior.columns if col.startswith('books_')]
feature_columns.extend(book_type_cols)

X = user_behavior[feature_columns].fillna(0)
y = user_behavior['is_potential']

print(f'✅ Features: {len(feature_columns)} columns')

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f'Training set: {len(X_train)} users')
print(f'Test set: {len(X_test)} users')

# 1. HYPERPARAMETER TUNING
print('\n' + '=' * 70)
print('1. HYPERPARAMETER TUNING')
print('=' * 70)

# Random Forest tuning
rf_params = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

rf_grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    rf_params, cv=5, scoring='f1', n_jobs=-1
)
rf_grid.fit(X_train, y_train)
print(f'✅ Random Forest - Best F1: {rf_grid.best_score_:.4f}')

# SVM tuning
svm_params = {
    'C': [0.1, 1, 10, 100],
    'gamma': ['scale', 'auto', 0.001, 0.01],
    'kernel': ['rbf', 'poly']
}

svm_grid = GridSearchCV(
    SVC(random_state=42, probability=True),
    svm_params, cv=5, scoring='f1', n_jobs=-1
)
svm_grid.fit(X_train_scaled, y_train)
print(f'✅ SVM - Best F1: {svm_grid.best_score_:.4f}')

# Gradient Boosting tuning
gb_params = {
    'n_estimators': [100, 200],
    'learning_rate': [0.05, 0.1, 0.2],
    'max_depth': [3, 5, 7]
}

gb_grid = GridSearchCV(
    GradientBoostingClassifier(random_state=42),
    gb_params, cv=5, scoring='f1', n_jobs=-1
)
gb_grid.fit(X_train, y_train)
print(f'✅ Gradient Boosting - Best F1: {gb_grid.best_score_:.4f}')

# 2. DEEP LEARNING
print('\n' + '=' * 70)
print('2. DEEP LEARNING')
print('=' * 70)

# Neural Network with multiple layers
mlp_params = {
    'hidden_layer_sizes': [(100,), (100, 50), (100, 50, 25)],
    'activation': ['relu', 'tanh'],
    'alpha': [0.0001, 0.001, 0.01],
    'learning_rate': ['constant', 'adaptive']
}

mlp_grid = GridSearchCV(
    MLPClassifier(random_state=42, max_iter=1000),
    mlp_params, cv=5, scoring='f1', n_jobs=-1
)
mlp_grid.fit(X_train_scaled, y_train)
print(f'✅ Neural Network - Best F1: {mlp_grid.best_score_:.4f}')

# 3. ENSEMBLE METHODS
print('\n' + '=' * 70)
print('3. ENSEMBLE METHODS')
print('=' * 70)

# Voting Classifier
voting_clf = VotingClassifier(
    estimators=[
        ('rf', rf_grid.best_estimator_),
        ('svm', svm_grid.best_estimator_),
        ('gb', gb_grid.best_estimator_),
        ('mlp', mlp_grid.best_estimator_)
    ],
    voting='soft'
)

# Stacking Classifier
stacking_clf = StackingClassifier(
    estimators=[
        ('rf', rf_grid.best_estimator_),
        ('svm', svm_grid.best_estimator_),
        ('gb', gb_grid.best_estimator_)
    ],
    final_estimator=LogisticRegression(random_state=42),
    cv=5
)

# Train ensemble models
voting_clf.fit(X_train_scaled, y_train)
stacking_clf.fit(X_train_scaled, y_train)

print('✅ Ensemble models trained')

# 4. COMPREHENSIVE EVALUATION
print('\n' + '=' * 70)
print('4. COMPREHENSIVE EVALUATION')
print('=' * 70)

models = {
    'Random Forest (Tuned)': rf_grid.best_estimator_,
    'SVM (Tuned)': svm_grid.best_estimator_,
    'Gradient Boosting (Tuned)': gb_grid.best_estimator_,
    'Neural Network (Tuned)': mlp_grid.best_estimator_,
    'Voting Classifier': voting_clf,
    'Stacking Classifier': stacking_clf
}

results = {}

for name, model in models.items():
    print(f'\n--- Evaluating {name} ---')
    
    # Predictions
    if name in ['SVM (Tuned)', 'Neural Network (Tuned)', 'Voting Classifier', 'Stacking Classifier']:
        y_pred = model.predict(X_test_scaled)
        y_proba = model.predict_proba(X_test_scaled)[:, 1]
    else:
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]
    
    # Metrics
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)
    
    # Cross-validation
    if name in ['SVM (Tuned)', 'Neural Network (Tuned)', 'Voting Classifier', 'Stacking Classifier']:
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=10, scoring='f1')
    else:
        cv_scores = cross_val_score(model, X_train, y_train, cv=10, scoring='f1')
    
    results[name] = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'auc': auc,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std()
    }
    
    print(f'Accuracy: {accuracy:.4f}')
    print(f'Precision: {precision:.4f}')
    print(f'Recall: {recall:.4f}')
    print(f'F1-score: {f1:.4f}')
    print(f'AUC: {auc:.4f}')
    print(f'CV F1: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})')

# 5. BEST MODEL SELECTION
print('\n' + '=' * 70)
print('5. BEST MODEL SELECTION')
print('=' * 70)

# Find best model based on F1-score
best_model_name = max(results.keys(), key=lambda x: results[x]['f1_score'])
best_model = models[best_model_name]

print(f'🏆 BEST MODEL: {best_model_name}')
print(f'   F1-score: {results[best_model_name]["f1_score"]:.4f}')
print(f'   AUC: {results[best_model_name]["auc"]:.4f}')
print(f'   CV F1: {results[best_model_name]["cv_mean"]:.4f}')

# Save best model and scaler
joblib.dump(best_model, 'advanced_best_model.pkl')
joblib.dump(scaler, 'advanced_scaler.pkl')
joblib.dump(results, 'advanced_model_results.pkl')

print('✅ Saved advanced models and results')

# 6. FEATURE IMPORTANCE
print('\n' + '=' * 70)
print('6. FEATURE IMPORTANCE ANALYSIS')
print('=' * 70)

if hasattr(best_model, 'feature_importances_'):
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print('Top 10 Most Important Features:')
    print(feature_importance.head(10).to_string(index=False))
    
    # Save feature importance
    feature_importance.to_csv('advanced_feature_importance.csv', index=False)

print('\n✨ ADVANCED ML PIPELINE COMPLETED!')
print('Models ready for master thesis level analysis!')
