import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

# Tiêu đề ứng dụng
st.title('Dự đoán khách hàng tiềm năng - Kyanon Digital')

# Tải mô hình và scaler
@st.cache_resource
def load_model():
    model = joblib.load('optimized_model.pkl')
    scaler = joblib.load('optimized_scaler.pkl')
    return model, scaler

model, scaler = load_model()

# Tạo form nhập liệu
st.header('Nhập thông tin khách hàng')

# Tạo các trường nhập liệu
col1, col2 = st.columns(2)

with col1:
    year_birth = st.number_input('Năm sinh', min_value=1900, max_value=datetime.now().year, value=1980)
    income = st.number_input('Thu nhập (USD)', min_value=0, value=50000)
    kidhome = st.number_input('Số con nhỏ', min_value=0, max_value=5, value=0)
    teenhome = st.number_input('Số con tuổi teen', min_value=0, max_value=5, value=0)
    recency = st.number_input('Số ngày kể từ lần mua cuối', min_value=0, value=30)

with col2:
    mnt_wines = st.number_input('Chi tiêu cho rượu vang (USD)', min_value=0, value=100)
    mnt_fruits = st.number_input('Chi tiêu cho trái cây (USD)', min_value=0, value=50)
    mnt_meat = st.number_input('Chi tiêu cho thịt (USD)', min_value=0, value=100)
    mnt_fish = st.number_input('Chi tiêu cho cá (USD)', min_value=0, value=50)
    mnt_sweet = st.number_input('Chi tiêu cho đồ ngọt (USD)', min_value=0, value=50)
    mnt_gold = st.number_input('Chi tiêu cho vàng (USD)', min_value=0, value=50)

col3, col4 = st.columns(2)

with col3:
    num_deals = st.number_input('Số lần mua hàng giảm giá', min_value=0, value=2)
    num_web = st.number_input('Số lần mua hàng qua web', min_value=0, value=4)
    num_catalog = st.number_input('Số lần mua hàng qua catalog', min_value=0, value=2)

with col4:
    num_store = st.number_input('Số lần mua hàng tại cửa hàng', min_value=0, value=4)
    num_web_visits = st.number_input('Số lần truy cập web trong tháng', min_value=0, value=6)

# Tạo nút dự đoán
if st.button('Dự đoán'):
    # Tạo DataFrame từ dữ liệu nhập vào
    input_data = pd.DataFrame({
        'Year_Birth': [year_birth],
        'Income': [income],
        'Kidhome': [kidhome],
        'Teenhome': [teenhome],
        'Recency': [recency],
        'MntWines': [mnt_wines],
        'MntFruits': [mnt_fruits],
        'MntMeatProducts': [mnt_meat],
        'MntFishProducts': [mnt_fish],
        'MntSweetProducts': [mnt_sweet],
        'MntGoldProds': [mnt_gold],
        'NumDealsPurchases': [num_deals],
        'NumWebPurchases': [num_web],
        'NumCatalogPurchases': [num_catalog],
        'NumStorePurchases': [num_store],
        'NumWebVisitsMonth': [num_web_visits]
    })

    # Chuẩn hóa dữ liệu
    input_scaled = scaler.transform(input_data)

    # Dự đoán
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][1]

    # Hiển thị kết quả
    st.header('Kết quả dự đoán')
    
    if prediction == 1:
        st.success(f'Khách hàng TIỀM NĂNG với xác suất {probability:.2%}')
        st.write('Đề xuất:')
        st.write('- Tập trung vào các chiến dịch marketing cá nhân hóa')
        st.write('- Cung cấp các ưu đãi đặc biệt')
        st.write('- Duy trì tần suất tương tác thường xuyên')
    else:
        st.warning(f'Khách hàng KHÔNG TIỀM NĂNG với xác suất {(1-probability):.2%}')
        st.write('Đề xuất:')
        st.write('- Tập trung vào các chiến dịch thu hút khách hàng mới')
        st.write('- Cải thiện trải nghiệm khách hàng')
        st.write('- Tăng cường các chương trình khuyến mãi')

# Thêm thông tin về ứng dụng
st.sidebar.header('Thông tin ứng dụng')
st.sidebar.write('Ứng dụng này sử dụng mô hình Gradient Boosting để dự đoán khách hàng tiềm năng dựa trên các đặc điểm và hành vi mua hàng.')
st.sidebar.write('Mô hình đã được tối ưu hóa để đạt hiệu suất tốt nhất.') 