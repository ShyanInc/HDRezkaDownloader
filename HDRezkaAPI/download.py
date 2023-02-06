import sys
import os
from os import path
from bs4 import BeautifulSoup
from .request import Request
from .get_stream import GetStream
from tqdm import tqdm
from slugify import slugify
from pathlib import Path


class Error(Exception):
    """Base class for other exceptions"""
    pass


class IncorrectEpisodeNumberException(Error):
    """Raised when incorrect episode number was in input"""
    pass


class EpisodeNumberIsOutOfRange(Error):
    """Raised when episode number is out of range of available episodes"""
    pass


class Download:
    def __init__(self, download_data, dorl):
        self.data = download_data
        self.dorl = dorl
        self.all = download_data['allepisodes']
        self.url = download_data['url']
        response = Request().get(self.url)
        self.soup = BeautifulSoup(response.content, 'html.parser')
        self.favs = self.soup.find('input', id='ctrl_favs').get('value')
        print(self.quality)
        if self.dorl == "pls":
            self.name = slugify(
                self.data['name'], allow_unicode=True, lowercase=False)
            self.filee = open(f"{self.data['data-id']}-{self.name}.list", "w")
        if self.data['translations_list']:
            self.translator_id = self.__get_translation()
        else:
            self.translator_id = self.__detect_translation()


    def download_all_serial(self):
        correct_season = False
        seasons_count = self.data['seasons_count']
        while not correct_season:
            try:
                for season in range(1, seasons_count + 1):
                    episodes_count = self.data['seasons_episodes_count'][season]
                    self.download_episodes(season, 1, episodes_count)
                correct_season = True
            except EpisodeNumberIsOutOfRange:
                print('Неверный диапазон эпизодов!')
        print('Скачивание успешно завершено!')

    def download_seasons(self, start, end):
        for season in range(start, end + 1):
            if season < 1 or season > self.data['seasons_count']:
                continue
            self.download_season(season)

    def download_season(self, season):
        if season < 1 or season > self.data['seasons_count']:
            # TODO Make new custom exception for incorrect season number and realize it
            return

        episodes_list = self.soup.find(
            'ul', id=f'simple-episodes-list-{season}')
        episodes_count = len(episodes_list.findAll('li'))

        
        for i in range(1, episodes_count + 1):
            self.download_episode(season, i, True)

    def download_episodes(self, season, start, end):
        if season < 1 or season > self.data['seasons_count']:
            # TODO Make new custom exception for incorrect season number and realize it
            return

        episodes_list = self.soup.find(
            'ul', id=f'simple-episodes-list-{season}')
        episodes_count = len(episodes_list.findAll('li'))

        if end > episodes_count or start < 0:
            raise EpisodeNumberIsOutOfRange

        for i in range(start, end + 1):
            self.download_episode(season, i, True)

    def download_episode(self, season, episode, multi_download=False):
        if self.data['type'] == 'movie':
            return
        if season > self.data['seasons_count']:
            return

        if episode < 1 or episode > self.data['seasons_episodes_count'][season]:
            raise IncorrectEpisodeNumberException

        data = {
            'id': self.data['data-id'],
            'translator_id': self.translator_id,
            'favs': self.favs,
            'season': season,
            'episode': episode,
            'action': 'get_stream'
        }

        stream_url = GetStream().get_series_stream(data)
        downloaded_folder = slugify(self.data['data-id'],
            self.data['name'], allow_unicode=True, lowercase=False)
        if self.dorl != "pls":
            os.makedirs(downloaded_folder, exist_ok=True)
        season = str(season).zfill(2)
        episode = str(episode).zfill(2)
        file_name = f"{downloaded_folder}/s{season}e{episode}.mp4"

        download_data = {
            'stream_url': stream_url,
            'file_name': file_name,

        }

        self.__download(download_data)

    def download_movie(self):
        if self.data['type'] == 'series':
            return

        data = {
            'url': self.url
        }

        stream_url = GetStream().get_movie_stream(data)
        file_name = f"{self.data['name']}.mp4"
        # TODO Fix file name bug
        # file_name = f"test.mp4"

        download_data = {
            'stream_url': stream_url,
            'file_name': file_name,
        }

        self.__download(download_data)

    def __download(self, download_data):
        if download_data['stream_url']:
            i = 0
            if self.dorl == "pls":
                self.filee.write(download_data['stream_url'] + "\n")

            elif self.data['type'] == 'series':
                os.system(f"bomi {download_data['stream_url']}")
            else:
                fullpath = path.join(path.curdir, download_data['file_name'])

                with Request().get(download_data['stream_url'], stream=True) as r, open(fullpath, "wb") as f, tqdm(
                        unit="B",
                        unit_scale=True,
                        unit_divisor=1024,
                        total=int(r.headers.get('content-length', 0)),
                        file=sys.stdout,
                        desc=download_data['file_name']
                ) as progress:
                    for chunk in r.iter_content(chunk_size=4096):
                        if chunk:
                            datasize = f.write(chunk)
                            progress.update(datasize)
            print(i)

    def convert_to_pls(self):
        file_name = self.filee.name
        self.filee.close()
        with open(file_name, 'r') as f:
            url_list = [line.strip() for line in f]
        with open(f"{self.name}.pls", 'w') as f:
            f.write("[playlist]\n")
            for i, url in enumerate(url_list):
                f.write(f"File{i+1}={url}\n")
                f.write(f"Title{i+1}=Track {i+1}\n")
            print(f'Pls len: {len(url_list)}')
            print(self.all)
            f.write(f"NumberOfEntries={len(url_list)}\n")
            f.write("Version=2\n")

    def __get_translation(self) -> int:
        for i, translation in zip(range(1, len(self.data['translations_list'])), self.data['translations_list']):
            print(f'{i} - {translation["name"]}')
        translation_id = self.data['translations_list'][int(
            input("Введите номер озвучки: ")) - 1]['id']
        return translation_id

    def __detect_translation(self):
        if self.data['type'] == 'movie':
            event_type = 'initCDNMoviesEvents'
        else:
            event_type = 'initCDNSeriesEvents'

        tmp = str(self.soup).split(f"sof.tv.{event_type}")[-1].split("{")[0]
        translator_id = tmp.split(",")[1].strip()

        return translator_id
