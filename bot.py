import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, \
    ContextTypes, Application
from handlers.menu import set_bot_commands
from reminders import reminder_job, handle_vote
from db import register_user, get_remaining_trainings, get_participants_for_today
from config import TOKEN, CHAT_ID
from datetime import time

user_states = {}

# Enable logging
logging.basicConfig(
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", level = logging.ERROR
)

# Команды
async def start(update, context):
    telegram_id = update.message.from_user.id
    user_states[telegram_id] = "awaiting_name"
    await update.message.reply_text("Привет! Введи, пожалуйста, своё имя для регистрации.")


async def handle_text(update, context):
    telegram_id = update.message.from_user.id
    text = update.message.text

    if user_states.get(telegram_id) == "awaiting_name":
        name = text
        already_registered = register_user(telegram_id, name)
        user_states.pop(telegram_id)

        if already_registered:
            await update.message.reply_text(f"{name}, ты уже зарегистрирован.")
        else:
            await update.message.reply_text(f"{name}, ты успешно зарегистрирован!")


async def trainings_command(update, context):
    telegram_id = update.message.from_user.id
    remaining = get_remaining_trainings(telegram_id)
    name = update.message.from_user.first_name

    if remaining is None:
        await update.message.reply_text(f"{name}, у тебя пока нет активного абонемента.")
    else:
        await update.message.reply_text(f"{name}, осталось {remaining} тренировок.")


# Кнопки из инлайн-меню
async def button_handler(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "join_training":
        await query.edit_message_text("🚀 Запись на тренировку скоро будет доступна!")
    elif query.data == "view_participants":
        await query.edit_message_text("📋 Список участников: (пока пусто)")
    elif query.data == "about_bot":
        await query.edit_message_text("🤖 Я бот для тренировок! Помогаю следить за участием и напоминать о занятиях.")

async def test_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await reminder_job(context)

async def participants_today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    participants = get_participants_for_today()
    if participants:
        names_text = "\n".join(f"• {name}" for name in participants)
        await update.message.reply_text(f"📋 Сегодня записались:\n{names_text}")
    else:
        await update.message.reply_text("Сегодня ещё никто не записался.")

# Запуск бота
def main():
    application = Application.builder().token(TOKEN).build()

    # Устанавливаем команды в меню Telegram
    async def post_init(app):
        await set_bot_commands(app.bot)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("trainings", trainings_command))
    application.add_handler(CallbackQueryHandler(handle_vote))  # Голосование
    application.add_handler(CallbackQueryHandler(button_handler))  # Обработка меню
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(CommandHandler("test_reminder", test_reminder))
    job_queue = application.job_queue
    # Задаем время для отправки напоминания в 12:00 в нужные дни недели (вт, чт, пт)
    reminder_time = time(hour=12, minute=0)
    application.add_handler(CommandHandler("participants_today", participants_today))
    application.post_init = post_init
    application.run_polling(allowed_updates=Update.ALL_TYPES)

# Устанавливаем ежедневное напоминание только в нужные дни
    job_queue.run_daily(reminder_job, reminder_time, days=(1, 3, 5), chat_id=CHAT_ID)  # 1: Вторник, 3: Четверг, 5: Пятница

if __name__ == "__main__":
    main()
