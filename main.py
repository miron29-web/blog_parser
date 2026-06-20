import asyncio
import aiohttp

from parser.settings import *
from parser.http_client import HttpClient

async def main():
    async with HttpClient(headers=HEADERS) as client:
        data = await client.fetch(BASE_URL)
        print(data)

if __name__ == "__main__":
    asyncio.run(main())