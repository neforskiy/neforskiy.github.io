from aiogram import Bot, Dispatcher
import asyncio
from dotenv import load_dotenv 
import os
from aiogram import types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, LabeledPrice, ReplyKeyboardMarkup, KeyboardButton

load_dotenv(".env")
BOT_TOKEN = os.getenv('BOT_TOKEN')
PAY_TOKEN = os.getenv('PAY_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

web_app = WebAppInfo(url='https://neforskiy.github.io/site/')

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Сайт', web_app=web_app)]
    ],
    resize_keyboard=True
)

PRICE = {
    '1': [LabeledPrice(label='Item1', amount=10000)],  # 1 рубль = 100 копеек
    '2': [LabeledPrice(label='Item2', amount=20000)],  # 2 рубля = 200 копеек
    '3': [LabeledPrice(label='Item3', amount=30000)],  # 3 рубля = 300 копеек
    '4': [LabeledPrice(label='Item4', amount=40000)],  # 4 рубля = 400 копеек
    '5': [LabeledPrice(label='Item5', amount=50000)],  # 5 рублей = 500 копеек
    '6': [LabeledPrice(label='Item6', amount=60000)],  # 6 рублей = 600 копеек
}



@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer('Тестируем WebApp!', reply_markup=keyboard)

@dp.message(lambda message: message.web_app_data)
async def buy_process(web_app_message):
    await web_app_message.answer_invoice(
        title='Laptop',
        description='Description',
        provider_token=PAY_TOKEN,
        currency='RUB',
        need_email=True,
        prices=PRICE[f'{web_app_message.web_app_data.data}'],
        start_parameter='example',
        payload='some_invoice'
    )

@dp.pre_checkout_query
async def pre_checkout_process(pre_checkout: types.PreCheckoutQuery):
    await pre_checkout.answer(ok=True)

@dp.message(lambda message: message.content_type == types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    await message.answer('Платеж прошел успешно!')

async def main():
    import logging
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
