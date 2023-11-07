import os
import shutil
import telebot
from make_mp3 import get_mp3
import tokens_and_ids

print("started")

bot = telebot.TeleBot(tokens_and_ids.token)
chat_id = tokens_and_ids.chat_id


@bot.channel_post_handler(content_types=['text'])
def channel(message):
    # memberobject = bot.get_chat_member(chat_id, message.from.user.id)
    # print(message)
    if message.chat.id == chat_id:
        mp3_info = get_mp3(message.text)
        audio_file = open(mp3_info['mp3_path'], 'rb')
        thumbnail_file = open(mp3_info['thumbnail_file_path'], 'rb')
        bot.delete_message(chat_id=chat_id, message_id=message.id)
        bot.send_audio(
            message.chat.id,
            audio_file,
            caption=f'[anything else](https://t.me/else_anything) | [ytm]({mp3_info["video_url"]}) | _{message.author_signature}_',
            parse_mode='Markdown',
            thumbnail=thumbnail_file,
            disable_notification=True
        )
        audio_file.close()
        thumbnail_file.close()

        shutil.rmtree(mp3_info['folder_path'])
    else:
        bot.send_message(message.chat.id, message.chat.id)


bot.infinity_polling()
