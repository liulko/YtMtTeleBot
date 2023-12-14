from ytmusicapi import YTMusic


def get_lyrics(video_id):
    ytmusic = YTMusic()
    lyrics_id = ytmusic.get_watch_playlist(video_id)['lyrics']
    if lyrics_id:
        lyrics_dict = ytmusic.get_lyrics(lyrics_id)
        lyrics_text = lyrics_dict['lyrics']
        lyrics_html = lyrics_text.replace('\n', '<br>').replace('\r', '')

        return lyrics_html
    else:
        return None
