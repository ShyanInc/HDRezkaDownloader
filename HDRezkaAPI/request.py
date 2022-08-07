import requests


class Request:
    def __init__(self, url: str):
        self.url = url
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/103.0.0.0 Safari/537.36 '
        }

    def get_page(self, params=None):
        return requests.get(self.url, params=params, headers=self.HEADERS)

    def post_request(self, data):
        return requests.post(self.url, data=data, headers=self.HEADERS)
