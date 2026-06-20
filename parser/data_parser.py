from bs4 import BeautifulSoup
import re

class BlogParser:
    """
    Парсер блога статей для получения количества страниц и списка статей
    """
    def __init__(self):
        pass

    def get_page_count(self, html):
        """
        Получает количество страниц пагинации
        """
        if not html:
            return None

        soup = BeautifulSoup(html, "html.parser")
        pag = soup.find("nav", class_=re.compile(r"^styles_pagination")).find("span")
        if not pag:
            return None
        
        page_count = pag.find_next("button").text
        if not page_count:
            return None

        return int(page_count)

    def article_parse(self, html:str):
        """
        Извлекает список статей из страницы HTML
        """
        if not html:
            return None
        
        result = list()
    
        soup = BeautifulSoup(html, "html.parser")
        card_body = soup.find_all("div", class_=re.compile(r"^styles_cardBody"))
        if not card_body:
            return None

        for aticle in card_body:
            title = aticle.find("p", class_=re.compile(r"^styles_cardTitle"))
            short_desc = title.find_next_sibling("p")

            article = dict()
            article["title"] = title.text.rstrip()
            article["desc"] = short_desc.text.rstrip()
            result.append(article)

        return result