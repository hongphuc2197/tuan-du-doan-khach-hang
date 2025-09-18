import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import uuid
import warnings
warnings.filterwarnings('ignore')

def create_realistic_687_users():
    """
    Tạo dataset 687 users dựa trên pattern thực tế từ 87 users gốc
    """
    print("Đang đọc dữ liệu users gốc...")
    
    # Đọc dữ liệu users gốc
    df_original = pd.read_csv('users_rows.csv')
    
    print(f"Dữ liệu gốc: {len(df_original)} users")
    
    # Phân tích pattern từ dữ liệu gốc
    print("Phân tích pattern từ dữ liệu gốc...")
    
    # Phân tích education
    education_dist = df_original['education'].value_counts(normalize=True)
    print(f"Education distribution: {education_dist.to_dict()}")
    
    # Phân tích marital_status
    marital_dist = df_original['marital_status'].value_counts(normalize=True)
    print(f"Marital status distribution: {marital_dist.to_dict()}")
    
    # Phân tích income
    income_stats = {
        'mean': df_original['income'].mean(),
        'std': df_original['income'].std(),
        'min': df_original['income'].min(),
        'max': df_original['income'].max()
    }
    print(f"Income stats: {income_stats}")
    
    # Phân tích year_birth
    year_birth_stats = {
        'mean': df_original['year_birth'].mean(),
        'std': df_original['year_birth'].std(),
        'min': df_original['year_birth'].min(),
        'max': df_original['year_birth'].max()
    }
    print(f"Year birth stats: {year_birth_stats}")
    
    # Phân tích kidhome và teenhome
    kidhome_dist = df_original['kidhome'].value_counts(normalize=True)
    teenhome_dist = df_original['teenhome'].value_counts(normalize=True)
    print(f"Kidhome distribution: {kidhome_dist.to_dict()}")
    print(f"Teenhome distribution: {teenhome_dist.to_dict()}")
    
    # Tạo dữ liệu mở rộng
    expanded_data = []
    target_users = 627
    current_users = len(df_original)
    users_to_generate = target_users - current_users
    
    print(f"\nCần tạo thêm {users_to_generate} users để đạt {target_users} users")
    print(f"Bao gồm {current_users} users gốc + {users_to_generate} users mới")
    
    # Tạo dữ liệu cho users mới
    for i in range(users_to_generate):
        # Tạo user_id mới
        new_user_id = str(uuid.uuid4())
        
        # Chọn education dựa trên phân phối thực tế
        education = np.random.choice(education_dist.index, p=education_dist.values)
        
        # Chọn marital_status dựa trên phân phối thực tế (thay YOLO thành Single)
        marital_status = np.random.choice(marital_dist.index, p=marital_dist.values)
        if marital_status == 'YOLO':
            marital_status = 'Single'
        
        # Tạo income dựa trên phân phối thực tế
        if income_stats['std'] > 0:
            income = max(0, np.random.normal(income_stats['mean'], income_stats['std']))
            # Giới hạn trong khoảng thực tế
            income = max(income_stats['min'], min(income_stats['max'], income))
        else:
            income = income_stats['mean']
        
        # Tạo year_birth dựa trên phân phối thực tế
        if year_birth_stats['std'] > 0:
            year_birth = int(np.random.normal(year_birth_stats['mean'], year_birth_stats['std']))
            # Giới hạn trong khoảng hợp lý
            year_birth = max(1950, min(2010, year_birth))
        else:
            year_birth = int(year_birth_stats['mean'])
        
        # Tạo kidhome và teenhome dựa trên phân phối thực tế
        kidhome = np.random.choice(kidhome_dist.index, p=kidhome_dist.values)
        teenhome = np.random.choice(teenhome_dist.index, p=teenhome_dist.values)
        
        # Tạo age
        current_year = datetime.now().year
        age = current_year - year_birth
        
        # Tạo email và name
        email = f"user{current_users + i + 1}@example.com"
        name = f"User {current_users + i + 1}"
        
        # Tạo income_level dựa trên income
        if income >= 1000000000:  # 1 tỷ
            income_level = 'Very High'
        elif income >= 100000000:  # 100 triệu
            income_level = 'High'
        elif income >= 10000000:  # 10 triệu
            income_level = 'Medium'
        elif income > 0:
            income_level = 'Low'
        else:
            income_level = 'Unknown'
        
        # Tạo một số hành động cho user này (dựa trên pattern thực tế)
        # Tất cả users đều có ít nhất 1 hành động
        has_actions = True
        
        if has_actions:
            # Số hành động: 1-5 hành động (dựa trên pattern thực tế)
            num_actions = np.random.poisson(2) + 1
            num_actions = min(num_actions, 5)
            
            for j in range(num_actions):
                # Tạo event_type (75% view, 25% purchase - dựa trên pattern thực tế)
                event_type = np.random.choice(['view', 'purchase'], p=[0.75, 0.25])
                
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
                
                # Tạo user_agent (dựa trên pattern thực tế)
                user_agents = [
                    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36",
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_11 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (Linux; Android 15; V2247 Build/AP3A.240905.015.A2_NNCS;) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/140.0.7339.51 Mobile Safari/537.36 Zalo android/25081840 ZaloTheme/light ZaloLanguage/vi"
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
    # Trước tiên, chuyển đổi dữ liệu gốc sang format actions
    original_actions = []
    for _, user in df_original.iterrows():
        # Tạo ít nhất 1 hành động cho mỗi user gốc
        num_actions = np.random.poisson(2) + 1
        num_actions = min(num_actions, 5)
        
        for j in range(num_actions):
            event_type = np.random.choice(['view', 'purchase'], p=[0.75, 0.25])
            product_id = random.randint(1, 20)
            category_id = random.randint(1, 10)
            
            # Tạo price dựa trên income
            if user['income'] >= 1000000000:
                base_price = 200000
            elif user['income'] >= 100000000:
                base_price = 150000
            elif user['income'] >= 10000000:
                base_price = 100000
            elif user['income'] > 0:
                base_price = 50000
            else:
                base_price = 80000
            
            price = max(10000, np.random.normal(base_price, base_price * 0.3))
            
            days_ago = random.randint(0, 30)
            event_time = datetime.now() - timedelta(days=days_ago)
            user_session = f"session_{int(event_time.timestamp() * 1000)}"
            user_agent = random.choice([
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_11 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
            ])
            user_created_at = event_time - timedelta(days=random.randint(1, 30))
            
            # Tạo income_level
            if user['income'] >= 1000000000:
                income_level = 'Very High'
            elif user['income'] >= 100000000:
                income_level = 'High'
            elif user['income'] >= 10000000:
                income_level = 'Medium'
            elif user['income'] > 0:
                income_level = 'Low'
            else:
                income_level = 'Unknown'
            
            original_actions.append({
                'id': str(uuid.uuid4()),
                'user_id': user['id'],
                'product_id': product_id,
                'event_type': event_type,
                'event_time': event_time.strftime('%Y-%m-%d %H:%M:%S.%f+00'),
                'category_id': category_id,
                'price': round(price, 2),
                'user_session': user_session,
                'user_agent': user_agent,
                'ip_address': '',
                'email': user['email'],
                'name': user['name'],
                'year_birth': user['year_birth'],
                'education': user['education'],
                'marital_status': 'Single' if user['marital_status'] == 'YOLO' else user['marital_status'],
                'income': user['income'],
                'kidhome': user['kidhome'],
                'teenhome': user['teenhome'],
                'user_created_at': user_created_at.strftime('%Y-%m-%d %H:%M:%S.%f+00'),
                'age': current_year - user['year_birth'],
                'income_level': income_level
            })
    
    # Kết hợp tất cả dữ liệu
    all_actions = original_actions + expanded_data
    df_expanded = pd.DataFrame(all_actions)
    
    print(f"\nDữ liệu gốc: {len(original_actions)} hành động từ {len(df_original)} users")
    print(f"Dữ liệu mở rộng: {len(expanded_data)} hành động từ {users_to_generate} users mới")
    print(f"Tổng cộng: {len(all_actions)} hành động từ {len(df_original) + users_to_generate} users")
    
    print(f"\nDữ liệu mở rộng: {len(df_expanded)} dòng, {df_expanded['user_id'].nunique()} users")
    
    # Lưu file mới
    output_file = 'user_actions_realistic_627.csv'
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
    expanded_data = create_realistic_687_users()
    print("\nTạo dataset 627 users hoàn tất!")