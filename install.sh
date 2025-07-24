#!/bin/bash

set -e

APP_NAME="deploy_push"
INSTALL_DIR="/usr/local/bin"

echo "🔧 Setting up $APP_NAME ..."

# Ensure Python and pip are available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install it first."
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install it first."
    exit 1
fi

# Create virtual environment (optional)
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created."
fi

source venv/bin/activate
pip install --upgrade pip

# No external requirements, but placeholder for future use
# pip install -r requirements.txt

chmod +x $APP_NAME.py

# Optional: install to /usr/local/bin
read -p "❓ Do you want to install '$APP_NAME' system-wide (requires sudo)? [y/N]: " confirm
if [[ "$confirm" =~ ^[Yy]$ ]]; then
    sudo cp $APP_NAME.py $INSTALL_DIR/$APP_NAME
    echo "✅ Installed as '$INSTALL_DIR/$APP_NAME'. You can now run it using: $APP_NAME"
else
    echo "ℹ️ You can run it locally using: ./deploy_push.py"
fi

echo "🎉 Installation complete."