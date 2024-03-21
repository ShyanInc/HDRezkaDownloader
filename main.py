from HDRezkaAPI import *

if History().status == 'run' and input('Continue[yN]?') != "n":
    movie_data = History().movie_data
else:
    History().status = "end"

    search_text = input('Поиск: ')
    search_result = Search(search_text)

    print(search_result)

    title_id = int(input('Введите номер: '))

    movie_data = search_result.get_data(title_id)

History().movie_data = movie_data

movie_info = MovieInfo(movie_data)

download_data = movie_info.get_data()
print (f'\n{download_data}\n')

if 0:
    quality = input("Введите качество: ")
else:
    quality = "1080"

downloader = Download(download_data, quality)

print(movie_info)

if download_data['type'] == 'movie':
    downloader.download_movie()
    print('Скачивание успешно завершено!')
else:     

    if History().status == 'run':
        download_type = History().download_type
    else:
        download_type = int(input('1 - Скачать сезон сериала\n2 - Скачать эпизоды сериала\n3 - Скачать сезонs сериала\n4 - Скачать сериал\n'
                            'Выберите тип скачивания: '))
    History().download_type = download_type

    if download_type == 1:
        if History().status == 'run' and History().download_type == 1 and History().run_season !="":
            season = History().run_season
        else:
            season = int(input('Введите номер сезона: '))   
        downloader.download_season(season)
        print('Скачивание успешно завершено!')
    elif download_type == 2:
        correct_episode = False
        season = int(input('Введите номер сезона: '))
        episodes_count = download_data['seasons_episodes_count'][season]
        print(f'В данном сезоне количество эпизодов: {episodes_count}')
        start = int(input('Введите стартовый эпизод: '))
        end = episodes_count
        while not correct_episode:
            try:
                downloader.download_episodes(season, start)
                correct_episode = True
            except EpisodeNumberIsOutOfRange:
                print('Неверный диапазон!')
                episode = int(input('Снова введите диапазон эпизодов: '))
        print('Скачивание успешно завершено!')
    elif download_type == 3:
        correct_season = False
        start = int(input('Enter the starting season number: '))
        end = int(input('Enter the ending season number: '))
        while not correct_season:
            try:
                downloader.download_seasons(start, end)
                correct_season = True
            except SeasonNumberIsOutOfRange:
                print('Invalid season range!')
                start = int(input('Enter the starting season number again: '))
                end = int(input('Enter the ending season number again: '))
        print('Download successful!')
    elif download_type == 4:
        downloader.download_all_serial()
        print('Скачивание успешно завершено!')
    else:
        print('Неверный тип скачивания!')

    History().status = "end"
