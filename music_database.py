# Music database

# esta función es la misma que load_pc_playlist()
# en sync-music-playlists/sync_music_playlists.py
def read_favorites_playlist(favorites_playlist_root_directory, playlist,
                            start_playlist, end_playlist,
                            music_root_directory,
                            start_favorite_songs, end_favorite_songs):
    from urllib.parse import unquote

    file = open(favorites_playlist_root_directory + playlist)
    favorites_playlist = file.readlines()
    file.close()

    s = 0
    for line in favorites_playlist:
        if start_playlist in line:
            break
        s = s + 1

    e = s
    for line in favorites_playlist[s:]:
        if line == end_playlist:
            break
        e = e + 1

    favorites_playlist = favorites_playlist[s + 1:e]

    start = start_favorite_songs + music_root_directory
    end = end_favorite_songs

    for i, l in enumerate(favorites_playlist):
        favorites_playlist[i] = \
        unquote(l[l.find(start) + len(start) + 2:l.find(end)]).replace('&amp;', '&')

    favorites_playlist.sort()

    return favorites_playlist


def read_music_library(root_directories, music_root_directory,
                       favorites_playlist_root_directory, playlist,
                       start_playlist, end_playlist,
                       start_favorite_songs, end_favorite_songs,
                       log_file):
    from utils import logging
    from os import walk
    from os.path import isdir
    from music_tag import load_file
    from pandas import DataFrame
    from numpy import array, unique, argsort

    # Load favorite songs relative location (directory)
    favorites = read_favorites_playlist(favorites_playlist_root_directory, playlist,
                                        start_playlist, end_playlist,
                                        music_root_directory,
                                        start_favorite_songs, end_favorite_songs)

    if isdir(root_directories[0] + music_root_directory):
        music_root_directory = root_directories[0] + music_root_directory
    else:
        music_root_directory = root_directories[1] + music_root_directory

    # Load relative location (directory),
    #      artist, year, album, track number, title and genre from all music files in mrd
    d = []
    for root, dirs, files in walk(top=music_root_directory):
        if not files:
            continue

        for f in files:
            if f[f.rindex('.') + 1:] not in ['png', 'jpg', 'jpeg', 'webp', 'lrc', 'txt']:
                md = root[len(music_root_directory):] + '/' + f
                m = load_file(music_root_directory + md)
                d.append((md, m['artist'].value, m['year'].value, m['album'].value,
                          m['tracknumber'].value, m['title'].value, m['genre'].value))

    d.sort()

    data = DataFrame(data=d, columns=['Location', 'Artist', 'Year', 'Album',
                                      'Track number', 'Title', 'Genre'])
    data = data.set_index('Location')
    data['Favorite'] = False
    data.loc[favorites, 'Favorite'] = True

    log = '######################################################################'
    logging(log, log_file)
    log = '##### SUMMARY ########################################################'
    logging(log, log_file)
    log = f'- Total number of songs: {len(data)}'
    logging(log, log_file)
    log = f'- Total number of favorite songs: {sum(data["Favorite"])}'
    logging(log, log_file)
    log = ''
    logging(log, log_file)

    artists = unique(array(data.loc[data['Favorite'], 'Artist']), return_counts=True)
    featured_artists = [artists[0][artists[1] > 10], artists[1][artists[1] > 10]]
    i = argsort(featured_artists[1])[::-1]
    log = '- Number of favourite songs of featured artists:'
    logging(log, log_file)
    for n, artist in zip(featured_artists[1][i], featured_artists[0][i]):
        log = str(n) + ': ' + artist
        logging(log, log_file)
    log = '######################################################################'
    logging(log, log_file)
    log = '\n'
    logging(log, log_file)

    return data


def read_music_database(database_root_directory):
    from pandas import read_csv

    data = read_csv(database_root_directory + 'music.csv')
    data = data.set_index('Location')

    return data


def update_music_database(database_root_directory, root_directories, music_root_directory,
                          favorites_playlist_root_directory, playlist,
                          start_playlist, end_playlist,
                          start_favorite_songs, end_favorite_songs,
                          log_file):
    from utils import logging
    data = read_music_library(root_directories, music_root_directory,
                              favorites_playlist_root_directory, playlist,
                              start_playlist, end_playlist,
                              start_favorite_songs, end_favorite_songs,
                              log_file)
    data_old = read_music_database(database_root_directory)

    data_deleted = data_old.loc[~ data_old.index.isin(data.index)]
    log = '######################################################################'
    logging(log, log_file)
    log = '##### DELETED ########################################################'
    logging(log, log_file)
    if len(data_deleted) == 0:
        log = 'Nothing was deleted'
        logging(log, log_file)
    else:
        for d in data_deleted.index:
            log = d
            logging(log, log_file)
    log = '######################################################################'
    logging(log, log_file)
    log = '\n'
    logging(log, log_file)

    data_new = data.loc[~ data.index.isin(data_old.index)]
    log = '######################################################################'
    logging(log, log_file)
    log = '##### NEWLY ADDED ####################################################'
    logging(log, log_file)
    if len(data_new) == 0:
        log = 'Nothing was added'
        logging(log, log_file)
    else:
        log = '- Artists:'
        logging(log, log_file)
        for i, artist in enumerate(data_new['Artist'].unique()):
            log = str(i + 1) + ': ' + artist
            logging(log, log_file)
        log = ''
        logging(log, log_file)
        log = f'- {len(data_new["Album"].unique())} albums'
        logging(log, log_file)
        log = f'- {len(data_new)}, songs'
        logging(log, log_file)
    log = '######################################################################'
    logging(log, log_file)

    data.to_csv(database_root_directory + 'music.csv')

