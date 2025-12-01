"""
Singleton Logger with configurable level.
"""

import logging
from typing import Optional

class Logger:
    """
    Singleton logging utility.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, level: str = "INFO"):
        if not hasattr(self, 'initialized'):
            logging.basicConfig(level=getattr(logging, level), format='%(asctime)s - %(levelname)s - %(message)s')
            self.logger = logging.getLogger(__name__)
            self.initialized = True
    
    @classmethod
    def get_instance(cls, level: Optional[str] = None) -> 'Logger':
        if level:
            instance = cls()
            instance.logger.setLevel(getattr(logging, level))
        return cls._instance
