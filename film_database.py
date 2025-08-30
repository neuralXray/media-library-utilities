# Films and music videos database

def read_film_library(video_root_directory, film_root_directory):
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
        #    print('\n-', category)

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

                #print(str(n) + ': ' + title + ' (' + year + '), by ' + director)

                d.append([fd, title, year, director, category])
                n = n + 1

    d.sort()

    data = DataFrame(data=d, columns=['Location', 'Title', 'Year', 'Director', 'Category'])
    data = data.set_index('Location')

    print('\n')
    print('################################################################################')
    print('##### SUMMARY ##################################################################')
    print('Total number of:')
    print('- Films:', len(data[data['Category'] == 'Films']))
    print('- Music videos:', len(data[data['Category'] == 'Music']))
    print('################################################################################')
    print('\n')

    return data


def read_film_database(database_root_directory):
    from pandas import read_csv

    data = read_csv(database_root_directory + 'films.csv')
    data = data.set_index('Location')

    return data


def update_film_database(database_root_directory, video_root_directory, film_root_directory):
    data = read_film_library(video_root_directory, film_root_directory)
    data_old = read_film_database(database_root_directory)

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
        if sum(data_new['Category'] == 'Films') > 0:
            print('  Films: ', len(data_new[data_new['Category'] == 'Films']))
        if sum(data_new['Category'] == 'Music') > 0:
            print('  Music videos: ', len(data_new[data_new['Category'] == 'Music']))
        for i in range(len(data_new)):
            print(str(i + 1) + ': ' + data_new.iloc[i]['Title'] + ' (' + data_new.iloc[i]['Year'] + '), by',
                  data_new.iloc[i]['Director'])
    print('################################################################################')

    data.to_csv(database_root_directory + 'films.csv')

