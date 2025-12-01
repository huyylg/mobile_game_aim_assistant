"""
Unit tests for capture module.
"""

import unittest
import numpy as np
from unittest.mock import patch, MagicMock
from src.capture.screen_capturer import ScreenCapturer
from src.capture.frame_buffer import FrameBuffer

class TestCapture(unittest.TestCase):
    
    def setUp(self):
        self.config = {'capture': {'buffer_size': 2, 'adb_host': None}}
    
    @patch('subprocess.Popen')
    def test_start_scrcpy(self, mock_popen):
        capturer = ScreenCapturer(self.config)
        capturer._start_scrcpy()
        mock_popen.assert_called()
    
    def test_frame_buffer(self):
        buffer = FrameBuffer(2)
        frame = np.zeros((600, 800, 3), dtype=np.uint8)
        buffer.put(frame)
        self.assertIsNotNone(buffer.get())
        # Test overflow
        for _ in range(3):
            buffer.put(frame)
        self.assertIsNotNone(buffer.get())

if __name__ == '__main__':
    unittest.main()
