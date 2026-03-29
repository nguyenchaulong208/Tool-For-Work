import sqlite3
import pandas as pd
import json
from datetime import datetime
import requests
from tkinter import Tk, filedialog

# ==========================
# CONFIG
# ==========================
LLM_ENDPOINT = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "qwen3-8b"   # đúng với tên model trong LM Studio


# ==========================
# FILE DIALOG
# ==========================
def choose_db(title):
    root = Tk()
    root.withdraw()
    path = filedialog.askopenfilename(
        title=title,
        filetypes=[("SQLite DB", "*.db"), ("All files", "*.*")]
    )
    return path


# ==========================
# LOAD DB (TỰ NHẬN BẢNG)
# ==========================
def load_db(path):
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cur.fetchall()]

    if not tables:
        raise Exception(f"❌ File {path} không có bảng nào.")

    target_table = None
    for name in ["gold_prices", "silver_prices"]:
        if name in tables:
            target_table = name
            break

    if not target_table:
        for table in tables:
            cur.execute(f"PRAGMA table_info({table})")
            cols = [c[1] for c in cur.fetchall()]
            if {"buy", "crawled_at"}.issubset(cols):
                target_table = table
                break

    if not target_table:
        raise Exception(f"❌ Không tìm thấy bảng dữ liệu giá trong file {path}.")

    print(f"📌 Đang đọc bảng: {target_table}")

    df = pd.read_sql_query(
        f"SELECT * FROM {target_table} ORDER BY crawled_at ASC",
        conn
    )

    conn.close()
    df["crawled_at"] = pd.to_datetime(df["crawled_at"])
    return df


# ==========================
# TÓM TẮT DỮ LIỆU (GỌN, CHO LLM)
# ==========================
def summarize_timeseries(df, key_name):
    result = {}
    for t in df[key_name].unique():
        sub = df[df[key_name] == t].sort_values("crawled_at")

        prices = sub["buy"].dropna()
        if len(prices) == 0:
            continue

        prices = prices.astype(int)

        result[t] = {
            "first_price": int(prices.iloc[0]),
            "last_price": int(prices.iloc[-1]),
            "min_price": int(prices.min()),
            "max_price": int(prices.max()),
            "mean_price": float(round(prices.mean(), 2)),
            "change_percent": float(round((prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0] * 100, 2)),
            "first_time": str(sub["crawled_at"].iloc[0]),
            "last_time": str(sub["crawled_at"].iloc[-1]),
            "num_points": int(len(prices)),
        }

    return result


# ==========================
# GỌI LLM LOCAL (LM STUDIO)
# ==========================
def ask_llm(prompt):
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
    }

    response = requests.post(LLM_ENDPOINT, json=payload)
    print("LLM RAW RESPONSE:", response.text[:500], "...\n")  # debug ngắn

    try:
        data = response.json()
    except Exception:
        return "❌ LLM trả về dữ liệu không phải JSON."

    if "choices" not in data:
        return f"❌ LLM lỗi: {data}"

    return data["choices"][0]["message"]["content"]


# ==========================
# MAIN
# ==========================
def main():
    print("📂 Chọn file GOLD DB...")
    gold_db = choose_db("Chọn file gold.db")

    print("📂 Chọn file SILVER DB...")
    silver_db = choose_db("Chọn file silver.db")

    print("📥 Đang tải dữ liệu vàng...")
    gold_df = load_db(gold_db)

    print("📥 Đang tải dữ liệu bạc...")
    silver_df = load_db(silver_db)

    print("📊 Đang tóm tắt dữ liệu vàng...")
    gold_summary = summarize_timeseries(gold_df, "type")

    print("📊 Đang tóm tắt dữ liệu bạc...")
    silver_summary = summarize_timeseries(silver_df, "product")

    prompt = f"""
Bạn là chuyên gia phân tích thị trường vàng bạc.

Dưới đây là dữ liệu ĐÃ ĐƯỢC TÓM TẮT từ lịch sử giá vàng và bạc (đã tính sẵn min, max, giá đầu, giá cuối, trung bình, % thay đổi).

Hãy phân tích theo các tiêu chí:

1. Xu hướng tổng thể của từng loại vàng và từng loại bạc.
2. Loại nào biến động mạnh nhất, loại nào ổn định nhất (dựa trên % thay đổi và khoảng min-max).
3. So sánh mức độ biến động giữa vàng và bạc.
4. Nhận diện các loại có xu hướng tăng dài hạn, giảm dài hạn, hoặc sideway.
5. Đưa ra nhận xét cho nhà đầu tư ngắn hạn và trung hạn.
6. Tóm tắt lại 5 insight quan trọng nhất.

Dữ liệu vàng (đã tóm tắt):
{json.dumps(gold_summary, indent=2, ensure_ascii=False)}

Dữ liệu bạc (đã tóm tắt):
{json.dumps(silver_summary, indent=2, ensure_ascii=False)}

Yêu cầu:
- Trả lời bằng tiếng Việt.
- Viết rõ ràng, có tiêu đề, gạch đầu dòng.
- Không cần nhắc lại toàn bộ số liệu, chỉ cần trích số liệu khi cần minh họa.
"""

    print("🤖 Đang gửi dữ liệu cho mô hình AI local...")
    analysis = ask_llm(prompt)

    print("\n==============================")
    print("📊 PHÂN TÍCH TỪ MÔ HÌNH LOCAL")
    print("==============================\n")
    print(analysis)


if __name__ == "__main__":
    main()
