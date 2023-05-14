import sqlite3
from aiogram import types

conn = sqlite3.connect('gpt.db')

def message_parser(msg: types.Message) -> dict:
    return {
        'user_id': msg.from_user.id,
        'username': msg.from_user.username,
        'first_name': msg.from_user.first_name,
        'last_name': msg.from_user.last_name,
        'text': msg.text
    }
    

def get_or_greate_user(msg: types.Message):
    with conn as cursor:
        user = message_parser(msg=msg)
        with conn as cursor:
            cursor.execute(f'INSERT INTO users (user_id, username, first_name, last_name) \
                           VALUES ({user.user_id}, {user.username}, {user.first_name}, {user.last_name})')


    