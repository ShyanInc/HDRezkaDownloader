from HDRezkaAPI import *

search_text = input('Поиск: ')

movie_data = Search(search_text).get_data()
download_data = MovieInfo(movie_data).get_data()

Download(download_data).download_season(1)
