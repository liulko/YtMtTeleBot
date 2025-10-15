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
        'outtmpl': '[%(id)s].%(ext)s'

    }

    ydl = YoutubeDL(ydl_opts)
    # ydl = YoutubeDL()
    ydl.download(URL)

    video_info = ydl.sanitize_info(ydl.extract_info(URL, download=False))
    # print(video_info)

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
        'artist': video_info['artist'],
        'mp3_path': f"[{video_info['id']}].mp3",
        # 'video_file_name': output_path,
        'thumbnail_file_path': thumbnail_file_path,
        'thumbnail_default': thumbnail_default
    }
