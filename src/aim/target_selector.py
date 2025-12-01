"""
TargetSelector: Priority scoring for targets (distance, health, threat).
"""

import math
from typing import List, Dict, Tuple
from src.utils.logger import Logger

class TargetSelector:
    """
    Selects best target based on scoring.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.fov = config['fov']
        self.logger = Logger.get_instance()
    
    def select(self, detections: List[Dict]) -> Optional[Dict]:
        """Select highest score target."""
        if not detections:
            return None
        
        scores = []
        crosshair = (400, 300)
        
        for det in detections:
            if det['class'] != 'enemy':
                continue
            box = det['box']
            center = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
            
            # Distance to crosshair
            dist = math.sqrt((center[0] - crosshair[0])**2 + (center[1] - crosshair[1])**2)
            
            # Visibility (simplified: conf)
            vis = det['conf']
            
            # Threat (assume 1.0 for now)
            threat = 1.0
            
            # Health estimation (placeholder)
            health = 1.0
            
            score = (1 / (dist + 1)) * vis * threat * health  # Weighted
            
            scores.append((score, det, center))
        
        if scores:
            best = max(scores, key=lambda x: x[0])[1]
            best['center'] = scores[0][2]  # Attach center
            self.logger.debug(f"Selected target score: {max(s[0] for s in scores)}")
            return best
        return None
