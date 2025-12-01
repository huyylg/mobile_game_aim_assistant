"""
MovementSimulator: Human-like aim paths using Bezier curves, smoothing.
Includes recoil compensation.
"""

import numpy as np
from typing import Tuple
import random
from src.utils.logger import Logger

class MovementSimulator:
    """
    Simulates human aim with curves, delays, errors.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.sens = config['sensitivity']
        self.speed = config['aim_speed']
        self.style = config['style']
        self.logger = Logger.get_instance()
    
    def smooth_movement(self, delta: Tuple[float, float]) -> Tuple[float, float]:
        """Apply Bezier curve and randomization."""
        try:
            # Scale by sens/speed
            dx, dy = delta[0] * self.sens * self.speed, delta[1] * self.sens * self.speed
            
            # Bezier for curve (simplified quadratic)
            t = 0.5  # Midpoint
            control = (dx * 0.1 * random.uniform(-1, 1), dy * 0.1 * random.uniform(-1, 1))  # Curve offset
            bezier_x = (1-t)**2 * 0 + 2*(1-t)*t * control[0] + t**2 * dx
            bezier_y = (1-t)**2 * 0 + 2*(1-t)*t * control[1] + t**2 * dy
            
            # Add human error
            error = (random.uniform(-0.05, 0.05) * abs(dx), random.uniform(-0.05, 0.05) * abs(dy))
            final = (bezier_x + error[0], bezier_y + error[1])
            
            # Recoil comp (placeholder: subtract upward)
            if self.style == "aggressive":
                final = (final[0], final[1] - 0.1)
            
            return final
        except Exception as e:
            self.logger.error(f"Movement sim error: {e}")
            return delta
