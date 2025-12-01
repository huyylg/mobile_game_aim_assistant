#!/bin/bash

# Update package list
sudo apt-get update

# Install ADB
sudo apt-get install -y android-tools-adb

# Install scrcpy
sudo apt-get install -y scrcpy

# Install Python dependencies
pip install -r requirements.txt

# Grant USB permissions
sudo usermod -aG plugdev $USER

echo "Setup completed! Please reconnect your phone via USB."
