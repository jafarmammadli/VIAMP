@echo off
echo Building EXE...

python -m pip install pyinstaller
python -m PyInstaller --onefile main.py

echo DONE
pause