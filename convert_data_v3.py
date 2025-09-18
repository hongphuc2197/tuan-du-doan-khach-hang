import pandas as pd
import numpy as np
from datetime import datetime
import csv
import warnings
warnings.filterwarnings('ignore')

def convert_thongtinsach_to_marketing_campaign():
    """
    Chuyển đổi dữ liệu từ thongtinsach.csv sang format tương thích với marketing_campaign.csv
    """
    print("Đang đọc file thongtinsach.csv...")
    
    # Đọc file CSV thủ công để xử lý đúng format
    data_rows = []
    with open('thongtinsach.csv', 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            data_rows.append(row)
    
    # Lấy header
    header = data_rows[0]
    print(f"Header có {len(header)} cột: {header}")
    
    # Tạo DataFrame
    df = pd.DataFrame(data_rows[1:], columns=header)
    
    print(f"Dữ liệu có {len(df)} dòng và {len(df.columns)} cột")
    print("Các cột trong dữ liệu:")
    for i, col in enumerate(df.columns):
        print(f"{i+1}. {col}")
    
    # Hiển thị vài dòng đầu để kiểm tra
    print("\nVài dòng đầu tiên:")
    print(df.head(3))
    
    # Tạo DataFrame mới với cấu trúc tương thích
    converted_data = []
    
    # Lấy danh sách user_id duy nhất
    unique_users = df['user_id'].unique()
    print(f"\nTìm thấy {len(unique_users)} người dùng duy nhất")
    
    for user_id in unique_users:
        user_data = df[df['user_id'] == user_id].iloc[0]  # Lấy dòng đầu tiên của mỗi user
        
        # Tính toán các giá trị cần thiết
        try:
            year_birth = int(user_data['year_birth']) if user_data['year_birth'] and str(user_data['year_birth']).isdigit() else 1990
        except:
            year_birth = 1990
            
        education = user_data['education']
        marital_status = user_data['marital_status']
        
        try:
            income = float(user_data['income']) if user_data['income'] and str(user_data['income']).replace('.', '').isdigit() else 0
        except:
            income = 0
            
        try:
            kidhome = int(user_data['kidhome']) if user_data['kidhome'] and str(user_data['kidhome']).isdigit() else 0
        except:
            kidhome = 0
            
        try:
            teenhome = int(user_data['teenhome']) if user_data['teenhome'] and str(user_data['teenhome']).isdigit() else 0
        except:
            teenhome = 0
        
        # Tính tuổi
        current_year = datetime.now().year
        age = current_year - year_birth
        
        # Tính recency (số ngày từ lần mua cuối)
        if 'event_time' in user_data and pd.notna(user_data['event_time']):
            try:
                last_purchase = pd.to_datetime(user_data['event_time'])
                recency = (datetime.now() - last_purchase).days
            except:
                recency = 30  # Giá trị mặc định
        else:
            recency = 30
        
        # Tính các chỉ số chi tiêu dựa trên dữ liệu có sẵn
        # Vì dữ liệu mới không có các chỉ số chi tiêu cụ thể, chúng ta sẽ tạo dữ liệu giả lập
        # dựa trên income và các đặc điểm khác
        
        # Tạo dữ liệu giả lập dựa trên income level
        income_level = user_data.get('income_level', 'Unknown')
        
        if income_level == 'Very High':
            base_spending = 1000
        elif income_level == 'High':
            base_spending = 500
        elif income_level == 'Medium':
            base_spending = 200
        elif income_level == 'Low':
            base_spending = 50
        else:
            base_spending = 100
        
        # Tạo dữ liệu chi tiêu cho các danh mục
        mnt_wines = max(0, np.random.normal(base_spending * 0.3, base_spending * 0.1))
        mnt_fruits = max(0, np.random.normal(base_spending * 0.1, base_spending * 0.05))
        mnt_meat = max(0, np.random.normal(base_spending * 0.2, base_spending * 0.1))
        mnt_fish = max(0, np.random.normal(base_spending * 0.15, base_spending * 0.05))
        mnt_sweet = max(0, np.random.normal(base_spending * 0.1, base_spending * 0.05))
        mnt_gold = max(0, np.random.normal(base_spending * 0.15, base_spending * 0.1))
        
        # Tính số lần mua hàng dựa trên dữ liệu event
        user_events = df[df['user_id'] == user_id]
        purchase_events = user_events[user_events['event_type'] == 'purchase']
        view_events = user_events[user_events['event_type'] == 'view']
        
        num_deals = len(purchase_events) if len(purchase_events) > 0 else 0
        num_web = len(user_events) // 2  # Giả lập
        num_catalog = len(user_events) // 4  # Giả lập
        num_store = len(purchase_events) if len(purchase_events) > 0 else 0
        num_web_visits = len(view_events) if len(view_events) > 0 else 0
        
        # Tạo response dựa trên số lần mua hàng và chi tiêu
        total_spending = mnt_wines + mnt_fruits + mnt_meat + mnt_fish + mnt_sweet + mnt_gold
        response = 1 if (len(purchase_events) > 0 and total_spending > base_spending * 0.5) else 0
        
        # Tạo dòng dữ liệu mới
        new_row = {
            'ID': len(converted_data) + 1,
            'Year_Birth': year_birth,
            'Education': education,
            'Marital_Status': marital_status,
            'Income': income,
            'Kidhome': kidhome,
            'Teenhome': teenhome,
            'Dt_Customer': '01-01-2020',  # Ngày mặc định
            'Recency': recency,
            'MntWines': round(mnt_wines, 2),
            'MntFruits': round(mnt_fruits, 2),
            'MntMeatProducts': round(mnt_meat, 2),
            'MntFishProducts': round(mnt_fish, 2),
            'MntSweetProducts': round(mnt_sweet, 2),
            'MntGoldProds': round(mnt_gold, 2),
            'NumDealsPurchases': num_deals,
            'NumWebPurchases': num_web,
            'NumCatalogPurchases': num_catalog,
            'NumStorePurchases': num_store,
            'NumWebVisitsMonth': num_web_visits,
            'AcceptedCmp3': 0,
            'AcceptedCmp4': 0,
            'AcceptedCmp5': 0,
            'AcceptedCmp1': 0,
            'AcceptedCmp2': 0,
            'Complain': 0,
            'Z_CostContact': 3,
            'Z_Revenue': 11,
            'Response': response
        }
        
        converted_data.append(new_row)
    
    # Tạo DataFrame mới
    converted_df = pd.DataFrame(converted_data)
    
    print(f"\nDữ liệu đã chuyển đổi có {len(converted_df)} dòng và {len(converted_df.columns)} cột")
    
    # Lưu file mới
    output_file = 'marketing_campaign_converted.csv'
    converted_df.to_csv(output_file, sep='\t', index=False)
    print(f"\nĐã lưu dữ liệu chuyển đổi vào file: {output_file}")
    
    # Hiển thị thống kê cơ bản
    print("\n=== THỐNG KÊ DỮ LIỆU CHUYỂN ĐỔI ===")
    print(f"Số lượng khách hàng: {len(converted_df)}")
    print(f"Số khách hàng có Response = 1: {converted_df['Response'].sum()}")
    print(f"Tỷ lệ khách hàng tiềm năng: {converted_df['Response'].mean():.2%}")
    
    print("\nThống kê thu nhập:")
    print(f"Thu nhập trung bình: {converted_df['Income'].mean():,.0f}")
    print(f"Thu nhập tối thiểu: {converted_df['Income'].min():,.0f}")
    print(f"Thu nhập tối đa: {converted_df['Income'].max():,.0f}")
    
    print("\nThống kê tuổi:")
    print(f"Tuổi trung bình: {current_year - converted_df['Year_Birth'].mean():.1f}")
    print(f"Tuổi tối thiểu: {current_year - converted_df['Year_Birth'].max()}")
    print(f"Tuổi tối đa: {current_year - converted_df['Year_Birth'].min()}")
    
    return converted_df

if __name__ == "__main__":
    converted_data = convert_thongtinsach_to_marketing_campaign()
    print("\nChuyển đổi dữ liệu hoàn tất!")