import os
import shutil
import telebot
from make_mp3 import get_mp3
import tokens_and_ids
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

print("bot started")

bot = telebot.TeleBot(tokens_and_ids.token)
channel_id = tokens_and_ids.channel_id

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Music", callback_data="cb_music"),
                     InlineKeyboardButton("No", callback_data="cb_no"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_music":
        bot.answer_callback_query(call.id, "Answer is Yes")
        answer = bot.send_message(call.message.chat.id, 'Send me link or title')
        bot.register_next_step_handler(answer, music_link_handler)
    elif call.data == "cb_no":
        bot.answer_callback_query(call.id, "Answer is No")


def music_link_handler(message):
    mp3_info = get_mp3(message.text)
    audio_file = open(mp3_info['mp3_path'], 'rb')
    thumbnail_file = open(mp3_info['thumbnail_file_path'], 'rb')

    if message.from_user.username:
        signature = f'by @{message.from_user.username}'
    elif message.from_user.last_name:
        signature = f'by {message.from_user.first_name} {message.from_user.last_name}'
    else:
        signature = f'by {message.from_user.first_name}'

    bot.send_audio(
        channel_id,
        audio_file,
        caption=f'[anything else](https://t.me/else_anything) | [ytm]({mp3_info["video_url"]}) | _{signature}_',
        parse_mode='Markdown',
        thumbnail=thumbnail_file,
        disable_notification=True
    )
    audio_file.close()
    thumbnail_file.close()

    shutil.rmtree(mp3_info['folder_path'])

@bot.message_handler(commands=['start'])
def message_handler(message):
    bot.send_message(message.chat.id, "?", reply_markup=gen_markup())


bot.infinity_polling()
