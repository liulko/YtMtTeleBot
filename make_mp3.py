import random

import pytube
import requests
import validators
import datetime
from moviepy.editor import *

import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error, TIT2, TPE1, WOAR, TSO2


def mp4_to_mp3(mp4, mp3):
    videoclip = AudioFileClip(mp4)
    videoclip.write_audiofile(mp3)
    videoclip.close()


def add_tags(path_mp3, artist, title, file_cover_name):
    audio = MP3(path_mp3, ID3=ID3)

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


def get_mp3(input_from_user):
    if validators.url(input_from_user):
        yt = pytube.YouTube(input_from_user)
    else:
        yt = pytube.Search(input_from_user).results[0]

    video_url = 'https://music.youtube.com/watch?v=' + yt.vid_info['videoDetails']['videoId']
    video_id = yt.vid_info['videoDetails']['videoId']
    artist = yt.vid_info['videoDetails']['author']
    title = yt.vid_info['videoDetails']['title']
    video_title = artist + '-' + title

    # create temporary folder
    folder_path = f'{datetime.datetime.now().strftime("%Y_%m_%d__%H_%M_%S")}_{random.randint(0, 1000)}/'
    try:
        os.mkdir(folder_path)
    finally:
        pass

    file_audio_title = f"{folder_path}{video_title.replace('/', '-')}"

    # get thumbnail
    thumbnails = yt.vid_info['videoDetails']['thumbnail']['thumbnails']
    # print(thumbnails)
    sorted_thumbnail = sorted(thumbnails, key=lambda d: d['width'], reverse=True)
    thumbnail_file_path = 'images/default_thumbnail.jpg'
    for i in sorted_thumbnail:
        if i['width'] <= 320 and i['height'] <= 320:
            thumbnail_response = requests.get(i['url'])
            file_mp3_cover = open(f"{file_audio_title}_cover.jpg", "wb")
            file_mp3_cover.write(thumbnail_response.content)
            file_mp3_cover.close()
            thumbnail_file_path = f"{file_audio_title}_cover.jpg"
            print('yeap')
            break

    # download mp4
    yt.streams.filter(type='audio', file_extension='mp4').order_by('abr').desc().first().download(
        filename=f'{file_audio_title}.mp4')

    # convert mp4 to mp3
    mp4_to_mp3(f'{file_audio_title}.mp4', f'{file_audio_title}.mp3')

    # add tags to mp3
    add_tags(f'{file_audio_title}.mp3', artist, title, thumbnail_file_path)

    return {
        'video_url': video_url,
        'video_id': video_id,
        'title': title,
        'artist': artist,
        'mp3_path': f'{file_audio_title}.mp3',
        'folder_path': folder_path,
        'thumbnail_file_path': thumbnail_file_path
    }
