import pandas as pd
import numpy as np
import joblib
import os
import json
from datetime import datetime

def predict_student_potential_customers():
    try:
        # Đường dẫn đến file dữ liệu sinh viên
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(script_dir, '..', 'user_actions_students_576.csv')
        
        # Đọc dữ liệu
        df = pd.read_csv(data_path)
        
        # Load model và scaler (sử dụng model đã train cho sinh viên)
        model_path = os.path.join(script_dir, '..', 'best_model.pkl')
        scaler_path = os.path.join(script_dir, '..', 'scaler.pkl')
        
        if not os.path.exists(model_path) or not os.path.exists(scaler_path):
            raise FileNotFoundError("Không tìm thấy model hoặc scaler")
        
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        
        # Tạo bảng tổng hợp theo user_id
        user_summary = df.groupby('user_id').agg({
            'id': 'count',  # Tổng số hành động
            'price': ['sum', 'mean', 'count'],  # Tổng chi tiêu, chi tiêu TB, số lần mua
            'year_birth': 'first',  # Năm sinh
            'education': 'first',  # Trình độ học vấn
            'marital_status': 'first',  # Tình trạng hôn nhân
            'income': 'first',  # Thu nhập
            'kidhome': 'first',  # Số con nhỏ
            'teenhome': 'first',  # Số con tuổi teen
            'age': 'first',  # Tuổi
            'income_level': 'first',  # Mức thu nhập
            'event_type': lambda x: (x == 'purchase').sum(),  # Số lần mua
            'event_time': ['min', 'max']  # Thời gian đầu và cuối
        }).reset_index()
        
        # Làm phẳng cột
        user_summary.columns = ['user_id', 'total_actions', 'total_spent', 'avg_purchase_value', 
                               'purchase_count', 'year_birth', 'education', 'marital_status', 
                               'income', 'kidhome', 'teenhome', 'age', 'income_level', 
                               'purchase_events', 'first_activity', 'last_activity']
        
        # Tính recency (số ngày từ lần hoạt động cuối)
        user_summary['last_activity'] = pd.to_datetime(user_summary['last_activity'])
        user_summary['recency'] = (datetime.now() - user_summary['last_activity']).dt.days
        
        # Tính frequency (số lần mua hàng)
        user_summary['frequency'] = user_summary['purchase_events']
        
        # Tính monetary (tổng chi tiêu)
        user_summary['monetary'] = user_summary['total_spent']
        
        # Tính các metrics bổ sung
        user_summary['avg_purchase_value'] = user_summary['total_spent'] / (user_summary['purchase_events'] + 1)
        user_summary['purchase_rate'] = user_summary['purchase_events'] / user_summary['total_actions']
        
        # Chuẩn bị features cho model (phải match với features đã train)
        # Model được train với: ['Year_Birth', 'Income', 'Kidhome', 'Teenhome', 'Recency',
        #                       'MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts',
        #                       'MntSweetProducts', 'MntGoldProds', 'NumDealsPurchases',
        #                       'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases',
        #                       'NumWebVisitsMonth']
        
        # Map dữ liệu sinh viên sang format của model
        user_summary['Year_Birth'] = user_summary['year_birth']
        user_summary['Income'] = user_summary['income']
        user_summary['Kidhome'] = user_summary['kidhome']
        user_summary['Teenhome'] = user_summary['teenhome']
        user_summary['Recency'] = user_summary['recency']
        
        # Tạo các features giả cho các cột không có trong dữ liệu sinh viên
        user_summary['MntWines'] = user_summary['total_spent'] * 0.3  # Giả sử 30% chi cho rượu
        user_summary['MntFruits'] = user_summary['total_spent'] * 0.1  # 10% cho trái cây
        user_summary['MntMeatProducts'] = user_summary['total_spent'] * 0.2  # 20% cho thịt
        user_summary['MntFishProducts'] = user_summary['total_spent'] * 0.15  # 15% cho cá
        user_summary['MntSweetProducts'] = user_summary['total_spent'] * 0.1  # 10% cho đồ ngọt
        user_summary['MntGoldProds'] = user_summary['total_spent'] * 0.15  # 15% cho vàng
        
        # Các features khác
        user_summary['NumDealsPurchases'] = user_summary['purchase_events'] * 0.3  # 30% mua qua deal
        user_summary['NumWebPurchases'] = user_summary['purchase_events'] * 0.5  # 50% mua qua web
        user_summary['NumCatalogPurchases'] = user_summary['purchase_events'] * 0.2  # 20% mua qua catalog
        user_summary['NumStorePurchases'] = user_summary['purchase_events'] * 0.3  # 30% mua tại cửa hàng
        user_summary['NumWebVisitsMonth'] = user_summary['total_actions'] * 0.8  # 80% actions là visit web
        
        # Features cho model
        features = ['Year_Birth', 'Income', 'Kidhome', 'Teenhome', 'Recency',
                   'MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts',
                   'MntSweetProducts', 'MntGoldProds', 'NumDealsPurchases',
                   'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases',
                   'NumWebVisitsMonth']
        
        # Xử lý missing values
        user_summary[features] = user_summary[features].fillna(user_summary[features].mean())
        
        X = user_summary[features]
        X_scaled = scaler.transform(X)
        
        # Dự đoán
        predictions = model.predict(X_scaled)
        probabilities = model.predict_proba(X_scaled)[:, 1]
        
        # Thêm kết quả vào DataFrame
        user_summary['probability'] = probabilities
        user_summary['is_potential'] = predictions
        
        # Lọc khách hàng tiềm năng (xác suất > 0.5)
        potential_customers = user_summary[user_summary['probability'] > 0.5].copy()
        
        # Sắp xếp theo xác suất giảm dần
        potential_customers = potential_customers.sort_values('probability', ascending=False)
        
        # Tạo ID cho frontend
        potential_customers['ID'] = potential_customers['user_id']
        
        # Chọn các cột cần thiết cho frontend
        result_columns = ['ID', 'probability', 'total_spent', 'avg_purchase_value', 
                         'purchase_events', 'age', 'education', 'income_level', 
                         'recency', 'frequency', 'monetary', 'purchase_rate']
        
        result = potential_customers[result_columns].copy()
        
        # Đổi tên cột cho phù hợp với frontend
        result = result.rename(columns={
            'total_spent': 'totalSpent',
            'avg_purchase_value': 'avgPurchaseValue', 
            'purchase_events': 'purchaseCount'
        })
        
        # Chuyển đổi thành list of dicts
        result_list = result.to_dict('records')
        
        # Trả về JSON
        return json.dumps(result_list, default=str)
        
    except Exception as e:
        error_msg = f"Lỗi trong quá trình dự đoán sinh viên: {str(e)}"
        print(error_msg)
        return json.dumps({"error": error_msg})

if __name__ == "__main__":
    result = predict_student_potential_customers()
    print(result)
