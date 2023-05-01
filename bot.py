import os
import random

import telebot
from telebot import types

import db
import config as cfg

bot = telebot.TeleBot(cfg.BOT_ID)


def check_user(message):
    """Проверяет разрешено ли пользователю писать сообщения, если нет удаляет сообщение"""
    new_users = db.get_all_new_users()
    for new_user in new_users:
        if message.from_user.id == int(new_user[0]):
            if message.text == db.get_capcha_or_false(message.from_user.id)[0]:
                db.remove_new_user_from_table(message.from_user.id)
                bot.send_message(message.chat.id, "Теперь вы можете писать сообщения", reply_to_message_id=message.message_id)
            else:
                bot.delete_message(message.chat.id, message.id)
                return


@bot.message_handler(content_types=['audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact', 'left_chat_member', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message', 'web_app_data'])
def get_another_message(message):
    """Нужно для того чтобы бот удалял сообщения любого типа от пользователя не прошедшего проверку"""
    check_user(message)


@bot.message_handler(content_types=['new_chat_members'])
def check_new_user(message):
    """Проверяет проходил ли пользователь проверку, если нет то просит пройти"""
    user_data = db.get_all_users()
    for user in user_data:
        if message.from_user.id == int(user[0]):
            return

    a = random.randint(1, 5)
    b = random.randint(1, 5)
    try:
        db.insert_new_user(message.from_user.id, str(a+b))
    except:
        db.update_capcha(message.from_user.id, str(a+b))
    bot.send_message(message.chat.id, f"Небольшая проверка что вы живой человек, напишите цифрой сколько будет {a} + {b} чтобы получить возможность писать сообщения", reply_to_message_id=message.message_id)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """Обробатывает текстовые сообщения, если находит мат то просит не материться"""
    check_user(message)

    list_users = db.get_all_users()
    good_user = False
    for user in list_users:
        if message.from_user.id == int(user[0]):
            good_user = True
    if not good_user:
        db.insert(message.from_user.id)
    text = message.text.lower()
    text_detect = 0
    for word in cfg.WORDS:
        if word in text:
            text_detect = 1
    if text_detect == 1:
        ans = "Давайте не материться"
        bot.send_message(message.chat.id, ans, reply_to_message_id=message.message_id)

bot.polling(none_stop=True, interval=0)
