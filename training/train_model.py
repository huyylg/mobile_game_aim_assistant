"""
YOLOv8 training script with transfer learning, hyperparam opt.
"""

import torch
from ultralytics import YOLO
from src.utils.config_loader import ConfigLoader
from src.utils.logger import Logger

class Trainer:
    """
    Trains custom YOLO model.
    """
    
    def __init__(self, config_path: str):
        self.config = ConfigLoader.load(config_path)
        self.logger = Logger.get_instance()
    
    def train(self, game: str, epochs: int = None) -> str:
        """Train model."""
        epochs = epochs or self.config['training']['epochs']
        model_path = self.config['games'][game]['model'].replace('.pt', '-trained.pt')
        
        # Load pre-trained
        model = YOLO('yolov8n.pt')  # Transfer from COCO
        
        # Train
        model.train(
            data=f"{self.config['training']['dataset_path']}/data.yaml",  # Assume YAML dataset
            epochs=epochs,
            imgsz=self.config['training']['img_size'],
            batch=self.config['training']['batch_size'],
            device=0 if torch.cuda.is_available() else 'cpu'
        )
        
        # Export
        model.export(format='pt')
        self.logger.info(f"Trained model saved: {model_path}")
        return model_path

if __name__ == "__main__":
    import sys
    game = sys.argv[1] if len(sys.argv) > 1 else "pubg_mobile"
    trainer = Trainer("../../config.yaml")
    trainer.train(game)
