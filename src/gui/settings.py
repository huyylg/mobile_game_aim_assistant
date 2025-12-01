"""
SettingsDialog: Adjust sensitivity, FOV, etc.
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QSlider, QLabel
from src.utils.config_loader import ConfigLoader

class SettingsDialog(QDialog):
    """
    Dialog for config adjustments.
    """
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()
    
    def init_ui(self) -> None:
        layout = QVBoxLayout()
        sens_label = QLabel("Sensitivity")
        sens_slider = QSlider()
        sens_slider.setRange(1, 10)
        sens_slider.setValue(int(self.config['aim']['sensitivity'] * 10))
        sens_slider.valueChanged.connect(lambda v: self.config['aim'].update({'sensitivity': v/10}))
        layout.addWidget(sens_label)
        layout.addWidget(sens_slider)
        # Add more sliders...
        self.setLayout(layout)
        self.setWindowTitle("Settings")
