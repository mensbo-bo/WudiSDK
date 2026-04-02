import asyncio
import aiohttp
from aiohttp import web

from typing import Any
#--------------------------------------------------
# Kelas ini berfungsi sebagai utility websocket server
# agar dapat bekerja dengan baik dimana menyediakan fungsi pendukung
# untuk menangani koneksi masuk
#---------------------------------------------------

class WSServerClient:
    def __init__(self) -> None:
        """ Objek untuk menyimpan daftar client yang terkoneksi dan melakukan komunikasi dengan klien"""
        self.client_dt = {}
    def __setattr__(self, name: str, value: Any) -> None:
        pass
    def WSGetClient(self) -> Any:
        return self.client_dt
    
    def WSSetClient(self, ws) -> Any:
        assert ws != None
        self.client_dt = ws

    async def WSSent_str(self, receiver, data):
        pass

    async def WSSent_bytes(self, receiver, data):
        pass

    async def WSSent_json(self, receiver, data):
        pass


class WSProtocol:
    def __init__(self) -> None:
        """
        WSProtocol adalah utility kelas untuk menjalankan Websocket Server pada class WSServer
        didalam file WGMServer
        """
        pass

    async def WebsocketServer(self, request : web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse(max_msg_size=0)
        await ws.prepare(request)

        print("Websocket Running")
        async for msg in ws:
            json_send = {}
            if msg.type == web.WSMsgType.TEXT:
                if msg.data == "close":
                    await ws.close()
                else:
                    print(msg.data)

            elif msg.type == web.WSMsgType.ERROR:
                print(f"Websocket connection error : {ws.exception()}")

            else:
                print(f"Data received: {msg.data}")

        print("Websocket close")
        return ws

    async def WSRunServer(self, host : str, port : int) -> None:
        app = web.Application()
        app.add_routes([web.get("/ws", self.WebsocketServer)])

        web.run_app(app, host=host, port=port)
