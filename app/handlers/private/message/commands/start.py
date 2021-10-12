from aiogram import Dispatcher, html, F
from aiogram.types import Message
from aiogram.utils.i18n import I18n

__all__ = ['setup']


async def start(message: Message, _: I18n.gettext):
    await message.answer(
        text=_(
            'Hi! {link_to_repo}'
        ).format(link_to_repo=html.link("My repo", "https://github.com/Robot-meow/aiogram-template-bot"))
    )


def setup(dispatcher: Dispatcher):
    dispatcher.message.register(
        start, F.chat.type == 'private', commands='start',
    )
