import importlib
import subprocess
import sys
import os

def install_missing(requirements_file="requirements.txt", log_file="installed.log"):
    if not os.path.exists(requirements_file):
        print(f"⚠ Không tìm thấy {requirements_file}")
        return

    with open(requirements_file) as f:
        packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    for package in packages:
        try:
            importlib.import_module(package.split("==")[0])  # chỉ check tên package
            print(f"✔ {package} đã có sẵn")
        except ImportError:
            print(f"➜ Cài đặt {package} ...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            with open(log_file, "a") as log:
                log.write(f"{package}\n")