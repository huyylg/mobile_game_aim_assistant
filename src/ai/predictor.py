"""
TargetPredictor: Predicts enemy movement using 2D kinematics.
"""

import numpy as np
from typing import Dict, Tuple
from src.utils.logger import Logger

class TargetPredictor:
    """
    Predicts future position based on velocity/acceleration.
    """
    
    def __init__(self):
        self.logger = Logger.get_instance()
    
    def predict(self, current_pos: Tuple[float, float], velocity: Tuple[float, float], 
                acceleration: Tuple[float, float], dt: float = 0.016) -> Tuple[float, float]:
        """Simple 2D prediction: pos + v*dt + 0.5*a*dt^2"""
        try:
            px = current_pos[0] + velocity[0] * dt + 0.5 * acceleration[0] * dt**2
            py = current_pos[1] + velocity[1] * dt + 0.5 * acceleration[1] * dt**2
            return (px, py)
        except Exception as e:
            self.logger.error(f"Prediction error: {e}")
            return current_pos
