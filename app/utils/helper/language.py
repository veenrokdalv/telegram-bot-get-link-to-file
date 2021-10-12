from aiogram.utils.helper import Helper, Item, HelperMode


class LanguageCodeType(Helper):
    """Класс языковых кодов"""
    mode = HelperMode.lowercase

    RU = Item()  # ru
    EN = Item()  # en
    BE = Item()  # be
    UK = Item()  # uk
