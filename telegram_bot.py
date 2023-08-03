import os

from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, Updater

from db import get_ids, insert_into_db, look_for_me, update_username


load_dotenv()

CHAT_ID = int(os.getenv('OWNER_CHAT_ID'))


updater = Updater(token=os.getenv('TOKEN'))


def send_message(chat_id, context, message):
    return context.bot.send_message(chat_id=chat_id, text=message)


def start_view(update, context):
    chat = update.effective_chat
    message = ('Привет, я буду присылать тебе уведомления '
               'о твоих дедлайнах в Trello, но для этого мне '
               'нужен твой username оттуда. '
               'Отправь мне его через команду "/set_username username" '
               'без "@"')
    send_message(chat.id, context, message)


def set_username(update, context):
    chat = update.effective_chat
    text = update.message.text.split(' ')
    if len(text) == 1 or len(text) > 2:
        message = ('Введите по образцу "/set_username username"')
        return send_message(chat, context, message)
    insert_into_db(chat_id=chat.id, username=text[1].lower())
    message = ('Ваш username занесен в базу. Если он изменится '
               'или вы ввели его неправильно - отправьте его заново '
               'по образцу "/upd_username username"')
    return send_message(chat.id, context, message)


def look_in_db(update, context):
    chat = update.effective_chat
    data = look_for_me(chat.id)
    if len(data) == 0:
        message = 'Вас нет в базе данных'
        return send_message(chat.id, context, message)
    data_tuple = look_for_me(chat.id)[0]
    map_text = map(str, data_tuple)
    message = ' '.join(map_text)
    send_message(chat.id, context, message)


def reset_username(update, context):
    chat = update.effective_chat
    data = look_for_me(chat.id)
    if len(data) == 0:
        message = 'Вас нет в базе данных'
        return send_message(chat.id, context, message)
    text = update.message.text.split(' ')
    if len(text) == 1 or len(text) > 2:
        message = ('Введите по образцу:\n/upd_username username"')
        return send_message(chat.id, context, message)
    update_username(chat_id=chat.id, username=text[1].lower())
    message = 'Ваши данные изменены'
    send_message(chat.id, context, message)


def deadlines(update, context, filters=Filters.chat(CHAT_ID)):
    usernames, deadline, card_name = update.message.text.split('|')
    usernames = usernames.split(' ')
    usernames.pop(0)
    data = get_ids(usernames)
    text = f'{deadline} истекает срок {card_name}'
    for id in data:
        send_message(id, context, text)


def help(update, context):
    chat = update.effective_chat
    text = (
        'Мои команды: \n '
        '/set_username <username> - Добавить юзернейм Trello в базу данных\n'
        '/upd_username <username> - Обновить юзернейм Trello в базе данных('
        'если он там есть)\n '
        '/look_for_me - Узнать есть ли твой юезрнейм Trello в базе данных\n')
    send_message(chat.id, context, text)


updater.dispatcher.add_handler(CommandHandler('start', start_view))
updater.dispatcher.add_handler(CommandHandler('set_username', set_username))
updater.dispatcher.add_handler(CommandHandler('look_for_me', look_in_db))
updater.dispatcher.add_handler(CommandHandler('upd_username', reset_username))
updater.dispatcher.add_handler(CommandHandler('send_deadlines', deadlines))
updater.dispatcher.add_handler(CommandHandler('help', help))

updater.start_polling()
updater.idle()
