@echo off
call conda activate powerbi_env
cd /d "%~dp0"
python fluxo.py
pause
