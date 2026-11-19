@echo off
setlocal
echo ========================================================
echo       AI Website Testing Agent - Windows Launcher
echo ========================================================
echo.

cd /d "%~dp0"

:: 1. Check Python installation via py launcher
py -0 >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python launcher 'py' was not found on your system.
    echo Please install Python 3.10 or 3.11 from python.org with "Add to PATH" checked.
    pause
    exit /b 1
)

:: 2. Check / Create Virtual Environment
if not exist "venv\Scripts\activate.bat" (
    echo [*] Creating virtual environment in .\venv...
    py -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created.
)

:: 3. Activate Virtual Environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

:: 4. Install Dependencies
echo [*] Checking dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

:: 5. Install Playwright Chromium Browser (optional if Chrome/Edge already present)
echo [*] Checking browser availability...
playwright install chromium >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Standalone Chromium download skipped. Using installed Chrome/Edge automatically.
)

:: 6. Launch Streamlit Web UI
echo.
echo ========================================================
echo [OK] All setup complete! Launching Streamlit web app...
echo ========================================================
echo.
streamlit run app.py

pause
