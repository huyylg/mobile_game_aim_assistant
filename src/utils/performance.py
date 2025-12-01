"""
Performance monitoring: FPS, memory, CPU.
"""

import psutil
import time
from typing import Dict

class PerformanceMonitor:
    """
    Monitors system performance.
    """
    
    def get_metrics(self) -> Dict:
        return {
            'fps': 60,  # Placeholder
            'cpu': psutil.cpu_percent(),
            'memory': psutil.virtual_memory().percent
        }
