import sqlite3
import datetime

# подключение к БД
def get_connection():
    return sqlite3.connect("boxclub.db")

# создание таблиц
def init_db():
    conn = get_connection()
    c = conn.cursor()

    # Создание таблицы пользователей с новым полем telegram_id
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            telegram_id INTEGER UNIQUE
        )
    ''')

    # Создание таблицы абонементов
    c.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            purchased_at TEXT,
            total_trainings INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Создание таблицы посещений
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

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


def get_remaining_trainings(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT (s.total_trainings - COUNT(a.id)) as res
        FROM subscriptions s
        LEFT JOIN attendances a ON a.user_id = s.user_id AND date(a.date) >= date(s.purchased_at)
        WHERE s.user_id = (SELECT id FROM users WHERE telegram_id = ?)
        GROUP BY s.id
        ORDER BY s.purchased_at DESC
        LIMIT 1
    ''', (telegram_id,))

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    else:
        return None

# Функция для добавления участника в посещение
def add_participant(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO attendances (user_id, date) VALUES (?, ?)", (telegram_id, datetime.date.today()))
    conn.commit()
    conn.close()

def get_user_id_by_telegram_id(telegram_id):
    conn = sqlite3.connect("boxclub.db")
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM users WHERE telegram_id = ?', (telegram_id,))
    user = cursor.fetchone()

    conn.close()

    if user:
        return user[0]  # Возвращаем user_id
    return None  # Если пользователя нет в базе данных, возвращаем None

def get_participants_for_today():
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.date.today().isoformat()

    cursor.execute("""
        SELECT users.name FROM users
        JOIN attendances ON attendances.user_id = users.id
        WHERE attendances.date = ?
    """, (today,))

    names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return names