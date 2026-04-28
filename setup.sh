#!/bin/bash

echo "========================================"
echo "   InternMatch - Linux/macOS Setup"
echo "========================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if Python 3 is installed
print_status "[1/6] Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    print_error "Python is not installed!"
    echo "Please install Python 3.7+ from:"
    echo "- macOS: brew install python"
    echo "- Ubuntu: sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

$PYTHON_CMD --version

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.7"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    print_error "Python $PYTHON_VERSION is too old. Please install Python 3.7 or higher."
    exit 1
fi

print_status "[2/6] Creating virtual environment..."
$PYTHON_CMD -m venv .venv
if [ $? -ne 0 ]; then
    print_error "Failed to create virtual environment"
    exit 1
fi

print_status "[3/6] Activating virtual environment..."
source .venv/bin/activate

print_status "[4/6] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    print_error "Failed to install dependencies"
    exit 1
fi

print_status "[5/6] Setting up database..."
python db_create.py
if [ $? -ne 0 ]; then
    print_error "Failed to create database"
    exit 1
fi

print_status "[6/6] Training ML model..."
python model_training.py
if [ $? -ne 0 ]; then
    print_error "Failed to train model"
    exit 1
fi

echo
echo "========================================"
echo "    Setup Complete! 🎉"
echo "========================================"
echo
echo "To run the application:"
echo "1. Activate virtual environment: source .venv/bin/activate"
echo "2. Run the app: python app.py"
echo "3. Open browser: http://127.0.0.1:5000"
echo

read -p "Press Enter to start the application now..."

echo
print_status "Starting InternMatch..."
python app.py