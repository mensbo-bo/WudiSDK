
import asyncio
import aiohttp
from aiohttp import web, BasicAuth

routes = web.RouteTableDef()

@routes.get("/ws", name="websocket")
async def WebSocket_View(request):
    print(request.headers)
    print(request.headers.get("Ser-Token", "Kosong"))
    print(request.headers.get("Cli-Token", "Kosong"))

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            if msg.data == "close":
                await ws.close()
            print(msg.data)

        elif msg.type == web.WSMsgType.ERROR:
            print("Websocket error")

        else:
            print("Unhandle data : ")
            print(msg.data)

    print("Websocket close")
    return ws

@routes.get("", name="index")
async def Index_View(request):
    print("======== HEADERS ========")
    print(request.headers)
    return web.Response(text="Simple Hello")

app = web.Application()
app.add_routes(routes)

web.run_app(app, host="127.0.0.1", port=8000)

