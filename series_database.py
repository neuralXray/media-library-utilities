# Series, Animated Sitcoms, Anime and Documentaries database

def read_series_library(video_root_directories, series_root_directory,
                        log_file):
    from utils import logging
    from os import listdir
    from os.path import isfile
    from pandas import DataFrame

    video_root_directories = [video_root_directory + series_root_directory
                              for video_root_directory in video_root_directories]

    #log = 'Total number of chapters (from each season of each series):'
    #logging(log, log_file)
    #log = ''
    #logging(log, log_file)
    d = []
    for video_root_directory in video_root_directories:
        categories = listdir(video_root_directory)
        categories.sort()

        for category in categories:
            #log = '- ' + category + '\n'
            #logging(log, log_file)
            series = listdir(video_root_directory + category)
            series.sort()

            for i, series in enumerate(series):
                #log = '  ' + str(i + 1) + ': ' + series
                #logging(log, log_file)
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
                        #log = season + ': ' + str(n)
                        #logging(log, log_file)
                        d.append([location, category, series, season, n])
                if m != 0:
                    #log = '1: ' + str(m)
                    #logging(log, log_file)
                    d.append([location, category, series, '1', m])

                #log = ''
                #logging(log, log_file)
            #log = ''
            #logging(log, log_file)
    #log = ''
    #logging(log, log_file)

    data = DataFrame(data=d, columns=['Location', 'Category', 'Series', 'Season',
                                      'Number of Chapters'])
    data = data.set_index('Location')

    log = '######################################################################'
    logging(log, log_file)
    log = '##### SUMMARY ########################################################'
    logging(log, log_file)
    log = 'Total number of:\n'
    logging(log, log_file)

    log = f'- Series: {len(data.loc[data["Category"] == "Series", "Series"].unique())}'
    logging(log, log_file)
    log = f'seasons: {len(data.loc[data["Category"] == "Series"])}'
    logging(log, log_file)
    log = f'chapters: {sum(data.loc[data["Category"] == "Series", "Number of Chapters"])}'
    logging(log, log_file)
    log = ''
    logging(log, log_file)

    log = '- Animated Sitcoms: ' + \
          str(len(data.loc[data['Category'] == 'Animated Sitcoms', 'Series'].unique()))
    logging(log, log_file)
    log = f'seasons: {len(data.loc[data["Category"] == "Animated Sitcoms"])}'
    logging(log, log_file)
    log = 'chapters: ' + \
          str(sum(data.loc[data['Category'] == 'Animated Sitcoms', 'Number of Chapters']))
    logging(log, log_file)
    log = ''
    logging(log, log_file)

    log = f'- Anime: {len(data.loc[data["Category"] == "Anime", "Series"].unique())}'
    logging(log, log_file)
    log = f'chapters: {sum(data.loc[data["Category"] == "Anime", "Number of Chapters"])}'
    logging(log, log_file)
    log = ''
    logging(log, log_file)

    log = '- Documentary series: ' + \
          str(len(data.loc[data['Category'] == 'Documentaries', 'Series'].unique()))
    logging(log, log_file)
    log = 'documentaries: ' + \
          str(sum(data.loc[data['Category'] == 'Documentaries', 'Number of Chapters']))
    logging(log, log_file)
    log = '######################################################################'
    logging(log, log_file)
    log = '\n'
    logging(log, log_file)

    return data


def read_series_database(database_root_directory):
    from pandas import read_csv

    data = read_csv(database_root_directory + 'series.csv')
    data = data.set_index('Location')

    return data


def update_series_database(database_root_directory, video_root_directories,
                           series_root_directory,
                           log_file):
    from utils import logging
    data = read_series_library(video_root_directories, series_root_directory,
                               log_file)
    data_old = read_series_database(database_root_directory)

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
        if sum(data_new['Category'] == 'Series') != 0:
            log = 'Series:'
            logging(log, log_file)
            for i, n in enumerate(data_new.loc[data_new['Category'] == 'Series',
                                               'Series'].unique()):
                log = f'{i + 1} {n}'
                logging(log, log_file)
            log = ''
            logging(log, log_file)
        if sum(data_new['Category'] == 'Animated Sitcoms') != 0:
            log = 'Animated Sitcoms:'
            logging(log, log_file)
            for i, n in enumerate(data_new.loc[data_new['Category'] == 'Animated Sitcoms',
                                               'Series'].unique()):
                log = f'{i + 1} {n}'
                logging(log, log_file)
            log = ''
            logging(log, log_file)
        if sum(data_new['Category'] == 'Anime') != 0:
            log = 'Anime:'
            logging(log, log_file)
            for i, n in enumerate(data_new.loc[data_new['Category'] == 'Anime',
                                               'Series'].unique()):
                log = f'{i + 1} {n}'
                logging(log, log_file)
            log = ''
            logging(log, log_file)
        if sum(data_new['Category'] == 'Documentaries') != 0:
            log = 'Documentaries:'
            logging(log, log_file)
            for i, n in enumerate(data_new.loc[data_new['Category'] == 'Documentaries',
                                               'Series'].unique()):
                log = f'{i + 1} {n}'
                logging(log, log_file)
    log = '######################################################################'
    logging(log, log_file)

    data.to_csv(database_root_directory + 'series.csv')

