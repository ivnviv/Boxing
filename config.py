import os
from dotenv import load_dotenv

load_dotenv()

# Чтение переменной AMVERA
amvera_var = os.getenv("AMVERA")  # Лучше использовать get() на случай отсутствия переменной

# Проверка, что значение переменной "AMVERA" равно "1"
if amvera_var == "1":
    print("Работаю в облаке Амвера")
    TOKEN = os.environ["TOKEN"]
    CHAT_ID = int(os.environ["CHAT_ID"])
else:
    print("Работаю локально")
    TOKEN = os.getenv("TOKEN")
    CHAT_ID = int(os.getenv("CHAT_ID", "0"))  # Если переменная отсутствует, можно задать дефолтное значение
