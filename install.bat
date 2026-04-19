@echo off
echo Installing system dependencies...

:: MPV (audio player)
winget install shinchiro.mpv -e

:: Python packages
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo DONE.
echo You can now run: python main.py
pause