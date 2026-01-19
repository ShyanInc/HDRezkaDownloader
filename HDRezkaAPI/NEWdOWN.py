import sys
import  os
import requests
from tqdm import tqdm
# from .history import  History
from concurrent.futures import ThreadPoolExecutor

def download_file(download_data):
    if download_data['stream_url']:
        print(download_data['file_name'])
        fullpath = os.path.join(os.path.curdir, download_data['file_name'])
        
        # Send HEAD request to get file size
        response = requests.head(download_data['stream_url'])
        total_size = int(response.headers.get('content-length', 0))

        # Download the file using GET request
        with requests.get(download_data['stream_url'], stream=True) as r:
            with open(fullpath, "wb") as f, tqdm(
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                    total=total_size,
                    file=sys.stdout,
                    desc=download_data['file_name']
            ) as progress:
                for chunk in r.iter_content(chunk_size=1024*4):
                    if chunk:
                        datasize = f.write(chunk)
                        progress.update(datasize)

data = {
            "stream_url": "https://stream.voidboost.cc/6fac7ad9ce36bdd25731bbca2a92e3c7:2024042219:QXlQUFEyYnNlVzBZOExha1Z0YVdHYUV3NVVrTXhGU2VYaXY0ZFBtLzhmL2lYcHprMVFJbXJKM0ZhS0VsMGtyMXcrOHJKSkg3Syt2djRsWEhYL1oyS2c9PQ==/1/3/5/0/1/1/7kqf9.mp4",

            'file_name': 'test.mp4'

        }
download_file(data)
