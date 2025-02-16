from keyboards import keyboard
from aiogram import types
from aiogram.filters import Command
from dotenv import load_dotenv
import os
from aiogram import F

load_dotenv(".env")
PAY_TOKEN = os.getenv('PAY_TOKEN')

def setup_handlers(dp):
    @dp.message(Command('start'))
    async def start(message: types.Message):
        await message.answer('Тестируем WebApp!',
                           reply_markup=keyboard)

    PRICE = {
        '1': [types.LabeledPrice(label='Item1', amount=1)],
        '2': [types.LabeledPrice(label='Item2', amount=2)],
        '3': [types.LabeledPrice(label='Item3', amount=3)],
        '4': [types.LabeledPrice(label='Item4', amount=4)],
        '5': [types.LabeledPrice(label='Item5', amount=5)],
        '6': [types.LabeledPrice(label='Item6', amount=6)]
    }

    @dp.message(F.web_app_data)
    async def buy_process(web_app_message):
        await web_app_message.answer_invoice(
            title='Laptop',
            description='Description',
            provider_token=PAY_TOKEN,
            currency='rub',
            need_email=True,
            prices=PRICE[f'{web_app_message.web_app_data.data}'],
            start_parameter='example',
            payload='some_invoice')

    @dp.pre_checkout_query
    async def pre_checkout_process(pre_checkout: types.PreCheckoutQuery):
        await pre_checkout.answer(ok=True)

    @dp.message(lambda message: message.content_type == types.ContentType.SUCCESSFUL_PAYMENT)
    async def successful_payment(message: types.Message):
        await message.answer('Платеж прошел успешно!')
