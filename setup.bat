@echo off
echo === GugaBot Setup ===

IF NOT EXIST ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat
echo Installing Python dependencies...
pip install --upgrade pip -q
pip install -r requirements.txt

echo.
echo === Setup complete! ===
echo Run the app with:
echo   .venv\Scripts\activate.bat ^&^& python main.py
pause
