import sys
import  os
from .request import Request
from .get_stream import GetStream
from .history import  History
from tqdm import tqdm


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
    def __init__(self, download_data, quality):
        self.data = download_data
        self.quality = quality
        self.url = download_data['url']
        self.name = download_data['url'].split('/')[-1].split('.')[0]

        if self.data['translations_list']:
            self.translator_id = self.__get_translation()
            if download_data.get("seasons_episodes_count") == 0:
                # If there are no seasons and episodes 
                print("select again:")
                self.translator_id = self.__get_translation()
        else:
            self.translator_id = self.__detect_translation()


    def download_all_serial(self):
        correct_season = False
        seasons_count = self.data['seasons_count']
        while not correct_season:
            try:
                if History().status == 'run' and History().run_season !="":
                    season = History().run_season()
                    self.download_seasons(season, seasons_count +1)
                else:
                    for season in range(1, seasons_count + 1):
                        self.download_season(season)
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

        episodes_count = self.data['seasons_episodes_count'][season]
        History().run_season = season

        if History().status == 'run' and History().run_episode !="":
            start = History( ).run_episode
        else:
            start = 1

        for i in range(start, episodes_count + 1):
            self.download_episode(season, i)

    def download_episodes(self, season, start):
        print(season)
        end = self.data['seasons_episodes_count'][season]
        if season < 1 or season > self.data['seasons_count']:
            # TODO Make new custom exception for incorrect season number and realize it
            return

        episodes_count = self.data['seasons_episodes_count'][season]


        if end > episodes_count or start < 0:
            raise EpisodeNumberIsOutOfRange

        for i in range(start, end + 1):
            self.download_episode(season, i)

    def download_episode(self, season, episode):
        if self.data['type'] == 'movie':
            return
        if season > self.data['seasons_count']:
            return

        if episode < 1 or episode > self.data['seasons_episodes_count'][season]:
            raise IncorrectEpisodeNumberException

        data = {
            'id': self.data['data-id'],
            'translator_id': self.translator_id,
            # 'favs': self.favs,
            'season': season,
            'episode': episode,
            'action': 'get_stream',
            'quality': self.quality
        }
        
        print(episode)
        History().run_episode = episode

        stream_url = GetStream().get_series_stream(data)
        downloaded_folder = f"../{self.name}"
        # downloaded_folder = self.name
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
            'url': self.url,
            'quality': self.quality
        }

        stream_url = GetStream().get_movie_stream(data)
        # TODO Fix file name bug

        download_data = {
            'stream_url': stream_url,
            'file_name': self.name,
        }

        self.__download(download_data)

    @staticmethod
    def __download( download_data):
        if download_data['stream_url']:
            print (download_data['file_name'])
            History().status = "run"
            fullpath = os.path.join(os.path.curdir, download_data['file_name'])

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
            History().run_episode = History().run_episode + 1
            

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
            print(self.download_data['allepisodes'])
            f.write(f"NumberOfEntries={len(url_list)}\n")
            f.write("Version=2\n")

    def __get_translation(self) -> int:
        if History().status == 'run':
            translation_id = History().translator_id
        else:
            for i, translation in zip(range(1, len(self.data['translations_list'])), self.data['translations_list']):
                print(f'{i} - {translation["name"]}')
            translation_id = self.data['translations_list'][int(
                input("Введите номер озвучки: ")) - 1]['id']
        History().translator_id = translation_id

        return translation_id

    # def __detect_translation(self):
    #     if self.data['type'] == 'movie':
    #         event_type = 'initCDNMoviesEvents'
    #     else:
    #         event_type = 'initCDNSeriesEvents'

    #     tmp = str(self.soup).split(f"sof.tv.{event_type}")[-1].split("{")[0]
    #     translator_id = tmp.split(",")[1].strip()

    #     return translator_id
