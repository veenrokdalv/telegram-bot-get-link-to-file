from aiogram import Dispatcher, html, F
from aiogram.types import Message
from aiogram.utils.i18n import I18n

from app.utils.bot.send_keyboards import get_main_keyboard

__all__ = ['setup']


async def help_menu(message: Message, _: I18n.gettext):
    await message.answer(
        text=_(
            f'Help menu\n\n'
            f'My commands.\n'
            f'/help\n'
            f'/settings\n'
            f'/start\n'
        )
    )


def setup(dispatcher: Dispatcher):
    dispatcher.message.register(
        help_menu, F.chat.type == 'private', commands='help',
    )
