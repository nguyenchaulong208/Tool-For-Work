import pandas as pd
from io import BytesIO
import streamlit as st
import file_merger

def save_and_download(merged, output_name):
    # Lưu file mới ra ổ đĩa
    path = file_merger.save_file(merged, output_name)
    st.success(f"✅ Đã tạo file mới: {path}")

    # Cho phép tải trực tiếp
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        merged.to_excel(writer, index=False)
    buffer.seek(0)

    st.download_button(
        label="📥 Tải file kết quả",
        data=buffer.getvalue(),
        file_name=output_name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )