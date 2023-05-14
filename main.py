from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
import dotenv
import os
import requests
import json

from services import _data_to_server

dotenv.load_dotenv()

DEBUG = os.environ.get('DEBUG', False)
TOKEN = os.environ['TOKEN']
SERVER_HOST = os.environ['SERVER_HOST']
PAYMENTS_TOKEN = os.environ['PAYMENTS_TOKEN']

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

if DEBUG:
    @dp.message_handler(commands=['test'])
    async def send_welcome(message: types.Message):
        response = requests.post(f'http://{SERVER_HOST}/api/payment/', data=_data_to_server(message, crypto=True)).text
        await message.reply("Привет!😊\nЯ самая умная нейросеть в мире🧐\nЗадавай мне любые вопросы!", reply_markup=markup)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    markup = types.ReplyKeyboardRemove()
    await message.reply("Привет!😊\nЯ самая умная нейросеть в мире🧐\nЗадавай мне любые вопросы!", reply_markup=markup)

@dp.message_handler(commands=['status'])
async def status(message: types.Message):
    response = requests.post(f'http://{SERVER_HOST}/api/status/', data=_data_to_server(message)).text
    response_to_dict = json.loads(response)
    username = response_to_dict['username']
    extra_messages = response_to_dict['extra_messages']
    day_limit_of_messages = response_to_dict['day_limit_of_messages']
    await message.answer(f'Привет {username}😊\nСуточный лимит сообщений: {day_limit_of_messages}\nПремиум сообщений:{extra_messages}')

# prices
PRICE = types.LabeledPrice(label="100 экстра сообщений", amount=500*100)  # в копейках (руб)

@dp.message_handler(commands=['buy'])
async def buy(message: types.Message):
    if PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, "Тестовый платеж!!!")


    await bot.send_invoice(message.chat.id,
                           title="💬100 экстра сообщений💬",
                           description="Экстра сообщения используются только после исчерпания дневного лимита",
                           provider_token=PAYMENTS_TOKEN,
                           currency="rub",
                           photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")

@dp.message_handler()
async def request_to_gpt(message: types.Message):
    status_response = requests.post(f'http://{SERVER_HOST}/api/status/', data=_data_to_server(message)).text
    response_to_dict = json.loads(status_response)
    extra_messages = response_to_dict['extra_messages']
    day_limit_of_messages = response_to_dict['day_limit_of_messages']
    wait_msg = await message.answer(f'Запрос отправлен, ожидайте ответа🤓\nЗапросов осталось: {day_limit_of_messages}\nЭктра запросов: {extra_messages}')
    json_response = requests.post(f'http://{SERVER_HOST}/api/request/', data=_data_to_server(message)).text
    dict_response = json.loads(json_response)
    await wait_msg.delete()
    await message.answer(dict_response['answer'])


# pre checkout  (must be answered in 10 seconds)
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# successful payment
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")
    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
