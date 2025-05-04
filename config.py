import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
TRAINER_CHAT_ID = int(os.getenv("TRAINER_CHAT_ID"))
CHAT_ID = int(os.getenv("CHAT_ID"))