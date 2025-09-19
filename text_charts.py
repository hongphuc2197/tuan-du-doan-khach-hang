import os

print('📊 TẠO BIỂU ĐỒ DẠNG TEXT')
print('=' * 40)

# Tạo biểu đồ text cho Model Comparison
def create_text_chart():
    print('\n=== BIỂU ĐỒ SO SÁNH MÔ HÌNH ===')
    models = [
        ('Logistic Regression', 66.4),
        ('Random Forest', 67.2),
        ('Gradient Boosting', 66.4),
        ('SVM', 69.8)
    ]
    
    max_value = max([score for _, score in models])
    
    for model, score in models:
        bar_length = int((score / max_value) * 50)
        bar = '█' * bar_length
        print(f'{model:<20} {bar} {score}%')
    
    print(f'\n🏆 SVM có Accuracy cao nhất: 69.8%')

# Tạo biểu đồ text cho SVM Performance
def create_svm_chart():
    print('\n=== BIỂU ĐỒ HIỆU SUẤT SVM ===')
    metrics = [
        ('Accuracy', 69.8),
        ('Precision', 69.1),
        ('Recall', 91.5),
        ('F1-Score', 78.8)
    ]
    
    max_value = max([score for _, score in metrics])
    
    for metric, score in metrics:
        bar_length = int((score / max_value) * 50)
        bar = '█' * bar_length
        print(f'{metric:<12} {bar} {score}%')
    
    print(f'\n🎯 SVM có F1-Score cao nhất: 78.8%')

# Tạo biểu đồ text cho Dataset Overview
def create_dataset_chart():
    print('\n=== BIỂU ĐỒ TỔNG QUAN DATASET ===')
    data = [
        ('Total Records', 1813),
        ('Users', 576),
        ('View Events', 1274),
        ('Purchase Events', 539)
    ]
    
    max_value = max([value for _, value in data])
    
    for label, value in data:
        bar_length = int((value / max_value) * 50)
        bar = '█' * bar_length
        print(f'{label:<15} {bar} {value:,}')

# Tạo biểu đồ text cho Feature Importance
def create_feature_chart():
    print('\n=== BIỂU ĐỒ TẦM QUAN TRỌNG FEATURES ===')
    features = [
        ('total_spending', 32.5),
        ('avg_spending', 29.4),
        ('age', 16.0),
        ('unique_products', 6.9),
        ('total_actions', 6.8),
        ('education', 5.0),
        ('income', 3.5)
    ]
    
    max_value = max([score for _, score in features])
    
    for feature, score in features:
        bar_length = int((score / max_value) * 50)
        bar = '█' * bar_length
        print(f'{feature:<15} {bar} {score}%')
    
    print(f'\n💡 total_spending là feature quan trọng nhất: 32.5%')

# Tạo tất cả biểu đồ
create_text_chart()
create_svm_chart()
create_dataset_chart()
create_feature_chart()

# Lưu vào file text
with open('charts.txt', 'w', encoding='utf-8') as f:
    f.write('📊 BIỂU ĐỒ DỰ ÁN MACHINE LEARNING\n')
    f.write('=' * 50 + '\n\n')
    
    # Model Comparison
    f.write('=== SO SÁNH MÔ HÌNH ===\n')
    models = [
        ('Logistic Regression', 66.4),
        ('Random Forest', 67.2),
        ('Gradient Boosting', 66.4),
        ('SVM', 69.8)
    ]
    max_value = max([score for _, score in models])
    for model, score in models:
        bar_length = int((score / max_value) * 30)
        bar = '█' * bar_length
        f.write(f'{model:<20} {bar} {score}%\n')
    f.write('\n')
    
    # SVM Performance
    f.write('=== HIỆU SUẤT SVM ===\n')
    metrics = [
        ('Accuracy', 69.8),
        ('Precision', 69.1),
        ('Recall', 91.5),
        ('F1-Score', 78.8)
    ]
    max_value = max([score for _, score in metrics])
    for metric, score in metrics:
        bar_length = int((score / max_value) * 30)
        bar = '█' * bar_length
        f.write(f'{metric:<12} {bar} {score}%\n')
    f.write('\n')
    
    # Dataset Overview
    f.write('=== TỔNG QUAN DATASET ===\n')
    data = [
        ('Total Records', 1813),
        ('Users', 576),
        ('View Events', 1274),
        ('Purchase Events', 539)
    ]
    max_value = max([value for _, value in data])
    for label, value in data:
        bar_length = int((value / max_value) * 30)
        bar = '█' * bar_length
        f.write(f'{label:<15} {bar} {value:,}\n')
    f.write('\n')
    
    # Feature Importance
    f.write('=== TẦM QUAN TRỌNG FEATURES ===\n')
    features = [
        ('total_spending', 32.5),
        ('avg_spending', 29.4),
        ('age', 16.0),
        ('unique_products', 6.9),
        ('total_actions', 6.8),
        ('education', 5.0),
        ('income', 3.5)
    ]
    max_value = max([score for _, score in features])
    for feature, score in features:
        bar_length = int((score / max_value) * 30)
        bar = '█' * bar_length
        f.write(f'{feature:<15} {bar} {score}%\n')

print('\n✅ Đã tạo file: charts.txt')
print('🎉 Hoàn thành tạo biểu đồ!')
