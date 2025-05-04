from telegram import InlineKeyboardButton, InlineKeyboardMarkup, BotCommand, Update
from telegram.ext import ContextTypes

# # Инлайн-меню (в чате)
# async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [InlineKeyboardButton("💪 Записаться на тренировку", callback_data="join_training")],
#         [InlineKeyboardButton("📋 Посмотреть участников", callback_data="view_participants")],
#         [InlineKeyboardButton("ℹ️ О боте", callback_data="about_bot")],
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.message.reply_text("Выбери действие:", reply_markup=reply_markup)

# Меню Telegram (нижняя кнопка «Меню»)
async def set_bot_commands(bot):
    await bot.set_my_commands([
        BotCommand("start", "Зарегистрироваться в системе"),
        BotCommand("trainings", "Посмотреть оставшееся количество тренировок"),
        BotCommand("test_reminder", "Протестировать напоминание"),
        BotCommand("participants_today", "Кто придет на ближайшую тренировку"),
    ])
