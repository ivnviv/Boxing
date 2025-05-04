# Функция для подключения к базе данных
import sqlite3

def get_connection():
    return sqlite3.connect("boxclub.db")

# Функция для регистрации пользователя в базе данных
def register_user(telegram_id, name):
    conn = get_connection()
    cursor = conn.cursor()


    # Проверяем, есть ли пользователь с таким telegram_id
    cursor.execute('SELECT id FROM users WHERE telegram_id = ?', (telegram_id,))
    user = cursor.fetchone()

    if not user:  # если пользователь не найден, добавляем его
        cursor.execute('''
            INSERT INTO users (name, telegram_id)
            VALUES (?, ?)
        ''', (name, telegram_id))
        conn.commit()
        conn.close()
        return False  # Вернем False, если нужно сообщить о регистрации
    else:
        conn.close()
        return True  # Вернем True, если пользователь уже есть
