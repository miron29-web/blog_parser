import asyncio

from parser.settings import *
from parser.http_client import HttpClient
from parser.data_parser import BlogParser

async def parse_process(current_page:int, client:HttpClient, parser:BlogParser):
    current_url = f"{BASE_URL}?page={current_page}"

    html = await client.fetch(current_url)
    article = parser.article_parse(html)

    return article

async def main():
    result_ls = list()
    blog_parser = BlogParser()

    async with HttpClient(headers=HEADERS) as client:
        html = await client.fetch(BASE_URL)
        page_count = blog_parser.get_page_count(html)
        
        tasks = [
            parse_process(page, client, blog_parser)
            for page in range(1, page_count+1)
        ]

        articles = await asyncio.gather(*tasks)

        for article in articles:
            result_ls.extend(article)

        print(f"Найдено: {len(result_ls)} статей")

    
if __name__ == "__main__":
    asyncio.run(main())