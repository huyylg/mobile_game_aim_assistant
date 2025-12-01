"""
InputInjector: ADB-based touch/swipe/gyro injection.
Thread-safe queue, randomization, rate limiting.
"""

import threading
import time
import random
import queue
from typing import Tuple, List
from src.capture.adb_controller import ADBController
from src.input.gesture_generator import GestureGenerator
from src.input.anti_detect import AntiDetect
from src.utils.logger import Logger

class InputInjector:
    """
    Injects inputs via ADB with anti-cheat measures.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.adb = ADBController()
        self.generator = GestureGenerator()
        self.anti = AntiDetect(config)
        self.input_queue = queue.Queue()
        self.rate_limit = config['rate_limit']
        self.last_input_time = 0
        self.logger = Logger.get_instance()
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self._input_loop, daemon=True)
        self.thread.start()
    
    def inject(self, movement: Tuple[float, float]) -> None:
        """Queue input movement (swipe)."""
        self.input_queue.put(movement)
    
    def _input_loop(self) -> None:
        """Process input queue."""
        while True:
            try:
                movement = self.input_queue.get(timeout=1)
                now = time.time()
                if now - self.last_input_time < 60 / self.rate_limit:
                    time.sleep(60 / self.rate_limit - (now - self.last_input_time))
                
                # Generate gesture
                gesture = self.generator.swipe(movement)
                
                # Anti-detect
                delayed_gesture = self.anti.randomize(gesture)
                
                # Inject
                self._adb_swipe(delayed_gesture)
                
                self.last_input_time = time.time()
                self.input_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Input loop error: {e}")
    
    def _adb_swipe(self, gesture: List[Tuple[int, int]]) -> None:
        """Execute ADB swipe."""
        try:
            # ADB input swipe: adb shell input swipe x1 y1 x2 y2 duration
            x1, y1 = gesture[0]
            x2, y2 = gesture[-1]
            duration = int(100 * self.config['aim_speed'])  # ms
            cmd = f"input swipe {x1} {y1} {x2} {y2} {duration}"
            self.adb.execute([cmd.split()[2:]], shell=True)  # Shell mode
        except Exception as e:
            self.logger.error(f"ADB swipe failed: {e}")
