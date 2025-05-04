import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from db import add_participant
from config import CHAT_ID
from db import get_user_id_by_telegram_id

# Функция для отправки напоминания
async def reminder_job(context: CallbackContext):
    chat_id = CHAT_ID  # Используем константу CHAT_ID из config
    text = "Напоминаем о записи на тренировку! Хотите присоединиться?"

    keyboard = [
        [InlineKeyboardButton("Я приду", callback_data="join")],
        [InlineKeyboardButton("Не приду", callback_data="no_join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Асинхронный вызов send_message
    await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

# Функция для обработки голосования
async def handle_vote(update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    # Получаем telegram_id из callback_query
    telegram_id = query.from_user.id

    # Теперь ищем user_id в базе данных по telegram_id
    user_id = get_user_id_by_telegram_id(telegram_id)

    if not user_id:
        # Если user_id не найден в базе данных, можно вернуть ошибку или сообщение
        await query.edit_message_text(text="Пользователь не зарегистрирован в системе.")
        return

    if query.data == "join":
        response = "Вы записаны на тренировку."
        add_participant(user_id)  # Добавляем участника в посещение по user_id
    else:
        response = "Вы не записались на тренировку."

    await query.edit_message_text(text=response)

