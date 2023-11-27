import os
import shutil
import telebot
from make_mp3 import get_mp3
import tokens_and_ids
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

print("bot started")

bot = telebot.TeleBot(tokens_and_ids.token)
channel_id = tokens_and_ids.channel_id


def gen_inline_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Music", callback_data="cb_music"),
               InlineKeyboardButton("No", callback_data="cb_no"))
    return markup


def gen_start_reply_markup():
    markup = ReplyKeyboardMarkup()
    markup.add(KeyboardButton('/start'))
    markup.resize_keyboard = True
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_music":
        bot.answer_callback_query(call.id, "Answer is Yes")
        answer = bot.send_message(call.message.chat.id, 'Send me link or title')
        bot.register_next_step_handler(answer, music_link_handler)
    elif call.data == "cb_no":
        bot.answer_callback_query(call.id, "Answer is No")


def get_signature(user):
    if type(user) is telebot.types.User:
        if user.username:
            signature = f'by @{user.username}'
        elif user.last_name:
            signature = f'by {user.first_name} {user.last_name}'
        else:
            signature = f'by {user.first_name}'
        return signature
    else:
        return 'signature'


def music_link_handler(message):
    mp3_info = get_mp3(message.text)
    audio_file = open(mp3_info['mp3_path'], 'rb')
    thumbnail_file = open(mp3_info['thumbnail_file_path'], 'rb')

    signature = get_signature(message.from_user)

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
    start_ans = bot.send_message(message.chat.id, "ok", reply_markup=gen_start_reply_markup())
    bot.send_message(start_ans.chat.id, 'sho?', reply_markup=gen_inline_markup())


bot.infinity_polling()
