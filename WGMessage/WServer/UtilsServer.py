import asyncio
import aiohttp
from aiohttp import web


#--------------------------------------------------
# Kelas ini berfungsi sebagai utility websocket server
# agar dapat bekerja dengan baik dimana menyediakan fungsi pendukung
# untuk menangani koneksi masuk
#---------------------------------------------------
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
