import pandas as pd
import numpy as np
import joblib
import os
import json

def predict_potential_customers():
    try:
        # Đường dẫn đến file dữ liệu
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(script_dir, '..', 'marketing_campaign.csv')
        
        # Đọc dữ liệu
        df = pd.read_csv(data_path, sep='\t')
        
        # Load model và scaler
        model_path = os.path.join(script_dir, '..', 'optimized_model.pkl')
        scaler_path = os.path.join(script_dir, '..', 'optimized_scaler.pkl')
        
        if not os.path.exists(model_path) or not os.path.exists(scaler_path):
            # Nếu không có model tối ưu, sử dụng model cơ bản
            model_path = os.path.join(script_dir, '..', 'best_model.pkl')
            scaler_path = os.path.join(script_dir, '..', 'scaler.pkl')
        
        if not os.path.exists(model_path) or not os.path.exists(scaler_path):
            raise FileNotFoundError("Không tìm thấy model hoặc scaler")
        
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        
        # Chuẩn bị features
        features = ['Year_Birth', 'Income', 'Kidhome', 'Teenhome', 'Recency',
                   'MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts',
                   'MntSweetProducts', 'MntGoldProds', 'NumDealsPurchases',
                   'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases',
                   'NumWebVisitsMonth']
        
        # Xử lý missing values
        df[features] = df[features].fillna(df[features].mean())
        
        X = df[features]
        X_scaled = scaler.transform(X)
        
        # Dự đoán
        predictions = model.predict(X_scaled)
        probabilities = model.predict_proba(X_scaled)[:, 1]
        
        # Tính toán các metrics
        df['probability'] = probabilities
        df['totalSpent'] = df[['MntWines', 'MntFruits', 'MntMeatProducts', 
                              'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']].sum(axis=1)
        df['avgPurchaseValue'] = df['totalSpent'] / (df['NumWebPurchases'] + df['NumCatalogPurchases'] + df['NumStorePurchases'] + 1)
        df['purchaseCount'] = df['NumWebPurchases'] + df['NumCatalogPurchases'] + df['NumStorePurchases']
        
        # Lọc khách hàng tiềm năng (xác suất > 0.5)
        potential_customers = df[df['probability'] > 0.5].copy()
        
        # Sắp xếp theo xác suất giảm dần
        potential_customers = potential_customers.sort_values('probability', ascending=False)
        
        # Chọn các cột cần thiết
        result_columns = ['ID', 'probability', 'totalSpent', 'avgPurchaseValue', 'purchaseCount']
        result = potential_customers[result_columns].copy()
        
        # Chuyển đổi thành list of dicts
        result_list = result.to_dict('records')
        
        # Trả về JSON
        return json.dumps(result_list, default=str)
        
    except Exception as e:
        error_msg = f"Lỗi trong quá trình dự đoán: {str(e)}"
        print(error_msg)
        return json.dumps({"error": error_msg})

if __name__ == "__main__":
    result = predict_potential_customers()
    print(result)
