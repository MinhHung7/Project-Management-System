import streamlit as st
import pandas as pd
from io import BytesIO

# Thiết lập cấu hình trang
st.set_page_config(page_title='Work Description', page_icon='', layout='wide')

# Function to clear cache before running
def clear_cache():
    # For Streamlit versions 1.14 and later
    try:
        st.cache_resource.clear()
    except AttributeError:
        pass  # st.cache_data may not be available in older versions

# Gọi hàm xóa cache trước khi tải file hoặc xử lý
clear_cache()

# Kiểm tra trạng thái của file đã tải lên
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

if 'uploaded_button' not in st.session_state:
    st.session_state.uploaded_button = None

if 'work_create_button' not in st.session_state:
    st.session_state.work_create_button = None

if 'work_update_button' not in st.session_state:
    st.session_state.work_update_button = None

with st.container(border=True):
    col1, col2 = st.columns(2)
    col1_expander = col1.expander("Upload your work description")
    with col1_expander:
        st.write("Allows users to upload a CSV file containing pre-prepared work description data, enabling quick import and display of information for management.")
        uploaded_button = col1_expander.button("Confirm upload")
    
    col2_expander = col2.expander("Create your work description")
    with col2_expander:
        st.write("Allows users to create a new work description directly on the application interface, entering each field and building the data table from scratch.")
        work_create_button = col2_expander.button("Confirm create")

# Hiển thị nút upload và xử lý trạng thái
if uploaded_button or st.session_state.uploaded_button is not None:
    uploaded_button = True
    st.session_state.uploaded_button = uploaded_button

    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    # Kiểm tra nếu file được tải lên
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(f"Uploaded file: {uploaded_file.name}")
        st.session_state.uploaded_file = df
        st.session_state.uploaded_button = None  # Reset button state after uploading

if work_create_button or st.session_state.work_create_button is not None:
    # Form input
    st.session_state.work_create_button = work_create_button

    with st.form(key='work_description_form'):
        # Công việc
        task = st.text_area("Công việc")

        # Chi tiết công việc
        job_details = st.text_area("Chi tiết công việc")
        
        # Người thực hiện
        person_in_charge = st.text_input("Người thực hiện")
        
        # Deadlines
        deadline = st.date_input("Deadlines", min_value=pd.to_datetime("today").date())
        
        # Ghi chú
        notes = st.text_area("Ghi chú")
        
        # Ưu tiên
        priority = st.selectbox("Ưu tiên", ["Thấp", "Trung bình", "Cao"])
        
        # Kết quả mong đợi
        expected_result = st.text_area("Kết quả mong đợi")
        
        # Submit button
        submit_button = st.form_submit_button(label="Submit")
    
    # Xử lý khi người dùng nhấn submit
    if submit_button:
        ####################################################
        # Cập nhật data
        if st.session_state.uploaded_file is None:
            df = pd.DataFrame(columns=[
                "Công việc",
                "Chi tiết công việc",
                "Người thực hiện",
                "Tiến độ (%)",
                "Ngày bắt đầu",
                "Deadlines",
                "Ngày hoàn thành",
                "Tài nguyên liên quan",
                "Ghi chú",
                "Ưu tiên",
                "Vai trò",
                "Rủi ro, khó khăn",
                "Kết quả mong đợi",
                "Kết quả thực tế",
                "Đánh giá chất lượng",
                "Người phê duyệt", 
                "Công cụ sử dụng",
                "Tài liệu tham chiếu", 
            ])

        else:
            df = st.session_state.uploaded_file
        ##########################################
        # Tạo dictionary để thêm vào DataFrame
        new_data = {
            "Công việc": task,
            "Chi tiết công việc": job_details,
            "Người thực hiện": person_in_charge,
            "Tiến độ (%)": None,
            "Ngày bắt đầu": None,
            "Deadlines": deadline,
            "Ngày hoàn thành": None,
            "Tài nguyên liên quan": None,
            "Ghi chú": notes,
            "Ưu tiên": priority,
            "Vai trò": None,
            "Rủi ro, khó khăn": None,
            "Kết quả mong đợi": expected_result,
            "Kết quả thực tế": None,
            "Đánh giá chất lượng": None,
            "Người phê duyệt": None,
            "Công cụ sử dụng": None,
            "Tài liệu tham chiếu": None,
        }

        # Thêm dữ liệu vào DataFrame
        df = df.append(new_data, ignore_index=True)
        st.session_state.uploaded_file = df

        st.session_state.work_create_button = None
        st.dialog("Form has been successfully submitted!")

        # Ẩn form sau khi submit
        st.rerun()


# Hiển thị DataFrame
if st.session_state.uploaded_file is not None:
    df = st.session_state.uploaded_file
    # Convert 'Ngày bắt đầu' column to datetime format
    df['Ngày bắt đầu'] = pd.to_datetime(df['Ngày bắt đầu'], format='%Y-%m-%d')
    df['Deadlines'] = pd.to_datetime(df['Deadlines'], format='%Y-%m-%d')
    df['Ngày hoàn thành'] = pd.to_datetime(df['Ngày hoàn thành'], format='%Y-%m-%d')
    st.subheader("Your work descriptions (editable)")
    df = st.data_editor(df,
                   column_config={
                       "Tiến độ (%)": st.column_config.NumberColumn(format="%d %%", min_value=0, max_value=100, step=1),
                       "Ngày bắt đầu": st.column_config.DateColumn(format="DD.MM.YYYY"),
                       "Deadlines": st.column_config.DateColumn(format="DD.MM.YYYY"),
                       "Ngày hoàn thành": st.column_config.DateColumn(format="DD.MM.YYYY"),
                       "Ưu tiên": st.column_config.SelectboxColumn(options=["Cao", "Trung Bình", "Thấp"]),
                       "Đánh giá chất lượng": st.column_config.NumberColumn(format="%f ⭐", min_value=0, max_value=10),
                       "Tài liệu tham chiếu": st.column_config.LinkColumn(width="medium"),
                   })
    
    with st.expander("Overview of your work description (uneditable)"):
        text_df = st.table(df)

    st.session_state.uploaded_file = df

    # with st.popover("Edit", icon="🔄"):
    #     row_index = st.number_input("What's the task index? (Enter a number)", min_value=0, max_value=len(df)-1, step=1)
    #     work_edit_submit_button = st.button("Submit")

    # if row_index is not None and work_edit_submit_button:
    #     with st.expander(f"Edit Task {row_index}"):
    #         df.loc[row_index, 'Chi tiết công việc'] = st.text_input("Chi tiết công việc", df.loc[row_index, 'Chi tiết công việc'])
    #         df.loc[row_index, 'Người thực hiện'] = st.text_input("Người thực hiện", df.loc[row_index, 'Người thực hiện'])
    #         df.loc[row_index, 'Tiến độ (%)'] = st.number_input("Tiến độ (%)", min_value=0, max_value=100, value=df.loc[row_index, 'Tiến độ (%)'], step=1)
    #         df.loc[row_index, 'Ngày bắt đầu'] = st.date_input("Ngày bắt đầu", pd.to_datetime(df.loc[row_index, 'Ngày bắt đầu']))
    #         df.loc[row_index, 'Ưu tiên'] = st.selectbox("Ưu tiên", ['Cao', 'Trung Bình', 'Thấp'], index=['Cao', 'Trung Bình', 'Thấp'].index(df.loc[row_index, 'Ưu tiên']))

    #         if st.button("Edit Submit"):
    #             st.session_state.uploaded_file = df
    #             st.rerun()
# Nút Save
# Lưu tệp CSV sau khi người dùng nhấn nút "Save"
if st.session_state.uploaded_file is not None:
    temp_df = st.session_state.uploaded_file

    csv_data = temp_df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')

    st.download_button(
            label="Save",
            data=csv_data,
            file_name="project_management.csv",
            mime="text/csv"
        )
