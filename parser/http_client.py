import aiohttp

class HttpClient:
    def __init__(self, headers):
        self._session:aiohttp.ClientSession = None
        self._headers = headers

    # асинхронный волшебный метод __enter__
    async def __aenter__(self):
        self._session = aiohttp.ClientSession(headers=self._headers)
        return self

    # асинхронный волшебный метод __exit__
    async def __aexit__(self, exc_type, exc, tb):
        await self._session.close()

    async def fetch(self, url):
        try:
            async with self._session.get(url) as resp:
                print(f"status={resp.status} url={url}")
                if resp.status == 200:
                    html = await resp.text()
                    return html
                return None
        except aiohttp.ClientResponseError as e:
            print(f"Ошибка: status={e.status}")
        