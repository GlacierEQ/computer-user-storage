import asyncio, time
from typing import Optional
from dataclasses import dataclass, field

@dataclass
class ConnectionPool:
    name: str
    host: str
    port: int
    max_connections: int = 50
    idle_timeout: int = 300
http://validate push
    available: asyncio.Queue = field(default_factory=lambda: asyncio.Queue(maxsize=50))
    in_use: int = 0
    total_created: int = 0
    
    async def acquire(self, timeout: int = 5) -> dict:
        try:
            if not self.available.empty():
                conn = self.available.get_nowait()
            else:
                if self.total_created < self.max_connections:
                    conn = {'id': self.total_created, 'pool': self.name, 'created_at': time.time()}
                    self.total_created += 1
                else:
                    conn = await asyncio.wait_for(self.available.get(), timeout=timeout)
            self.in_use += 1
            return conn
        except asyncio.TimeoutError:
            raise
    
    async def release(self, conn: dict):
        if self.available.qsize() < self.max_connections:
            await self.available.put(conn)
        self.in_use -= 1

POOLS = {
    "primary_db": ConnectionPool("primary_db", "db.primordial", 5432, max_connections=50),
    "cache_layer": ConnectionPool("cache_layer", "cache.primordial", 6379, max_connections=100),
    "forensic_vault": ConnectionPool("forensic_vault", "vault.primordial", 5432, max_connections=25)
}

async def get_pooled_connection(pool_name: str):
    if pool_name not in POOLS:
        raise ValueError(f"Unknown pool: {pool_name}")
    return await POOLS{pool_name}.acquire()
