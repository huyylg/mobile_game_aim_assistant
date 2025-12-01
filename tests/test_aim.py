"""
Unit tests for aim module.
"""

import unittest
import math
from src.aim.target_selector import TargetSelector

class TestAim(unittest.TestCase):
    
    def setUp(self):
        self.config = {'aim': {'fov': 90}}
    
    def test_select(self):
        selector = TargetSelector(self.config)
        detections = [{'class': 'enemy', 'box': (100, 100, 200, 200), 'conf': 0.9}]
        target = selector.select(detections)
        self.assertIsNotNone(target)
        self.assertIn('center', target)

if __name__ == '__main__':
    unittest.main()
