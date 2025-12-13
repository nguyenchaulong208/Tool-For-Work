@echo off
cd /d %~dp0

REM Kích hoạt môi trường ảo trong thư mục cha
@REM call %current_dir%\.venv\Scripts\activate.bat

REM Chạy Streamlit qua Python
python -m streamlit run app.py

pause
