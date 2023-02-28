from typing import Never

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import ContextTypes

from bot_utils import update_main_message, set_main_message_id
from config import REMINDER_LEVEL, END, SELECTING_ACTION


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_name = update.effective_user.first_name
    text = (
        f"Привет <b>{user_name}</b>!"
        "\n----------------------------------------------------"
        "\nЯ, бот  удаленной поддержки"
        "\nВыберите раздел с которым хотите взаимодействовать"
        "\nдля прекращения работы бота в любой момент наберите  /stop."
        "\n----------------------------------------------------"
    )

    buttons = [
        [
            InlineKeyboardButton(text="⏰ Напоминания", callback_data=str(REMINDER_LEVEL)),
        ],
        [
            InlineKeyboardButton(text="Завершить", callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update_main_message(context, chat_id=update.effective_chat.id, text=text, reply_markup=keyboard)

    return SELECTING_ACTION


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update_main_message(context, chat_id=update.effective_chat.id, text="До новых встреч")
    set_main_message_id(context, None)
    return END


async def set_commands(bot) -> Never:
    commands = [BotCommand("/start", "Запуск бота")]
    await bot.set_my_commands(commands)
