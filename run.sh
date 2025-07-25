
#!/bin/bash

# ===================== DEBUG PAUSE OPTION =====================
# Set DEBUG_PAUSE=1 to keep the terminal open after the script finishes.
# This is useful for debugging errors. Default is 0 (no pause).
DEBUG_PAUSE=0
# =============================================================

# This script sets up a Python virtual environment, installs dependencies,
# and runs the main application. It uses 'uv' for fast environment and
# package management.

PYTHON_CMD="python3"
# Check if python3 is available, otherwise use python
if ! command -v python3 &> /dev/null
then
    PYTHON_CMD="python"
fi

# Validate Python version (requires 3.10+)
echo "Checking Python version..."
PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "0.0")
REQUIRED_VERSION="3.10"

if [[ $(echo "$PYTHON_VERSION $REQUIRED_VERSION" | awk '{print ($1 >= $2)}') == 0 ]]; then
    echo "ERROR: Python $REQUIRED_VERSION or higher is required. Found: $PYTHON_VERSION"
    echo "Please install Python $REQUIRED_VERSION or higher and try again."
    exit 1
fi
echo "Python version check passed: $PYTHON_VERSION"

# Function to check for uv and install if not present
install_uv() {
    if ! command -v uv &> /dev/null
    then
        echo "uv not found. Attempting to install..."
        $PYTHON_CMD -m pip install uv
        # Refresh PATH and check again
        hash -r 2>/dev/null || true
        if ! command -v uv &> /dev/null
        then
            echo "Failed to install uv. Please install it manually:"
            echo "https://astral.sh/uv#installation"
            exit 1
        fi
        echo "uv installed successfully."
    fi
}

# --- Main Script ---

# 1. Ensure uv is available
install_uv

# 2. Create a virtual environment in ./.venv
echo "Creating virtual environment..."

# Clean up existing virtual environment if it exists
if [ -d ".venv" ]; then
    echo
    echo "WARNING: An existing virtual environment (.venv) was found."
    echo "This will be removed to create a fresh environment."
    echo
    read -p "Do you want to remove the existing .venv folder? (y/N): " confirm
    if [[ ! "$confirm" =~ ^[Yy]([Ee][Ss])?$ ]]; then
        echo "Operation cancelled by user."
        exit 0
    fi
    echo "Removing existing virtual environment..."
    rm -rf .venv
    if [ -d ".venv" ]; then
        echo "ERROR: Cannot remove existing .venv directory."
        echo "Please manually delete the .venv folder and try again."
        exit 1
    fi
    echo "Existing virtual environment removed successfully."
fi

uv venv
if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment."
    echo "Please check that uv is properly installed and try again."
    exit 1
fi

# 3. Install dependencies from pyproject.toml
echo "Installing dependencies..."
uv pip install -e .
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies."
    echo "Please check your pyproject.toml file and try again."
    exit 1
fi

# 4. Run the application
echo "Starting the application..."
uv run python src/template_project/main.py
if [ $? -ne 0 ]; then
    echo "Failed to run application."
    echo "Please check the application logs for more details."
    exit 1
fi

echo "Application finished."

# Pause if debugging is enabled
if [ "$DEBUG_PAUSE" = "1" ]; then
    echo "Press Enter to close this window..."
    read
fi
