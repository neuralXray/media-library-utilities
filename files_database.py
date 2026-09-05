# Update music, series (series, animated sitcom, anime, documentary) and film databases

def update_files_database(database_root_directory='/mnt/C62820CF2820C073/Security Copies/Files Database/',
                          root_directories=('/media/user/TOSHIBA EXT/',
                                            '/media/user/TOSHIBA EXT1/'),
                          music_root_directory='Music/',
                          favorites_playlist_root_directory='/home/user/.local/share/rhythmbox/',
                          playlist='playlists.xml', start_playlist='name="Favorites"',
                          end_playlist='  </playlist>\n',
                          start_favorite_songs='    <location>file:///home/user',
                          end_favorite_songs='</location>\n',
                          series_root_directory='Video/Series/',
                          film_root_directory='Video/Films/'):
    from music_database import update_music_database
    from series_database import update_series_database
    from film_database import update_film_database
    from utils import logging
    from os.path import exists
    from os import mkdir
    from datetime import datetime

    log_dir = 'logs'
    if not exists(log_dir):
        mkdir(log_dir)
    datetime_now = datetime.now()
    date_time = datetime_now.strftime('%Y %b %d %H:%M:%S')
    log_file = f'{log_dir}/{date_time}.log'
    file = open(log_file, 'w')
    file.close()

    log = '######################################################################'
    logging(log, log_file)
    log = '########## MUSIC  ####################################################'
    logging(log, log_file)
    log = '######################################################################'
    logging(log, log_file)
    log = ''
    logging(log, log_file)
    update_music_database(database_root_directory, root_directories, music_root_directory,
                          favorites_playlist_root_directory, playlist,
                          start_playlist, end_playlist,
                          start_favorite_songs, end_favorite_songs,
                          log_file)
    log = '\n\n'
    logging(log, log_file)
    log = '######################################################################'
    logging(log, log_file)
    log = '########## SERIES (series, animated sitcoms, anime and documentaries) '
    logging(log, log_file)
    log = '######################################################################'
    logging(log, log_file)
    log = ''
    logging(log, log_file)
    update_series_database(database_root_directory, root_directories,
                           series_root_directory,
                           log_file)
    log = '\n\n'
    logging(log, log_file)
    log = '######################################################################'
    logging(log, log_file)
    log = '########## FILM (films and music videos) #############################'
    logging(log, log_file)
    log = '######################################################################'
    logging(log, log_file)
    log = ''
    logging(log, log_file)
    update_film_database(database_root_directory, root_directories, film_root_directory,
                         log_file)


update_files_database()

