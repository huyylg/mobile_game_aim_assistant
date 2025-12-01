"""
ADBController for handling ADB connections and commands.
Supports USB/WiFi, error handling, multi-device.
"""

import subprocess
import time
from typing import List, Optional
from src.utils.logger import Logger

class ADBController:
    """
    Manages ADB connections for single/multiple devices.
    """
    
    def __init__(self, host: str = None):
        self.host = host
        self.logger = Logger.get_instance()
        self.devices: List[str] = []
        self._connect()
    
    def _connect(self) -> None:
        """Connect to device."""
        try:
            if self.host:
                subprocess.run(["adb", "connect", self.host], check=True)
            self.devices = [line.split('\t')[0] for line in subprocess.check_output(["adb", "devices"]).decode().splitlines() if '\tdevice' in line]
            if not self.devices:
                raise RuntimeError("No devices found")
            self.logger.info(f"Connected to devices: {self.devices}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"ADB connect failed: {e}")
            raise
    
    def reconnect(self) -> None:
        """Reconnect on disconnect."""
        self._connect()
    
    def execute(self, cmd: List[str], device: str = None) -> str:
        """Execute ADB command."""
        full_cmd = ["adb"] + (["-s", device] if device else []) + cmd
        try:
            output = subprocess.check_output(full_cmd, stderr=subprocess.STDOUT).decode()
            return output
        except subprocess.CalledProcessError as e:
            self.logger.error(f"ADB command failed: {e}")
            self.reconnect()
            raise
