#!/usr/bin/env python3
"""
Main entry point for MobileGameAimAssistant.
Integrates all components: capture, AI, aim, input, GUI.
"""

import sys
import threading
import logging
from typing import Optional
from PyQt5.QtWidgets import QApplication
from src.utils.logger import Logger
from src.utils.config_loader import ConfigLoader
from src.capture.screen_capturer import ScreenCapturer
from src.ai.detector import Detector
from src.aim.aim_controller import AimController
from src.input.input_injector import InputInjector
from src.gui.main_window import MainWindow

class MobileGameAimAssistant:
    """
    Main orchestrator class for the aim assistant system.
    Uses multi-threading for capture, detection, aiming.
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = ConfigLoader.load(config_path)
        self.logger = Logger.get_instance(self.config['general']['log_level'])
        self.capturer: Optional[ScreenCapturer] = None
        self.detector: Optional[Detector] = None
        self.aim_controller: Optional[AimController] = None
        self.input_injector: Optional[InputInjector] = None
        self.gui: Optional[MainWindow] = None
        self.running = False
        self.lock = threading.Lock()
    
    def initialize(self) -> None:
        """Initialize all components."""
        try:
            self.logger.info("Initializing components...")
            self.capturer = ScreenCapturer(self.config['capture'])
            self.detector = Detector(self.config['ai'])
            self.aim_controller = AimController(self.config['aim'], self.detector)
            self.input_injector = InputInjector(self.config['input'])
            self.gui = MainWindow(self)
            self.logger.info("Initialization complete.")
        except Exception as e:
            self.logger.error(f"Initialization failed: {e}")
            sys.exit(1)
    
    def start(self) -> None:
        """Start the system in threads."""
        self.running = True
        self.capturer.start()
        threading.Thread(target=self._detection_loop, daemon=True).start()
        threading.Thread(target=self._aim_loop, daemon=True).start()
        self.gui.show()
        self.logger.info("System started.")
    
    def stop(self) -> None:
        """Stop all components."""
        with self.lock:
            self.running = False
        if self.capturer:
            self.capturer.stop()
        self.logger.info("System stopped.")
    
    def _detection_loop(self) -> None:
        """Thread for continuous detection."""
        while self.running:
            try:
                frame = self.capturer.get_frame()
                if frame is not None:
                    detections = self.detector.detect(frame)
                    self.aim_controller.update_detections(detections)
            except Exception as e:
                self.logger.error(f"Detection loop error: {e}")
    
    def _aim_loop(self) -> None:
        """Thread for continuous aiming."""
        while self.running:
            try:
                if self.gui and self.gui.auto_aim_enabled:
                    target = self.aim_controller.get_target()
                    if target:
                        movement = self.aim_controller.calculate_aim(target)
                        self.input_injector.inject(movement)
            except Exception as e:
                self.logger.error(f"Aim loop error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    assistant = MobileGameAimAssistant()
    assistant.initialize()
    assistant.start()
    sys.exit(app.exec_())
