from bs4 import BeautifulSoup
import re

class BlogParser:
    def __init__(self):
        pass

    def get_page_count(self, html):
        if not html:
            return None

        soup = BeautifulSoup(html, "html.parser")
        pag = soup.find("nav", class_=re.compile(r"^styles_pagination")).find("span")
        page_count = pag.find_next("button").text

        return int(page_count)

    def article_parse(self, html:str):
        if not html:
            return None
        
        result = list()
    
        soup = BeautifulSoup(html, "html.parser")
        card_body = soup.find_all("div", class_=re.compile(r"^styles_cardBody"))

        for aticle in card_body:
            title = aticle.find("p", class_=re.compile(r"^styles_cardTitle"))
            short_desc = title.find_next_sibling("p")

            article = dict()
            article["title"] = title.text.rstrip()
            article["short_desc"] = short_desc.text.rstrip()
            result.append(article)

        return result