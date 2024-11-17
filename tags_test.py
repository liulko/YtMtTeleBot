

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error, TIT2, TPE1, WOAR, TSO2


def add_tags(path_mp3, artist, title, file_cover_name):
    audio = MP3(path_mp3)

    ID3.delall(audio.tags, 'APIC')

    audio.tags.add(
        APIC(
            encoding=3,  # 3 is for utf-8
            mime="image/jpeg",  # can be image/jpeg or image/png
            type=3,  # 3 is for the cover image
            desc='cover',
            data=open(file_cover_name, mode='rb').read()
        )
    )
    audio.tags.add(TIT2(encoding=3, text=title))
    audio.tags.add(TPE1(encoding=3, text=artist))

    audio.tags.save(path_mp3)


path = "2024_11_11__21_10_39_818/3 Doors Down-Kryptonite.mp3"
artist = "bawn"
title = "Gul"
thumbnail_file_path = "2024_11_11__21_10_39_818/BaWN - Topic-Гул_cover.jpg"
add_tags(path, artist, title, thumbnail_file_path)

