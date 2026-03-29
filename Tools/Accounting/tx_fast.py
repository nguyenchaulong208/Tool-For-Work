import xml.etree.ElementTree as ET
import pandas as pd
from tkinter import Tk, filedialog

# Ẩn cửa sổ Tkinter chính
root = Tk()
root.withdraw()

# Hộp thoại chọn file
file_path = filedialog.askopenfilename(
    title="Chọn file XML Fast Online",
    filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
)

if not file_path:
    print("Không có file nào được chọn.")
    exit()

# Parse XML
tree = ET.parse(file_path)
root_xml = tree.getroot()

# Namespace Excel XML 2003
ns = {"ss": "urn:schemas-microsoft-com:office:spreadsheet"}

rows = root_xml.findall(".//ss:Row", ns)

data = []
for row in rows:
    cells = row.findall("ss:Cell", ns)
    if len(cells) >= 2:
        code_el = cells[0].find("ss:Data", ns)
        name_el = cells[1].find("ss:Data", ns)

        if code_el is not None and name_el is not None:
            code = code_el.text.strip()
            name = name_el.text.strip()

            # Bỏ dòng tiêu đề và dòng trống
            if code not in ["Mã khách", "", None]:
                data.append([code, name])

# Xuất Excel
df = pd.DataFrame(data, columns=["Mã đối tượng", "Tên đối tượng"])
df.to_excel("danh_muc_khach_hang.xlsx", index=False)

print("Đã xuất file danh_muc_khach_hang.xlsx thành công!")
