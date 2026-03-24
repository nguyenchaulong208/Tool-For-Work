import sqlite3
import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://giabac.phuquygroup.vn/"
DB = "silver.db"

def clean_number(text):
    return int(text.replace(".", "").replace(",", "").strip())

def crawl_once():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(URL)
    time.sleep(3)

    # Lấy tất cả bảng bạc
    tables = driver.find_elements(By.XPATH, "//table[contains(@class,'table-bordered')]")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS silver_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT,
        unit TEXT,
        buy INTEGER,
        sell INTEGER,
        crawled_at TEXT
    )
    """)

    rows_saved = 0

    for table in tables:
        rows = table.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) != 4:
                continue

            product = cols[0].text.strip()
            unit = cols[1].text.strip()
            buy = clean_number(cols[2].text)
            sell = clean_number(cols[3].text)

            cur.execute("""
                INSERT INTO silver_prices (product, unit, buy, sell, crawled_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                product,
                unit,
                buy,
                sell,
                datetime.datetime.now().isoformat()
            ))

            rows_saved += 1

    conn.commit()
    conn.close()
    driver.quit()

    return rows_saved


def main():
    print("🚀 Bắt đầu auto-crawl giá bạc mỗi 5 phút...\n")

    while True:
        try:
            count = crawl_once()
            now = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[{now}] ✔ Crawl xong {count} dòng dữ liệu.")
        except Exception as e:
            print("❌ Lỗi khi crawl:", e)

        print("⏳ Chờ 5 phút...\n")
        time.sleep(300)  # 5 phút


if __name__ == "__main__":
    main()
