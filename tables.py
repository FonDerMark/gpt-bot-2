import sqlite3
import datetime

conn = sqlite3.connect('gpt.db')

def create_tables():
    tables = [
    '''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    username TEXT,
    firstname TEXT,
    lastname TEXT,
    message_limit INTEGER,
    day_of_limit DATETIME,
    extra_messages INTEGER
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    price INTEGER
    )
    ''',
    '''
    CREATE TABLE IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    product_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
    )
    '''
    ]
    # Необходимо внести все таблицы в список цикла
    with conn as cursor:
        for table in tables:
            cursor.execute(table)

def alter_tables():
    alters = [

    ]
    with conn as cursor:
        for alter in alters:
            cursor.execute(alter)

def tables_init():
    create_tables()
    alter_tables()

if __name__ == '__main__':
    tables_init()