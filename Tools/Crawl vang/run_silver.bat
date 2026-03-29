@echo off
cd /d "%~dp0"
call .venv\Scripts\activate

:loop
python silver.py

