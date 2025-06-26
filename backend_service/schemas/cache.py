from pydantic import BaseModel

class Cache(BaseModel):
    cache_key: str
