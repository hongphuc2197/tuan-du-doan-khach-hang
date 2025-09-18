import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def convert_627_users_to_marketing_campaign():
    """
    Chuyển đổi dataset 627 users sang format marketing_campaign.csv
    """
    print("Đang đọc file user_actions_realistic_627.csv...")
    
    # Đọc file CSV
    df = pd.read_csv('user_actions_realistic_627.csv')
    
    print(f"Dữ liệu có {len(df)} dòng và {len(df.columns)} cột")
    print(f"Số user_id duy nhất: {df['user_id'].nunique()}")
    
    # Tạo DataFrame mới với cấu trúc tương thích
    converted_data = []
    
    # Lấy danh sách user_id duy nhất
    unique_users = df['user_id'].unique()
    print(f"\nChuyển đổi {len(unique_users)} users...")
    
    for i, user_id in enumerate(unique_users):
        if (i + 1) % 100 == 0:
            print(f"Đã xử lý {i + 1}/{len(unique_users)} users...")
        
        # Lấy tất cả dữ liệu của user này
        user_actions = df[df['user_id'] == user_id]
        
        # Lấy thông tin profile từ dòng đầu tiên
        user_profile = user_actions.iloc[0]
        
        # Tính toán các giá trị cần thiết
        try:
            year_birth = int(user_profile['year_birth']) if user_profile['year_birth'] and str(user_profile['year_birth']).isdigit() else 1990
        except:
            year_birth = 1990
            
        education = user_profile['education']
        marital_status = user_profile['marital_status']
        
        # Thay đổi YOLO thành Single
        if marital_status == 'YOLO':
            marital_status = 'Single'
        
        try:
            income = float(user_profile['income']) if user_profile['income'] and str(user_profile['income']).replace('.', '').isdigit() else 0
        except:
            income = 0
            
        try:
            kidhome = int(user_profile['kidhome']) if user_profile['kidhome'] and str(user_profile['kidhome']).isdigit() else 0
        except:
            kidhome = 0
            
        try:
            teenhome = int(user_profile['teenhome']) if user_profile['teenhome'] and str(user_profile['teenhome']).isdigit() else 0
        except:
            teenhome = 0
        
        # Tính tuổi
        current_year = datetime.now().year
        age = current_year - year_birth
        
        # Tính recency (số ngày từ lần mua cuối)
        if 'event_time' in user_profile and pd.notna(user_profile['event_time']):
            try:
                last_purchase = pd.to_datetime(user_profile['event_time'])
                recency = (datetime.now() - last_purchase).days
            except:
                recency = 30  # Giá trị mặc định
        else:
            recency = 30
        
        # Tính các chỉ số dựa trên hành động thực tế của user
        purchase_events = user_actions[user_actions['event_type'] == 'purchase']
        view_events = user_actions[user_actions['event_type'] == 'view']
        
        # Tính tổng chi tiêu thực tế từ các lần mua hàng
        total_spent = purchase_events['price'].sum() if len(purchase_events) > 0 else 0
        
        # Tạo dữ liệu chi tiêu cho các danh mục dựa trên chi tiêu thực tế
        if total_spent > 0:
            # Phân bổ chi tiêu thực tế cho các danh mục
            mnt_wines = total_spent * 0.3
            mnt_fruits = total_spent * 0.1
            mnt_meat = total_spent * 0.2
            mnt_fish = total_spent * 0.15
            mnt_sweet = total_spent * 0.1
            mnt_gold = total_spent * 0.15
        else:
            # Nếu không có chi tiêu thực tế, tạo dữ liệu giả lập dựa trên income level
            income_level = user_profile.get('income_level', 'Unknown')
            
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
            
            mnt_wines = max(0, np.random.normal(base_spending * 0.3, base_spending * 0.1))
            mnt_fruits = max(0, np.random.normal(base_spending * 0.1, base_spending * 0.05))
            mnt_meat = max(0, np.random.normal(base_spending * 0.2, base_spending * 0.1))
            mnt_fish = max(0, np.random.normal(base_spending * 0.15, base_spending * 0.05))
            mnt_sweet = max(0, np.random.normal(base_spending * 0.1, base_spending * 0.05))
            mnt_gold = max(0, np.random.normal(base_spending * 0.15, base_spending * 0.1))
        
        # Tính số lần mua hàng dựa trên dữ liệu event thực tế
        num_deals = len(purchase_events)
        num_web = len(user_actions) // 2  # Giả lập
        num_catalog = len(user_actions) // 4  # Giả lập
        num_store = len(purchase_events)  # Số lần mua hàng thực tế
        num_web_visits = len(view_events)  # Số lần xem sản phẩm
        
        # Tạo response dựa trên số lần mua hàng thực tế
        response = 1 if len(purchase_events) > 0 else 0
        
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
    output_file = 'marketing_campaign_627_users.csv'
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
    
    print("\nThống kê giáo dục:")
    print(converted_df['Education'].value_counts())
    
    print("\nThống kê tình trạng hôn nhân:")
    print(converted_df['Marital_Status'].value_counts())
    
    print("\nThống kê số lần mua hàng:")
    print(f"Số lần mua hàng trung bình: {converted_df['NumDealsPurchases'].mean():.2f}")
    print(f"Số lần mua hàng tối đa: {converted_df['NumDealsPurchases'].max()}")
    print(f"Số khách hàng có mua hàng: {(converted_df['NumDealsPurchases'] > 0).sum()}")
    
    print("\nThống kê chi tiêu theo danh mục sách:")
    print(f"Chi tiêu trung bình cho sách Công nghệ giáo dục: {converted_df['MntWines'].mean():.2f} VND")
    print(f"Chi tiêu trung bình cho sách Công nghệ thông tin: {converted_df['MntMeatProducts'].mean():.2f} VND")
    print(f"Chi tiêu trung bình cho sách Thiết kế web: {converted_df['MntFishProducts'].mean():.2f} VND")
    print(f"Chi tiêu trung bình cho sách Lập trình: {converted_df['MntSweetProducts'].mean():.2f} VND")
    print(f"Chi tiêu trung bình cho sách Nghiên cứu khoa học: {converted_df['MntGoldProds'].mean():.2f} VND")
    
    return converted_df

if __name__ == "__main__":
    converted_data = convert_627_users_to_marketing_campaign()
    print("\nChuyển đổi dữ liệu 627 users hoàn tất!")