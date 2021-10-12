from aiogram import Dispatcher

from . import (post, )

__all__ = ['setup']


def setup(dispatcher: Dispatcher, *args, **kwargs):
    for module in (post,):
        module.setup(dispatcher, *args, **kwargs)
