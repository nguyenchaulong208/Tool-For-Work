import sys
from Tools_py.MSK.openFile import load_excel_sheets
from Tools_py.MSK.searchKeyword import search_header
from Tools_py.MSK.convertHeader import convert_header
from Tools_py.MSK.buildData import build_data_done
from Tools_py.MSK.writeExcel import save_data_done_to_excel

def main():
    print(">> Đang đọc file Excel...")

    # Đọc tất cả sheet
    sheets, excel_path = load_excel_sheets(return_path=True)

    df_raw = sheets["DATA_RAW"]
    df_proc = sheets["DATA_PROC"]

    # Tìm header
    headers_raw = search_header(df_raw, "DATA_RAW")
    headers_proc = search_header(df_proc, "DATA_PROC")

    # Chuẩn hóa header
    df_raw = convert_header(df_raw, headers_raw)
    df_proc = convert_header(df_proc, headers_proc)

    print(">> Đang xử lý DATA_DONE...")

    # Build DATA_DONE
    data_done = build_data_done(df_raw, df_proc, headers_raw, headers_proc)

    print("Số dòng DATA_DONE:", len(data_done))
    print("5 dòng đầu:", data_done[:5])

    print(">> Đang ghi vào sheet DATA_DONE của file gốc...")

    save_data_done_to_excel(data_done, excel_path)

    print(">> Hoàn tất!")

if __name__ == "__main__":
    main()
