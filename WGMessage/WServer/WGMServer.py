import asyncio
import aiohttp

import uuid

from typing import Any
from __pstrogeWServer import __ws
import WGMessage.WServer.utils as utils

class WSServer:
    def __init__(self) -> None:
        self.ServerToken = __ws.WSToken(uuid.uuid4().hex)
        self.setClient = {}
    
    def __setattr__(self, name: str, value: Any) -> None:
        pass

    async def WSRun(self, host : str, port : int ) -> None:
        pass

    async def WSGetToken(self) -> Any:
        return self.ServerToken.get()
    
    async def GetTokenClient(self) -> dict:
        """Menggambil token server yang sudah dibuat"""
        return self.setClient
    
    async def GenTokenClient(self, numClient : int) -> dict:
        """Setiap kali dipanggil websocket server akan membuat token baru
        bersama dengan jumlah klien yang ingin dibuat
        """
        for i in range(numClient):
            hexUUID = uuid.uuid4().hex
            self.setClient[hexUUID[:5]] = hexUUID

        return self.setClient
    



#===================================================================
# This part to create Asyncronouse TCP Server
#===================================================================
class AsyncServer(asyncio.Protocol):
    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        peername = transport.get_extra_info("peername")
        self.transport = transport
    
    def connection_lost(self, exc: Exception | None) -> None:
        print("Connection lost")
        print(f"Error : {exc}")
    
    def data_received(self, data: bytes) -> None:
        print(data)
    
class TCPServer:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
    
    async def TCPRun(self, host:str, port:int) -> None:
        # Get event loop
        loop = asyncio.get_running_loop()
        
        server = await loop.create_server(
            AsyncServer, host=host, port=port
        )

        async with server:
            await server.serve_forever()
            

    
