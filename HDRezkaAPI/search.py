from bs4 import BeautifulSoup
from .request import Request


class Search:
    def __init__(self, search_text: str):
        self.url = 'https://rezka.ag/search/'
        self.search_text = search_text
        self.search_response = Request(self.url).get_page(params={'do': 'search',
                                                                  'subaction': 'search',
                                                                  'q': self.search_text}
                                                          ).content
        self.search_data = BeautifulSoup(self.search_response, 'html.parser')
        self.results = self.search_data.select('div.b-content__inline_item')
        self.titles_list = []
        self.__get_info()

    def __iter__(self):
        return iter(self.titles_list)

    def __str__(self):
        s = ''
        for title in self.titles_list:
            s += (f'{title["id"]} - Название: {title["name"]} | Год: {title["info"]["year"]} | '
                  f'Страна: {title["info"]["country"]} | Жанр: {title["info"]["genre"]}\n')
        return s[:-1]

    def __get_info(self):
        for title in self.results:
            self.titles_list.append({'id': len(self.titles_list)+1,
                                     'name': title.select_one('div.b-content__inline_item-link > a')
                                    .text,
                                     'info': {'type': title.select_one('div.b-content__inline_item-cover > a '
                                                                       '> span > i.entity')
                                    .text,
                                              'year': title.select_one('div.b-content__inline_item-link > div')
                                    .text.split(',')[0],
                                              'country': title.select_one('div.b-content__inline_item-link > div')
                                    .text.split(',')[1],
                                              'genre': title.select_one('div.b-content__inline_item-link > div')
                                    .text.split(',')[2]},
                                     'data-id': title['data-id'],
                                     'url': title.select_one('div > a')['href']})

    def get_url(self) -> str:
        print(self.__str__())
        id = int(input('Enter title number: '))
        return self.titles_list[id - 1]['url']
