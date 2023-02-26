import os
from datetime import timedelta
from pytz import timezone
import logging

# идентификатор бота
API_TOKEN = os.getenv('REMINDER_BOT_API_TOKEN', default='5957265855:AAGjxqDh-XqfUVFfIY6WdtjIt2OWhdFwQuA')

# путь к базе данных
DATABASE_CONNECTION_STRING = os.getenv('REMINDER_BOT_CONNECTION_STRING', default='sqlite:///jobs.db')
DEFAULT_TZNAME: str = 'Europe/Moscow'
DEFAULT_TZ: timezone = timezone(DEFAULT_TZNAME)

DATE_SEARCH_SETTINGS = {'TIMEZONE': DEFAULT_TZNAME, 'RETURN_AS_TIMEZONE_AWARE': True, 'PREFER_DATES_FROM': 'future'}
DATE_SEARCH_LANGUAGES = ['ru', 'en']

MINIMUM_SCHEDULING_PERIOD = timedelta(seconds=10)
DEVELOPER_CHAT_ID = '5235429783:AAFT8GrhRazJalixcmwr2TNZOT-I0LZKICg'

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)