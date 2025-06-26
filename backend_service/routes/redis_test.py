import sys, os



sys.path.append(
    os.path.abspath(r"h:\code\AI-BASED FACIAL RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")
)
from backend_service.schemas.cache import Cache
from backend_service.utilities.cache_handler import get_cache
from fastapi import APIRouter, Depends, HTTPException
from backend_service.config.redis_app import redis_client
cacheRouter = APIRouter()


@cacheRouter.post("/cache")
def read_cache(cache: Cache):
    value = get_cache(cache.cache_key)
    print(value)
    if value is None:
        raise HTTPException(status_code=404, detail="Cache key not found or expired")
    return value