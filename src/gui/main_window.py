"""
MainWindow: PyQt5 GUI for control, real-time display with overlays.
"""

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QSlider, QLabel, QComboBox
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from typing import Optional
import cv2
import numpy as np
from src.gui.overlay import Overlay
from src.gui.settings import SettingsDialog
from src.utils.logger import Logger

class MainWindow(QMainWindow):
    """
    GUI with real-time frame display, toggles, settings.
    """
    
    update_frame = pyqtSignal(np.ndarray)
    
    def __init__(self, assistant):
        super().__init__()
        self.assistant = assistant
        self.auto_aim_enabled = False
        self.auto_fire_enabled = False
        self.logger = Logger.get_instance()
        self.init_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # 60 FPS
        self.overlay = Overlay()
    
    def init_ui(self) -> None:
        """Setup UI."""
        central = QWidget()
        layout = QVBoxLayout()
        
        self.frame_label = QLabel("No frame")
        layout.addWidget(self.frame_label)
        
        self.aim_toggle = QPushButton("Toggle Auto Aim")
        self.aim_toggle.clicked.connect(self.toggle_aim)
        layout.addWidget(self.aim_toggle)
        
        self.fire_toggle = QPushButton("Toggle Auto Fire")
        self.fire_toggle.clicked.connect(self.toggle_fire)
        layout.addWidget(self.fire_toggle)
        
        self.settings_btn = QPushButton("Settings")
        self.settings_btn.clicked.connect(self.open_settings)
        layout.addWidget(self.settings_btn)
        
        self.game_combo = QComboBox()
        self.game_combo.addItems(["pubg_mobile", "cod_mobile", "valorant_mobile"])
        layout.addWidget(self.game_combo)
        
        central.setLayout(layout)
        self.setCentralWidget(central)
        self.setWindowTitle("MobileGameAimAssistant")
    
    def toggle_aim(self) -> None:
        self.auto_aim_enabled = not self.auto_aim_enabled
        self.aim_toggle.setText("Auto Aim: ON" if self.auto_aim_enabled else "Auto Aim: OFF")
    
    def toggle_fire(self) -> None:
        self.auto_fire_enabled = not self.auto_fire_enabled
        self.fire_toggle.setText("Auto Fire: ON" if self.auto_fire_enabled else "Auto Fire: OFF")
    
    def open_settings(self) -> None:
        dialog = SettingsDialog(self.assistant.config)
        dialog.exec_()
    
    def update(self) -> None:
        """Update frame display."""
        frame = self.assistant.capturer.get_frame()
        if frame is not None:
            # Draw overlay
            frame_with_boxes = self.overlay.draw_boxes(frame, [])  # Pass detections
            h, w, ch = frame_with_boxes.shape
            bytes_per_line = ch * w
            qt_img = QImage(frame_with_boxes.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.frame_label.setPixmap(QPixmap.fromImage(qt_img))
