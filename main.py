from aiogram import Bot, Dispatcher, executor, types
import dotenv
import os
import requests
import json

from services import _data_to_server
from tables import tables_init

tables_init()
dotenv.load_dotenv()

TOKEN = os.environ['TOKEN']
SERVER_HOST = os.environ['SERVER_HOST']

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
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

@dp.message_handler(commands=['buy'])
async def send_welcome(message: types.Message):
    await message.reply("Покупка")

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

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
