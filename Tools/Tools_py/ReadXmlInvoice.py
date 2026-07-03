import xml.etree.ElementTree as ET
import pandas as pd
import os
from tkinter import Tk, filedialog
import traceback
from datetime import datetime

# ==========================
# TẠO FILE LOG
# ==========================
LOG_FILE = "error.log"

def write_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

# ==========================
# HÀM LẤY TEXT AN TOÀN
# ==========================
def get_text(node, path):
    el = node.find(path)
    return el.text.strip() if el is not None and el.text else ""

# ==========================
# XỬ LÝ 1 FILE XML (NHIỀU DÒNG HÀNG)
# ==========================
def parse_invoice(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except Exception as e:
        write_log(f"Lỗi đọc XML: {xml_path} — {e}")
        return []

    # Thông tin chung hóa đơn
    common = {
        "File": os.path.basename(xml_path),
        "Số hóa đơn": get_text(root, ".//SHDon"),
        "Ngày hóa đơn": get_text(root, ".//NLap"),
        "Ký hiệu hóa đơn": get_text(root, ".//KHHDon"),

        "Đơn vị bán hàng": get_text(root, ".//NBan/Ten"),
        "MST người bán": get_text(root, ".//NBan/MST"),
        "Địa chỉ người bán": get_text(root, ".//NBan/DChi"),

        "Biển số xe": get_text(root, ".//NBan/TTKhac/TTin[TTruong='SoPhuongTien']/DLieu"),

        "Hình thức thanh toán": get_text(root, ".//HTTToan"),

        "Tổng tiền (trước thuế)": get_text(root, ".//TToan/TgTCThue"),
        "Tiền thuế GTGT (tổng)": get_text(root, ".//TToan/TgTThue"),
        "Tổng tiền thanh toán": get_text(root, ".//TToan/TgTTTBSo"),
    }

    rows = []

    # Lặp qua tất cả dòng hàng
    for item in root.findall(".//HHDVu"):
        try:
            vat_amount_line = get_text(item, "TTKhac/TTin[TTruong='VATAmount']/DLieu")
            amount_line = get_text(item, "TTKhac/TTin[TTruong='Amount']/DLieu")

            row = common.copy()
            row.update({
                "Tên hàng hóa dịch vụ": get_text(item, "THHDVu"),
                "Đơn vị tính": get_text(item, "DVTinh"),
                "Số lượng": get_text(item, "SLuong"),
                "Đơn giá": get_text(item, "DGia"),
                "Thành tiền (dòng)": get_text(item, "ThTien"),
                "Thuế suất": get_text(item, "TSuat"),
                "Tiền thuế GTGT (dòng)": vat_amount_line,
                "Tổng tiền dòng (Amount)": amount_line,
            })
            rows.append(row)

        except Exception as e:
            write_log(f"Lỗi xử lý dòng hàng trong file {xml_path}: {e}")
            write_log(traceback.format_exc())

    return rows

# ==========================
# CHỌN THƯ MỤC CHỨA XML
# ==========================
Tk().withdraw()
folder = filedialog.askdirectory(title="Chọn thư mục chứa các file XML")

if not folder:
    print("Bạn chưa chọn thư mục.")
    exit()

# ==========================
# DUYỆT TẤT CẢ FILE XML
# ==========================
all_rows = []

for file in sorted(os.listdir(folder)):
    if file.lower().endswith(".xml"):
        full_path = os.path.join(folder, file)
        try:
            rows = parse_invoice(full_path)
            all_rows.extend(rows)
            print("Đã đọc:", file)
        except Exception as e:
            write_log(f"Lỗi không xác định khi đọc file {file}: {e}")
            write_log(traceback.format_exc())

# ==========================
# GHI RA EXCEL
# ==========================
if not all_rows:
    print("Không có dữ liệu để xuất.")
else:
    df = pd.DataFrame(all_rows)
    df.to_excel("tong_hop_hoa_don.xlsx", index=False)
    print("\nĐã xuất file tong_hop_hoa_don.xlsx")

print("Nếu có lỗi, xem file error.log")