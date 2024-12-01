import random
import pytubefix
import requests
import datetime
import os
import metadata_handler
import video_converter


def get_mp3(input_from_user):
    yt = pytubefix.YouTube(input_from_user, use_po_token=True)
    print(yt.title)

    video_url = 'https://music.youtube.com/watch?v=' + yt.vid_info['videoDetails']['videoId']
    video_id = yt.vid_info['videoDetails']['videoId']
    artist = yt.vid_info['videoDetails']['author'].replace('/', '-').replace(' - Topic', '')
    title = yt.vid_info['videoDetails']['title'].replace('/', '-')
    video_title = artist + ' - ' + title
    print(yt.vid_info['videoDetails'])
    print(yt.streams)

    # create temporary folder
    output_path = f'{datetime.datetime.now().strftime("%Y_%m_%d__%H_%M_%S")}_{random.randint(0, 1000)}/'
    try:
        os.mkdir(output_path)
    finally:
        pass

    video_filename = f"{output_path}{video_title}"

    # get thumbnail
    thumbnails = yt.vid_info['videoDetails']['thumbnail']['thumbnails']
    print(thumbnails)
    sorted_thumbnail = sorted(thumbnails, key=lambda d: d['width'], reverse=True)
    thumbnail_file_path = 'images/default_thumbnail.jpg'
    thumbnail_default = True
    for i in sorted_thumbnail:
        if i['width'] <= 320 and i['height'] <= 320:
            thumbnail_default = False
            thumbnail_response = requests.get(i['url'])
            thumbnail_file_path = f"{video_filename}_cover.jpg"
            file_mp3_cover = open(thumbnail_file_path, "wb")
            file_mp3_cover.write(thumbnail_response.content)
            file_mp3_cover.close()
            break

    # download mp4
    yt.streams.filter(mime_type='audio/mp4').order_by('abr').desc().first().download(
        output_path=output_path,
        filename=f'{video_title}.mp4')


    # convert mp4 to mp3
    # mp4_to_mp3(f'{file_audio_title}.mp4', f'{file_audio_title}.mp3')
    video_converter.mp4_to_mp3(video_filename)
    # add tags to mp3
    metadata_handler.add_tags(video_filename+'.mp3', artist, title, thumbnail_file_path)

    return {
        'video_url': video_url,
        'video_id': video_id,
        'title': title,
        'artist': artist,
        'mp3_path': f'{video_filename}.mp3',
        'folder_path': output_path,
        'thumbnail_file_path': thumbnail_file_path,
        'thumbnail_default': thumbnail_default
    }
