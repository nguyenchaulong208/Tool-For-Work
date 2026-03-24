import sqlite3
import pandas as pd
import numpy as np

DB = "gold.db"

def load_data():
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("SELECT * FROM gold_prices ORDER BY crawled_at ASC", conn)
    conn.close()
    df["crawled_at"] = pd.to_datetime(df["crawled_at"])
    return df

def analyze_all():
    df = load_data()

    print("\n=== 📌 TỔNG QUAN DỮ LIỆU ===")
    print(f"Số bản ghi: {len(df)}")
    print(f"Số loại vàng: {df['type'].nunique()}")
    print(f"Khoảng thời gian: {df['crawled_at'].min()} → {df['crawled_at'].max()}")

    results = []

    for gold_type in df["type"].unique():
        sub = df[df["type"] == gold_type].sort_values("crawled_at")

        # Tính biến động
        sub["buy_diff"] = sub["buy"].diff()
        sub["sell_diff"] = sub["sell"].diff()

        # % thay đổi
        sub["buy_pct"] = sub["buy"].pct_change() * 100
        sub["sell_pct"] = sub["sell"].pct_change() * 100

        # Độ biến động (volatility)
        buy_vol = sub["buy"].pct_change().std() * 100
        sell_vol = sub["sell"].pct_change().std() * 100

        # Tổng tăng/giảm
        total_buy_change = sub["buy"].iloc[-1] - sub["buy"].iloc[0]
        total_sell_change = sub["sell"].iloc[-1] - sub["sell"].iloc[0]

        # Điểm đảo chiều (trend reversal)
        reversals = ((sub["buy_diff"].shift(1) > 0) & (sub["buy_diff"] < 0)) | \
                    ((sub["buy_diff"].shift(1) < 0) & (sub["buy_diff"] > 0))
        reversal_count = reversals.sum()

        results.append({
            "type": gold_type,
            "first_buy": sub["buy"].iloc[0],
            "last_buy": sub["buy"].iloc[-1],
            "total_buy_change": total_buy_change,
            "volatility_buy_%": round(buy_vol, 4),
            "reversals": int(reversal_count)
        })

        print(f"\n=== 📈 PHÂN TÍCH: {gold_type} ===")
        print(f"• Giá mua đầu tiên: {sub['buy'].iloc[0]:,}")
        print(f"• Giá mua cuối cùng: {sub['buy'].iloc[-1]:,}")
        print(f"• Tổng thay đổi: {total_buy_change:+,}")
        print(f"• Biến động (volatility): {buy_vol:.4f}%")
        print(f"• Số lần đảo chiều xu hướng: {reversal_count}")

        print("\nTop 5 lần tăng mạnh nhất:")
        print(sub.nlargest(5, "buy_diff")[["crawled_at", "buy", "buy_diff"]])

        print("\nTop 5 lần giảm mạnh nhất:")
        print(sub.nsmallest(5, "buy_diff")[["crawled_at", "buy", "buy_diff"]])

    # Xuất bảng tổng hợp
    summary = pd.DataFrame(results)
    print("\n\n=== 📊 BẢNG TỔNG HỢP BIẾN ĐỘNG ===")
    print(summary)

if __name__ == "__main__":
    analyze_all()
