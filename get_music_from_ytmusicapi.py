import random

import requests
from ytmusicapi import YTMusic
from urllib.parse import parse_qs
import logging

logger = logging.getLogger(__name__)
import pytube

ytmusic = YTMusic()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

html_text = requests.get('https://music.youtube.com/watch?v=588KWuXVAFA&si=_QnaPS5NQuKnunhi', headers=headers).text
# print(html_text)
player_js_url = pytube.extract.get_ytplayer_js(html_text)
player_js = requests.get('https://www.youtube.com' + player_js_url, headers=headers).text
cipher = pytube.cipher.Cipher(js=player_js)
fmt = ytmusic.get_song('588KWuXVAFA')['streamingData']['formats'][0]['signatureCipher']
fmtsigcipherq = parse_qs(fmt)
sig = cipher.get_signature(fmtsigcipherq['s'][0])
print(fmtsigcipherq['s'][0])
print(sig)
url = fmtsigcipherq['url'][0] + '&' + fmtsigcipherq['sp'][0] + '=' + sig
print(url)
response = requests.get(url, stream=True, headers=headers)
print(response.status_code)
with open(f'test_{random.randrange(0, 1000)}.mp4', "wb") as fout:
    for chunk in response.iter_content(chunk_size=1024*1024):
        fout.write(chunk)
    print('ok')
