import pandas as pd
import re
import unicodedata
from tkinter import Tk, filedialog
import os

# ============================
# BỎ DẤU TIẾNG VIỆT
# ============================
def remove_accents(input_str):
    if not isinstance(input_str, str):
        return ""
    nfkd = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])

# ============================
# CHUYỂN ĐỔI NGÀY dd/mm/yyyy → mm/dd/yyyy
# ============================
def convert_date_format(text):
    if not isinstance(text, str):
        return text
    pattern = r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b"
    def repl(match):
        d, m, y = match.groups()
        return f"{m.zfill(2)}/{d.zfill(2)}/{y}"
    return re.sub(pattern, repl, text)

# ============================
# ĐỌC FILE QUY TẮC DUY NHẤT
# ============================
def load_rules(path):
    alias_map = {}
    account_rules = []
    mode = None  # ALIAS hoặc ACCOUNT

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.upper() == "[ALIAS]":
                mode = "ALIAS"
                continue
            if line.upper() == "[ACCOUNT]":
                mode = "ACCOUNT"
                continue

            if "=" in line:
                key, val = line.split("=", 1)
                key = key.strip().upper()
                val = val.strip().upper()

                if mode == "ALIAS":
                    alias_map[key] = val
                elif mode == "ACCOUNT":
                    account_rules.append((key, val))

    return alias_map, account_rules

# ============================
# TÁCH TÊN ĐỐI TƯỢNG
# ============================
def extract_company(text):
    t = text.upper()

    m1 = re.search(r"CHO CTY\s+([A-Z0-9\s]+?)(?:-|THEO|HD|HĐ|SO|SỐ|$)", t)
    if m1:
        return m1.group(1).strip()

    m2 = re.search(r"CHO\s+([A-Z0-9\s]+?)(?:-|THEO|HD|HĐ|SO|SỐ|$)", t)
    if m2:
        return m2.group(1).strip()

    return None

# ============================
# CHƯƠNG TRÌNH CHÍNH
# ============================
def main():
    root = Tk()
    root.withdraw()

    # Đường dẫn tương đối đến file regext.txt
    rule_path = os.path.join(os.path.dirname(__file__), "regext.txt")
    alias_map, account_rules = load_rules(rule_path)

    print("Chọn file danh mục khách hàng...")
    dm_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])

    print("Chọn file dữ liệu mô tả...")
    data_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])

    # Load danh mục
    dm = pd.read_excel(dm_path)
    dm["ten_norm"] = (
        dm["Tên đối tượng"]
        .astype(str)
        .apply(remove_accents)
        .str.upper()
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    # Load dữ liệu input (A = ngày, B = mô tả) — ép toàn bộ thành chuỗi
    df = pd.read_excel(data_path, header=None, dtype=str)

    # Lấy đúng 2 cột đầu tiên
    df = df.iloc[:, :2]
    df.columns = ["ngay", "mo_ta"]

    # Chuyển đổi ngày dd/mm/yyyy → mm/dd/yyyy
    df["ngay"] = df["ngay"].apply(convert_date_format)

    # Chuẩn hóa mô tả
    df["mo_ta_norm"] = (
        df["mo_ta"]
        .astype(str)
        .apply(remove_accents)
        .str.upper()
    )

    # Tách tên đối tượng
    df["ten_cong_ty"] = df["mo_ta_norm"].apply(extract_company)

    # Áp dụng alias
    df["ten_cong_ty"] = df["ten_cong_ty"].apply(
        lambda x: alias_map.get(x, x) if isinstance(x, str) else x
    )

    # Ghép mã đối tượng
    def find_code(name):
        if not name:
            return "KR"
        for _, row in dm.iterrows():
            if name in row["ten_norm"]:
                return row["Mã đối tượng"]
        return "KR"

    df["ma_doi_tuong"] = df["ten_cong_ty"].apply(find_code)

    # Tài khoản hạch toán
    def detect_account(text):
        t = text.upper()
        for pattern, acc in account_rules:
            if re.search(pattern, t):
                return acc
        return ""

    df["tai_khoan"] = df["mo_ta_norm"].apply(detect_account)

    print("Chọn nơi lưu file kết quả...")
    output_path = filedialog.asksaveasfilename(defaultextension=".xlsx")

    df.to_excel(output_path, index=False)
    print("Đã xuất file:", output_path)

if __name__ == "__main__":
    main()
