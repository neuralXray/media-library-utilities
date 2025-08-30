from os.path import expanduser
from os import walk
from music_tag import load_file


# Asign artist to album artist tag
# Embed image file in folder to music files

music_root_directory = expanduser('~/Music/')


for root, dirs, files in walk(music_root_directory):
    if not files:
        continue
    for f in files:
        if f[f.rindex('.') + 1:] in ['png', 'jpg', 'jpeg', 'webp']:
            print(f[:f.rindex('.')])
            img_in = open(root + '/' + f, 'rb')
            artwork = img_in.read()
            img_in.close()
            for f in files:
                if f[f.rindex('.') + 1:] not in ['png', 'jpg', 'jpeg', 'webp', 'lrc', 'txt', 'tmp']:
                    md = root[len(music_root_directory):] + '/' + f
                    m = load_file(music_root_directory + md)
                    m['artwork'] = artwork
                    m['album artist'] = m['artist'].value
                    m.save()
            break

