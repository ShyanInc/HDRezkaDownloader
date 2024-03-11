enable
conf ter
vlan 10
 name v10
vlan 20
 name v20
vlan 30
 name v30
 
 import os
import pathlib
import sys
import asyncio
import aiohttp
from tqdm import tqdm
from requests import Request

class MultiDownload:
    def __init__(self, data, dorl):
        self.data = data
        self.dorl = dorl
        self.filee = open("download_links.txt", "w")

    async def download(self, download_data):
        if download_data['stream_url']:
            print (download_data['file_name'])
            if self.dorl == "pls":
                self.filee.write(download_data['stream_url'] + "\n")

                if self.data['type'] == 'movie':
                    os.system(f"bomi {download_data['stream_url']}")
            else:
                fullpath = pathlib.Path.cwd() / download_data['file_name']

                async with aiohttp.ClientSession() as session:
                    async with session.get(download_data['stream_url']) as r:
                        total_size = int(r.headers.get('content-length', 0))
                        with open(fullpath, "wb") as f, tqdm(
                                unit="B",
                                unit_scale=True,
                                unit_divisor=1024,
                                total=total_size,
                                file=sys.stdout,
                                desc=download_data['file_name']
                        ) as progress:
                            while True:
                                chunk = await r.content.read(4096)
                                if not chunk:
                                    break
                                datasize = f.write(chunk)
                                progress.update(datasize)

    async def download_all(self):
        tasks = [self.download(download_data) for download_data in self.data['download_data']]
        await asyncio.gather(*tasks)

    def start(self):
        asyncio.run(self.download_all())

# Example usage
data = {
    'type': 'movie',
    'download_data': [
        {'file_name': 'file1.mp4', 'stream_url': 'https://example.com/file1.mp4'},
        {'file_name': 'file2.mp4', 'stream_url': 'https://example.com/file2.mp4'},
    ]
}

multi_download = MultiDownload(data, dorl="pls")
multi_download.start()