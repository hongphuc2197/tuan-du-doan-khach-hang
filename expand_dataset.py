import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import uuid
import warnings
warnings.filterwarnings('ignore')

def expand_dataset_to_687_users():
    """
    Mở rộng dataset từ 49 users lên 687 users dựa trên pattern của dữ liệu thực tế
    """
    print("Đang đọc dữ liệu gốc...")
    
    # Đọc dữ liệu gốc
    df_original = pd.read_csv('user_actions_with_profile_rows.csv')
    
    print(f"Dữ liệu gốc: {len(df_original)} dòng, {df_original['user_id'].nunique()} users")
    
    # Phân tích pattern từ dữ liệu gốc
    unique_users = df_original['user_id'].unique()
    print(f"Phân tích pattern từ {len(unique_users)} users gốc...")
    
    # Tạo dữ liệu mở rộng
    expanded_data = []
    target_users = 687
    current_users = len(unique_users)
    users_to_generate = target_users - current_users
    
    print(f"Cần tạo thêm {users_to_generate} users để đạt {target_users} users")
    
    # Phân tích các pattern từ dữ liệu gốc
    education_dist = df_original['education'].value_counts(normalize=True)
    marital_dist = df_original['marital_status'].value_counts(normalize=True)
    income_level_dist = df_original['income_level'].value_counts(normalize=True)
    
    # Phân tích income theo income_level
    income_by_level = {}
    for level in df_original['income_level'].unique():
        if pd.notna(level):
            level_data = df_original[df_original['income_level'] == level]['income']
            income_by_level[level] = {
                'mean': level_data.mean() if not level_data.empty else 0,
                'std': level_data.std() if not level_data.empty else 0,
                'min': level_data.min() if not level_data.empty else 0,
                'max': level_data.max() if not level_data.empty else 0
            }
    
    # Phân tích year_birth
    year_birth_stats = {
        'mean': df_original['year_birth'].mean(),
        'std': df_original['year_birth'].std(),
        'min': df_original['year_birth'].min(),
        'max': df_original['year_birth'].max()
    }
    
    # Phân tích kidhome và teenhome
    kidhome_dist = df_original['kidhome'].value_counts(normalize=True)
    teenhome_dist = df_original['teenhome'].value_counts(normalize=True)
    
    print("Đang tạo dữ liệu mở rộng...")
    
    # Tạo dữ liệu cho users mới
    for i in range(users_to_generate):
        # Tạo user_id mới
        new_user_id = str(uuid.uuid4())
        
        # Chọn education dựa trên phân phối
        education = np.random.choice(education_dist.index, p=education_dist.values)
        
        # Chọn marital_status dựa trên phân phối (thay YOLO thành Single)
        marital_status = np.random.choice(marital_dist.index, p=marital_dist.values)
        if marital_status == 'YOLO':
            marital_status = 'Single'
        
        # Chọn income_level dựa trên phân phối
        income_level = np.random.choice(income_level_dist.index, p=income_level_dist.values)
        
        # Tạo income dựa trên income_level
        if income_level in income_by_level and pd.notna(income_level):
            income_stats = income_by_level[income_level]
            if income_stats['std'] > 0:
                income = max(0, np.random.normal(income_stats['mean'], income_stats['std']))
            else:
                income = income_stats['mean']
        else:
            income = 0
        
        # Tạo year_birth
        year_birth = int(np.random.normal(year_birth_stats['mean'], year_birth_stats['std']))
        year_birth = max(1950, min(2010, year_birth))  # Giới hạn trong khoảng hợp lý
        
        # Tạo kidhome và teenhome
        kidhome = np.random.choice(kidhome_dist.index, p=kidhome_dist.values)
        teenhome = np.random.choice(teenhome_dist.index, p=teenhome_dist.values)
        
        # Tạo age
        current_year = datetime.now().year
        age = current_year - year_birth
        
        # Tạo email và name
        email = f"user{687 - users_to_generate + i + 1}@example.com"
        name = f"User {687 - users_to_generate + i + 1}"
        
        # Tạo một số hành động cho user này
        num_actions = np.random.poisson(2) + 1  # Trung bình 2-3 hành động
        num_actions = min(num_actions, 10)  # Tối đa 10 hành động
        
        for j in range(num_actions):
            # Tạo event_type (70% view, 30% purchase)
            event_type = np.random.choice(['view', 'purchase'], p=[0.7, 0.3])
            
            # Tạo product_id và category_id
            product_id = random.randint(1, 20)
            category_id = random.randint(1, 10)
            
            # Tạo price dựa trên income_level
            if income_level == 'Very High':
                base_price = 200000
            elif income_level == 'High':
                base_price = 150000
            elif income_level == 'Medium':
                base_price = 100000
            elif income_level == 'Low':
                base_price = 50000
            else:
                base_price = 80000
            
            price = max(10000, np.random.normal(base_price, base_price * 0.3))
            
            # Tạo event_time (trong vòng 30 ngày gần đây)
            days_ago = random.randint(0, 30)
            event_time = datetime.now() - timedelta(days=days_ago)
            
            # Tạo user_session
            user_session = f"session_{int(event_time.timestamp() * 1000)}"
            
            # Tạo user_agent
            user_agents = [
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_11 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
            ]
            user_agent = random.choice(user_agents)
            
            # Tạo user_created_at (trước event_time)
            user_created_at = event_time - timedelta(days=random.randint(1, 30))
            
            # Tạo dòng dữ liệu
            new_row = {
                'id': str(uuid.uuid4()),
                'user_id': new_user_id,
                'product_id': product_id,
                'event_type': event_type,
                'event_time': event_time.strftime('%Y-%m-%d %H:%M:%S.%f+00'),
                'category_id': category_id,
                'price': round(price, 2),
                'user_session': user_session,
                'user_agent': user_agent,
                'ip_address': '',
                'email': email,
                'name': name,
                'year_birth': year_birth,
                'education': education,
                'marital_status': marital_status,
                'income': income,
                'kidhome': kidhome,
                'teenhome': teenhome,
                'user_created_at': user_created_at.strftime('%Y-%m-%d %H:%M:%S.%f+00'),
                'age': age,
                'income_level': income_level
            }
            
            expanded_data.append(new_row)
    
    # Kết hợp dữ liệu gốc và dữ liệu mở rộng
    df_expanded = pd.concat([df_original, pd.DataFrame(expanded_data)], ignore_index=True)
    
    print(f"\nDữ liệu mở rộng: {len(df_expanded)} dòng, {df_expanded['user_id'].nunique()} users")
    
    # Lưu file mới
    output_file = 'user_actions_expanded_687.csv'
    df_expanded.to_csv(output_file, index=False)
    print(f"Đã lưu dữ liệu mở rộng vào: {output_file}")
    
    # Thống kê
    print("\n=== THỐNG KÊ DỮ LIỆU MỞ RỘNG ===")
    print(f"Tổng số users: {df_expanded['user_id'].nunique()}")
    print(f"Tổng số hành động: {len(df_expanded)}")
    print(f"Hành động trung bình/user: {len(df_expanded) / df_expanded['user_id'].nunique():.2f}")
    
    print("\nThống kê event_type:")
    print(df_expanded['event_type'].value_counts())
    
    print("\nThống kê education:")
    print(df_expanded['education'].value_counts())
    
    print("\nThống kê marital_status:")
    print(df_expanded['marital_status'].value_counts())
    
    print("\nThống kê income_level:")
    print(df_expanded['income_level'].value_counts())
    
    # Thống kê users có mua hàng
    users_with_purchase = df_expanded[df_expanded['event_type'] == 'purchase']['user_id'].nunique()
    print(f"\nUsers có mua hàng: {users_with_purchase}")
    print(f"Tỷ lệ users có mua hàng: {users_with_purchase / df_expanded['user_id'].nunique():.2%}")
    
    return df_expanded

if __name__ == "__main__":
    expanded_data = expand_dataset_to_687_users()
    print("\nMở rộng dataset hoàn tất!")