import requests
import creds
import telegraph
import ytmusicapi2

access_token = creds.get_creds()['telegraph_token']

telegraph = telegraph.Telegraph(access_token)

endpoint = 'https://api.telegra.ph/'


def get_account_info(token):
    response = requests.get(
        endpoint + 'getAccountInfo' + '?access_token=' + token + '&fields=["short_name", "author_name", "author_url", "auth_url", "page_count"]')
    return response.text


def create_lyrics_page(lyrics, title, author_name, author_url):
    page_url = telegraph.create_page(title=title,
                                     author_name=author_name,
                                     author_url=author_url,
                                     html_content=lyrics)['url']
    # print('created lyrics page on: ' + page_url)
    return page_url

# print(create_lyrics_page(lyrics=ytmusicapi2.get_lyrics('A4ud4WxXTEk'), author_name='Христина', title='Тримай'))