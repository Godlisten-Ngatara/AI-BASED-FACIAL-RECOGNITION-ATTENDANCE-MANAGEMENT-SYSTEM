# cache.py
import time
from typing import Any, Optional

# Simple in-memory cache dictionary
_cache = {}

def set_cache(key: str, value: Any, ttl: int = 300) -> None:
    """
    Stores value in cache with a time-to-live (ttl) in seconds.
    """
    expiry = time.time() + ttl
    _cache[key] = (value, expiry)

def get_cache(key: str) -> Optional[Any]:
    """
    Retrieves value from cache if not expired.
    """
    if key in _cache:
        value, expiry = _cache[key]
        if time.time() < expiry:
            return value
        else:
            del _cache[key]  # Clean expired entry
    return None
