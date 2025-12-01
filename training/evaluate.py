"""
Evaluation: mAP, real-time FPS test.
"""

from ultralytics import YOLO
import time
from src.ai.detector import Detector
from src.utils.config_loader import ConfigLoader
from src.utils.logger import Logger

class Evaluator:
    """
    Evaluates model performance.
    """
    
    def __init__(self, config_path: str):
        self.config = ConfigLoader.load(config_path)
        self.logger = Logger.get_instance()
    
    def evaluate_map(self, model_path: str, test_path: str) -> float:
        """Calculate mAP on test set."""
        model = YOLO(model_path)
        results = model.val(data=f"{test_path}/data.yaml")
        map_score = results.box.map
        self.logger.info(f"mAP: {map_score}")
        return map_score
    
    def benchmark_realtime(self, model_path: str, num_frames: int = 100) -> float:
        """Benchmark inference FPS."""
        detector = Detector({'model_path': model_path, 'cuda_enabled': self.config['general']['cuda_enabled']})
        # Dummy frames
        dummy_frame = np.zeros((600, 800, 3), dtype=np.uint8)
        frames = [dummy_frame] * num_frames
        
        start = time.time()
        for f in frames:
            detector.detect(f)
        fps = num_frames / (time.time() - start)
        self.logger.info(f"Real-time FPS: {fps}")
        return fps

if __name__ == "__main__":
    import sys
    model = sys.argv[1]
    evaluator = Evaluator("../../config.yaml")
    evaluator.evaluate_map(model, "data/test")
    evaluator.benchmark_realtime(model)
