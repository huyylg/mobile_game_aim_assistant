"""
Overlay: Draws bounding boxes on frame.
"""

import cv2
import numpy as np
from typing import List, Dict

class Overlay:
    """
    Draws detections on frame for visualization.
    """
    
    def draw_boxes(self, frame: np.ndarray, detections: List[Dict]) -> np.ndarray:
        """Draw boxes."""
        for det in detections:
            box = det['box']
            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
            cv2.putText(frame, f"{det['class']} {det['conf']:.2f}", (box[0], box[1]-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        return frame
