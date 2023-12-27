import os
import shutil
import telebot
from make_mp3 import get_mp3
import tokens_and_ids
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import ytmusicapi2
import telegraph_api

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
    info_message = bot.send_message(message.chat.id, f'😯 | work on {message.text}', disable_web_page_preview=True)
    mp3_info = get_mp3(message.text)
    audio_file = open(mp3_info['mp3_path'], 'rb')
    info_message = bot.edit_message_text(info_message.text + '\n✅ | audio downloaded', info_message.chat.id,
                                         info_message.id, disable_web_page_preview=True)
    thumbnail_file = open(mp3_info['thumbnail_file_path'], 'rb')
    if mp3_info['thumbnail_default']:
        info_message = bot.edit_message_text(info_message.text + '\n⚠️ | thumbnail default', info_message.chat.id,
                                             info_message.id, disable_web_page_preview=True)
    else:
        info_message = bot.edit_message_text(info_message.text + '\n✅ | thumbnail received', info_message.chat.id,
                                             info_message.id, disable_web_page_preview=True)
    signature = get_signature(message.from_user)
    info_message = bot.edit_message_text(info_message.text + '\n✅ | signature received', info_message.chat.id,
                                         info_message.id, disable_web_page_preview=True)

    lyrics = ytmusicapi2.get_lyrics(mp3_info['video_id'])
    if lyrics:
        info_message = bot.edit_message_text(info_message.text + '\n✅ | lyrics found', info_message.chat.id,
                                             info_message.id, disable_web_page_preview=True)
        telegraph_lyrics_page_link = telegraph_api.create_lyrics_page(lyrics,
                                                                      title=f"{mp3_info['artist']} - {mp3_info['title']}",
                                                                      author_name='anything else',
                                                                      author_url='https://t.me/else_anything')
        lyrics_for_quote = lyrics.strip().replace('<br><br>', '<br>')
        inner_blockquote = f"<em><a href='{telegraph_lyrics_page_link}'>{lyrics_for_quote.split('<br>')[0]}\n{lyrics_for_quote.split('<br>')[1]}...</a></em>"
        blockquote = f"<blockquote>{inner_blockquote}</blockquote>\n"
    else:
        info_message = bot.edit_message_text(info_message.text + '\n⚠️ | lyrics not found', info_message.chat.id,
                                             info_message.id, disable_web_page_preview=True)
        blockquote = ''

    caption = (f"{blockquote}"
               f"<a href='https://t.me/else_anything'>anything else</a> | "
               f"<a href='{mp3_info['video_url']}'>ytm</a> | "
               f"<em>{signature}</em>")
    audio_message = bot.send_audio(
        channel_id,
        audio_file,
        caption=caption,
        parse_mode='HTML',
        thumbnail=thumbnail_file,
        disable_notification=True
    )
    info_message = bot.edit_message_text(info_message.text + '\n✅ | audio successfully posted', info_message.chat.id,
                                         info_message.id, disable_web_page_preview=True)
    caption = (f"{blockquote}"
               f"<a href='https://t.me/else_anything/{audio_message.message_id}'>anything else</a> | "
               f"<a href='{mp3_info['video_url']}'>ytm</a> | "
               f"<em>{signature}</em>")
    bot.edit_message_caption(caption, audio_message.chat.id, audio_message.message_id, parse_mode='HTML')
    bot.send_message(message.chat.id, 'shos\' she?', reply_markup=gen_inline_markup(), disable_notification=True)
    thumbnail_file.close()
    audio_file.close()

    shutil.rmtree(mp3_info['folder_path'])


@bot.message_handler(commands=['start'])
def message_handler(message):
    bot.send_message(message.chat.id, 'sho?', reply_markup=gen_inline_markup())


bot.infinity_polling()
