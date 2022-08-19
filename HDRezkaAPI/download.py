import sys
from os import path
from bs4 import BeautifulSoup
from .request import Request
from .get_stream import GetStream
from tqdm import tqdm


class Download:
    def __init__(self, download_data):
        self.data = download_data
        self.url = download_data['url']
        response = Request().get(self.url)
        self.soup = BeautifulSoup(response.content, 'html.parser')
        self.favs = self.soup.find('input', id='ctrl_favs').get('value')

    def download_season(self, season):
        if self.data['type'] == 'movie':
            return
        if season > self.data['seasons_count']:
            return
        episodes_list = self.soup.find('ul', id=f'simple-episodes-list-{season}')
        episodes_count = len(episodes_list.findAll('li'))
        if self.data['translations_list']:
            translator_id = self.__get_translation()
        else:
            translator_id = self.__detect_translation()

        for i in range(1, episodes_count + 1):
            self.download_episode(season, i, translator_id, True)

        print('Скачивание успешно завершено!')

    def download_episode(self, season, episode, translator_id=None, multi_download=False):
        if self.data['type'] == 'movie':
            return
        if season > self.data['seasons_count']:
            return
        episodes_list = self.soup.find('ul', id=f'simple-episodes-list-{season}')
        episodes_count = len(episodes_list.findAll('li'))
        if episode > episodes_count:
            return
        if not multi_download:
            if self.data['translations_list']:
                translator_id = self.__get_translation()
            else:
                translator_id = self.__detect_translation()

        data = {
            'id': self.data['data-id'],
            'translator_id': translator_id,
            'favs': self.favs,
            'season': season,
            'episode': episode,
            'action': 'get_stream'
        }

        url = GetStream().get_stream(data)
        if url:
            file_name = f"{self.data['name']} {season}s{episode}e.mp4"
            fullpath = path.join(path.curdir, file_name)

            with Request().get(url, stream=True) as r, open(fullpath, "wb") as f, tqdm(
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                    total=int(r.headers.get('content-length', 0)),
                    file=sys.stdout,
                    desc=file_name
            ) as progress:
                for chunk in r.iter_content(chunk_size=4096):
                    if chunk:
                        datasize = f.write(chunk)
                        progress.update(datasize)
        if not multi_download:
            print('Скачивание успешно завершено!')

    def download_movie(self):
        if self.data['type'] == 'series':
            return

    def __get_translation(self) -> int:
        for i, translation in zip(range(1, len(self.data['translations_list'])), self.data['translations_list']):
            print(f'{i} - {translation["name"]}')
        translation_id = self.data['translations_list'][int(input("Введите номер озвучки: ")) - 1]['id']
        return translation_id

    def __detect_translation(self):
        if self.data['type'] == 'movie':
            event_type = 'initCDNMoviesEvents'
        else:
            event_type = 'initCDNSeriesEvents'

        tmp = str(self.soup).split(f"sof.tv.{event_type}")[-1].split("{")[0]
        translator_id = tmp.split(",")[1].strip()

        return translator_id
