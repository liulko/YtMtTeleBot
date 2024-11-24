import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error, TIT2, TPE1, WOAR, TSO2


def add_tags(path_mp3, artist, title, file_cover_name):

    tags = MP3(path_mp3, ID3=ID3).tags
    print(tags)


    tags.add(
        APIC(
            encoding=3,  # 3 is for utf-8
            mime="image/jpeg",  # can be image/jpeg or image/png
            type=3,  # 3 is for the cover image
            desc='cover',
            data=open(file_cover_name, mode='rb').read()
        )
    )
    print(f'adding tag TIT2 with text: {title}')
    tags.add(TIT2(encoding=3, text=title + '|Æ'))
    print(f'adding tag TPE1 with text: {artist}')
    tags.add(TPE1(encoding=3, text=artist))

    tags.save(path_mp3)