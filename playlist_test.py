from os import mkdir

from yt_dlp import YoutubeDL
import json
import requests

def download_video(URL):
    ydl_opts = {
        'format': 'mp3/bestaudio/best',
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'outtmpl': 'tmp/%(id)s.%(ext)s',

    }

    ydl = YoutubeDL(ydl_opts)
    # ydl = YoutubeDL()
    video_info = ydl.sanitize_info(ydl.extract_info(URL, download=False))

    temp_folder_name = f'{video_info.get('id')}/'


    if video_info.get('_type') in ('playlist', 'multi_video'):
        entries_info = []
        for entry in video_info.get('entries'):
            ydl.download(entry.get('original_url'))

            print(entry.get('original_url'))
            if 'artist' in entry:
                artist_name = entry['artist']
            else:
                artist_name = entry['channel']

            # get thumbnail
            filtered_sorted_thumbs = sorted([i for i in video_info['thumbnails'] if i.get('width')],
                                            key=lambda w: (w['height']), reverse=True)

            thumbnail_file_path = 'images/default_thumbnail.jpg'
            thumbnail_default = True
            for i in filtered_sorted_thumbs:
                if i['width'] <= 320 and i['height'] <= 320:
                    thumbnail_default = False
                    thumbnail_response = requests.get(i['url'])
                    thumbnail_file_path = f"{video_info['id']}_cover.jpg"
                    file_mp3_cover = open(thumbnail_file_path, "wb")
                    file_mp3_cover.write(thumbnail_response.content)
                    file_mp3_cover.close()
                    break
            entries_info.append(
                {

                    'video_url': 'https://music.youtube.com/watch?v=' + video_info['id'],
                    'video_id': video_info['id'],
                    'title': video_info['title'] + ' | Æ',
                    'artist': artist_name,
                    'mp3_path': f"[{video_info['id']}].mp3",
                    # 'video_file_name': output_path,
                    'thumbnail_file_path': thumbnail_file_path,
                    'thumbnail_default': thumbnail_default
                }
            )



    if 'artist' in video_info:
        artist_name = video_info['artist']
    else:
        artist_name = video_info['channel']

    with open(f'{artist_name}_video_info', 'w+', encoding='utf-8') as f:
        f.write(str(video_info))
    # print(video_info)

    # ydl.download(URL)
    # get thumbnail
    filtered_sorted_thumbs = sorted([i for i in video_info['thumbnails'] if i.get('width')], key=lambda w: (w['height']), reverse=True)

    thumbnail_file_path = 'images/default_thumbnail.jpg'
    thumbnail_default = True
    for i in filtered_sorted_thumbs:
        if i['width'] <= 320 and i['height'] <= 320:
            thumbnail_default = False
            thumbnail_response = requests.get(i['url'])
            thumbnail_file_path = f"{video_info['id']}_cover.jpg"
            file_mp3_cover = open(thumbnail_file_path, "wb")
            file_mp3_cover.write(thumbnail_response.content)
            file_mp3_cover.close()
            break


    return {
        'video_url': 'https://music.youtube.com/watch?v=' + video_info['id'],
        'video_id': video_info['id'],
        'title': video_info['title'] + ' | Æ',
        'artist': artist_name,
        'mp3_path': f"[{video_info['id']}].mp3",
        # 'video_file_name': output_path,
        'thumbnail_file_path': thumbnail_file_path,
        'thumbnail_default': thumbnail_default
    }

p_url = 'https://music.youtube.com/playlist?list=OLAK5uy_lYg0AGH5U1_bEBB-vouULM_SMFulbbE9A&si=tieCk5jxXpUmY_Fq'
url_2 = 'https://music.youtube.com/playlist?list=PLpNh642peb1Fl-p0kwr0MlGbUIb9hD9Es&si=vR0cGkGabWtir7FL'
download_video(url_2)