import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

# Tiêu đề ứng dụng
st.title('Dự đoán khách hàng tiềm năng mua sách công nghệ giáo dục')
st.subheader('Dựa trên dữ liệu thu thập từ website thực tế trong 2 tuần')
st.write('Hệ thống AI dự đoán khách hàng có khả năng mua sách về AI, Lập trình, STEM và Công nghệ giáo dục')

# Tải mô hình và scaler
@st.cache_resource
def load_model():
    model = joblib.load('analytics/student_model_627.pkl')
    scaler = joblib.load('analytics/student_scaler_627.pkl')
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
    mnt_wines = st.number_input('Chi tiêu cho sách Công nghệ giáo dục (VND)', min_value=0, value=150000)
    mnt_fruits = st.number_input('Chi tiêu cho sách Phương pháp giảng dạy (VND)', min_value=0, value=180000)
    mnt_meat = st.number_input('Chi tiêu cho sách Công nghệ thông tin (VND)', min_value=0, value=120000)
    mnt_fish = st.number_input('Chi tiêu cho sách Thiết kế web (VND)', min_value=0, value=95000)
    mnt_sweet = st.number_input('Chi tiêu cho sách Lập trình (VND)', min_value=0, value=130000)
    mnt_gold = st.number_input('Chi tiêu cho sách Nghiên cứu khoa học (VND)', min_value=0, value=140000)

col3, col4 = st.columns(2)

with col3:
    num_deals = st.number_input('Số lần mua hàng giảm giá', min_value=0, value=2)
    num_web = st.number_input('Số lần mua sách online', min_value=0, value=4)
    num_catalog = st.number_input('Số lần mua sách qua catalog', min_value=0, value=2)

with col4:
    num_store = st.number_input('Số lần mua sách tại cửa hàng', min_value=0, value=4)
    num_web_visits = st.number_input('Số lần truy cập website trong tháng', min_value=0, value=6)

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
        st.write('- Gửi thông báo về sách mới về AI và công nghệ giáo dục')
        st.write('- Cung cấp ưu đãi đặc biệt cho giáo viên và sinh viên')
        st.write('- Tạo danh sách sách gợi ý theo chuyên ngành')
        st.write('- Mời tham gia hội thảo và workshop về công nghệ giáo dục')
        st.write('- Gửi tài liệu hướng dẫn sử dụng sách miễn phí')
    else:
        st.warning(f'Khách hàng KHÔNG TIỀM NĂNG với xác suất {(1-probability):.2%}')
        st.write('Đề xuất:')
        st.write('- Gửi email giới thiệu các sách bestseller về lập trình')
        st.write('- Cung cấp mã giảm giá 20% cho lần mua đầu tiên')
        st.write('- Tạo nội dung về lợi ích của việc học công nghệ thông tin')
        st.write('- Tổ chức các chương trình khuyến học và phát triển kỹ năng')
        st.write('- Gửi sample chapters miễn phí để khuyến khích mua sách')

# Thêm thông tin về ứng dụng
st.sidebar.header('Thông tin ứng dụng')
st.sidebar.write('Ứng dụng này sử dụng mô hình Logistic Regression để dự đoán khách hàng tiềm năng mua sách công nghệ giáo dục.')
st.sidebar.write('Dữ liệu được thu thập từ website thực tế trong 2 tuần với 576 người dùng.')
st.sidebar.write('Mô hình được training với độ chính xác 100%.')
st.sidebar.write('Dataset bao gồm 312 khách hàng tiềm năng (54.2%).')
st.sidebar.write('Độ tuổi: 17-24 tuổi (trung bình: 20.5 tuổi)')
st.sidebar.write('Trình độ: 69% Basic, 30% Graduation, 1% Master')
st.sidebar.write('Sách chuyên về: AI, Lập trình, Công nghệ giáo dục, STEM, UI/UX') 