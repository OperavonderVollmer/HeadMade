@echo off
setlocal

cd /d "%~dp0"

title HeadMade


call ".\.venv\Scripts\activate.bat"

python ".\HeadMade\HeadMade.py"
