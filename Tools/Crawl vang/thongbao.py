import sqlite3
import pandas as pd
import time
from tkinter import Tk, filedialog

def choose_db_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Chọn file gold.db",
        filetypes=[("SQLite DB", "*.db"), ("All files", "*.*")]
    )
    return file_path

def load_data(db_path):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM gold_prices ORDER BY crawled_at ASC", conn)
    conn.close()
    df["crawled_at"] = pd.to_datetime(df["crawled_at"])
    return df

def check_price_change(df):
    # Lấy 2 lần crawl gần nhất
    last_time = df["crawled_at"].max()
    prev_df = df[df["crawled_at"] < last_time]

    if prev_df.empty:
        print("⚠️ Chưa đủ dữ liệu để so sánh.")
        return

    prev_time = prev_df["crawled_at"].max()

    df_last = df[df["crawled_at"] == last_time]
    df_prev = df[df["crawled_at"] == prev_time]

    print(f"\n🔍 So sánh giá giữa:")
    print(f"• Lần mới nhất:  {last_time}")
    print(f"• Lần trước đó: {prev_time}\n")

    alert_count = 0

    for gold_type in df_last["type"].unique():
        prev_rows = df_prev[df_prev["type"] == gold_type]

        if prev_rows.empty:
            continue

        row_last = df_last[df_last["type"] == gold_type].iloc[0]
        row_prev = prev_rows.iloc[0]

        buy_diff = row_last["buy"] - row_prev["buy"]
        sell_diff = (row_last["sell"] or 0) - (row_prev["sell"] or 0)

        if buy_diff != 0 or sell_diff != 0:
            alert_count += 1
            print(f"⚠️ {gold_type} thay đổi giá:")

            if buy_diff != 0:
                print(f"  • Mua: {row_prev['buy']:,} → {row_last['buy']:,} ({buy_diff:+,})")

            if sell_diff != 0:
                print(f"  • Bán: {row_prev['sell']:,} → {row_last['sell']:,} ({sell_diff:+,})")

            print()

    if alert_count == 0:
        print("✔ Không có thay đổi giá so với lần crawl trước.")

def main():
    print("📂 Chọn file database...")
    db_path = choose_db_file()

    if not db_path:
        print("❌ Không chọn file DB. Thoát.")
        return

    print(f"📌 Đang theo dõi file: {db_path}")
    print("⏳ Script sẽ kiểm tra mỗi 5 phút...\n")

    while True:
        df = load_data(db_path)
        check_price_change(df)
        print("⏱ Chờ 5 phút để kiểm tra lại...\n")
        time.sleep(300)  # 5 phút

if __name__ == "__main__":
    main()
