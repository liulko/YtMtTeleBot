import pytube
import requests
import validators
import datetime
from moviepy.editor import *

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error, TIT2, TPE1, WOAR, TSO2


def mp4_to_mp3(mp4, mp3):
    videoclip = AudioFileClip(mp4)
    videoclip.write_audiofile(mp3)
    videoclip.close()


def add_tags(path_mp3, artist, title, file_cover_name):
    audio = MP3(path_mp3, ID3=ID3)
    audio.tags.add(
        APIC(
            encoding=3,  # 3 is for utf-8
            mime="image/jpeg",  # can be image/jpeg or image/png
            type=3,  # 3 is for the cover image
            desc='Cover',
            data=open(file_cover_name, mode='rb').read()
        )
    )
    audio.tags.add(TIT2(encoding=3, text=title))
    audio.tags.add(TPE1(encoding=3, text=artist))

    audio.tags.save(path_mp3)


def get_mp3(input_from_user):
    if validators.url(input_from_user):
        yt = pytube.YouTube(input_from_user)
    else:
        yt = pytube.Search(input_from_user).results[0]

    video_url = 'https://music.youtube.com/watch?v=' + yt.vid_info['videoDetails']['videoId']
    artist = yt.vid_info['videoDetails']['author']
    title = yt.vid_info['videoDetails']['title']
    video_title = artist + '-' + title

    # create temporary folder
    folder_path = f'{datetime.datetime.now().strftime("%Y_%m_%d__%H_%M_%S")}/'
    print(folder_path)
    try:
        os.mkdir(folder_path)
    finally:
        pass

    # get cover
    thumbnail = yt.vid_info['videoDetails']['thumbnail']['thumbnails']
    sorted_thumbnail = sorted(thumbnail, key=lambda d: d['width'], reverse=True)
    mp3_cover_url = sorted_thumbnail[0]['url']
    response = requests.get(mp3_cover_url)
    file_mp3_cover = open(f"{folder_path}{video_title}_cover.jpg", "wb")
    file_mp3_cover.write(response.content)
    file_mp3_cover.close()

    # download mp4
    yt.streams.filter(type='audio', file_extension='mp4').order_by('abr').desc().first().download(
        filename=f'{folder_path}{video_title}.mp4')

    # convert mp4 to mp3
    mp4_to_mp3(f'{folder_path}{video_title}.mp4', f'{folder_path}{video_title}.mp3')

    # add tags to mp3
    add_tags(f'{folder_path}{video_title}.mp3', artist, title, f"{folder_path}{video_title}_cover.jpg")

    return {
        'video_url': video_url,
        'title': title,
        'artist': artist,
        'mp3_path': f'{folder_path}{video_title}.mp3',
        'folder_path': folder_path
    }
