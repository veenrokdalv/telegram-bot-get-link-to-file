import datetime as dt
from pathlib import Path

from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
from environs import Env

START_TIME = dt.datetime.utcnow()

BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'
TMP_DIR = BASE_DIR / 'tmp'
LOGS_DIR = BASE_DIR / 'logs'

# Settings i18n.
I18N_DOMAIN = 'messages'

env = Env()
env.read_env(f'{BASE_DIR}/.env')

APP_NAME = env('APP_NAME')


# Settings bot.
TELEGRAM_BOT_API_TOKENS = [bot_token for bot_token in env('TELEGRAM_BOT_API_TOKENS').split()]
DEFAULT_LOCALE = env('DEFAULT_LOCALE')
DEFAULT_TIMEZONE = env('DEFAULT_TIMEZONE')
SUPERUSERS_TELEGRAM_ID = [int(_id) for _id in env('SUPERUSERS_TELEGRAM_ID').split() if _id.isdigit()]
USE_SKIP_UPDATES = env.bool('USE_SKIP_UPDATES')
BOT_COMMANDS = [
    {
        'commands': [
            BotCommand(command='help', description='Help menu.'),
            BotCommand(command='settings', description='Menu profile settings.'),
            BotCommand(command='start', description='Bot reload.')
        ],
        'scope': BotCommandScopeAllPrivateChats(),
        'locale': 'en'
    },
]

# Settings database connection.
USE_CLEAR_TABLES = env.bool('USE_CLEAR_TABLES')
DATABASE_HOST = env('DATABASE_HOST', '127.0.0.1')
DATABASE_PORT = env('DATABASE_PORT', '5432')
DATABASE_DATABASE = env('DATABASE_DATABASE', APP_NAME)
DATABASE_USER = env('DATABASE_USER')
DATABASE_PASSWORD = env('DATABASE_PASSWORD')

# Settings redis.
USE_REDIS_STORAGE = env.bool('USE_REDIS_STORAGE', False)
REDIS_HOST = env('REDIS_HOST', '127.0.0.1')
REDIS_PORT = env('REDIS_PORT', '6793')
REDIS_DATABASE = env.int('REDIS_DATABASE', 5)
