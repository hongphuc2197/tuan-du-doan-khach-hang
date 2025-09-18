import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def create_student_dataset():
    """
    Tạo dataset 627 users tập trung vào sinh viên (18-25 tuổi)
    """
    print("Tạo dataset sinh viên mua sách công nghệ giáo dục...")
    
    # Đọc dữ liệu gốc
    df_original = pd.read_csv('user_actions_with_profile_rows.csv')
    print(f"Dữ liệu gốc có {len(df_original)} dòng")
    
    # Tạo danh sách 627 users với độ tuổi sinh viên
    target_users = 627
    current_users = len(df_original)
    users_to_generate = target_users - current_users
    
    print(f"Cần tạo thêm {users_to_generate} users để đạt {target_users} users")
    
    # Tạo dữ liệu mới
    new_data = []
    
    # Sử dụng dữ liệu gốc trước
    for _, row in df_original.iterrows():
        # Điều chỉnh tuổi thành sinh viên (18-25)
        current_year = datetime.now().year
        student_age = np.random.randint(18, 26)  # 18-25 tuổi
        year_birth = current_year - student_age
        
        # Điều chỉnh thu nhập cho sinh viên (thấp hơn)
        original_income = row.get('income', 0)
        if pd.notna(original_income) and original_income > 0:
            # Thu nhập sinh viên: 1-5 triệu VND/tháng
            student_income = np.random.randint(1000000, 5000000)
        else:
            student_income = np.random.randint(1000000, 3000000)
        
        # Điều chỉnh education cho sinh viên - 70% đại học, ~9% cao học, ~1% thạc sĩ
        education_options = ['Basic', 'Graduation', 'Master']
        education_weights = [0.7, 0.29, 0.01]  # 70% đại học, 29% cao học, 1% thạc sĩ
        education = np.random.choice(education_options, p=education_weights)
        
        # Marital status: hầu hết là Single
        marital_status = 'Single' if np.random.random() > 0.1 else 'Married'
        
        # Số con: hầu hết là 0
        kidhome = 0 if np.random.random() > 0.05 else 1
        teenhome = 0
        
        # Tạo hành động mua sách
        num_actions = np.random.poisson(2) + 1  # 1-5 hành động
        num_actions = min(num_actions, 5)
        
        for j in range(num_actions):
            # Chọn loại sách (category_id 1-12)
            category_id = np.random.randint(1, 13)
            
            # Giá sách dựa trên category
            book_prices = {
                1: 150000, 2: 180000, 3: 120000, 4: 95000, 5: 110000, 6: 140000,
                7: 160000, 8: 200000, 9: 130000, 10: 170000, 11: 145000, 12: 190000
            }
            price = book_prices.get(category_id, 150000)
            
            # Thêm một chút biến động giá
            price = int(price * np.random.uniform(0.8, 1.2))
            
            # Event type: 70% view, 30% purchase
            event_type = 'purchase' if np.random.random() < 0.3 else 'view'
            
            # Event time trong 30 ngày gần đây
            days_ago = np.random.randint(0, 30)
            event_time = datetime.now() - pd.Timedelta(days=days_ago)
            
            new_row = {
                'id': f"{row['id']}_{j}" if j > 0 else row['id'],
                'user_id': row['user_id'],
                'product_id': np.random.randint(1, 13),
                'event_type': event_type,
                'event_time': event_time,
                'category_id': category_id,
                'price': price,
                'user_session': f"session_{int(datetime.now().timestamp() * 1000)}_{j}",
                'user_agent': row.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'),
                'ip_address': row.get('ip_address', ''),
                'email': row['email'],
                'name': row['name'],
                'year_birth': year_birth,
                'education': education,
                'marital_status': marital_status,
                'income': student_income,
                'kidhome': kidhome,
                'teenhome': teenhome,
                'user_created_at': row['user_created_at'],
                'age': student_age,
                'income_level': 'Low' if student_income < 2000000 else 'Medium'
            }
            new_data.append(new_row)
    
    # Tạo thêm users mới để đạt 627 users
    print(f"Tạo thêm {users_to_generate} users mới...")
    
    for i in range(users_to_generate):
        # Tạo thông tin user mới
        user_id = f"student_{i+1:04d}"
        email = f"student{i+1}@university.edu.vn"
        name = f"Sinh viên {i+1}"
        
        # Độ tuổi sinh viên
        student_age = np.random.randint(18, 26)
        year_birth = current_year - student_age
        
        # Thu nhập sinh viên
        student_income = np.random.randint(1000000, 5000000)
        
        # Education - 70% sinh viên đại học, ~29% cao học, ~1% thạc sĩ
        education_options = ['Basic', 'Graduation', 'Master']
        education_weights = [0.7, 0.29, 0.01]  # 70% đại học, 29% cao học, 1% thạc sĩ
        education = np.random.choice(education_options, p=education_weights)
        
        # Marital status
        marital_status = 'Single' if np.random.random() > 0.1 else 'Married'
        
        # Số con
        kidhome = 0 if np.random.random() > 0.05 else 1
        teenhome = 0
        
        # Tạo hành động
        num_actions = np.random.poisson(2) + 1
        num_actions = min(num_actions, 5)
        
        for j in range(num_actions):
            category_id = np.random.randint(1, 13)
            book_prices = {
                1: 150000, 2: 180000, 3: 120000, 4: 95000, 5: 110000, 6: 140000,
                7: 160000, 8: 200000, 9: 130000, 10: 170000, 11: 145000, 12: 190000
            }
            price = book_prices.get(category_id, 150000)
            price = int(price * np.random.uniform(0.8, 1.2))
            
            event_type = 'purchase' if np.random.random() < 0.3 else 'view'
            days_ago = np.random.randint(0, 30)
            event_time = datetime.now() - pd.Timedelta(days=days_ago)
            
            new_row = {
                'id': f"student_{i+1}_{j}",
                'user_id': user_id,
                'product_id': np.random.randint(1, 13),
                'event_type': event_type,
                'event_time': event_time,
                'category_id': category_id,
                'price': price,
                'user_session': f"session_{int(datetime.now().timestamp() * 1000)}_{j}",
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'ip_address': '',
                'email': email,
                'name': name,
                'year_birth': year_birth,
                'education': education,
                'marital_status': marital_status,
                'income': student_income,
                'kidhome': kidhome,
                'teenhome': teenhome,
                'user_created_at': datetime.now() - pd.Timedelta(days=np.random.randint(1, 365)),
                'age': student_age,
                'income_level': 'Low' if student_income < 2000000 else 'Medium'
            }
            new_data.append(new_row)
    
    # Tạo DataFrame mới
    df_new = pd.DataFrame(new_data)
    
    print(f"\nDataset mới có {len(df_new)} dòng")
    print(f"Số user_id duy nhất: {df_new['user_id'].nunique()}")
    
    # Thống kê độ tuổi
    age_stats = df_new.groupby('user_id')['age'].first().describe()
    print(f"\nThống kê độ tuổi:")
    print(f"Tuổi trung bình: {age_stats['mean']:.1f}")
    print(f"Tuổi tối thiểu: {age_stats['min']:.0f}")
    print(f"Tuổi tối đa: {age_stats['max']:.0f}")
    
    # Phân khúc độ tuổi
    age_groups = df_new.groupby('user_id')['age'].first()
    age_18_25 = (age_groups >= 18) & (age_groups <= 25)
    print(f"Số sinh viên (18-25 tuổi): {age_18_25.sum()}/{len(age_groups)} ({age_18_25.mean()*100:.1f}%)")
    
    # Thống kê thu nhập
    income_stats = df_new.groupby('user_id')['income'].first().describe()
    print(f"\nThống kê thu nhập:")
    print(f"Thu nhập trung bình: {income_stats['mean']:,.0f} VNĐ")
    print(f"Thu nhập tối thiểu: {income_stats['min']:,.0f} VNĐ")
    print(f"Thu nhập tối đa: {income_stats['max']:,.0f} VNĐ")
    
    # Lưu file
    output_file = 'user_actions_students_627.csv'
    df_new.to_csv(output_file, index=False)
    print(f"\nĐã lưu dataset sinh viên vào: {output_file}")
    
    return df_new

if __name__ == "__main__":
    df_students = create_student_dataset()
    print("\nTạo dataset sinh viên hoàn tất!")