# Update music, series (series, animated sitcom, anime, documentary) and film databases

def update_files_database(database_root_directory='/mnt/C62820CF2820C073/Security Copies/Files Database/',
                          root_directories=('/media/user/TOSHIBA EXT/', '/media/user/TOSHIBA EXT1/'),
                          music_root_directory='Music/',
                          favorites_playlist_root_directory='/home/user/.local/share/rhythmbox/',
                          playlist='playlists.xml',
                          start_playlist='name="Favorites"', end_playlist='  </playlist>\n',
                          start_favorite_songs='    <location>file:///home/user',
                          end_favorite_songs='</location>\n',
                          series_root_directory='Video/Series/', film_root_directory='Video/Films/'):
    from music_database import update_music_database
    from series_database import update_series_database
    from film_database import update_film_database

    print('################################################################################')
    print('########## MUSIC  ##############################################################')
    print('################################################################################')
    print()
    update_music_database(database_root_directory, root_directories, music_root_directory,
                          favorites_playlist_root_directory, playlist,
                          start_playlist, end_playlist, start_favorite_songs, end_favorite_songs)
    print('\n\n')
    print('################################################################################')
    print('########## SERIES (series, animated sitcoms, anime and documentaries) ##########')
    print('################################################################################')
    print()
    update_series_database(database_root_directory, root_directories, series_root_directory)
    print('\n\n')
    print('################################################################################')
    print('########## FILM (films and music videos) #######################################')
    print('################################################################################')
    print()
    update_film_database(database_root_directory, root_directories, film_root_directory)


update_files_database()
