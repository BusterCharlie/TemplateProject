
@echo off
setlocal

REM ===================== DEBUG PAUSE OPTION =====================
REM Set DEBUG_PAUSE to 1 to keep the console open after the script finishes.
REM This is useful for debugging errors. Default is 0 (no pause).
set "DEBUG_PAUSE=0"
REM =============================================================

echo Starting Python Project Generator...
echo Current directory: %cd%

REM This script sets up a Python virtual environment, installs dependencies,
REM and runs the main application. It uses 'uv' for fast environment and
REM package management.

set "PYTHON_CMD=python"

REM Check for python first (more common on Windows), then fallback to python3
echo Checking Python installation...
python --version >nul 2>nul
if %errorlevel% equ 0 (
    set "PYTHON_CMD=python"
    echo Found python, using python
) else (
    python3 --version >nul 2>nul
    if %errorlevel% equ 0 (
        set "PYTHON_CMD=python3"
        echo Found python3, using python3
    ) else (
        echo ERROR: Python is not installed or not in PATH.
        echo Please install Python 3.10 or higher and add it to your PATH.
        echo Make sure 'python' or 'python3' command is available.
        pause
        exit /b 1
    )
)

REM Validate Python version (requires 3.10+)
echo Checking Python version...
for /f "tokens=*" %%i in ('%PYTHON_CMD% -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2^>nul') do set "PYTHON_VERSION=%%i"
if "%PYTHON_VERSION%"=="" (
    echo ERROR: Could not determine Python version.
    pause
    exit /b 1
)

REM Simple version check (assumes format like 3.11, 3.10, etc.)
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    if %%a lss 3 (
        echo ERROR: Python 3.10 or higher is required. Found: %PYTHON_VERSION%
        pause
        exit /b 1
    )
    if %%a equ 3 if %%b lss 10 (
        echo ERROR: Python 3.10 or higher is required. Found: %PYTHON_VERSION%
        pause
        exit /b 1
    )
)
echo Python version check passed: %PYTHON_VERSION%

REM Check for uv and install if not present
echo Checking for UV...
where uv >nul 2>nul
if %errorlevel% neq 0 (
    echo uv not found. Attempting to install...
    %PYTHON_CMD% -m pip install uv
    REM Refresh PATH and check again
    call refreshenv >nul 2>nul || echo Note: PATH refresh failed, you may need to restart your terminal
    where uv >nul 2>nul
    if %errorlevel% neq 0 (
        echo Failed to install uv or uv is not in PATH.
        echo Please try one of the following:
        echo 1. Restart your terminal and run this script again
        echo 2. Install uv manually: https://astral.sh/uv#installation
        echo 3. Add uv to your PATH manually
        pause
        exit /b 1
    )
    echo uv installed successfully.
)
echo UV is available, proceeding...

REM 2. Create a virtual environment in ./.venv
echo Creating virtual environment...

REM More aggressive cleanup of existing virtual environment
if exist .venv (
    echo Removing existing virtual environment...

    REM Try to deactivate any active virtual environment
    if defined VIRTUAL_ENV (
        echo Deactivating current virtual environment...
        call deactivate 2>nul
    )

    REM Remove read-only attributes
    attrib -r .venv\*.* /s /d 2>nul

    REM Force remove with multiple attempts
    echo Attempting removal attempt 1...
    rmdir /s /q .venv 2>nul

    if exist .venv (
        echo Attempting removal attempt 2...
        timeout /t 1 /nobreak >nul
        rmdir /s /q .venv 2>nul
    )

    if exist .venv (
        echo Attempting removal attempt 3...
        rmdir /s /q .venv 2>nul
    )

    if exist .venv (
        echo ERROR: Cannot remove existing .venv directory.
        echo Please manually delete the .venv folder and try again.
        echo You can also try running this batch file as Administrator.
        pause
        exit /b 1
    )
    echo Virtual environment removed successfully.
)

echo Running: uv venv
uv venv
if %errorlevel% neq 0 (
    echo Failed to create virtual environment with error code: %errorlevel%
    echo This might be due to file locks. Try closing any open terminals or editors.
    pause
    exit /b 1
)
echo Virtual environment created successfully.

REM 3. Install dependencies from pyproject.toml
echo Installing dependencies...
echo Running: uv pip install -e .
uv pip install -e .
if %errorlevel% neq 0 (
    echo Failed to install dependencies with error code: %errorlevel%
    pause
    exit /b 1
)
echo Dependencies installed successfully.

REM 4. Run the application
echo Starting the application...
echo Running: uv run python -m template_project.main
echo The GUI window should open now. Close this window after closing the GUI.
uv run python -m template_project.main
if %errorlevel% neq 0 (
    echo Failed to run application with error code: %errorlevel%
    pause
    exit /b 1
)

echo Application finished successfully.
if "%DEBUG_PAUSE%"=="1" (
    echo Press any key to close this window...
    pause
)
endlocal
