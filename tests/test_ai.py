"""
Unit tests for AI module.
"""

import unittest
from unittest.mock import patch
import numpy as np
from src.ai.detector import Detector

class TestAI(unittest.TestCase):
    
    def setUp(self):
        self.config = {'ai': {'model_path': 'dummy.pt', 'confidence_threshold': 0.8, 'cuda_enabled': False}}
    
    @patch('ultralytics.YOLO')
    def test_detect(self, mock_yolo):
        mock_model = MagicMock()
        mock_model.return_value = [MagicMock(boxes=MagicMock())]  # Simplified
        mock_yolo.return_value = mock_model
        detector = Detector(self.config)
        frame = np.zeros((600, 800, 3), dtype=np.uint8)
        detections = detector.detect(frame)
        self.assertIsInstance(detections, list)

if __name__ == '__main__':
    unittest.main()
