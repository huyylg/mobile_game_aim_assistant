#!/bin/bash

# Setup script for ADB and Scrcpy
# Run: chmod +x setup.sh && ./setup.sh

echo "Installing ADB and Scrcpy..."

# Install ADB (platform dependent)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt update
    sudo apt install android-tools-adb android-tools-fastboot -y
elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew install android-platform-tools
else
    echo "Windows: Download from https://developer.android.com/studio/releases/platform-tools"
fi

# Install Scrcpy
wget https://github.com/Genymobile/scrcpy/releases/download/v2.0/scrcpy-server-v2.0
# Extract and setup (simplified; adjust path)
mkdir -p ~/scrcpy
# Full install: curl -s https://install.scrcpy.org | bash

echo "Setup complete. Connect device via USB/WiFi and run 'adb devices' to verify."
