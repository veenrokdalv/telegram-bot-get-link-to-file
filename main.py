import datetime as dt
import logging
import os
from zoneinfo import ZoneInfo

from aiogram import Dispatcher, Bot
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.fsm.storage.redis import RedisStorage
from aiogram.dispatcher.fsm.strategy import FSMStrategy
from aiogram.utils.i18n import I18n
from aioredis import Redis
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncConnection, AsyncEngine
from sqlalchemy.orm import sessionmaker

import loggers
import settings
from app import middlewares, filters, handlers
from app.services.repo import Repo
from app.utils.bot import malling_message


async def _on_startup(bots: list[Bot], i18n: I18n, _: I18n.gettext, db_engine: AsyncEngine):
    """Executed before launching bots.

    Parameters
    ----------
    bots :
    i18n :
    _ :
    db_engine :

    Returns
    -------

    """
    # Init models.
    from app import models

    _start_time = settings.START_TIME.astimezone(ZoneInfo(settings.DEFAULT_TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S")

    # Create tables in db.
    async with db_engine.begin() as conn:
        conn: AsyncConnection
        if settings.USE_CLEAR_TABLES:
            await conn.run_sync(models.base.BaseModel.metadata.drop_all)
        await conn.run_sync(models.base.BaseModel.metadata.create_all)

    for bot in bots:
        bot_me = await bot.me()

        if settings.USE_SKIP_UPDATES:
            # Skip updates.
            await bot.get_updates(offset=-1, limit=1)

        for bot_command in settings.BOT_COMMANDS:
            await bot.set_my_commands(
                commands=bot_command['commands'],
                scope=bot_command['scope'],
                language_code=bot_command['locale'],
            )

        # Notify superusers.
        await malling_message.text(
            bot=bot, chat_ids=settings.SUPERUSERS_TELEGRAM_ID,
            message_text=_(
                '<b>Bot started!</>\n\n'
                '<b>My id:</> <code>{bot_me_id}</>\n'
                '<b>My username:</> <i>@{bot_account_username}</>\n'
                '<b>Locale default:</> <i>{default_locale}</>.\n'
                '<b>Available locales:</> <i>{available_locales}</>.\n'
                '<b>Timezone default:</> <i>{default_timezone}</>.\n'
                '<b>Start time:</> <code>{start_time}</>.\n'
            ).format(
                bot_me_id=bot_me.id,
                bot_account_username=bot_me.username,
                default_locale=settings.DEFAULT_LOCALE,
                available_locales=", ".join(i18n.available_locales) or settings.DEFAULT_LOCALE,
                default_timezone=settings.DEFAULT_TIMEZONE,
                start_time=_start_time
            )
        )


async def _on_shutdown(dispatcher: Dispatcher, bots: list[Bot], _: I18n.gettext):
    """Executed before completing bots.

    Parameters
    ----------
    dispatcher :
    bots :
    _ :

    Returns
    -------

    """
    for bot in bots:
        await malling_message.text(
            bot=bot,
            chat_ids=settings.SUPERUSERS_TELEGRAM_ID,
            message_text=_(
                '<b>Bot stopped!</>\n'
                '<b>Time stopped:</> <code>{time_stopped}</>\n'
                '<b>Working time:</> <code>{working_time}</>\n\n'
            ).format(
                time_stopped=dt.datetime.now(ZoneInfo(settings.DEFAULT_TIMEZONE)),
                working_time=str(dt.datetime.utcnow() - settings.START_TIME).split('.')[0]
            )
        )
        try:
            await bot.delete_my_commands()
            await bot.close()
        except Exception as ex:
            continue

    await dispatcher.fsm.storage.close()


if __name__ == '__main__':

    # Create dirs.
    if not os.path.isdir(settings.TMP_DIR):
        os.mkdir(settings.TMP_DIR)
    if not os.path.isdir(settings.LOGS_DIR):
        os.mkdir(settings.LOGS_DIR)
    if not os.path.isdir(f'{settings.LOGS_DIR}/{settings.START_TIME}'):
        os.mkdir(f'{settings.LOGS_DIR}/{settings.START_TIME}')

    loggers.setup()

    # Url db.
    url = (f'postgresql+asyncpg://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:'
           f'{settings.DATABASE_PORT}/{settings.DATABASE_DATABASE}')

    db_engine = create_async_engine(url=url)
    db_session = sessionmaker(bind=db_engine, future=True, class_=AsyncSession, expire_on_commit=False)
    repo = Repo(db_session, db_engine)

    # List bots.
    bots = [
        Bot(token=bot_token, parse_mode='HTML') for bot_token in settings.TELEGRAM_BOT_API_TOKENS
    ]

    # Init memory storage.
    if settings.USE_REDIS_STORAGE:
        redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DATABASE)
        storage = RedisStorage(redis=redis)
    else:
        storage = MemoryStorage()

    dispatcher = Dispatcher(storage=storage, fsm_strategy=FSMStrategy.USER_IN_CHAT, isolate_events=False)

    i18n = I18n(path=settings.LOCALES_DIR, default_locale=settings.DEFAULT_LOCALE, domain=settings.I18N_DOMAIN)

    # Data available in the workflow.
    bot_data = {
        '_': i18n.gettext, 'i18n': i18n, 'repo': repo, 'db_engine': db_engine, 'db_session': db_session
    }

    # Registration of logic before launching bots.
    dispatcher.startup.register(_on_startup)

    # Registering logic before completing bots.
    dispatcher.shutdown.register(_on_shutdown)

    # Registration middlewares, filters, handlers.
    middlewares.setup(dispatcher, i18n=i18n)
    filters.setup(dispatcher)
    handlers.setup(dispatcher)

    try:
        # Start long polling.
        dispatcher.run_polling(*bots, **bot_data)
    except (KeyboardInterrupt, SystemExit):
        logging.warning('Bot stopped!')
    except Exception as ex:
        logging.exception(ex)
