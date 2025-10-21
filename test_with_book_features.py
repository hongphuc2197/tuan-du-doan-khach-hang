#!/usr/bin/env python3
"""
Test ML models WITH book type features
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
import joblib
import json
import warnings
warnings.filterwarnings('ignore')

print('=' * 70)
print('ML WITH BOOK TYPE FEATURES')
print('=' * 70)

# Load data
df = pd.read_csv('user_actions_students_576.csv')
print(f'\n✓ Data: {len(df)} records, {df["user_id"].nunique()} users')

# Book type mapping
book_type_mapping = {
    1: "Công nghệ giáo dục", 2: "Phương pháp giảng dạy", 3: "Công nghệ thông tin",
    4: "Thiết kế web", 5: "Lập trình", 6: "Nghiên cứu khoa học",
    7: "Giáo dục STEM", 8: "Giảng dạy tiếng Anh", 9: "Thiết kế",
    10: "Cơ sở dữ liệu", 11: "Phát triển ứng dụng", 12: "Công nghệ giáo dục"
}

df['book_type'] = df['product_id'].map(book_type_mapping)

print('\n⚙️  Creating features WITH book types...')

# Basic features
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

# Add book type features
print('   Adding book type features...')
for idx, row in user_behavior.iterrows():
    user_id = row['user_id']
    user_books = df[df['user_id'] == user_id]
    
    for book_type in set(book_type_mapping.values()):
        col_name = f'books_{book_type.lower().replace(" ", "_").replace("đ", "d")}'
        count = len(user_books[user_books['book_type'] == book_type])
        user_behavior.loc[idx, col_name] = count

# Encode categorical
le_income = LabelEncoder()
le_education = LabelEncoder()
user_behavior['income_encoded'] = le_income.fit_transform(user_behavior['income_level'])
user_behavior['education_encoded'] = le_education.fit_transform(user_behavior['education'])

# Prepare features
feature_columns_basic = ['total_actions', 'unique_products', 'total_spending', 
                         'avg_spending', 'age', 'income_encoded', 'education_encoded']

book_type_cols = [col for col in user_behavior.columns if col.startswith('books_')]
feature_columns_with_books = feature_columns_basic + book_type_cols

print(f'✓ Basic features: {len(feature_columns_basic)}')
print(f'✓ Book type features: {len(book_type_cols)}')
print(f'✓ TOTAL features: {len(feature_columns_with_books)}')

# Prepare data
X_basic = user_behavior[feature_columns_basic].fillna(0)
X_with_books = user_behavior[feature_columns_with_books].fillna(0)
y = user_behavior['is_potential']

print(f'\n✓ Potential: {y.sum()}/{len(y)} ({y.mean()*100:.1f}%)')

# Split
X_train_basic, X_test_basic, y_train, y_test = train_test_split(
    X_basic, y, test_size=0.2, random_state=42, stratify=y
)
X_train_books, X_test_books, _, _ = train_test_split(
    X_with_books, y, test_size=0.2, random_state=42, stratify=y
)

# Scale
scaler_basic = StandardScaler()
X_train_basic_scaled = scaler_basic.fit_transform(X_train_basic)
X_test_basic_scaled = scaler_basic.transform(X_test_basic)

scaler_books = StandardScaler()
X_train_books_scaled = scaler_books.fit_transform(X_train_books)
X_test_books_scaled = scaler_books.transform(X_test_books)

print(f'\nTrain: {len(X_train_basic)}, Test: {len(X_test_basic)}')

# Compare: Basic vs With Book Features
print('\n' + '=' * 70)
print('COMPARISON: BASIC vs WITH BOOK FEATURES')
print('=' * 70)

results = {}

# Test each model with both feature sets
models_to_test = {
    'SVM': lambda: SVC(probability=True, random_state=42),
    'Random Forest': lambda: RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42),
    'Gradient Boosting': lambda: GradientBoostingClassifier(n_estimators=100, learning_rate=0.05, 
                                                              max_depth=3, random_state=42)
}

print(f'\n{"Model":<20s} {"Basic (7)":<12s} {"+ Books ({len(feature_columns_with_books)})":<15s} {"Improvement":<15s}')
print('-' * 70)

for name, model_func in models_to_test.items():
    # Basic features
    model_basic = model_func()
    if name == 'SVM':
        model_basic.fit(X_train_basic_scaled, y_train)
        y_pred_basic = model_basic.predict(X_test_basic_scaled)
    else:
        model_basic.fit(X_train_basic, y_train)
        y_pred_basic = model_basic.predict(X_test_basic)
    
    f1_basic = f1_score(y_test, y_pred_basic)
    
    # With book features
    model_books = model_func()
    if name == 'SVM':
        model_books.fit(X_train_books_scaled, y_train)
        y_pred_books = model_books.predict(X_test_books_scaled)
    else:
        model_books.fit(X_train_books, y_train)
        y_pred_books = model_books.predict(X_test_books)
    
    f1_books = f1_score(y_test, y_pred_books)
    
    improvement = f1_books - f1_basic
    pct = (improvement / f1_basic) * 100
    
    results[name] = {
        'basic_f1': float(f1_basic),
        'books_f1': float(f1_books),
        'improvement': float(improvement),
        'improvement_pct': float(pct)
    }
    
    print(f'{name:<20s} {f1_basic:>7.4f}     {f1_books:>7.4f}         {improvement:>+6.4f} ({pct:>+6.2f}%)')

# Detailed metrics for best
print('\n' + '=' * 70)
print('DETAILED COMPARISON (Best Model)')
print('=' * 70)

best_name = max(results.keys(), key=lambda x: results[x]['books_f1'])
model_best = models_to_test[best_name]()

# Basic
if best_name == 'SVM':
    model_best.fit(X_train_basic_scaled, y_train)
    y_pred_basic = model_best.predict(X_test_basic_scaled)
else:
    model_best.fit(X_train_basic, y_train)
    y_pred_basic = model_best.predict(X_test_basic)

# With books
model_best_books = models_to_test[best_name]()
if best_name == 'SVM':
    model_best_books.fit(X_train_books_scaled, y_train)
    y_pred_books = model_best_books.predict(X_test_books_scaled)
else:
    model_best_books.fit(X_train_books, y_train)
    y_pred_books = model_best_books.predict(X_test_books)

print(f'\nModel: {best_name}')
print(f'\n{"Metric":<15s} {"Basic (7)":<12s} {"+ Books ({len(feature_columns_with_books)})":<15s} {"Change":<12s}')
print('-' * 60)
print(f'{"F1-Score":<15s} {f1_score(y_test, y_pred_basic):>7.4f}     {f1_score(y_test, y_pred_books):>7.4f}         {f1_score(y_test, y_pred_books) - f1_score(y_test, y_pred_basic):>+6.4f}')
print(f'{"Accuracy":<15s} {accuracy_score(y_test, y_pred_basic):>7.4f}     {accuracy_score(y_test, y_pred_books):>7.4f}         {accuracy_score(y_test, y_pred_books) - accuracy_score(y_test, y_pred_basic):>+6.4f}')
print(f'{"Precision":<15s} {precision_score(y_test, y_pred_basic):>7.4f}     {precision_score(y_test, y_pred_books):>7.4f}         {precision_score(y_test, y_pred_books) - precision_score(y_test, y_pred_basic):>+6.4f}')
print(f'{"Recall":<15s} {recall_score(y_test, y_pred_basic):>7.4f}     {recall_score(y_test, y_pred_books):>7.4f}         {recall_score(y_test, y_pred_books) - recall_score(y_test, y_pred_basic):>+6.4f}')

# Feature importance for RF
if best_name == 'Random Forest':
    print('\n' + '=' * 70)
    print('FEATURE IMPORTANCE (Random Forest with Book Types)')
    print('=' * 70)
    
    importance_df = pd.DataFrame({
        'feature': feature_columns_with_books,
        'importance': model_best_books.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f'\nTop 15 features:')
    print(importance_df.head(15).to_string(index=False))

# Summary
print('\n' + '=' * 70)
print('SUMMARY')
print('=' * 70)

best_basic = max(results.values(), key=lambda x: x['basic_f1'])['basic_f1']
best_books = max(results.values(), key=lambda x: x['books_f1'])['books_f1']
best_improvement = max(results.values(), key=lambda x: x['improvement'])

print(f'\nBest with basic features (7):  {best_basic:.4f}')
print(f'Best with book features ({len(feature_columns_with_books)}): {best_books:.4f}')
print(f'Improvement:                   +{(best_books - best_basic):.4f} ({((best_books - best_basic)/best_basic)*100:+.2f}%)')

if best_books > best_basic:
    print(f'\n✅ BOOK FEATURES HELP! Improvement: {((best_books - best_basic)/best_basic)*100:+.2f}%')
else:
    print(f'\n⚠️  No significant improvement from book features')

# Save results
import os
os.makedirs('defense_results/book_features', exist_ok=True)

book_features_results = {
    'feature_comparison': {
        'basic_features': feature_columns_basic,
        'book_type_features': book_type_cols,
        'total_features': len(feature_columns_with_books)
    },
    'results_by_model': results,
    'best_with_basic': float(best_basic),
    'best_with_books': float(best_books),
    'improvement': float(best_books - best_basic),
    'improvement_percent': float(((best_books - best_basic)/best_basic)*100)
}

with open('defense_results/book_features/book_features_results.json', 'w') as f:
    json.dump(book_features_results, f, indent=2)

# Save best model with book features
best_model_with_books = models_to_test[best_name]()
if best_name == 'SVM':
    best_model_with_books.fit(X_train_books_scaled, y_train)
    joblib.dump(scaler_books, 'defense_results/book_features/scaler_with_books.pkl')
else:
    best_model_with_books.fit(X_train_books, y_train)

joblib.dump(best_model_with_books, 'defense_results/book_features/model_with_books.pkl')

print('\n✅ Saved results to defense_results/book_features/')
print('   • model_with_books.pkl')
print('   • scaler_with_books.pkl (if SVM)')
print('   • book_features_results.json')

print('\n' + '=' * 70)
print('✨ BOOK FEATURES TEST COMPLETED!')
print('=' * 70)

