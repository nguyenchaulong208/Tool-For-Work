import sqlite3
import pandas as pd
from tkinter import Tk, filedialog

# Chọn file SQLite
def choose_database():
    root = Tk()
    root.withdraw()
    db_path = filedialog.askopenfilename(
        title="Chọn file SQLite",
        filetypes=[("SQLite Database", "*.db *.sqlite *.sqlite3"), ("All files", "*.*")]
    )
    root.destroy()
    return db_path

# Chọn nơi lưu file xuất
def choose_output_file(ext):
    root = Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        title="Lưu file xuất",
        defaultextension=ext,
        filetypes=[(f"{ext.upper()} file", f"*{ext}")]
    )
    root.destroy()
    return file_path

# Lấy danh sách bảng
def get_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return [t[0] for t in cursor.fetchall()]

# Xuất dữ liệu bảng
def export_table(db_path, table_name, output_path):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f'SELECT * FROM "{table_name}"', conn)
    conn.close()

    if output_path.endswith(".json"):
        df.to_json(output_path, orient="records", indent=4, force_ascii=False)
    else:
        df.to_excel(output_path, index=False)

    print(f"Đã xuất bảng {table_name} → {output_path}")


# MAIN
db = choose_database()
if not db:
    print("Bạn chưa chọn database.")
    exit()

conn = sqlite3.connect(db)
tables = get_tables(conn)
conn.close()

print("Các bảng trong database:")
for i, t in enumerate(tables):
    print(f"{i+1}. {t}")

index = int(input("Nhập số thứ tự bảng muốn xuất: ")) - 1
table_name = tables[index]

fmt = input("Xuất ra (json/excel): ").strip().lower()
ext = ".json" if fmt == "json" else ".xlsx"

output = choose_output_file(ext)
if not output:
    print("Bạn chưa chọn nơi lưu.")
    exit()

export_table(db, table_name, output)