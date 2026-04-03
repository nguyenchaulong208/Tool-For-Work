import os
import unicodedata
from tkinter import Tk, filedialog
from PyPDF2 import PdfReader, PdfWriter

# 1. Bỏ dấu tiếng Việt
def remove_accents(text):
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    return text

# 2. Lấy tên nhân viên từ PDF
def extract_employee_name(pdf_path):
    try:
        # Dùng context manager để file được đóng ngay sau khi đọc
        with open(pdf_path, "rb") as f:
            reader = PdfReader(f)
            full_text = ""

            for page in reader.pages:
                txt = page.extract_text()
                if txt:
                    full_text += txt + "\n"

        for line in full_text.split("\n"):
            if "Họ và tên" in line:
                # Ví dụ: "Họ và tên: NGUYỄN ĐĂNG THÁI HÀ"
                parts = line.split(":")
                if len(parts) > 1:
                    name = parts[1].strip()
                    return name

    except Exception as e:
        print(f"❌ Không đọc được PDF {pdf_path}: {e}")

    return None

# 3. Chuẩn hóa tên → không dấu + viết liền
def get_clean_name(pdf_path):
    name = extract_employee_name(pdf_path)
    if not name:
        return None

    name_no_accents = remove_accents(name)
    name_clean = name_no_accents.lower().replace(" ", "")
    return name_clean

# 4. Chọn file PDF
def select_pdf_files():
    Tk().withdraw()
    pdf_paths = filedialog.askopenfilenames(
        title="Chọn các file PDF",
        filetypes=[("PDF Files", "*.pdf")]
    )
    return list(pdf_paths)

# 5. Đổi tên file PDF theo cấu trúc
def rename_pdf(pdf_path, new_name):
    folder = os.path.dirname(pdf_path)
    new_path = os.path.join(folder, new_name + ".pdf")

    try:
        os.rename(pdf_path, new_path)
        print(f"✔️ Đã đổi tên:\n{pdf_path}\n→ {new_path}\n")
        return new_path
    except Exception as e:
        print(f"❌ Lỗi đổi tên file {pdf_path}: {e}")
        return pdf_path

# 6. Khóa PDF bằng password
def encrypt_pdf(pdf_path, password):
    try:
        # Mở file bằng context manager để tránh giữ handle
        with open(pdf_path, "rb") as f:
            reader = PdfReader(f)
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            writer.encrypt(password)

            folder = os.path.dirname(pdf_path)
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            output_path = os.path.join(folder, base_name + "_encrypted.pdf")

            with open(output_path, "wb") as out_f:
                writer.write(out_f)

        print(f"🔐 Đã khóa PDF: {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Lỗi khóa PDF {pdf_path}: {e}")
        return None

# 7. MAIN
def main():
    pdf_files = select_pdf_files()
    if not pdf_files:
        print("Không chọn file PDF nào.")
        return

    output_lines = []

    for pdf in pdf_files:
        clean_name = get_clean_name(pdf)

        if not clean_name:
            print(f"⚠️ Không tìm thấy tên nhân viên trong file: {pdf}")
            continue

        # Đổi tên file PDF
        new_pdf_path = rename_pdf(pdf, clean_name)

        # Khóa PDF bằng chính tên nhân viên
        encrypted_path = encrypt_pdf(new_pdf_path, clean_name)

        output_lines.append(f"{os.path.basename(new_pdf_path)} : {clean_name}")

    # Ghi file password_output.txt
    with open("password_output.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    print("\n🎉 Hoàn tất! Đã tạo password_output.txt")

if __name__ == "__main__":
    main()
