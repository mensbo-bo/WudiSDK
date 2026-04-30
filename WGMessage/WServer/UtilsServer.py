import asyncio
import aiohttp
from aiohttp import web

from typing import Any
import json

from db import modules
from db.caching import WRedis

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
        """ Mengambil klien yang terkoneksi kedalam jaringan"""
        return self.client_dt
    
    def WSSetClient(self, ws) -> Any:
        assert ws != None
        self.client_dt = ws

    async def WSSent_str(self, receiver, data):
        # Mengirim data string ke target token bersama dengan token server
        pass

    async def WSSent_bytes(self, receiver, data):
        # Mengirim data bytes ke target token bersama dengan token server
        pass

    async def WSSent_json(self, receiver, data):
        # Mengirim data json ke target token bersama dengan token server
        pass


class WSProtocol(WSServerClient):
    def __init__(self) -> None:
        super().__init__()
        """
        WSProtocol adalah utility kelas untuk menjalankan Websocket Server pada class WSServer
        didalam file WGMServer
        """
        pass

    async def WebsocketServer(self, request : web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse(max_msg_size=0)
        await ws.prepare(request)

        redis = request.app['redis']
        
        print("Websocket Running")
        access = False
        async for msg in ws:
            json_send = {}
            if access:
                """ 
                Bagian yang akan diakses jika Server Token dan Klien Token
                sudah di verfikasi
                """
                if msg.type == web.WSMsgType.TEXT:
                    data_text = json.loads(msg.data)
                    if data_text['type'] == "close":
                        await ws.close()
                    else:
                        print(msg.data)
                
                elif msg.type == web.WSMsgType.BINARY:
                    print("Receive binary")
                
                elif msg.type == web.WSMsgType.CLOSED:
                    print("Webocket close connection")

                elif msg.type == web.WSMsgType.ERROR:
                    print(f"Websocket connection error : {ws.exception()}")

                else:
                    print(f"Data received: {msg.data}")

            else:
                """ 
                Bagian yang akan diakses jika data server token dan klien token di 
                database belum di verifikasi dan ini hanya di akses sekali jika verifikasi
                gagal maka websocket akan memanggil await ws.close()
                """
                if msg.type == web.WSMsgType.TEXT:
                    try:

                        data_akses = json.loads(msg.data)
                        #print(data_akses)
                        print(data_akses['serverToken'])

                        print(data_akses['clientToken'])
                    except Exception as e:
                        print(e)


        print("Websocket close")
        return ws
    
    """ Fungsi yang akan di pangil saat aplikasi web pertamakali di jalankan """
    async def on_startup(self, app):
        # Menjalankan aplikasi redis di background agar di gunakana
        # didalam aplikasi server
        app['redis'] = WRedis.RedisCache()
        await app['redis'].WRedisConnect()

    """ Fungsi yang akan dipangil saat aplikasih ingin dimatikan """
    async def on_cleanup(self, app):
        # Menutup koneksi dengan redis 
        await app['redis'].WRedisClose()

    def WSRunServer(self, host : str, port : int) -> None:
        app = web.Application()
        app.on_startup.append(self.on_startup)
        app.on_cleanup.append(self.on_cleanup)

        app.add_routes([web.get("/ws", self.WebsocketServer)])

        web.run_app(app, host=host, port=port)
