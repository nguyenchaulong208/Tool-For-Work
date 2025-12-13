import streamlit as st
import file_preview
from ui_components import upload_files, select_sheets, edit_dataframe
from data_operations import merge_data
from file_io import save_and_download

def run_workflow():
    uploaded_files = upload_files()

    if uploaded_files:
        st.markdown("### Thiết lập gộp dữ liệu")
        selections = []

        for f in uploaded_files:
            with st.expander(f"Thiết lập cho: {f.name}", expanded=False):
                sheets = file_preview.get_sheets(f)
                sheet_sel = select_sheets(f, sheets)

                if sheet_sel:
                    for sheet in sheet_sel:
                        df = file_preview.preview_sheet(f, sheet)
                        edited_df, start_row = edit_dataframe(df, sheet, f)

                        st.session_state[f"edited_{f.name}_{sheet}"] = edited_df

                        selections.append({
                            "file": f,
                            "sheet": sheet,
                            "columns": None,
                            "start_row": start_row,
                            "key": f"edited_{f.name}_{sheet}"
                        })

        st.markdown("---")
        st.markdown("### Gộp và xuất file")

        output_name = st.text_input("Tên file xuất (xlsx)", value="merged_result.xlsx")
        if st.button("Gộp file"):
            try:
                merged = merge_data(selections, st.session_state, file_preview)
                st.subheader("Kết quả gộp")
                st.dataframe(merged.head(50))
                save_and_download(merged, output_name)
            except Exception as e:
                st.error(f"❌ Lỗi khi gộp: {e}")