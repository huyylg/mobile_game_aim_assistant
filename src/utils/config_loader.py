"""
ConfigLoader: Loads YAML config, supports updates.
"""

import yaml
from typing import Dict, Any
from src.utils.logger import Logger

class ConfigLoader:
    """
    Loads and manages YAML config.
    """
    
    logger = Logger.get_instance()
    
    @classmethod
    def load(cls, path: str) -> Dict[str, Any]:
        try:
            with open(path, 'r') as f:
                config = yaml.safe_load(f)
            cls.logger.info(f"Loaded config: {path}")
            return config
        except Exception as e:
            cls.logger.error(f"Config load failed: {e}")
            raise
