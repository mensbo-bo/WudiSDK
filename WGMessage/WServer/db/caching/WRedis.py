""" Ini adalah bagian untuk menangani paket cache menggunakan redis """

import asyncio
from typing import Any

import json
import redis.asyncio as redis

class WRedisData:
    def __init__(self):
        self.redis = redis.Redis(decode_responses=True)
        self.hname = set()

    def __setattr__(self, name: str, value: Any) -> None:
        pass

    async def Redis_Hset(self, name, key):
        hexist = await self.redis.hexists(name, key)
        if not hexist:
            store =  await self.redis.hset(name=name, key=key, value=key)
            self.hname.add(name)
            return True
        
        return False

    async def Redis_Hdel(self, name, key):
        hexist = await self.redis.hexists(name=name, key=key)
        if hexist:
            await self.redis.hdel(name=name, key=key)
            self.hname.discard(key)
            return True
        
        return False
    
    async def Redis_HClean(self):
        for hname in self.hname:
            hfield = self.redis.hgetall(hname)
            await self.redis.hdel(hname, *hfield)

    async def Redis_Close(self):
        await self.Redis_HClean()
        await self.redis.aclose()


class RedisPubSub:
    pass


