from typing import Union

from aiogram.types import User

from app.utils.helper.language import LanguageCodeType


def username(user_username: Union[str, User], default: str = 'Not user_username') -> str:
    """Formats the user's username.

    Parameters
    ----------
    user_username :
    default : Default value if username is not present.

    Returns
    -------
    Formatted username of the user as a string.
    """
    if isinstance(user_username, User):
        user_username = user_username.username

    if str(user_username) == 'None':
        user_username = default
    else:
        user_username = '@' + user_username

    return user_username


def title_country(locale: str) -> str:
    """Returns the name of the country, by localization.

    Parameters
    ----------
    locale :

    Returns
    -------

    """
    if locale == LanguageCodeType.EN:
        return 'English'
    if locale == LanguageCodeType.RU:
        return 'Россия'
    if locale == LanguageCodeType.BE:
        return 'Беларусь'
    if locale == LanguageCodeType.UK:
        return 'Україна'

    raise ValueError


def country_flag(locale: str) -> str:
    """Returns the flag of the country, by localization.
    
    Parameters
    ----------
    locale : 

    Returns
    -------

    """
    if locale == LanguageCodeType.EN:
        return '🇬🇧'
    if locale == LanguageCodeType.RU:
        return '🇷🇺'
    if locale == LanguageCodeType.BE:
        return '🇧🇾'
    if locale == LanguageCodeType.UK:
        return '🇺🇦'

    raise ValueError
