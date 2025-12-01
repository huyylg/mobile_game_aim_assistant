"""
YOLOv8-based Detector for game objects (enemy, head, body).
Supports batch, NMS, quantization, TensorRT.
"""

import torch
import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional
from ultralytics import YOLO  # YOLOv8
from src.utils.logger import Logger
from src.ai.model_manager import ModelManager

class Detector:
    """
    Real-time object detector using YOLOv8.
    Multi-class: enemy, teammate, head, body.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.model = ModelManager.load(config['model_path'])
        self.device = 'cuda' if config['cuda_enabled'] and torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)
        self.logger = Logger.get_instance()
        self.classes = config['classes']
        self.conf_threshold = config['confidence_threshold']
        self.nms_threshold = config['nms_threshold']
    
    def detect(self, frame: np.ndarray) -> List[Dict]:
        """
        Detect objects in frame.
        Returns list of {'class': str, 'box': Tuple[int,int,int,int], 'conf': float}
        """
        try:
            # Preprocess
            img = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            results = self.model(img, conf=self.conf_threshold, iou=self.nms_threshold)
            
            detections = []
            for r in results:
                boxes = r.boxes
                if boxes is not None:
                    for box in boxes:
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        conf = box.conf[0].cpu().numpy()
                        cls = int(box.cls[0].cpu().numpy())
                        detections.append({
                            'class': self.classes[cls],
                            'box': (int(x1), int(y1), int(x2), int(y2)),
                            'conf': float(conf)
                        })
            self.logger.debug(f"Detected {len(detections)} objects")
            return detections
        except Exception as e:
            self.logger.error(f"Detection error: {e}")
            return []
    
    def benchmark(self, frames: List[np.ndarray]) -> float:
        """Benchmark inference time."""
        start = time.time()
        for f in frames:
            self.detect(f)
        return (time.time() - start) / len(frames)
