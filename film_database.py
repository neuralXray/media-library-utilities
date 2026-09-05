# Films and music videos database

def read_film_library(video_root_directory, film_root_directory,
                      log_file):
    from utils import logging
    from os import walk
    from os.path import isdir
    import re
    from pandas import DataFrame

    if isdir(video_root_directory[0] + film_root_directory):
        video_root_directory = video_root_directory[0]
    else:
        video_root_directory = video_root_directory[1]

    d = []
    n = 1
    for root, dirs, files in walk(video_root_directory + film_root_directory):
        category = root[len(video_root_directory + film_root_directory):]
        i = category.find('/')
        if i != -1:
            category = category[:i]
        #if category == 'Music':
        #    log = '\n- ' + category
        #    logging(log, log_file)

        files.sort()

        for file in files:
            if file[-4:] == '.srt':
                pass
            else:
                fd = root[len(video_root_directory):] + '/' + file

                i = re.search(' [0-9]{4} ', file).span()
                title = file[:i[0]]
                year = file[i[0] + 1:i[1] - 1]
                director = file[i[1]:]
                director = director[:director.rindex('.')]

                #log = str(n) + ': ' + title + ' (' + year + '), by ' + director
                #logging(log, log_file)

                d.append([fd, title, year, director, category])
                n = n + 1

    d.sort()

    data = DataFrame(data=d,
                     columns=['Location', 'Title', 'Year', 'Director', 'Category'])
    data = data.set_index('Location')

    log = '\n'
    logging(log, log_file)
    log = '######################################################################'
    logging(log, log_file)
    log = '##### SUMMARY ########################################################'
    logging(log, log_file)
    log = 'Total number of:'
    logging(log, log_file)
    log = f'- Films: {len(data[data["Category"] == "Films"])}'
    logging(log, log_file)
    log = f'- Music videos: {len(data[data["Category"] == "Music"])}'
    logging(log, log_file)
    log = '######################################################################'
    logging(log, log_file)
    log = '\n'
    logging(log, log_file)

    return data


def read_film_database(database_root_directory):
    from pandas import read_csv

    data = read_csv(database_root_directory + 'films.csv')
    data = data.set_index('Location')

    return data


def update_film_database(database_root_directory, video_root_directory,
                         film_root_directory,
                         log_file):
    from utils import logging
    data = read_film_library(video_root_directory, film_root_directory,
                             log_file)
    data_old = read_film_database(database_root_directory)

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
        if sum(data_new['Category'] == 'Films') > 0:
            log = f'  Films:  {len(data_new[data_new["Category"] == "Films"])}'
            logging(log, log_file)
        if sum(data_new['Category'] == 'Music') > 0:
            log = f'  Music videos: {len(data_new[data_new["Category"] == "Music"])}'
            logging(log, log_file)
        for i in range(len(data_new)):
            log = str(i + 1) + ': ' + data_new.iloc[i]['Title'] + \
                  ' (' + str(data_new.iloc[i]['Year']) + '), by ' + \
                  data_new.iloc[i]['Director']
            logging(log, log_file)
    log = '######################################################################'
    logging(log, log_file)

    data.to_csv(database_root_directory + 'films.csv')

