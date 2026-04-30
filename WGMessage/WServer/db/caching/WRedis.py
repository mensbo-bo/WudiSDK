""" Ini adalah bagian untuk menangani paket cache menggunakan redis """

import asyncio
from typing import Any

import json
import redis.asyncio as redis


""" Class for creating redis object """
class RedisCache:
    def __init__(self) -> None:
        self.redis = None

    async def WRedisConnect(self):
        self.redis = redis.Redis(
            host="localhost",
            port=6379,
            db=0,
            decode_responses=True
        )
        print("Redis connection has made")

    async def WRedisClose(self):
        await self.redis.aclose()
        print("Redis connection has closed")

    async def WRedisAddClientToken(self, server_token: str, client_token: str, ttl_seconds: int = 3600 ): # default 1 hour):
        """
        Redis structure:

        key:
            server:{server_token}

        value:
        {
            "serverToken": "...",
            "clientTokens": [
                "...",
                "...",
                "..."
            ]
        }

        ttl_seconds:
            time to live in seconds
        """

        redis_key = f"server:{server_token}"

        # Get existing data
        existing = await self.redis.get(redis_key)

        if existing:
            data = json.loads(existing)
        else:
            data = {
                "serverToken": server_token,
                "clientTokens": []
            }

        # Prevent duplicate token
        if client_token not in data["clientTokens"]:
            data["clientTokens"].append(client_token)

        # Save with TTL
        await self.redis.set(
            redis_key,
            json.dumps(data),
            ex=ttl_seconds  # expiration time
        )

        return data

    async def WRedisGetServerToken(self,server_token: str):
        redis_key = f"server:{server_token}"

        value = await self.redis.get(redis_key)

        if value:
            return json.loads(value)

        raise NameError("Server token not found or expired")

    async def WRedisRemoveClientToken(self,server_token: str, client_token: str, ttl_seconds: int = 3600):
        redis_key = f"server:{server_token}"

        value = await self.redis.get(redis_key)

        if not value:
            raise NameError("Server token not found")

        data = json.loads(value)

        if client_token in data["clientTokens"]:
            data["clientTokens"].remove(client_token)

            # Save again and refresh TTL
            await self.redis.set(
                redis_key,
                json.dumps(data),
                ex=ttl_seconds
            )

        return data

    async def WRedisGetTTL(self,server_token: str):
        """
        Get remaining TTL in seconds
        """

        redis_key = f"server:{server_token}"

        ttl = await self.redis.ttl(redis_key)

        return ttl

    async def WRedisDeleteServerToken(self, server_token: str):
        redis_key = f"server:{server_token}"

        result = await self.redis.delete(redis_key)

        return result > 0


class RedisPubSub:
    pass


