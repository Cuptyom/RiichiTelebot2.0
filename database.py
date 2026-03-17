# database.py - исправленная функция simple_execute

import sqlite3
import os

db_file = 'bot_database.db'  # имя файла базы данных

# функция для простых запросов не требующих возврата данных
def simple_execute(sql):
    """
    Выполняет SQL запрос без возврата данных
    """
    global db_file
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Ошибка в simple_execute: {e}")
        print(f"SQL запрос: {sql}")
        return False

# функция для запросов с возвратом данных
def fetch_one(sql):
    """
    Выполняет SQL запрос и возвращает одну запись
    """
    global db_file
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.close()
        return result
    except Exception as e:
        print(f"Ошибка в fetch_one: {e}")
        return None

# функция для запросов с возвратом всех данных
def fetch_all(sql):
    """
    Выполняет SQL запрос и возвращает все записи
    """
    global db_file
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.close()
        return result
    except Exception as e:
        print(f"Ошибка в fetch_all: {e}")
        return None

# остальной код check_and_create_db() без изменений...


#функция проверки и создания БД по необходимости
def check_and_create_db():
    global db_file
    """
    Проверяет наличие файла базы данных и создает его с необходимыми таблицами, если он отсутствует
    """
    
    # Проверяем существует ли файл базы данных
    if not os.path.exists(db_file):
        print("DB file has been created")
        
        # Создаем подключение к базе данных (файл создастся автоматически)
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Создаем таблицу chats
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                chat_id INTEGER UNIQUE NOT NULL,
                chat_only_mod INTEGER DEFAULT 0 NOT NULL,
                PRIMARY KEY (chat_id)
            )
        ''')
        
        # Создаем таблицу links
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                pantheon_id INTEGER NOT NULL,
                pantheon_name VARCHAR NOT NULL,
                pantheon_sorting VARCHAR DEFAULT 'rating' NOT NULL,
                pantheon_filter VARCHAR,
                FOREIGN KEY (chat_id) REFERENCES chats (chat_id)
            )
        ''')
        
        # Создаем таблицу weekly_poll
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weekly_poll (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                poll_type VARCHAR NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES chats (chat_id)
            )
        ''')
        
        # Создаем индексы для оптимизации запросов
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_links_chat_id ON links (chat_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_weekly_poll_chat_id ON weekly_poll (chat_id)')
        
        # Сохраняем изменения и закрываем соединение
        conn.commit()
        conn.close()
        
        print("База данных успешно создана!")
    else:
        print("DB is already exist!")
        
        # Даже если файл существует, проверяем структуру таблиц
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Проверяем наличие таблицы chats и создаем если нет
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                chat_id INTEGER UNIQUE NOT NULL,
                chat_only_mod INTEGER DEFAULT 0 NOT NULL,
                PRIMARY KEY (chat_id)
            )
        ''')
        
        # Проверяем наличие таблицы links и создаем если нет
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                pantheon_id INTEGER NOT NULL,
                pantheon_name VARCHAR NOT NULL,
                pantheon_sorting VARCHAR DEFAULT 'rating' NOT NULL,
                pantheon_filter VARCHAR,
                FOREIGN KEY (chat_id) REFERENCES chats (chat_id)
            )
        ''')
        
        # Проверяем наличие таблицы weekly_poll и создаем если нет
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weekly_poll (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                poll_type VARCHAR NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES chats (chat_id)
            )
        ''')
        
        # Проверяем наличие индексов
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_links_chat_id ON links (chat_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_weekly_poll_chat_id ON weekly_poll (chat_id)')
        
        conn.commit()
        conn.close()
        
    
    return 0