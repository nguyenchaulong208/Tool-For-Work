@echo off
title Chay tong hop hoa don XML

REM Lay duong dan thu muc hien tai (noi dat file bat)
set CURRENT_DIR=%~dp0

REM Duong dan den Python portable
set PYTHON_PORTABLE="D:\Github Code\Python Portbale\python.exe"


REM Kiem tra Python portable co ton tai khong
if not exist %PYTHON_PORTABLE% (
    echo Khong tim thay python.exe trong thu muc:
    echo %CURRENT_DIR%
    pause
    exit /b
)

REM Chay script Python (duong dan tuong doi)
%PYTHON_PORTABLE% "%CURRENT_DIR%ReadXmlInvoice.py"

echo.
echo Da chay xong script. Bam phim bat ky de thoat.
pause