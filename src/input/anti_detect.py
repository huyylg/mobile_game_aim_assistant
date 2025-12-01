"""
AntiDetect: Randomizes inputs, adds delays/errors.
"""

import random
import time
from typing import List, Tuple
from src.utils.logger import Logger

class AntiDetect:
    """
    Applies stealth features to inputs.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.delays = config['delay_randomization']
        self.logger = Logger.get_instance()
    
    def randomize(self, gesture: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Add random errors/delays."""
        randomized = []
        for point in gesture:
            # Add pixel error
            rx = point[0] + random.uniform(-2, 2)
            ry = point[1] + random.uniform(-2, 2)
            randomized.append((int(rx), int(ry)))
        
        # Delay
        delay = random.uniform(*self.delays)
        time.sleep(delay)
        
        return randomized
