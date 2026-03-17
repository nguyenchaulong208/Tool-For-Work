import streamlit as st
import pandas as pd
import numpy as np
from tkinter import Tk, filedialog

# Hàm mở file dialog
def open_file_dialog():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Chọn file Excel",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    root.destroy()
    return file_path

# Tìm theo nhiều số tiền
def search_multiple_amounts(df, amounts):
    df_str = df.astype(str)
    mask = df_str.apply(lambda row: row.str.contains("|".join(amounts), na=False)).any(axis=1)
    return df[mask]

# Tìm theo khoảng tiền
def search_range(df, min_val, max_val):
    df_num = df.apply(pd.to_numeric, errors="coerce")
    mask = df_num.apply(lambda col: col.between(min_val, max_val)).any(axis=1)
    return df[mask]

# Tìm theo từ khóa
def search_keyword(df, keyword):
    df_str = df.astype(str)
    mask = df_str.apply(lambda row: row.str.contains(keyword, case=False, na=False)).any(axis=1)
    return df[mask]

# Giao diện Streamlit
st.title("🔍 Công cụ tìm kiếm nâng cao trong Excel")
st.write("Tìm theo nhiều số tiền, khoảng tiền hoặc từ khóa — nhanh hơn Excel rất nhiều.")

# Chọn file
if st.button("📂 Chọn file Excel"):
    file_path = open_file_dialog()
    st.session_state["file_path"] = file_path

if "file_path" in st.session_state:
    st.success(f"Đã chọn file: {st.session_state['file_path']}")

    try:
        df = pd.read_excel(st.session_state["file_path"], dtype=str)
        st.write("📄 **Xem trước dữ liệu:**")
        st.dataframe(df.head(), use_container_width=True)

        st.divider()

        # --- TÌM THEO NHIỀU SỐ TIỀN ---
        st.subheader("🔢 Tìm theo nhiều số tiền")
        amount_input = st.text_input("Nhập nhiều số tiền, cách nhau bởi dấu phẩy (ví dụ: 8318818,1500000):")

        if amount_input:
            amounts = [x.strip() for x in amount_input.split(",") if x.strip()]
            result = search_multiple_amounts(df, amounts)
            st.write(f"🔎 Kết quả ({len(result)} dòng):")
            st.dataframe(result, use_container_width=True)

        st.divider()

        # --- TÌM THEO KHOẢNG TIỀN ---
        st.subheader("📈 Tìm theo khoảng tiền")
        col1, col2 = st.columns(2)
        min_val = col1.number_input("Giá trị nhỏ nhất", min_value=0, value=0)
        max_val = col2.number_input("Giá trị lớn nhất", min_value=0, value=0)

        if max_val > 0:
            df_num = df.apply(pd.to_numeric, errors="coerce")
            result = search_range(df_num, min_val, max_val)
            st.write(f"🔎 Kết quả ({len(result)} dòng):")
            st.dataframe(result, use_container_width=True)

        st.divider()

        # --- TÌM THEO TỪ KHÓA ---
        st.subheader("🔤 Tìm theo từ khóa (mã chứng từ, diễn giải, TK đối ứng...)")
        keyword = st.text_input("Nhập từ khóa:")

        if keyword:
            result = search_keyword(df, keyword)
            st.write(f"🔎 Kết quả ({len(result)} dòng):")
            st.dataframe(result, use_container_width=True)

    except Exception as e:
        st.error(f"Lỗi khi đọc file: {e}")
