import os
import shutil

import telebot
from make_mp3 import get_mp3


token = '1549377862:AAGoupqWih_2TpUut9GkbbGYxmVmemrn5FA'


print("started")

bot = telebot.TeleBot(token)
chat_id = -1002041935041


#   dsfg channel id             -1002041935041
#   anything else channel id    -1001555273110
@bot.channel_post_handler(content_types=['text'])
def channel(message):

    if message.chat.id == chat_id:
        mp3_info = get_mp3(message.text)
        audio_file = open(mp3_info['mp3_path'], "rb")
        bot.delete_message(chat_id=chat_id, message_id=message.id)
        bot.send_audio(message.chat.id, audio_file,
                       caption=f'[anything else](https://t.me/else_anything) | [ytm]({mp3_info["video_url"]}) | {message.author_signature}',
                       parse_mode='Markdown')
        audio_file.close()

        shutil.rmtree(mp3_info['folder_path'])
    else:
        bot.send_message(message.chat.id, message.chat.id)


bot.infinity_polling()
