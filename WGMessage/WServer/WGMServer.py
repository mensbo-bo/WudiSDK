import asyncio
import aiohttp

import uuid

class WSServer:
    def __init__(self) -> None:
        self.ServerToken = uuid.uuid4().hex
        self.setClient = {}

    async def WSRun(self, host : str, port : int ) -> None:
        pass

    async def WSGetToken(self) -> str:
        return self.ServerToken
    
    async def GetTokenClient(self) -> dict:
        return self.setClient
    
    async def GenTokenClient(self, numClient : int) -> dict:
        for i in range(numClient):
            hexUUID = uuid.uuid4().hex
            self.setClient[hexUUID[:5]] = hexUUID

        return self.setClient
    
