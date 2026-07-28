import aiohttp
import asyncio
from aiohttp_socks import ProxyConnector

async def test():
    connector = ProxyConnector.from_url('socks5://127.0.0.1:10808')
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get('http://ifconfig.me') as resp:
            print(await resp.text())

asyncio.run(test())
