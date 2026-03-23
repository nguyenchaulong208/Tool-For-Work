from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from tabulate import tabulate
import sqlite3
import datetime
import time

URL = "https://www.mihong.vn/gia-vang-trong-nuoc"

def clean_number(text):
    """Xóa dấu phẩy, dấu chấm và chuyển thành số"""
    return int(text.replace(".", "").replace(",", "").strip())

def crawl_once():
    # Khởi tạo Chrome headless
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(URL)
    time.sleep(3)  # chờ React load dữ liệu

    rows_display = []

    # 2 bảng giá
    selectors = [
        '//div[@data-testid="gold-table-1"]//tbody/tr',
        '//div[@data-testid="gold-table-2"]//tbody/tr'
    ]

    # SQLite
    conn = sqlite3.connect("gold.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS gold_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        buy INTEGER,
        sell INTEGER,
        updated_at TEXT,
        crawled_at TEXT
    )
    """)

    for xpath in selectors:
        rows = driver.find_elements(By.XPATH, xpath)
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 4:
                continue

            gold_type = cols[0].text.strip()
            updated_at = cols[1].text.split("\n")[-1].strip()

            buy_text = cols[2].text.split("\n")[0].strip()
            sell_text = cols[3].text.split("\n")[0].strip()

            buy = clean_number(buy_text)

            sell = None
            if sell_text != "-":
                sell = clean_number(sell_text)

            # Lưu SQLite
            cur.execute("""
                INSERT INTO gold_prices (type, buy, sell, updated_at, crawled_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                gold_type,
                buy,
                sell,
                updated_at,
                datetime.datetime.now().isoformat()
            ))

            # Thêm vào bảng hiển thị
            rows_display.append([
                gold_type,
                f"{buy:,}".replace(",", "."),
                f"{sell:,}".replace(",", ".") if sell else "-",
                updated_at
            ])

    conn.commit()
    conn.close()
    driver.quit()

    # Hiển thị bảng
    print("\n=== GIÁ VÀNG HIỆN TẠI (Mi Hồng) ===")
    print(tabulate(rows_display, headers=["Loại", "Mua", "Bán", "Cập nhật"], tablefmt="fancy_grid"))
    print("Lần crawl:", datetime.datetime.now().strftime("%H:%M:%S"))

# AUTO CRAWL 5 PHÚT / LẦN
while True:
    crawl_once()
    print("Chờ 5 phút để crawl tiếp...\n")
    time.sleep(300)
