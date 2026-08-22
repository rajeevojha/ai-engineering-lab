"""
Common utilities for AI Engineering Lab.

Includes logging, timing, and other helpers shared across days.
"""

import logging
import time
from functools import wraps
from typing import Any, Callable


def setup_logging(name: str, level: str = "INFO") -> logging.Logger:
    """
    Set up a logger for a given module.
    
    Args:
        name: Module name (e.g., __name__).
        level: Logging level (default "INFO").
    
    Returns:
        Configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger


def timed(func: Callable) -> Callable:
    """
    Decorator to measure function execution time.
    
    Args:
        func: Function to time.
    
    Returns:
        Wrapped function that prints execution time.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.3f} seconds")
        return result
    return wrapper
