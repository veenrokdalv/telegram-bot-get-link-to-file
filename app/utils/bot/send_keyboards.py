from typing import Optional

from aiogram import Bot
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, User
from aiogram.utils.i18n import I18n

import settings
from app.keyboards import reply


async def send_main_keyboard(_: I18n.gettext, user: User, state: FSMContext = None, **kwargs):
    """Moves the user to the main menu.
    If you pass FSM, completing it.

    Parameters
    ----------
    _ :
    user :
    state :
    kwargs :

    Returns
    -------

    """
    bot: Bot = kwargs.get('bot', Bot.get_current())

    if isinstance(state, FSMContext):
        await state.clear()

    keyboard = get_main_keyboard(_, user, locale=kwargs.get('locale'))

    text = _('You have been moved to the main menu.', locale=kwargs.get('locale'))

    await bot.send_message(
        text=text,
        reply_markup=keyboard
    )


def get_main_keyboard(_: I18n.gettext, user: User, **kwargs) -> Optional[ReplyKeyboardMarkup]:
    """Returns the keyboard of the main menu.
    Parameters
    ----------
    _ :
    user :
    kwargs :

    Returns
    -------
    Returns the reply keyboard object.
    """

    # Check user is superuser.
    if user.id in settings.SUPERUSERS_TELEGRAM_ID:
        keyboard = reply.start.superuser_keyboard(_, locale=kwargs.get('locale'))
    else:
        keyboard = reply.start.user_keyboard(_, locale=kwargs.get('locale'))

    return keyboard
