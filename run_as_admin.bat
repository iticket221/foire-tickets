@echo off
cd /d "%~dp0"
powershell -Command "Start-Process cmd -Verb RunAs -ArgumentList '/c cd /d %cd% && venv\Scripts\python app.py'"
