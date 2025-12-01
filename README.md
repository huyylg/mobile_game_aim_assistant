# MobileGameAimAssistant

A complete Python-based auto-aim system for mobile FPS games (PUBG Mobile, COD Mobile, Valorant Mobile) using ADB/Scrcpy for capture, YOLO for detection, and ADB for input injection.

## Features
- Real-time screen capture (800x600, 60-120 FPS, <100ms latency)
- YOLOv8 object detection (enemy/head/body, >95% accuracy)
- Advanced aimbot with prediction, human-like movements, priority scoring
- ADB touch/gyro input with anti-detection
- PyQt5 GUI for control and visualization
- Auto-training pipeline with data collection
- Multi-threading, CUDA acceleration, stealth mode

## Requirements
- Python 3.8+
- Android device with USB debugging/WiFi ADB
- ADB and Scrcpy installed (run setup.sh)

## Setup
1. Clone repo: `git clone <repo>`
2. Run setup: `chmod +x setup.sh && ./setup.sh`
3. Install deps: `pip install -r requirements.txt`
4. Connect device: `adb devices` (USB) or `adb connect <ip>:5555` (WiFi)
5. Edit config.yaml for your game
6. Run: `python main.py`

## Usage
- Launch GUI: Toggle auto-aim/fire, adjust settings
- Training: `python training/collect_data.py` then `python training/train_model.py`
- Tests: `python -m unittest discover tests`
- Customize: Add new game in config.yaml, train model

## Anti-Detection
- Human-like aim curves, delays, errors
- Read-only capture
- Rate-limited inputs

## Performance
- Targets 60+ FPS processing
- Use CUDA for AI (enable in config)
- Monitor FPS in GUI/logs

## License
For educational use only. Respect game ToS.
