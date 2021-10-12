from aiogram import Dispatcher

__all__ = ['setup']


def setup(dispatcher: Dispatcher, *args, **kwargs):
    for module in ():
        module.setup(dispatcher, *args, **kwargs)
