import streamlit as st
import pandas as pd
import numpy as np
import re

st.set_page_config(layout="wide")

# ============================
# HÀM CHUẨN HÓA
# ============================

def normalize_amount(text):
    if not text:
        return ""
    return text.replace(".", "").replace(",", "").replace(" ", "")

def format_money(value):
    try:
        num = float(value)
        return f"{num:,.0f}"
    except:
        return value

# ============================
# HÀM TÌM KIẾM
# ============================

def search_keyword(df, keyword):
    df_str = df.astype(str)
    mask = df_str.apply(lambda row: row.str.contains(keyword, case=False, na=False)).any(axis=1)
    return df[mask]

def search_in_two_fixed_columns(df, amounts):
    # Cột F và G tương ứng index 5 và 6
    col1 = df.columns[5]   # F
    col2 = df.columns[6]   # G

    df_copy = df.copy()
    df_copy[col1] = df_copy[col1].astype(str).apply(normalize_amount)
    df_copy[col2] = df_copy[col2].astype(str).apply(normalize_amount)

    # OR — chỉ cần trùng 1 trong 2 cột
    mask = df_copy[col1].isin(amounts) | df_copy[col2].isin(amounts)

    return df[mask]

# ============================
# GIAO DIỆN
# ============================

st.title("🔍 Công cụ tìm kiếm nâng cao trong Excel")

uploaded_file = st.file_uploader("📂 Chọn file Excel", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, dtype=str)
    st.success("Đã tải file thành công!")
    st.dataframe(df.head(), use_container_width=True)

    st.divider()

    # ============================
    # 🔤 TÌM THEO TỪ KHÓA (MỤC CHÍNH)
    # ============================
    st.subheader("🔤 Tìm theo từ khóa (mã chứng từ, diễn giải, TK đối ứng...)")
    keyword = st.text_input("Nhập từ khóa:")

    if keyword:
        kw = normalize_amount(keyword)
        result = search_keyword(df, kw)
        st.write(f"🔎 Kết quả ({len(result)} dòng):")

        result_display = result.applymap(format_money)
        st.dataframe(result_display, use_container_width=True)

    st.divider()

    # ============================
    # 💰 TÌM THEO SỐ TIỀN TRONG 2 CỘT F & G
    # ============================
    st.subheader("💰 Tìm theo số tiền trong 2 cột cố định (F và G)")

    st.caption("👉 Nếu nhập nhiều số tiền, hãy dùng dấu **;** để phân tách. Ví dụ: `294,300; 831,818`")

    amount_input = st.text_input("Nhập số tiền:")

    if amount_input:
        # Tách theo dấu ; hoặc xuống dòng — KHÔNG tách theo dấu phẩy
        raw_amounts = [x.strip() for x in re.split(r"[;\n]+", amount_input) if x.strip()]
        amounts = [normalize_amount(x) for x in raw_amounts if normalize_amount(x)]

        result = search_in_two_fixed_columns(df, amounts)
        st.write(f"🔎 Kết quả ({len(result)} dòng):")

        result_display = result.applymap(format_money)
        st.dataframe(result_display, use_container_width=True)
