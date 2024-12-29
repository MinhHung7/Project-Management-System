import pandas as pd
import streamlit as st
import plotly.express as px
from ydata_profiling import ProfileReport
import plotly.graph_objects as go

st.title("📅 Biểu đồ Gantt - Quản lý dự án")

if 'uploaded_file' in st.session_state and st.session_state.uploaded_file is not None:
    # Chuyển đổi dữ liệu thành DataFrame
    df = pd.DataFrame(st.session_state.uploaded_file)
    
    # Kiểm tra cột có tồn tại không
    required_columns = ['Ngày bắt đầu', 'Ngày hoàn thành', 'Công việc', 'Ưu tiên']
    if all(col in df.columns for col in required_columns):
        temp_df = df[required_columns]
        
        # Chuyển đổi kiểu dữ liệu datetime
        temp_df['Ngày bắt đầu'] = pd.to_datetime(temp_df['Ngày bắt đầu'])
        temp_df['Ngày hoàn thành'] = pd.to_datetime(temp_df['Ngày hoàn thành'])

        # Grid Layout
        col1, col2 = st.columns([2, 1])  # Tạo hai cột (col1 lớn hơn col2)

        with col1:
            st.subheader("📊 Biểu đồ Gantt")
            # Tạo biểu đồ Gantt với Plotly
            fig = px.timeline(temp_df, 
                              x_start="Ngày bắt đầu", 
                              x_end="Ngày hoàn thành", 
                              y="Công việc", 
                              color="Ưu tiên", 
                              title="Biểu đồ Gantt - Quản lý dự án",
                              labels={"Công việc": "Tên công việc", "Ưu tiên": "Mức độ ưu tiên"})
            # Tinh chỉnh biểu đồ
            fig.update_yaxes(categoryorder="total ascending")
            fig.update_layout(xaxis_title="Ngày", yaxis_title="Công việc", xaxis=dict(showgrid=True), yaxis=dict(showgrid=True))
            st.plotly_chart(fig)

            ####################################################
            # Lọc cột 'Ưu tiên' cho biểu đồ tròn
            temp_df = df
            if 'Ưu tiên' in temp_df.columns:
                st.header("📊 Biểu đồ Tròn (Pie Chart) Phân Bố Ưu Tiên")

                # Tạo bảng tần suất cho cột 'Ưu tiên'
                priority_counts = temp_df['Ưu tiên'].value_counts().reset_index()
                priority_counts.columns = ['Ưu tiên', 'Số lượng']

                # Tạo biểu đồ tròn với Plotly
                fig = px.pie(priority_counts, 
                            names='Ưu tiên', 
                            values='Số lượng', 
                            title='Biểu đồ Phân Bố Ưu Tiên Công Việc',
                            color='Ưu tiên',
                            color_discrete_map={'Cao': '#E63946', 
                                                'Trung Bình': '#F1FAEE', 
                                                'Thấp': '#457B9D'})

                # Hiển thị biểu đồ trong Streamlit
                st.plotly_chart(fig)
            else:
                st.warning("Cột 'Ưu tiên' không tồn tại trong dữ liệu. Vui lòng kiểm tra tệp Excel.")

            ####################################################

        with col2:
            st.subheader("⚙️ Bộ lọc")
            # Bộ lọc cho Mức độ ưu tiên
            priority_filter = st.multiselect("Chọn mức độ ưu tiên:", 
                                             options=temp_df['Ưu tiên'].unique(),
                                             default=temp_df['Ưu tiên'].unique())
            
            # Áp dụng bộ lọc
            filtered_df = temp_df[temp_df['Ưu tiên'].isin(priority_filter)]
            st.write("📋 **Dữ liệu sau khi lọc:**")
            st.dataframe(filtered_df)
            
            st.write("📊 **Số lượng công việc theo mức độ ưu tiên:**")
            st.bar_chart(filtered_df['Ưu tiên'].value_counts(), color="Ưu tiên")
    else:
        st.error("❌ Dữ liệu không chứa đủ các cột yêu cầu: 'Ngày bắt đầu', 'Ngày hoàn thành', 'Công việc', 'Ưu tiên'")

    ####################################################    


    st.header('📊 Biểu đồ Cột (Bar Chart) cho Tiến Độ Công Việc')

    # Lọc các cột cần thiết cho biểu đồ tiến độ
    temp_df = df[['Công việc', 'Tiến độ (%)']]

    # Chuyển đổi cột Tiến độ thành kiểu dữ liệu số
    temp_df['Tiến độ (%)'] = pd.to_numeric(temp_df['Tiến độ (%)'], errors='coerce')

    # Tạo biểu đồ cột với Plotly
    fig = px.bar(temp_df, 
                 x='Công việc', 
                 y='Tiến độ (%)', 
                 title='Biểu đồ Tiến Độ Công Việc',
                 labels={'Công việc': 'Tên công việc', 'Tiến độ (%)': 'Phần trăm hoàn thành'},
                 color='Tiến độ (%)',
                 color_continuous_scale='Viridis')

    # Cải thiện giao diện biểu đồ
    fig.update_layout(xaxis_title='Công việc',
                      yaxis_title='Tiến độ (%)',
                      xaxis={'tickangle': -45},
                      height=500)

    # Hiển thị biểu đồ trong Streamlit
    st.plotly_chart(fig)

    ####################################################

    # Kiểm tra các cột cần thiết
    if {'Ngày bắt đầu', 'Ngày hoàn thành', 'Tiến độ (%)'}.issubset(df.columns):
        
        temp_df = df

        st.header("Biểu đồ Đường (Line Chart) Tiến Độ Theo Thời Gian")

        # Chuyển đổi cột ngày sang định dạng datetime
        temp_df['Ngày bắt đầu'] = pd.to_datetime(temp_df['Ngày bắt đầu'])
        temp_df['Ngày hoàn thành'] = pd.to_datetime(temp_df['Ngày hoàn thành'])

        # Tạo một DataFrame phụ cho biểu đồ đường
        df_progress = temp_df[['Ngày bắt đầu', 'Tiến độ (%)', 'Công việc']].sort_values('Ngày bắt đầu')

        # Vẽ biểu đồ đường với Plotly
        fig = px.line(df_progress, 
                      x='Ngày bắt đầu', 
                      y='Tiến độ (%)', 
                      color='Công việc',
                      markers=True,
                      title='Biểu Đồ Tiến Độ Công Việc Theo Thời Gian',
                      labels={'Ngày bắt đầu': 'Ngày', 'Tiến độ (%)': 'Phần trăm hoàn thành', 'Công việc': 'Tên công việc'})

        # Tùy chỉnh giao diện biểu đồ
        fig.update_layout(xaxis_title="Ngày",
                          yaxis_title="Tiến độ (%)",
                          hovermode="x unified")

        # Hiển thị biểu đồ
        st.plotly_chart(fig)
    else:
        st.warning("Dữ liệu thiếu một trong các cột sau: 'Ngày bắt đầu', 'Ngày hoàn thành', 'Tiến độ (%)'. Vui lòng kiểm tra tệp Excel.")

    ########################################################

    # Kiểm tra cột cần thiết
    if 'Đánh giá chất lượng' in df.columns:
        st.header("📊 Biểu đồ Phân Phối (Histogram) Đánh Giá Chất Lượng Công Việc")

        temp_df = df
        # Lọc dữ liệu cần thiết
        df_quality = temp_df[['Công việc', 'Đánh giá chất lượng']]

        # Vẽ biểu đồ Histogram với Plotly
        fig = px.histogram(df_quality,
                           x='Đánh giá chất lượng',
                           nbins=10,
                           title='Biểu Đồ Phân Phối Đánh Giá Chất Lượng Công Việc',
                           labels={'Đánh giá chất lượng': 'Mức đánh giá chất lượng'},
                           color_discrete_sequence=['skyblue'])

        # Tùy chỉnh giao diện biểu đồ
        fig.update_layout(xaxis_title="Mức đánh giá chất lượng (1-10)",
                          yaxis_title="Số lượng công việc",
                          bargap=0.1)

        # Hiển thị biểu đồ
        st.plotly_chart(fig)
    else:
        st.warning("Dữ liệu thiếu cột 'Đánh giá chất lượng'. Vui lòng kiểm tra tệp Excel.")

    ####################################################

    # Kiểm tra cột cần thiết
    if {'Công việc', 'Tài nguyên liên quan'}.issubset(df.columns):
        
        st.header("📊 Biểu đồ Thanh Chồng (Stacked Bar Chart) Tài Nguyên Sử Dụng Theo Công Việc")

        temp_df = df

        df_exploded = temp_df.assign(**{'Tài nguyên liên quan': temp_df['Tài nguyên liên quan'].str.split(',')}).explode('Tài nguyên liên quan')
        df_exploded['Tài nguyên liên quan'] = df_exploded['Tài nguyên liên quan'].str.strip()

        # Tạo cột đếm số lượng tài nguyên cho mỗi công việc
        resource_count = df_exploded.groupby(['Công việc', 'Tài nguyên liên quan']).size().reset_index(name='Số lượng')

        # Vẽ biểu đồ thanh chồng với Plotly
        fig = px.bar(
            resource_count,
            x='Công việc',
            y='Số lượng',
            color='Tài nguyên liên quan',
            title='Biểu Đồ Thanh Chồng - Tài Nguyên Sử Dụng Theo Công Việc',
            labels={'Số lượng': 'Số lượng Tài nguyên', 'Công việc': 'Tên Công Việc'},
            barmode='stack'
        )

        # Tùy chỉnh biểu đồ
        fig.update_layout(
            xaxis_title='Công việc',
            yaxis_title='Số lượng Tài nguyên',
            legend_title='Tài nguyên'
        )

        # Hiển thị biểu đồ trong Streamlit
        st.plotly_chart(fig)
    else:
        st.warning("Dữ liệu thiếu cột 'Công việc' hoặc 'Tài nguyên liên quan'. Vui lòng kiểm tra tệp Excel.")
        ########################################################
    
    if st.button("Report Generating"):

        profile = ProfileReport(df)  # or provide a valid path
        profile.to_file("report.html")

        # Read and display the HTML file in Streamlit
        with open("report.html", "r", encoding='utf-8') as f:
            html_content = f.read()

        # Display the HTML content in Streamlit
        st.components.v1.html(html_content, height=1000, scrolling=True)

else:
    st.warning("⚠️ Vui lòng tải lên tệp dữ liệu trước.")
