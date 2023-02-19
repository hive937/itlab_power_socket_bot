import telegram
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    CommandHandler,
)
from telegram import (
    ReplyKeyboardMarkup,
    Update,
)
import requests
import logging
import os

from dotenv import load_dotenv

load_dotenv()

secret_token = os.getenv("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

URL = 'http://51.250.78.79/api/v1/devices/2/'  # надо править, тк заточено только под определенный айди сейчас
URL_2 = 'http://51.250.78.79/api/v1/jwt/create/'
AUTH = ''
CURR_INFO = ''

LOGIN, PASSWORD, INFO, TEMP, TEMP_LOW, TEMP_HIGH, ON_OFF, HEAT_COOL = range(8)

user_pass = {
    "username": LOGIN,
    "password": PASSWORD
}


async def wake_up(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.chat.first_name

    await update.message.reply_text(
        text=f'Привет, {format(name)}. Здесь будет информация о твоей розетке.'
             f'Введи свой логин.',
    )
    return LOGIN


async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    login_from_user = update.message.text
    global LOGIN
    LOGIN = login_from_user

    await update.message.reply_text(
        text=f'Введи свой пароль.',
    )
    print(login_from_user)
    return PASSWORD


async def password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    password_from_user = update.message.text
    global PASSWORD
    PASSWORD = password_from_user

    button = ReplyKeyboardMarkup([['/get_info']], resize_keyboard=True)

    await context.bot.send_message(
        chat_id=chat.id,
        text=f'Нажми на кнопку, чтобы получить имеющуюся конфигурацию',
        reply_markup=button
    )
    print(password_from_user)
    return INFO


async def get_token(one, two):
    try:
        response = requests.post(URL_2, data={
            "username": LOGIN,
            "password": PASSWORD
        })
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')

    auth = response.json().get('access')
    global AUTH
    AUTH = f'Bearer {auth}'
    print(auth)
    return INFO


async def get_info():
    await get_token(1, 2)
    try:
        response = requests.get(URL, headers={
            'Authorization': AUTH
        })
        info_api = response.json()
        print(info_api)
        global CURR_INFO
        CURR_INFO = response.json()
        return f'ID: {CURR_INFO.get("id")},\n' \
               f'Текст: {CURR_INFO.get("text")},\n' \
               f'Минимальная температура: {CURR_INFO.get("temp_low")},\n' \
               f'Максимальная температура: {CURR_INFO.get("temp_high")},\n' \
               f'Текущая температура: {CURR_INFO.get("temp_cur")},\n' \
               f'Включено или нет (0 или 1): {CURR_INFO.get("on_off")},\n' \
               f'Горячий или холодный (0 или 1): {CURR_INFO.get("heat_cool")},\n' \
               f'Последнее обновление: {CURR_INFO.get("lastupd")},\n' \
               f'Владелец: {CURR_INFO.get("owner")}'
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
    return INFO


async def send_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=await get_info(),
    )
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['/get_info'], ['/update_info']], resize_keyboard=True)
    await context.bot.send_message(
        chat_id=chat.id,
        text='Желаешь получить конфигурацию или обновить ее данные?',
        reply_markup=button
    )


async def update_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = ReplyKeyboardMarkup([['/temp_low'], ['/temp_high'], ['/on_off'], ['/heat_cool']], resize_keyboard=True)
    await update.message.reply_text(
        text="Какие данные ты желаешь обновить?",
        reply_markup=button
    )
    return TEMP


async def temp_low(update: Update, context: ContextTypes.DEFAULT_TYPE):
    temp_low_current = CURR_INFO.get('temp_low')
    await update.message.reply_text(
        text=f'Текущее значение: {temp_low_current}.\n'
             f'Введи новое значение.',
    )
    return TEMP_LOW


async def temp_low_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    temp_low_send_info = update.message.text
    try:
        response = requests.patch(URL, data={
            'temp_low': int(temp_low_send_info)
        },
        headers={
            'Authorization': AUTH
        })
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
    await update.message.reply_text(
        text=f'Текущее значение: {temp_low_send_info}.'
    )
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['/get_info'], ['/update_info']], resize_keyboard=True)
    await context.bot.send_message(
        chat_id=chat.id,
        text='Желаешь получить конфигурацию или обновить ее данные?',
        reply_markup=button
    )
    return INFO


async def temp_high(update: Update, context: ContextTypes.DEFAULT_TYPE):
    temp_low_current = CURR_INFO.get('temp_high')
    await update.message.reply_text(
        text=f'Текущее значение: {temp_low_current}.\n'
             f'Введи новое значение.',
    )
    return TEMP_HIGH


async def temp_high_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    temp_high_send_info = update.message.text
    try:
        response = requests.patch(URL, data={
            'temp_high': int(temp_high_send_info)
        },
        headers={
            'Authorization': AUTH
        })
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
    await update.message.reply_text(
        text=f'Текущее значение: {temp_high_send_info}.'
    )
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['/get_info'], ['/update_info']], resize_keyboard=True)
    await context.bot.send_message(
        chat_id=chat.id,
        text='Желаешь получить конфигурацию или обновить ее данные?',
        reply_markup=button
    )
    return INFO


async def on_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    on_off_current = CURR_INFO.get('on_off')
    await update.message.reply_text(
        text=f'Текущее значение: {on_off_current}.\n'
             f'Введи новое значение.',
    )
    return ON_OFF


async def on_off_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    on_off_send_info = update.message.text
    try:
        response = requests.patch(URL, data={
            'on_off': int(on_off_send_info)
        },
        headers={
            'Authorization': AUTH
        })
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
    await update.message.reply_text(
        text=f'Текущее значение: {on_off_send_info}.'
    )
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['/get_info'], ['/update_info']], resize_keyboard=True)
    await context.bot.send_message(
        chat_id=chat.id,
        text='Желаешь получить конфигурацию или обновить ее данные?',
        reply_markup=button
    )
    return INFO


async def heat_cool(update: Update, context: ContextTypes.DEFAULT_TYPE):
    heat_cool_current = CURR_INFO.get('heat_cool')
    await update.message.reply_text(
        text=f'Текущее значение: {heat_cool_current}.\n'
             f'Введи новое значение.',
    )
    return HEAT_COOL


async def heat_cool_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    heat_cool_send_info = update.message.text
    try:
        response = requests.patch(URL, data={
            'heat_cool': int(heat_cool_send_info)
        },
        headers={
            'Authorization': AUTH
        })
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
    await update.message.reply_text(
        text=f'Текущее значение: {heat_cool_send_info}.'
    )
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['/get_info'], ['/update_info']], resize_keyboard=True)
    await context.bot.send_message(
        chat_id=chat.id,
        text='Желаешь получить конфигурацию или обновить ее данные?',
        reply_markup=button
    )
    return INFO


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.",
    )

    return ConversationHandler.END


def main():
    application = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", wake_up)],
        states={
            LOGIN: [MessageHandler(filters.TEXT, login)],
            PASSWORD: [MessageHandler(filters.TEXT, password)],
            INFO: [CommandHandler("get_info", send_info),
                   CommandHandler("update_info", update_info), ],
            TEMP: [CommandHandler("temp_low", temp_low),
                   CommandHandler("temp_high", temp_high),
                   CommandHandler("on_off", on_off),
                   CommandHandler("heat_cool", heat_cool), ],
            TEMP_LOW: [MessageHandler(filters.TEXT, temp_low_send), ],
            TEMP_HIGH: [MessageHandler(filters.TEXT, temp_high_send), ],
            ON_OFF: [MessageHandler(filters.TEXT, on_off_send), ],
            HEAT_COOL: [MessageHandler(filters.TEXT, heat_cool_send), ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    application.run_webhook(
        listen='0.0.0.0',
        port=
    )


if __name__ == '__main__':
    main()
