from aiogram import Dispatcher

from . import (inline_query, message, callback_query)

__all__ = ['setup']


def setup(dispatcher: Dispatcher, *args, **kwargs):
    for module in (inline_query, message, callback_query):
        module.setup(dispatcher, *args, **kwargs)
