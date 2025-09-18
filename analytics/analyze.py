import pandas as pd
import numpy as np
import json
import warnings
warnings.filterwarnings('ignore')

def analyze_data():
    # Đọc kết quả từ file CSV
    results_df = pd.read_csv('../model_results.csv')
    
    # Đọc dữ liệu gốc
    df = pd.read_csv('../marketing_campaign.csv', sep='\t')
    df['Age'] = 2024 - df['Year_Birth']
    
    # 1. Phân tích phân khúc khách hàng theo độ tuổi
    age_segments = pd.cut(df['Age'], 
                         bins=[0, 30, 40, 50, 60, 100],
                         labels=['<30', '30-40', '40-50', '50-60', '>60'])
    age_distribution = age_segments.value_counts().sort_index()
    
    # 2. Phân tích theo trình độ học vấn
    education_stats = df.groupby('Education')['Response'].agg(['count', 'mean']).reset_index()
    education_stats['potential_rate'] = education_stats['mean'] * 100
    education_stats = education_stats.sort_values('potential_rate', ascending=False)
    
    # 3. Phân tích theo tình trạng hôn nhân
    marital_stats = df.groupby('Marital_Status')['Response'].agg(['count', 'mean']).reset_index()
    marital_stats['potential_rate'] = marital_stats['mean'] * 100
    marital_stats = marital_stats.sort_values('potential_rate', ascending=False)
    
    # 4. Phân tích theo thu nhập
    income_segments = pd.qcut(df['Income'], q=5, labels=['Rất thấp', 'Thấp', 'Trung bình', 'Cao', 'Rất cao'])
    income_stats = df.groupby(income_segments)['Response'].agg(['count', 'mean']).reset_index()
    income_stats['potential_rate'] = income_stats['mean'] * 100
    
    # 5. Phân tích chi tiêu theo nhóm sản phẩm
    spending_cols = ['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 
                    'MntSweetProducts', 'MntGoldProds']
    spending_stats = df[spending_cols].agg(['mean', 'median', 'max']).round(2)
    
    # 6. Phân tích kênh mua hàng
    channel_cols = ['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases']
    channel_stats = df[channel_cols].agg(['mean', 'median', 'max']).round(2)
    
    # 7. Phân tích tương tác
    interaction_stats = df.groupby('Response').agg({
        'NumWebVisitsMonth': ['mean', 'median', 'max'],
        'NumDealsPurchases': ['mean', 'median', 'max']
    }).round(2)
    
    # Lấy kết quả của mô hình tốt nhất
    best_model_results = results_df.loc[results_df['F1-score'].idxmax()]
    
    # Tạo kết quả JSON
    result = {
        'potentialCustomers': int(sum(df['Response'] == 1)),
        'nonPotentialCustomers': int(sum(df['Response'] == 0)),
        'modelPerformance': {
            'model': best_model_results['Model'],
            'accuracy': float(best_model_results['Accuracy']),
            'precision': float(best_model_results['Precision']),
            'recall': float(best_model_results['Recall']),
            'f1Score': float(best_model_results['F1-score']),
            'cvMean': float(best_model_results['CV Mean']),
            'cvStd': float(best_model_results['CV Std'])
        },
        'demographics': {
            'ageSegments': [
                {'name': age, 'count': int(count)} 
                for age, count in age_distribution.items()
            ],
            'education': education_stats.to_dict('records'),
            'maritalStatus': marital_stats.to_dict('records'),
            'income': income_stats.to_dict('records')
        },
        'spending': {
            'byProduct': spending_stats.to_dict(),
            'byChannel': channel_stats.to_dict()
        },
        'interactions': {
            'webVisits': interaction_stats['NumWebVisitsMonth'].to_dict(),
            'dealPurchases': interaction_stats['NumDealsPurchases'].to_dict()
        }
    }
    
    return result

if __name__ == '__main__':
    try:
        result = analyze_data()
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({'error': str(e)})) 