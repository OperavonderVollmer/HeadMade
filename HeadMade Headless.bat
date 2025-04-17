
@echo off
setlocal

cd /d "%~dp0"

title HeadMade
start "" ".\.venv\Scripts\pythonw.exe" ".\main.py" "HEADLESS"

