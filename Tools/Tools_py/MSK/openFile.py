import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def load_excel_sheets(return_path=False):
    # Mở file dialog để chọn file Excel
    root = Tk()
    root.withdraw()  # Ẩn cửa sổ Tkinter

    excel_path = askopenfilename(
        title="Chọn file Excel cần xử lý",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )

    if not excel_path:
        raise Exception("Bạn chưa chọn file Excel!")

    # Đọc toàn bộ sheet
    xls = pd.ExcelFile(excel_path)

    sheets = {
        name: xls.parse(name, header=None)
        for name in xls.sheet_names
    }

    # Trả về cả đường dẫn file nếu cần
    if return_path:
        return sheets, excel_path

    return sheets
