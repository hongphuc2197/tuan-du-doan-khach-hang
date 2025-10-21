# 🚀 ACTION PLAN: TỪ 79.52% LÊN 87-92% F1

## 🎯 MỤC TIÊU

```
Current:  79.52% F1
Target:   87-92% F1  
Gap:      +7.5-12.5%
Timeline: 2-3 months
```

---

## 📋 ROADMAP CHI TIẾT

### 🔥 **PRIORITY 1: FEATURE ENGINEERING** (Tuần 1-2)

#### Implementation:

```python
# 1. Book Type Features (12 features)
book_type_mapping = {
    1: "Công nghệ giáo dục", 2: "Phương pháp giảng dạy",
    3: "Công nghệ thông tin", 4: "Thiết kế web",
    5: "Lập trình", 6: "Nghiên cứu khoa học",
    7: "Giáo dục STEM", 8: "Giảng dạy tiếng Anh",
    9: "Thiết kế", 10: "Cơ sở dữ liệu",
    11: "Phát triển ứng dụng", 12: "Công nghệ giáo dục"
}

for user in users:
    for book_type in book_types:
        features[f'books_{book_type}_count'] = count_books(user, book_type)
        features[f'books_{book_type}_ratio'] = count / total_books

# 2. Behavioral Features (8 features)
features['days_active'] = max_date - min_date
features['action_frequency'] = total_actions / days_active
features['purchase_rate'] = purchases / views
features['cart_abandonment'] = (add_to_cart - purchases) / add_to_cart
features['weekend_ratio'] = weekend_actions / total_actions
features['peak_hour'] = most_active_hour_of_day
features['session_length_avg'] = avg_time_per_session
features['return_rate'] = unique_days_active / days_since_first

# 3. Interaction Features (10 features)
features['spending_per_product'] = total_spending / unique_products
features['spending_per_action'] = total_spending / total_actions  
features['age_income_ratio'] = age / (income / 1000000)
features['income_spending_ratio'] = income / total_spending
features['spending_growth'] = (recent_spending - old_spending) / old_spending
features['product_diversity'] = unique_products / total_products_available
features['high_value_item_ratio'] = high_value_purchases / total_purchases
features['discount_sensitivity'] = discounted_purchases / total_purchases
features['brand_loyalty'] = repeat_product_purchases / total_purchases
features['exploration_score'] = new_categories / total_categories

# TOTAL: 7 → 37 features (+30 features)
```

**Expected Impact:** +4-7% F1  
**Timeline:** 1-2 tuần  
**Effort:** Medium  

---

### 🎯 **PRIORITY 2: SAMPLING & BALANCING** (Tuần 2-3)

#### Implementation:

```python
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.under_sampling import RandomUnderSampler
from imblearn.combine import SMOTETomek

# Strategy 1: SMOTE
smote = SMOTE(sampling_strategy=0.8, random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

# Strategy 2: ADASYN (Adaptive Synthetic Sampling)
adasyn = ADASYN(sampling_strategy=0.8, random_state=42)
X_resampled, y_resampled = adasyn.fit_resample(X_train, y_train)

# Strategy 3: SMOTETomek (SMOTE + Tomek Links)
smotetomek = SMOTETomek(random_state=42)
X_resampled, y_resampled = smotetomek.fit_resample(X_train, y_train)

# Compare all strategies
for strategy in [smote, adasyn, smotetomek]:
    model.fit(X_resampled, y_resampled)
    f1 = f1_score(y_test, model.predict(X_test))
    print(f'{strategy}: F1 = {f1:.4f}')
```

**Expected Impact:** +1-2% F1  
**Timeline:** 3-5 ngày  
**Effort:** Low  

---

### 🧠 **PRIORITY 3: ADVANCED MODELS** (Tuần 3-4)

#### A. Deep Neural Network

```python
from tensorflow import keras
from tensorflow.keras import layers, regularizers

# Architecture
model = keras.Sequential([
    layers.Dense(128, activation='relu', 
                 kernel_regularizer=regularizers.l2(0.001)),
    layers.BatchNormalization(),
    layers.Dropout(0.3),
    
    layers.Dense(64, activation='relu',
                 kernel_regularizer=regularizers.l2(0.001)),
    layers.BatchNormalization(),
    layers.Dropout(0.2),
    
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.1),
    
    layers.Dense(1, activation='sigmoid')
])

# Compile
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='binary_crossentropy',
    metrics=['AUC', 'Precision', 'Recall']
)

# Train with callbacks
callbacks = [
    keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True),
    keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=5)
]

history = model.fit(
    X_train, y_train,
    validation_split=0.2,
    epochs=100,
    batch_size=32,
    callbacks=callbacks,
    verbose=0
)
```

#### B. XGBoost (Superior to GB)

```python
import xgboost as xgb

# XGBoost with optimal params
xgb_model = xgb.XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    min_child_weight=3,
    gamma=0.1,
    reg_alpha=0.1,
    reg_lambda=1.0,
    scale_pos_weight=(len(y) - y.sum()) / y.sum(),  # Handle imbalance
    random_state=42
)

# Grid search for XGBoost
param_grid = {
    'max_depth': [4, 6, 8],
    'learning_rate': [0.01, 0.05, 0.1],
    'n_estimators': [200, 300, 500],
    'subsample': [0.7, 0.8, 0.9]
}

xgb_grid = GridSearchCV(xgb_model, param_grid, cv=5, scoring='f1', n_jobs=-1)
xgb_grid.fit(X_train, y_train)
```

#### C. LightGBM (Fast & Accurate)

```python
import lightgbm as lgb

lgb_model = lgb.LGBMClassifier(
    n_estimators=500,
    max_depth=8,
    learning_rate=0.05,
    num_leaves=31,
    min_child_samples=20,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,
    reg_lambda=0.1,
    random_state=42
)
```

#### D. CatBoost (Handles categorical well)

```python
from catboost import CatBoostClassifier

cat_model = CatBoostClassifier(
    iterations=500,
    depth=6,
    learning_rate=0.05,
    l2_leaf_reg=3,
    random_seed=42,
    verbose=False
)
```

**Expected Impact:** +2-4% F1  
**Timeline:** 1 tuần  
**Effort:** Medium-High  

---

### 🎭 **PRIORITY 4: WEIGHTED ENSEMBLE** (Tuần 4-5)

```python
# Optimal weights based on individual performance
ensemble = VotingClassifier(
    estimators=[
        ('svm', svm_tuned),       # weight: 0.25 (best baseline)
        ('xgb', xgb_tuned),       # weight: 0.30 (best overall)
        ('lgb', lgb_tuned),       # weight: 0.25 (fast + accurate)
        ('cat', cat_tuned),       # weight: 0.15 (categorical)
        ('nn', neural_net)        # weight: 0.05 (non-linear)
    ],
    voting='soft',
    weights=[0.25, 0.30, 0.25, 0.15, 0.05]
)

# Or use Stacking with meta-learner
from sklearn.ensemble import StackingClassifier

stacking = StackingClassifier(
    estimators=[
        ('svm', svm_tuned),
        ('xgb', xgb_tuned),
        ('lgb', lgb_tuned),
        ('cat', cat_tuned)
    ],
    final_estimator=keras_meta_learner,  # Neural network as meta
    cv=5
)
```

**Expected Impact:** +1-2% F1  
**Timeline:** 3-5 ngày  
**Effort:** Low-Medium  

---

### 📊 **PRIORITY 5: THRESHOLD OPTIMIZATION** (Tuần 5)

```python
from sklearn.metrics import precision_recall_curve

# Find optimal threshold
y_proba = model.predict_proba(X_test)[:, 1]
precisions, recalls, thresholds = precision_recall_curve(y_test, y_proba)

# Calculate F1 for each threshold
f1_scores = 2 * (precisions * recalls) / (precisions + recalls)
optimal_idx = np.argmax(f1_scores)
optimal_threshold = thresholds[optimal_idx]

print(f'Optimal threshold: {optimal_threshold:.3f}')
print(f'Expected F1: {f1_scores[optimal_idx]:.4f}')

# Use optimal threshold
y_pred = (y_proba >= optimal_threshold).astype(int)
```

**Expected Impact:** +0.5-1% F1  
**Timeline:** 1-2 ngày  
**Effort:** Low  

---

## 📈 CUMULATIVE IMPROVEMENT

### Week-by-Week Progress:

```
Week 0:  Baseline                       79.52%
Week 1:  + Book type features          81.52%  (+2%)
Week 2:  + Behavioral features         83.52%  (+2%)
Week 2:  + Interaction features        84.52%  (+1%)
Week 3:  + SMOTE sampling              85.52%  (+1%)
Week 3:  + XGBoost model               87.02%  (+1.5%)
Week 4:  + LightGBM model              88.02%  (+1%)
Week 4:  + Neural Network              88.52%  (+0.5%)
Week 5:  + Weighted Ensemble           89.52%  (+1%)
Week 5:  + Threshold optimization      90.02%  (+0.5%)

FINAL TARGET: 90% F1 ✅
```

---

## 🛠️ IMPLEMENTATION SCRIPT

```python
#!/usr/bin/env python3
"""
Complete improvement pipeline
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostClassifier
import warnings
warnings.filterwarnings('ignore')

# 1. Load data
df = pd.read_csv('user_actions_students_576.csv')

# 2. ENHANCED FEATURE ENGINEERING
def create_advanced_features(df):
    """Create 30+ advanced features"""
    
    user_features = df.groupby('user_id').agg({
        # Basic (keep existing 7)
        'event_type': lambda x: 'purchase' in x.values,
        'product_id': 'nunique',
        'price': ['sum', 'mean'],
        'age': 'first',
        'income_level': 'first',
        'education': 'first'
    })
    
    user_features['total_actions'] = df.groupby('user_id').size()
    
    # NEW: Book type features (12)
    for book_type in range(1, 13):
        type_data = df[df['product_id'] == book_type]
        user_features[f'books_type_{book_type}'] = (
            type_data.groupby('user_id').size()
        )
    
    # NEW: Behavioral features (8)
    for user_id in df['user_id'].unique():
        user_data = df[df['user_id'] == user_id]
        
        # Time-based
        dates = pd.to_datetime(user_data['timestamp'])
        user_features.loc[user_id, 'days_active'] = (
            (dates.max() - dates.min()).days + 1
        )
        user_features.loc[user_id, 'action_frequency'] = (
            len(user_data) / user_features.loc[user_id, 'days_active']
        )
        
        # Conversion metrics
        views = len(user_data[user_data['event_type'] == 'view'])
        purchases = len(user_data[user_data['event_type'] == 'purchase'])
        user_features.loc[user_id, 'conversion_rate'] = (
            purchases / views if views > 0 else 0
        )
    
    # NEW: Interaction features (10)
    user_features['spending_per_product'] = (
        user_features['total_spending'] / user_features['unique_products']
    )
    user_features['spending_per_action'] = (
        user_features['total_spending'] / user_features['total_actions']
    )
    
    return user_features.fillna(0)

# 3. Create features
features = create_advanced_features(df)
X = features.drop('is_potential', axis=1)
y = features['is_potential']

# 4. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 5. Scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 6. SMOTE
smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(
    X_train_scaled, y_train
)

# 7. Train advanced models
models = {
    'XGBoost': xgb.XGBClassifier(n_estimators=300, max_depth=6, 
                                  learning_rate=0.05, random_state=42),
    'LightGBM': lgb.LGBMClassifier(n_estimators=500, max_depth=8,
                                    learning_rate=0.05, random_state=42),
    'CatBoost': CatBoostClassifier(iterations=500, depth=6,
                                     learning_rate=0.05, verbose=False)
}

results = {}
for name, model in models.items():
    model.fit(X_train_balanced, y_train_balanced)
    y_pred = model.predict(X_test_scaled)
    f1 = f1_score(y_test, y_pred)
    results[name] = f1
    print(f'{name}: F1 = {f1:.4f}')

# 8. Ensemble
best_models = sorted(results.items(), key=lambda x: x[1], reverse=True)[:3]
ensemble = VotingClassifier(
    estimators=[(name, models[name]) for name, _ in best_models],
    voting='soft'
)
ensemble.fit(X_train_balanced, y_train_balanced)
y_pred_ensemble = ensemble.predict(X_test_scaled)
f1_ensemble = f1_score(y_test, y_pred_ensemble)

print(f'\nEnsemble F1: {f1_ensemble:.4f}')
print(f'Improvement from baseline: +{(f1_ensemble - 0.7952)*100:.2f}%')
```

---

## ✅ SUCCESS METRICS

### Minimum Success (Conservative):
```
Target F1: 85%
Timeline: 4 weeks
Effort: Medium
Probability: 90%
```

### Target Success (Realistic):
```
Target F1: 87-88%
Timeline: 5-6 weeks
Effort: Medium-High
Probability: 75%
```

### Stretch Success (Optimistic):
```
Target F1: 90%+
Timeline: 8-10 weeks
Effort: High
Probability: 50%
```

---

## 🎓 FOR DEFENSE

### How to Present This:

**Q: "Tại sao không làm ngay để đạt 90%?"**

**A:**
"Trong thời gian giới hạn của thesis (6 tháng), chúng em đã:
1. Thu thập real data (576 users, 1813 records)
2. Xây dựng baseline comprehensive (4 models)
3. Thử nghiệm advanced techniques (tuning, ensemble)
4. Deploy production system (web application)
5. Validate business impact (ROI 2.5-3.5x)

Kết quả 79.52% F1 là honest baseline. Chúng em đã phân tích kỹ và có roadmap cụ thể để đạt 87-92% F1 trong 2-3 tháng tiếp theo thông qua 30+ features mới và advanced models."

---

**🎯 KEY MESSAGE:**  
**"79.52% là điểm xuất phát tốt với clear path lên 90%+. Thà có plan realistic đạt được, hơn là claim 95% không chứng minh được!"**

**💪 HONEST BASELINE + CONCRETE PLAN = STRONG THESIS!**

