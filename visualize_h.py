import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

st.set_page_config(page_title="Dashboard", layout="wide")
# Function to load data with caching to improve performance
@st.cache_data
def load_data():
    # Load data
    data = pd.read_excel('data_visualize (1).xlsx')
    data['Doanh thu thực thu'] = data['Doanh thu thực thu'].replace(r'^\s*$', np.nan, regex=True)
    data['Doanh thu thực thu'] = pd.to_numeric(data['Doanh thu thực thu'], errors='coerce').fillna(0)
    bins = [3,11,15, 22, 38, 100]
    labels = ['Trẻ em', "Thiếu niên",'Thanh niên','Trung niên','Người già']
    data['Khoảng Tuổi'] = pd.cut(data['Tuổi'], bins=bins, labels=labels, right=False)
    # Tách cột 'Ngày liên hệ' thành các cột ngày, tháng, năm
    data['Ngày liên hệ'] = pd.to_datetime(data['Ngày liên hệ'])
    data['Ngày'] = data['Ngày liên hệ'].dt.day
    data['Tháng'] = data['Ngày liên hệ'].dt.month
    data['Năm'] = data['Ngày liên hệ'].dt.year
    contact_channels = data['Kênh liên lạc'].str.split(', ', expand=True)
    # Đặt tên cột cho DataFrame mới dựa trên kênh liên lạc
    for i in range(contact_channels.shape[1]):
        contact_channels.rename(columns={i: f'Channel_{i+1}'}, inplace=True)
    data = pd.concat([data, contact_channels], axis=1)
    return data

def main():
    data = load_data()
    st.markdown("""
        <style>
        div.stSelectbox > div {
            min-height: 10px; /* Giảm chiều cao tối thiểu */
            height: 30px; /* Đặt chiều cao cụ thể nếu cần */
            box-shadow: 2px 2px 5px rgba(0.1, 0.1, 0.1, 0.1); /* Thêm hiệu ứng shadow */
            transition: background-color 0.3s, box-shadow 0.3s
        }
        div[role='combobox'] {
            width: 100px !important; /* Thu nhỏ chiều dài của filter */
            background-color: #f0f0f0 !important; /* Làm filter nhạt hơn */
        }
        .st-bb {
            margin-bottom: 0px; /* Giảm khoảng cách phía dưới */
        }
        .st-at {
            margin-top: 0px; /* Giảm khoảng cách phía trên */
        }
        .metric-container {
            font-size: 60px; /* Tăng size của metrics */
            font-weight: bold; /* In đậm */
            text-align: center; /* Căn giữa */
        }
        .metric-label {
            font-size: 30px;
            color: #6e6e6e; /* Màu nhạt hơn cho label */
            text-align: center; /* Căn giữa */
        }
        .stButton > button {
            height: 80px;
            width: 200px;
            font-size: 40px;
            margin: 0px 10px; /* Giảm khoảng cách giữa các nút */
            border: 1px solid #ccc; /* Đường viền của button */
            border-radius: 10px; /* Bo tròn góc của button */
            background-color: #f9f9f9;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            cursor: pointer;
            transition: background-color 0.3s, box-shadow 0.3s;
        }
        .stButton > button:hover {
            background-color: #e0e0e0;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
        }
        .button-container {
            display: flex;
            justify-content: center; /* Căn giữa các nút */
            align-items: center;
            gap: 10px; /* Giảm khoảng cách giữa các nút */
            margin-top: 20px; /* Khoảng cách phía trên các nút */
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Create header in the center
    st.markdown("<h1 style='text-align: center; font-size: 62px;'>BÁO CÁO HỖ TRỢ TRUNG TÂM TIẾNG ANH SKYLARK</h1>", unsafe_allow_html=True)

    # Initialize session state for tab tracking
    if 'current_tab' not in st.session_state:
        st.session_state['current_tab'] = 'Tổng Quan Khách Hàng'

    # Create button container with columns for proper centering
    cols = st.columns([2, 1, 1, 2])
    with cols[1]:
        if st.button("Tổng Quan Khách Hàng"):
            st.session_state['current_tab'] = "Tổng Quan Khách Hàng"
    with cols[2]:
        if st.button("Doanh Thu"):
            st.session_state['current_tab'] = "Doanh Thu"            
    ## Dashboard chân dung khách hàng
    if st.session_state['current_tab'] == "Tổng Quan Khách Hàng":
        st.markdown("<h1 style='text-align: center; font-size: 50px;'>Tổng Quan Khách Hàng</h1>", unsafe_allow_html=True)
        # Filter by age group
        age_groups = ['Tất cả'] + list(data['Khoảng Tuổi'].cat.categories)
        selected_age_group = st.selectbox("Khoảng Tuổi", age_groups)        
        if selected_age_group == 'Tất cả':
            data = data
        else:
            data = data[data['Khoảng Tuổi'] == selected_age_group]
        total_customers = len(data)
        average_age = round(data['Tuổi'].mean())
        col_metric1, col_metric2 = st.columns(2)
        
        with col_metric1:
            st.markdown(f"<div class='metric-container'><div class='metric-label'>Tổng Số Khách Hàng</div>{total_customers}</div>", unsafe_allow_html=True)        
        with col_metric2:
            st.markdown(f"<div class='metric-container'><div class='metric-label'>Độ Tuổi Trung Bình</div>{average_age}</div>", unsafe_allow_html=True)

        # Vẽ hàng đầu tiên :
        col4, col5 = st.columns(2)
        with col4:
            data['Đánh giá KQ quả trình độ sau test đầu vào'] = data['Đánh giá KQ quả trình độ sau test đầu vào'].fillna('Học sinh không tham gia test')
            # Compute value counts for the column
            evaluation_counts = data['Đánh giá KQ quả trình độ sau test đầu vào'].value_counts().reset_index()
            evaluation_counts.columns = ['Đánh giá', 'Số lượng']

            # Generate pie chart using Plotly
            fig1 = px.pie(evaluation_counts, values='Số lượng', names='Đánh giá', title='Phân bố đánh giá trình độ sau test đầu vào')
            fig1.update_traces(textposition='inside', textinfo='percent+label')
            fig1.update_layout(width=500, height=500)
            st.plotly_chart(fig1)
        with col5:
            # Compute value counts for the column
            evaluation_counts = data['Nguồn'].value_counts().reset_index()
            evaluation_counts.columns = ['Nguồn', 'Số lượng']

            # Calculate total for percentage calculation
            total_counts = evaluation_counts['Số lượng'].sum()
            evaluation_counts['Phần trăm'] = (evaluation_counts['Số lượng'] / total_counts * 100).round(2)

            # Create a new column for display text combining 'Số lượng' and 'Phần trăm'
            evaluation_counts['Display Text'] = evaluation_counts.apply(lambda x: f"{x['Số lượng']} ({x['Phần trăm']}%)", axis=1)

            # Calculate sizeref to make bubble sizes more meaningful
            max_size = evaluation_counts['Số lượng'].max()
            sizeref_value = 2.0 * max_size / (100**2)  # Adjust the denominator based on desired bubble size scale

            # Generate bubble chart using Plotly with dynamic sizeref
            fig2 = px.scatter(evaluation_counts, x='Nguồn', y='Số lượng', size='Số lượng', color='Nguồn', 
                            title='Phân bố nguồn liên hệ khách hàng đối với trung tâm', text='Display Text')
            
            # Update traces and layout for better appearance
            fig2.update_traces(textposition='middle center', textfont=dict(size=12, color='black'), 
                            marker=dict(sizemode='area', sizeref=sizeref_value, sizemin=4))
            fig2.update_layout(width=700, height=500, plot_bgcolor='white', paper_bgcolor='white',
                            xaxis=dict(tickangle=-45), yaxis=dict(tickmode='array', tickvals=[0, 100, 200, 300, 400, 500, 600]),
                            margin=dict(l=40, r=40, t=40, b=80))
            st.plotly_chart(fig2)

        # Vẽ hàng thứ hai : 
        col6,col7=st.columns(2)
        with col6: 
            monthly_revenue = data.groupby('Tháng')['Doanh thu thực thu'].sum().reset_index()
            fig3 = px.line(monthly_revenue, x='Tháng', y='Doanh thu thực thu',
                        title='Doanh thu thực thu theo Tháng',
                        markers=True)
            fig3.update_layout(title='<b>Doanh thu theo Tháng</b>',
                            xaxis_title="Tháng",
                            yaxis_title="Doanh thu thực thu",
                            xaxis=dict(tickmode='linear'))
            st.plotly_chart(fig3)
        with col7:
            month_counts = data['Tháng'].value_counts().sort_index()
            month_counts = month_counts.reset_index()
            month_counts.columns = ['Tháng', 'Số Lượng']
            fig4 = px.line(month_counts, x='Tháng', y='Số Lượng',
                        title='Số lượng ghi nhận theo Tháng',
                        markers=True)
            fig4.update_layout(title='<b>Lượng liên hệ theo Tháng</b>',
                            xaxis_title="Tháng",
                            yaxis_title="Số Lượng",
                            xaxis=dict(tickmode='linear'))
            st.plotly_chart(fig4)
        # Vẽ hàng thứ ba 
        col8,col9=st.columns(2)
        with col8:
            data['Đánh giá KQ quả trình độ sau test đầu vào'].fillna('Học sinh không tham gia test', inplace=True)
            grouped = data.groupby(['Đánh giá KQ quả trình độ sau test đầu vào', 'Kế hoạch tiếp theo']).size().reset_index(name='Số lượng')
            categories = grouped['Kế hoạch tiếp theo'].unique()

            fig4 = go.Figure()
            for category in categories:
                filtered = grouped[grouped['Kế hoạch tiếp theo'] == category]
                fig4.add_trace(go.Bar(
                    x=filtered['Đánh giá KQ quả trình độ sau test đầu vào'],
                    y=filtered['Số lượng'],
                    name=category
                ))

            fig4.update_layout(
                barmode='group',
                title='Mối quan hệ giữa Đánh giá Kết quả Trình độ sau Test Đầu Vào và Kế Hoạch Tiếp Theo',
                xaxis_title='Đánh giá Kết quả Trình độ sau Test Đầu Vào',
                yaxis_title='Số lượng',
                legend_title='Kế hoạch Tiếp Theo',
                xaxis=dict(tickangle=-45)
            )
            st.plotly_chart(fig4)
        with col9:
            def summarize_contact_channels(data):
                # Xử lý NaN: Chuyển NaN thành chuỗi rỗng
                data[['Channel_1', 'Channel_2', 'Channel_3']] = data[['Channel_1', 'Channel_2', 'Channel_3']].fillna('')
                
                # Đếm số lượng cho mỗi kênh liên lạc
                counts = {
                    'SĐT': (data['Channel_1'] == 'SĐT').sum(),
                    'Facebook': (data['Channel_2'] == 'Facebook').sum(),
                    'Zalo': (data['Channel_3'] == 'Zalo').sum()
                }
                # Chuyển dictionary thành DataFrame
                summary_df = pd.DataFrame(list(counts.items()), columns=['Kiểu liên lạc', 'Số lượng'])
                return summary_df
            summary_df = summarize_contact_channels(data)
                # Tạo biểu đồ cột sử dụng Plotly Express
            fig5 = px.bar(summary_df, x='Kiểu liên lạc', y='Số lượng', title='Số Lượng Liên Lạc Theo Kênh',
                        labels={'Kiểu liên lạc': 'Kênh Liên Lạc', 'Số lượng': 'Số Lượng'},
                        color='Kiểu liên lạc', barmode='group')

            # Cập nhật layout của biểu đồ
            fig5.update_layout(xaxis_title='Kênh Liên Lạc', yaxis_title='Số Lượng',
                            yaxis=dict(gridcolor='gray', gridwidth=0.5),
                            xaxis=dict(gridcolor='gray', gridwidth=0.5))
            # Hiển thị biểu đồ trên Streamlit
            st.plotly_chart(fig5)
        col10,col11=st.columns(2)
        with col10:
            grouped_data = data.groupby(['Tháng', 'Trạng thái']).size().reset_index(name='Counts')  
            # Create a stacked bar chart
            fig6 = px.bar(grouped_data, x='Tháng', y='Counts', color='Trạng thái',
                        title='Số lượng liên hệ qua các Tháng theo Trạng thái của khách hàng',
                        labels={'Counts': 'Số Lượng Liên Hệ', 'Tháng': 'Tháng', 'Trạng thái': 'Trạng thái'})
            fig6.update_layout(xaxis=dict(type='category'))  # Ensure that months are treated as categorical data
            st.plotly_chart(fig6)
        with col11:
            day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            data['Day of Week'] = pd.Categorical(data['Ngày liên hệ'].dt.day_name(), categories=day_order, ordered=True)

            # Filter out any rows where the month might be 0 or invalid
            data = data[data['Ngày liên hệ'].dt.month != 0]

            grouped_data = data.groupby(['Day of Week', data['Ngày liên hệ'].dt.month]).size().unstack()

            fig7 = go.Figure(data=go.Heatmap(
                z=grouped_data.values,
                x=grouped_data.columns,
                y=grouped_data.index,
                colorscale='Blues',
                text=grouped_data.applymap(lambda x: '{:.0f}'.format(x) if x != 0 else ''),
                texttemplate="%{text}",
                hoverinfo='text'
            ))

            fig7.update_layout(
                title='Số lần liên hệ theo ngày trong tuần và tháng',
                xaxis_title='Tháng',
                yaxis_title='Ngày trong tuần',
                yaxis=dict(tickmode='array', tickvals=grouped_data.index),
                font=dict(size=12),
                autosize=False
            )
            st.plotly_chart(fig7)        
    elif st.session_state['current_tab'] == "Doanh Thu":
        st.markdown("<h1 style='text-align: center; font-size: 50px;'>Tổng Quan Doanh Thu</h1>", unsafe_allow_html=True)
        unfiltered_data=data.copy()
        # Filter by age group
        age_groups = ['Tất cả'] + list(data['Khoảng Tuổi'].cat.categories)
        selected_age_group = st.selectbox("Khoảng Tuổi", age_groups)
        
        if selected_age_group == 'Tất cả':
            data = data
        else:
            data = data[data['Khoảng Tuổi'] == selected_age_group]
        total_revenue = data['Doanh thu thực thu'].sum()
        unique_course = data['Khóa học'].nunique(dropna=True)

        col_metric1, col_metric2 = st.columns(2)
        
        with col_metric1:
            st.markdown(f"<div class='metric-container'><div class='metric-label'>Tổng Doanh Thu</div>{total_revenue:,.0f} VND</div>", unsafe_allow_html=True)        
        with col_metric2:
            st.markdown(f"<div class='metric-container'><div class='metric-label'>Khóa Học</div>{unique_course}</div>", unsafe_allow_html=True)
        # Vẽ hàng đầu tiên :
        col4, col5 = st.columns(2)
        with col4:
            group_data = data.groupby('Giao cho nhân viên Sale')['Doanh thu thực thu'].sum().reset_index()
            fig = px.bar(group_data, x='Giao cho nhân viên Sale', y='Doanh thu thực thu',
                        title='Doanh thu thực thu theo Nhân viên',
                        color='Doanh thu thực thu',
                        color_continuous_scale=px.colors.sequential.Viridis)
            fig.update_layout(title='<b>Doanh thu theo Nhân viên</b>',
                            xaxis_title="Nhân viên",
                            yaxis_title="Doanh thu thực thu",
                            width=700,  # Chiều rộng của biểu đồ
                            height=600  # Chiều cao của biểu đồ)
            )
            st.plotly_chart(fig)

        with col5:
            monthly_revenue = data.groupby('Nguồn')['Doanh thu thực thu'].sum().reset_index()
            fig2 = px.bar(monthly_revenue, x='Nguồn', y='Doanh thu thực thu',
                        title='Doanh thu thực thu theo Nguồn',
                        color='Doanh thu thực thu',
                        color_continuous_scale=px.colors.sequential.Rainbow
                        )
            fig2.update_layout(
                title='<b>Doanh thu theo Nguồn</b>',
                xaxis_title="Nguồn",
                yaxis_title="Doanh thu thực thu",
                xaxis=dict(tickmode='linear'),
                width=800,  # Chiều rộng của biểu đồ
                height=600  # Chiều cao của biểu đồ
            )
            st.plotly_chart(fig2)


        col6, col7 = st.columns(2)
        with col6:
            group_data = data.groupby('Khóa học')['Doanh thu thực thu'].sum().reset_index()
            fig3 = px.bar(group_data, x='Khóa học', y='Doanh thu thực thu',
                            title='Doanh thu thực thu theo Nhân viên',
                            color='Doanh thu thực thu',
                            color_continuous_scale=px.colors.sequential.Rainbow)
            fig3.update_layout(title='<b>Doanh thu theo Khóa học</b>',
                                xaxis_title="Khóa học",
                                yaxis_title="Doanh thu thực thu")
            st.plotly_chart(fig3)

        with col7:
            def summarize_contact_channels(data):
            # Đảm bảo không có giá trị NaN nào trong các cột channel
                data[['Channel_1', 'Channel_2', 'Channel_3']] = data[['Channel_1', 'Channel_2', 'Channel_3']].fillna('')

                # Tính tổng doanh thu cho mỗi kênh
                revenue_by_channel = {
                    'SĐT': data[data['Channel_1'] == 'SĐT']['Doanh thu thực thu'].sum(),
                    'Facebook': data[data['Channel_2'] == 'Facebook']['Doanh thu thực thu'].sum(),
                    'Zalo': data[data['Channel_3'] == 'Zalo']['Doanh thu thực thu'].sum()
                }

                # Chuyển dictionary thành DataFrame
                summary_dff = pd.DataFrame(list(revenue_by_channel.items()), columns=['Kiểu liên lạc', 'Doanh thu thực thu'])
                return summary_dff
            # Chuyển đổi cột 'Doanh thu thực thu' sang kiểu số, sử dụng 'coerce' để chuyển các không thể chuyển đổi thành NaN
            data['Doanh thu thực thu'] = pd.to_numeric(data['Doanh thu thực thu'], errors='coerce')
            # Sau đó bạn có thể tiếp tục tính toán mà không lo lỗi kiểu dữ liệu
            summary_dff = summarize_contact_channels(data)
            fig4 = px.bar(summary_dff, x='Kiểu liên lạc', y='Doanh thu thực thu', title='Doanh thu thực thu theo kênh liên lạc',
                        labels={'Kiểu liên lạc': 'Kênh Liên Lạc', 'Doanh Thu': 'Doanh thu thực thu'},
                        color='Kiểu liên lạc', barmode='group')

            # Cập nhật layout của biểu đồ
            fig4.update_layout(xaxis_title='Kênh Liên Lạc', yaxis_title='Doanh thu thực thu',
                            yaxis=dict(gridcolor='gray', gridwidth=0.5),
                            xaxis=dict(gridcolor='gray', gridwidth=0.5))
            # Hiển thị biểu đồ trên Streamlit
            st.plotly_chart(fig4)
        col8, col9 = st.columns(2)
        with col8:
            monthly_revenue = data.groupby('Tháng')['Doanh thu thực thu'].sum().reset_index()
            fig5 = px.line(monthly_revenue, x='Tháng', y='Doanh thu thực thu',
                        title='Doanh thu thực thu theo Tháng',
                        markers=True)
            fig5.update_layout(title='<b>Doanh thu theo Tháng</b>',
                            xaxis_title="Tháng",
                            yaxis_title="Doanh thu thực thu",
                            xaxis=dict(tickmode='linear'))
            st.plotly_chart(fig5)
        with col9:
            fig = px.scatter(data, x='Tuổi', y='Doanh thu thực thu', trendline="ols",
                labels={
                    "Tuổi": "Tuổi",
                    "Doanh thu thực thu": "Doanh thu thực thu (VND)"
                },
                title='Doanh thu thực thu theo Tuổi')

            fig.update_layout(transition_duration=150)
            st.plotly_chart(fig)
            ## pareto
            age_data = unfiltered_data.groupby('Khoảng Tuổi')['Doanh thu thực thu'].sum().reset_index().sort_values(by='Doanh thu thực thu', ascending=False)
            age_data['Cummulative %'] = (age_data['Doanh thu thực thu'].cumsum() / age_data['Doanh thu thực thu'].sum()) * 100
            # Plotting Pareto chart
            fig = go.Figure()
            # Thêm biểu đồ cột
            fig.add_trace(go.Bar(
                x=age_data['Khoảng Tuổi'],
                y=age_data['Doanh thu thực thu'],
                name='Doanh thu',
                marker=dict(color=px.colors.qualitative.Plotly)  # Bảng màu sáng
            ))

            # Thêm biểu đồ đường cho phần trăm tích lũy
            fig.add_trace(go.Scatter(
                x=age_data['Khoảng Tuổi'],
                y=age_data['Cummulative %'],
                name='Cumulative %',
                marker_color='red',  # Thay đổi màu đường thành màu vàng
                yaxis='y2'
            ))

            # Cập nhật bố cục với hai trục y
            fig.update_layout(
                title='<b>Biểu đồ Pareto Doanh thu theo Khoảng Tuổi</b>',
                xaxis_title="Khoảng Tuổi",
                yaxis=dict(
                    title='Doanh thu thực thu',
                    titlefont=dict(color='black'),  # Thay đổi màu chữ thành trắng
                    tickfont=dict(color='black')  # Thay đổi màu số liệu trục thành trắng
                ),
                yaxis2=dict(
                    title='Cumulative Percentage',
                    titlefont=dict(color='red'),  # Thay đổi màu chữ của trục y2
                    tickfont=dict(color='red'),  # Thay đổi màu số liệu trục y2
                    anchor='x',
                    overlaying='y',
                    side='right'
                )
            )

        # Hiển thị biểu đồ
        st.plotly_chart(fig)


   
if __name__ == "__main__":
    main()
