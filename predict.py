import streamlit as st
import numpy as np
import pandas as pd
import base64
import requests
import joblib
import json

def app():
    # st.header('Dự đoán')
    # Load models and scalers
    model = joblib.load('decision_tree_model.joblib')


    # Creating two columns
    # col1, col2 = st.columns(2)

    # Column for technical specifications

    # Column for design and style

        # Danh sách các hãng xe
    source = ['Fanpage', 'Data cũ', 'Hotline', 'Người quen', 'HV giới thiệu',
    'Đến trung tâm', 'Data mua', 'Seeding', 'Website']
    # Sắp xếp danh sách theo thứ tự bảng chữ cái
    employee = ['Thu', 'Linh', 'Duyên ', 'Phương', 'Loan', 'Ánh', 'Cúc', 'Yến',
    'Thảo']
    # Sử dụng danh sách đã sắp xếp trong selectbox
    source = st.selectbox('Nguồn', options=source)
    year = st.slider('Tuổi', min_value=3, max_value=70)
    sale_employee = st.selectbox('Nhân viên', options=employee)
    tested = st.selectbox('Đã test', options=['Không', 'Có'])
    month = st.slider('Tháng', min_value=1, max_value=12, value=1)
    facebook = st.selectbox('Liên hệ qua Facebook', options=['Có','Không'])
    zalo = st.selectbox('Liên hệ qua Zalo', options=['Có','Không'])
    phone = st.selectbox('Liên hệ qua Số Điện Thoại', options=['Có','Không'])
    
    encoding_dict = {
        'Data cũ': 0, 'Data mua': 1, 'Fanpage': 2, 'HV giới thiệu': 3,
        'Hotline': 4, 'Người quen': 5, 'Seeding': 6, 'Website': 7, 'Đến trung tâm': 8,
        'Cúc': 0, 'Duyên ': 1, 'Linh': 2, 'Loan': 3, 'Phương': 4,
        'Thu': 5, 'Thảo': 6, 'Yến': 7, 'Ánh': 8,
        'Chốt': 0, 'Từ chối': 1,
        'Có': 0, 'Không': 1
    }
    def map_value(value):
        return encoding_dict.get(value, None)

    # Predict button in the center or under columns
    if st.button('Dự đoán'):
        features = [source, sale_employee, tested, facebook, zalo, phone]
        nume = [year, month]
        mapped_data = [map_value(value) for value in features]
        all_features = np.hstack((mapped_data, nume))
        prediction_proba = model.predict_proba(all_features.reshape(1, -1))
        
        # Assuming the positive class (Đăng kí học) is the second column
        proba_đăng_kí_học = prediction_proba[0][1] * 100
        proba_không_học = prediction_proba[0][0] * 100
        
        st.write(f'Khả năng Đăng kí học: {proba_đăng_kí_học:.2f}%')
        st.write(f'Khả năng Không học: {proba_không_học:.2f}%')


# def app():
#     st.header('Dự đoán')
#     # Load model and encoders
#     try:
#         model = joblib.load('decision_tree.joblib')
#         encoders = joblib.load('label_encoders.joblib')
#     except FileNotFoundError:
#         st.error('Không tìm thấy tệp model hoặc encoder.')
#         return  # Dừng chương trình nếu không tìm thấy file

#     # Input forms
#     source_options = ['Fanpage', 'Data cũ', 'Hotline', 'Người quen', 'HV giới thiệu',
#                       'Đến trung tâm', 'Data mua', 'Seeding', 'Website']
#     employee_options = ['Thu', 'Linh', 'Duyên', 'Phương', 'Loan', 'Ánh', 'Cúc', 'Yến', 'Thảo']

#     source = st.selectbox('Nguồn', options=source_options)
#     year = st.slider('Tuổi', min_value=3, max_value=70)
#     sale_employee = st.selectbox('Nhân viên', options=employee_options)
#     tested = st.selectbox('Đã test', options=['Không', 'Có'])
#     month = st.slider('Tháng', min_value=1, max_value=12, value=1)
#     facebook = st.selectbox('Liên hệ qua Facebook', options=['Có', 'Không'])
#     zalo = st.selectbox('Liên hệ qua Zalo', options=['Có', 'Không'])
#     phone = st.selectbox('Liên hệ qua Số Điện Thoại', options=['Có', 'Không'])

#     def encode_features(features):
#         encoded_features = []
#         feature_names = ['source', 'sale_employee', 'tested', 'facebook', 'zalo', 'phone']
#         for feature_name, feature_value in zip(feature_names, features):
#             if feature_name in encoders:
#                 encoder = encoders[feature_name]
#                 encoded_feature = encoder.transform([feature_value])[0]
#                 encoded_features.append(encoded_feature)
#             else:
#                 st.error(f'Không tìm thấy bộ mã hóa cho {feature_name}.')
#                 return  # Dừng chương trình nếu không tìm thấy bộ mã hóa
#         return encoded_features

#     if st.button('Dự đoán'):
#         features = [source, sale_employee, tested, facebook, zalo, phone]
#         numerical = [year, month]
#         try:
#             mapped_features = encode_features(features)
#             if mapped_features is None:  # Kiểm tra nếu có lỗi trong hàm encode_features
#                 return
#             all_features = np.hstack((mapped_features, numerical))
#             prediction = model.predict(all_features.reshape(1, -1))
#             result = 'Đăng kí học' if prediction == 1 else 'Không học'
#             st.write(f'Dự đoán: {result}')
#         except Exception as e:
#             st.error(f'Đã xảy ra lỗi khi dự đoán: {e}')


