from .request import Request
from .translations import Translations
from bs4 import BeautifulSoup


class MovieInfo:
    def __init__(self, url: str):
        self.url = url.split('.html')[0] + '.html'
        self.page = Request(self.url).get_page().content
        self.soup = BeautifulSoup(self.page, 'html.parser')
        self.info = None

    def __str__(self):
        s = ''
        info = self.__get_info()
        if info['type'] == 'movie':
            s += f'Фильм | {info["name"]}\n'
        else:
            s += f'Сериал | {info["name"]}\nКоличество сезонов: {info["number_of_seasons"]}\n'
        s += f'Длительность: {info["duration"]}\n' \
             f'Рейтинг IMDb - {info["rating_imdb"]}\n' \
             f'Рейтинг Кинопоиск - {info["rating_kp"]}\n' \
             f'Жанр:'
        for i in info['genre']:
            s += f' {i}'
        if info["translations_list"]:
            s += f'\nОзвучки: {info["translations_list"]}'

        return s

    def __get_info(self):
        if 'series' in self.url:
            return self.series_info()
        elif 'films' in self.url:
            return self.movie_info()
        else:
            return 'Wrong link!'

    def series_info(self):
        return {
            'type': 'series',
            'name': self.soup.select_one("h1").text,
            'number_of_seasons': len(self.soup.select('#simple-seasons-tabs > li')),
            'duration': self.soup.find('td', itemprop='duration').text,
            'rating_imdb': self.soup.select_one('span.b-post__info_rates.imdb > span').text,
            'rating_kp': self.soup.select_one('span.b-post__info_rates.kp > span').text,
            'genre': [i.text for i in self.soup.findAll('span', itemprop='genre')],
            'translations_list': Translations(self.soup).get()
        }

    def movie_info(self):
        return {
            'type': 'movie',
            'name': self.soup.select_one("h1").text,
            'duration': self.soup.find('td', itemprop='duration').text,
            'rating_imdb': self.soup.select_one('span.b-post__info_rates.imdb > span').text,
            'rating_kp': self.soup.select_one('span.b-post__info_rates.kp > span').text,
            'genre': [i.text for i in self.soup.findAll('span', itemprop='genre')],
            'translations_list': Translations(self.soup).get()
        }
