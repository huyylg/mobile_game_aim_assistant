"""
AimController: Manages aiming logic, prediction, smoothing.
Integrates TargetSelector and MovementSimulator.
"""

import time
import threading
from typing import Optional, Dict, Tuple
from src.aim.target_selector import TargetSelector
from src.aim.movement_simulator import MovementSimulator
from src.ai.predictor import TargetPredictor
from src.utils.logger import Logger
from src.utils.config_loader import ConfigLoader

class AimController:
    """
    Central aim controller with state machine.
    States: IDLE, ACQUIRING, AIMING, FIRING
    """
    
    def __init__(self, config: dict, detector):
        self.config = config
        self.detector = detector
        self.selector = TargetSelector(config)
        self.simulator = MovementSimulator(config)
        self.predictor = TargetPredictor()
        self.logger = Logger.get_instance()
        self.current_target: Optional[Dict] = None
        self.state = "IDLE"
        self.lock = threading.Lock()
    
    def update_detections(self, detections: list) -> None:
        """Update available targets."""
        with self.lock:
            self.current_target = self.selector.select(detections)
    
    def get_target(self) -> Optional[Dict]:
        """Get highest priority target."""
        with self.lock:
            return self.current_target
    
    def calculate_aim(self, target: Dict) -> Tuple[float, float]:
        """Calculate aim delta with prediction and smoothing."""
        try:
            # Predict
            if self.config['prediction_enabled']:
                vel = (target.get('vx', 0), target.get('vy', 0))  # Assume from tracking
                acc = (0, 0)  # Simplified
                pred_pos = self.predictor.predict(target['center'], vel, acc)
            else:
                pred_pos = target['center']
            
            # Crosshair position (assume center)
            crosshair = (400, 300)  # 800x600 center
            
            # Delta
            delta = (pred_pos[0] - crosshair[0], pred_pos[1] - crosshair[1])
            
            # Smooth and humanize
            smoothed = self.simulator.smooth_movement(delta)
            
            self.state = "AIMING"
            return smoothed
        except Exception as e:
            self.logger.error(f"Aim calculation error: {e}")
            return (0, 0)
