from telegram import __version__ as TG_VER, BotCommand

from PTBSQLAlchemyJobStoreV20 import PTBSQLAlchemyJobStoreV20

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(f"Данный бот не совместим с Вашей версией  PTB {TG_VER}.")

from config import (
    API_TOKEN,
    DEFAULT_TZ,
    DATABASE_CONNECTION_STRING,
    START_DIALOG,
    SELECTING_ACTION,
    STOPPING,
    END)
from error_handler import error_handler
import asyncio
from typing import Never
from telegram.constants import ParseMode
from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters, PicklePersistence, Defaults, )
from commands import start, stop, set_commands


def main() -> Never:
    defaults = Defaults(parse_mode=ParseMode.HTML, tzinfo=DEFAULT_TZ)
    application = (
        Application.builder()
        .concurrent_updates(False)
        .arbitrary_callback_data(True)
        .defaults(defaults)
        .token(API_TOKEN)
        .build())

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(set_commands(bot=application.bot))
    finally:
        pass

    job_store = PTBSQLAlchemyJobStoreV20(url=DATABASE_CONNECTION_STRING, application=application)
    application.job_queue.scheduler.add_jobstore(jobstore=job_store)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_DIALOG: [CallbackQueryHandler(start, pattern="^" + str(END) + "$")],
            SELECTING_ACTION:[

                CallbackQueryHandler(stop, pattern="^" + str(END) + "$")
            ],
            STOPPING: [CommandHandler("start", start)],
        },
        fallbacks=[
            CommandHandler("start", start),
            CommandHandler("stop", stop)],
    )

    application.add_error_handler(error_handler)
    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
