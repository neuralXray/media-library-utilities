# Series, Animated Sitcoms, Anime and Documentaries database

def read_series_library(video_root_directories, series_root_directory):
    from os import listdir
    from os.path import isfile
    from pandas import DataFrame

    video_root_directories = [video_root_directory + series_root_directory
                              for video_root_directory in video_root_directories]

    #print('Total number of chapters (from each season of each series):')
    #print()
    d = []
    for video_root_directory in video_root_directories:
        categories = listdir(video_root_directory)
        categories.sort()

        for category in categories:
            #print('-', category + '\n')
            series = listdir(video_root_directory + category)
            series.sort()

            for i, series in enumerate(series):
                #print('  ' + str(i + 1) + ': ' + series)
                seasons = listdir(video_root_directory + category + '/' + series)
                seasons.sort()

                location = category + '/' + series
                m = 0
                for season in seasons:
                    if isfile(video_root_directory + location + '/' + season):
                        m = m + 1
                    else:
                        location = category + '/' + series + '/' + season
                        season = season[len(series) + 1:]
                        n = len(listdir(video_root_directory + location))
                        #print(season + ': ' + str(n))
                        d.append([location, category, series, season, n])
                if m != 0:
                    #print('1: ' + str(m))
                    d.append([location, category, series, '1', m])

                #print()
            #print()
    #print()

    data = DataFrame(data=d, columns=['Location', 'Category', 'Series', 'Season', 'Number of Chapters'])
    data = data.set_index('Location')

    print('################################################################################')
    print('##### SUMMARY ##################################################################')
    print('Total number of:\n')

    print('- Series:', len(data.loc[data['Category'] == 'Series', 'Series'].unique()))
    print('seasons:', len(data.loc[data['Category'] == 'Series']))
    print('chapters:', sum(data.loc[data['Category'] == 'Series', 'Number of Chapters']))
    print()

    print('- Animated Sitcoms:', len(data.loc[data['Category'] == 'Animated Sitcoms', 'Series'].unique()))
    print('seasons:', len(data.loc[data['Category'] == 'Animated Sitcoms']))
    print('chapters:', sum(data.loc[data['Category'] == 'Animated Sitcoms', 'Number of Chapters']))
    print()

    print('- Anime:', len(data.loc[data['Category'] == 'Anime', 'Series'].unique()))
    print('chapters:', sum(data.loc[data['Category'] == 'Anime', 'Number of Chapters']))
    print()

    print('- Documentary series:', len(data.loc[data['Category'] == 'Documentaries', 'Series'].unique()))
    print('documentaries:', sum(data.loc[data['Category'] == 'Documentaries', 'Number of Chapters']))
    print('################################################################################')
    print('\n')

    return data


def read_series_database(database_root_directory):
    from pandas import read_csv

    data = read_csv(database_root_directory + 'series.csv')
    data = data.set_index('Location')

    return data


def update_series_database(database_root_directory, video_root_directories, series_root_directory):
    data = read_series_library(video_root_directories, series_root_directory)
    data_old = read_series_database(database_root_directory)

    data_deleted = data_old.loc[~ data_old.index.isin(data.index)]
    print('################################################################################')
    print('##### DELETED ##################################################################')
    if len(data_deleted) == 0:
        print('Nothing was deleted')
    else:
        for d in data_deleted.index:
            print(d)
    print('################################################################################')
    print('\n')

    data_new = data.loc[~ data.index.isin(data_old.index)]
    print('################################################################################')
    print('##### NEWLY ADDED ##############################################################')
    if len(data_new) == 0:
        print('Nothing was added')
    else:
        if sum(data_new['Category'] == 'Series') != 0:
            print('Series:')
            for i, n in enumerate(data_new.loc[data_new['Category'] == 'Series', 'Series'].unique()):
                print(i + 1, n)
            print()
        if sum(data_new['Category'] == 'Animated Sitcoms') != 0:
            print('Animated Sitcoms:')
            for i, n in enumerate(data_new.loc[data_new['Category'] == 'Animated Sitcoms', 'Series'].unique()):
                print(i + 1, n)
            print()
        if sum(data_new['Category'] == 'Anime') != 0:
            print('Anime:')
            for i, n in enumerate(data_new.loc[data_new['Category'] == 'Anime', 'Series'].unique()):
                print(i + 1, n)
            print()
        if sum(data_new['Category'] == 'Documentaries') != 0:
            print('Documentaries:')
            for i, n in enumerate(data_new.loc[data_new['Category'] == 'Documentaries', 'Series'].unique()):
                print(i + 1, n)
    print('################################################################################')

    data.to_csv(database_root_directory + 'series.csv')
