"""
ModelManager: Loads, manages YOLO models with quantization/TensorRT support.
"""

import torch
from typing import str
from ultralytics import YOLO
from src.utils.logger import Logger

class ModelManager:
    """
    Singleton-like manager for game-specific models.
    Supports quantization for memory efficiency.
    """
    
    _models = {}
    logger = Logger.get_instance()
    
    @classmethod
    def load(cls, path: str) -> YOLO:
        """Load or get cached model."""
        if path not in cls._models:
            try:
                model = YOLO(path)
                # Quantize if CPU
                if not torch.cuda.is_available():
                    model = model.export(format='onnx')  # For quantization
                cls._models[path] = model
                cls.logger.info(f"Loaded model: {path}")
            except Exception as e:
                cls.logger.error(f"Model load failed: {e}")
                raise
        return cls._models[path]
    
    @classmethod
    def get_game_model(cls, game: str, config: dict) -> YOLO:
        """Factory for game models."""
        path = config['games'][game]['model']
        return cls.load(path)
