import hashlib, json, time
from typing import Any, Optional
from collections import OrderedDict

class CacheEntry:
    def __init__(self, value: Any, ttl: int = 3600):
        self.value = value
        self.created = time.time()
        self.ttl = ttl
        self.hits = 0
    
    def is_expired(self) -> bool
        return time.time() - self.created > self.ttl
    
    def record_hit(self)
        self.hits += 1

class IntelligentCache:
    def __init__(self, max_size: int = 10000, default_ttl: int = 3600):
        self.cache = OrderedDict()
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.stats = {"hits": 0, "misses": 0, "evictions": 0}
    
    def _hash_key(self, key: str) -> str:
        return hashlib.sha256(key.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        hash_key = self._hash_key(key)
        if hash_key in self.cache:
            entry = self.cache[hash_key]
            if not entry.is_expired():
                entry.record_hit()
                self.stats["hits"] += 1
                self.cache.move_to_end(hash_key)
                return entry.value
            else:
                del self.cache[hash_key]
        self.stats["misses"] += 1
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        hash_key = self._hash_key(key)
        ttl = ttl or self.default_ttl
        entry = CacheEntry(value, ttl)
        if hash_key in self.cache:
            self.cache.move_to_end(hash_key)
        self.cache[hash_key] = entry
        while len(self.cache) > self.max_size:
            self.cache.popitem(last=False)
            self.stats["evictions"] += 1
    
    def get_stats(self) -> dict:
        total = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total * 100) if total > 0 else 0
        return {\"cache_size\": len(self.cache), **self.stats, \"hit_rate_percent\": hit_rate}

QUERY_CACHE= IntelligentCache(max_size=5000, default_ttl=1800)
