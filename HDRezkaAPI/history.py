import json

class History:
    def __init__(self):
        self._load_data()

    def _load_data(self):
        try:
            with open('history.json', 'r') as json_file:
                data = json.load(json_file)
            self._movie_data = data.get('movie_data', {})
            self._quality = data.get('quality', '')
            self._dorl = data.get('dorl', '')
            self._download_type = data.get('download_type', {})
            self._translator_id = data.get('translator_id', '')
            self._status = data.get('status', '')
            self._run_season = data.get('run_season', '')
            self._run_episode = data.get('run_episode', '')
        except FileNotFoundError:
            self._movie_data = {}
            self._quality = ''
            self._dorl = ''
            self._download_type = {}
            self._translator_id = ''
            self._status = ''
            self._run_season = ''
            self._run_episode = ''

    def _save_data(self):
        data = {
            'movie_data': self._movie_data,
            'quality': self._quality,
            'dorl': self._dorl,
            'download_type': self._download_type,
            'translator_id': self._translator_id,
            'status': self._status,
            'run_season': self._run_season,
            'run_episode': self._run_episode
        }
        with open('history.json', 'w') as json_file:
            json.dump(data, json_file)

    @property
    def movie_data(self):
        return self._movie_data

    @movie_data.setter
    def movie_data(self, value):
        self._movie_data = value
        self._save_data()

    @property
    def quality(self):
        return self._quality

    @quality.setter
    def quality(self, value):
        self._quality = value
        self._save_data()

    @property
    def dorl(self):
        return self._dorl

    @dorl.setter
    def dorl(self, value):
        self._dorl = value
        self._save_data()

    @property
    def download_type(self):
        return self._download_type

    @download_type.setter
    def download_type(self, value):
        self._download_type = value
        self._save_data()

    @property
    def translator_id(self):
        return self._translator_id

    @translator_id.setter
    def translator_id(self, value):
        self._translator_id = value
        self._save_data()

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
        self._save_data()

    @property
    def run_season(self):
        return self._run_season

    @run_season.setter
    def run_season(self, value):
        self._run_season = value
        self._save_data()

    @property
    def run_episode(self):
        return self._run_episode

    @run_episode.setter
    def run_episode(self, value):
        self._run_episode = value
        self._save_data()


