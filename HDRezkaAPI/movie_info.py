from .request import Request
from bs4 import BeautifulSoup


class MovieInfo:
    def __init__(self, url: str):
        self.url = url.split('.html')[0] + '.html'
        self.page = Request(self.url).get_page().content
        self.soup = BeautifulSoup(self.page, 'html.parser')
        self.info = None

    def __str__(self):
        s = ''
        s += self.soup.select_one('h1').text
        return s

    def __get_info(self):
        pass
