"""
Data collection: Record gameplay, auto-label.
"""

import cv2
import os
from typing import str
from src.capture.screen_capturer import ScreenCapturer
from src.utils.config_loader import ConfigLoader
from src.utils.logger import Logger

class DataCollector:
    """
    Collects frames and auto-labels using existing model.
    """
    
    def __init__(self, config_path: str):
        self.config = ConfigLoader.load(config_path)
        self.capturer = ScreenCapturer(self.config['capture'])
        self.detector = Detector(self.config['ai'])  # For auto-label
        self.dataset_path = self.config['training']['dataset_path']
        os.makedirs(self.dataset_path, exist_ok=True)
        self.logger = Logger.get_instance()
    
    def collect(self, duration: int = 300, game: str = "pubg_mobile") -> None:
        """Collect for duration seconds."""
        self.capturer.start()
        frame_count = 0
        start = time.time()
        while time.time() - start < duration:
            frame = self.capturer.get_frame()
            if frame is not None:
                # Auto-label
                detections = self.detector.detect(frame)
                # Save frame and labels (YOLO format)
                cv2.imwrite(f"{self.dataset_path}/img_{frame_count}.jpg", frame)
                with open(f"{self.dataset_path}/label_{frame_count}.txt", 'w') as f:
                    for d in detections:
                        # YOLO label format: class x y w h
                        cls_id = self.config['ai']['classes'].index(d['class'])
                        x, y, w, h = self._box_to_yolo(d['box'], frame.shape)
                        f.write(f"{cls_id} {x} {y} {w} {h}\n")
                frame_count += 1
        self.capturer.stop()
        self.logger.info(f"Collected {frame_count} frames")
    
    def _box_to_yolo(self, box: tuple, shape: tuple) -> tuple:
        """Convert box to YOLO normalized."""
        x, y, w, h = box[0], box[1], box[2]-box[0], box[3]-box[1]
        cx = (x + w/2) / shape[1]
        cy = (y + h/2) / shape[0]
        w_norm = w / shape[1]
        h_norm = h / shape[0]
        return cx, cy, w_norm, h_norm

if __name__ == "__main__":
    collector = DataCollector("../../config.yaml")
    collector.collect()
