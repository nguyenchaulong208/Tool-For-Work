import string
import secrets

SPECIAL = "!@#$%^&*()-_=+[]{};:,.<>?/"

def generate_password(length=8):
    if length < 3:
        raise ValueError("Độ dài phải >= 3 để đảm bảo có chữ hoa, số và ký tự đặc biệt.")

    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    special = SPECIAL

    all_chars = lower + upper + digits + special

    # Bắt buộc có ít nhất 1 chữ hoa, 1 số, 1 ký tự đặc biệt
    password = [
        secrets.choice(upper),
        secrets.choice(digits),
        secrets.choice(special)
    ]

    # Thêm ký tự ngẫu nhiên cho đủ độ dài
    while len(password) < length:
        password.append(secrets.choice(all_chars))

    # Xáo trộn vị trí
    secrets.SystemRandom().shuffle(password)
    return "".join(password)

def ask_int(prompt):
    while True:
        val = input(prompt).strip()
        if not val:
            print("Vui lòng nhập một số.")
            continue
        if not val.isdigit():
            print("Chỉ nhập số nguyên dương.")
            continue
        n = int(val)
        if n <= 0:
            print("Số lượng phải > 0.")
            continue
        return n

def main():
    try:
        n = ask_int("Nhập số lượng mật khẩu cần sinh: ")
        passwords = [generate_password(8) for _ in range(n)]

        with open("passwords.txt", "w", encoding="utf-8") as f:
            for pw in passwords:
                f.write(pw + "\n")

        print(f"Đã sinh {n} mật khẩu và lưu vào file passwords.txt")
    except Exception as e:
        print("Có lỗi xảy ra:", e)
    finally:
        input("Nhấn Enter để thoát...")

if __name__ == "__main__":
    main()
