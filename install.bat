@echo off
setlocal EnableDelayedExpansion
title GugaBot Installer
color 0A

echo.
echo  ============================================
echo   GugaBot Installer
echo  ============================================
echo.

:: ── Step 1: Check Python ────────────────────────────────────────────────────
echo [1/5] Checking for Python 3.11+...

set PY_OK=0
for /f "tokens=*" %%V in ('python --version 2^>^&1') do set PY_VER=%%V
echo        Found: %PY_VER%

:: Extract major.minor from "Python X.Y.Z"
for /f "tokens=2 delims= " %%V in ("%PY_VER%") do (
    for /f "tokens=1,2 delims=." %%A in ("%%V") do (
        set PY_MAJOR=%%A
        set PY_MINOR=%%B
    )
)

:: Require Python 3.11+
if defined PY_MAJOR if defined PY_MINOR (
    if !PY_MAJOR! GEQ 3 (
        if !PY_MINOR! GEQ 11 (
            set PY_OK=1
        )
    )
)

if "%PY_OK%"=="0" (
    echo.
    echo  Python 3.11+ not found. Attempting to install via winget...
    echo  (This requires Windows 10/11 with winget installed)
    echo.
    winget install Python.Python.3.12 --silent --accept-source-agreements --accept-package-agreements
    if errorlevel 1 (
        echo.
        echo  [ERROR] Automatic Python install failed.
        echo  Please install Python 3.11 or newer manually from:
        echo    https://www.python.org/downloads/
        echo  Make sure to check "Add Python to PATH" during install.
        echo.
        pause
        exit /b 1
    )
    echo  Python installed. Refreshing PATH...
    :: Refresh PATH so the new python is found
    for /f "skip=2 tokens=3*" %%A in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "USR_PATH=%%A %%B"
    set "PATH=%PATH%;%USR_PATH%"
)

echo        OK
echo.

:: ── Step 2: Create virtual environment ──────────────────────────────────────
echo [2/5] Creating virtual environment...

if exist ".venv" (
    echo        .venv already exists, skipping creation.
) else (
    python -m venv .venv
    if errorlevel 1 (
        echo  [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo        Created .venv
)
echo.

:: ── Step 3: Upgrade pip ──────────────────────────────────────────────────────
echo [3/5] Upgrading pip...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip --quiet
echo        OK
echo.

:: ── Step 4: Install dependencies ────────────────────────────────────────────
echo [4/5] Installing dependencies...
echo        (pyaudio is skipped — voice features require a manual install)
echo.

pip install ^
    "PyQt6>=6.4.0" ^
    "openai>=1.0.0" ^
    "pyautogui>=0.9.54" ^
    "Pillow>=10.0.0" ^
    "SpeechRecognition>=3.10.0" ^
    "pynput>=1.7.6" ^
    "requests>=2.31.0" ^
    "pyperclip>=1.8.0"

if errorlevel 1 (
    echo.
    echo  [ERROR] Some packages failed to install.
    echo  Check the errors above, then re-run install.bat.
    pause
    exit /b 1
)
echo.
echo        Dependencies installed.
echo.

:: ── Step 5: Create desktop shortcut ─────────────────────────────────────────
echo [5/5] Creating desktop shortcut...

set "INSTALL_DIR=%~dp0"
set "SHORTCUT=%USERPROFILE%\Desktop\Launch GugaBot.bat"

(
    echo @echo off
    echo cd /d "%INSTALL_DIR%"
    echo call .venv\Scripts\activate.bat
    echo start "" pythonw main.py
) > "%SHORTCUT%"

if exist "%SHORTCUT%" (
    echo        Shortcut created: %SHORTCUT%
) else (
    echo        Could not create shortcut. You can still run GugaBot manually ^(see below^).
)
echo.

:: ── Done ─────────────────────────────────────────────────────────────────────
echo  ============================================
echo   Installation complete!
echo  ============================================
echo.
echo  To launch GugaBot:
echo    - Double-click "Launch GugaBot" on your Desktop
echo    OR
echo    - Run: .venv\Scripts\activate.bat ^&^& python main.py
echo.
echo  Note on voice features:
echo    pyaudio is not installed automatically because it requires
echo    Microsoft Visual C++ build tools. Voice wake-word detection
echo    will be silently disabled; all other features work normally.
echo    To enable voice: install pyaudio from a prebuilt wheel at
echo    https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
echo.
pause
