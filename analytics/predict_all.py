import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import joblib
from datetime import datetime

def load_and_preprocess_data(file_path='marketing_campaign.csv'):
    # Đọc dữ liệu
    df = pd.read_csv(file_path, sep='\t')
    
    # Xử lý missing values
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    imputer = SimpleImputer(strategy='mean')
    df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
    
    # Tính tuổi từ năm sinh
    current_year = datetime.now().year
    df['Age'] = current_year - df['Year_Birth']
    
    # Tính tổng chi tiêu
    spending_cols = ['MntWines', 'MntFruits', 'MntMeatProducts', 
                    'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
    df['TotalSpending'] = df[spending_cols].sum(axis=1)
    
    # Tính tỷ lệ chi tiêu theo từng danh mục
    for col in spending_cols:
        df[f'{col}_Ratio'] = df[col] / df['TotalSpending']
    
    # Tính tổng số lượng mua hàng
    purchase_cols = ['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases']
    df['TotalPurchases'] = df[purchase_cols].sum(axis=1)
    
    # Tính chi tiêu trung bình mỗi lần mua
    df['AvgPurchaseValue'] = df['TotalSpending'] / df['TotalPurchases']
    
    # Tính tỷ lệ mua hàng theo kênh
    for col in purchase_cols:
        df[f'{col}_Ratio'] = df[col] / df['TotalPurchases']
    
    # Tính tỷ lệ mua hàng theo kênh
    df['WebPurchaseRatio'] = df['NumWebPurchases'] / df['TotalPurchases']
    df['CatalogPurchaseRatio'] = df['NumCatalogPurchases'] / df['TotalPurchases']
    df['StorePurchaseRatio'] = df['NumStorePurchases'] / df['TotalPurchases']
    
    # Chọn các features quan trọng đã được xác định
    features = ['Year_Birth', 'Income', 'Kidhome', 'Teenhome', 'Recency',
                'MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts',
                'MntSweetProducts', 'MntGoldProds', 'NumDealsPurchases',
                'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases',
                'NumWebVisitsMonth']
    
    X = df[features]
    
    # Load scaler đã được tối ưu
    scaler = joblib.load('optimized_scaler.pkl')
    
    # Chuẩn hóa dữ liệu
    X_scaled = scaler.transform(X)
    
    return df, X_scaled

def analyze_customer_segments(potential_customers):
    # Phân tích phân khúc độ tuổi
    age_segments = pd.cut(potential_customers['Age'], 
                         bins=[0, 30, 40, 50, 60, 100],
                         labels=['<30', '30-40', '40-50', '50-60', '>60'])
    age_distribution = age_segments.value_counts().sort_index()
    
    # Phân tích phân khúc thu nhập
    income_segments = pd.qcut(potential_customers['Income'], q=4, 
                            labels=['Low', 'Medium', 'High', 'Very High'])
    income_distribution = income_segments.value_counts().sort_index()
    
    # Phân tích theo trạng thái gia đình
    potential_customers['HasChildren'] = (potential_customers['Kidhome'] + potential_customers['Teenhome']) > 0
    family_distribution = potential_customers['HasChildren'].value_counts()
    
    # Phân tích phân khúc chi tiêu
    spending_segments = pd.qcut(potential_customers['TotalSpending'], q=4, labels=['Low', 'Medium', 'High', 'Premium'])
    spending_distribution = spending_segments.value_counts().sort_index()
    
    return {
        'age_distribution': age_distribution,
        'income_distribution': income_distribution,
        'family_distribution': family_distribution,
        'spending_distribution': spending_distribution
    }

def analyze_spending_patterns(customers):
    # Phân tích chi tiêu theo danh mục
    spending_cols = ['MntWines', 'MntFruits', 'MntMeatProducts', 
                    'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
    
    spending_patterns = {}
    
    # Tính tổng chi tiêu theo danh mục
    total_spending = customers[spending_cols].sum()
    spending_patterns['total_by_category'] = total_spending.sort_values(ascending=False)
    
    # Tính tỷ lệ trung bình chi tiêu theo danh mục
    ratio_cols = [col + '_Ratio' for col in spending_cols]
    avg_ratios = customers[ratio_cols].mean() * 100
    spending_patterns['avg_category_ratios'] = avg_ratios.sort_values(ascending=False)
    
    # Phân tích kênh mua hàng
    channel_cols = ['WebPurchaseRatio', 'CatalogPurchaseRatio', 'StorePurchaseRatio']
    channel_ratios = customers[channel_cols].mean() * 100
    spending_patterns['channel_ratios'] = channel_ratios
    
    # Phân tích recency
    recency_segments = pd.qcut(customers['Recency'], q=4, 
                             labels=['Very Recent', 'Recent', 'Less Recent', 'Not Recent'])
    spending_patterns['recency_distribution'] = recency_segments.value_counts().sort_index()
    
    return spending_patterns

def analyze_top_customers(potential_customers, n=10):
    """Phân tích chi tiết top n khách hàng tiềm năng"""
    top_n = potential_customers.nlargest(n, 'TotalSpending')
    
    # Tính tỷ lệ chi tiêu theo danh mục cho top n khách hàng
    spending_cols = ['MntWines', 'MntFruits', 'MntMeatProducts', 
                    'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
    
    for col in spending_cols:
        top_n[f'{col}_Percentage'] = (top_n[col] / top_n['TotalSpending'] * 100).round(2)
    
    # Tính tỷ lệ sử dụng các kênh mua hàng
    top_n['WebRatio'] = (top_n['NumWebPurchases'] / top_n['TotalPurchases'] * 100).round(2)
    top_n['CatalogRatio'] = (top_n['NumCatalogPurchases'] / top_n['TotalPurchases'] * 100).round(2)
    top_n['StoreRatio'] = (top_n['NumStorePurchases'] / top_n['TotalPurchases'] * 100).round(2)
    
    return top_n

def predict_potential_customers():
    # Load model đã được tối ưu
    best_model = joblib.load('optimized_model.pkl')
    
    # Load và tiền xử lý dữ liệu
    df, X_scaled = load_and_preprocess_data()
    
    # Dự đoán
    predictions = best_model.predict(X_scaled)
    probabilities = best_model.predict_proba(X_scaled)[:, 1]
    
    # Thêm kết quả vào DataFrame
    df['IsPotentialCustomer'] = predictions
    df['PredictionProbability'] = probabilities
    
    # Lọc ra các khách hàng tiềm năng
    potential_customers = df[df['IsPotentialCustomer'] == 1].copy()
    
    # Sắp xếp theo xác suất giảm dần
    potential_customers = potential_customers.sort_values('PredictionProbability', ascending=False)
    
    # Chọn các cột quan trọng để xuất ra
    columns_to_save = [
        'ID', 'Age', 'Income', 'Recency', 
        'TotalSpending', 'AvgPurchaseValue',
        'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases',
        'NumWebVisitsMonth', 'NumDealsPurchases',
        'MntWines', 'MntFruits', 'MntMeatProducts',
        'MntFishProducts', 'MntSweetProducts', 'MntGoldProds',
        'Kidhome', 'Teenhome',
        'PredictionProbability'
    ]
    
    # Lưu kết quả
    potential_customers[columns_to_save].to_csv('result.csv', index=False)
    
    # Phân tích thống kê cơ bản
    print("\n=== THỐNG KÊ KHÁCH HÀNG TIỀM NĂNG ===")
    print(f"Tổng số khách hàng: {len(df)}")
    print(f"Số khách hàng tiềm năng: {len(potential_customers)}")
    print(f"Tỷ lệ khách hàng tiềm năng: {(len(potential_customers)/len(df))*100:.2f}%")
    
    # Phân tích chi tiết
    print("\n=== CHI TIẾT KHÁCH HÀNG TIỀM NĂNG ===")
    print("\nThống kê chung:")
    stats = potential_customers[['Age', 'Income', 'TotalSpending', 'AvgPurchaseValue']].describe()
    print(stats.round(2))
    
    # Phân tích phân khúc
    segments = analyze_customer_segments(potential_customers)
    
    print("\nPhân bố độ tuổi:")
    print(segments['age_distribution'])
    
    print("\nPhân bố thu nhập:")
    print(segments['income_distribution'])
    
    print("\nPhân bố gia đình:")
    print(segments['family_distribution'])
    
    print("\nPhân bố chi tiêu:")
    print(segments['spending_distribution'])
    
    # Phân tích chi tiêu và hành vi mua hàng
    spending_patterns = analyze_spending_patterns(potential_customers)
    
    print("\n=== PHÂN TÍCH CHI TIÊU VÀ HÀNH VI MUA HÀNG ===")
    print("\nTổng chi tiêu theo danh mục:")
    print(spending_patterns['total_by_category'].round(2))
    
    print("\nTỷ lệ trung bình chi tiêu theo danh mục (%):")
    print(spending_patterns['avg_category_ratios'].round(2))
    
    print("\nTỷ lệ sử dụng các kênh mua hàng (%):")
    print(spending_patterns['channel_ratios'].round(2))
    
    print("\nPhân bố theo thời gian mua hàng gần đây:")
    print(spending_patterns['recency_distribution'])
    
    print("\nTop 5 khách hàng tiềm năng (sắp xếp theo xác suất):")
    top_5 = potential_customers[['ID', 'Age', 'Income', 'TotalSpending', 'AvgPurchaseValue', 'PredictionProbability']].head()
    print(top_5.round(2).to_string(index=False))
    
    # Phân tích chi tiết top 5 khách hàng
    print("\nChi tiết mua hàng của top 5 khách hàng:")
    top_5_details = potential_customers.head()[['ID', 'MntWines', 'MntFruits', 'MntMeatProducts', 
                                              'MntFishProducts', 'MntSweetProducts', 'MntGoldProds',
                                              'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases']]
    print(top_5_details.round(2).to_string(index=False))
    
    # Phân tích top 10 khách hàng
    print("\n=== PHÂN TÍCH CHI TIẾT TOP 10 KHÁCH HÀNG TIỀM NĂNG ===")
    top_10 = analyze_top_customers(potential_customers, 10)
    
    print("\n1. Thông tin cơ bản:")
    basic_info = top_10[['ID', 'Age', 'Income', 'TotalSpending', 'AvgPurchaseValue', 'PredictionProbability']]
    print(basic_info.round(2).to_string(index=False))
    
    print("\n2. Chi tiết chi tiêu theo danh mục:")
    spending_details = top_10[['ID', 'MntWines', 'MntFruits', 'MntMeatProducts', 
                             'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']]
    print(spending_details.round(2).to_string(index=False))
    
    print("\n3. Tỷ lệ chi tiêu theo danh mục (%):")
    spending_ratios = top_10[['ID', 'MntWines_Percentage', 'MntFruits_Percentage', 
                             'MntMeatProducts_Percentage', 'MntFishProducts_Percentage',
                             'MntSweetProducts_Percentage', 'MntGoldProds_Percentage']]
    print(spending_ratios.round(2).to_string(index=False))
    
    print("\n4. Thông tin mua hàng:")
    purchase_info = top_10[['ID', 'NumWebPurchases', 'NumCatalogPurchases', 
                           'NumStorePurchases', 'NumWebVisitsMonth', 'Recency']]
    print(purchase_info.round(2).to_string(index=False))
    
    print("\n5. Tỷ lệ sử dụng các kênh mua hàng (%):")
    channel_ratios = top_10[['ID', 'WebRatio', 'CatalogRatio', 'StoreRatio']]
    print(channel_ratios.round(2).to_string(index=False))
    
    print("\n6. Thông tin gia đình:")
    family_info = top_10[['ID', 'Age', 'Kidhome', 'Teenhome']]
    print(family_info.round(2).to_string(index=False))
    
    print("\nĐã lưu danh sách đầy đủ khách hàng tiềm năng vào file 'result.csv'")

if __name__ == "__main__":
    predict_potential_customers() 