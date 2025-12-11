import streamlit as st
import file_preview, file_merger
from io import BytesIO
import pandas as pd

st.title("Excel Tool 🚀")

# Upload nhiều file Excel
uploaded_files = st.file_uploader("Chọn file Excel", type=["xlsx"], accept_multiple_files=True)

if uploaded_files:
    # --- Xem trước dữ liệu ---
    st.markdown("### Xem trước dữ liệu")
    file_choice = st.selectbox("Chọn file để xem trước", uploaded_files, format_func=lambda f: f.name)
    if file_choice:
        sheets = file_preview.get_sheets(file_choice)
        sheet_choice_preview = st.selectbox("Chọn sheet để xem trước", sheets, key="preview_sheet")
        if sheet_choice_preview:
            df_preview = file_preview.preview_sheet(file_choice, sheet_choice_preview)
            st.dataframe(df_preview)

    st.markdown("---")
    st.markdown("### Thiết lập gộp dữ liệu")

    selections = []
    for f in uploaded_files:
        with st.expander(f"Thiết lập cho: {f.name}", expanded=False):
            sheets = file_preview.get_sheets(f)
            # Cho phép chọn nhiều sheet
            sheet_sel = st.multiselect(f"Chọn sheet trong {f.name}", sheets, key=f"{f.name}_sheets")

            if sheet_sel:
                # Preview sheet đầu tiên trong danh sách chọn
                df_tmp = file_preview.preview_sheet(f, sheet_sel[0], nrows=20)
                st.dataframe(df_tmp)

                # Chọn cột
                cols = list(df_tmp.columns)
                cols_sel = st.multiselect("Chọn cột cần gộp (bỏ trống = tất cả)", cols, key=f"{f.name}_cols")

                # Nhập dòng bắt đầu gộp
                start_row = st.number_input("Muốn gộp từ dòng số:", min_value=0, value=0, key=f"{f.name}_start")

                selections.append({
                    "file": f,
                    "sheets": sheet_sel,
                    "columns": cols_sel if cols_sel else None,
                    "start_row": start_row
                })

    st.markdown("---")
    st.markdown("### Gộp và xuất file")

    output_name = st.text_input("Tên file xuất (xlsx)", value="merged_result.xlsx")
    if st.button("Gộp file"):
        try:
            merged = file_merger.merge_selected(selections)
            st.subheader("Kết quả gộp")
            st.dataframe(merged.head(50))

            # Lưu file mới ra ổ đĩa
            path = file_merger.save_file(merged, output_name)
            st.success(f"Đã tạo file mới: {path}")

            # Cho phép tải trực tiếp
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                merged.to_excel(writer, index=False)
            buffer.seek(0)

            st.download_button(
                label="Tải file kết quả",
                data=buffer.getvalue(),
                file_name=output_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        except Exception as e:
            st.error(f"Lỗi khi gộp: {e}")
