# File nay dung de run streamlit khi dong goi exe vi streamlit khong the build truc tiep thanh .exe
import subprocess
import sys

subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])