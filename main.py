import asyncio

from parser.settings import *
from parser.http_client import HttpClient
from parser.data_parser import BlogParser

from storage.model import Article
from storage.sqlite_storage import SQLiteStorage

async def parse_process(current_page:int, client:HttpClient, parser:BlogParser):
    """
    Загружает и парсит статьи одной страницы блога.
    Args:
        current_page (int): номер страницы пагинации
        client (HttpClient): HTTP клиент для запроса HTML
        parser (BlogParser): парсер HTML → статьи

    Returns:
        list[dict]: список статей с одной страницы
    """
    current_url = f"{BASE_URL}?page={current_page}"

    html = await client.fetch(current_url)
    article = parser.article_parse(html)

    return article

def get_new_articles(result_ls: list[dict], bd_ls: list[dict]) -> list[dict]:
    """
    Возвращает список новых статей, которых нет в базе данных.

    Сравнение выполняется по полю `title` без учёта регистра и пробелов.

    Args:
        result_ls (list[dict]): статьи, полученные с сайта
        bd_ls (list[dict]): статьи, уже сохранённые в БД

    Returns:
        list[dict]: только новые статьи
    """
    bd_titles = {
        item["title"].strip().lower()
        for item in bd_ls
    }

    new_articles = [
        item for item in result_ls
        if item["title"].strip().lower() not in bd_titles
    ]
    return new_articles

def print_menu():
    """
    Выводит меню в консоль
    """
    print()
    print("(1) Считать статьи с сайта")
    print("(2) Сохранить данные в БД")
    print("(3) Показать первые 5 статей считанных из бд")
    print("(4) Выйти из программы")

async def main():
    blog_parser = BlogParser()
    storage = SQLiteStorage(Article)

    model_article = Article()
    model_article.create_table()

    result_ls = list()

    bd_ls = storage.get_from_sqlite()
    print(f"Считано {len(bd_ls)} записей из БД")


    print_menu()

    while True:
        command = input(">>> ")

        if command == "1":
            async with HttpClient(headers=HEADERS) as client:
                html = await client.fetch(BASE_URL)
                if not html:
                    print("ошибка при получении количества страниц пагинации")
                    continue

                page_count = blog_parser.get_page_count(html)
                
                tasks = [
                    parse_process(page, client, blog_parser)
                    for page in range(1, page_count+1)
                ]

                articles = await asyncio.gather(*tasks)

                for article in articles:
                    result_ls.extend(article)

                new_articles = get_new_articles(result_ls, bd_ls)

                print(f"Всего спарсили: {len(result_ls)} статей")
                print(f"Всего новых статей: {len(new_articles)}")
                print(f"Выберите (2) для сохранения в БД")

                print_menu()
                
        elif command == "2":
            if result_ls:
                storage.save_to_sqlite(result_ls)

                new_articles = get_new_articles(result_ls, bd_ls)
                print(f"Успешно записано {len(new_articles)} новых статей")
                bd_ls = storage.get_from_sqlite()
            else:
                print("Нет новых считанных данных для сохранения в БД")
            print_menu()
        elif command == "3":
            if not bd_ls:
                print("Нет считанных из БД данных")
                print("Выберите пункт (1) для загрузки данных из блога")
            else:
                print("work")
                for i in range(0, 5):
                    article = bd_ls[i]
                    print(f"Заголовок = {article["title"]}")
                    print(f"Описание = {article["desc"]}")
                    print("<<<<<<--------------->>>>>>")

                print_menu()

        elif command == "4":
            print("программа успешно завершена")
            break
        else:
            print("Введена неизвестная комманда")
    
if __name__ == "__main__":
    asyncio.run(main())