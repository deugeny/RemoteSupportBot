from typing import Never

from telegram import InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import MAIN_MESSAGE


def try_get_main_message_id(context: ContextTypes.DEFAULT_TYPE) -> int | None:
    assert context is not None
    return context.user_data.get(MAIN_MESSAGE)


def set_main_message_id(context: ContextTypes.DEFAULT_TYPE, main_message_id: int | None) -> Never:
    assert context is not None
    assert main_message_id is None or isinstance(main_message_id, int)
    context.user_data[MAIN_MESSAGE] = main_message_id


async def update_main_message(context: ContextTypes.DEFAULT_TYPE,
                              chat_id: int,
                              text: str,
                              reply_markup: "InlineKeyboardMarkup" = None) -> Never:
    main_message_id = try_get_main_message_id(context)
    if main_message_id is not None:
        await context.bot.edit_message_text(chat_id=chat_id, message_id=main_message_id, text=text,
                                            reply_markup=reply_markup)
    else:
        message = await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
        main_message_id = message.id
        context.user_data[MAIN_MESSAGE] = main_message_id
