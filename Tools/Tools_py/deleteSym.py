import os
import csv
import ast
import ctypes
from tkinter import Tk
from tkinter.filedialog import askopenfilename

TARGET_DRIVE = "F:\\"
FILE_ATTRIBUTE_REPARSE_POINT = 0x0400

def is_reparse_point(path):
    try:
        attrs = ctypes.windll.kernel32.GetFileAttributesW(path)
        if attrs == -1:
            return False
        return bool(attrs & FILE_ATTRIBUTE_REPARSE_POINT)
    except:
        return False

def delete_path(path):
    try:
        if os.path.isdir(path):
            os.rmdir(path)
        else:
            os.remove(path)
        return True
    except Exception as e:
        return str(e)

def parse_target(raw):
    if not raw or raw.strip() == "":
        return None
    try:
        parsed = ast.literal_eval(raw)
        if isinstance(parsed, list) and len(parsed) > 0:
            return parsed[0]
        return None
    except:
        return None

def main():
    Tk().withdraw()

    print("Chọn file CSV kết quả quét symlink...")
    csv_file = askopenfilename(
        title="Chọn file symlink_deep_report.csv",
        filetypes=[("CSV Files", "*.csv")]
    )

    if not csv_file:
        print("Không chọn file nào. Thoát.")
        return

    print(f"Đã chọn file: {csv_file}")

    to_delete = []

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_target = row.get("target", "")
            path = row.get("path", "").strip()

            target = parse_target(raw_target)

            if target and target.startswith(TARGET_DRIVE):
                to_delete.append(path)

    print(f"Tìm thấy {len(to_delete)} symlink/junction trỏ về ổ {TARGET_DRIVE}")

    for path in to_delete:
        if not os.path.exists(path):
            print(f"[SKIP] Không tồn tại: {path}")
            continue

        if not is_reparse_point(path):
            print(f"[SKIP] Không phải reparse point: {path}")
            continue

        result = delete_path(path)
        if result is True:
            print(f"[OK] Đã xóa: {path}")
        else:
            print(f"[ERR] Không thể xóa {path}: {result}")

    print("Hoàn tất.")

if __name__ == "__main__":
    main()