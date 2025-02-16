from aiogram.types import WebAppInfo
from aiogram import types

web_app = WebAppInfo(url='https://neforskiy.github.io/')

keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text='Сайт', web_app=web_app)]
    ],
    resize_keyboard=True
)