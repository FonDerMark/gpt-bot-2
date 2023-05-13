import aiogram
from aiogram import Bot, Dispatcher, executor, types
import dotenv
import os
import requests
import json

from services import _data_to_server

dotenv.load_dotenv()

TOKEN = os.environ['TOKEN']
SERVER_HOST = os.environ['SERVER_HOST']

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")

@dp.message_handler(text=['Статус'])
async def status(message: types.Message):
    response = requests.post(f'http://{SERVER_HOST}/api/status/', data=_data_to_server(message)).text
    await message.answer(response)

@dp.message_handler()
async def request_to_gpt(message: types.Message):
    wait_msg = await message.answer('Запрос отправлен, ожидайте ответа🤓')
    json_response = requests.post(f'http://{SERVER_HOST}/api/request/', data=_data_to_server(message)).text
    dict_response = json.loads(json_response)
    await wait_msg.delete()
    await message.answer(dict_response['answer'])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
