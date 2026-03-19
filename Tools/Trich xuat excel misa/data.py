import pandas as pd
import re
from tkinter import Tk, filedialog

# Ẩn cửa sổ Tkinter
root = Tk()
root.withdraw()

# Chọn file Excel
input_file = filedialog.askopenfilename(
    title="Chọn file Excel sổ cái MISA",
    filetypes=[("Excel files", "*.xlsx *.xls")]
)

if not input_file:
    print("Không chọn file.")
    exit()

print("Đang đọc file:", input_file)

# Đọc toàn bộ file Excel
df = pd.read_excel(input_file, header=None, dtype=str)

# Tìm vị trí bắt đầu mỗi tài khoản
start_indices = []
account_names = []

for i, row in df.iterrows():
    cell = str(row[0]) if row[0] is not None else ""
    if cell.startswith("Tài khoản:"):
        start_indices.append(i)

        # Lấy số tài khoản
        match = re.search(r"Tài khoản:\s*([0-9A-Za-z]+)", cell)
        if match:
            account_names.append(match.group(1))
        else:
            account_names.append(f"unknown_{i}")

# Thêm điểm kết thúc cuối cùng
start_indices.append(len(df))

print(f"Tìm thấy {len(account_names)} tài khoản.")

# Tách từng tài khoản
for idx in range(len(account_names)):
    start = start_indices[idx]
    end = start_indices[idx + 1] - 1

    sub_df = df.iloc[start:end+1]

    account = account_names[idx]
    output_file = f"Tai_khoan_{account}.xlsx"

    sub_df.to_excel(output_file, index=False, header=False)
    print(f"Đã xuất: {output_file}")

print("Hoàn tất tách file.")
