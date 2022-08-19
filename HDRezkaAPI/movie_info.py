from .request import Request
from .translations import Translations
from bs4 import BeautifulSoup


class MovieInfo:
    def __init__(self, movie_data):
        self.data = movie_data
        self.url = movie_data['url'].split('.html')[0] + '.html'
        self.page = Request().get(self.url).content
        self.soup = BeautifulSoup(self.page, 'html.parser')
        self.info = None

    def __str__(self):
        s = ''
        info = self.get_data()
        if info['type'] == 'movie':
            s += f'Фильм | {info["name"]}\n'
        else:
            s += f'Сериал | {info["name"]}\nКоличество сезонов: {info["seasons_count"]}\n'
        s += f'Год выпуска: {info["year"]}\n' \
             f'Страна:{info["country"]}\n' \
             f'Длительность: {info["duration"]}\n' \
             f'Рейтинг IMDb - {info["rating_imdb"]}\n' \
             f'Рейтинг Кинопоиск - {info["rating_kp"]}\n' \
             f'Жанр:'
        for i in info['genre']:
            s += f' {i}'
        if info["translations_list"]:
            s += '\nОзвучки: '
            for i in info['translations_list']:
                s += f'{i["name"]}, '
        return s

    def get_data(self):
        if 'series' in self.url:
            return self.series_info()
        elif 'films' in self.url:
            return self.movie_info()
        else:
            return 'Wrong link!'

    def series_info(self):
        data = {
            'type': 'series',
            'name': self.data['name'],
            'year': self.data['info']['year'],
            'country': self.data['info']['country'],
            'seasons_count': len(self.soup.select('#simple-seasons-tabs > li')),
            'rating_imdb': None,
            'rating_kp': None,
            'duration': self.soup.find('td', itemprop='duration').text,
            'genre': [i.text for i in self.soup.findAll('span', itemprop='genre')],
            'translations_list': Translations(self.soup).get(),
            'data-id': self.data['data-id'],
            'url': self.url
        }
        try:
            rating_imdb = self.soup.select_one('span.b-post__info_rates.imdb > span').text
            data.update({'rating_imdb': rating_imdb})
        except AttributeError:
            pass
        try:
            rating_kp = self.soup.select_one('span.b-post__info_rates.kp > span').text
            data.update({'rating_kp': rating_kp})
        except AttributeError:
            pass
        return data

    def movie_info(self):
        return {
            'type': 'movie',
            'name': self.data['name'],
            'year': self.data['info']['year'],
            'country': self.data['info']['country'],
            'duration': self.soup.find('td', itemprop='duration').text,
            'rating_imdb': self.soup.select_one('span.b-post__info_rates.imdb > span').text,
            'rating_kp': self.soup.select_one('span.b-post__info_rates.kp > span').text,
            'genre': [i.text for i in self.soup.findAll('span', itemprop='genre')],
            'translations_list': Translations(self.soup).get(),
            'data-id': self.data['data-id'],
            'url': self.url
        }
