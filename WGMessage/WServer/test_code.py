
import asyncio
from WGMServer import WSServer
from db.modules import WMCreateTable, WMCRUDServerUsers


"""
Bagian ini digunakan untuk pengujian untuk mengetahui apakah sudah berfungsi atau tidak
setiap fungsi WudiSDK
"""
async def Testing1():
    ser = WSServer()
    ser.WSRun(host="192.168.0.190", port=8000)

async def Testing2():
    """ Testing untuk menguji akses ke database """
    db = WMCRUDServerUsers()
    await db.WConnect_db()
    await db.WCreate_tbl()
    print("Berhasil Membuat table")

async def main():
    pass

if __name__ == "__main__":
    asyncio.run(main())