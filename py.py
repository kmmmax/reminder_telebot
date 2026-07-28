#def get_name(source: str) -> str:
#    list = source.split()
#    if len(list) == 3:
#        if len(list[0]) == 5 and len(list[1]) == 8:
#            if len(list[2]) > 2 and len(list[2]) < 41:
#                return list[2]
#    return ""
#print(get_name("19:21 25.07.26 physics"))

import aiohttp
import asyncio
from aiohttp_socks import ProxyConnector

async def test():
    connector = ProxyConnector.from_url('socks5://127.0.0.1:10808')
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get('http://ifconfig.me') as resp:
            print(await resp.text())

asyncio.run(test())
