#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Statistical Analysis & Validation cho đồ án thạc sĩ
- Statistical significance testing
- Confidence intervals
- Effect size analysis
- Model validation
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import warnings
warnings.filterwarnings('ignore')

print('=' * 70)
print('STATISTICAL ANALYSIS & VALIDATION')
print('=' * 70)

# Load data and model
df = pd.read_csv('../user_actions_students_576.csv')
model = joblib.load('advanced_best_model.pkl')
scaler = joblib.load('advanced_scaler.pkl')

print('✅ Loaded data and model')

# 1. DESCRIPTIVE STATISTICS
print('\n' + '=' * 70)
print('1. DESCRIPTIVE STATISTICS')
print('=' * 70)

# Basic statistics
print(f'Dataset size: {len(df)} records, {df["user_id"].nunique()} users')
print(f'Target distribution: {df.groupby("user_id")["event_type"].apply(lambda x: "purchase" in x.values).value_counts()}')

# Age statistics
age_stats = df.groupby('user_id')['age'].first()
print(f'\nAge statistics:')
print(f'Mean: {age_stats.mean():.2f}')
print(f'Median: {age_stats.median():.2f}')
print(f'Std: {age_stats.std():.2f}')
print(f'Min: {age_stats.min()}')
print(f'Max: {age_stats.max()}')

# Income statistics
income_stats = df.groupby('user_id')['income'].first()
print(f'\nIncome statistics:')
print(f'Mean: {income_stats.mean():,.0f} VNĐ')
print(f'Median: {income_stats.median():,.0f} VNĐ')
print(f'Std: {income_stats.std():,.0f} VNĐ')

# 2. STATISTICAL SIGNIFICANCE TESTING
print('\n' + '=' * 70)
print('2. STATISTICAL SIGNIFICANCE TESTING')
print('=' * 70)

# Prepare features (simplified version)
user_behavior = df.groupby('user_id').agg({
    'event_type': lambda x: 'purchase' in x.values,
    'product_id': 'nunique',
    'price': ['sum', 'mean'],
    'age': 'first',
    'income': 'first'
}).reset_index()

user_behavior.columns = ['user_id', 'is_potential', 'unique_products', 'total_spending', 'avg_spending', 'age', 'income']
user_behavior['total_actions'] = df.groupby('user_id')['event_type'].count().values

# Chi-square test for categorical variables
print('--- Chi-square Tests ---')

# Age groups vs potential
age_groups = pd.cut(user_behavior['age'], bins=[17, 20, 23, 26], labels=['18-20', '21-23', '24-25'])
contingency_age = pd.crosstab(age_groups, user_behavior['is_potential'])
chi2_age, p_age = stats.chi2_contingency(contingency_age)[:2]
print(f'Age groups vs potential: χ² = {chi2_age:.4f}, p = {p_age:.4f}')

# Income groups vs potential
income_groups = pd.cut(user_behavior['income'], bins=[0, 2000000, 4000000, float('inf')], labels=['Low', 'Medium', 'High'])
contingency_income = pd.crosstab(income_groups, user_behavior['is_potential'])
chi2_income, p_income = stats.chi2_contingency(contingency_income)[:2]
print(f'Income groups vs potential: χ² = {chi2_income:.4f}, p = {p_income:.4f}')

# T-tests for continuous variables
print('\n--- T-tests ---')

potential_customers = user_behavior[user_behavior['is_potential'] == True]
non_potential = user_behavior[user_behavior['is_potential'] == False]

# Age t-test
t_age, p_age_ttest = stats.ttest_ind(potential_customers['age'], non_potential['age'])
print(f'Age t-test: t = {t_age:.4f}, p = {p_age_ttest:.4f}')

# Income t-test
t_income, p_income_ttest = stats.ttest_ind(potential_customers['income'], non_potential['income'])
print(f'Income t-test: t = {t_income:.4f}, p = {p_income_ttest:.4f}')

# Spending t-test
t_spending, p_spending = stats.ttest_ind(potential_customers['total_spending'], non_potential['total_spending'])
print(f'Spending t-test: t = {t_spending:.4f}, p = {p_spending:.4f}')

# 3. EFFECT SIZE ANALYSIS
print('\n' + '=' * 70)
print('3. EFFECT SIZE ANALYSIS')
print('=' * 70)

# Cohen's d for continuous variables
def cohens_d(group1, group2):
    """Calculate Cohen's d effect size"""
    n1, n2 = len(group1), len(group2)
    s1, s2 = group1.std(ddof=1), group2.std(ddof=1)
    s_pooled = np.sqrt(((n1-1)*s1**2 + (n2-1)*s2**2) / (n1+n2-2))
    return (group1.mean() - group2.mean()) / s_pooled

# Effect sizes
d_age = cohens_d(potential_customers['age'], non_potential['age'])
d_income = cohens_d(potential_customers['income'], non_potential['income'])
d_spending = cohens_d(potential_customers['total_spending'], non_potential['total_spending'])

print(f'Cohen\'s d - Age: {d_age:.4f}')
print(f'Cohen\'s d - Income: {d_income:.4f}')
print(f'Cohen\'s d - Spending: {d_spending:.4f}')

# Effect size interpretation
def interpret_effect_size(d):
    if abs(d) < 0.2:
        return "negligible"
    elif abs(d) < 0.5:
        return "small"
    elif abs(d) < 0.8:
        return "medium"
    else:
        return "large"

print(f'\nEffect size interpretations:')
print(f'Age: {interpret_effect_size(d_age)}')
print(f'Income: {interpret_effect_size(d_income)}')
print(f'Spending: {interpret_effect_size(d_spending)}')

# 4. CONFIDENCE INTERVALS
print('\n' + '=' * 70)
print('4. CONFIDENCE INTERVALS')
print('=' * 70)

# Confidence intervals for means
def confidence_interval(data, confidence=0.95):
    """Calculate confidence interval for mean"""
    n = len(data)
    mean = data.mean()
    std_err = stats.sem(data)
    h = std_err * stats.t.ppf((1 + confidence) / 2, n-1)
    return mean - h, mean + h

# CI for potential customers
age_ci_potential = confidence_interval(potential_customers['age'])
income_ci_potential = confidence_interval(potential_customers['income'])
spending_ci_potential = confidence_interval(potential_customers['total_spending'])

print(f'Potential customers - Age CI (95%): [{age_ci_potential[0]:.2f}, {age_ci_potential[1]:.2f}]')
print(f'Potential customers - Income CI (95%): [{income_ci_potential[0]:,.0f}, {income_ci_potential[1]:,.0f}]')
print(f'Potential customers - Spending CI (95%): [{spending_ci_potential[0]:,.0f}, {spending_ci_potential[1]:,.0f}]')

# 5. MODEL VALIDATION
print('\n' + '=' * 70)
print('5. MODEL VALIDATION')
print('=' * 70)

# Prepare features for validation
from sklearn.preprocessing import LabelEncoder
le_income = LabelEncoder()
le_education = LabelEncoder()

user_behavior['income_encoded'] = le_income.fit_transform(user_behavior['income_level'])
user_behavior['education_encoded'] = le_education.fit_transform(user_behavior['education'])

feature_columns = ['total_actions', 'unique_products', 'total_spending', 'avg_spending', 'age', 'income_encoded', 'education_encoded']
X = user_behavior[feature_columns].fillna(0)
y = user_behavior['is_potential']

# Cross-validation
cv_scores = cross_val_score(model, scaler.fit_transform(X), y, cv=10, scoring='f1')
print(f'Cross-validation F1 scores: {cv_scores}')
print(f'Mean CV F1: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})')

# Bootstrap confidence interval for model performance
def bootstrap_ci(model, X, y, n_bootstrap=1000, confidence=0.95):
    """Bootstrap confidence interval for model performance"""
    scores = []
    for _ in range(n_bootstrap):
        # Bootstrap sample
        indices = np.random.choice(len(X), len(X), replace=True)
        X_boot, y_boot = X.iloc[indices], y.iloc[indices]
        
        # Train and test
        X_boot_scaled = scaler.fit_transform(X_boot)
        model.fit(X_boot_scaled, y_boot)
        
        # Test on original data
        X_scaled = scaler.transform(X)
        y_pred = model.predict(X_scaled)
        from sklearn.metrics import f1_score
        score = f1_score(y, y_pred)
        scores.append(score)
    
    return np.percentile(scores, [(1-confidence)/2*100, (1+confidence)/2*100])

# Bootstrap CI for F1-score
f1_ci = bootstrap_ci(model, X, y)
print(f'Bootstrap F1 CI (95%): [{f1_ci[0]:.4f}, {f1_ci[1]:.4f}]')

# 6. STATISTICAL POWER ANALYSIS
print('\n' + '=' * 70)
print('6. STATISTICAL POWER ANALYSIS')
print('=' * 70)

# Power analysis for t-test
from statsmodels.stats.power import ttest_power

# Effect size for age
effect_size_age = abs(d_age)
n = len(user_behavior)
power_age = ttest_power(effect_size_age, n, alpha=0.05)
print(f'Statistical power for age difference: {power_age:.4f}')

# Effect size for income
effect_size_income = abs(d_income)
power_income = ttest_power(effect_size_income, n, alpha=0.05)
print(f'Statistical power for income difference: {power_income:.4f}')

# 7. CORRELATION ANALYSIS
print('\n' + '=' * 70)
print('7. CORRELATION ANALYSIS')
print('=' * 70)

# Correlation matrix
correlation_data = user_behavior[['age', 'income', 'total_spending', 'total_actions', 'unique_products']]
correlation_matrix = correlation_data.corr()

print('Correlation matrix:')
print(correlation_matrix.round(3))

# Significant correlations
from scipy.stats import pearsonr

print('\nSignificant correlations (p < 0.05):')
for i in range(len(correlation_data.columns)):
    for j in range(i+1, len(correlation_data.columns)):
        col1, col2 = correlation_data.columns[i], correlation_data.columns[j]
        corr, p_val = pearsonr(correlation_data[col1], correlation_data[col2])
        if p_val < 0.05:
            print(f'{col1} vs {col2}: r = {corr:.3f}, p = {p_val:.4f}')

# 8. SAVE RESULTS
print('\n' + '=' * 70)
print('8. SAVING RESULTS')
print('=' * 70)

# Save statistical results
statistical_results = {
    'descriptive_stats': {
        'n_users': len(user_behavior),
        'age_mean': age_stats.mean(),
        'income_mean': income_stats.mean(),
        'potential_rate': user_behavior['is_potential'].mean()
    },
    'significance_tests': {
        'age_chi2': chi2_age,
        'age_p': p_age,
        'income_chi2': chi2_income,
        'income_p': p_income,
        'age_t': t_age,
        'age_t_p': p_age_ttest,
        'income_t': t_income,
        'income_t_p': p_income_ttest
    },
    'effect_sizes': {
        'age_cohens_d': d_age,
        'income_cohens_d': d_income,
        'spending_cohens_d': d_spending
    },
    'confidence_intervals': {
        'age_ci': age_ci_potential,
        'income_ci': income_ci_potential,
        'spending_ci': spending_ci_potential
    },
    'model_validation': {
        'cv_f1_mean': cv_scores.mean(),
        'cv_f1_std': cv_scores.std(),
        'bootstrap_f1_ci': f1_ci
    }
}

import json
with open('statistical_analysis_results.json', 'w') as f:
    json.dump(statistical_results, f, indent=2)

print('✅ Statistical analysis completed and saved!')
print('Results saved to: statistical_analysis_results.json')

print('\n✨ STATISTICAL VALIDATION COMPLETED!')
print('Ready for master thesis statistical requirements!')
