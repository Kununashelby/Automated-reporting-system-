@echo off

cd /d "C:\Users\kununa\Desktop\Automated-reporting-system-"

call ".venv\Scripts\activate.bat"

python scheduler.py

pause