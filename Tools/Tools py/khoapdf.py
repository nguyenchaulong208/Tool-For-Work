import os
from tkinter import Tk, filedialog
from PyPDF2 import PdfReader, PdfWriter

def select_pdf_files():
    Tk().withdraw()
    pdf_paths = filedialog.askopenfilenames(
        title="Chọn các file PDF cần khóa",
        filetypes=[("PDF Files", "*.pdf")]
    )
    return list(pdf_paths)

def select_password_file():
    Tk().withdraw()
    password_path = filedialog.askopenfilename(
        title="Chọn file password.txt",
        filetypes=[("Text Files", "*.txt")]
    )
    return password_path

def load_passwords(password_file):
    with open(password_file, "r", encoding="utf-8") as f:
        passwords = [line.strip() for line in f.readlines()]
    return passwords

def encrypt_pdfs(pdf_files, passwords):
    output_lines = []

    if len(pdf_files) != len(passwords):
        print("⚠️ Số lượng PDF và số lượng password không khớp!")
        return

    for pdf_path, pwd in zip(pdf_files, passwords):
        try:
            reader = PdfReader(pdf_path)
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            writer.encrypt(pwd)

            folder = os.path.dirname(pdf_path)
            filename = os.path.basename(pdf_path).replace(".pdf", "_encrypted.pdf")
            output_path = os.path.join(folder, filename)

            with open(output_path, "wb") as f:
                writer.write(f)

            output_lines.append(f"{os.path.basename(pdf_path)} : {pwd}")
            print(f"✔️ Đã khóa: {pdf_path}")

        except Exception as e:
            print(f"❌ Lỗi khi xử lý {pdf_path}: {e}")

    with open("password_output.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    print("\n🎉 Hoàn tất! File password_output.txt đã được tạo.")

def main():
    pdf_files = select_pdf_files()
    if not pdf_files:
        print("Không chọn file PDF nào.")
        return

    password_file = select_password_file()
    if not password_file:
        print("Không chọn file password.txt.")
        return

    passwords = load_passwords(password_file)

    encrypt_pdfs(pdf_files, passwords)

if __name__ == "__main__":
    main()
