from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
from telegram import ReplyKeyboardMarkup
import requests
import logging
import os


TOKEN = '5730316983:AAES63OC30h32FUpOABm7xUG28uSHLnmOOk'
URL = 'http://51.250.78.79/api/v1/devices/2/'


def temp_low():
    try:
        response = requests.get(URL).json()
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')

    temp_low_info = response.get('temp_low')
    return temp_low_info


def new_temp_low(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat.id, f'Минимальная температура: {temp_low()}')


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Привет, {format(name)}. Здесь будет информация о твоей розетке.'
             f'Введи номер своего девайса.',
    )


def info(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['/temp_low'], ['temp_high'], ['temp_curr'], ['on_off']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Какую информацию ты хотел бы получить?',
        reply_markup=button
    )


def main():
    updater = Updater(token=TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('info', info))
    updater.dispatcher.add_handler(CommandHandler('temp_low', new_temp_low))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
