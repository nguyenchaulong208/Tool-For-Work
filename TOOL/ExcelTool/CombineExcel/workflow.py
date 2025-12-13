import streamlit as st
import file_preview
from ui_components import upload_files, select_sheets, edit_dataframe
from data_operations import merge_data
from file_io import save_and_download
from form_handler import preview_form_sheet, save_with_form_dynamic_by_index
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

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

        form_choice = st.selectbox("Chọn file làm form", [f.name for f in uploaded_files])
        form_file = next(f for f in uploaded_files if f.name == form_choice)
        form_sheets = file_preview.get_sheets(form_file)
        form_sheet_choice = st.selectbox("Chọn sheet trong form", form_sheets)

        df_preview = preview_form_sheet(form_file, sheet_name=form_sheet_choice)
        df_preview.reset_index(inplace=True)  # thêm cột "index" để lấy dòng

        gb = GridOptionsBuilder.from_dataframe(df_preview)
        gb.configure_selection(selection_mode="multiple", use_checkbox=True)  # tick chọn bằng checkbox
        grid_options = gb.build()

        st.subheader("📊 Tick chọn nhanh bằng checkbox")
        grid_response = AgGrid(
            df_preview,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            fit_columns_on_grid_load=True
        )

        # Lấy index các dòng đã chọn
        selected_rows = []
        selected_data = grid_response.get("selected_rows", [])
        if isinstance(selected_data, list):
            for r in selected_data:
                if isinstance(r, dict) and "index" in r:
                    selected_rows.append(r["index"])

        # Gán vùng
        region_type = st.radio("Gán vùng cho dòng đã chọn", ["Header", "Body", "Footer"])
        if st.button("Gán vùng"):
            if selected_rows:
                if region_type == "Header":
                    st.session_state["header_rows"] = selected_rows
                elif region_type == "Body":
                    st.session_state["body_rows"] = selected_rows
                elif region_type == "Footer":
                    st.session_state["footer_rows"] = selected_rows
                st.success(f"✅ Đã gán {len(selected_rows)} dòng vào vùng {region_type}")
            else:
                st.warning("⚠️ Bạn chưa tick dòng nào để gán vùng")

        # Hiển thị vùng đã gán
        st.write("Header:", st.session_state.get("header_rows", []))
        st.write("Body:", st.session_state.get("body_rows", []))
        st.write("Footer:", st.session_state.get("footer_rows", []))

        # Nút clear vùng
        if st.button("Clear Header"):
            st.session_state["header_rows"] = []
            st.info("Đã xoá vùng Header")
        if st.button("Clear Body"):
            st.session_state["body_rows"] = []
            st.info("Đã xoá vùng Body")
        if st.button("Clear Footer"):
            st.session_state["footer_rows"] = []
            st.info("Đã xoá vùng Footer")

        body_start_col = st.number_input("Cột bắt đầu body", min_value=1, value=1)

        if st.button("Gộp file"):
            try:
                merged = merge_data(selections, st.session_state, file_preview)
                st.subheader("Kết quả gộp")
                st.dataframe(merged)  # hiển thị toàn bộ dữ liệu

                save_with_form_dynamic_by_index(
                    merged=merged,
                    form_file=form_file,
                    output_name=output_name,
                    sheet_name=form_sheet_choice,
                    header_rows=st.session_state.get("header_rows", []),
                    body_rows=st.session_state.get("body_rows", []),
                    footer_rows=st.session_state.get("footer_rows", []),
                    body_start_col=body_start_col
                )

            except Exception as e:
                st.error(f"❌ Lỗi khi gộp: {e}")