"""
FrameBuffer: Thread-safe queue for frames (max 2 to avoid latency).
"""

import queue
import threading
from typing import Optional
import numpy as np
from src.utils.logger import Logger

class FrameBuffer:
    """
    Bounded queue for memory-efficient frame buffering.
    """
    
    def __init__(self, max_size: int = 2):
        self.queue = queue.Queue(maxsize=max_size)
        self.lock = threading.Lock()
        self.logger = Logger.get_instance()
    
    def put(self, frame: np.ndarray) -> None:
        """Put frame, drop oldest if full."""
        with self.lock:
            if self.queue.full():
                try:
                    self.queue.get_nowait()  # Drop old
                except queue.Empty:
                    pass
            self.queue.put(frame)
    
    def get(self) -> Optional[np.ndarray]:
        """Get latest frame."""
        try:
            return self.queue.get_nowait()
        except queue.Empty:
            return None
