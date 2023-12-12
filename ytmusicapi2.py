from ytmusicapi import YTMusic


def get_lyrics(video_id):
    ytmusic = YTMusic()
    lyrics_id = ytmusic.get_watch_playlist(video_id)['lyrics']
    if lyrics_id:
        lyrics_dict = ytmusic.get_lyrics(lyrics_id)
        lyrics_text = lyrics_dict['lyrics']
        lyrics_text_html = lyrics_dict['lyrics'].replace('\n', '<br>')
        with open(f'../www/{video_id}.html', 'w') as f:
            f.write(lyrics_text_html)

        return lyrics_text
    else:
        return None
