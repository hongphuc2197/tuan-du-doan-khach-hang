import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def convert_student_dataset_to_marketing_campaign():
    """
    Chuyển đổi dataset sinh viên 627 users sang format marketing_campaign.csv
    """
    print("Đang đọc file user_actions_students_627.csv...")
    
    # Đọc file CSV
    df = pd.read_csv('user_actions_students_627.csv')
    
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
        
        # Thông tin cơ bản
        year_birth = int(user_profile['year_birth'])
        education = user_profile['education']
        marital_status = user_profile['marital_status']
        income = float(user_profile['income'])
        kidhome = int(user_profile['kidhome'])
        teenhome = int(user_profile['teenhome'])
        
        # Tính tuổi
        current_year = datetime.now().year
        age = current_year - year_birth
        
        # Tính recency (số ngày từ lần mua cuối)
        if 'event_time' in user_profile and pd.notna(user_profile['event_time']):
            try:
                last_purchase = pd.to_datetime(user_profile['event_time'])
                recency = (datetime.now() - last_purchase).days
            except:
                recency = 30
        else:
            recency = 30
        
        # Tính các chỉ số dựa trên hành động thực tế của user
        purchase_events = user_actions[user_actions['event_type'] == 'purchase']
        view_events = user_actions[user_actions['event_type'] == 'view']
        
        # Tính tổng chi tiêu thực tế từ các lần mua hàng
        total_spent = purchase_events['price'].sum() if len(purchase_events) > 0 else 0
        
        # Tạo dữ liệu chi tiêu cho các danh mục sách
        if total_spent > 0:
            # Phân bổ chi tiêu thực tế cho các danh mục sách
            mnt_wines = total_spent * 0.3      # Công nghệ giáo dục
            mnt_fruits = total_spent * 0.1     # Phương pháp giảng dạy
            mnt_meat = total_spent * 0.2       # Công nghệ thông tin
            mnt_fish = total_spent * 0.15      # Thiết kế web
            mnt_sweet = total_spent * 0.1      # Lập trình
            mnt_gold = total_spent * 0.15      # Nghiên cứu khoa học
        else:
            # Nếu không có chi tiêu thực tế, tạo dữ liệu dựa trên thu nhập sinh viên
            if income > 4000000:  # Thu nhập cao
                base_spending = 500000
            elif income > 2000000:  # Thu nhập trung bình
                base_spending = 300000
            else:  # Thu nhập thấp
                base_spending = 150000
            
            mnt_wines = base_spending * 0.3
            mnt_fruits = base_spending * 0.1
            mnt_meat = base_spending * 0.2
            mnt_fish = base_spending * 0.15
            mnt_sweet = base_spending * 0.1
            mnt_gold = base_spending * 0.15
        
        # Tính số lần mua hàng
        num_deals = len(purchase_events[purchase_events['price'] < purchase_events['price'].mean() * 0.8])
        num_web = len(purchase_events)  # Tất cả mua hàng đều qua web (sinh viên)
        num_catalog = 0  # Sinh viên ít mua qua catalog
        num_store = len(purchase_events) // 3  # Một số mua tại cửa hàng
        num_web_visits = len(view_events) + len(purchase_events)
        
        # Tính tổng chi tiêu
        total_spending = mnt_wines + mnt_fruits + mnt_meat + mnt_fish + mnt_sweet + mnt_gold
        
        # Tạo ID cho user
        user_id_num = i + 1
        
        # Tạo dữ liệu chuyển đổi
        converted_row = {
            'ID': user_id_num,
            'Year_Birth': year_birth,
            'Education': education,
            'Marital_Status': marital_status,
            'Income': income,
            'Kidhome': kidhome,
            'Teenhome': teenhome,
            'Dt_Customer': '01-01-2024',  # Ngày đăng ký
            'Recency': recency,
            'MntWines': int(mnt_wines),      # Công nghệ giáo dục
            'MntFruits': int(mnt_fruits),    # Phương pháp giảng dạy
            'MntMeatProducts': int(mnt_meat), # Công nghệ thông tin
            'MntFishProducts': int(mnt_fish), # Thiết kế web
            'MntSweetProducts': int(mnt_sweet), # Lập trình
            'MntGoldProds': int(mnt_gold),   # Nghiên cứu khoa học
            'NumDealsPurchases': num_deals,
            'NumWebPurchases': num_web,
            'NumCatalogPurchases': num_catalog,
            'NumStorePurchases': num_store,
            'NumWebVisitsMonth': min(num_web_visits, 20),  # Giới hạn tối đa 20
            'AcceptedCmp3': 0,
            'AcceptedCmp4': 0,
            'AcceptedCmp5': 0,
            'AcceptedCmp1': 0,
            'AcceptedCmp2': 0,
            'Complain': 0,
            'Z_CostContact': 3,
            'Z_Revenue': 11,
            'Response': 1 if total_spending > 200000 else 0  # Khách hàng tiềm năng nếu chi tiêu > 200k
        }
        
        converted_data.append(converted_row)
    
    # Tạo DataFrame chuyển đổi
    converted_df = pd.DataFrame(converted_data)
    
    print(f"\nDataset chuyển đổi có {len(converted_df)} users")
    
    # Thống kê độ tuổi
    age_stats = converted_df['Year_Birth'].apply(lambda x: 2024 - x).describe()
    print(f"\nThống kê độ tuổi sinh viên:")
    print(f"Tuổi trung bình: {age_stats['mean']:.1f}")
    print(f"Tuổi tối thiểu: {age_stats['min']:.0f}")
    print(f"Tuổi tối đa: {age_stats['max']:.0f}")
    
    # Phân khúc độ tuổi
    ages = 2024 - converted_df['Year_Birth']
    age_18_25 = ((ages >= 18) & (ages <= 25)).sum()
    print(f"Số sinh viên (18-25 tuổi): {age_18_25}/{len(converted_df)} ({age_18_25/len(converted_df)*100:.1f}%)")
    
    # Thống kê thu nhập
    income_stats = converted_df['Income'].describe()
    print(f"\nThống kê thu nhập sinh viên:")
    print(f"Thu nhập trung bình: {income_stats['mean']:,.0f} VNĐ")
    print(f"Thu nhập tối thiểu: {income_stats['min']:,.0f} VNĐ")
    print(f"Thu nhập tối đa: {income_stats['max']:,.0f} VNĐ")
    
    # Thống kê khách hàng tiềm năng
    potential_customers = (converted_df['Response'] == 1).sum()
    print(f"\nThống kê khách hàng tiềm năng:")
    print(f"Số khách hàng tiềm năng: {potential_customers}/{len(converted_df)} ({potential_customers/len(converted_df)*100:.1f}%)")
    
    # Thống kê chi tiêu
    print(f"\nThống kê chi tiêu theo danh mục sách:")
    print(f"Chi tiêu trung bình cho sách Công nghệ giáo dục: {converted_df['MntWines'].mean():.2f} VNĐ")
    print(f"Chi tiêu trung bình cho sách Công nghệ thông tin: {converted_df['MntMeatProducts'].mean():.2f} VNĐ")
    print(f"Chi tiêu trung bình cho sách Thiết kế web: {converted_df['MntFishProducts'].mean():.2f} VNĐ")
    print(f"Chi tiêu trung bình cho sách Lập trình: {converted_df['MntSweetProducts'].mean():.2f} VNĐ")
    print(f"Chi tiêu trung bình cho sách Nghiên cứu khoa học: {converted_df['MntGoldProds'].mean():.2f} VNĐ")
    
    # Lưu file
    output_file = 'marketing_campaign_students_627.csv'
    converted_df.to_csv(output_file, sep='\t', index=False)
    print(f"\nĐã lưu dataset sinh viên vào: {output_file}")
    
    return converted_df

if __name__ == "__main__":
    converted_data = convert_student_dataset_to_marketing_campaign()
    print("\nChuyển đổi dataset sinh viên hoàn tất!")